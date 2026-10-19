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

from psengine.analyst_notes import AnalystNoteMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..formatters.output_formatters import format_line, format_time
from .helpers import sanitize_csv_field


def search_notes(
    published: str,
    entity: str,
    author: str,
    title: str,
    topic: list[str],
    label: str,
    source: str,
    limit: int,
    pretty: bool,
):
    """Search for analyst notes."""
    note_manager = AnalystNoteMgr()
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(description='Searching for Analyst Notes', total=None)
        results = note_manager.search(
            published=published,
            entity=entity,
            author=author,
            title=title,
            topic=topic,
            label=label,
            source=source,
            max_results=limit,
        )

    if not pretty:
        notes = [note.json() for note in results]
        print_json(json.dumps(notes), indent=2)

    else:
        for note in results:
            print(format_line('Title', note.attributes.title))
            print(format_line('Published', format_time(note.attributes.published)))
            print(format_line('Source', note.source.name))
            print(format_line('Note', sanitize_csv_field(note.attributes.text)))
            print()
