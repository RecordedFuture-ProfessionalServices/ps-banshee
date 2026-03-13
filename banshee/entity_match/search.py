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

from psengine.entity_match import EntityMatchMgr
from rich import print_json

from ..formatters.output_formatters import format_line
from .constants import EntityType
from .errors import EntityNotFoundError


def entity_search(
    name: str,
    type_: list[EntityType],
    limit: int,
    pretty: bool = False,
):
    match_mgr = EntityMatchMgr()

    type_ = [t.value for t in type_] if type_ else None

    results = match_mgr.match(name, type_, limit)

    if results[0].is_found is False:
        if type_:
            error_msg = f"Entity {name} of type(s) '{', '.join(type_)}' not found"
        else:
            error_msg = f"Entity '{name}' not found"
        raise EntityNotFoundError(error_msg)

    if pretty:
        for result in results:
            print(format_line('ID', result.content.id_))
            print(format_line('Name', result.entity))
            print(format_line('Type', result.content.type_))
            print()
        print(f'{len(results)} entities')
    else:
        results = [entity.json()['content'] for entity in results]
        print_json(json.dumps(results), indent=2)
