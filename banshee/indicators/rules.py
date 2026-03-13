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

from psengine.endpoints import CONNECT_API_BASE_URL
from psengine.rf_client import RFClient
from rich import print as rich_print
from rich import print_json

from ..formatters.output_formatters import format_line


def search_ioc_rules(
    entity_type: str, freetext: str, mitre_code: str, criticality: int, pretty: bool
):
    """Search IOC rules."""
    rf_client = RFClient()
    rules = rf_client.request(
        method='get', url=f'{CONNECT_API_BASE_URL}/{entity_type}/riskrules'
    ).json()
    rules = rules['data']['results']

    rules = _filter_rules(rules, freetext, mitre_code, criticality)

    if pretty:
        _pretty_print(rules)
    else:
        if len(rules) == 0:
            print_json(json.dumps([]), indent=2)
        else:
            print_json(json.dumps(rules), indent=2)


def _filter_rules(rules: dict, freetext: str, mitre_code: str, criticality: int):
    if freetext:
        rules = [
            rule
            for rule in rules
            if freetext.lower() in rule['description'].lower()
            or freetext.lower() in rule['name'].lower()
        ]

    if mitre_code:
        rules = [
            rule
            for rule in rules
            if any(
                mitre_code.lower() in category['name'].lower()
                for category in rule.get('categories', [])
            )
        ]

    if criticality is not None:
        rules = [rule for rule in rules if rule['criticality'] == criticality]

    # Sort the rules by criticality
    return sorted(rules, key=lambda x: x['criticality'], reverse=True)


def _pretty_print(rules: dict):
    for rule in rules:
        print(format_line('Name', rule['name']))
        print(format_line('Description', rule['description']))
        print(format_line('Criticality', f'{rule["criticality"]} ({rule["criticalityLabel"]})'))
        if rule['count'] == 0:
            rich_print(format_line('IOC Count', '[red]0[/red]'))
        else:
            rich_print(format_line('IOC Count', f'[cyan]{rule["count"]}[/cyan]'))
        print('')  # noqa: FURB105

    print(f'Total {len(rules)} rules found')
