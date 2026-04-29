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


def search_lists(name: str, list_type: str, limit: int, pretty: bool):
    list_mgr = EntityListMgr()
    search_params = {'max_results': limit}

    if name is not None:
        search_params['list_name'] = name

    if list_type is not None:
        search_params['list_type'] = list_type
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description='Searching for lists', total=None)
        results = list_mgr.search(**search_params)

    if pretty:
        _pretty_print(results)
    else:
        alerts_json = [alert.json() for alert in results]
        print_json(json.dumps(alerts_json), indent=2)


def _pretty_print(results: list[EntityList]):
    for list_ in results:
        print(format_line('ID', list_.id_))
        print(format_line('Name', list_.name))
        print(format_line('Type', list_.type_))
        print(format_line('Created', format_time(list_.created)))
        print(format_line('Updated', format_time(list_.updated)))
        print(format_line('Owner', list_.owner_name))
        print(format_line('Enterprise', list_.owner_organisation_details.enterprise_name))
        print()
    print(f'{len(results)} list(s)')
