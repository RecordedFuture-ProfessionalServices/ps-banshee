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


import csv
import io
import json
import sys

from psengine.fusion import FusionMgr
from psengine.rf_client import RFClient
from psengine.risklists import RisklistMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..fusion_files import stat_fusion_file


def _print_count_table(title: str, counts: dict[int, int]):
    console = Console()
    table = Table(title=title)
    table.add_column('Risk Score', style='cyan', justify='right')
    table.add_column('Count', style='white', justify='right')

    total = 0
    for score in sorted(counts):
        table.add_row(str(score), str(counts[score]))
        total += counts[score]

    table.add_section()
    table.add_row('Total', str(total), style='bold')
    console.print(table)


def _count_from_rows(rows) -> dict[int, int]:
    if not rows:
        print('Risk list is empty', file=sys.stderr)
        sys.exit(1)

    header = rows[0]
    try:
        risk_idx = header.index('Risk')
    except ValueError:
        print("Risk list has no 'Risk' column", file=sys.stderr)
        sys.exit(1)

    counts: dict[int, int] = {}
    for row in rows[1:]:
        try:
            score = int(row[risk_idx])
        except (ValueError, IndexError):
            continue
        counts[score] = counts.get(score, 0) + 1
    return counts


def _count_api_risklist(list_: str, entity_type: str) -> dict[int, int]:
    mgr = RisklistMgr()
    csv.field_size_limit(4 * 131072)  # 512KB
    rows = list(mgr.fetch_risklist(list_, entity_type, headers=False))
    return _count_from_rows(rows)


def _count_custom_risklist(custom_list_path: str) -> dict[int, int]:
    mgr = FusionMgr()
    response = mgr.get_files(custom_list_path)[0]
    if not response.exists:
        print(f"Risklist '{custom_list_path}' not found", file=sys.stderr)
        sys.exit(1)

    content = response.content.decode('utf-8', errors='replace')
    rows = list(csv.reader(io.StringIO(content)))
    return _count_from_rows(rows)


def count_risklist(
    entity_type: str = None, list_: str = None, custom_list_path: str = None
):
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description='Fetching risklist')
        if custom_list_path:
            title = custom_list_path
            counts = _count_custom_risklist(custom_list_path)
        else:
            entity_type = entity_type.value
            title = f'{list_}_{entity_type}_risklist'
            counts = _count_api_risklist(list_, entity_type)

    _print_count_table(title, counts)


def stat_risklist(
    entity_type: str = None,
    list_: str = None,
    custom_list_path: str = None,
    pretty: bool = False,
    count: bool = False,
):
    if count:
        count_risklist(
            entity_type=entity_type, list_=list_, custom_list_path=custom_list_path
        )
        return

    if custom_list_path:
        stat_fusion_file(file_path=custom_list_path, pretty=pretty)
    else:
        entity_type = entity_type.value
        rf_client = RFClient()
        url = f'https://api.recordedfuture.com/v2/{entity_type}/risklist'
        params = {'list': list_}

        response = rf_client.request('HEAD', url, params=params)

        if not pretty:
            filtered_headers = {
                'name': f'{list_}_{entity_type}_risklist',
                'exists': response.status_code == 200,
                'etag': response.headers.get('etag', '').strip('"'),
            }
            print_json(json.dumps(filtered_headers, indent=2))
        else:
            console = Console()
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column('Property', style='cyan bold', no_wrap=True)
            table.add_column('Value', style='white')

            if list_:
                table.add_row('Name:', f'{list_}_{entity_type}_risklist')

            if 'etag' in response.headers:
                etag = response.headers['etag'].strip('"')
                table.add_row('ETag:', f'[yellow]{etag}[/yellow]')

            console.print(table)
