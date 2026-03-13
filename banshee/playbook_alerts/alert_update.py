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


from collections import defaultdict

import typer
from psengine.playbook_alerts import PlaybookAlertMgr, PlaybookAlertUpdateError
from rich.progress import track

from .constants import RFPAPriority, RFPAReopenStrategy, RFPAStatus


def update_alerts(
    alert_ids: list[str],
    status: RFPAStatus = None,
    reopen_strategy: RFPAReopenStrategy = None,
    priority: RFPAPriority = None,
    comment: str = None,
    assignee: str = None,
):
    _bulk_update_alerts_by_id(
        alert_ids=alert_ids,
        status=status,
        comment=comment,
        reopen_strategy=reopen_strategy,
        priority=priority,
        assignee=assignee,
    )


def _call_update(
    alert_mgr: PlaybookAlertMgr,
    alert_id: str,
    priority: RFPAPriority = None,
    status: RFPAStatus = None,
    comment: str = None,
    reopen_strategy: RFPAReopenStrategy = None,
    assignee: str = None,
):
    if not alert_id.startswith('task:'):
        alert_id = 'task:' + alert_id

    try:
        alert_mgr.update(
            alert_id,
            priority=priority,
            status=status,
            log_entry=comment,
            reopen_strategy=reopen_strategy,
            assignee=assignee,
        ).json()
    except PlaybookAlertUpdateError as err:
        # This bit ugly, must be better way to do this
        if err.__cause__.__cause__.response.status_code == 404:
            return 'NOT FOUND'
        return 'ERROR'

    return 'SUCCESS'


def _bulk_update_alerts_by_id(
    alert_ids: list[str],
    priority: RFPAPriority = None,
    status: RFPAStatus = None,
    comment: str = None,
    reopen_strategy: RFPAReopenStrategy = None,
    assignee: str = None,
):
    alert_mgr = PlaybookAlertMgr()
    results = {}
    for alert_id in track(
        alert_ids, transient=True, description=f'Updating {len(alert_ids)} playbook alerts'
    ):
        results[alert_id] = _call_update(
            alert_mgr=alert_mgr,
            alert_id=alert_id,
            status=status,
            comment=comment,
            reopen_strategy=reopen_strategy,
            assignee=assignee,
            priority=priority,
        )

    # Group by results and print out the IDs
    grouped = defaultdict(list)
    for alert_id, result in results.items():
        grouped[result].append(alert_id)

    for result_type, ids in grouped.items():
        typer.echo(f'{result_type.upper()}:')
        for alert_id in ids:
            typer.echo(alert_id)

    # So we know something failed
    if 'NOT FOUND' in grouped or 'ERROR' in grouped:
        raise typer.Exit(code=1)
