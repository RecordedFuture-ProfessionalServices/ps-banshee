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
from collections import defaultdict

from psengine.enrich import EnrichmentSoarError, SoarMgr
from psengine.links import LinksMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .constants import _TYPE_MAPPING, MAX_ENRICHMENT_WORKERS, PRETTY_IOC_DISPLAY_CAP
from .helpers import _print_search


def _sort_links_iocs(results: list, limit: int | None = None):
    """Sort the result links for an entity into a readable dict."""
    sorted_iocs = defaultdict(set)
    for result in results:
        for ioc_type, iocs in result.iocs().items():
            converted_type = _TYPE_MAPPING.get(ioc_type)
            if converted_type:
                sorted_iocs[converted_type].update(i.name for i in iocs[:limit])
    return sorted_iocs


def _enrich_linked_iocs(to_enrich: dict):
    """Enrich the linked IOC's via SOAR manager."""
    try:
        soar_mgr = SoarMgr()
        enriched = soar_mgr.soar(**to_enrich, max_workers=MAX_ENRICHMENT_WORKERS)
        return {r.entity: r for r in enriched}
    except EnrichmentSoarError:
        Console(stderr=True).print('NOTE: SOAR Enrichment failed, skipping additional enrichment.')
        return {}


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
    skip_enrichment: bool,
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
        task = progress.add_task(description='Searching for Links')
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

        enriched = {}
        if not skip_enrichment:
            progress.update(task, description='Extracting IOCs to enrich')
            iocs_to_enrich = _sort_links_iocs(
                results, limit=PRETTY_IOC_DISPLAY_CAP if pretty else None
            )
            if iocs_to_enrich:
                progress.update(task, description='Enriching linked IOCs')
                enriched = _enrich_linked_iocs(iocs_to_enrich)

    if pretty:
        console = Console(stderr=True)
        for result in results:
            console.print(f'[bold]{result.entity.name} ({result.entity.id_})[/bold]')
            _print_search(console, result, enriched)

    else:
        out = []
        for r in results:
            d = r.model_dump(mode='json')
            for link, link_dict in zip(r.links, d['links']):
                e = enriched.get(link.name)
                link_dict['enrichment'] = (
                    e.content.model_dump(mode='json') if e and e.is_enriched and e.content else None
                )
            out.append(d)
        print_json(data=out)
