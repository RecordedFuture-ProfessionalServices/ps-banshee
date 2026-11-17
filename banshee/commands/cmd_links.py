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

import re
import sys
from typing import Annotated

from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..links.constants import LinkSource
from ..links.links_search import search_links
from .args import OPT_PRETTY_PRINT
from .epilogs import EPILOG_LINKS_SEARCH

CMD_NAME = 'links'
CMD_HELP = 'Fetch and export linked entities'
CMD_RICH_HELP = 'Recorded Future Links'

app = Typer(no_args_is_help=True)


def _parse_entity_ids(value: list[str] | str):
    if not value:
        raise BadParameter('No entities provided.')

    entity_ids = value
    if isinstance(value, str):
        entity_ids = [x for x in re.split(r'\s+', value) if x]

        if not entity_ids:
            raise BadParameter('No entities provided.')

    for entity_id in entity_ids:
        _validate_entity_ids(entity_id)

    return entity_ids


def _validate_entity_ids(entity_id: str):
    if entity_id is None:
        raise BadParameter('No entity_id provided.')
    if not isinstance(entity_id, str):
        raise BadParameter('Invalid entity_id provided.')
    if len(entity_id) != 6:
        raise BadParameter(f'Invalid entity ID: {entity_id}. ')
    return entity_id


@banshee_cmd(app=app, help_='Search and export linked entities', epilog=EPILOG_LINKS_SEARCH)
def search(
    entities: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more whitespace separated entity IDs',
    ),
    entity_types: Annotated[
        list[str],
        Option(
            '--type',
            '-t',
            help='Type of entity to return',
            show_default=False,
        ),
    ] = None,
    sources: Annotated[
        LinkSource,
        Option(
            '--source',
            '-s',
            help='Source of entity to return',
            show_default=False,
        ),
    ] = None,
    sections: Annotated[
        list[str],
        Option(
            '--sections',
            '-S',
            help="Filter by the type of link. (e.g. 'Indicators and Detection Rules')",
            show_default=False,
        ),
    ] = None,
    timeframe: Annotated[
        str,
        Option(
            '--timeframe',
            '-T',
            help="Timeframe for the Link being made. (e.g. '-1d', max: '-90d'.)",
            show_default=False,
        ),
    ] = None,
    events: Annotated[
        list[str],
        Option(
            '--events',
            '-e',
            help="Filter by the type of event (e.g. 'type:MalwareAnalysis')",
            show_default=False,
        ),
    ] = None,
    connected_entities: Annotated[
        list[str],
        Option(
            '--connected-entities',
            '-c',
            help='Only return entities that are also connected to these entities.',
            show_default=False,
        ),
    ] = None,
    per_entity_type: Annotated[
        int,
        Option(
            '--limit',
            '-l',
            help='Limit the number of entities to return per type.',
            show_default=False,
            min=1,
            max=1_000_000,
        ),
    ] = None,
    small: Annotated[
        bool,
        Option(
            '--small',
            help='Search 10 references and 10 Insikt Notes per event type.',
            show_default=False,
        ),
    ] = False,
    large: Annotated[
        bool,
        Option(
            '--large',
            help='Search 100 references and 500 Insikt Notes per event type.',
            show_default=False,
        ),
    ] = False,
    skip_enrichment: Annotated[
        bool,
        Option(
            '--skip-enrichment',
            help='Skip running additional enrichment of entities.',
            show_default=False,
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):

    if entities is None:
        entities = sys.stdin.read()

    entities = _parse_entity_ids(entities)

    if small and large:
        raise BadParameter('--small and --large are mutually exclusive.')
    if small and not large:
        scope = 'small'
    elif large and not small:
        scope = 'large'
    else:
        scope = 'medium'

    search_links(
        entities=entities,
        entity_types=entity_types,
        sources=sources,
        sections=sections,
        timeframe=timeframe,
        events=events,
        connected_entities=connected_entities,
        per_entity_type=per_entity_type,
        search_scope=scope,
        skip_enrichment=skip_enrichment,
        pretty=pretty,
    )
