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

import sys

import typer
from psengine.classic_alerts import (
    AlertUpdateError,
    ClassicAlertMgr,
)
from requests.exceptions import HTTPError
from rich.progress import Progress, SpinnerColumn, TextColumn

from .constants import AlertStatus


def update_alerts(
    alert_ids: list[str],
    status: AlertStatus,
    note: str,
    note_append: bool = None,
    assignee: str = None,
):
    alert_mgr = ClassicAlertMgr()
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description=f'Updating {len(alert_ids)} classic alerts', total=None)
        payload = []
        for alert in alert_ids:
            entry = {'id': alert}

            if status:
                entry['statusInPortal'] = status.value

            if note:
                entry['note'] = note
                if note_append:
                    fetched_alert = alert_mgr.fetch(id_=alert, fields=['review'])
                    if fetched_alert.review.note is not None:
                        entry['note'] = f'{fetched_alert.review.note}. {note}'

            if assignee:
                entry['assignee'] = assignee

            payload.append(entry)

        try:
            updated = alert_mgr.update(payload)
        except (ValueError, AttributeError, HTTPError, AlertUpdateError) as err:
            raise AlertUpdateError(
                'Failed to update alert(s). Please check the input parameters and try again.'
            ) from err

    _print_bulk_update_results(updated)


def _print_bulk_update_results(updated):
    for key in ['success', 'error']:
        alerts = updated.get(key, [])
        if alerts:
            typer.echo(f'{key.upper()}:')
            for alert in alerts:
                typer.echo(alert.get('id'))

    # If at least on alert failed, then exit with non zero code
    if len(updated.get('error', [])):
        sys.exit(1)
