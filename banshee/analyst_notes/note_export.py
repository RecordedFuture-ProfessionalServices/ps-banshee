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

import json

from psengine.analyst_notes import AnalystNoteLookupError, AnalystNoteMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .helpers import format_as_csv


def _get_note(note_id: str, manager: AnalystNoteMgr):
    """Get a singular analyst note."""
    try:
        return manager.lookup(note_id)
    except AnalystNoteLookupError as err:
        raise err from note_id


def export_notes(
    note_ids: list[str],
    csv_flag: bool,
):
    """Lookup multiple analyst notes."""
    note_manager = AnalystNoteMgr()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(f'Fetching {len(note_ids)} analyst notes', total=len(note_ids))

        notes = [_get_note(note_id, note_manager) for note_id in note_ids]

    if csv_flag:
        format_as_csv(notes)
    else:
        notes = [note.json() for note in notes]
        print_json(json.dumps(notes, indent=2))
