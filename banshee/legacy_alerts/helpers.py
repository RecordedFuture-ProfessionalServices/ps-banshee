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

from psengine.classic_alerts.classic_alert import ClassicAlert

from .constants import DATE_TIME_FORMAT


def sanitize_csv_field(text):
    if text is None:
        return ''

    return str(text).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace(',', ' ')


def parse_alerts_to_csv(ca_alerts: list[ClassicAlert]):
    alerts = []
    for alert in ca_alerts:
        entities: list[str] = []
        for hit in alert.hits:
            if hit.primary_entity:
                name = sanitize_csv_field(hit.primary_entity.name)
                if name not in entities:
                    entities.append(name)

        alerts.append(
            {
                'ID': alert.id_,
                'Priority': '',  # Placeholder until the API adds this
                'Alert Rule': alert.rule.name,
                'Status': alert.review.status_in_portal,
                'Created': alert.log.triggered.strftime(DATE_TIME_FORMAT),
                'Updated': '',  # placeholder too if added to the API response
                'Title': alert.title,
                'Assignee': alert.review.assignee,
                'URL': str(alert.url.portal),
                'Entities': '; '.join(entities),
                'Recorded Future AI Insights': sanitize_csv_field(
                    alert.ai_insights.text or alert.ai_insights.comment
                ),
            }
        )

    if alerts:
        writer = csv.DictWriter(sys.stdout, fieldnames=alerts[0].keys())
        writer.writeheader()
        writer.writerows(alerts)
