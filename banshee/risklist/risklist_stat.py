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

from ..fusion_files import stat_fusion_file
from ..fusion_files.feed_stat import (
    _print_count_table,
    _print_metadata_block,
    _summary_line,
)


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


def _fetch_counts(
    entity_type=None, list_: str = None, custom_list_path: str = None
) -> dict[int, int]:
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        progress.add_task(description='Computing risk score distribution')
        if custom_list_path:
            return _count_custom_risklist(custom_list_path)
        return _count_api_risklist(list_, entity_type.value)


def stat_risklist(
    entity_type: str = None,
    list_: str = None,
    custom_list_path: str = None,
    pretty: bool = False,
    count: bool = False,
):
    counts = None
    if count:
        counts = _fetch_counts(
            entity_type=entity_type, list_=list_, custom_list_path=custom_list_path
        )

    if custom_list_path:
        stat_fusion_file(file_path=custom_list_path, pretty=pretty, counts=counts)
    else:
        entity_type = entity_type.value
        rf_client = RFClient()
        url = f'https://api.recordedfuture.com/v2/{entity_type}/risklist'
        params = {'list': list_}

        response = rf_client.request('HEAD', url, params=params)
        title = list_ if list_.endswith('_risklist') else f'{list_}_{entity_type}_risklist'

        if not pretty:
            filtered_headers = {
                'name': title,
                'exists': response.status_code == 200,
                'etag': response.headers.get('etag', '').strip('"'),
            }
            if counts is not None:
                filtered_headers['counts'] = {str(k): counts[k] for k in sorted(counts)}
            print_json(json.dumps(filtered_headers, indent=2))
        else:
            console = Console()
            metadata: list[tuple[str, str]] = []
            if list_:
                metadata.append(('Name', title))
            if 'etag' in response.headers:
                etag = response.headers['etag'].strip('"')
                metadata.append(('ETag', f'[yellow]{etag}[/yellow]'))
            if counts:
                summary = _summary_line(counts)
                if summary:
                    metadata.append(('Total', summary))

            _print_metadata_block(metadata, console)

            if counts:
                console.print()
                _print_count_table(counts, console)
