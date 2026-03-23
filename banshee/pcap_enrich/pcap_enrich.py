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

import ipaddress
from collections import defaultdict
from contextlib import suppress
from pathlib import Path

import polars as pl
import pyshark
from psengine.enrich import EnrichmentLookupError, EnrichmentSoarError, LookupMgr, SoarMgr
from psengine.enrich.models.soar import Evidence
from psengine.risklists import RisklistMgr, RiskListNotAvailableError
from pydantic import ValidationError
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from banshee.pcap_enrich.constants import MAX_WORKERS, TA_DOMAIN_LIST, TA_IP_LIST
from banshee.pcap_enrich.helpers import TARisklist


def _serialize_risk_rule_evidence(evidence: list[Evidence]) -> list[dict]:
    if not evidence:
        return []
    evidence = sorted(evidence, key=lambda x: x.level, reverse=True)
    return [e.json() for e in evidence]


def _extract_entities_from_capture(
    capture_file: Path,
) -> tuple[list[str], list[str], dict[str, list]]:
    """Extract entities from pcap.

    Returns:
        list of dedup ips (IPv4 and IPv6)
        list of dedup domains
        dict of key a domain and value a set of IPv4 resolved for that domain via DNS.
    """
    ips = []
    dns_resolutions = defaultdict(set)
    ipv4, ipv6, domains = set(), set(), set()

    caps = pyshark.FileCapture(capture_file, keep_packets=False)
    for pkt in caps:
        with suppress(AttributeError):
            ipv4.add(pkt.ip.src)
            ipv4.add(pkt.ip.dst)

        with suppress(AttributeError):
            ipv6.add(pkt.ipv6.src)
            ipv6.add(pkt.ipv6.dst)

        if 'DNS' in pkt:
            with suppress(AttributeError):
                qry = pkt.dns.qry_name
                if qry:
                    if isinstance(qry, (list, tuple)):
                        for q in qry:
                            if q:
                                domains.add(str(q))
                                if hasattr(pkt.dns, 'a') and pkt.dns.a:
                                    dns_resolutions[q].add(pkt.dns.a)
                    else:
                        domains.add(str(qry))
                        if hasattr(pkt.dns, 'a') and pkt.dns.a:
                            dns_resolutions[str(qry)].add(pkt.dns.a)

    caps.close()

    ips = [x for x in ipv4.union(ipv6) if x and ipaddress.ip_address(x).is_global]
    domains = [x for x in domains if x]

    return ips, domains, dns_resolutions


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


def _wireshark_query(ioc, ioc_type, dns_resolutions):
    if ioc_type == 'IpAddress':
        return f'ip.src == {ioc} or ip.dst == {ioc}'

    ips = dns_resolutions.get(ioc)
    if ips:
        return ' && '.join(f'ip.src == {ip} or ip.dst == {ip}' for ip in ips)
    return ''


def _print_capture(df, pretty, console):
    if pretty:
        df = df.rename(
            {
                'ioc': 'IOC',
                'risk_score': 'Risk Score',
                'most_malicious_rule': 'Most Malicious Risk Rule',
                'ta_names': 'Threat Actor(s) Name',
                'malwares': 'Related Malware(s)',
                'wireshark_query': 'Wireshark Query',
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


def empty_error(msg, pretty):
    if pretty:
        print(msg)
    else:
        print([])


def pcap_enrich(capture_file: Path, pretty: bool, hunt: bool, min_risk_score: int):
    """Enrich the capture."""
    console = Console(highlighter=None)
    soar_mgr = SoarMgr()
    lookup_mgr = LookupMgr()
    risklist_mgr = RisklistMgr()
    df = pl.DataFrame()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description='Extracting network indicators')
        ips, domains, dns_resolutions = _extract_entities_from_capture(capture_file)
        if not (len(ips) or len(domains)):
            empty_error('No IPs or domains extracted from the capture.', pretty)
            return

        progress.update(task_id, description='Enriching indicators')
        try:
            iocs = soar_mgr.soar(ip=ips, domain=domains, max_workers=MAX_WORKERS)
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

        try:
            ip_ta_risklist = pl.DataFrame(
                [v.json() for v in risklist_mgr.fetch_risklist(TA_IP_LIST, validate=TARisklist)]
            )
            domain_ta_risklist = pl.DataFrame(
                [v.json() for v in risklist_mgr.fetch_risklist(TA_DOMAIN_LIST, validate=TARisklist)]
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

        df = df.with_columns(
            pl.struct(['ioc', 'type_'])
            .map_elements(
                lambda row: _wireshark_query(row['ioc'], row['type_'], dns_resolutions),
                return_dtype=pl.String,
            )
            .alias('wireshark_query')
        )

        df.drop_in_place('type_')
        df = df.sort('risk_score')

    _print_capture(df, pretty, console)
