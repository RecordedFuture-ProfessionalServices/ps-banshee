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

from typing import Annotated

from typer import Argument, Option, Typer

from ..branding import banshee_cmd
from ..sandbox import (
    fetch_sandbox_stats,
    get_sandbox_profile,
    list_sandbox_profiles,
    print_sandbox_stats,
)
from .args import OPT_PRETTY_PRINT, OPT_SANDBOX_SUBSET
from .epilogs import EPILOG_SANDBOX_PROFILE_GET, EPILOG_SANDBOX_PROFILE_LIST, EPILOG_SANDBOX_STATS

CMD_NAME = 'sandbox'
CMD_HELP = 'Sandbox submission analytics and profile management'
CMD_RICH_HELP = 'Sandbox'

_PANEL_ANALYTICS = 'Analytics'
_PANEL_PROFILE_MGMT = 'Profile Management'

_HELP_STATS = (
    'Aggregate sandbox submissions over a configurable window and print a '
    '"morning brief" suitable for SOC shift handover or daily triage. '
    'Shows submission volume, score distribution, top malware families, platform '
    'coverage, extracted C2s, and SOAR-validated network IOCs. '
    'Default output is JSON; use `--pretty` for a human-readable Rich layout.'
)

_HELP_PROFILE_GET = 'Fetch a single analysis profile by ID or name'
_HELP_PROFILE_LIST = 'List all analysis profiles available in Recorded Future Sandbox'

app = Typer(no_args_is_help=True)
profile_app = Typer(no_args_is_help=True)


@banshee_cmd(
    app=app, help_=_HELP_STATS, epilog=EPILOG_SANDBOX_STATS, rich_help_panel=_PANEL_ANALYTICS
)
def stats(
    days: Annotated[
        int,
        Option('--days', '-d', help='Lookback window in days', min=1),
    ] = 7,
    subset: OPT_SANDBOX_SUBSET = 'org',
    pretty: OPT_PRETTY_PRINT = False,
):
    result = fetch_sandbox_stats(days=days, subset=subset)
    print_sandbox_stats(result, pretty=pretty)


@banshee_cmd(
    app=profile_app, name='get', help_=_HELP_PROFILE_GET, epilog=EPILOG_SANDBOX_PROFILE_GET
)
def get_(
    profile_id_or_name: Annotated[str, Argument(help='Profile ID or name')],
    pretty: OPT_PRETTY_PRINT = False,
):
    get_sandbox_profile(profile_id_or_name, pretty=pretty)


@banshee_cmd(
    app=profile_app, name='list', help_=_HELP_PROFILE_LIST, epilog=EPILOG_SANDBOX_PROFILE_LIST
)
def list_(pretty: OPT_PRETTY_PRINT = False):
    list_sandbox_profiles(pretty=pretty)


app.add_typer(
    profile_app,
    name='profile',
    help='Manage analysis profiles',
    rich_help_panel=_PANEL_PROFILE_MGMT,
)
