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
from typing import Annotated, Optional

from typer import Argument, BadParameter, Option, Typer

from ..branding import banshee_cmd
from ..indicators import IOCType, lookup_ioc, search_ioc, search_ioc_rules, soar_enrich
from .args import OPT_PRETTY_PRINT
from .epilogs import EPILOG_IOC_BULK_LOOKUP, EPILOG_IOC_LOOKUP, EPILOG_IOC_RULES, EPILOG_IOC_SEARCH

CMD_NAME = 'ioc'
CMD_HELP = 'Search and lookup IOCs'
CMD_RICH_HELP = 'Indicators of Compromise'

app = Typer(no_args_is_help=True)


def parse_ioc_input(value: list[str]):
    if not value:
        raise BadParameter('No IOCs supplied')

    iocs = value
    if isinstance(value, str):
        iocs = [x for x in re.split(r'[\s]+', value) if x]

        if not len(iocs):
            raise BadParameter('No IOCs provided')

    return iocs


@banshee_cmd(
    app=app,
    help_=(
        'Detailed enrichment for one or more IOCs — one API call per indicator. '
        'Use `--verbosity` to control how many fields are returned, from basic risk score up to '
        'full intel including links, analyst notes, etc. '
        'Use this when you need rich context.'
    ),
    epilog=EPILOG_IOC_LOOKUP,
    rich_help_panel='IOC Enrichment',
)
def lookup(
    entity_type: Annotated[IOCType, Argument(show_default=False, help='Type of IOC')],
    ioc: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more whitespace separated IOC',
    ),
    ai_insights: Annotated[
        bool,
        Option(
            '--ai-insights',
            '-a',
            help=(
                'Enable AI-generated insights from Recorded Future that summarize relevant '
                'risk rules and key references. Response times may be slightly longer due '
                'to AI processing.'
            ),
        ),
    ] = False,
    verbosity: Annotated[
        int,
        Option(
            '--verbosity',
            '-v',
            min=1,
            max=5,
            help=(
                'Controls the amount of data returned in the response. '
                'Higher verbosity levels include additional fields and details '
                'in the JSON output. Higher verbosity levels may result in slower '
                'response times due to increased data retrieval. '
            ),
        ),
    ] = 1,
    pretty: OPT_PRETTY_PRINT = False,
):
    if ioc is None:
        ioc = sys.stdin.read()

    ioc = parse_ioc_input(ioc)

    lookup_ioc(
        indicators=ioc,
        entity_type=entity_type,
        verbose_level=verbosity,
        pretty=pretty,
        ai_insights=ai_insights,
    )


@banshee_cmd(
    app=app,
    help_=(
        'Fast bulk enrichment that batches up to 1000 IOCs per API call — '
        'submit any number of indicators and the command handles the batching automatically. '
        'Returns a fixed set of fields — risk score and triggered risk rules. '
        'Use this for high-volume triage. '
    ),
    epilog=EPILOG_IOC_BULK_LOOKUP,
    rich_help_panel='IOC Enrichment',
)
def bulk_lookup(
    entity_type: Annotated[IOCType, Argument(show_default=False, help='Type of IOC')],
    ioc: list[str] = Argument(  # noqa: B008
        ... if sys.stdin.isatty() else None,  # noqa: B008
        show_default=False,
        help='One or more whitespace separated IOC',
    ),
    pretty: OPT_PRETTY_PRINT = False,
):
    if ioc is None:
        ioc = sys.stdin.read()

    ioc = parse_ioc_input(ioc)

    soar_enrich(indicators=ioc, entity_type=entity_type.value, pretty=pretty)


def parse_risk_score_input(value: str):
    if not value:
        return value

    if not re.match(r'^[\[\(](\d+|),(\d+|)[\]\)]$', value.strip()):
        raise BadParameter('Invalid risk score format')

    return value.strip()


@banshee_cmd(
    app=app, help_='Search for IOCs', epilog=EPILOG_IOC_SEARCH, rich_help_panel='IOC Search'
)
def search(
    entity_type: Annotated[IOCType, Argument()],
    limit: Annotated[
        Optional[int],
        Option('--limit', '-l', help='Maximum number of IOCs to return', min=1, max=1000),
    ] = 5,
    risk_score: Annotated[
        Optional[str],
        Option(
            '--risk-score',
            '-r',
            help='Filter by risk score range',
            callback=parse_risk_score_input,
            show_default=False,
        ),
    ] = None,
    risk_rule: Annotated[
        Optional[str], Option('--risk-rule', '-R', help='Filter by risk rule', show_default=False)
    ] = None,
    verbosity: Annotated[
        int,
        Option(
            '--verbosity',
            '-v',
            min=1,
            max=5,
            help=(
                'Controls the amount of data returned in the response. '
                'Higher verbosity levels include additional fields and details '
                'in the JSON output. Higher verbosity levels may result in slower '
                'response times due to increased data retrieval. '
            ),
        ),
    ] = 1,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_ioc(
        entity_type=entity_type.value,
        limit=limit,
        risk_score=risk_score,
        risk_rule=risk_rule,
        verbose_level=verbosity,
        pretty=pretty,
    )


@banshee_cmd(
    app=app, help_='Search for IOC Rules', epilog=EPILOG_IOC_RULES, rich_help_panel='IOC Rules'
)
def rules(
    entity_type: Annotated[IOCType, Argument(show_default=False, help='Type of IOC')],
    freetext: Annotated[
        str,
        Option(
            '-F',
            '--freetext',
            show_default=False,
            help='Free text search to filter rules by name/description',
        ),
    ] = None,
    mitre_code: Annotated[
        str,
        Option(
            '-M',
            '--mitre-code',
            show_default=False,
            help='Filter by MITRE ATT&CK code',
        ),
    ] = None,
    criticality: Annotated[
        int,
        Option(
            '-C',
            '--criticality',
            show_default=False,
            min=0,
            max=5,
            help='Filter by criticality. Higher the value, higher the criticality',
        ),
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_ioc_rules(
        entity_type=entity_type.value,
        freetext=freetext,
        mitre_code=mitre_code,
        criticality=criticality,
        pretty=pretty,
    )
