##################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly "as-is" and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

import json
from urllib.parse import quote_plus

from rich import print_json
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from .stats import SandboxStats, VerifiedIoc

_SCORE_COLORS = {
    'malicious': 'red',
    'suspicious': 'yellow',
    'potentially_suspicious': 'dark_orange',
    'clean': 'green',
    'unknown': 'grey50',
}

_SCORE_LABELS = {
    'malicious': 'malicious (8–10)',
    'suspicious': 'suspicious (5–7)',
    'potentially_suspicious': 'potentially suspicious (3–4)',
    'clean': 'clean (1–2)',
    'unknown': 'unknown',
}

_SANDBOX_FRONTEND_URLS = {
    'eu': 'https://sandbox.recordedfuture.com',
    'usa': 'https://us-sandbox.recordedfuture.com',
    'apj': 'https://apj-sandbox.recordedfuture.com',
    'public': 'https://tria.ge',
    'private': 'https://private.tria.ge',
}


def _search_url(frontend_base: str, query: str) -> str:
    return f'{frontend_base}/s?q={quote_plus(query)}'


def _trend_str(curr: int, prev: int) -> str:
    if prev == 0:
        return f'{curr:,}  (no prior data)'
    delta = curr - prev
    pct = (delta / prev) * 100
    sign = '+' if delta >= 0 else ''
    arrow = '▲' if delta >= 0 else '▼'
    color = 'green' if delta >= 0 else 'red'
    return f'{curr:,}  vs {prev:,} prev  [{color}]{arrow} {sign}{pct:.0f}%[/{color}]'


def _fmt_tags(
    tag_dict: dict,
    strip_prefix: str = '',
    query_prefix: str = '',
    frontend_base: str = '',
    top_n: int = 8,
) -> str:
    items = list(tag_dict.items())[:top_n]
    if not items:
        return '[grey50]—[/grey50]'
    parts = []
    for tag, count in items:
        label = tag[len(strip_prefix) :] if strip_prefix else tag
        if frontend_base:
            query = f'{query_prefix}{tag}' if query_prefix else tag
            url = _search_url(frontend_base, query)
            parts.append(f'[link={url}]{label}[/link] ({count})')
        else:
            parts.append(f'{label} ({count})')
    return '  '.join(parts)


def _ioc_rf_score(ioc) -> int:
    return ioc.rf_score if isinstance(ioc, VerifiedIoc) else ioc['rf_score']


def _ioc_field(ioc, attr: str) -> str:
    return getattr(ioc, attr) if isinstance(ioc, VerifiedIoc) else ioc[attr]


def _print_summary(console: Console, stats: SandboxStats) -> None:
    trend = stats.trend_vs_prior_period
    console.print(
        f'  [bold]Submissions[/bold]'
        f'  {_trend_str(trend["total"]["current"], trend["total"]["prev"])}'
    )
    console.print(
        f'  [bold]Reported   [/bold]'
        f'  {_trend_str(trend["reported"]["current"], trend["reported"]["prev"])}'
    )
    console.print()

    status_str = '  '.join(f'{k}: {v}' for k, v in stats.by_status.items())
    kind_str = '  '.join(f'{k}: {v}' for k, v in stats.by_kind.items())
    console.print(f'  [dim]by status[/dim]  {status_str}')
    console.print(f'  [dim]by kind  [/dim]  {kind_str}')
    console.print()

    if stats.by_score:
        parts = []
        for bucket in ('malicious', 'suspicious', 'potentially_suspicious', 'clean', 'unknown'):
            count = stats.by_score.get(bucket, 0)
            if count:
                color = _SCORE_COLORS[bucket]
                label = _SCORE_LABELS[bucket]
                parts.append(f'[{color}]{label}: {count}[/{color}]')
        console.print('  [dim]by score  [/dim]  ' + '   '.join(parts))
        console.print()


def _print_platform(console: Console, by_platform: dict) -> None:
    if not by_platform:
        return
    console.print(Rule('[bold]Platform[/bold]  (behavioral tasks)', style='dim'))
    tbl = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
    tbl.add_column('OS', style='cyan', no_wrap=True)
    tbl.add_column('Count', style='bold')
    for os_name, count in by_platform.items():
        tbl.add_row(os_name, str(count))
    console.print(tbl)
    console.print()


def _print_threat_intel(console: Console, tags, frontend_base: str) -> None:
    has_tags = any([tags.malware_families, tags.botnets, tags.behavioral_ttp, tags.arch_file])
    if not has_tags:
        return
    console.print(Rule('[bold]Threat intel[/bold]', style='dim'))
    if tags.malware_families:
        console.print(
            f'  [bold magenta]Malware families[/bold magenta]'
            f'   {_fmt_tags(tags.malware_families, strip_prefix="family:", frontend_base=frontend_base)}'
        )
    if tags.botnets:
        unique = len(tags.botnets)
        top_str = _fmt_tags(
            tags.botnets, strip_prefix='botnet:', frontend_base=frontend_base, top_n=5
        )
        suffix = f'   [dim][{unique} unique botnet IDs][/dim]' if unique > 5 else ''
        console.print(f'  [bold magenta]Botnets tracked [/bold magenta]   {top_str}{suffix}')
    if tags.behavioral_ttp:
        console.print(
            f'  [bold magenta]Behavioral/TTP  [/bold magenta]'
            f'   {_fmt_tags(tags.behavioral_ttp, query_prefix="tag:", frontend_base=frontend_base)}'
        )
    if tags.arch_file:
        console.print(
            f'  [bold magenta]Arch / file type[/bold magenta]'
            f'   {_fmt_tags(tags.arch_file, query_prefix="tag:", frontend_base=frontend_base)}'
        )
    console.print()


def _print_iocs(console: Console, iocs, soar_skipped: bool, frontend_base: str) -> None:
    if iocs.extracted_c2:
        console.print(
            Rule('[bold]Extracted C2s[/bold]  (parsed from malware configs)', style='dim')
        )
        tbl = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
        tbl.add_column('URL', style='cyan')
        tbl.add_column('Count', style='bold')
        for c2_url, count in iocs.extracted_c2:
            if frontend_base:
                link = _search_url(frontend_base, f'url:{c2_url}')
                display = f'[link={link}]{c2_url}[/link]'
            else:
                display = c2_url
            tbl.add_row(display, str(count))
        console.print(tbl)
        console.print()

    if iocs.verified_network:
        console.print(Rule('[bold]Verified network IOCs[/bold]  (SOAR · score ≥ 25)', style='dim'))
        tbl = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
        tbl.add_column('Score', style='bold', width=5)
        tbl.add_column('Indicator', style='cyan', width=40, no_wrap=True)
        tbl.add_column('Rule', style='dim')
        for ioc in iocs.verified_network:
            score = _ioc_rf_score(ioc)
            color = 'red' if score >= 65 else 'yellow' if score >= 25 else 'grey50'
            indicator = _ioc_field(ioc, 'indicator')
            if frontend_base:
                link = _search_url(frontend_base, indicator)
                indicator_cell = f'[link={link}]{indicator}[/link]'
            else:
                indicator_cell = indicator
            tbl.add_row(
                f'[{color}]{score}[/{color}]',
                indicator_cell,
                _ioc_field(ioc, 'most_critical_rule') or '',
            )
        console.print(tbl)
        console.print()
    elif soar_skipped and iocs.extracted_c2:
        console.print(
            '  [dim]SOAR-validated IOCs skipped (RF_TOKEN not set or enrichment failed).[/dim]'
        )
        console.print()


def _print_hashes(console: Console, hashes: list, frontend_base: str) -> None:
    shown = hashes[:20]
    console.print(Rule('[bold]Malicious SHA256s[/bold]  (top 20)', style='dim'))
    tbl = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
    tbl.add_column('SHA256', style='cyan', no_wrap=True)
    for sha in shown:
        if frontend_base:
            link = _search_url(frontend_base, f'sha256:{sha}')
            display = f'[link={link}]{sha}[/link]'
        else:
            display = sha
        tbl.add_row(display)
    console.print(tbl)
    if len(hashes) > 20:
        console.print(
            f'  [dim]… and {len(hashes) - 20} more (use JSON output for the full list)[/dim]'
        )
    console.print()


def _to_json_dict(stats: SandboxStats) -> dict:
    return {
        'period_start': stats.period_start.isoformat(),
        'period_end': stats.period_end.isoformat(),
        'period_days': stats.period_days,
        'subset': stats.subset,
        'total': stats.total,
        'pending': stats.pending,
        'by_status': stats.by_status,
        'by_kind': stats.by_kind,
        'by_platform': stats.by_platform,
        'by_score': stats.by_score,
        'top_tags': {
            'malware_families': stats.top_tags.malware_families,
            'botnets': stats.top_tags.botnets,
            'arch_file': stats.top_tags.arch_file,
            'behavioral_ttp': stats.top_tags.behavioral_ttp,
        },
        'top_iocs': {
            'extracted_c2': [list(pair) for pair in stats.top_iocs.extracted_c2],
            'verified_network': [
                {
                    'indicator': _ioc_field(ioc, 'indicator'),
                    'type': _ioc_field(ioc, 'type'),
                    'rf_score': _ioc_rf_score(ioc),
                    'most_critical_rule': _ioc_field(ioc, 'most_critical_rule'),
                }
                for ioc in stats.top_iocs.verified_network
            ],
            'malicious_sha256': stats.top_iocs.malicious_sha256,
        },
        'trend_vs_prior_period': stats.trend_vs_prior_period,
        'limit_hit': stats.limit_hit,
        'soar_skipped': stats.soar_skipped,
    }


def print_sandbox_stats(stats: SandboxStats, pretty: bool = False, show_hashes: bool = False) -> None:
    if pretty:
        console = Console()
        frontend_base = _SANDBOX_FRONTEND_URLS.get(
            stats.sandbox_choice, _SANDBOX_FRONTEND_URLS['eu']
        )
        period = (
            f'{stats.period_start.strftime("%Y-%m-%d")} → {stats.period_end.strftime("%Y-%m-%d")}'
        )
        console.print()
        console.print(
            Rule(
                f'[bold]Sandbox · last {stats.period_days}d · {period} · {stats.subset}[/bold]',
                style='bold magenta',
            )
        )
        console.print()
        _print_summary(console, stats)
        _print_platform(console, stats.by_platform)
        _print_threat_intel(console, stats.top_tags, frontend_base)
        _print_iocs(console, stats.top_iocs, stats.soar_skipped, frontend_base)

        if show_hashes and stats.top_iocs.malicious_sha256:
            _print_hashes(console, stats.top_iocs.malicious_sha256, frontend_base)

        footer_parts = []
        if stats.top_iocs.malicious_sha256:
            n = len(stats.top_iocs.malicious_sha256)
            footer_parts.append(f'[bold]{n}[/bold] malicious SHA256s')
        if stats.pending:
            footer_parts.append(f'[yellow]{stats.pending}[/yellow] pending (not yet reported)')
        if footer_parts:
            console.print('  ' + '  ·  '.join(footer_parts))
        console.print()
    else:
        print_json(json.dumps(_to_json_dict(stats)), indent=2)
