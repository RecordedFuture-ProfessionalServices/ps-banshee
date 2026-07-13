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

from typer import Argument, BadParameter, Option, Typer, confirm

from ..branding import banshee_cmd
from ..sandbox import (
    create_sandbox_profile,
    delete_sandbox_profile,
    fetch_behavioral_reports,
    fetch_overview_report,
    fetch_sandbox_stats,
    fetch_static_report,
    get_sandbox_profile,
    list_sandbox_profiles,
    list_sandbox_samples,
    print_sandbox_stats,
    set_sandbox_sample_profile,
    submit_sandbox_sample,
    update_sandbox_profile,
)
from .args import (
    OPT_PRETTY_PRINT,
    OPT_PROFILE_UNSET,
    OPT_SANDBOX_BROWSER,
    OPT_SANDBOX_NETWORK,
    OPT_SANDBOX_SUBSET,
)
from .epilogs import (
    EPILOG_SANDBOX_LIST,
    EPILOG_SANDBOX_PROFILE_CREATE,
    EPILOG_SANDBOX_PROFILE_DELETE,
    EPILOG_SANDBOX_PROFILE_GET,
    EPILOG_SANDBOX_PROFILE_LIST,
    EPILOG_SANDBOX_PROFILE_UPDATE,
    EPILOG_SANDBOX_REPORT_BEHAVIORAL,
    EPILOG_SANDBOX_REPORT_OVERVIEW,
    EPILOG_SANDBOX_REPORT_STATIC,
    EPILOG_SANDBOX_SET_PROFILE,
    EPILOG_SANDBOX_STATS,
    EPILOG_SANDBOX_SUBMIT,
)

CMD_NAME = 'sandbox'
CMD_HELP = 'Sandbox submission analytics and profile management'
CMD_RICH_HELP = 'Sandbox'

_PANEL_ANALYTICS = 'Analytics'
_PANEL_PROFILE_MGMT = 'Profile Management'
_PANEL_REPORTS = 'Reports'
_PANEL_SUBMISSION = 'Samples'

_HELP_STATS = (
    'Aggregate sandbox submissions over a configurable window and print a '
    '"morning brief" suitable for SOC shift handover or daily triage. '
    'Shows submission volume, score distribution, top malware families, platform '
    'coverage, extracted C2s, and SOAR-validated network IOCs. '
    'Default output is JSON; use `--pretty` for a human-readable Rich layout.'
)

_HELP_LIST = (
    'List sandbox samples: your own submissions, all submissions in your '
    'organisation (default), or the public feed. Default output is a JSON '
    'array of samples; use `--pretty` for a human-readable table. '
    'An empty result prints `[]` and exits 0.'
)

_HELP_PROFILE_CREATE = (
    'Create a new analysis profile in Recorded Future Sandbox. '
    'Prints the created profile, including its assigned ID. '
    'The profile name must be unique within your company.'
)
_HELP_PROFILE_DELETE = (
    'Delete an analysis profile by ID or name. Idempotent: deleting a profile '
    'that does not exist prints a warning and exits 0. Prompts for confirmation '
    'unless --yes is given.'
)
_HELP_PROFILE_GET = 'Fetch a single analysis profile by ID or name'
_HELP_PROFILE_LIST = 'List all analysis profiles available in Recorded Future Sandbox'
_HELP_PROFILE_UPDATE = (
    'Update an existing analysis profile. Only the options you supply change — '
    'omitted options keep their current value. Use --unset to clear network, '
    'browser, or geolocation. Updating a non-existent profile prints '
    '{"updated": false} and exits 0.'
)
_HELP_REPORT_BEHAVIORAL = (
    'Fetch the behavioral (post-detonation) reports for a completed sandbox '
    'sample, one per behavioral task: verdict score, platform, triggered '
    'signatures, observed processes, network activity, and extracted malware '
    'configs. Default output is a JSON array of the full reports; use '
    '`--pretty` for a summarised human-readable view per task. A sample with '
    'no behavioral tasks prints an empty array and exits 0.'
)
_HELP_REPORT_OVERVIEW = (
    'Fetch the overview report for a completed sandbox sample: verdict score, '
    'malware family, tags, hashes, detection signatures, extracted malware '
    'configs, network IOCs, and per-task results. Default output is the full '
    'report as JSON; use `--pretty` for a summarised human-readable view. '
    'Requires the sample to have finished analysis (status `reported`).'
)
_HELP_REPORT_STATIC = (
    'Fetch the static (pre-detonation) analysis report for a sandbox sample: '
    'verdict score, tags, the files unpacked from the submission, static '
    'detection signatures, and extracted malware configs. Available as soon '
    'as static analysis completes — no need to wait for behavioral tasks to '
    'finish. Default output is the full report as JSON; use `--pretty` for a '
    'summarised human-readable view.'
)
_HELP_SET_PROFILE = (
    'Assign analysis profiles to a sample paused at static analysis '
    '(submitted with interactive=True). Use --auto to let the sandbox choose '
    'automatically, or --pick FILE:PROFILE for manual per-file mapping.'
)
_HELP_SUBMIT = (
    'Submit a sample to Recorded Future Sandbox for analysis. The submission '
    'kind is detected from the target: an existing local file is uploaded, a '
    'URL is detonated in a browser (or downloaded first with --fetch), and '
    '--import brings in a public sample by ID. Default output is the submitted '
    'sample as JSON; --wait polls until analysis completes and prints the '
    'overview report instead. --interactive pauses at static analysis and '
    'prompts for file and profile selection before detonation.'
)

app = Typer(no_args_is_help=True)
profile_app = Typer(no_args_is_help=True)
report_app = Typer(no_args_is_help=True)


def _require_non_empty(**options):
    for flag, value in options.items():
        values = [value] if isinstance(value, str) else value or []
        if any(not v for v in values):
            raise BadParameter(f'--{flag} must not be empty')


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
    app=profile_app,
    name='create',
    help_=_HELP_PROFILE_CREATE,
    epilog=EPILOG_SANDBOX_PROFILE_CREATE,
)
def create(
    name: Annotated[
        str,
        Option('--name', '-n', help='Profile name (must be unique)'),
    ],
    tags: Annotated[
        list[str],
        Option('--tags', '-T', help='OS/locale tag (repeatable)'),
    ],
    timeout: Annotated[
        int,
        Option('--timeout', '-t', help='Analysis timeout in seconds', min=1, max=3600),
    ],
    network: OPT_SANDBOX_NETWORK = None,
    geolocation: Annotated[
        list[str] | None,
        Option('--geolocation', help='VPN country code; requires a vpn network (repeatable)'),
    ] = None,
    browser: OPT_SANDBOX_BROWSER = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    _require_non_empty(name=name, tags=tags)
    if geolocation and network != 'vpn':
        raise BadParameter('--geolocation requires --network vpn')
    create_sandbox_profile(
        name=name,
        tags=tags,
        timeout=timeout,
        network=network,
        geolocation=geolocation,
        browser=browser,
        pretty=pretty,
    )


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


@banshee_cmd(
    app=profile_app,
    name='update',
    help_=_HELP_PROFILE_UPDATE,
    epilog=EPILOG_SANDBOX_PROFILE_UPDATE,
)
def update(
    profile_id_or_name: Annotated[str, Argument(help='Profile ID or name')],
    name: Annotated[
        str | None,
        Option('--name', '-n', help='New profile name'),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Option('--tags', '-T', help='OS/locale tag; replaces all existing tags (repeatable)'),
    ] = None,
    timeout: Annotated[
        int | None,
        Option('--timeout', '-t', help='Analysis timeout in seconds', min=1, max=3600),
    ] = None,
    network: OPT_SANDBOX_NETWORK = None,
    geolocation: Annotated[
        list[str] | None,
        Option('--geolocation', help='VPN country code; requires a vpn network (repeatable)'),
    ] = None,
    browser: OPT_SANDBOX_BROWSER = None,
    unset: OPT_PROFILE_UNSET = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    _require_non_empty(name=name, tags=tags)
    supplied = {'network': network, 'browser': browser, 'geolocation': geolocation}
    if not any([name, tags, timeout, *supplied.values(), unset]):
        raise BadParameter('nothing to update — supply at least one field option or --unset')
    conflicts = sorted(f for f, v in supplied.items() if v is not None and f in (unset or []))
    if conflicts:
        raise BadParameter(f'cannot both set and unset: {", ".join(conflicts)}')
    if geolocation and (network is not None and network != 'vpn' or 'network' in (unset or [])):
        raise BadParameter('--geolocation requires --network vpn')
    update_sandbox_profile(
        profile_id_or_name,
        name=name,
        tags=tags,
        timeout=timeout,
        network=network,
        geolocation=geolocation,
        browser=browser,
        unset=unset,
        pretty=pretty,
    )


@banshee_cmd(
    app=profile_app,
    name='delete',
    help_=_HELP_PROFILE_DELETE,
    epilog=EPILOG_SANDBOX_PROFILE_DELETE,
)
def delete(
    profile_id_or_name: Annotated[str, Argument(help='Profile ID or name')],
    yes: Annotated[
        bool,
        Option('--yes', '-y', help='Delete without asking for confirmation'),
    ] = False,
):
    if not yes:
        confirm(f'Delete profile {profile_id_or_name!r}?', abort=True)
    delete_sandbox_profile(profile_id_or_name)


@banshee_cmd(
    app=app,
    name='list',
    help_=_HELP_LIST,
    epilog=EPILOG_SANDBOX_LIST,
    rich_help_panel=_PANEL_SUBMISSION,
)
def list_samples(
    subset: OPT_SANDBOX_SUBSET = 'org',
    limit: Annotated[
        int,
        Option('--limit', '-l', help='Maximum number of samples to return', min=1, max=4095),
    ] = 20,
    pretty: OPT_PRETTY_PRINT = False,
):
    list_sandbox_samples(subset=subset, limit=limit, pretty=pretty)


@banshee_cmd(
    app=app,
    name='submit',
    help_=_HELP_SUBMIT,
    epilog=EPILOG_SANDBOX_SUBMIT,
    rich_help_panel=_PANEL_SUBMISSION,
)
def submit(
    target: Annotated[
        str,
        Argument(help='File path, URL, or public sample ID (with --import)'),
    ],
    fetch: Annotated[
        bool,
        Option('--fetch', help='Download the URL target first, then analyse the downloaded file'),
    ] = False,
    import_: Annotated[
        bool,
        Option('--import', help='Treat the target as a public sample ID to import'),
    ] = False,
    profile: Annotated[
        list[str] | None,
        Option('--profile', help='Analysis profile name or ID (repeatable)'),
    ] = None,
    timeout: Annotated[
        int | None,
        Option('--timeout', '-t', help='Analysis timeout in seconds', min=1, max=3600),
    ] = None,
    network: OPT_SANDBOX_NETWORK = None,
    geolocation: Annotated[
        str | None,
        Option('--geolocation', help='VPN exit country code; requires --network vpn'),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Option('--tags', '-T', help='Custom tag attached to the submission (repeatable)'),
    ] = None,
    password: Annotated[
        str | None,
        Option('--password', help='Password for protected archives'),
    ] = None,
    wait: Annotated[
        bool,
        Option('--wait', '-w', help='Wait for analysis to finish and print the overview report'),
    ] = False,
    interactive: Annotated[
        bool,
        Option(
            '--interactive',
            '-i',
            help='Pause at static analysis and prompt for file and profile selection',
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):
    _require_non_empty(profile=profile, tags=tags, geolocation=geolocation, password=password)
    if fetch and import_:
        raise BadParameter('--fetch and --import are mutually exclusive')
    if interactive and profile:
        raise BadParameter('--interactive and --profile are mutually exclusive')
    if geolocation and network != 'vpn':
        raise BadParameter('--geolocation requires --network vpn')
    submit_sandbox_sample(
        target,
        fetch=fetch,
        import_=import_,
        profiles=profile,
        timeout=timeout,
        network=network,
        geolocation=geolocation,
        tags=tags,
        password=password,
        wait=wait,
        interactive=interactive,
        pretty=pretty,
    )


@banshee_cmd(
    app=app,
    name='set-profile',
    help_=_HELP_SET_PROFILE,
    epilog=EPILOG_SANDBOX_SET_PROFILE,
    rich_help_panel=_PANEL_SUBMISSION,
)
def set_profile(
    sample_id: Annotated[str, Argument(help='Sandbox sample ID')],
    auto: Annotated[
        bool,
        Option('--auto', '-a', help='Let the sandbox auto-select profiles for all files'),
    ] = False,
    pick: Annotated[
        list[str] | None,
        Option(
            '--pick',
            help='Map a file to a profile: FILE:PROFILE (repeatable)',
            metavar='FILE:PROFILE',
        ),
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    if auto and pick:
        raise BadParameter('--auto and --pick are mutually exclusive')
    if not auto and not pick:
        raise BadParameter('provide either --auto or at least one --pick FILE:PROFILE')
    for raw in pick or []:
        file_, sep, profile = raw.partition(':')
        if not sep or not file_ or not profile:
            raise BadParameter(f'--pick value must be FILE:PROFILE, got: {raw!r}')
    set_sandbox_sample_profile(sample_id, auto=auto, picks=pick, pretty=pretty)


@banshee_cmd(
    app=report_app,
    name='overview',
    help_=_HELP_REPORT_OVERVIEW,
    epilog=EPILOG_SANDBOX_REPORT_OVERVIEW,
)
def overview(
    sample_id: Annotated[str, Argument(help='Sandbox sample ID')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_overview_report(sample_id, pretty=pretty)


@banshee_cmd(
    app=report_app,
    name='static',
    help_=_HELP_REPORT_STATIC,
    epilog=EPILOG_SANDBOX_REPORT_STATIC,
)
def static(
    sample_id: Annotated[str, Argument(help='Sandbox sample ID')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_static_report(sample_id, pretty=pretty)


@banshee_cmd(
    app=report_app,
    name='behavioral',
    help_=_HELP_REPORT_BEHAVIORAL,
    epilog=EPILOG_SANDBOX_REPORT_BEHAVIORAL,
)
def behavioral(
    sample_id: Annotated[str, Argument(help='Sandbox sample ID')],
    pretty: OPT_PRETTY_PRINT = False,
):
    fetch_behavioral_reports(sample_id, pretty=pretty)


app.add_typer(
    profile_app,
    name='profile',
    help='Manage analysis profiles',
    rich_help_panel=_PANEL_PROFILE_MGMT,
)
app.add_typer(
    report_app,
    name='report',
    help='Sample analysis reports',
    rich_help_panel=_PANEL_REPORTS,
)
