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
import re
import sys
from typing import Annotated

from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..legacy_alerts.alert_lookup import bulk_lookup_alerts, lookup_alert
from ..legacy_alerts.alert_search import search_alerts
from ..legacy_alerts.alert_update import update_alerts
from ..legacy_alerts.constants import AlertStatus
from ..legacy_alerts.rules_search import search_alert_rules
from .args import OPT_PRETTY_PRINT
from .epilogs import (
    EPILOG_ALERT_BULK_LOOKUP,
    EPILOG_ALERT_LOOKUP,
    EPILOG_ALERT_RULES_SEARCH,
    EPILOG_ALERT_SEARCH,
    EPILOG_ALERT_UPDATE,
)

CMD_NAME = 'ca'
CMD_HELP = 'Search and lookup Classic Alerts'
CMD_RICH_HELP = 'Recorded Future Classic Alerts'

app = Typer(no_args_is_help=True)

ALERT_ID_INVALID_MSG = "Alert ID '{}' is not valid. Alert ID should be at least 6 characters long."  # noqa: E501

###################################
# Callbacks
###################################


def validate_alert_id(alert_id: str):
    # if value is less than 6 char long
    if len(alert_id) < 6:
        raise BadParameter(ALERT_ID_INVALID_MSG.format(alert_id))

    return alert_id


def parse_alert_ids_input(value: list[str]):
    if not value:
        raise BadParameter('No Alert IDs supplied')

    alert_ids = value
    if isinstance(value, str):
        alert_ids = [x for x in re.split(r'[\s]+', value) if x]

        if not len(alert_ids):
            raise BadParameter('No Alert IDs provided')

    # Now check that each ID is valid
    for alert_id in alert_ids:
        validate_alert_id(alert_id)

    return alert_ids


def parse_triggered(value: str):
    if not value.startswith('[') and not value.startswith('('):
        value = f'-{value.strip()}'

    return value


def parse_search_alerts(value: str):
    if not value:
        raise BadParameter('No Alert data supplied')

    try:
        alerts = json.loads(value)
    except json.JSONDecodeError as err:
        raise BadParameter('Invalid JSON supplied') from err

    alert_ids = [alert['id'] for alert in alerts]

    for alert_id in alert_ids:
        validate_alert_id(alert_id)

    return alert_ids


###################################
# Commands
###################################


@banshee_cmd(app=app, help_='Lookup a single Classic Alert', epilog=EPILOG_ALERT_LOOKUP)
def lookup(
    alert_id: Annotated[
        str, Argument(help='Alert ID to lookup', callback=validate_alert_id, show_default=False)
    ],
    pretty: OPT_PRETTY_PRINT = False,
):
    lookup_alert(id_=alert_id, pretty=pretty)


@banshee_cmd(app=app, help_='Lookup multiple Classic Alerts', epilog=EPILOG_ALERT_BULK_LOOKUP)
def bulk_lookup(
    csv_flag: Annotated[
        bool,
        Option(
            '--csv', help='Output the result as CSV, Using predefined fields', show_default=False
        ),
    ] = False,
):
    if sys.stdin.isatty():
        raise BadParameter(
            'This command only accepts piped input. Usage: banshee ca search | banshee ca bulk-lookup'  # noqa: E501
        )

    raw_alerts = sys.stdin.read().strip()

    alert_ids = parse_search_alerts(raw_alerts)

    bulk_lookup_alerts(alert_ids=alert_ids, csv_flag=csv_flag)


@banshee_cmd(app=app, help_='Search for Classic Alerts', epilog=EPILOG_ALERT_SEARCH)
def search(
    triggered: Annotated[
        str,
        Option(
            '--triggered',
            '-t',
            callback=parse_triggered,
            help='Filter on triggered time, e.g. 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)',  # noqa: E501
            show_default=True,
        ),
    ] = '1d',
    alert_rules: Annotated[
        list[str],
        Option('--rule', '-r', help='Filter by an alert rule name (freetext)', show_default=False),
    ] = None,
    status: Annotated[
        AlertStatus, Option('-s', '--status', help='Filter by alert status', show_default=False)
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_alerts(triggered=triggered, alert_rules=alert_rules, status=status, pretty=pretty)


@banshee_cmd(app=app, help_='Search Classic Alert rules', epilog=EPILOG_ALERT_RULES_SEARCH)
def rules(
    freetext: Annotated[str, Argument(help='Freetext to search in alert rules')] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_alert_rules(pretty=pretty, freetext=freetext)


@banshee_cmd(app=app, help_='Update a classic alert', epilog=EPILOG_ALERT_UPDATE)
def update(
    alert_ids: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more whitespace separated Alert ID',
    ),
    status: Annotated[
        AlertStatus, Option('-s', '--status', help='New alert status', show_default=False)
    ] = None,
    note: Annotated[str, Option('-n', '--note', help='Add a text note', show_default=False)] = None,
    note_append: Annotated[
        bool,
        Option(
            '-A',
            '--append',
            help='Append to the existing text note, instead of overwriting it.',
            show_default=True,
        ),
    ] = False,
    assignee: Annotated[
        str,
        Option(
            '--assignee',
            '-a',
            help='New user to assign the alert(s) to. Accepts uhash or email address of the user, for example: uhash:3aXZxdkM12; analyst@acme.com',  # noqa: E501
            show_default=False,
        ),
    ] = None,
):
    if alert_ids is None:
        alert_ids = sys.stdin.read()

    parsed_ids = parse_alert_ids_input(alert_ids)

    if status is None and note is None and assignee is None:
        raise BadParameter('At least one of --status, --note or --assignee must be privded.')

    if note_append and note is None:
        raise BadParameter('note argument must be provided when append option is set')

    update_alerts(
        alert_ids=parsed_ids, status=status, note=note, note_append=note_append, assignee=assignee
    )
