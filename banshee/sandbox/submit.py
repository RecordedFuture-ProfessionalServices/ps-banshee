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
from psengine.sandbox.errors import SampleProfileError
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

_ERR_CONSOLE = Console(stderr=True)


def _spinner(label: str = 'Setting profile…') -> Progress:
    return Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)


def _parse_picks(picks: list[str]) -> list[dict]:
    return [
        {'pick': file_, 'profile': profile}
        for file_, _, profile in (raw.partition(':') for raw in picks)
    ]


def set_sandbox_sample_profile(
    sample_id: str,
    auto: bool,
    picks: list[str] | None,
    pretty: bool = False,
) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    profiles = _parse_picks(picks) if picks else None
    try:
        with _spinner():
            result = mgr.set_sample_profile(sample_id, auto=auto, profiles=profiles)
    except SampleProfileError as exc:
        _ERR_CONSOLE.print(f'[red]Profile assignment failed:[/red] {exc}')
        sys.exit(1)
    if pretty:
        console = Console()
        msg = 'Profile assigned successfully' if result.success else 'Profile assignment failed'
        console.print(msg)
    else:
        print_json(json.dumps(result.json()))
