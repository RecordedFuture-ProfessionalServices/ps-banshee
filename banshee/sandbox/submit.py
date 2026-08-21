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
import time
from pathlib import Path

from psengine.errors import RecordedFutureError
from psengine.sandbox import SandboxMgr
from psengine.sandbox.errors import SampleProfileError, SampleSubmitError
from psengine.sandbox.sandbox import Sample, SampleTasks, StaticAnalysisReport
from pydantic import ValidationError
from rich import print_json
from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from .helpers import get_sandbox_mgr, spinner
from .reports import fetch_overview_report

_POLL_INTERVAL = 10
_POLL_TIMEOUT = 600
_TERMINAL_STATUSES = frozenset({'reported', 'failed'})


def _status_spinner() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn('{task.description}'),
        transient=True,
        console=Console(stderr=True),
    )


def _fail(message: str) -> None:
    Console(stderr=True).print(f'[red]{message}[/red]')
    sys.exit(1)


def _parse_picks(picks: list[str]) -> list[dict]:
    return [
        {'pick': file_, 'profile': profile}
        for file_, _, profile in (raw.partition(':') for raw in picks)
    ]


def set_sandbox_sample_profile(
    sample_id: str,
    auto: bool,
    picks: list[str] | None,
    pretty: bool = False,
) -> None:
    mgr = get_sandbox_mgr()
    profiles = _parse_picks(picks) if picks else None
    try:
        with spinner('Setting profile…'):
            result = mgr.set_sample_profile(sample_id, auto=auto, profiles=profiles)
    except SampleProfileError as exc:
        Console(stderr=True).print(f'[red]Profile assignment failed:[/red] {exc}')
        sys.exit(1)
    if pretty:
        console = Console()
        msg = 'Profile assigned successfully' if result.success else 'Profile assignment failed'
        console.print(msg)
    else:
        print_json(json.dumps(result.json()))


def _resolve_submission(target: str, fetch: bool, import_: bool) -> dict:
    if import_:
        return {'kind': 'import', 'source_id': target}
    if Path(target).is_file():
        if fetch:
            _fail(f'--fetch requires a URL target, got a local file: {escape(target)}')
        return {'kind': 'file', 'file_path': Path(target)}
    if target.startswith(('http://', 'https://')):
        return {'kind': 'fetch' if fetch else 'url', 'url': target}
    _fail(f'Target is neither an existing file nor a URL: {escape(target)}')
    return {}  # unreachable; _fail exits


def _validation_messages(exc: ValidationError) -> str:
    return '; '.join(err['msg'] for err in exc.errors())


def _print_sample(sample: Sample, pretty: bool) -> None:
    if not pretty:
        print_json(json.dumps(sample.json()))
        return
    console = Console()
    console.print(f'[bold]Sample {escape(sample.id_)}[/bold], status [cyan]{sample.status}[/cyan]')
    target = sample.filename or sample.url
    details = [f'kind: {sample.kind}']
    if target:
        details.append(f'target: {escape(target)}')
    details.append(f'submitted: {sample.submitted.isoformat()}')
    console.print('  '.join(details))


def _poll(mgr: SandboxMgr, sample_id: str, done, label: str) -> SampleTasks | None:
    deadline = time.monotonic() + _POLL_TIMEOUT
    progress = _status_spinner()
    with progress:
        task = progress.add_task(label)
        while True:
            try:
                sample = mgr.fetch_sample(sample_id)
            except RecordedFutureError as exc:
                _fail(f'Failed to fetch sample {escape(sample_id)}: {escape(str(exc))}')
            if done(sample.status):
                return sample
            progress.update(task, description=f'{label} [dim]status: {sample.status}[/dim]')
            if time.monotonic() >= deadline:
                return None
            time.sleep(_POLL_INTERVAL)


def poll_until_terminal(mgr: SandboxMgr, sample_id: str) -> SampleTasks | None:
    return _poll(
        mgr, sample_id, lambda s: s in _TERMINAL_STATUSES, label='Waiting for analysis to complete…'
    )


def _wait_and_report(mgr: SandboxMgr, sample_id: str, pretty: bool) -> None:
    sample = poll_until_terminal(mgr, sample_id)
    if sample is None:
        _fail(
            f'Analysis still running after {_POLL_TIMEOUT}s. Check later with '
            f'`banshee sandbox report overview {escape(sample_id)}`.'
        )
    if sample.status == 'failed':
        _fail(f'Sample {escape(sample_id)} finished with status `failed`.')
    fetch_overview_report(sample_id, pretty=pretty)


def _build_picks(report: StaticAnalysisReport) -> tuple[list[dict], bool]:
    if report.sample.kind == 'url':
        target = report.sample.target or ''
        return [{'name': target, 'path': target}], False
    if len(report.files) == 1:
        file = report.files[0]
        return [{'name': file.filename, 'path': file.relpath or file.filename}], False
    if not report.files:
        return [], True
    return _prompt_file_picks(report.files)


def _prompt_file_picks(files: list) -> tuple[list[dict], bool]:
    Console(stderr=True).print('Files found in the sample:')
    for idx, file in enumerate(files, start=1):
        marker = ' [green](recommended)[/green]' if file.selected else ''
        Console(stderr=True).print(f'  {idx}) {escape(file.filename)}{marker}')
    answer = Prompt.ask(
        'Files to analyse (e.g. 1,3; blank = recommended files + automatic profiles)',
        console=Console(stderr=True),
        default='',
        show_default=False,
    ).strip()
    if not answer:
        picks = [{'name': f.filename, 'path': f.relpath or f.filename} for f in files if f.selected]
        return picks, True
    indexes = _parse_selection(answer, len(files))
    picks = [
        {'name': files[i].filename, 'path': files[i].relpath or files[i].filename} for i in indexes
    ]
    return picks, False


def _parse_selection(answer: str, count: int) -> list[int]:
    try:
        indexes = sorted({int(part) - 1 for part in answer.split(',')})
    except ValueError:
        _fail(f'Invalid selection: {escape(answer)}')
    if any(i < 0 or i >= count for i in indexes):
        _fail(f'Selection out of range 1–{count}: {escape(answer)}')
    return indexes


def _prompt_profiles(picks: list[dict], profiles: list) -> tuple[list[dict], bool]:
    Console(stderr=True).print('Available profiles:')
    for idx, profile in enumerate(profiles, start=1):
        Console(stderr=True).print(f'  {idx}) {escape(profile.name)}')
    selections = []
    for pick in picks:
        answer = Prompt.ask(
            f'Profile for {escape(pick["name"])} (blank = automatic for all)',
            console=Console(stderr=True),
            default='',
            show_default=False,
        ).strip()
        if not answer:
            return [], True
        indexes = _parse_selection(answer, len(profiles))
        selections.extend({'pick': pick['path'], 'profile': profiles[i].id_} for i in indexes)
    return selections, False


def interactive_profile_selection(mgr: SandboxMgr, sample_id: str) -> None:
    """Pause at static analysis, prompt file→profile mappings, and advance the sample."""
    sample = _poll(mgr, sample_id, lambda s: s != 'pending', label='Waiting for static analysis…')
    if sample is None:
        _fail(
            f'Static analysis still running after {_POLL_TIMEOUT}s. Assign profiles later with '
            f'`banshee sandbox set-profile {escape(sample_id)}`.'
        )
    if sample.status == 'failed':
        _fail(f'Sample {escape(sample_id)} failed during static analysis.')
    if sample.status != 'static_analysis':
        Console(stderr=True).print(
            f'Sample does not need profile selection (status: {escape(sample.status)}).'
        )
        return
    try:
        report = mgr.fetch_sample_static_report(sample_id)
        profiles = mgr.fetch_profiles()
    except RecordedFutureError as exc:
        _fail(f'Failed to prepare profile selection: {escape(str(exc))}')
    picks, auto = _build_picks(report)
    selections = []
    if not auto:
        if profiles:
            selections, auto = _prompt_profiles(picks, profiles)
        else:
            auto = True
    if auto:
        Console(stderr=True).print('Using automatic profile selection.')
    try:
        with spinner('Setting profile…'):
            if auto:
                mgr.set_sample_profile(
                    sample_id, auto=True, pick=[p['path'] for p in picks] or None
                )
            else:
                mgr.set_sample_profile(sample_id, auto=False, profiles=selections)
    except SampleProfileError as exc:
        _fail(f'Profile assignment failed: {escape(str(exc))}')


def submit_sandbox_sample(
    target: str,
    *,
    fetch: bool = False,
    import_: bool = False,
    profiles: list[str] | None = None,
    timeout: int | None = None,
    network: str | None = None,
    geolocation: str | None = None,
    tags: list[str] | None = None,
    password: str | None = None,
    wait: bool = False,
    interactive: bool = False,
    pretty: bool = False,
) -> None:
    """Submit a sample for analysis, optionally waiting and/or selecting profiles interactively.

    Default output is the submitted sample as JSON on stdout. With `wait`, polls until the
    analysis finishes and prints the overview report instead. With `interactive`, pauses at
    static analysis for a prompted file→profile selection before continuing.
    """
    kind_kwargs = _resolve_submission(target, fetch, import_)
    mgr = get_sandbox_mgr()
    try:
        with spinner('Submitting sample…'):
            sample = mgr.submit_sample(
                **kind_kwargs,
                interactive=interactive or None,
                password=password,
                profiles=[{'profile': p} for p in profiles] if profiles else None,
                user_tags=tags,
                timeout=timeout,
                network=network,
                geolocation=geolocation,
            )
    except ValidationError as exc:
        _fail(f'Invalid submission: {escape(_validation_messages(exc))}')
    except SampleSubmitError as exc:
        _fail(f'Submission failed: {escape(str(exc))}')
    if interactive:
        interactive_profile_selection(mgr, sample.id_)
    if wait:
        _wait_and_report(mgr, sample.id_, pretty=pretty)
        return
    if interactive:
        try:
            sample = mgr.fetch_sample(sample.id_)
        except RecordedFutureError as exc:
            _fail(f'Failed to fetch sample {escape(sample.id_)}: {escape(str(exc))}')
    _print_sample(sample, pretty)
