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

from psengine.links import LinksMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


def search_links(
    entity_ids: list[str],
    return_entity_types: list[str],
    source: str,
    sections: list[str],
    timeframe: str,
    events: list[str],
    connected_entities: list[str],
    limit_per_type: int,
    search_scope: str,
    pretty: bool,
):
    """Search for links between given entities."""
    link_manager = LinksMgr()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(description='Searching for Links')
        results = link_manager.search(
            entities=entity_ids,
            sections=sections,
            entity_types=return_entity_types,
            sources=source,
            timeframe=timeframe,
            events=events,
            connected_entities=connected_entities,
            search_scope=search_scope,
            per_entity_type=limit_per_type,
        )

    if pretty:
        for result in results:
            entity = result.entity
            print(f'Entity: {entity.name}')
            print(f'Total Links: {len(result.links)}')
            for link in result.links[:5]:
                print(f' -> {link.name} Source: {link.source}')

    else:
        print_json(data=[result.model_dump() for result in results])
