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

from psengine.rf_client import RFClient
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .constants import ENTITY_FIELD_MAP, IOCType
from .helpers import get_most_critical_rule


def search_ioc(
    entity_type: str,
    limit: int = 5,
    risk_score: str = None,
    risk_rule: str = None,
    verbose_level: int = 1,
    pretty: bool = False,
):
    """Search for IOCs using the <entity_type>/search endpoint."""
    rf_client = RFClient()

    verbose_level = 1 if pretty else verbose_level
    fields = ENTITY_FIELD_MAP.get(entity_type).get(verbose_level)

    params = {}
    params['limit'] = limit
    if risk_score:
        params['riskScore'] = risk_score

    if risk_rule:
        params['riskRule'] = risk_rule

    params['fields'] = ','.join(fields)

    params = {k: v for k, v in params.items() if v is not None}
    url = f'https://api.recordedfuture.com/v2/{entity_type}/search'

    response = rf_client.request(method='get', url=url, params=params)

    results = response.json()

    if pretty:
        for result in results['data']['results']:
            print(format_line('IOC', result['entity']['name']))
            if entity_type == IOCType.hash:
                print(format_line('Algorithm', result['hashAlgorithm']))
            if entity_type == IOCType.vulnerability:
                print(format_line('Lifecycle', result['lifecycleStage']))
            print(format_line('Risk Score', result['risk']['score']))
            print(format_line('Criticality', result['risk']['criticalityLabel']))

            top_rule = get_most_critical_rule(result['risk']['evidenceDetails'])
            print(format_line('Top Risk Rule', top_rule))

            first_seen = format_time(result['timestamps']['firstSeen'])
            print(format_line('First Seen', first_seen))

            last_seen = format_time(result['timestamps']['lastSeen'])
            print(format_line('Last Seen', last_seen), end='\n\n')

        counts = results.get('counts', {})
        print(
            'Returned {} IOCs out of {}'.format(counts.get('returned', 0), counts.get('total', 0))
        )

    else:
        print_json(json.dumps(results), indent=2)
