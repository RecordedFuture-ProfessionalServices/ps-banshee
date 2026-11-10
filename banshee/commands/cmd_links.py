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
from typing import Annotated

from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..links.constants import LinkSource
from ..links.link_search import search_links
from .args import OPT_PRETTY_PRINT

CMD_NAME = 'links'
CMD_HELP = 'Fetch and export linked entities'
CMD_RICH_HELP = 'Recorded Future Links'

app = Typer(no_args_is_help=True)


@banshee_cmd(app=app, help_='Search and export linked entities', epilog='')
def search(
    entity_id: list[str] = Argument(  # noqa: B008
        default=None,
        show_default=False,
        help='One or more whitespace separated Entities IDs',
    ),
    return_entity_types: Annotated[
        list[str],
        Option(
            '--type',
            '-t',
            help='Type of entity to return',
            show_default=False,
        ),
    ] = None,
    source: Annotated[
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
    limit: Annotated[
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
    pretty: OPT_PRETTY_PRINT = False,
):
    if small and large:
        raise BadParameter('--small and --large are mutually exclusive.')
    if small and not large:
        scope = 'small'
    elif large and not small:
        scope = 'large'
    else:
        scope = 'medium'

    search_links(
        entity_id,
        return_entity_types,
        source,
        sections,
        timeframe,
        events,
        connected_entities,
        limit,
        scope,
        pretty,
    )
