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

from .constants import DATE_TIME_FORMAT


def sanitize_csv_field(text):
    if text is None:
        return ''

    return str(text).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace(',', ' ')


def parse_alerts_to_csv(ca_alerts):
    alerts = []
    for alert in ca_alerts:
        entities = []
        entities_descriptions = []
        for hit in alert.hits:
            if 'primary_entity' in hit:
                entities.append(
                    sanitize_csv_field(hit.primary_entity.name)
                ) if hit.primary_entity.name not in entities else None
                entities_descriptions.append(
                    sanitize_csv_field(hit.primary_entity.description)
                ) if hit.primary_entity.description not in entities_descriptions else None

        alerts.append(
            {
                'alert_id': alert.id_,
                'alert_title': alert.title,
                'alert_datetime': alert.log.triggered.strftime(DATE_TIME_FORMAT),
                'alert_status': alert.review.status_in_portal,
                'url_to_portal': str(alert.url.portal),
                'alert_rule_name': alert.rule.name,
                'count_of_hits': len(alert.hits),
                'primary_entities': ' <-> '.join(entities),
                'primary_entities_description': ' <-> '.join(entities_descriptions),
                'ai_insight': sanitize_csv_field(alert.ai_insights.comment),
            }
        )

    if alerts:
        writer = csv.DictWriter(sys.stdout, fieldnames=alerts[0].keys())
        writer.writeheader()
        writer.writerows(alerts)
