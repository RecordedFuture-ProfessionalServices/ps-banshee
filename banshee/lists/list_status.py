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

from psengine.entity_lists import EntityList, ListStatusOut
from rich import print_json

from ..formatters.output_formatters import format_line
from .fetch_list import fetch_list


def fetch_list_status(list_id: str, is_pretty: bool = False):
    entity_list = fetch_list(list_id)
    list_status = entity_list.status()

    if is_pretty:
        _pretty_print(entity_list, list_status)
    else:
        print_json(json.dumps(list_status.json(), indent=2))


def _pretty_print(entity_list: EntityList, list_status: ListStatusOut):
    print(format_line('ID', entity_list.id_))
    print(format_line('Name', entity_list.name))
    print(format_line('Size', list_status.size))
    print(format_line('Status', list_status.status))
