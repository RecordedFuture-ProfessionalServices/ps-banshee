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

from pathlib import Path
from typing import Annotated

from typer import Argument, BadParameter, Option, Typer

from ..analyst_notes.note_attachment import fetch_note_attachment
from ..analyst_notes.note_lookup import lookup_note
from ..analyst_notes.note_search import search_notes
from ..branding import banshee_cmd
from .args import OPT_PRETTY_PRINT

CMD_NAME = 'analyst-notes'
CMD_HELP = 'Fetch and create Analyst Notes'
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


@banshee_cmd(app=app, help_='Search for analyst Notes', epilog='')
def search(
    published: Annotated[
        str,
        Option(
            '--published',
            '-p',
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
            '-t',
            help='Filter for alerts with specific topics',
            show_default=False,
        ),
    ] = None,
    label: Annotated[
        list[str],
        Option(
            '--label',
            '-l',
            help='Recorded Future Note topics (repetable)',
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
