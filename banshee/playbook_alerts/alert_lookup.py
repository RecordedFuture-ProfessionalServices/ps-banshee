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

from psengine.playbook_alerts import PBA_Generic, PlaybookAlertMgr
from psengine.playbook_alerts.errors import PlaybookAlertRetrieveImageError
from rich import print_json
from rich.console import Console
from rich.markdown import Markdown

###############################################################################
# PBA lookup and helper functions
###############################################################################


def output_alert(alert: PBA_Generic, is_pretty: bool):
    if not is_pretty:
        print_json(json.dumps(alert.json()), indent=2)
    else:
        console = Console()
        md = Markdown(alert.markdown(html_tags=False))
        console.print(md)


def lookup_alert(alert_id, is_pretty):
    alert_mgr = PlaybookAlertMgr()

    category = alert_mgr._fetch_alert_category(alert_id)

    try:
        alert = alert_mgr.fetch(alert_id=alert_id, category=category, fetch_images=True)
    except PlaybookAlertRetrieveImageError:
        # Retry but without the image fetching
        alert = alert_mgr.fetch(alert_id=alert_id, category=category, fetch_images=False)

    if alert is not None:
        output_alert(alert, is_pretty)
