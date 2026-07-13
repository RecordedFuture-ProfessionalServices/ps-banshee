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

from psengine.config import get_config
from psengine.sandbox import OverviewReport, SandboxMgr, StaticAnalysisReport
from psengine.sandbox.errors import (
    SampleOverviewError,
    SampleReportNotAvailableError,
    SampleReportNotFoundError,
    SampleStaticReportError,
)
from rich import print_json
from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .output import _DISPLAY_CAP, _MORE_MSG, _SCORE_COLORS

_ERR_CONSOLE = Console(stderr=True)

_SCORE_BUCKETS = (
    (8, 'malicious'),
    (5, 'suspicious'),
    (3, 'potentially_suspicious'),
    (1, 'clean'),
)
_SCORE_LABELS = {
    'malicious': 'MALICIOUS',
    'suspicious': 'SUSPICIOUS',
    'potentially_suspicious': 'LIKELY BENIGN',
    'clean': 'NO THREAT',
    'unknown': 'UNKNOWN',
}
_HASH_PREVIEW_LEN = 16
_IOC_PREVIEW_LEN = 60


def _spinner(label: str = 'Fetching overview report…') -> Progress:
    return Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)


def _score_bucket(score: int | None) -> str:
    if score is not None:
        for threshold, bucket in _SCORE_BUCKETS:
            if score >= threshold:
                return bucket
    return 'unknown'


def _joined_capped(items: list[str], sep: str = ', ') -> str:
    """Join up to the display cap, markup-escaping each item; note how many were dropped."""
    text = sep.join(escape(item) for item in items[:_DISPLAY_CAP])
    extra = len(items) - _DISPLAY_CAP
    if extra > 0:
        text += f' [dim]+{extra} more[/dim]'
    return text


def _elide(value: str, keep: int) -> str:
    return f'{value[:keep]}…' if len(value) > keep else value


def _print_header(console: Console, report: OverviewReport) -> None:
    analysis = report.analysis
    bucket = _score_bucket(analysis.score)
    color = _SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '—'
    console.print(
        f'[bold]Sample {escape(report.sample.id_)}[/bold] — '
        f'[bold {color}]SCORE {score} {_SCORE_LABELS[bucket]}[/bold {color}]'
    )
    parts = []
    if analysis.family:
        parts.append(f'Family: [cyan]{escape(", ".join(analysis.family))}[/cyan]')
    if analysis.tags:
        parts.append(f'Tags: [dim]{_joined_capped(analysis.tags)}[/dim]')
    if parts:
        console.print('   '.join(parts))
    sample = report.sample
    hashes = [
        (name, value)
        for name, value in (('SHA256', sample.sha256), ('MD5', sample.md5), ('SHA1', sample.sha1))
        if value
    ]
    if hashes:
        console.print(
            '  '.join(f'[dim]{n}[/dim] {escape(_elide(v, _HASH_PREVIEW_LEN))}' for n, v in hashes)
        )
    console.print()


def _print_signatures(console: Console, signatures: list) -> None:
    if not signatures:
        return
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Signatures')
    tbl.add_column('Score', justify='right')
    tbl.add_column('ATT&CK', style='dim')
    for sig in ordered[:_DISPLAY_CAP]:
        score = str(sig.score) if sig.score is not None else '—'
        tbl.add_row(escape(sig.name), score, escape(', '.join(sig.ttp)))
    console.print(tbl)
    if len(ordered) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(ordered) - _DISPLAY_CAP))
    console.print()


def _print_extracted(console: Console, extracted: list) -> None:
    configs = [entry.config for entry in extracted if entry.config]
    if not configs:
        return
    console.print('[dim]Extracted configs[/dim]')
    for cfg in configs[:_DISPLAY_CAP]:
        line = f'  [cyan]{escape(cfg.family or "—")}[/cyan]'
        if cfg.botnet:
            line += f'  botnet: {escape(cfg.botnet)}'
        if cfg.c2:
            line += f'  C2: {_joined_capped(cfg.c2)}'
        console.print(line)
    if len(configs) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(configs) - _DISPLAY_CAP))
    console.print()


def _collect_iocs(targets: list) -> dict:
    collected = {'domains': [], 'ips': [], 'urls': []}
    for target in targets:
        if not target.iocs:
            continue
        for kind, values in collected.items():
            for value in getattr(target.iocs, kind):
                if value not in values:
                    values.append(value)
    return {kind: values for kind, values in collected.items() if values}


def _print_iocs(console: Console, targets: list) -> None:
    iocs = _collect_iocs(targets)
    if not iocs:
        return
    console.print('[dim]IOCs (all targets)[/dim]')
    width = max(len(kind) for kind in iocs)
    for kind, values in iocs.items():
        shown = [_elide(v, _IOC_PREVIEW_LEN) for v in values]
        console.print(f'  {kind.ljust(width)}  {_joined_capped(shown)}')
    console.print()


def _print_tasks(console: Console, tasks: dict) -> None:
    if not tasks:
        return
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Tasks')
    tbl.add_column('Kind')
    tbl.add_column('Status')
    tbl.add_column('Score', justify='right')
    for task_id, task in tasks.items():
        score = str(task.score) if task.score is not None else '—'
        color = 'green' if task.status == 'reported' else 'yellow'
        tbl.add_row(
            escape(task_id), escape(task.kind), f'[{color}]{escape(task.status)}[/{color}]', score
        )
    console.print(tbl)


def _print_pretty(report: OverviewReport) -> None:
    console = Console()
    _print_header(console, report)
    _print_signatures(console, report.signatures)
    _print_extracted(console, report.extracted)
    _print_iocs(console, report.targets)
    _print_tasks(console, report.tasks)


def _print_static_header(console: Console, report: StaticAnalysisReport) -> None:
    analysis = report.analysis
    bucket = _score_bucket(analysis.score)
    color = _SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '—'
    console.print(
        f'[bold]Sample {escape(report.sample.sample)}[/bold] — '
        f'[bold {color}]SCORE {score} {_SCORE_LABELS[bucket]}[/bold {color}]'
    )
    if analysis.tags:
        console.print(f'Tags: [dim]{_joined_capped(analysis.tags)}[/dim]')
    parts = []
    target = report.sample.target or report.task.target
    if target:
        parts.append(f'Target: {escape(_elide(target, _IOC_PREVIEW_LEN))}')
    if report.unpack_count is not None:
        parts.append(f'Unpacked: {report.unpack_count}')
    if report.error_count is not None:
        err_color = 'red' if report.error_count else 'dim'
        parts.append(f'Errors: [{err_color}]{report.error_count}[/{err_color}]')
    if parts:
        console.print('   '.join(parts))
    console.print()


def _print_static_files(console: Console, files: list) -> None:
    if not files:
        return
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Files')
    tbl.add_column('Kind')
    tbl.add_column('Size', justify='right')
    tbl.add_column('SHA256', overflow='fold')
    tbl.add_column('Sel')
    for file in files[:_DISPLAY_CAP]:
        tbl.add_row(
            escape(file.filename),
            escape(file.kind) if file.kind else '—',
            str(file.filesize) if file.filesize is not None else '—',
            escape(file.sha256) if file.sha256 else '—',
            '✓' if file.selected else '',
        )
    console.print(tbl)
    if len(files) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(files) - _DISPLAY_CAP))
    console.print()


def _print_static_signatures(console: Console, signatures: list) -> None:
    if not signatures:
        return
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Signatures')
    tbl.add_column('Score', justify='right')
    for sig in ordered[:_DISPLAY_CAP]:
        score = str(sig.score) if sig.score is not None else '—'
        tbl.add_row(escape(sig.name), score)
    console.print(tbl)
    if len(ordered) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(ordered) - _DISPLAY_CAP))
    console.print()


def _print_static_pretty(report: StaticAnalysisReport) -> None:
    console = Console()
    _print_static_header(console, report)
    _print_static_files(console, report.files)
    _print_static_signatures(console, report.signatures)
    _print_extracted(console, report.extracted)


def _is_not_found(exc: SampleStaticReportError) -> bool:
    """A 404 on the static report endpoint means the sample does not exist.

    Static reports exist from the moment a sample is submitted, so unlike the
    overview endpoint there is no separate not-yet-available 404 to distinguish.
    """
    response = getattr(exc.__cause__, 'response', None)
    return response is not None and response.status_code == 404


def fetch_static_report(sample_id: str, pretty: bool = False) -> None:
    """Fetch the static (pre-detonation) analysis report for a sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner('Fetching static report…'):
            report = mgr.fetch_sample_static_report(sample_id)
    except SampleStaticReportError as exc:
        if _is_not_found(exc):
            _ERR_CONSOLE.print(f'Sample not found: {escape(sample_id)}')
        else:
            _ERR_CONSOLE.print(f'Failed to fetch static report: {escape(str(exc))}')
        sys.exit(1)
    if pretty:
        _print_static_pretty(report)
    else:
        print_json(json.dumps(report.json()))


def fetch_overview_report(sample_id: str, pretty: bool = False) -> None:
    """Fetch the overview report for a completed sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    try:
        with _spinner():
            report = mgr.fetch_sample_overview_report(sample_id)
    except SampleReportNotAvailableError:
        _ERR_CONSOLE.print('Analysis not complete. Retry once the sample status is `reported`.')
        sys.exit(1)
    except SampleReportNotFoundError:
        _ERR_CONSOLE.print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleOverviewError as exc:
        _ERR_CONSOLE.print(f'Failed to fetch overview report: {escape(str(exc))}')
        sys.exit(1)
    if pretty:
        _print_pretty(report)
    else:
        print_json(json.dumps(report.json()))
