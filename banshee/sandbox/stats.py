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

import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from psengine.config import get_config
from psengine.enrich import SoarMgr
from psengine.enrich.errors import EnrichmentSoarError
from psengine.helpers import MultiThreadingHelper
from psengine.sandbox import SandboxMgr
from psengine.sandbox.errors import SampleOverviewError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

_ARCH_FILE_TAGS = {
    'pe',
    'pe32',
    'pe64',
    'x86',
    'x64',
    'elf',
    'mach-o',
    'apk',
    'dex',
    'office',
    'doc',
    'docx',
    'xls',
    'xlsx',
    'pdf',
    'powershell',
    'vbs',
    'js',
    'jscript',
    'script',
    'bat',
    'cmd',
    'hta',
    'jar',
    'zip',
    'archive',
    'iso',
    'img',
    'lnk',
    'dll',
    'exe',
}

_OVERVIEW_WORKERS = 50
_SOAR_WORKERS = 10
_SOAR_TOP_N = 50
_SOAR_MIN_SCORE = 25
_DEFAULT_MAX_RESULTS = 2000

_ERR_CONSOLE = Console(stderr=True)


def _score_bucket(score) -> str:
    if score is None:
        return 'unknown'
    if score >= 8:
        return 'malicious'
    if score >= 5:
        return 'suspicious'
    if score >= 3:
        return 'potentially_suspicious'
    return 'clean'


def _spinner(_label: str = '') -> Progress:
    """Create a transient stderr spinner."""
    return Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=_ERR_CONSOLE,
    )


@dataclass
class TopTags:
    """Classified tag counts from overview reports."""

    malware_families: dict = field(default_factory=dict)
    botnets: dict = field(default_factory=dict)
    arch_file: dict = field(default_factory=dict)
    behavioral_ttp: dict = field(default_factory=dict)


@dataclass
class VerifiedIoc:
    """A SOAR-validated network indicator."""

    indicator: str
    type: str
    rf_score: int
    most_critical_rule: str


@dataclass
class TopIocs:
    """Extracted and verified IOCs from malicious samples."""

    extracted_c2: list = field(default_factory=list)  # [(url, count), ...]
    verified_network: list = field(default_factory=list)  # [VerifiedIoc, ...]
    malicious_sha256: list = field(default_factory=list)


@dataclass
class SandboxStats:
    """Aggregated sandbox submission statistics for a time window."""

    period_start: datetime
    period_end: datetime
    period_days: int
    subset: str
    total: int
    pending: int
    by_status: dict
    by_kind: dict
    by_platform: dict
    by_score: dict
    top_tags: TopTags
    top_iocs: TopIocs
    trend_vs_prior_period: dict
    limit_hit: bool = False
    soar_skipped: bool = False
    sandbox_choice: str = 'eu'


def _fetch_overviews(mgr: SandboxMgr, reported: list) -> list:
    """Fetch overview reports in parallel; silently skip unavailable ones."""

    def _safe(sample_id: str):
        try:
            return mgr.fetch_sample_overview_report(sample_id)
        except SampleOverviewError:
            return None

    label = f'Enriching {len(reported)} overview reports…'
    with _spinner(label) as progress:
        progress.add_task(label)
        raw = MultiThreadingHelper.multithread_it(
            _OVERVIEW_WORKERS,
            _safe,
            iterator=[s.id_ for s in reported],
        )
    return [(s, r) for s, r in zip(reported, raw) if r is not None]


def _build_score_and_platform(reports: list) -> tuple:
    """Return (by_score dict, by_platform dict) from overview reports."""
    score_counter: Counter = Counter(_score_bucket(r.analysis.score) for _, r in reports)
    platform_counter: Counter = Counter()
    for _, r in reports:
        for task in r.tasks.values():
            if task.kind == 'behavioral' and task.os:
                platform_counter[task.os] += 1
    return dict(score_counter), dict(platform_counter.most_common())


def _build_tag_taxonomy(reports: list) -> TopTags:
    """Classify tags into malware families, botnets, arch/file, and behavioral TTPs."""
    all_tags: list[str] = []
    for _, r in reports:
        all_tags.extend(r.analysis.tags)
    tag_counter = Counter(all_tags)

    family_tags = {t: c for t, c in tag_counter.items() if t.startswith('family:')}
    botnet_tags = {t: c for t, c in tag_counter.items() if t.startswith('botnet:')}
    prefixed = (
        set(family_tags)
        | set(botnet_tags)
        | {t for t in tag_counter if t.startswith(('brand:', 'os:'))}
    )
    remaining = {t: c for t, c in tag_counter.items() if t not in prefixed}
    arch_file = {t: c for t, c in remaining.items() if t.lower() in _ARCH_FILE_TAGS}
    behavioral_ttp = {t: c for t, c in remaining.items() if t.lower() not in _ARCH_FILE_TAGS}

    return TopTags(
        malware_families=dict(Counter(family_tags).most_common(10)),
        botnets=dict(Counter(botnet_tags).most_common(10)),
        arch_file=dict(Counter(arch_file).most_common(5)),
        behavioral_ttp=dict(Counter(behavioral_ttp).most_common(15)),
    )


def _extract_raw_iocs(malicious: list) -> tuple:
    """Extract raw IOCs and SHA256 hashes from malicious samples."""
    ip_counter: Counter = Counter()
    domain_counter: Counter = Counter()
    sha256_map: dict[str, dict] = {}
    extracted_c2: Counter = Counter()

    for _, report in malicious:
        sha256 = report.sample.sha256
        if sha256 and sha256 not in sha256_map:
            top_tag = next(
                (t[len('family:'):] for t in report.analysis.tags if t.startswith('family:')), ''
            )
            sha256_map[sha256] = {'sha256': sha256, 'score': report.analysis.score, 'top_tag': top_tag}
        for target in report.targets:
            if target.iocs:
                ip_counter.update(target.iocs.ips)
                domain_counter.update(target.iocs.domains)
        for ex in report.extracted:
            if ex.config and ex.config.c2:
                extracted_c2.update(ex.config.c2)
            if ex.dropper:
                for durl in ex.dropper.urls:
                    if durl.url:
                        extracted_c2[durl.url] += 1

    return ip_counter, domain_counter, list(sha256_map.values()), extracted_c2


def _soar_enrich(ip_counter: Counter, domain_counter: Counter) -> tuple:
    """SOAR-validate top raw IOCs. Returns (verified_iocs, soar_skipped)."""
    if not ip_counter and not domain_counter:
        return [], True

    rf_token = get_config().rf_token
    if not rf_token or not rf_token.get_secret_value():
        print('NOTE: SOAR validation skipped — RF_TOKEN not set.', file=sys.stderr)
        return [], True

    candidate_ips = [ip for ip, _ in ip_counter.most_common(_SOAR_TOP_N)]
    candidate_domains = [d for d, _ in domain_counter.most_common(_SOAR_TOP_N)]
    n_ips, n_dom = len(candidate_ips), len(candidate_domains)
    label = f'SOAR-enriching {n_ips} IPs + {n_dom} domains…'

    try:
        with _spinner(label) as progress:
            progress.add_task(label)
            soar_results = SoarMgr().soar(
                ip=candidate_ips or None,
                domain=candidate_domains or None,
                max_workers=_SOAR_WORKERS,
            )
    except EnrichmentSoarError:
        print('NOTE: SOAR enrichment failed — skipping network IOC validation.', file=sys.stderr)
        return [], True

    risky = sorted(
        [r for r in soar_results if r.content and r.content.risk.score >= _SOAR_MIN_SCORE],
        key=lambda r: r.content.risk.score,
        reverse=True,
    )
    verified = [
        VerifiedIoc(
            indicator=r.entity,
            type=r.content.entity.type_,
            rf_score=r.content.risk.score,
            most_critical_rule=r.content.risk.rule.most_critical,
        )
        for r in risky
    ]
    return verified, False


def fetch_sandbox_stats(
    days: int = 7,
    subset: str = 'org',
    limit: int = 0,
) -> SandboxStats:
    """Aggregate sandbox submissions over a configurable time window.

    Fetches 2× the window so the prior period is available for trend comparison
    without a second API call. Overview reports are fetched in parallel.

    Args:
        days: Lookback window in days (default 7). Prior period = same length before window.
        subset: Sample scope — 'org' (org-wide) or 'owned' (current user).
        limit: Cap on total samples fetched. 0 means use the default cap (2000).
            Prints a warning if the cap is reached.

    Returns:
        SandboxStats dataclass with all aggregated counts and IOCs.
    """
    config = get_config()
    mgr = SandboxMgr(sandbox_choice=config.sandbox_choice)

    now = datetime.now(timezone.utc)
    cutoff_current = now - timedelta(days=days)
    cutoff_prev = now - timedelta(days=days * 2)

    max_results = limit if limit > 0 else _DEFAULT_MAX_RESULTS

    label = 'Fetching sandbox submissions…'
    with _spinner(label) as progress:
        progress.add_task(label)
        all_samples = mgr.fetch_samples(subset=subset, max_results=max_results)

    limit_hit = limit > 0 and len(all_samples) >= limit
    if limit_hit:
        print(f'[WARNING] Hit --limit={limit} cap — stats may be incomplete.', file=sys.stderr)

    current = [s for s in all_samples if s.submitted >= cutoff_current]
    prev = [s for s in all_samples if cutoff_prev <= s.submitted < cutoff_current]
    reported_current = [s for s in current if s.status == 'reported']
    reported_prev = [s for s in prev if s.status == 'reported']

    by_status = dict(Counter(s.status for s in current).most_common())
    by_kind = dict(Counter(s.kind for s in current).most_common())
    pending = sum(1 for s in current if s.status != 'reported')
    trend = {
        'total': {'current': len(current), 'prev': len(prev)},
        'reported': {'current': len(reported_current), 'prev': len(reported_prev)},
    }

    if not reported_current:
        return SandboxStats(
            period_start=cutoff_current,
            period_end=now,
            period_days=days,
            subset=subset,
            total=len(current),
            pending=pending,
            by_status=by_status,
            by_kind=by_kind,
            by_platform={},
            by_score={},
            top_tags=TopTags(),
            top_iocs=TopIocs(),
            trend_vs_prior_period=trend,
            limit_hit=limit_hit,
            soar_skipped=True,
            sandbox_choice=config.sandbox_choice,
        )

    reports = _fetch_overviews(mgr, reported_current)
    by_score, by_platform = _build_score_and_platform(reports)
    top_tags = _build_tag_taxonomy(reports)

    malicious = [(s, r) for s, r in reports if _score_bucket(r.analysis.score) == 'malicious']
    ip_ctr, dom_ctr, sha256_entries, extracted_c2 = _extract_raw_iocs(malicious)
    verified, soar_skipped = _soar_enrich(ip_ctr, dom_ctr)

    top_iocs = TopIocs(
        extracted_c2=extracted_c2.most_common(),
        verified_network=verified,
        malicious_sha256=sorted(sha256_entries, key=lambda x: x['score'], reverse=True),
    )

    return SandboxStats(
        period_start=cutoff_current,
        period_end=now,
        period_days=days,
        subset=subset,
        total=len(current),
        pending=pending,
        by_status=by_status,
        by_kind=by_kind,
        by_platform=by_platform,
        by_score=by_score,
        top_tags=top_tags,
        top_iocs=top_iocs,
        trend_vs_prior_period=trend,
        limit_hit=limit_hit,
        soar_skipped=soar_skipped,
        sandbox_choice=config.sandbox_choice,
    )
