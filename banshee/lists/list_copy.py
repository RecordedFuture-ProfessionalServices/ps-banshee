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

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .fetch_list import fetch_list
from .list_bulk_add import bulk_add_entities


def copy_list(source_list_id: str, destination_list_id: str, overwrite: bool = False):
    """Copies entities from one list to another."""
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(description='Retrieving entities from source list', total=None)
        entities_list = fetch_list(source_list_id)
        entities_to_copy = [entity.entity.id_ for entity in entities_list.entities()]

    if len(entities_to_copy) > 0:
        bulk_add_entities(
            list_id=destination_list_id, entities=entities_to_copy, overwrite=overwrite
        )
    else:
        console = Console(stderr=True)
        console.print(f"The source list '{entities_list.name}' is empty!")
