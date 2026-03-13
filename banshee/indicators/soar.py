##################################### TERMS OF USE ###########################################
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

import json

from psengine.enrich import EnrichmentSoarError, SoarMgr
from psengine.enrich.soar import SOAREnrichOut
from rich import print_json
from rich.console import Console

from ..formatters.output_formatters import color_risk_score, format_line
from .constants import MAX_ENRICHMENT_WORKERS, IOCType


def soar_enrich(indicators: list[str], entity_type: str, pretty: bool = False) -> None:
    """Bulk SOAR enrichment of a list of IOCs."""
    mgr = SoarMgr()
    kwarg_key = 'hash_' if entity_type == 'hash' else entity_type
    try:
        results = mgr.soar(**{kwarg_key: indicators}, max_workers=MAX_ENRICHMENT_WORKERS)
    except EnrichmentSoarError as err:
        raise err

    if pretty:
        _pretty_print(results, entity_type)
    else:
        if not results:
            print('No results found for the provided IOCs')
        else:
            output = [r.content.json() if r.is_enriched else r.json() for r in results]
            print_json(json.dumps(output), indent=2)


def _pretty_print(results: list[SOAREnrichOut], entity_type: str):
    console = Console()
    for r in results:
        console.print(format_line('IOC', r.entity), highlight=False)
        if r.is_enriched and r.content:
            console.print(format_line('Risk Score', color_risk_score(r.content.risk.score)))
            console.print(format_line('Top Rule', r.content.risk.rule.most_critical or 'N/A'))
            if entity_type == IOCType.vulnerability:
                console.print(format_line('Description', r.content.entity.description))
        else:
            console.print(
                format_line('Status', str(r.content) if r.content else 'Unable to enrich')
            )
        console.print()
