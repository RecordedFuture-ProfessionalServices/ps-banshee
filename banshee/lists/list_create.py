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

from psengine.entity_lists import EntityList, EntityListMgr
from rich import print_json
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..formatters.output_formatters import format_line, format_time


def create_list(name: str, list_type: str, pretty: bool):
    list_mgr = EntityListMgr()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description='Creating list', total=None)
        result = list_mgr.create(list_name=name, list_type=list_type)

    if pretty:
        _pretty_print(result)
    else:
        print_json(json.dumps(result.json()), indent=2)


def _pretty_print(payload: EntityList):
    print(format_line('ID', payload.id_))
    print(format_line('Name', payload.name))
    print(format_line('Type', payload.type_))
    print(format_line('Created', format_time(payload.created)))
    print(format_line('Owner', payload.owner_name))
    print(format_line('Enterprise', payload.owner_organisation_details.enterprise_name))
