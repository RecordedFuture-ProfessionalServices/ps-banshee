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

from enum import Enum
from typing import Annotated, Optional

from typer import BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..risklist import create_risklist, fetch_risklist, stat_risklist
from .args import OPT_PRETTY_PRINT
from .epilogs import RISKLIST_CREATE, RISKLIST_FETCH, RISKLIST_STAT

CMD_NAME = 'risklist'
CMD_HELP = 'Manage Risk Lists'
CMD_RICH_HELP = 'Risk Lists'

HELP_FETCH = """Download a risk list for a specific entity type and list name, or use a custom \
risk list file.
Risk lists can be downloaded from Recorded Future by specifying an entity type \
`--entity-type` and list name `--list-name`. Available list names include \
`default`, `large`, or any rule name from `banshee ioc rules`. \
Alternatively, you can provide a path to a custom risk list file using `--custom-list-path`.
"""

HELP_CREATE = """Build a custom risk list by combining one or more Recorded Future risk rules \
into a single deduplicated file.
Fetch entries for each `--risk-rule` (e.g. `default`, `large`, or any rule from \
`banshee ioc rules`), merge them by IOC, and optionally filter the result down to a minimum \
`--risk-score`. The output is a single file in your chosen format — ready to feed into a firewall, \
SIEM, or other integration.
Output is written to a local file by default. Use `--fusion` with `--output-path` to upload the \
result directly to Recorded Future Fusion.
"""

app = Typer(no_args_is_help=True)


class EntityType(str, Enum):
    """Enum for possible entity types."""

    ip = 'ip'
    domain = 'domain'
    url = 'url'
    hash = 'hash'
    vulnerability = 'vulnerability'


class OutputFormat(str, Enum):
    """Enum for output formats."""

    csv = 'csv'
    edl = 'edl'
    json = 'json'


def validate_risklist_args(entity_type, list_name, custom_list_path: str, as_json: str):
    """Validate risklist fetch arguments."""
    if custom_list_path and (list_name or entity_type):
        raise BadParameter(
            '--custom-list-path must be specified alone (cannot be used with --list-name or --entity-type)'  # noqa: E501
        )

    if list_name and not entity_type:
        raise BadParameter('--entity-type is required when using --list-name')

    if entity_type and not list_name:
        raise BadParameter('--list-name is required when using --entity-type')

    if not custom_list_path and not list_name:
        raise BadParameter(
            'Either --custom-list-path or (--list-name and --entity-type) must be specified'
        )

    if custom_list_path and as_json:
        raise BadParameter('--as-json can only be used with --list-name and --entity-type')


@banshee_cmd(app=app, help_=HELP_FETCH, epilog=RISKLIST_FETCH)
def fetch(
    entity_type: Annotated[
        EntityType,
        Option('--entity-type', '-e', help='Entity type for the risk list', show_default=False),
    ] = None,
    list_name: Annotated[
        str,
        Option(
            '--list-name',
            '-l',
            help='Risk list name: default, large, or rule name from `banshee ioc rules`',
            show_default=False,
        ),
    ] = None,
    custom_list_path: Annotated[
        str,
        Option(
            '--custom-list-path',
            '-c',
            help='Path to custom risk list file',
            show_default=False,
        ),
    ] = None,
    output_path: Annotated[
        str,
        Option(
            '--output-path',
            '-o',
            help='Output file path (defaults to current directory with auto-generated filename)',
            show_default=False,
        ),
    ] = None,
    as_json: Annotated[
        bool,
        Option(
            '--as-json',
            '-j',
            help='Convert risk list to JSON format. Only applicable when using `--list-name` and `--entity-type`',  # noqa: E501
        ),
    ] = False,
):
    validate_risklist_args(entity_type, list_name, custom_list_path, as_json)

    fetch_risklist(
        entity_type=entity_type,
        list_=list_name,
        custom_list_path=custom_list_path,
        output_path=output_path,
        as_json=as_json,
    )


@banshee_cmd(app=app, help_=HELP_CREATE, epilog=RISKLIST_CREATE)
def create(
    entity_type: Annotated[
        EntityType,
        Option('--entity-type', '-e', help='Entity type for the risk list', show_default=False),
    ] = None,
    risk_rules: Annotated[
        list[str],
        Option(
            '--risk-rule',
            '-R',
            help='Risk rule to include (repeatable). Use "default", "large", or a rule name from `banshee ioc rules`',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    risk_score: Annotated[
        Optional[int],
        Option(
            '--risk-score',
            '-r',
            help='Minimum risk score threshold (5-99). Entries below this score are excluded.',
            min=5,
            max=99,
            show_default=False,
        ),
    ] = None,
    format_: Annotated[
        OutputFormat,
        Option('--format', '-f', help='Output format', show_default=True),
    ] = OutputFormat.csv,
    output_path: Annotated[
        Optional[str],
        Option(
            '--output-path',
            '-o',
            help='Output file path (defaults to current directory with auto-generated filename)',
            show_default=False,
        ),
    ] = None,
    fusion: Annotated[
        bool,
        Option(
            '--fusion',
            '-F',
            help='Write to Recorded Future Fusion using --output-path as the fusion destination path',  # noqa: E501
        ),
    ] = False,
):
    if not entity_type:
        raise BadParameter('--entity-type is required')

    if not risk_rules:
        raise BadParameter('At least one --risk-rule is required')

    if fusion and not output_path:
        raise BadParameter('--output-path is required when using --fusion')

    create_risklist(
        entity_type=entity_type.value,
        risk_rules=risk_rules,
        risk_score=risk_score,
        output_path=output_path,
        fusion=fusion,
        format_=format_.value,
    )


@banshee_cmd(app=app, help_='Show risk list metadata (etag and timestamp)', epilog=RISKLIST_STAT)
def stat(
    entity_type: Annotated[
        EntityType,
        Option('--entity-type', '-e', help='Entity type for the risk list', show_default=False),
    ] = None,
    list_name: Annotated[
        str,
        Option(
            '--list-name',
            '-l',
            help='Risk list name: default, large, or rule name from `banshee ioc rules`',
            show_default=False,
        ),
    ] = None,
    custom_list_path: Annotated[
        str,
        Option(
            '--custom-list-path', '-c', help='Path to custom risk list file', show_default=False
        ),
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    validate_risklist_args(entity_type, list_name, custom_list_path, as_json=None)

    stat_risklist(
        entity_type=entity_type,
        list_=list_name,
        custom_list_path=custom_list_path,
        pretty=pretty,
    )
