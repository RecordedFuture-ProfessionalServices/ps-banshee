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
from .errors import EntityNotFoundError


def entity_lookup(
    entity_id: str,
    pretty: bool = False,
):
    match_mgr = EntityMatchMgr()
    results = match_mgr.lookup(entity_id)

    if not results:
        raise EntityNotFoundError(f'Entity ID {entity_id} not found')

    if pretty:
        print(format_line('ID', results.id_))
        print(format_line('Name', results.attributes.name))
        print(format_line('Type', results.type_))
        print(format_line('Threat Actor', results.attributes.is_threat_actor))
        if results.attributes.is_threat_actor:
            print(format_line('Common Names', ', '.join(results.attributes.common_names)))
            print(format_line('Alias', ', '.join(results.attributes.alias)))
    else:
        print_json(json.dumps(results.json()), indent=2)
