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
from banshee.pcap_enrich.constants import MIN_RISK_SCORE

from ..branding import banshee_cmd
from ..pcap_enrich.helpers import check_tshark_version
from ..pcap_enrich.pcap_enrich import pcap_enrich
from .epilogs import EPILOG_PCAP_ANALYZER

CMD_NAME = 'pcap'
CMD_HELP = 'Enrich packet captures (pcap) with Recorded Future intelligence'
CMD_RICH_HELP = 'Packet Capture Enrichment'

app = Typer(no_args_is_help=True)

ENRICH_COMMAND_HELP = (
    'Enrich a packet capture (pcap) file with Recorded Future intelligence. '
    'This command parses the pcap file to extract network indicators like IP addresses and '
    'domains, then enriches them with threat intelligence data. '
    'By default, results are filtered to show only indicators that meet your risk score threshold. '
    'Use `--threat-hunt` to also include indicators linked to threat actors, even if they fall '
    'below the risk score threshold. '
    'Please note that lowering the risk score threshold and/or enabling threat hunting may '
    'significantly increase both the number of results and processing time.'
)


@app.callback()
def check_tshark():
    """Check if tshark is installed and its version."""
    check_tshark_version()


@banshee_cmd(app=app, help_=ENRICH_COMMAND_HELP, epilog=EPILOG_PCAP_ANALYZER)
def enrich(
    file_path: Annotated[str, Argument(help='Path to pcap file', show_default=False)],
    risk_score: Annotated[
        Optional[int],
        Option(
            '--risk-score',
            '-r',
            help='Filter results to show only indicators with risk score above this threshold',
            show_default=True,
            min=1,
            max=99,
        ),
    ] = MIN_RISK_SCORE,
    hunt: Annotated[
        bool,
        Option(
            '--threat-hunt',
            '-t',
            help='Include indicators linked to threat actors regardless of risk score threshold (retrospective threat hunting)',  # noqa: E501
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):
    pcap_enrich(file_path, pretty, hunt, risk_score)
