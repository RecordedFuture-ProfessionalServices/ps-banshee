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

from typing import Union

from psengine.entity_lists import ListApiError
from rich.progress import Progress, SpinnerColumn, TextColumn

from .fetch_list import fetch_list
from .list_helpers import api_error_cause


def add_entity(list_id: str, entity: Union[str, tuple[str, str]], properties: str):
    entity_list = fetch_list(list_id)
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description='Adding entity...')
        context = {}
        if properties:
            for prop in properties.split(','):
                key, value = prop.split('=')
                context[key] = value
        try:
            result = entity_list.add(entity=entity, context=context)
        except ListApiError as err:
            err.message = f"Failed to add entity '{entity}'. {api_error_cause(err)}"
            raise err
        if result.result == 'added':
            print(f'{entity} added')
        elif result.result == 'unchanged':
            print(f'{entity} already in the list')
        elif result.result == 'updated':
            print(f'{entity} updated')
        elif result.result == 'Entity ID not found':
            print(f'{entity} not found, check name and type or use entity ID')
        elif result.result.startswith('Multiple matches found'):
            print(f'Multiple matches found for {entity}, check name and type or use entity ID')
        else:
            print('??? we should not be here')
            print(result.result)
