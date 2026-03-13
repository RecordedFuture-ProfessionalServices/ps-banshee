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
import logging

from psengine.playbook_alerts import PACategory, PlaybookAlertMgr
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .constants import RFPAPriority, RFPAStatus

LOG = logging.getLogger('psengine')


def search_alerts(
    created: str,
    updated: str,
    category: PACategory,
    entity: str,
    priority: RFPAPriority,
    status: RFPAStatus,
    limit: int,
    pretty: bool,
):
    """Search functionality for playbook alerts."""
    pa_mgr = PlaybookAlertMgr()
    results = pa_mgr.search(
        created_from=created,
        updated_from=updated,
        category=category,
        entity=entity,
        priority=priority,
        statuses=status,
        max_results=limit,
    )
    if not pretty:
        print_json(json.dumps(results.json()), indent=2)
    else:
        for data in results.data:
            print(format_line('Title', data.title))
            print(format_line('Category', data.category))
            print(format_line('Created', format_time(data.created)))
            print(format_line('Updated', format_time(data.updated)))
            print(format_line('Status', data.status))
            print(format_line('Priority', data.priority))
            print(format_line('Enterprise', data.owner_organisation_details.enterprise_name))
            print(format_line('Alert ID', data.playbook_alert_id))
            print()

        print(f'{results.counts.returned} playbook alert(s)')
