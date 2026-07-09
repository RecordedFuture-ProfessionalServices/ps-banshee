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
import math
import sys
from email.utils import parsedate_to_datetime

from psengine.fusion import FusionMgr
from rich import print_json
from rich.console import Console

_BAR_MAX_WIDTH = 24
_BAR_EIGHTHS = '▏▎▍▌▋▊▉'


def _bar(count: int, max_count: int, width: int = _BAR_MAX_WIDTH) -> str:
    if max_count <= 0 or count <= 0:
        return ''
    portion = count / max_count * width
    full = int(portion)
    remainder = portion - full
    frac_idx = int(remainder * 8) - 1
    bar = '█' * full
    if 0 <= frac_idx < len(_BAR_EIGHTHS):
        bar += _BAR_EIGHTHS[frac_idx]
    return bar


def _compute_stats(counts: dict[int, int]) -> dict:
    total = sum(counts.values())
    if total == 0:
        return {}

    scores_sorted = sorted(counts)
    weighted_sum = sum(s * counts[s] for s in scores_sorted)
    mean = weighted_sum / total

    def percentile(p: float) -> int:
        target = math.ceil(p * total)
        running = 0
        for s in scores_sorted:
            running += counts[s]
            if running >= target:
                return s
        return scores_sorted[-1]

    mode_score = max(counts, key=lambda s: counts[s])
    return {
        'total': total,
        'mean': f'{mean:.1f}',
        'median': percentile(0.5),
        'mode': mode_score,
        'p95': percentile(0.95),
        'p99': percentile(0.99),
    }


def _summary_line(counts: dict[int, int]) -> str:
    stats = _compute_stats(counts)
    if not stats:
        return ''
    return (
        f'{stats["total"]:,} entries · '
        f'mean {stats["mean"]} · '
        f'median {stats["median"]} · '
        f'mode {stats["mode"]} · '
        f'p95 {stats["p95"]} · '
        f'p99 {stats["p99"]}'
    )


_INDENT = '  '


def _print_metadata_block(rows: list[tuple[str, str]], console: Console = None) -> None:
    if not rows:
        return
    console = console or Console()
    label_w = max(len(label) for label, _ in rows)
    for label, value in rows:
        console.print(f'{_INDENT}[cyan bold]{label:<{label_w}}[/cyan bold]  {value}')


def _print_count_table(counts: dict[int, int], console: Console = None) -> None:
    if not counts:
        return
    console = console or Console()

    scores = sorted(counts)
    total = sum(counts.values())
    max_count = max(counts.values())

    rows = []
    for s in scores:
        c = counts[s]
        pct = c / total * 100 if total else 0
        rows.append(
            (
                f'{s:,}',
                f'{c:,}',
                f'{pct:.2f} %',
                _bar(c, max_count),
            )
        )

    total_label = 'Total'
    total_val = f'{total:,}'
    headers = ('Score', 'Count', 'Pct')
    w_score = max(len(headers[0]), max(len(r[0]) for r in rows), len(total_label))
    w_count = max(len(headers[1]), max(len(r[1]) for r in rows), len(total_val))
    w_pct = max(len(headers[2]), max(len(r[2]) for r in rows))
    gap = '  '

    header_line = (
        f'{_INDENT}[bold magenta]{headers[0]:>{w_score}}[/bold magenta]{gap}'
        f'[bold magenta]{headers[1]:>{w_count}}[/bold magenta]{gap}'
        f'[bold magenta]{headers[2]:>{w_pct}}[/bold magenta]'
    )
    full_rule = f'{_INDENT}{"─" * w_score}{gap}{"─" * w_count}{gap}{"─" * w_pct}'
    total_rule = f'{_INDENT}{"─" * w_score}{gap}{"─" * w_count}'

    console.print(header_line)
    console.print(full_rule)
    for s, c, p, bar in rows:
        line = (
            f'{_INDENT}[cyan bold]{s:>{w_score}}[/cyan bold]{gap}'
            f'[green bold]{c:>{w_count}}[/green bold]{gap}'
            f'{p:>{w_pct}}'
        )
        if bar:
            line += f'{gap}{bar}'
        console.print(line)
    console.print(total_rule)
    console.print(
        f'{_INDENT}[bold]{total_label:>{w_score}}[/bold]{gap}[bold]{total_val:>{w_count}}[/bold]'
    )


def _format_datetime(date_str: str) -> str:
    """Format datetime from HTTP date format to include seconds and timezone."""
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime('%b %d %H:%M:%S %Z')

    except Exception:  # noqa: BLE001
        return date_str


def stat_fusion_file(file_path: str, pretty: bool = False, counts: dict[int, int] = None):
    fusion_mgr = FusionMgr()

    head_response = fusion_mgr.head_files(file_paths=file_path)
    response = head_response[0]

    if not pretty:
        response_data = response.json()
        response_data.pop('content-disposition', None)
        response_data.pop('Content-Length', None)
        if counts is not None:
            response_data['counts'] = {str(k): counts[k] for k in sorted(counts)}
        print_json(json.dumps(response_data), indent=2)

        if not response.exists:
            sys.exit(1)
    else:
        console = Console()

        if not response.exists:
            print(f'File not found {file_path}', file=sys.stderr)
            sys.exit(1)

        metadata: list[tuple[str, str]] = [('Path', file_path)]
        if hasattr(response, 'last_modified') and response.last_modified:
            date_str = _format_datetime(response.last_modified)
            metadata.append(('Last Modified', f'[blue]{date_str}[/blue]'))
        if hasattr(response, 'etag') and response.etag:
            metadata.append(('ETag', f'[yellow]{response.etag}[/yellow]'))
        if counts:
            summary = _summary_line(counts)
            if summary:
                metadata.append(('Total', summary))

        _print_metadata_block(metadata, console)

        if counts:
            console.print()
            _print_count_table(counts, console)
