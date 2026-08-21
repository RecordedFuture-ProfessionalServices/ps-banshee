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
from urllib.parse import quote

from psengine.config import get_config
from psengine.sandbox.sandbox import Sample
from rich import print_json
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from .constants import INTEL_CARD_BASE, SANDBOX_FRONTEND_URLS
from .helpers import get_sandbox_mgr, spinner

_DATETIME_FMT = '%Y-%m-%d %H:%M'


def _status_color(status: str) -> str:
    if status == 'reported':
        return 'green'
    if status == 'failed':
        return 'red'
    return 'yellow'


def _samples_table(samples: list[Sample]) -> Table:
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 0), header_style='bold magenta')
    tbl.add_column('ID', style='dim')
    tbl.add_column('Target', style='bold cyan')
    tbl.add_column('Status')
    tbl.add_column('Kind', style='dim')
    tbl.add_column('Submitted')
    tbl.add_column('Completed')
    tbl.add_column('SHA256', style='dim')
    for s in samples:
        target = s.filename or s.url or '-'
        completed = s.completed.strftime(_DATETIME_FMT) if s.completed else '-'
        color = _status_color(s.status)
        tbl.add_row(
            s.id_,
            target,
            f'[{color}]{s.status}[/{color}]',
            s.kind,
            s.submitted.strftime(_DATETIME_FMT),
            completed,
            s.sha256 or '-',
        )
    return tbl


def list_sandbox_samples(subset: str = 'org', limit: int = 20, pretty: bool = False) -> None:
    mgr = get_sandbox_mgr()
    with spinner('Fetching samples'):
        samples = mgr.fetch_samples(subset=subset, max_results=limit)
    if pretty:
        Console().print(_samples_table(samples))
    else:
        print_json(json.dumps([s.json() for s in samples]))


def _filter_summary(filters: dict) -> str:
    parts = []
    for name, value in filters.items():
        if not value:
            continue
        if isinstance(value, list):
            parts.extend(f'{name}:{v}' for v in value)
        else:
            parts.append(f'{name}:{value}')
    return ' · '.join(parts) if parts else '(no filters)'


def _search_results_table(samples: list[Sample], frontend_base: str) -> Table:
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
    tbl.add_column('ID', style='cyan', no_wrap=True)
    tbl.add_column('Target', style='bold cyan')
    tbl.add_column('Status', width=8)
    tbl.add_column('Kind', style='dim', width=6)
    tbl.add_column('Submitted', style='dim')
    tbl.add_column('SHA256', style='dim', no_wrap=True)
    for s in samples:
        target = s.filename or s.url or '-'
        color = _status_color(s.status)
        id_cell = f'[link={frontend_base}/{quote(s.id_, safe="")}]{s.id_}[/link]'
        if s.sha256:
            hash_url = f'{INTEL_CARD_BASE}/{quote(f"hash:{s.sha256}", safe="")}'
            sha_cell = f'[link={hash_url}]{s.sha256}[/link]'
        else:
            sha_cell = '-'
        tbl.add_row(
            id_cell,
            target,
            f'[{color}]{s.status}[/{color}]',
            s.kind,
            s.submitted.strftime(_DATETIME_FMT),
            sha_cell,
        )
    return tbl


def _print_search_pretty(
    samples: list[Sample], filters: dict, limit: int, frontend_base: str
) -> None:
    console = Console()
    summary = _filter_summary(filters)
    count_label = f'{len(samples)} result{"" if len(samples) == 1 else "s"}'
    truncated = ' (truncated)' if len(samples) >= limit else ''
    console.print()
    console.print(
        Rule(
            f'[bold]Sandbox search · {count_label}{truncated} · {summary}[/bold]',
            style='bold magenta',
        )
    )
    console.print()
    if not samples:
        console.print('  [dim]No matching samples.[/dim]')
        console.print()
        return
    console.print(_search_results_table(samples, frontend_base))
    console.print()


def search_sandbox_samples(
    file_hash: str | None = None,
    family: str | None = None,
    tag: list[str] | None = None,
    botnet: str | None = None,
    wallet: str | None = None,
    ip: str | None = None,
    domain: str | None = None,
    url: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    query: str | None = None,
    limit: int = 50,
    pretty: bool = False,
) -> None:
    mgr = get_sandbox_mgr()
    with spinner('Searching samples'):
        samples = mgr.search_samples(
            file_hash=file_hash,
            family=family,
            tag=tag,
            botnet=botnet,
            wallet=wallet,
            ip=ip,
            domain=domain,
            url=url,
            from_date=from_date,
            to_date=to_date,
            query=query,
            results_per_page=min(limit, 200),
            max_results=limit,
        )
    if pretty:
        sandbox_choice = get_config().sandbox_choice
        frontend_base = SANDBOX_FRONTEND_URLS.get(sandbox_choice, SANDBOX_FRONTEND_URLS['eu'])
        filters = {
            'hash': file_hash,
            'family': family,
            'tag': tag,
            'botnet': botnet,
            'wallet': wallet,
            'ip': ip,
            'domain': domain,
            'url': url,
            'from': from_date,
            'to': to_date,
            'q': query,
        }
        _print_search_pretty(samples, filters, limit, frontend_base)
    else:
        print_json(json.dumps([s.json() for s in samples]))
