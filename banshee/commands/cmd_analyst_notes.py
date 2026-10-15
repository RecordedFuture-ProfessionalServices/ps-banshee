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

from typing import Annotated

from typer import Option, Typer

from ..analyst_notes.note_search import search_notes
from ..branding import banshee_cmd
from .args import OPT_PRETTY_PRINT

CMD_NAME = 'analyst-notes'
CMD_HELP = 'Fetch and create Analyst Notes'
CMD_RICH_HELP = 'Recorded Future Analyst Notes'

app = Typer(no_args_is_help=True)


def parse_triggered(value: str):
    if not value.startswith('[') and not value.startswith('('):
        value = f'-{value.strip()}'

    return value


@banshee_cmd(app=app, help_='Search for analyst Notes', epilog='')
def search(
    published: Annotated[
        str,
        Option(
            '--published',
            '-p',
            callback=parse_triggered,
            help='Filter based on published time, e.g. 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)', # noqa: E501
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
