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

from pathlib import Path

from psengine.analyst_notes import AnalystNoteAttachmentError, AnalystNoteMgr, save_attachment


def fetch_note_attachment(
    note_id: str,
    output_path: Path,
):
    """Save Analyst Note Attachments."""
    note_manager = AnalystNoteMgr()

    try:
        attachment, extension = note_manager.fetch_attachment(note_id)
    except AnalystNoteAttachmentError:
        print(f'No attachment found for {note_id}')
        return

    if attachment and extension:
        save_attachment(note_id, attachment, extension, output_path)
        print(f'Saved attachment for {note_id}')

    else:
        print(f'No attachment found for {note_id}')
