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

from psengine.config import get_config
from psengine.sandbox import SandboxMgr
from psengine.sandbox.sandbox import Sample
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

_ERR_CONSOLE = Console(stderr=True)

_DATETIME_FMT = '%Y-%m-%d %H:%M'


def _spinner(label: str = 'Fetching samples…') -> Progress:
    return Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)


def _samples_table(samples: list[Sample]) -> Table:
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold')
    tbl.add_column('Target')
    tbl.add_column('Status')
    tbl.add_column('Kind')
    tbl.add_column('Submitted')
    tbl.add_column('Completed')
    tbl.add_column('SHA256', style='dim')
    tbl.add_column('ID', style='dim')
    for s in samples:
        target = s.filename or s.url or '—'
        completed = s.completed.strftime(_DATETIME_FMT) if s.completed else '—'
        tbl.add_row(
            target,
            s.status,
            s.kind,
            s.submitted.strftime(_DATETIME_FMT),
            completed,
            s.sha256 or '—',
            s.id_,
        )
    return tbl


def list_sandbox_samples(subset: str = 'org', limit: int = 20, pretty: bool = False) -> None:
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    with _spinner():
        samples = mgr.fetch_samples(subset=subset, max_results=limit)
    if pretty:
        Console().print(_samples_table(samples))
    else:
        print_json(json.dumps([s.json() for s in samples]))
