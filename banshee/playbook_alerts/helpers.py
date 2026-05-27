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

import csv
import sys

from psengine.playbook_alerts.constants import PLAYBOOK_ALERT_TYPE

from .constants import DATE_TIME_FORMAT

CSV_FIELDNAMES = (
    'ID',
    'Priority',
    'Alert Rule',
    'Status',
    'Created',
    'Updated',
    'Title',
    'Assignee',
    'Entities',
    'Reopen Strategy',
    'Onwards Actions',
)


def sanitize_csv_field(text):
    if text is None:
        return ''

    return str(text).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')


def parse_targets(targets: list):
    target_entities = []
    for entity in targets:
        name = entity.name if hasattr(entity, 'name') else entity.removeprefix('idn:')
        if name not in target_entities:
            target_entities.append(name)
    return target_entities


def parse_alerts_to_csv(pba_alerts: list[PLAYBOOK_ALERT_TYPE]):
    writer = csv.DictWriter(sys.stdout, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()
    for alert in pba_alerts:
        alert_entities = parse_targets(alert.panel_status.targets)

        if alert_entities:
            if len(alert_entities) > 1:
                alert_title = f'{alert_entities[0]} +{len(alert_entities)}'
            else:
                alert_title = str(alert_entities[0])
        else:
            alert_title = alert.panel_status.alert_rule.name

        writer.writerow(
            {
                'ID': alert.playbook_alert_id,
                'Priority': alert.panel_status.priority,
                'Alert Rule': sanitize_csv_field(
                    alert.panel_status.alert_rule.name or alert.panel_status.alert_rule.label
                ),
                'Status': alert.panel_status.status,
                'Created': alert.panel_status.created.strftime(DATE_TIME_FORMAT),
                'Updated': alert.panel_status.updated.strftime(DATE_TIME_FORMAT),
                'Title': sanitize_csv_field(alert_title),
                'Assignee': sanitize_csv_field(alert.panel_status.assignee_name),
                'Entities': '; '.join(alert_entities),
                'Reopen Strategy': sanitize_csv_field(
                    alert.panel_status.reopen if hasattr(alert.panel_status, 'reopen') else ''
                ),
                'Onwards Actions': sanitize_csv_field(
                    '; '.join(alert.panel_status.actions_taken or [])
                ),
            }
        )
