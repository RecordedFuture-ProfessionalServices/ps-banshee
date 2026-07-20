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

import json
import sys

from psengine.config import get_config
from psengine.sandbox import ProfileUpdateOut, SandboxMgr
from psengine.sandbox.errors import ProfileCreateError, ProfileNotFoundError, ProfileUpdateError
from psengine.sandbox.sandbox import Profile
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

_ERR_CONSOLE = Console(stderr=True)


def _spinner(label: str) -> Progress:
    return Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)


def _profiles_table(profiles: list[Profile]) -> Table:
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Name', style='bold cyan')
    tbl.add_column('ID', style='dim')
    tbl.add_column('Timeout', style='yellow', justify='right')
    tbl.add_column('Network', style='blue')
    tbl.add_column('Geolocation', style='magenta')
    tbl.add_column('Browser', style='green bold')
    tbl.add_column('Tags', style='white dim')
    for p in profiles:
        tags = ', '.join(p.tags) if p.tags else '—'
        timeout = f'{p.timeout}s' if p.timeout is not None else '—'
        network = p.network or '—'
        geolocation = ', '.join(p.geolocation) if p.geolocation else '—'
        browser = (p.options.browser if p.options and p.options.browser else None) or '—'
        tbl.add_row(p.name, p.id_, timeout, network, geolocation, browser, tags)
    return tbl


def create_sandbox_profile(
    name: str,
    tags: list[str],
    timeout: int,
    network: str | None = None,
    geolocation: list[str] | None = None,
    browser: str | None = None,
    pretty: bool = False,
) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Creating profile'):
            profile = mgr.create_profile(
                name=name,
                tags=tags,
                timeout=timeout,
                network=network,
                geolocation=geolocation,
                browser=browser,
            )
    except ProfileCreateError as exc:
        _ERR_CONSOLE.print(f'[red]Profile creation failed:[/red] {exc}')
        sys.exit(1)
    if pretty:
        Console().print(_profiles_table([profile]))
    else:
        print_json(json.dumps(profile.json()))


def get_sandbox_profile(profile_id_or_name: str, pretty: bool = False) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Fetching profile'):
            profile = mgr.fetch_profile(profile_id_or_name)
    except ProfileNotFoundError as exc:
        _ERR_CONSOLE.print(f'[red]Profile not found:[/red] {exc}')
        sys.exit(1)
    if pretty:
        console = Console()
        console.print(_profiles_table([profile]))
    else:
        print_json(json.dumps(profile.json()))


def _merged(supplied, existing, cleared: bool = False):
    if cleared:
        return None
    return supplied if supplied is not None else existing


def _print_update_result(result: ProfileUpdateOut, pretty: bool) -> None:
    if pretty:
        msg = (
            '[green]Profile updated[/green]'
            if result.updated
            else '[yellow]Profile not found — nothing updated[/yellow]'
        )
        Console().print(msg)
    else:
        print_json(json.dumps(result.json()))


def update_sandbox_profile(
    profile_id_or_name: str,
    name: str | None = None,
    tags: list[str] | None = None,
    timeout: int | None = None,
    network: str | None = None,
    geolocation: list[str] | None = None,
    browser: str | None = None,
    unset: list[str] | None = None,
    pretty: bool = False,
) -> None:
    """Merge the supplied fields into the existing profile and PUT the result.

    Omitted fields keep their current values; fields listed in `unset` are cleared.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Fetching profile'):
            profile = mgr.fetch_profile(profile_id_or_name)
    except ProfileNotFoundError:
        _print_update_result(ProfileUpdateOut(updated=False), pretty)
        return

    cleared = set(unset or [])
    existing_browser = profile.options.browser if profile.options else None
    merged_timeout = _merged(timeout, profile.timeout)
    merged_network = _merged(network, profile.network, 'network' in cleared)
    merged_geolocation = _merged(geolocation, profile.geolocation, 'geolocation' in cleared) or None
    if merged_timeout is None:
        _ERR_CONSOLE.print('[red]Profile has no stored timeout — supply --timeout[/red]')
        sys.exit(1)
    # Only guard the user's explicit intent: profiles fetched from the server may
    # already hold geolocation with a non-vpn network, and inherited state must
    # not block unrelated updates -- the API stays the authority there.
    if geolocation and merged_network != 'vpn':
        _ERR_CONSOLE.print(
            '[red]Geolocation requires a vpn network[/red] — '
            f"this profile's network is {merged_network or 'not set'}; "
            'pass --network vpn together with --geolocation'
        )
        sys.exit(1)

    try:
        with _spinner('Updating profile'):
            result = mgr.update_profile(
                profile.id_,
                name=_merged(name, profile.name),
                tags=_merged(tags, profile.tags),
                timeout=merged_timeout,
                network=merged_network,
                geolocation=merged_geolocation,
                browser=_merged(browser, existing_browser, 'browser' in cleared),
            )
    except ProfileUpdateError as exc:
        _ERR_CONSOLE.print(f'[red]Profile update failed:[/red] {exc}')
        sys.exit(1)
    _print_update_result(result, pretty)


def delete_sandbox_profile(profile_id_or_name: str) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    with _spinner('Deleting profile'):
        result = mgr.delete_profile(profile_id_or_name)
    if result.deleted:
        print(f'Deleted profile: {profile_id_or_name}')
    else:
        print(f'Profile not found: {profile_id_or_name}')


def list_sandbox_profiles(pretty: bool = False) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    with _spinner('Fetching profiles'):
        profiles = mgr.fetch_profiles()
    if pretty:
        console = Console()
        console.print(_profiles_table(profiles))
    else:
        print_json(json.dumps([p.json() for p in profiles]))
