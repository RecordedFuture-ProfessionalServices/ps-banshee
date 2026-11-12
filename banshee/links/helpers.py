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
from urllib.parse import quote

from rich.console import Console
from rich.table import Table

from .constants import INTEL_CARD_BASE, PRETTY_IOC_DISPLAY_CAP


def _intel_card_url(ioc) -> str:
    return f'{INTEL_CARD_BASE}/{quote(f"{ioc.id_}", safe="")}'


def _print_search(console: Console, result: dict, enrichment: dict):
    if result.iocs():
        console.print('[bold]Linked IOCs[/bold]', style='dim')
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('IOC', style='bold cyan')
        tbl.add_column('Risk Score', style='bold', width=10)
        tbl.add_column('Top Risk Rule', style='dim')

        for iocs in result.iocs().values():
            for ioc in iocs[:PRETTY_IOC_DISPLAY_CAP]:
                ioc_intel_card = f'[link={_intel_card_url(ioc)}]{ioc.name}[/link]'
                e = enrichment.get(ioc.name)
                enriched = e and e.is_enriched and e.content
                top_risk_rule = (enriched and e.content.risk.rule.most_critical) or 'N/A'
                tbl.add_row(
                    ioc_intel_card,
                    str(ioc.risk_score),
                    top_risk_rule,
                )
        console.print(tbl)
        console.print()

    if result.ttps():
        console.print('[bold]Linked TTPs[/bold]', style='dim')
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('TTP', style='bold cyan')
        tbl.add_column('TTP Name', style='bold')

        for ttp in result.ttps()[:PRETTY_IOC_DISPLAY_CAP]:
            tbl.add_row(
                f'[link={_intel_card_url(ttp)}]{ttp.name}[/link]',
                ttp.display_name,
            )

        console.print(tbl)
        console.print()

    if result.malwares():
        console.print('[bold]Linked Malware[/bold]', style='dim')
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('Malware', style='bold cyan')

        for malware in result.malwares()[:PRETTY_IOC_DISPLAY_CAP]:
            tbl.add_row(
                f'[link={_intel_card_url(malware)}]{malware.name}[/link]',
            )
        console.print(tbl)
        console.print()

    if result.threat_actors():
        console.print('[bold]Linked Threat Actors[/bold]', style='dim')
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('Treat Actor', style='bold cyan')

        for ta in result.threat_actors()[:PRETTY_IOC_DISPLAY_CAP]:
            tbl.add_row(
                f'[link={_intel_card_url(ta)}]{ta.name}[/link]',
            )
        console.print(tbl)
        console.print()
