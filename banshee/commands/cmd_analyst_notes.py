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

from ..analyst_notes.helpers import URL
from ..analyst_notes.note_attachment import fetch_note_attachment
from ..analyst_notes.note_export import export_notes
from ..analyst_notes.note_delete import delete_note
from ..analyst_notes.note_lookup import lookup_note
from ..analyst_notes.note_search import search_notes
from ..analyst_notes.note_write import write_note
from ..branding import banshee_cmd
from .args import OPT_PRETTY_PRINT

CMD_NAME = 'analyst-notes'
CMD_HELP = 'Fetch, Create and Search Analyst Notes'
CMD_RICH_HELP = 'Recorded Future Analyst Notes'

CWD = Path.cwd()

NOTE_ID_INVALID_MSG = "Note ID '{}' is not valid. Alert ID should be at least 6 characters long."  # noqa: E501

app = Typer(no_args_is_help=True)


def parse_triggered(value: str):
    if not value.startswith('[') and not value.startswith('('):
        value = f'-{value.strip()}'

    return value


def validate_note_id(note_id: str):
    if len(note_id) < 6:
        raise BadParameter(NOTE_ID_INVALID_MSG.format(note_id))

    return note_id


def validate_url(url: str):
    try:
        URL(url)
    except ValueError as err:
        raise BadParameter(NOTE_ID_INVALID_MSG.format(url)) from err


def validate_list_urls(urls: list[str]):
    for this_url in urls:
        validate_url(this_url)


@banshee_cmd(app=app, help_='Search for analyst Notes', epilog='')
def search(
    published: Annotated[
        str,
        Option(
            '--published',
            '-P',
            callback=parse_triggered,
            help='Filter based on published time, e.g. 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)',  # noqa: E501
            show_default=True,
        ),
    ] = '1d',
    entity: Annotated[
        str,
        Option(
            '--entity',
            '-e',
            help='Filter for notes associated with an entity',
            show_default=False,
        ),
    ] = None,
    author: Annotated[
        str,
        Option(
            '--author',
            '-a',
            help='Filter notes based on the author',
            show_default=False,
        ),
    ] = None,
    title: Annotated[
        str,
        Option(
            '--title',
            '-t',
            help='Filter for notes with a specific title',
            show_default=False,
        ),
    ] = None,
    topic: Annotated[
        str,
        Option(
            '--topic',
            '-T',
            help='Filter for alerts with specific topics',
            show_default=False,
        ),
    ] = None,
    label: Annotated[
        list[str],
        Option(
            '--label',
            '-l',
            help='Recorded Future Note topics (repeatable)',
            show_default=False,
        ),
    ] = None,
    source: Annotated[
        str, Option('--source', '-s', help='Recorded Future Sources.', show_default=False)
    ] = None,
    limit: Annotated[
        int,
        Option(
            '--limit',
            '-l',
            help='Limit the number of alerts to return.',
            min=1,
            max=10_000,
        ),
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
        limit=limit,
        pretty=pretty,
    )


@banshee_cmd(app=app, help_='Lookup a single Analyst Note', epilog='')
def lookup(
    note_id: Annotated[
        str, Argument(help='Note ID to lookup', callback=validate_note_id, show_default=False)
    ],
    tagged_text: Annotated[
        bool,
        Option(
            '--tagged-text',
            '-t',
            help="Show Recorded Future ID's for entities within the note.",
            show_default=False,
        ),
    ] = False,
    pretty: OPT_PRETTY_PRINT = False,
):
    lookup_note(note_id=note_id, tagged_text=tagged_text, pretty=pretty)


@banshee_cmd(app=app, help_='Save attachments from an Analyst Notes', epilog='')
def fetch_attachments(
    note_id: Annotated[
        str, Argument(help='Note ID to lookup', callback=validate_note_id, show_default=False)
    ],
    output_path: Annotated[
        Path,
        Option(
            '--output-path',
            '-o',
            help='Path to save attachments',
            show_default=True,
        ),
    ] = CWD / 'attachments',
):
    fetch_note_attachment(note_id=note_id, output_path=output_path)


@banshee_cmd(app=app, help_='Publish a new Analyst Note', epilog='')
def publish(
    title: Annotated[str, Argument(show_default=False, help='Title for the Note')],
    note_text: str = Argument(
        ... if sys.stdin.isatty() else None, show_default=False, help='Note Body'
    ),
    topic: Annotated[
        list[str],
        Option(
            '--topic',
            '-t',
            help='One or more topics to associate with the note',
            show_default=False,
        ),
    ] = None,
    context_entities: Annotated[
        list[str],
        Option(
            '--context-entities',
            '-c',
            help='One or more context entities to associate with the note',
            show_default=False,
        ),
    ] = None,
    note_entities: Annotated[
        list[str],
        Option(
            '--note-entities',
            '-e',
            help='One or more entities to associate with the note',
            show_default=False,
        ),
    ] = None,
    validation_urls: Annotated[
        list[str],
        Option(
            '--validation-urls',
            '-v',
            help='One or more URLs to associate with the note',
            show_default=False,
        ),
    ] = None,
):
    if note_text:
        note_text = sys.stdin.read()

    if note_entities and context_entities:
        raise BadParameter('Either "note-entities" or "context-entities" must be provided')

    if not validation_urls:
        validate_list_urls(validation_urls)

    write_note(
        title=title,
        note_text=note_text,
        topic=topic,
        context_entities=context_entities,
        note_entities=note_entities,
        validation_urls=validation_urls,
    )


@banshee_cmd(app=app, help_='Delete an Analyst Note', epilog='')
def delete(
    note_id: Annotated[
        str, Argument(help='Note ID to lookup', callback=validate_note_id, show_default=False)
    ],
):
    delete_note(note_id)

_PIPED_INPUT_HINT = (
    "Expected piped JSON output from 'banshee analyst-notes search' "
    "(e.g. 'banshee analyst-notes search -t 1d | banshee analyst-notes export')."
)

def _parse_search_notes(value: str):
    if not value:
        raise BadParameter(f'No input received. {_PIPED_INPUT_HINT}')

    try:
        notes = json.loads(value)
    except json.JSONDecodeError as err:
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

@banshee_cmd(app=app, help_="Export Analyst Notes as JSON or CSV", epilog='')
def export(
        csv_flag: Annotated[
            bool,
            Option(
                '--csv',
                help='Export as CSV (Fixed column set) instead of JSON (Full note details).',
                show_default=False
            )
        ] = False,
):
    if sys.stdin.isatty():
        raise BadParameter(f'No Input received. {_PIPED_INPUT_HINT}')

    raw_notes = sys.stdin.read().strip()

    note_ids = _parse_search_notes(raw_notes)

    export_notes(note_ids, csv_flag)