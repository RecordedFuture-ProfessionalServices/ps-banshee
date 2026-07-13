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
from psengine.sandbox import SandboxMgr
from psengine.sandbox.errors import ProfileNotFoundError
from psengine.sandbox.sandbox import Profile
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

_ERR_CONSOLE = Console(stderr=True)


def _spinner(label: str = 'Fetching profiles…') -> Progress:
    return Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)


def _profiles_table(profiles: list[Profile]) -> Table:
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold')
    tbl.add_column('Name')
    tbl.add_column('ID', style='dim')
    tbl.add_column('Timeout', justify='right')
    tbl.add_column('Network')
    tbl.add_column('Geolocation')
    tbl.add_column('Browser')
    tbl.add_column('Tags')
    for p in profiles:
        tags = ', '.join(p.tags) if p.tags else '—'
        timeout = f'{p.timeout}s' if p.timeout is not None else '—'
        network = p.network or '—'
        geolocation = ', '.join(p.geolocation) if p.geolocation else '—'
        browser = (p.options.browser if p.options and p.options.browser else None) or '—'
        tbl.add_row(p.name, p.id_, timeout, network, geolocation, browser, tags)
    return tbl


def get_sandbox_profile(profile_id_or_name: str, pretty: bool = False) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Fetching profile…'):
            profile = mgr.fetch_profile(profile_id_or_name)
    except ProfileNotFoundError as exc:
        _ERR_CONSOLE.print(f'Profile not found: {exc}')
        sys.exit(1)
    if pretty:
        console = Console()
        console.print(_profiles_table([profile]))
    else:
        print_json(json.dumps(profile.json()))


def list_sandbox_profiles(pretty: bool = False) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    with _spinner():
        profiles = mgr.fetch_profiles()
    if pretty:
        console = Console()
        console.print(_profiles_table(profiles))
    else:
        print_json(json.dumps([p.json() for p in profiles]))
