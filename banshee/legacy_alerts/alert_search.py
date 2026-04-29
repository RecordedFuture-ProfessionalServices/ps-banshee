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


import json

from psengine.classic_alerts import ClassicAlert, ClassicAlertMgr, NoRulesFoundError
from rich import print_json
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..formatters.output_formatters import format_line, format_time
from ..legacy_alerts.constants import AlertStatus


def search_alerts(triggered: str, alert_rules: str, status: AlertStatus, pretty: bool):
    """Search functionality for Legacy alerts."""
    alert_mgr = ClassicAlertMgr()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        rule_ids = []
        if alert_rules:
            progress.add_task(description='Searching for Classic Alerts rules', total=None)
            rule_ids = [
                rule.id_ for rule in alert_mgr.fetch_rules(freetext=alert_rules, max_results=1000)
            ]
            if not rule_ids:
                raise NoRulesFoundError(f'No matching rules found for rule IDs: {alert_rules}')

        if progress.task_ids:
            progress.remove_task(progress.task_ids[0])
        progress.add_task(description='Searching for Classic Alerts')
        results = alert_mgr.search(
            triggered=triggered,
            status=status,
            rule_id=rule_ids or None,
            fields=['owner_organisation_details', 'title', 'id', 'log', 'review'],
            max_results=1000,
        )

        # deduplicate the alerts as _fetch_triggered_alerts returns dups
        # when multiple rules are passed
        results = list({alert.id_: alert for alert in results}.values())

    if pretty:
        _pretty_print(results)
    else:
        alerts_json = [alert.json() for alert in results]
        print_json(json.dumps(alerts_json), indent=2)


def _pretty_print(results: list[ClassicAlert]):
    for alert in results:
        print(format_line('Title', alert.title))

        triggered = format_time(alert.log.triggered)
        print(format_line('Triggered', triggered))
        print(format_line('Status', alert.review.status_in_portal))
        print(
            format_line(
                'Owner',
                alert.owner_organisation_details.enterprise_name,
            )
        )
        print(format_line('Alert ID', alert.id_))

        print()

    print(f'Total {len(results)} alerts found')
