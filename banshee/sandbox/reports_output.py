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

import re

from psengine.sandbox import BehavioralReport, OverviewReport, StaticAnalysisReport
from rich.console import Console
from rich.markup import escape
from rich.rule import Rule
from rich.table import Table

from .constants import (
    BAR_CHAR,
    DISPLAY_CAP,
    EMPTY_BAR_COLOR,
    FAMILY_BADGE_BG,
    MORE_MSG,
    SCORE_COLORS,
    SCORE_LABELS,
    TAG_BADGE_BG,
)
from .helpers import score_bucket

_SCORE_BAR_WIDTH = 16
_ROW_BAR_WIDTH = 6
_TARGET_SIG_CAP = 5
_ROW_TAG_CAP = 4
_CMD_TRUNCATE_LEN = 20


def _section(title: str) -> Rule:
    return Rule(f'[bold magenta]{title}[/bold magenta]', style='bold magenta')


def _score_bar(score: int | None, width: int = _SCORE_BAR_WIDTH) -> str:
    bucket = score_bucket(score)
    color = SCORE_COLORS[bucket]
    filled = 0 if not score else min(width, max(1, round(score / 10 * width)))
    bar = f'[{color}]{BAR_CHAR * filled}[/{color}]'
    empty = width - filled
    if empty:
        bar += f'[{EMPTY_BAR_COLOR}]{BAR_CHAR * empty}[/{EMPTY_BAR_COLOR}]'
    return bar


def _colored_score(score: int | None) -> str:
    if score is None:
        return '-'
    color = SCORE_COLORS[score_bucket(score)]
    return f'[{color}]{score}[/{color}]'


def _badge(text: str, bg: str = TAG_BADGE_BG) -> str:
    return f'[bold white on {bg}] {escape(text)} [/]'


def _task_sort_key(item: tuple) -> tuple:
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


def _joined_capped(items: list[str], sep: str = ', ') -> str:
    text = sep.join(escape(item) for item in items[:DISPLAY_CAP])
    extra = len(items) - DISPLAY_CAP
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
    bucket = score_bucket(analysis.score)
    color = SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '-'
    console.print(
        f'[bold]Sample {escape(sample.id_)}[/bold], '
        f'[bold {color}]SCORE {score} {SCORE_LABELS[bucket]}[/bold {color}]  '
        f'{_score_bar(analysis.score)}'
    )
    badges = [_badge(fam, bg=FAMILY_BADGE_BG) for fam in analysis.family]
    badges += [_badge(tag) for tag in analysis.tags[:DISPLAY_CAP]]
    extra = len(analysis.tags) - DISPLAY_CAP
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


def _print_signatures(console: Console, signatures: list, *, include_ttp: bool = True) -> None:
    if not signatures:
        return
    console.print(_section('Signatures'))
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('Signatures', style='bold cyan')
    tbl.add_column('Score', justify='right')
    if include_ttp:
        tbl.add_column('ATT&CK', style='dim')
    for sig in ordered[:DISPLAY_CAP]:
        row = [escape(sig.name), _colored_score(sig.score)]
        if include_ttp:
            row.append(escape(', '.join(sig.ttp)))
        tbl.add_row(*row)
    console.print(tbl)
    if len(ordered) > DISPLAY_CAP:
        console.print(MORE_MSG.format(len(ordered) - DISPLAY_CAP))
    console.print()


def _print_extracted(console: Console, extracted: list) -> None:
    configs = [entry.config for entry in extracted if entry.config]
    if not configs:
        return
    console.print(_section('Malware Config'))
    for cfg in configs[:DISPLAY_CAP]:
        line = f'  {_badge(cfg.family, bg=FAMILY_BADGE_BG)}' if cfg.family else '  -'
        if cfg.botnet:
            line += f'  botnet: {escape(cfg.botnet)}'
        if cfg.c2:
            line += f'  C2: {_joined_capped(cfg.c2)}'
        console.print(line)
    if len(configs) > DISPLAY_CAP:
        console.print(MORE_MSG.format(len(configs) - DISPLAY_CAP))
    console.print()


def _print_target_signatures(console: Console, signatures: list) -> None:
    ordered = sorted(signatures, key=lambda s: s.score if s.score is not None else -1, reverse=True)
    for sig in ordered[:_TARGET_SIG_CAP]:
        bucket = score_bucket(sig.score)
        color = SCORE_COLORS[bucket]
        console.print(f'  [{color}]▎[/{color}] [bold]{escape(sig.name)}[/bold]')
        if sig.desc:
            console.print(f'    [dim]{escape(sig.desc)}[/dim]')
    if len(ordered) > _TARGET_SIG_CAP:
        console.print(f'  {MORE_MSG.format(len(ordered) - _TARGET_SIG_CAP)}')


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
        bucket = score_bucket(target.score)
        color = SCORE_COLORS[bucket]
        score = target.score if target.score is not None else '-'
        console.print(
            f'[bold cyan]Score[/bold cyan]   [bold {color}]{score}/10[/bold {color}]  '
            f'{_score_bar(target.score, width=_ROW_BAR_WIDTH)}'
        )
        badges = [_badge(fam, bg=FAMILY_BADGE_BG) for fam in target.family]
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
        status_color = 'green' if task.status == 'reported' else 'yellow'
        display_id = task_id.removeprefix(prefix)
        tbl.add_row(
            escape(display_id),
            escape(task.kind),
            f'[{status_color}]{escape(task.status)}[/{status_color}]',
            _colored_score(task.score),
            _joined_badges(task.tags),
        )
    console.print(tbl)
    console.print()


def print_overview_pretty(report: OverviewReport) -> None:
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
    bucket = score_bucket(analysis.score)
    color = SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '-'
    console.print(
        f'[bold]Sample {escape(sample.sample)}[/bold], '
        f'[bold {color}]SCORE {score} {SCORE_LABELS[bucket]}[/bold {color}]  '
        f'{_score_bar(analysis.score)}'
    )
    if analysis.tags:
        badges = [
            _badge(tag.removeprefix('family:'), bg=FAMILY_BADGE_BG)
            if tag.startswith('family:')
            else _badge(tag)
            for tag in analysis.tags[:DISPLAY_CAP]
        ]
        extra = len(analysis.tags) - DISPLAY_CAP
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
    for file in files[:DISPLAY_CAP]:
        tbl.add_row(
            escape(file.filename),
            escape(file.kind) if file.kind else '-',
            str(file.filesize) if file.filesize is not None else '-',
            escape(file.sha256) if file.sha256 else '-',
            '[green]✓[/green]' if file.selected else '',
        )
    console.print(tbl)
    if len(files) > DISPLAY_CAP:
        console.print(MORE_MSG.format(len(files) - DISPLAY_CAP))
    console.print()


def print_static_pretty(report: StaticAnalysisReport) -> None:
    console = Console(highlight=False)
    _print_static_header(console, report)
    _print_extracted(console, report.extracted)
    _print_signatures(console, report.signatures, include_ttp=False)
    _print_static_files(console, report.files)


def _print_behavioral_header(console: Console, report: BehavioralReport) -> None:
    analysis = report.analysis
    bucket = score_bucket(analysis.score)
    color = SCORE_COLORS[bucket]
    score = analysis.score if analysis.score is not None else '-'
    line = (
        f'[bold]{escape(report.task_id or "behavioral")}[/bold], '
        f'[bold {color}]SCORE {score} {SCORE_LABELS[bucket]}[/bold {color}]'
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
    cmd = cmd or proc.image or '-'
    if not full_cmd and len(cmd) > _CMD_TRUNCATE_LEN:
        cmd = f'{cmd[:_CMD_TRUNCATE_LEN]}...'
    return cmd


def _print_behavioral_processes(console: Console, processes: list, full_cmd: bool = False) -> None:
    if not processes:
        return
    console.print('[dim]Processes[/dim]')
    for proc in processes[:DISPLAY_CAP]:
        pid = proc.pid if proc.pid is not None else '-'
        console.print(f'  [dim]{pid}[/dim]  {escape(_proc_cmd(proc, full_cmd=full_cmd))}')
    if len(processes) > DISPLAY_CAP:
        console.print(MORE_MSG.format(len(processes) - DISPLAY_CAP))
    console.print()


def _print_behavioral_flows(console: Console, flows: list) -> None:
    if not flows:
        return
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='dim')
    tbl.add_column('Network flows')
    tbl.add_column('Domain')
    tbl.add_column('Proto')
    tbl.add_column('TLS SNI')
    for flow in flows[:DISPLAY_CAP]:
        tbl.add_row(
            escape(flow.dst) if flow.dst else '-',
            escape(flow.domain) if flow.domain else '-',
            escape(flow.proto) if flow.proto else '-',
            escape(flow.tls_sni) if flow.tls_sni else '-',
        )
    console.print(tbl)
    if len(flows) > DISPLAY_CAP:
        console.print(MORE_MSG.format(len(flows) - DISPLAY_CAP))
    console.print()


def print_behavioral_pretty(reports: list[BehavioralReport], full_cmd: bool = False) -> None:
    console = Console()
    for index, report in enumerate(reports):
        if index:
            console.print()
        _print_behavioral_header(console, report)
        _print_signatures(console, report.signatures)
        _print_behavioral_processes(console, report.processes, full_cmd=full_cmd)
        _print_behavioral_flows(console, report.network.flows)
        _print_extracted(console, report.extracted)
