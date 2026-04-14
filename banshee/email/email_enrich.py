#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

import hashlib
import re
from email.parser import BytesParser
from pathlib import Path

import polars as pl
from psengine.enrich import EnrichmentLookupError, EnrichmentSoarError, LookupMgr, SoarMgr
from psengine.enrich.models.soar import Evidence
from psengine.risklists import RisklistMgr, RiskListNotAvailableError
from pydantic import ValidationError
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from banshee.email import constants
from banshee.email.helpers import TARisklist


def _serialize_risk_rule_evidence(evidence: list[Evidence]) -> list[dict]:
    if not evidence:
        return []
    evidence = sorted(evidence, key=lambda x: x.level, reverse=True)
    return [e.json() for e in evidence]


def empty_error(msg, pretty):
    if pretty:
        print(msg)
    else:
        print([])


def _enrich_by_ioc_type(lookup_mgr: LookupMgr, ioc_type, rows):
    iocs = rows['ioc'].to_list()
    try:
        enriched_iocs = lookup_mgr.lookup_bulk(
            iocs,
            ioc_type,
            fields=['links'],
            max_workers=min(30, len(iocs)),
        )
    except (ValidationError, EnrichmentLookupError) as err:
        raise err

    map_ioc_links = {
        ioc: enriched_data.links('Actors, Tools & TTPs', 'Malware')
        for ioc, enriched_data in zip(iocs, enriched_iocs)
    }
    return pl.DataFrame(
        {'ioc': list(map_ioc_links.keys()), 'malwares': list(map_ioc_links.values())},
        schema={
            'ioc': pl.String,
            'malwares': pl.List(pl.String),
        },
    )


def _print_email(df, pretty, console):
    if pretty:
        df = df.rename(
            {
                'ioc': 'IOC',
                'location': 'Email Section',
                'risk_score': 'Risk Score',
                'most_malicious_rule': 'Most Malicious Risk Rule',
                'ta_names': 'Threat Actor(s) Name',
                'malwares': 'Related Malware(s)',
            }
        )
        lines = []
        for row in df.iter_rows(named=True):
            for key, value in row.items():
                if key == 'Risk Score':
                    color = 'red' if value >= 65 else 'yellow' if value >= 25 else 'grey'
                    lines.append(f'{key:>25}: [{color}]{value}[/{color}] \n')
                elif key == 'rule_evidence':
                    continue
                else:
                    row_value = value
                    if isinstance(value, list):
                        row_value = ', '.join(value)
                    if value:
                        lines.append(f'{key:>25}: {row_value} \n')
            lines.append('\n')

        console.print(''.join(lines), markup=True)
        return
    print_json(df.write_json())


def _parse_eml(eml_path: Path) -> tuple[tuple, dict, dict[str, str]]:
    """Parses the EML into three lists.

    Returns:
        tuple of header keys and values
        dict of the types and the contents. The body can have both HTML and plain text.
        list of the attachment hashes
    """
    with Path.open(eml_path, 'rb') as f:
        parsed_email = BytesParser().parse(f)

        headers = [[key, value] for key, value in parsed_email.items()]

        body = {}
        attachments = []
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            content_disposition = part.get_content_disposition()

            if content_type == 'text/plain' or content_type == 'text/html':
                body[content_type] = part.get_payload(decode=True).decode(
                    part.get_content_charset(), errors='replace'
                )

            elif content_disposition == 'attachment':
                attachment_name = part.get_filename()
                attachment_content = part.get_payload(decode=True)
                sha265 = hashlib.sha256(attachment_content).hexdigest()
                attachments.append({'name': attachment_name, 'hash': sha265})

    return (headers, body, attachments)


def _extract_entities(headers: dict, body: dict, attachments: dict) -> list[dict]:
    """Takes the parsed sections of an e-mail and extracts entities from them.

    Returns:
        A dataframe of the entities extracted
    """
    entities = []

    for header_kv in headers:
        if header_kv[0] == 'To' or header_kv[0] == 'From':
            email_domains = re.findall(constants.DOMAIN_FROM_SENDER_STRING, header_kv[1])
            entities.extend(
                {'entity': domain, 'type': 'domain', 'location': 'header'}
                for domain in email_domains
            )
        else:
            extracted_ip_addresses = re.findall(constants.IP_ADDRESSES, header_kv[1])
            entities.extend(
                {'entity': ip, 'type': 'ip', 'location': 'header'} for ip in extracted_ip_addresses
            )

    for content_type in body:
        plain_text_urls = re.findall(constants.URL_ADDRESSES, body[content_type])
        entities.extend(
            {'entity': url, 'type': 'url', 'location': 'body'} for url in plain_text_urls
        )

        plain_text_domains = re.findall(constants.DOMAINS, body[content_type])
        entities.extend(
            {'entity': domain, 'type': 'domain', 'location': 'body'}
            for domain in plain_text_domains
        )

    entities.extend(
        {
            'entity': attachment['hash'],
            'type': 'hash',
            'location': 'attachments/' + attachment['name'],
        }
        for attachment in attachments
    )

    return entities


def email_enrich(file_path, pretty, hunt, min_risk_score):
    console = Console()
    lookup_mgr = LookupMgr()
    soar_mgr = SoarMgr()
    risklist_mgr = RisklistMgr()

    df = pl.DataFrame()

    with Progress(
        SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True
    ) as progress:
        task_id = progress.add_task('Parsing EML file')
        headers, body, attachments = _parse_eml(file_path)

        progress.update(task_id, description='Extracting Entities')
        extracted_entities = _extract_entities(headers, body, attachments)

        progress.update(task_id, description='Building Entities Dataframe')
        entities_df = pl.DataFrame(
            {'ioc': entity['entity'], 'type': entity['type'], 'location': entity['location']}
            for entity in extracted_entities
        )
        entities_df = entities_df.unique(subset=['ioc', 'type', 'location'])

        progress.update(task_id, description='Enriching Entities')
        try:
            ips = entities_df.filter(pl.col('type') == 'ip')['ioc'].to_list()
            domains = entities_df.filter(pl.col('type') == 'domain')['ioc'].to_list()
            hashes = entities_df.filter(pl.col('type') == 'hash')['ioc'].to_list()
            urls = entities_df.filter(pl.col('type') == 'url')['ioc'].to_list()
            iocs = soar_mgr.soar(ip=ips, domain=domains, hash_=hashes, url=urls)
        except (EnrichmentSoarError, ValidationError) as err:
            raise err

        progress.update(task_id, description='Filtering results')
        iocs = pl.DataFrame(
            {
                'ioc': ioc.entity,
                'type_': ioc.content.entity.type_,
                'risk_score': ioc.content.risk.score,
                'most_malicious_rule': ioc.content.risk.rule.most_critical,
                'rule_evidence': _serialize_risk_rule_evidence(ioc.content.risk.rule.evidence),
            }
            for ioc in iocs
        )

        progress.update(task_id, description='Merging Dataframes')
        iocs = iocs.join(entities_df, on='ioc', how='inner')

        progress.update(task_id, description='Fetching Risk Lists')
        try:
            ip_ta_risklist = pl.DataFrame(
                [
                    v.json()
                    for v in risklist_mgr.fetch_risklist(constants.TA_IP_LIST, validate=TARisklist)
                ]
            )
            domain_ta_risklist = pl.DataFrame(
                [
                    v.json()
                    for v in risklist_mgr.fetch_risklist(
                        constants.TA_DOMAIN_LIST, validate=TARisklist
                    )
                ]
            )

        except (RiskListNotAvailableError, ValidationError) as err:
            raise err

        ta_risklists = pl.concat([ip_ta_risklist, domain_ta_risklist])
        df = iocs.join(ta_risklists, on='ioc', how='left').with_columns(
            pl.col('ta_names').fill_null(pl.lit([], dtype=pl.List(pl.Utf8)))
        )

        if hunt:
            df = df.filter(
                (pl.col('risk_score') >= min_risk_score) | (pl.col('ta_names').list.len() > 0)
            )
        else:
            df = df.filter(pl.col('risk_score') >= min_risk_score)

        if len(df) == 0:
            empty_error(
                f'No indicators above the risk score threshold of {min_risk_score} found', pretty
            )
            return

        progress.update(task_id, description='Fetching additional information')
        entities_with_links = [
            _enrich_by_ioc_type(lookup_mgr, ioc_type[0], rows)
            for ioc_type, rows in df.group_by('type_')
        ]

        progress.update(task_id, description='Preparing results')

        malwares_all = pl.concat(entities_with_links)
        df = df.join(malwares_all, on='ioc', how='left')

        df.drop_in_place('type_')
        df = df.sort('risk_score')

    _print_email(df, pretty, console)
