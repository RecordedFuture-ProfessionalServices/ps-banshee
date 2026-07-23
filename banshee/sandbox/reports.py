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
import re
import sys

from psengine.config import get_config
from psengine.sandbox import (
    BehavioralReport,
    BehavioralReportFailure,
    BehavioralReportsResult,
    OverviewReport,
    SandboxMgr,
    StaticAnalysisReport,
)
from psengine.sandbox.errors import (
    SampleBehavioralReportError,
    SampleOverviewError,
    SampleReportNotAvailableError,
    SampleReportNotFoundError,
    SampleStaticReportError,
)
from rich import print_json
from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table

from .output import _BAR_CHAR, _DISPLAY_CAP, _MORE_MSG, _SCORE_COLORS

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
_BEHAVIORAL_MAX_WORKERS = 10
_WAIT_TIMEOUT = 600
_OVERVIEW_WAIT_TIMEOUT = 1800
_BEHAVIORAL_WAIT_TIMEOUT = 1800
_SCORE_BAR_WIDTH = 16
_ROW_BAR_WIDTH = 6
_EMPTY_BAR_COLOR = 'grey23'
_FAMILY_BADGE_BG = 'magenta'
_TAG_BADGE_BG = 'grey23'
_TARGET_SIG_CAP = 5
_ROW_TAG_CAP = 4
_CMD_TRUNCATE_LEN = 20


def _section(title: str) -> Rule:
    return Rule(f'[bold magenta]{title}[/bold magenta]', style='bold magenta')


def _score_bar(score: int | None, width: int = _SCORE_BAR_WIDTH) -> str:
    bucket = _score_bucket(score)
    color = _SCORE_COLORS[bucket]
    filled = 0 if not score else min(width, max(1, round(score / 10 * width)))
    bar = f'[{color}]{_BAR_CHAR * filled}[/{color}]'
    empty = width - filled
    if empty:
        bar += f'[{_EMPTY_BAR_COLOR}]{_BAR_CHAR * empty}[/{_EMPTY_BAR_COLOR}]'
    return bar


def _badge(text: str, bg: str = _TAG_BADGE_BG) -> str:
    return f'[bold white on {bg}] {escape(text)} [/]'


def _task_sort_key(item: tuple) -> tuple:
    """Sort tasks static-first, then naturally by task id (behavioral2 before behavioral10)."""
    task_id, task = item
    kind_rank = 0 if task.kind == 'static' else 1
    # Zero-pad digit chunks so the key stays all-strings (safe to compare) while still
    # sorting numerically.
    natural = tuple(
        f'{int(chunk):08d}' if chunk.isdigit() else chunk for chunk in re.split(r'(\d+)', task_id)
    )
    return (kind_rank, natural)


def _joined_badges(tags: list[str], cap: int = _ROW_TAG_CAP) -> str:
    if not tags:
        return ''
    text = ' '.join(_badge(tag) for tag in tags[:cap])
    extra = len(tags) - cap
    if extra > 0:
        text += f' [dim]+{extra}[/dim]'
    return text


def _spinner(label: str = 'Fetching overview report') -> Progress:
    progress = Progress(SpinnerColumn(), TextColumn(label), transient=True, console=_ERR_CONSOLE)
    progress.add_task('')  # a Progress with zero tasks renders nothing
    return progress


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


def _print_header(console: Console, report: OverviewReport) -> None:
    console.print(_section('General'))
    sample = report.sample
    analysis = report.analysis
    if sample.target:
        console.print(f'[bold cyan]Target[/bold cyan]  {escape(sample.target)}')
    if sample.size is not None:
        console.print(f'[bold cyan]Size[/bold cyan]    {sample.size:,} bytes')
    bucket = _score_bucket(analysis.score)
    color = _SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '—'
    console.print(
        f'[bold]Sample {escape(sample.id_)}[/bold] — '
        f'[bold {color}]SCORE {score} {_SCORE_LABELS[bucket]}[/bold {color}]  '
        f'{_score_bar(analysis.score)}'
    )
    badges = [_badge(fam, bg=_FAMILY_BADGE_BG) for fam in analysis.family]
    badges += [_badge(tag) for tag in analysis.tags[:_DISPLAY_CAP]]
    extra = len(analysis.tags) - _DISPLAY_CAP
    if badges:
        line = '  '.join(badges)
        if extra > 0:
            line += f' [dim]+{extra} more[/dim]'
        console.print(line)
    hashes = [
        (name, value)
        for name, value in (('SHA256', sample.sha256), ('MD5', sample.md5), ('SHA1', sample.sha1))
        if value
    ]
    for name, value in hashes:
        console.print(f'[dim]{name}[/dim] {escape(value)}')
    console.print()


def _print_signatures(console: Console, signatures: list) -> None:
    if not signatures:
        return
    console.print(_section('Signatures'))
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Signatures', style='bold cyan')
    tbl.add_column('Score', justify='right')
    tbl.add_column('ATT&CK', style='dim')
    for sig in ordered[:_DISPLAY_CAP]:
        bucket = _score_bucket(sig.score)
        color = _SCORE_COLORS[bucket]
        score = f'[{color}]{sig.score}[/{color}]' if sig.score is not None else '—'
        tbl.add_row(escape(sig.name), score, escape(', '.join(sig.ttp)))
    console.print(tbl)
    if len(ordered) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(ordered) - _DISPLAY_CAP))
    console.print()


def _print_extracted(console: Console, extracted: list) -> None:
    configs = [entry.config for entry in extracted if entry.config]
    if not configs:
        return
    console.print(_section('Malware Config'))
    for cfg in configs[:_DISPLAY_CAP]:
        line = f'  {_badge(cfg.family, bg=_FAMILY_BADGE_BG)}' if cfg.family else '  —'
        if cfg.botnet:
            line += f'  botnet: {escape(cfg.botnet)}'
        if cfg.c2:
            line += f'  C2: {_joined_capped(cfg.c2)}'
        console.print(line)
    if len(configs) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(configs) - _DISPLAY_CAP))
    console.print()


def _print_target_signatures(console: Console, signatures: list) -> None:
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    for sig in ordered[:_TARGET_SIG_CAP]:
        bucket = _score_bucket(sig.score)
        color = _SCORE_COLORS[bucket]
        console.print(f'  [{color}]▎[/{color}] [bold]{escape(sig.name)}[/bold]')
        if sig.desc:
            console.print(f'    [dim]{escape(sig.desc)}[/dim]')
    if len(ordered) > _TARGET_SIG_CAP:
        console.print(f'  {_MORE_MSG.format(len(ordered) - _TARGET_SIG_CAP)}')


def _print_targets(console: Console, targets: list, sample_target: str | None) -> None:
    if not targets:
        return
    # A lone target that IS the submitted sample (same identity) duplicates the General
    # and Signatures sections entirely -- nothing new to show, so skip it.
    if len(targets) == 1 and targets[0].target and targets[0].target == sample_target:
        return
    console.print(_section('Targets'))
    for index, target in enumerate(targets):
        if index:
            console.print()
        label = target.target or target.pick or f'target-{index + 1}'
        console.print(f'[bold cyan]Target[/bold cyan]  {escape(label)}')
        if target.size is not None:
            console.print(f'[bold cyan]Size[/bold cyan]    {target.size:,} bytes')
        bucket = _score_bucket(target.score)
        color = _SCORE_COLORS[bucket]
        score = target.score if target.score is not None else '—'
        console.print(
            f'[bold cyan]Score[/bold cyan]   [bold {color}]{score}/10[/bold {color}]  '
            f'{_score_bar(target.score, width=_ROW_BAR_WIDTH)}'
        )
        badges = [_badge(fam, bg=_FAMILY_BADGE_BG) for fam in target.family]
        badges += [_badge(tag) for tag in target.tags]
        if badges:
            console.print('  '.join(badges))
        if target.signatures:
            _print_target_signatures(console, target.signatures)
    console.print()


def _print_tasks(console: Console, tasks: dict, sample_id: str) -> None:
    if not tasks:
        return
    console.print(_section('Tasks'))
    prefix = f'{sample_id}-'
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Tasks', style='bold cyan')
    tbl.add_column('Kind', style='dim')
    tbl.add_column('Status')
    tbl.add_column('Score', justify='right')
    tbl.add_column('Tags')
    for task_id, task in sorted(tasks.items(), key=_task_sort_key):
        bucket = _score_bucket(task.score)
        color = _SCORE_COLORS[bucket]
        score = f'[{color}]{task.score}[/{color}]' if task.score is not None else '—'
        status_color = 'green' if task.status == 'reported' else 'yellow'
        display_id = task_id.removeprefix(prefix)
        tbl.add_row(
            escape(display_id),
            escape(task.kind),
            f'[{status_color}]{escape(task.status)}[/{status_color}]',
            score,
            _joined_badges(task.tags),
        )
    console.print(tbl)
    console.print()


def _print_pretty(report: OverviewReport) -> None:
    console = Console(highlight=False)
    _print_header(console, report)
    _print_signatures(console, report.signatures)
    _print_extracted(console, report.extracted)
    _print_targets(console, report.targets, report.sample.target)
    _print_tasks(console, report.tasks, report.sample.id_)


def _print_static_header(console: Console, report: StaticAnalysisReport) -> None:
    console.print(_section('General'))
    sample = report.sample
    analysis = report.analysis
    target = sample.target or report.task.target
    if target:
        console.print(f'[bold cyan]Target[/bold cyan]  {escape(target)}')
    if sample.size is not None:
        console.print(f'[bold cyan]Size[/bold cyan]    {sample.size:,} bytes')
    bucket = _score_bucket(analysis.score)
    color = _SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '—'
    console.print(
        f'[bold]Sample {escape(sample.sample)}[/bold] — '
        f'[bold {color}]SCORE {score} {_SCORE_LABELS[bucket]}[/bold {color}]  '
        f'{_score_bar(analysis.score)}'
    )
    if analysis.tags:
        badges = [
            _badge(tag.removeprefix('family:'), bg=_FAMILY_BADGE_BG)
            if tag.startswith('family:')
            else _badge(tag)
            for tag in analysis.tags[:_DISPLAY_CAP]
        ]
        extra = len(analysis.tags) - _DISPLAY_CAP
        line = '  '.join(badges)
        if extra > 0:
            line += f' [dim]+{extra} more[/dim]'
        console.print(line)
    submitted = next((f for f in report.files if f.depth == 0), None)
    if submitted:
        hashes = [
            (name, value)
            for name, value in (
                ('SHA256', submitted.sha256),
                ('MD5', submitted.md5),
                ('SHA1', submitted.sha1),
            )
            if value
        ]
        for name, value in hashes:
            console.print(f'[dim]{name}[/dim] {escape(value)}')
    if report.unpack_count is not None:
        console.print(f'[dim]Unpacked[/dim] {report.unpack_count}')
    if report.error_count is not None:
        err_color = 'red' if report.error_count else 'dim'
        console.print(f'[dim]Errors[/dim] [{err_color}]{report.error_count}[/{err_color}]')
    console.print()


def _print_static_files(console: Console, files: list) -> None:
    if not files:
        return
    console.print(_section('Files'))
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Files', style='bold cyan')
    tbl.add_column('Kind', style='dim')
    tbl.add_column('Size', justify='right', style='bold')
    tbl.add_column('SHA256', style='dim', overflow='fold')
    tbl.add_column('Selected', justify='center')
    for file in files[:_DISPLAY_CAP]:
        tbl.add_row(
            escape(file.filename),
            escape(file.kind) if file.kind else '—',
            str(file.filesize) if file.filesize is not None else '—',
            escape(file.sha256) if file.sha256 else '—',
            '[green]✓[/green]' if file.selected else '',
        )
    console.print(tbl)
    if len(files) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(files) - _DISPLAY_CAP))
    console.print()


def _print_static_signatures(console: Console, signatures: list) -> None:
    if not signatures:
        return
    console.print(_section('Signatures'))
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Signatures', style='bold cyan')
    tbl.add_column('Score', justify='right')
    for sig in ordered[:_DISPLAY_CAP]:
        bucket = _score_bucket(sig.score)
        color = _SCORE_COLORS[bucket]
        score = f'[{color}]{sig.score}[/{color}]' if sig.score is not None else '—'
        tbl.add_row(escape(sig.name), score)
    console.print(tbl)
    if len(ordered) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(ordered) - _DISPLAY_CAP))
    console.print()


def _print_static_pretty(report: StaticAnalysisReport) -> None:
    console = Console(highlight=False)
    _print_static_header(console, report)
    _print_extracted(console, report.extracted)
    _print_static_signatures(console, report.signatures)
    _print_static_files(console, report.files)


def _print_behavioral_header(console: Console, report: BehavioralReport) -> None:
    analysis = report.analysis
    bucket = _score_bucket(analysis.score)
    color = _SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '—'
    line = (
        f'[bold]{escape(report.task_id or "behavioral")}[/bold] — '
        f'[bold {color}]SCORE {score} {_SCORE_LABELS[bucket]}[/bold {color}]'
    )
    if analysis.platform:
        line += f'   platform: {escape(analysis.platform)}'
    console.print(line)
    parts = []
    if analysis.tags:
        parts.append(f'Tags: [dim]{_joined_capped(analysis.tags)}[/dim]')
    counts = [
        (label, count)
        for label, count in (
            ('Requests', len(report.network.requests)),
            ('IPs', len(report.network.ips)),
            ('Dumped', len(report.dumped)),
        )
        if count
    ]
    if counts:
        parts.append('  '.join(f'[dim]{label}:[/dim] {count}' for label, count in counts))
    if parts:
        console.print('   '.join(parts))
    for error in report.errors:
        console.print(f'[red]Error: {escape(error.reason or error.task or "unknown")}[/red]')
    console.print()


def _proc_cmd(proc, full_cmd: bool = False) -> str:
    cmd = ' '.join(proc.cmd) if isinstance(proc.cmd, list) else proc.cmd
    cmd = cmd or proc.image or '—'
    if not full_cmd and len(cmd) > _CMD_TRUNCATE_LEN:
        cmd = f'{cmd[:_CMD_TRUNCATE_LEN]}...'
    return cmd


def _print_behavioral_processes(console: Console, processes: list, full_cmd: bool = False) -> None:
    if not processes:
        return
    console.print('[dim]Processes[/dim]')
    for proc in processes[:_DISPLAY_CAP]:
        pid = proc.pid if proc.pid is not None else '—'
        console.print(f'  [dim]{pid}[/dim]  {escape(_proc_cmd(proc, full_cmd=full_cmd))}')
    if len(processes) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(processes) - _DISPLAY_CAP))
    console.print()


def _print_behavioral_flows(console: Console, flows: list) -> None:
    if not flows:
        return
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Network flows')
    tbl.add_column('Domain')
    tbl.add_column('Proto')
    tbl.add_column('TLS SNI')
    for flow in flows[:_DISPLAY_CAP]:
        tbl.add_row(
            escape(flow.dst) if flow.dst else '—',
            escape(flow.domain) if flow.domain else '—',
            escape(flow.proto) if flow.proto else '—',
            escape(flow.tls_sni) if flow.tls_sni else '—',
        )
    console.print(tbl)
    if len(flows) > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(len(flows) - _DISPLAY_CAP))
    console.print()


def _print_behavioral_pretty(reports: list[BehavioralReport], full_cmd: bool = False) -> None:
    console = Console()
    for index, report in enumerate(reports):
        if index:
            console.print()
        _print_behavioral_header(console, report)
        _print_signatures(console, report.signatures)
        _print_behavioral_processes(console, report.processes, full_cmd=full_cmd)
        _print_behavioral_flows(console, report.network.flows)
        _print_extracted(console, report.extracted)


def fetch_static_report(sample_id: str, pretty: bool = False, wait: bool = False) -> None:
    """Fetch the static (pre-detonation) analysis report for a sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead. With `wait`, a report that is not
    yet available is polled internally for up to _WAIT_TIMEOUT seconds before
    giving up.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    label = 'Waiting for static report' if wait else 'Fetching static report'
    try:
        with _spinner(label):
            report = mgr.fetch_sample_static_report(
                sample_id, wait_until_ready=wait, timeout=_WAIT_TIMEOUT
            )
    except SampleReportNotAvailableError as exc:
        if wait:
            _ERR_CONSOLE.print(escape(str(exc)))
        else:
            _ERR_CONSOLE.print('Static report not available yet. Retry shortly or pass --wait.')
        sys.exit(1)
    except SampleReportNotFoundError:
        _ERR_CONSOLE.print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleStaticReportError as exc:
        _ERR_CONSOLE.print(f'Failed to fetch static report: {escape(str(exc))}')
        sys.exit(1)
    if pretty:
        _print_static_pretty(report)
    else:
        print_json(json.dumps(report.json()))


def fetch_overview_report(sample_id: str, pretty: bool = False, wait: bool = False) -> None:
    """Fetch the overview report for a completed sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead. With `wait`, a report that is not
    yet available is polled internally for up to _OVERVIEW_WAIT_TIMEOUT seconds
    before giving up.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    label = 'Waiting for overview report' if wait else 'Fetching overview report'
    try:
        with _spinner(label):
            report = mgr.fetch_sample_overview_report(
                sample_id, wait_until_ready=wait, timeout=_OVERVIEW_WAIT_TIMEOUT
            )
    except SampleReportNotAvailableError as exc:
        if wait:
            _ERR_CONSOLE.print(escape(str(exc)))
        else:
            _ERR_CONSOLE.print(
                'Analysis not complete. Retry once the sample status is `reported`, or pass --wait.'
            )
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


def _fetch_behavioral(mgr: SandboxMgr, sample_id: str, wait: bool) -> BehavioralReportsResult:
    label = (
        'Waiting for all behavioral reports to complete' if wait else 'Fetching behavioral reports'
    )
    try:
        with _spinner(label):
            return mgr.fetch_behavioral_reports(
                sample_id,
                max_workers=_BEHAVIORAL_MAX_WORKERS,
                wait_until_ready=wait,
                timeout=_BEHAVIORAL_WAIT_TIMEOUT,
            )
    except SampleReportNotFoundError:
        _ERR_CONSOLE.print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleBehavioralReportError as exc:
        _ERR_CONSOLE.print(f'Failed to fetch behavioral reports: {escape(str(exc))}')
        sys.exit(1)


def _print_behavioral_failures(failed: list[BehavioralReportFailure]) -> None:
    for failure in failed:
        parts = []
        if failure.status_code is not None:
            parts.append(f'HTTP {failure.status_code}')
        if failure.error:
            parts.append(escape(failure.error))
        detail = ' '.join(parts) or 'unknown error'
        _ERR_CONSOLE.print(f'Report fetch failed for {escape(failure.task_id)} ({detail}).')


def _print_behavioral_not_ready(not_ready: list[str], waited: bool) -> None:
    ids = ', '.join(escape(task_id) for task_id in not_ready)
    hint = '' if waited else ', or pass --wait'
    _ERR_CONSOLE.print(
        f'{len(not_ready)} behavioral report(s) not available yet ({ids}). '
        f'Retry once the sample status is `reported`{hint}.'
    )


def fetch_behavioral_reports(
    sample_id: str, pretty: bool = False, wait: bool = False, full_cmd: bool = False
) -> None:
    """Fetch the behavioral (post-detonation) reports for a sample and print them.

    Default output is a JSON array on stdout with one full report per finished
    behavioral task; `pretty` renders a summarised human-readable view per task
    instead. Tasks still being analysed are omitted from the output and noted on
    stderr; with `wait`, they are polled internally for up to
    _BEHAVIORAL_WAIT_TIMEOUT seconds before giving up. Task reports that failed
    to fetch for a terminal reason are noted on stderr without failing the
    command, as long as at least one report was fetched. Exits non-zero when
    any report is still pending at print time or when every fetch failed
    terminally; ready reports are always printed, even when others are pending.
    A sample with no behavioral tasks prints an empty array and a note on
    stderr. In `pretty` mode, process commands are truncated to 20 characters
    unless `full_cmd` is set.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)
    result = _fetch_behavioral(mgr, sample_id, wait)
    _print_behavioral_failures(result.failed)
    if result.not_ready:
        _print_behavioral_not_ready(result.not_ready, waited=wait)
    elif not result.reports and not result.failed:
        _ERR_CONSOLE.print('No behavioral tasks for this sample.')
    if result.reports or result.complete:
        if pretty:
            _print_behavioral_pretty(result.reports, full_cmd=full_cmd)
        else:
            print_json(json.dumps([report.json() for report in result.reports]))
    all_failed = result.failed and not result.reports
    if not result.complete or all_failed:
        sys.exit(1)
