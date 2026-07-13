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

import json
from datetime import timedelta
from urllib.parse import quote, quote_plus

from rich import print_json
from rich.columns import Columns
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from .stats import SandboxStats, VerifiedIoc

_SCORE_COLORS = {
    'malicious': 'red',
    'suspicious': 'dark_orange',
    'potentially_suspicious': 'yellow',
    'clean': 'green',
    'unknown': 'grey50',
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


_INTEL_CARD_BASE = 'https://app.recordedfuture.com/portal/intelligence-card'
_INTEL_CARD_TYPE = {
    'IpAddress': 'ip',
    'InternetDomainName': 'idn',
    'URL': 'url',
    'Hash': 'hash',
}


def _intel_card_url(rf_type: str, value: str) -> str:
    return f'{_INTEL_CARD_BASE}/{quote(f"{rf_type}:{value}", safe="")}'


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


_CHART_FAMILIES = 8
_SPARK_CHARS = '▁▂▃▄▅▆▇█'
_SPARK_MAX_BUCKETS = 40
_FAMILY_COLORS = [
    'steel_blue1',
    'green3',
    'magenta',
    'yellow',
    'cyan',
    'orange1',
    'bright_red',
    'medium_purple',
]


def _bucket_counts(counts: list, max_buckets: int) -> list:
    """Aggregate counts into at most max_buckets by summing consecutive groups."""
    n = len(counts)
    if n <= max_buckets:
        return counts
    result = []
    for i in range(max_buckets):
        start = round(i * n / max_buckets)
        end = round((i + 1) * n / max_buckets)
        result.append(sum(counts[start:end]))
    return result


def _sparkline(counts: list, global_max: int) -> str:
    if global_max == 0:
        return _SPARK_CHARS[0] * len(counts)
    result = []
    for c in counts:
        if c == 0:
            result.append(_SPARK_CHARS[0])
        else:
            level = max(1, min(7, round(c / global_max * 7)))
            result.append(_SPARK_CHARS[level])
    return ''.join(result)


def _trend_str(current: int, prev: int) -> str:
    """Return a Rich-markup trend indicator, or '' when prior period is unknown."""
    if prev == 0:
        return ''
    if current == prev:
        return '[dim]—[/dim]'
    pct = round(abs(current - prev) / prev * 100)
    if current > prev:
        return f'[red]↑ {pct}%[/red]'
    return f'[green]↓ {pct}%[/green]'


def _trend_pct(current: int, prev: int):
    """Return signed percentage change, or None when prior period is zero."""
    if prev == 0:
        return None
    return round((current - prev) / prev * 100)


def _summary_lines(stats: SandboxStats) -> list:
    trend = stats.trend_vs_prior_period
    total = trend['total']['current']
    analyzed = trend['reported']['current']
    submissions_trend = _trend_str(total, trend['total']['prev'])
    submissions_cell = f'[bold]{total:,}[/bold] submissions'
    if submissions_trend:
        submissions_cell += f' {submissions_trend}'
    kind_parts = []
    for k, v in stats.by_kind.items():
        t = _trend_str(v, stats.by_kind_prev.get(k, 0))
        kind_parts.append(f'{k}: {v}' + (f' {t}' if t else ''))
    kind_str = '  '.join(kind_parts)
    header_parts = [
        submissions_cell,
        f'[bold]{analyzed:,}[/bold] analyzed',
    ]
    if stats.pending:
        header_parts.append(f'[bold]{stats.pending:,}[/bold] pending')
    if stats.failed:
        header_parts.append(f'[bold red]{stats.failed:,}[/bold red] failed')
    lines = [
        f'  [dim]·[/dim]  '.join(header_parts),
        '',
        f'[dim]by kind  [/dim]  {kind_str}',
    ]
    if stats.by_score:
        buckets = [
            (b, stats.by_score[b])
            for b in ('malicious', 'suspicious', 'potentially_suspicious', 'clean')
            if stats.by_score.get(b, 0)
        ]
        if buckets:
            max_count = max(c for _, c in buckets)
            count_w = max(len(str(c)) for _, c in buckets)
            label_w = max(len(_SCORE_SHORT_LABELS[b]) for b, _ in buckets)
            lines.append('')
            for i, (bucket, count) in enumerate(buckets):
                color = _SCORE_COLORS[bucket]
                label = _SCORE_SHORT_LABELS[bucket].ljust(label_w)
                bar_len = max(1, round(count / max_count * _SCORE_BAR_WIDTH))
                bar = _BAR_CHAR * bar_len
                prefix = '[dim]by score[/dim]  ' if i == 0 else '          '
                lines.append(
                    f'{prefix}[{color}]{label}[/{color}]'
                    f'  {count:>{count_w}}  [{color}]{bar}[/{color}]'
                )
    return lines


def _print_summary(console: Console, stats: SandboxStats) -> None:
    for line in _summary_lines(stats):
        console.print(f'  {line}' if line else '')
    console.print()


def _print_chart_and_summary(console: Console, stats: SandboxStats) -> None:
    daily_by_family = stats.daily_by_family

    if not daily_by_family:
        _print_summary(console, stats)
        return

    all_dates = []
    d = stats.period_start.date()
    end = stats.period_end.date()
    while d <= end:
        all_dates.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)

    totals = {f: sum(v.values()) for f, v in daily_by_family.items()}
    top_families = sorted(totals, key=lambda k: totals[k], reverse=True)[:_CHART_FAMILIES]

    # Bucket large windows down to _SPARK_MAX_BUCKETS; short windows stay one-day-per-slot.
    # Stretch each slot for readability: ≤10 slots → 4 chars, ≤20 → 2, else → 1.
    n = len(all_dates)
    raw_by_family = {f: [daily_by_family[f].get(ds, 0) for ds in all_dates] for f in top_families}
    bucketed = {f: _bucket_counts(raw_by_family[f], _SPARK_MAX_BUCKETS) for f in top_families}
    n_display = len(next(iter(bucketed.values()))) if bucketed else n
    bar_w = 4 if n_display <= 10 else 2 if n_display <= 20 else 1
    total_width = n_display * bar_w

    all_nonzero = [c for f in top_families for c in bucketed[f] if c > 0]
    global_max = max(all_nonzero) if all_nonzero else 0

    # Date axis label scaled to the stretched (bucketed) sparkline width
    start_lbl = stats.period_start.strftime('%-d %b')
    end_lbl = stats.period_end.strftime('%-d %b')
    date_spark = ''
    if total_width >= len(start_lbl) + len(end_lbl) + 2:
        gap = total_width - len(start_lbl) - len(end_lbl)
        date_spark = f'[dim]{start_lbl}{" " * gap}{end_lbl}[/dim]'

    # Build left (chart) rows
    chart_rows: list[tuple[str, str, str]] = []
    for i, family in enumerate(top_families):
        color = _FAMILY_COLORS[i % len(_FAMILY_COLORS)]
        counts = bucketed[family]
        peak = max(raw_by_family[family]) if raw_by_family[family] else 0
        spark = ''.join(c * bar_w for c in _sparkline(counts, global_max))
        chart_rows.append((family, f'[{color}]{spark}[/{color}]', str(peak)))
    chart_rows.append(('', date_spark, ''))

    right_lines = _summary_lines(stats)

    # Single table: stats column | │ divider | chart columns.
    # The │ appears in every row so it spans the full height naturally.
    tbl = Table(show_header=False, box=None, padding=(0, 1, 0, 1), expand=True)
    tbl.add_column('Stats', no_wrap=False)
    tbl.add_column('Sep', justify='center', width=1, no_wrap=True)
    tbl.add_column('Family', style='dim', justify='right', width=16, no_wrap=True)
    tbl.add_column('Spark', no_wrap=True)
    tbl.add_column('Peak', style='bold dim', justify='right', width=5)
    tbl.add_column('Filler', ratio=1)

    total_rows = max(len(chart_rows), len(right_lines))
    for i in range(total_rows):
        fam, spark, peak = chart_rows[i] if i < len(chart_rows) else ('', '', '')
        right = right_lines[i] if i < len(right_lines) else ''
        tbl.add_row(right, '[dim]│[/dim]', fam, spark, peak, '')

    console.print(tbl)
    console.print()


_BAR_WIDTH = 28
_BAR_WIDTH_HALF = 16
_BAR_CHAR = '█'
_PANEL_TOP_N = 8
_SCORE_BAR_WIDTH = 12
_SCORE_SHORT_LABELS = {
    'malicious': 'malicious (8–10)',
    'suspicious': 'suspicious (5–7)',
    'potentially_suspicious': 'likely benign (3–4)',
    'clean': 'no threat (1–2)',
    'unknown': 'unknown',
}


def _platform_table(by_platform: dict) -> Table:
    tbl = Table(
        title='[dim]Platform[/dim]',
        title_justify='left',
        show_header=False,
        box=None,
        padding=(0, 2, 0, 0),
        expand=True,
    )
    tbl.add_column('OS', style='cyan', no_wrap=True)
    tbl.add_column('Count', style='bold', justify='right', width=5)
    for os_name, count in by_platform.items():
        tbl.add_row(os_name, str(count))
    return tbl


def _file_type_table(by_file_type: dict) -> Table:
    max_count = max(by_file_type.values())
    tbl = Table(
        title='[dim]File types[/dim]',
        title_justify='left',
        show_header=False,
        box=None,
        padding=(0, 1, 0, 0),
        expand=True,
    )
    tbl.add_column('Type', style='dim', justify='right', width=8, no_wrap=True)
    tbl.add_column('Count', style='bold', justify='right', width=5)
    tbl.add_column('Bar', no_wrap=True)
    for ext, count in by_file_type.items():
        bar_len = max(1, int(count / max_count * _BAR_WIDTH_HALF))
        bar = f'[steel_blue1]{_BAR_CHAR * bar_len}[/steel_blue1]'
        tbl.add_row(ext, str(count), bar)
    return tbl


def _print_submission_profile(console: Console, by_platform: dict, by_file_type: dict) -> None:
    if not by_platform and not by_file_type:
        return
    console.print(Rule('[bold]Submission profile[/bold]', style='dim'))
    cols = []
    if by_platform:
        cols.append(_platform_table(by_platform))
    if by_file_type:
        cols.append(_file_type_table(by_file_type))
    console.print(Columns(cols, equal=True, expand=True))
    console.print()


def _make_threat_col(
    title: str,
    tags: dict,
    strip_prefix: str = '',
    query_prefix: str = '',
    frontend_base: str = '',
    top_n: int = _PANEL_TOP_N,
) -> Table:
    items = list(tags.items())[:top_n]
    tbl = Table(
        title=f'[bold magenta]{title}[/bold magenta]',
        title_justify='center',
        show_header=False,
        box=None,
        padding=(0, 2, 0, 2),
        expand=True,
    )
    tbl.add_column('Name', style='cyan')
    tbl.add_column('Count', style='bold dim', justify='right', width=5, no_wrap=True)
    for tag, count in items:
        name = tag[len(strip_prefix) :] if strip_prefix else tag
        if frontend_base:
            query = f'{query_prefix}{tag}' if query_prefix else tag
            url = _search_url(frontend_base, query)
            cell = f'[link={url}]{name}[/link]'
        else:
            cell = name
        tbl.add_row(cell, str(count))
    return tbl


def _print_threat_intel(console: Console, tags, frontend_base: str) -> None:
    has_tags = any([tags.malware_families, tags.botnets, tags.behavioral_ttp])
    if not has_tags:
        return
    console.print(Rule('[bold]Threat intel[/bold]', style='dim'))
    cols = []
    if tags.malware_families:
        cols.append(
            _make_threat_col(
                'Malware families',
                tags.malware_families,
                strip_prefix='family:',
                frontend_base=frontend_base,
            )
        )
    if tags.behavioral_ttp:
        cols.append(
            _make_threat_col(
                'Behavioral / TTP',
                tags.behavioral_ttp,
                query_prefix='tag:',
                frontend_base=frontend_base,
            )
        )
    if tags.botnets:
        cols.append(
            _make_threat_col(
                'Botnets',
                tags.botnets,
                strip_prefix='botnet:',
                frontend_base=frontend_base,
                top_n=5,
            )
        )
    if cols:
        console.print(Columns(cols, equal=True, expand=True))
        console.print()


_DISPLAY_CAP = 10
_MORE_MSG = '  [dim]… and {} more (use JSON output for the full list)[/dim]'


def _print_iocs(console: Console, iocs, soar_skipped: bool) -> None:
    if iocs.extracted_c2:
        total = len(iocs.extracted_c2)
        console.print(Rule('[bold]Extracted C2s[/bold]', style='dim'))
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('Risk Score', style='bold', width=10)
        tbl.add_column('Hits', style='bold', width=7)
        tbl.add_column('URL', style='cyan')
        tbl.add_column('Top Risk Rule', style='dim')
        for c2_url, count in iocs.extracted_c2[:_DISPLAY_CAP]:
            hit_color = 'red' if count >= 5 else 'yellow' if count >= 2 else 'grey50'
            soar = iocs.c2_soar.get(c2_url) or {}
            display = f'[link={_intel_card_url("url", c2_url)}]{c2_url}[/link]'
            tbl.add_row(
                _rf_score_cell(soar.get('rf_score')),
                f'[{hit_color}]{count}[/{hit_color}]',
                display,
                soar.get('top_risk_rule') or '',
            )
        console.print(tbl)
        if total > _DISPLAY_CAP:
            console.print(_MORE_MSG.format(total - _DISPLAY_CAP))
        console.print()

    if iocs.verified_network:
        total = len(iocs.verified_network)
        console.print(Rule('[bold]Verified network IOCs[/bold]', style='dim'))
        tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
        tbl.add_column('Risk Score', style='bold', width=10)
        tbl.add_column('Indicator', style='cyan', width=40, no_wrap=True)
        tbl.add_column('Top Risk Rule', style='dim')
        for ioc in iocs.verified_network[:_DISPLAY_CAP]:
            score = _ioc_rf_score(ioc)
            color = 'red' if score >= 65 else 'yellow' if score >= 25 else 'grey50'
            indicator = _ioc_field(ioc, 'indicator')
            rf_type = _INTEL_CARD_TYPE.get(_ioc_field(ioc, 'type'), 'ip')
            indicator_cell = f'[link={_intel_card_url(rf_type, indicator)}]{indicator}[/link]'
            tbl.add_row(
                f'[{color}]{score}[/{color}]',
                indicator_cell,
                _ioc_field(ioc, 'most_critical_rule') or '',
            )
        console.print(tbl)
        if total > _DISPLAY_CAP:
            console.print(_MORE_MSG.format(total - _DISPLAY_CAP))
        console.print()
    elif soar_skipped and iocs.extracted_c2:
        console.print(
            '  [dim]SOAR-validated IOCs skipped (RF_TOKEN not set or enrichment failed).[/dim]'
        )
        console.print()


def _rf_score_cell(rf_score) -> str:
    if not rf_score:
        return '[grey50]—[/grey50]'
    color = 'red' if rf_score >= 65 else 'yellow' if rf_score >= 25 else 'grey50'
    return f'[{color}]{rf_score}[/{color}]'


def _print_hashes(console: Console, hashes: list, frontend_base: str) -> None:
    shown = hashes[:_DISPLAY_CAP]
    total = len(hashes)
    console.print(Rule('[bold]Malicious SHA256s[/bold]', style='dim'))
    tbl = Table(show_header=True, box=None, padding=(0, 2, 0, 2), header_style='dim')
    tbl.add_column('Sandbox Score', style='bold', width=13)
    tbl.add_column('Risk Score', style='bold', width=10)
    tbl.add_column('SHA256', style='cyan', no_wrap=True)
    tbl.add_column('Family', style='dim')
    tbl.add_column('Top Risk Rule', style='dim')
    for entry in shown:
        score = entry['score']
        sha = entry['sha256']
        top_tag = entry.get('top_tag', '')
        color = 'red' if score >= 9 else 'dark_orange'
        display = f'[link={_intel_card_url("hash", sha)}]{sha}[/link]'
        if frontend_base and top_tag:
            family_url = _search_url(frontend_base, f'family:{top_tag}')
            family_cell = f'[link={family_url}]{top_tag}[/link]'
        else:
            family_cell = top_tag
        tbl.add_row(
            f'[{color}]{score}[/{color}]',
            _rf_score_cell(entry.get('rf_score')),
            display,
            family_cell,
            entry.get('top_risk_rule') or '',
        )
    console.print(tbl)
    if total > _DISPLAY_CAP:
        console.print(_MORE_MSG.format(total - _DISPLAY_CAP))
    console.print()


def _to_json_dict(stats: SandboxStats) -> dict:
    return {
        'period_start': stats.period_start.isoformat(),
        'period_end': stats.period_end.isoformat(),
        'period_days': stats.period_days,
        'subset': stats.subset,
        'total': stats.total,
        'pending': stats.pending,
        'failed': stats.failed,
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
            'extracted_c2': [
                {
                    'url': url,
                    'count': count,
                    'rf_score': (stats.top_iocs.c2_soar.get(url) or {}).get('rf_score'),
                    'top_risk_rule': (stats.top_iocs.c2_soar.get(url) or {}).get('top_risk_rule'),
                }
                for url, count in stats.top_iocs.extracted_c2
            ],
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
        'by_file_type': stats.by_file_type,
        'daily_by_family': stats.daily_by_family,
        'trend_vs_prior_period': {
            k: {**v, 'pct_change': _trend_pct(v['current'], v['prev'])}
            for k, v in stats.trend_vs_prior_period.items()
        },
        'limit_hit': stats.limit_hit,
        'soar_skipped': stats.soar_skipped,
    }


def print_sandbox_stats(stats: SandboxStats, pretty: bool = False) -> None:
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
        _print_chart_and_summary(console, stats)
        _print_submission_profile(console, stats.by_platform, stats.by_file_type)
        _print_threat_intel(console, stats.top_tags, frontend_base)
        _print_iocs(console, stats.top_iocs, stats.soar_skipped)

        if stats.top_iocs.malicious_sha256:
            _print_hashes(console, stats.top_iocs.malicious_sha256, frontend_base)

        console.print()
    else:
        print_json(json.dumps(_to_json_dict(stats)), indent=2)
