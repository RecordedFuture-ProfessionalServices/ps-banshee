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

import re
import sys
from typing import Annotated

from psengine.helpers import TimeHelpers
from psengine.playbook_alerts import PACategory
from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..playbook_alerts.alert_lookup import lookup_alert
from ..playbook_alerts.alert_search import search_alerts
from ..playbook_alerts.alert_update import update_alerts
from ..playbook_alerts.constants import RFPAPriority, RFPAReopenStrategy, RFPAStatus
from .args import OPT_PRETTY_PRINT
from .epilogs import (
    EPILOG_PBA_LOOKUP,
    EPILOG_PBA_SEARCH,
    EPILOG_PBA_UPDATE,
)

CMD_NAME = 'pba'
CMD_HELP = 'Fetch and manage Playbook Alerts'
CMD_RICH_HELP = 'Recorded Future Playbook Alerts'

app = Typer(no_args_is_help=True)

ALERT_ID_INVALID_MSG = "Alert ID '{}' is not valid. Alert ID should be 36 characters long or 41 characters with 'task:' prefix."  # noqa: E501


###################################
# Callbacks
###################################


def validate_alert_id(alert_id: str):
    if len(alert_id) == 36:
        alert_id = 'task:' + alert_id
    if len(alert_id) != 41 or not alert_id.startswith('task:'):
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


def validate_status_reopen_options(status: RFPAStatus, reopen: RFPAReopenStrategy):
    if status is not None and reopen is not None:
        if status not in [RFPAStatus.Dismissed, RFPAStatus.Resolved]:
            raise BadParameter(
                'Reopen strategy can only be applied to alerts with a status of Dismissed or Resolved.'  # noqa: E501
            )
        if status == RFPAStatus.Dismissed and reopen != RFPAReopenStrategy.Never:
            raise BadParameter(
                'Reopen strategy Never can only be applied to alerts with a status of Dismissed.'
            )
        if status == RFPAStatus.Resolved and reopen not in [
            RFPAReopenStrategy.Never,
            RFPAReopenStrategy.SignificantUpdates,
        ]:
            raise BadParameter(
                'Reopen strategy can only be Never or SignificantUpdates for alerts with a status of Resolved.'  # noqa: E501
            )
    if status is None and reopen is not None:
        raise BadParameter(
            'Reopen strategy can only be applied to alerts with a status of Dismissed or Resolved.'
        )


###################################
# Commands
###################################


@banshee_cmd(app=app, help_='Search for playbook alerts', epilog=EPILOG_PBA_SEARCH)
def search(
    created: Annotated[
        str,
        Option(
            '--created',
            '-C',
            help='Recorded Future Playbook Alert created date to lookup, e.g. 1d',
            show_default=False,
        ),
    ] = None,
    updated: Annotated[
        str,
        Option(
            '--updated',
            '-u',
            help='Recorded Future Playbook Alert updated date to lookup, e.g. 1d',
            show_default=False,
        ),
    ] = None,
    category: Annotated[
        list[PACategory],
        Option(
            '--category',
            '-c',
            help='Recorded Future Playbook Alert category. Default to all categories',
            show_default=False,
        ),
    ] = None,
    entity: Annotated[
        list[str],
        Option(
            '--entity',
            '-e',
            help='Filter alerts by associated entity.',
            show_default=False,
        ),
    ] = None,
    priority: Annotated[
        list[RFPAPriority],
        Option(
            '--priority',
            '-P',
            help='Recorded Future Playbook Alert priority. Default to all priorities',
            show_choices=True,
            show_default=False,
        ),
    ] = None,
    status: Annotated[
        list[RFPAStatus],
        Option(
            '--status',
            '-s',
            help='Recorded Future Playbook Alert status. Default to all statuses',
            show_choices=True,
            show_default=False,
        ),
    ] = None,
    limit: Annotated[
        int,
        Option(
            '--limit',
            '-l',
            help='Limit the number of alerts to return.',
            min=1,
            max=10_000,
        ),
    ] = 100,
    pretty: OPT_PRETTY_PRINT = False,
):
    """Search playbook alerts.

    Args:
        created (str, optional): lookback for created time. Defaults to None
        updated (str, optional): lookback for updated time. Defaults to None
        category (str, optional): lookback for category. Defaults to None
        entity (str, optional): filter by entity. Defaults to None
        priority (str, optional): lookback for priority. Defaults to None
        status (str, optional): lookback for status. Defaults to None
        limit (int, optional): limit total alerts returned. Defaults to 10
        pretty (bool, optional): Pretty print the output. Defaults to False
    """
    created_lookback = TimeHelpers.rel_time_to_date(created) if created is not None else None
    updated_lookback = TimeHelpers.rel_time_to_date(updated) if updated is not None else None
    search_alerts(
        created=created_lookback,
        updated=updated_lookback,
        category=category,
        entity=entity,
        priority=priority,
        status=status,
        limit=limit,
        pretty=pretty,
    )


@banshee_cmd(app=app, help_='Lookup a single playbook alert', epilog=EPILOG_PBA_LOOKUP)
def lookup(
    alert_id: Annotated[
        str, Argument(help='Alert ID to lookup', callback=validate_alert_id, show_default=False)
    ],
    pretty: OPT_PRETTY_PRINT = False,
):
    """Lookup a playbook alert.

    Args:
        alert_id (str): Alert ID to lookup.
        pretty (bool, optional): Pretty print the output. Defaults to False
    """
    lookup_alert(alert_id, pretty)


@banshee_cmd(app=app, help_='Update one or more playbook alerts', epilog=EPILOG_PBA_UPDATE)
def update(
    alert_ids: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more whitespace separated Alert ID',
    ),
    status: Annotated[
        RFPAStatus,
        Option(
            '--status',
            '-s',
            help='New status to set for the alert(s)',
            show_choices=True,
            show_default=False,
        ),
    ] = None,
    reopen_strategy: Annotated[
        RFPAReopenStrategy,
        Option(
            '--reopen',
            '-r',
            help='Reopen strategies can only be applied to alerts with a status of Dismissed or Resolved. The following combinations of status/reopen are allowed: Dismissed -> Never; Resolved -> Never; Resolved -> SignificantUpdates',  # noqa: E501
            show_choices=True,
            show_default=False,
        ),
    ] = None,
    priority: Annotated[
        RFPAPriority,
        Option(
            '--priority',
            '-p',
            help='New priority to set for the alert(s)',
            show_choices=True,
            show_default=False,
        ),
    ] = None,
    comment: Annotated[
        str,
        Option(
            '-t',
            '--comment',
            help='Comment to add to the alert(s), for example: "Bulk resolved via banshee"',
            show_default=False,
        ),
    ] = None,
    assignee: Annotated[
        str,
        Option(
            '--assignee',
            '-a',
            help='New user to assign the alert(s) to. Accepts uhash of the user, for example: uhash:3aXZxdkM12',  # noqa: E501
            show_default=False,
        ),
    ] = None,
):
    """Update one or more playbook alerts.

    Args:
        alert_ids (list[str]): One or more Alert IDs to update.
        status (RFPAStatus, optional): New status to set for the alert(s). Defaults to None.
        reopen_strategy (RFPAReopenStrategy, optional): Reopen strategy to apply. Defaults to None.
        priority (RFPAPriority, optional): New priority to set for the alert(s). Defaults to None.
        comment (str, optional): Comment to add to the alert(s). Defaults to None.
        assignee (str, optional): User uhash to assign the alert(s) to. Defaults to None.
    """
    if alert_ids is None:
        alert_ids = sys.stdin.read()

    parsed_ids = parse_alert_ids_input(alert_ids)
    if status is None and priority is None and comment is None and assignee is None:
        raise BadParameter(
            'At least one of --status, --priority, --comment or --assignee must be provided.'
        )
    validate_status_reopen_options(status, reopen_strategy)
    update_alerts(
        alert_ids=parsed_ids,
        status=status,
        priority=priority,
        comment=comment,
        reopen_strategy=reopen_strategy,
        assignee=assignee,
    )
