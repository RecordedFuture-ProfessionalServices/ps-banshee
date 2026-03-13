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

from psengine.classic_alerts import ClassicAlert, ClassicAlertMgr
from rich import print_json
from rich.console import Console
from rich.markdown import Markdown


def lookup_alert(id_: str, pretty: bool):
    alert_mgr = ClassicAlertMgr()

    alert = alert_mgr.fetch(id_)

    if pretty:
        _pretty_print(alert)
    else:
        print_json(json.dumps(alert.json()), indent=2)


def _pretty_print(alert: ClassicAlert):
    console = Console()
    md = Markdown(alert.markdown(fragment_entities=False, html_tags=False))
    console.print(md)

    return
