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

import sys
from enum import Enum
from typing import Annotated, Union

from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..lists import (
    add_entity,
    bulk_add_entities,
    bulk_remove_entities,
    clear_list,
    create_list,
    fetch_entities,
    fetch_entries,
    fetch_list_info,
    fetch_list_status,
    resolve_tech_stack,
    remove_entity,
    search_lists,
)
from .args import OPT_PRETTY_PRINT
from .epilogs import (
    EPILOG_LIST_ADD,
    EPILOG_LIST_BULK_ADD,
    EPILOG_LIST_BULK_REMOVE,
    EPILOG_LIST_CLEAR,
    EPILOG_LIST_CREATE,
    EPILOG_LIST_ENTITIES,
    EPILOG_LIST_ENTRIES,
    EPILOG_LIST_INFO,
    EPILOG_LIST_REMOVE,
    EPILOG_LIST_SEARCH,
    EPILOG_LIST_STATUS,
    EPILOG_TECH_STACK_RESOLVE,
)

CMD_NAME = 'list'
CMD_HELP = 'Manage Recorded Future Lists & Watch Lists'
CMD_RICH_HELP = 'Recorded Future Lists & Watch Lists'

PANEL_LIST_MGMT = 'List Management'
PANEL_ENTITY_MGMT = 'Entity Management'
PANEL_TEXT_MATCH_MGMT = 'Text Match Management'
PANEL_WORKFLOWS = 'Use Cases'

app = Typer(no_args_is_help=True)


def parse_entity_input(entities: Union[list, str]):
    parsed_entities = []
    for entity in entities:
        if ',' in entity:
            # Split on the last comma to handle entity names that contain commas
            parsed_entity = entity.rsplit(',', 1)
            if len(parsed_entity) != 2:
                raise BadParameter(f"Invalid entity input '{entity}': expected '<name>,<type>'")
            if any(e.strip() == '' for e in parsed_entity):
                raise BadParameter(f"Invalid entity input '{entity}': expected '<name>,<type>'")

            parsed_entity = [e.strip() for e in parsed_entity]
        else:
            parsed_entity = entity
        parsed_entities.append(parsed_entity)

    return parsed_entities


class ListType(str, Enum):
    """Enum for possible list types."""

    entity = 'entity'
    source = 'source'
    text = 'text'
    custom = 'custom'
    ip = 'ip'
    domain = 'domain'
    tech_stack = 'tech_stack'
    industry = 'industry'
    brand = 'brand'
    partner = 'partner'
    industry_peer = 'industry_peer'
    location = 'location'
    supplier = 'supplier'
    vulnerability = 'vulnerability'
    company = 'company'
    hash = 'hash'
    operation = 'operation'
    attacker = 'attacker'
    target = 'target'
    method = 'method'
    executive = 'executive'


class ListCreateOption(str, Enum):
    """Enum for possible list types to create."""

    entity = 'entity'
    source = 'source'
    text = 'text'


@banshee_cmd(
    app=app, help_='Create a list', epilog=EPILOG_LIST_CREATE, rich_help_panel=PANEL_LIST_MGMT
)
def create(
    name: Annotated[str, Argument(show_default=False, help='Name of the list to create')],
    list_type: Annotated[
        ListCreateOption, Argument(help='Type of entities the list will be used for')
    ] = ListCreateOption.entity,
    pretty: OPT_PRETTY_PRINT = False,
):
    create_list(name=name, list_type=list_type, pretty=pretty)


@banshee_cmd(
    app=app,
    help_='Get basic information about a specified list',
    epilog=EPILOG_LIST_INFO,
    rich_help_panel=PANEL_LIST_MGMT,
)
def info(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_list_info(list_id=list_id, pretty=pretty)


@banshee_cmd(
    app=app, help_='Search for lists', epilog=EPILOG_LIST_SEARCH, rich_help_panel=PANEL_LIST_MGMT
)
def search(
    name: Annotated[
        str, Argument(show_default=False, help='Name of the list(s) to search for')
    ] = None,
    list_type: Annotated[
        ListType, Option('--list-type', '-t', help='List(s) type to search for', show_default=False)
    ] = None,
    limit: Annotated[
        int, Option('--limit', '-l', help='Limit the number of lists returned', min=1, max=3_000)
    ] = 1_000,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_lists(name=name, list_type=list_type, limit=limit, pretty=pretty)


@banshee_cmd(
    app=app,
    help_='Get status information about a specified list',
    epilog=EPILOG_LIST_STATUS,
    rich_help_panel=PANEL_LIST_MGMT,
)
def status(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_list_status(list_id=list_id, is_pretty=pretty)


@banshee_cmd(
    app=app,
    help_='Get entities on the list',
    epilog=EPILOG_LIST_ENTITIES,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def entities(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_entities(list_id=list_id, pretty=pretty)


@banshee_cmd(
    app=app,
    help_='Add a single entity to a list',
    epilog=EPILOG_LIST_ADD,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def add(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    entity_id: str = Argument(
        show_default=False,
        help='Entity ID or name with type to add, for example: 1. SoA6SP, 2. wannacry,malware',
    ),
    properties: Annotated[
        str,
        Argument(
            show_default=False,
            help='Properties to add, for example: key=value,another=value',
        ),
    ] = None,
):
    if ',' in entity_id:
        entity_id = entity_id.split(',')
    add_entity(list_id=list_id, entity=entity_id, properties=properties)


@banshee_cmd(
    app=app,
    help_='Add multiple entities to a list',
    epilog=EPILOG_LIST_BULK_ADD,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def bulk_add(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    entity_input: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more space-separated entities (CLI) or newline-separated entities (stdin), for example: SoA6SP wannacry,malware',  # noqa: E501
    ),
):
    if entity_input is None:
        entity_input = sys.stdin.read()
        entity_input = entity_input.strip().split('\n')
        entity_input = list(filter(lambda x: x, entity_input))

    entities = parse_entity_input(entity_input)
    bulk_add_entities(list_id=list_id, entities=entities)


@banshee_cmd(
    app=app,
    help_='Remove a single entity from a list',
    epilog=EPILOG_LIST_REMOVE,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def remove(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    entity_id: Annotated[
        str, Argument(show_default=False, help='ID of the entity to remove from the list')
    ],
):
    if ',' in entity_id:
        entity_id = entity_id.split(',')
    remove_entity(list_id=list_id, entity=entity_id)


@banshee_cmd(
    app=app,
    help_='Remove multiple entities from a list',
    epilog=EPILOG_LIST_BULK_REMOVE,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def bulk_remove(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    entity_input: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more space-separated entities (CLI) or newline-separated entities (stdin), for example: SoA6SP wannacry,malware',  # noqa: E501
    ),
):
    if entity_input is None:
        entity_input = sys.stdin.read()
        entity_input = entity_input.strip().split('\n')
        entity_input = list(filter(lambda x: x, entity_input))

    entities = parse_entity_input(entity_input)
    bulk_remove_entities(list_id=list_id, entities=entities)


@banshee_cmd(
    app=app,
    help_='Clear the list of all entities',
    epilog=EPILOG_LIST_CLEAR,
    rich_help_panel=PANEL_ENTITY_MGMT,
)
def clear(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
):
    clear_list(list_id=list_id)


@banshee_cmd(
    app=app,
    help_='Get text entries on the list',
    epilog=EPILOG_LIST_ENTRIES,
    rich_help_panel=PANEL_TEXT_MATCH_MGMT,
)
def entries(
    list_id: Annotated[str, Argument(show_default=False, help='ID of the list')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_entries(list_id=list_id, pretty=pretty)


@banshee_cmd(
    app=app,
    help_=(
        'Resolve technologies and products from a CSV file to Recorded Future entities '
        'with mapped CVE counts. Designed for Tech Stack Watch List candidate selection.'
    ),
    epilog=EPILOG_TECH_STACK_RESOLVE,
    rich_help_panel=PANEL_WORKFLOWS,
)
def tech_stack_resolve(
    file_path: Annotated[
        str,
        Argument(
            show_default=False,
            help='CSV file to resolve against Recorded Future entities (first column is used)',
        ),
    ],
    list_id: Annotated[str, Argument(show_default=False, help='ID of the Tech Stack Watch List to add resolved entities to. If not provided, entities will not be added to any list.')] = None,
    possible_matches: Annotated[
        int,
        Option(
            '--possible-matches',
            '-m',
            help='Maximum number of candidate entity matches to keep for each supplied value',
            min=1,
            max=25,
        ),
    ] = 3,
    output_file: Annotated[
        str,
        Option(
            '--output-file',
            '-o',
            help='Output CSV path for the entity reslution results',
            show_default=True,
        ),
    ] = 'tech_stack_entity_match.csv',
):
    resolve_tech_stack(
        list_id=list_id,
        infile=file_path,
        possible_matches=possible_matches,
        output_file=output_file,
    )
