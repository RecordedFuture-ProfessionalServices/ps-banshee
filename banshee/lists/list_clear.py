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

from psengine.helpers import MultiThreadingHelper
from rich.progress import Progress, SpinnerColumn, TextColumn

from .fetch_list import fetch_list

MAX_WORKERS = 50


def clear_list(list_id: str):
    """Clears the list of all entities (text entries can't be removed via API)."""
    with Progress(
        SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True
    ) as progress:
        entity_list = fetch_list(list_id)
        entities = entity_list.entities()

        entities_count = len(entities)

        if entities_count == 0:
            print('No entities to remove')
            return

        task_id = progress.add_task(description=f'Removing {entities_count} entities')
        results = MultiThreadingHelper.multithread_it(
            MAX_WORKERS, lambda e: entity_list.remove(entity=e.entity.id_), iterator=entities
        )

        progress.update(task_id, description='Validating entities have been removed')
        failed = [r.result for r in results if r.result != 'removed']

        if not failed:
            print(f'Successfully removed {entities_count} entities')

        if failed:
            remaining = entity_list.entities()
            print(f'{len(failed)} entities were not removed from the list:')
            for entity in remaining:
                print(f'\t- {entity.entity.id_}, {entity.entity.name}')
