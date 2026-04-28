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

import re
from contextlib import suppress
from html import unescape

import polars as pl
from psengine.enrich import EnrichmentLookupError, LookupMgr
from psengine.enrich.models.soar import Evidence
from psengine.risklists import RisklistMgr, RiskListNotAvailableError
from psengine.constants import TIMESTAMP_STR
from pydantic import ValidationError
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from banshee.email import constants
from banshee.email.helpers import IP, URL, HrefExtractor, TARisklist, parse_eml, validate_eml


def _serialize_risk_rule_evidence(evidence: list[Evidence]) -> list[dict]:
    to_return = []
    if evidence:
        parsed = [
            {
                'rule': e.rule,
                'level': e.criticality,
                'timestamp': e.timestamp,
                'evidence_string': e.evidence_string,
            }
            for e in evidence
        ]
        to_return = sorted(parsed, key=lambda x: x['level'], reverse=True)
    return to_return


def empty_error(msg, pretty):
    if pretty:
        print(msg)
    else:
        print([])


def _print_email(df, pretty, console):
    if pretty:
        df = df.rename(
            {
                'ioc': 'IOC',
                'type_': 'Type',
                'location': 'Email Section',
                'risk_score': 'Risk Score',
                'ta_names': 'Threat Actor(s) Name',
                'malwares': 'Related Malware(s)',
                'first_seen': 'First Seen Time',
                'last_seen': 'Last Seen Time',
                'count_of_analyst_notes': 'Count of analyst Notes',
            }
        )
        lines = []
        for row in df.iter_rows(named=True):
            for key, value in row.items():
                if key == 'Risk Score':
                    color = 'red' if value >= 65 else 'yellow' if value >= 25 else 'grey'
                    lines.append(f'{key:>35}: [{color}]{value}[/{color}] \n')
                elif key == 'rule_evidence':
                    if value:
                        lines.append(f'{"Most Malicious Risk Rule":>35}: {value[0]["rule"]} \n')
                        evidence_string = value[0]['evidence_string'].replace('://', '[:]//')
                        lines.append(
                            f'{"Most Malicious Risk Rule Evidence":>35}: {evidence_string} \n'
                        )
                else:
                    row_value = value
                    if isinstance(value, list):
                        row_value = ', '.join(value)
                    if value:
                        lines.append(f'{key:>35}: {row_value} \n')
            lines.append('\n')

        console.print(''.join(lines), markup=True)
        return
    print_json(df.write_json())


def _trim_until_valid(url: str) -> str | None:
    url = constants.URL_TEXT.sub('', url)

    while url:
        with suppress(ValidationError):
            URL(url=url)
            return url

        url = url[:-1]

    return None


def extract_urls_from_body(body: dict[str, str]) -> list[dict[str, str]]:
    entities = []
    already_added = set()

    for content_type, content in body.items():
        candidates = []

        if content_type == 'text/html':
            parser = HrefExtractor()
            parser.feed(content)
            parser.close()
            candidates.extend(parser.hrefs)

            for text_chunk in parser.text_chunks:
                candidates.extend(constants.URL_HTML.findall(unescape(text_chunk)))
        else:
            candidates.extend(constants.URL_HTML.findall(content))

        for url in candidates:
            valid_url = _trim_until_valid(url)

            if valid_url and valid_url not in already_added:
                already_added.add(valid_url)
                entities.append(
                    {
                        'entity': valid_url,
                        'type_': 'url',
                        'location': 'body',
                    }
                )

    return entities


def _extract_entities(headers: dict, body: dict, attachments: dict) -> list[dict]:
    """Takes the parsed sections of an e-mail and extracts entities from them.

    Args:
        headers: list of Key, Value pairs from the header
        body: dict of the emails body/contents ("text/plain" and/or "text/html")
        attachments: list of dicts for names and hashes of the attachments

    Returns:
        A list of dictionaries of the extracted entities. These have the keys:
            "entity", "type" and "location"
    """
    entities = []

    for header_kv in headers:
        if header_kv[0] == 'To' or header_kv[0] == 'From':
            email_domains = re.findall(constants.DOMAIN_FROM_SENDER_STRING, header_kv[1])
            entities.extend(
                {'entity': domain, 'type_': 'domain', 'location': 'header'}
                for domain in email_domains
            )
        else:
            extracted_ip_addresses = re.findall(constants.IP_ADDRESSES, header_kv[1])
            for ip in extracted_ip_addresses:
                with suppress(ValidationError):
                    IP(ip=ip)
                    entities.append({'entity': ip, 'type_': 'ip', 'location': 'header'})

    entities.extend(extract_urls_from_body(body))
    for content_type in body:
        plain_text_domains = re.findall(constants.DOMAINS, body[content_type])
        entities.extend(
            {'entity': domain, 'type_': 'domain', 'location': 'body'}
            for domain in plain_text_domains
        )

    entities.extend(
        {
            'entity': attachment['hash'],
            'type_': 'hash',
            'location': 'attachments/' + attachment['name'],
        }
        for attachment in attachments
    )
    return entities


def _enrich_by_ioc_type(lookup_mgr: LookupMgr, ioc_type: str, entities: list):
    """Takes a list of entities and their type and adds additional context.

    Args:
        lookup_mgr: the PSEngine Manager used for enrichment of IOC's in bulk
        ioc_type: the type of entity
        entities: the list of entities to enrich

    Returns:
        array of dicts that contain the enrichment
    """
    try:
        enriched_iocs = lookup_mgr.lookup_bulk(
            entities,
            ioc_type,
            fields=['links'],
            max_workers=min(30, len(entities)),
        )

    except (ValidationError, EnrichmentLookupError) as err:
        raise err

    return [
        {
            'ioc': ioc.entity,
            'risk_score': ioc.content.risk.score,
            'first_seen': ioc.content.timestamps.first_seen.strftime(TIMESTAMP_STR),
            'last_seen': ioc.content.timestamps.last_seen.strftime(TIMESTAMP_STR),
            'rule_evidence': _serialize_risk_rule_evidence(ioc.content.risk.evidence_details),
            'analyst_notes': ioc.content.analyst_notes,
            'malwares': ioc.links('Actors, Tools & TTPs', 'Malware'),
            'count_of_analyst_notes': len(ioc.content.analyst_notes),
        }
        for ioc in enriched_iocs
        if ioc.is_enriched
    ]


def email_enrich(file_path, pretty, hunt, min_risk_score):
    console = Console()
    lookup_mgr = LookupMgr()
    risklist_mgr = RisklistMgr()

    df = pl.DataFrame()

    with Progress(
        SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True
    ) as progress:
        validate_eml(file_path)

        headers, body, attachments = parse_eml(file_path)

        extracted_entities = _extract_entities(headers, body, attachments)

        df = pl.DataFrame(
            {'ioc': entity['entity'], 'type_': entity['type_'], 'location': entity['location']}
            for entity in extracted_entities
        )
        df = df.unique(subset=['ioc', 'type_', 'location'])

        task_id = progress.add_task(description='Enriching Entities')
        entities_with_context = []
        for ioc_type, rows in df.group_by('type_'):
            enriched = _enrich_by_ioc_type(lookup_mgr, ioc_type[0], rows['ioc'].to_list())
            if enriched:
                entities_with_context.extend(enriched)

        enriched_df = pl.DataFrame(entities_with_context)
        df = df.join(enriched_df, on='ioc', how='left')

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
        df = df.join(ta_risklists, on='ioc', how='left').with_columns(
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

        progress.update(task_id, description='Preparing results')
        df = df.sort('risk_score')

    _print_email(df, pretty, console)
