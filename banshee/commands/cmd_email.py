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

from typing import Annotated, Optional

from typer import Argument, Option, Typer

from banshee.commands.args import OPT_PRETTY_PRINT
from banshee.email.constants import MIN_RISK_SCORE

from ..branding import banshee_cmd
from ..email.email_enrich import email_enrich
from .epilogs import EPILOG_EMAIL_ENRICH

CMD_NAME = 'email'
CMD_HELP = 'Enrich e-mail files (EML) with Recorded Future intelligence'
CMD_RICH_HELP = 'email Enrichment'

ENRICH_COMMAND_HELP = (
    'Enrich an e-mail (EML) file with Recorded Future Intelligence. '
    "This command parses the eml file to extract IP's from the header, "
    "URL's (prefixed with http/https) found in the body"
)

app = Typer(no_args_is_help=True)


@banshee_cmd(app=app, help_=ENRICH_COMMAND_HELP, epilog=EPILOG_EMAIL_ENRICH)
def enrich(
    file_path: Annotated[str, Argument(help='Path to eml file', show_default=False)],
    min_risk_score: Annotated[
        Optional[int],
        Option(
            '-r',
            '--risk-score',
            help='Filter the results to only show indicators above this threshold',
            show_default=True,
            min=0,
            max=99,
        ),
    ] = MIN_RISK_SCORE,
    hunt: Annotated[
        bool,
        Option(
            '--threat-hunt',
            '-t',
            help='Include indicators linked to threat actors regardless of risk score threshold',
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):
    email_enrich(file_path, pretty, hunt, min_risk_score)
