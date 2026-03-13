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

from psengine.enrich import EnrichmentData, EnrichmentLookupError, LookupMgr
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .constants import ENTITY_FIELD_MAP, MAX_ENRICHMENT_WORKERS, IOCType
from .helpers import get_most_critical_rule


def lookup_ioc(
    indicators: list[str],
    entity_type: str = 'ip',
    verbose_level: int = 1,
    pretty: bool = False,
    ai_insights: bool = False,
) -> None:
    """Lookup of IOC and print info retrieved."""
    lookup_mgr = LookupMgr()
    verbose_level = 1 if pretty else verbose_level

    fields = ENTITY_FIELD_MAP.get(entity_type).get(verbose_level) + (
        ['aiInsights'] if ai_insights else []
    )
    try:
        lookup_results = lookup_mgr.lookup_bulk(
            entity=indicators,
            entity_type=entity_type,
            fields=fields,
            max_workers=MAX_ENRICHMENT_WORKERS,
        )
    except EnrichmentLookupError as err:
        if err.__cause__.response is not None:
            err.message = (
                str(err.__cause__.response.status_code)
                + ' status received from lookup. Verify settings and try again.'
            )
            raise err
        err.message = (
            type(err.__cause__).__name__ + ' received from lookup. Verify settings and try again.'
        )
        raise err

    if pretty:
        _pretty_print(lookup_results)
    else:
        if len(lookup_results) == 0:
            print('No results found for the provided IOCs')
        else:
            results = [
                ioc.content.json() if ioc.is_enriched else ioc.json() for ioc in lookup_results
            ]
            print_json(json.dumps(results), indent=2)


def _pretty_print(lookup_results: list[EnrichmentData]):
    """Print human readbale output of enriched ioc."""
    for ioc in lookup_results:
        if ioc.is_enriched:
            print(format_line('IOC', ioc.entity))
            if ioc.entity_type == IOCType.hash:
                print(format_line('Algorithm', ioc.content.hash_algorithm))
            if ioc.entity_type == IOCType.vulnerability:
                print(format_line('Lifecycle', ioc.content.lifecycle_stage))
            print(format_line('Risk Score', ioc.content.risk.score))
            print(format_line('Criticality', ioc.content.risk.criticality_label))
            print(
                format_line(
                    'Top Risk Rule', get_most_critical_rule(ioc.content.risk.evidence_details)
                )
            )
            print(format_line('First Seen', format_time(ioc.content.timestamps.first_seen)))
            print(format_line('Last Seen', format_time(ioc.content.timestamps.last_seen)))
            if ioc.content.ai_insights:
                print(format_line('AI Insights', ioc.content.ai_insights.text))
        else:
            print(format_line('IOC', ioc.entity))
            print(format_line('Status', ioc.content))
        print()
