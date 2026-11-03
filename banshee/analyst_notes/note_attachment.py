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

import sys
from pathlib import Path

from psengine.analyst_notes import AnalystNoteAttachmentError, AnalystNoteMgr, save_attachment
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


def fetch_note_attachment(
    note_ids: list[str],
    output_dir: Path,
):
    """Save Analyst Note Attachments."""
    note_manager = AnalystNoteMgr()
    saved_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(f'Fetching {len(note_ids)} Analyst Note attachments', total=len(note_ids))

        for note_id in note_ids:
            try:
                attachment, extension = note_manager.fetch_attachment(note_id)
            except AnalystNoteAttachmentError:
                print(f'No attachment found for "{note_id}"')
                attachment, extension = None, None

            if attachment and extension:
                save_attachment(note_id, attachment, extension, output_dir)
                saved_count += 1

        if saved_count < len(note_ids):
            print(
                f'Warning: {saved_count} out of {len(note_ids)} note attachments were saved.',
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            print(f'Saved {saved_count} note attachments to disk.')
