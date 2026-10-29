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
from pathlib import Path
from typing import Annotated

from typer import Argument, BadParameter, Option, Typer

from ..analyst_notes.note_attachment import fetch_note_attachment
from ..analyst_notes.note_delete import delete_note
from ..analyst_notes.note_export import export_notes
from ..analyst_notes.note_lookup import lookup_note
from ..analyst_notes.note_publish import publish_note
from ..analyst_notes.note_search import search_notes
from ..branding import banshee_cmd
from .args import OPT_PRETTY_PRINT
from .epilogs import (
    EPILOG_ANALYST_NOTE_ATTACHMENT,
    EPILOG_ANALYST_NOTE_DELETE,
    EPILOG_ANALYST_NOTE_EXPORT,
    EPILOG_ANALYST_NOTE_LOOKUP,
    EPILOG_ANALYST_NOTE_PUBLISH,
    EPILOG_ANALYST_NOTE_SEARCH,
)

CMD_NAME = 'analyst-notes'
CMD_HELP = 'Fetch and manage Analyst notes'
CMD_RICH_HELP = 'Recorded Future Analyst notes'

app = Typer(no_args_is_help=True)


_PIPED_INPUT_HINT = (
    "Expected piped JSON output from 'banshee analyst-notes search' "
    "(e.g. 'banshee analyst-notes search -P -1d | banshee analyst-notes export')"
)
NOTE_ID_INVALID_MSG = (
    "Note ID '{}' is not valid. Note ID should be 7 characters long or 11 with 'doc:' prefix."  # noqa: E501
)

_PIPED_PUBLISH_HINT = (
    'Expected note text to be passed via command or piped in.'
    ' (e.g. \'banshee analyst-note publish "A Note" -e idn:example.url < note_text.txt\' or '
    ' \'banshee analyst-note publish "A Note" "Note Text" -e idn:example.url\''
)


def validate_time_search(value: str):
    if not value.startswith('-'):
        value = '-' + value

    return value


def validate_note_id(note_id: str):
    if len(note_id) == 7:
        note_id = 'doc:' + note_id
    if len(note_id) != 11 or not note_id.startswith('doc:'):
        raise BadParameter(NOTE_ID_INVALID_MSG.format(note_id))

    return note_id


def parse_search_notes(value: str):
    if not value:
        raise BadParameter(f'No input received. {_PIPED_INPUT_HINT}')

    try:
        notes = json.loads(value)
    except json.decoder.JSONDecodeError as err:
        raise BadParameter(
            f'Malformed input: could not parse as JSON ({err.msg}). {_PIPED_INPUT_HINT}'
        ) from err

    if not isinstance(notes, list):
        raise BadParameter(
            f'Malformed input: expected a JSON array, got {type(notes).__name__}. '
            f'{_PIPED_INPUT_HINT}'
        )

    try:
        note_ids = [note['id'] for note in notes]
    except (KeyError, TypeError) as err:
        raise BadParameter(
            f'Malformed input: every note object must have an "id" field. {_PIPED_INPUT_HINT}'
        ) from err

    for note_id in note_ids:
        validate_note_id(note_id)

    return note_ids


def _parse_note_id_input(note_ids: list[str]):
    if not note_ids:
        raise BadParameter('No Note IDs supplied')

    for note_id in note_ids:
        validate_note_id(note_id)

    return note_ids


@banshee_cmd(app=app, help_='Search for Analyst notes', epilog=EPILOG_ANALYST_NOTE_SEARCH)
def search(
    published: Annotated[
        str,
        Option(
            '-P',
            '--published',
            help='Filter on triggered time, e.g. -1d; -12h',
            callback=validate_time_search,
            show_default=True,
        ),
    ] = '-1d',
    entity: Annotated[
        str,
        Option(
            '-e',
            '--entity',
            help='Filter notes for specific entities (Recorded Future ID)',
            show_default=False,
        ),
    ] = None,
    author: Annotated[
        str,
        Option(
            '-a',
            '--author',
            help='Filter notes for specific authors (Recorded Future ID)',
            show_default=False,
        ),
    ] = None,
    title: Annotated[
        str,
        Option('-t', '--title', help='Filter notes for specific titles', show_default=False),
    ] = None,
    topic: Annotated[
        list[str],
        Option(
            '-T',
            '--topic',
            help='Filter notes for specific topics',
            show_default=False,
        ),
    ] = None,
    label: Annotated[
        str,
        Option(
            '-l',
            '--label',
            help='Filter notes for specific labels',
            show_default=False,
        ),
    ] = None,
    source: Annotated[
        str,
        Option(
            '-s',
            '--source',
            help='Filter notes for specific sources',
            show_default=False,
        ),
    ] = None,
    max_results: Annotated[
        int,
        Option('-r', '--max_results', help='Limit the number of notes returned', min=1, max=1000),
    ] = 100,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_notes(
        published=published,
        entity=entity,
        author=author,
        title=title,
        topic=topic,
        label=label,
        source=source,
        max_results=max_results,
        pretty=pretty,
    )


@banshee_cmd(app=app, help_='Lookup a single Analyst Note', epilog=EPILOG_ANALYST_NOTE_LOOKUP)
def lookup(
    note_id: Annotated[
        str, Argument(help='Note ID to lookup', callback=validate_note_id, show_default=False)
    ],
    tagged_text: Annotated[
        bool,
        Option(
            '-t',
            '--tagged_text',
            help='Add Recorded Future IDs to entities',
            show_default=False,
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):
    lookup_note(
        note_id=note_id,
        tagged_text=tagged_text,
        pretty=pretty,
    )


@banshee_cmd(app=app, help_='Delete an Analyst Note', epilog=EPILOG_ANALYST_NOTE_DELETE)
def delete(
    note_id: Annotated[
        str, Argument(help='Note ID to delete', callback=validate_note_id, show_default=False)
    ],
):
    delete_note(note_id)


@banshee_cmd(app=app, help_='Publish an Analyst Note', epilog=EPILOG_ANALYST_NOTE_PUBLISH)
def publish(
    title: Annotated[
        str,
        Argument(help='Title for the created analyst note', show_default=False),
    ],
    note_text: Annotated[
        str,
        Argument(help='The note text to publish', show_default=False),
    ] = None,
    topic: Annotated[
        list[str],
        Option(
            '-t',
            '--topic',
            help='Topic to associate with the created note',
            show_default=False,
        ),
    ] = None,
    note_entities: Annotated[
        list[str],
        Option(
            '-e',
            '--note_entities',
            help='Entities within the created note',
            show_default=False,
        ),
    ] = None,
    context_entities: Annotated[
        list[str],
        Option(
            '-c',
            '--context_entities',
            help='Context entities to associate with the created note',
            show_default=False,
        ),
    ] = None,
    validation_urls: Annotated[
        list[str],
        Option(
            '-v',
            '--validation_urls',
            help='Validation URLs to associate with the created note',
            show_default=False,
        ),
    ] = None,
):
    if not context_entities and not note_entities:
        raise BadParameter('Either `--context_entities` or `--note_entities` must be provided')

    if note_text is None:
        if sys.stdin.isatty():
            raise BadParameter(f'No note text supplied. {_PIPED_PUBLISH_HINT}')
        note_text = sys.stdin.read().strip()

    if not note_text:
        raise BadParameter(f'No note text supplied. {_PIPED_PUBLISH_HINT}')

    publish_note(
        title=title,
        note_text=note_text,
        topic=topic,
        note_entities=note_entities,
        context_entities=context_entities,
        validation_urls=validation_urls,
    )


@banshee_cmd(
    app=app,
    help_='Save Attachments associated with a note',
    epilog=EPILOG_ANALYST_NOTE_ATTACHMENT,
)
def attachment(
    note_ids: list[str] = Argument(  # noqa: B008
        None, show_default=False, help='One or more whitespace separated Note IDs to fetch'
    ),
    output_dir: Annotated[
        Path,
        Option(
            '-d',
            '--output-dir',
            help='Directory to save the note attachments (created if missing)',
            show_default=False,
        ),
    ] = None,
):
    if output_dir is None:
        raise BadParameter('`--output-dir` is required')

    if not note_ids:
        if sys.stdin.isatty():
            raise BadParameter('No Note IDs supplied')

        raw = sys.stdin.read().strip()
        note_ids = parse_search_notes(raw) if raw.startswith('[') else raw.split()

    note_ids = _parse_note_id_input(note_ids)

    fetch_note_attachment(note_ids=note_ids, output_dir=output_dir)


@banshee_cmd(
    app=app, help_='Export Analyst Notes as JSON or CSV', epilog=EPILOG_ANALYST_NOTE_EXPORT
)
def export(
    csv_flag: Annotated[
        bool,
        Option(
            '-c',
            '--csv',
            help='Format the output as CSV',
            show_default=False,
        ),
    ] = False,
):
    if sys.stdin.isatty():
        raise BadParameter(f'No input received! {_PIPED_INPUT_HINT}')

    raw_notes = sys.stdin.read().strip()

    note_ids = parse_search_notes(raw_notes)

    export_notes(
        note_ids=note_ids,
        csv_flag=csv_flag,
    )
