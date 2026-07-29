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

from psengine.sandbox import BehavioralReportFailure, BehavioralReportsResult, SandboxMgr
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

from .constants import (
    BEHAVIORAL_MAX_WORKERS,
    BEHAVIORAL_WAIT_TIMEOUT,
    OVERVIEW_WAIT_TIMEOUT,
    STATIC_WAIT_TIMEOUT,
)
from .helpers import get_sandbox_mgr, spinner
from .reports_output import print_behavioral_pretty, print_overview_pretty, print_static_pretty


def fetch_static_report(sample_id: str, pretty: bool = False, wait: bool = False) -> None:
    """Fetch the static (pre-detonation) analysis report for a sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead. With `wait`, a report that is not
    yet available is polled internally for up to STATIC_WAIT_TIMEOUT seconds before
    giving up.
    """
    mgr = get_sandbox_mgr()
    label = 'Waiting for static report' if wait else 'Fetching static report'
    try:
        with spinner(label):
            report = mgr.fetch_sample_static_report(
                sample_id, wait_until_ready=wait, timeout=STATIC_WAIT_TIMEOUT
            )
    except SampleReportNotAvailableError as exc:
        if wait:
            Console(stderr=True).print(escape(str(exc)))
        else:
            Console(stderr=True).print(
                'Static report not available yet. Retry shortly or pass --wait.'
            )
        sys.exit(1)
    except SampleReportNotFoundError:
        Console(stderr=True).print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleStaticReportError as exc:
        Console(stderr=True).print(f'Failed to fetch static report: {escape(str(exc))}')
        sys.exit(1)
    if pretty:
        print_static_pretty(report)
    else:
        print_json(json.dumps(report.json()))


def fetch_overview_report(sample_id: str, pretty: bool = False, wait: bool = False) -> None:
    """Fetch the overview report for a completed sample and print it.

    Default output is the full report as JSON on stdout; `pretty` renders a
    summarised human-readable view instead. With `wait`, a report that is not
    yet available is polled internally for up to OVERVIEW_WAIT_TIMEOUT seconds
    before giving up.
    """
    mgr = get_sandbox_mgr()
    label = 'Waiting for overview report' if wait else 'Fetching overview report'
    try:
        with spinner(label):
            report = mgr.fetch_sample_overview_report(
                sample_id, wait_until_ready=wait, timeout=OVERVIEW_WAIT_TIMEOUT
            )
    except SampleReportNotAvailableError as exc:
        if wait:
            Console(stderr=True).print(escape(str(exc)))
        else:
            Console(stderr=True).print(
                'Analysis not complete. Retry once the sample status is `reported`, or pass --wait.'
            )
        sys.exit(1)
    except SampleReportNotFoundError:
        Console(stderr=True).print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleOverviewError as exc:
        Console(stderr=True).print(f'Failed to fetch overview report: {escape(str(exc))}')
        sys.exit(1)
    if pretty:
        print_overview_pretty(report)
    else:
        print_json(json.dumps(report.json()))


def _fetch_behavioral(mgr: SandboxMgr, sample_id: str, wait: bool) -> BehavioralReportsResult:
    label = (
        'Waiting for all behavioral reports to complete' if wait else 'Fetching behavioral reports'
    )
    try:
        with spinner(label):
            return mgr.fetch_behavioral_reports(
                sample_id,
                max_workers=BEHAVIORAL_MAX_WORKERS,
                wait_until_ready=wait,
                timeout=BEHAVIORAL_WAIT_TIMEOUT,
            )
    except SampleReportNotFoundError:
        Console(stderr=True).print(f'Sample not found: {escape(sample_id)}')
        sys.exit(1)
    except SampleBehavioralReportError as exc:
        Console(stderr=True).print(f'Failed to fetch behavioral reports: {escape(str(exc))}')
        sys.exit(1)


def _print_behavioral_failures(failed: list[BehavioralReportFailure]) -> None:
    for failure in failed:
        parts = []
        if failure.status_code is not None:
            parts.append(f'HTTP {failure.status_code}')
        if failure.error:
            parts.append(escape(failure.error))
        detail = ' '.join(parts) or 'unknown error'
        Console(stderr=True).print(
            f'Report fetch failed for {escape(failure.task_id)} ({detail}).'
        )


def _print_behavioral_not_ready(not_ready: list[str], waited: bool) -> None:
    ids = ', '.join(escape(task_id) for task_id in not_ready)
    hint = '' if waited else ', or pass --wait'
    Console(stderr=True).print(
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
    BEHAVIORAL_WAIT_TIMEOUT seconds before giving up. Task reports that failed
    to fetch for a terminal reason are noted on stderr without failing the
    command, as long as at least one report was fetched. Exits non-zero when
    any report is still pending at print time or when every fetch failed
    terminally; ready reports are always printed, even when others are pending.
    A sample with no behavioral tasks prints an empty array and a note on
    stderr. In `pretty` mode, process commands are truncated to 20 characters
    unless `full_cmd` is set.
    """
    mgr = get_sandbox_mgr()
    result = _fetch_behavioral(mgr, sample_id, wait)
    _print_behavioral_failures(result.failed)
    if result.not_ready:
        _print_behavioral_not_ready(result.not_ready, waited=wait)
    elif not result.reports and not result.failed:
        Console(stderr=True).print('No behavioral tasks for this sample.')
    if result.reports or result.complete:
        if pretty:
            print_behavioral_pretty(result.reports, full_cmd=full_cmd)
        else:
            print_json(json.dumps([report.json() for report in result.reports]))
    all_failed = result.failed and not result.reports
    if not result.complete or all_failed:
        sys.exit(1)
