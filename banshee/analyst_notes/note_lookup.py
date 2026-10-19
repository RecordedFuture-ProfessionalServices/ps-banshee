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

from psengine.analyst_notes import AnalystNoteLookupError, AnalystNoteMgr
from rich import print_json

from ..formatters.output_formatters import format_line, format_time
from .helpers import sanitize_csv_field


def lookup_note(
    note_id: str,
    tagged_text: bool,
    pretty: bool,
):
    """Lookup a singular analyst note."""
    note_manager = AnalystNoteMgr()

    try:
        note = note_manager.lookup(note_id=note_id, tagged_text=tagged_text)
    except AnalystNoteLookupError as err:
        raise err

    if not pretty:
        print_json(data=note.json(), indent=2)

    else:
        print(format_line('Id', note.id_))
        print(format_line('Title', note.attributes.title))
        print(format_line('Published', format_time(note.attributes.published)))
        print(format_line('Source Name', note.source.name))
        print(format_line('Note', sanitize_csv_field(note.attributes.text)))
        print()
