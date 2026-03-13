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

from psengine.entity_lists import ListEntity
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .fetch_list import fetch_list


def fetch_entities(list_id: str, pretty: bool):
    entity_list = fetch_list(list_id)
    entities = entity_list.entities()

    if pretty:
        _pretty_print(entities)
    else:
        entities_json = [entity.json() for entity in entities]
        print_json(json.dumps(entities_json), indent=2)


def _pretty_print(entities: list[ListEntity]):
    for entity in entities:
        print(format_line('ID', entity.entity.id_))
        print(format_line('Name', entity.entity.name))
        print(format_line('Type', entity.entity.type_))
        print(format_line('Added', format_time(entity.added)))
        print()
    print()
    print(f'Total entities: {len(entities)}')
