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

from psengine.entity_lists import EntityList
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .fetch_list import fetch_list


def fetch_list_info(list_id: str, pretty: bool):
    entity_list = fetch_list(list_id)

    if pretty:
        _pretty_print(entity_list)
    else:
        print_json(json.dumps(entity_list.json()), indent=2)


def _pretty_print(entity_list: EntityList):
    print(format_line('ID', entity_list.id_))
    print(format_line('Name', entity_list.name))
    print(format_line('Type', entity_list.type_))
    print(format_line('Created', format_time(entity_list.created)))
    print(format_line('Updated', format_time(entity_list.updated)))
    print(format_line('Owner', entity_list.owner_name))
    print(format_line('Enterprise', entity_list.owner_organisation_details.enterprise_name))
