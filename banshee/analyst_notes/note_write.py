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

from psengine.analyst_notes import AnalystNoteMgr, AnalystNotePublishError

from ..formatters.output_formatters import format_line

def write_note(
    title: str,
    note_text: str,
    topic: list[str],
    context_entities: list[str],
    note_entities: list[str],
    validation_urls: list[str],
):
    """Publish an Analyst Note."""
    note_mgr = AnalystNoteMgr()

    try:
        published_note = note_mgr.publish(
            title=title,
            text=note_text,
            topic=topic,
            context_entities=context_entities,
            note_entities=note_entities,
            validation_urls=validation_urls
        )
    except AnalystNotePublishError as err:
        raise err

    print(format_line('Note published', published_note.note_id))
