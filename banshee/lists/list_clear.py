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

from .fetch_list import fetch_list
from .list_bulk_remove import bulk_remove_entities


def clear_list(
    list_id: str, note: list[str] | None, exclude_note: list[str] | None, no_note: bool = False
):
    """Clears the list of all entities (text entries can't be removed via API)."""
    entities_list = fetch_list(list_id)
    all_entities = entities_list.entities()

    if note:
        notes_lower = [n.lower() for n in note]
        entities_to_remove = [
            e.entity.id_
            for e in all_entities
            if e.context
            and any(n in str(v).lower() for n in notes_lower for v in e.context.values())
        ]
    elif no_note:
        entities_to_remove = [
            e.entity.id_ for e in all_entities if not e.context or not any(e.context.values())
        ]
    elif exclude_note:
        exclude_lower = [n.lower() for n in exclude_note]
        entities_to_remove = [
            e.entity.id_
            for e in all_entities
            if not e.context
            or not any(n in str(v).lower() for n in exclude_lower for v in e.context.values())
        ]
    else:
        entities_to_remove = [e.entity.id_ for e in all_entities]

    if entities_to_remove:
        bulk_remove_entities(list_id, entities_to_remove)
    else:
        console = Console()
        if note or no_note or exclude_note:
            console.print(f"No matching entities found in '{entities_list.name}'.")
        else:
            console.print(f"The list '{entities_list.name}' is already empty!")
