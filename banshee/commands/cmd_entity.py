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

from typer import Argument, Option, Typer

from ..branding import banshee_cmd
from ..entity_match import EntityType, entity_lookup, entity_search
from .args import OPT_PRETTY_PRINT
from .epilogs import EPILOG_ENTITY_LOOKUP, EPILOG_ENTITY_SEARCH

CMD_NAME = 'entity'
CMD_HELP = 'Search and lookup entities'
CMD_RICH_HELP = 'Entity Match'

PANEL_ENTITY = 'Entity Match'

app = Typer(no_args_is_help=True)


@banshee_cmd(
    app=app,
    help_='Lookup an entity by its ID',
    epilog=EPILOG_ENTITY_LOOKUP,
    rich_help_panel=PANEL_ENTITY,
)
def lookup(
    entity_id: str = Argument(show_default=False, help='ID of the entity to lookup'),
    pretty: OPT_PRETTY_PRINT = False,
):
    entity_lookup(entity_id=entity_id, pretty=pretty)


@banshee_cmd(
    app=app,
    help_='Search entities by name and optically by type',
    epilog=EPILOG_ENTITY_SEARCH,
    rich_help_panel=PANEL_ENTITY,
)
def search(
    name: str = Argument(show_default=False, help='Name of the entity to search for'),
    type_: Annotated[
        list[EntityType],
        Option(
            '-t', '--type', help='One or more type of the entity to search for', show_default=False
        ),
    ] = None,
    limit: Annotated[
        int, Option('-l', '--limit', help='Limit number of results', min=1, max=100)
    ] = 100,
    pretty: OPT_PRETTY_PRINT = False,
):
    entity_search(name=name, type_=type_, limit=limit, pretty=pretty)
