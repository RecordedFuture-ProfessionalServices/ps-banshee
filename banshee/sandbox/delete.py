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

from psengine.config import get_config
from psengine.sandbox import SandboxMgr
from psengine.sandbox.errors import SampleDeleteError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


def _spinner(label: str) -> Progress:
    progress = Progress(
        SpinnerColumn(), TextColumn(label), transient=True, console=Console(stderr=True)
    )
    progress.add_task('')
    return progress


def delete_sandbox_sample(sample_id: str) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Deleting sample'):
            mgr.delete_sample(sample_id)
    except SampleDeleteError as exc:
        Console(stderr=True).print(f'[red]Delete failed:[/red] {exc}')
        sys.exit(1)
    Console().print(f'Deleted: {sample_id}')
