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

from psengine.analyst_notes import AnalystNoteDeleteError, AnalystNoteMgr

from ..formatters.output_formatters import format_line


def delete_note(note_id: str):
    """Delete a single analyst note."""
    note_manager = AnalystNoteMgr()

    try:
        deleted_note = note_manager.delete(note_id=note_id)
    except AnalystNoteDeleteError as err:
        raise err

    if delete_note:
        print(format_line('Deleted Note', note_id))
    else:
        print(format_line('Unable to Delete Note', deleted_note.note_id))
