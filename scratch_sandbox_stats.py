#!/usr/bin/env python3
"""Sandbox stats scratch script — exploration for PSF-1392.

Run with:
    RF_PROD_SANDBOX_TOKEN=<token> RF_TOKEN=<token> uv run python scratch_sandbox_stats.py
    RF_PROD_SANDBOX_TOKEN=<token> RF_TOKEN=<token> uv run python scratch_sandbox_stats.py --days 14 --subset owned

Findings validated against prod data:
  - Triage scores are 1-10, not 0-100
  - Platform comes from OverviewTask.os (behavioral tasks only), not tags
  - tags use namespaced prefixes: family:*, botnet:*, brand:*, os:* (rare)
  - targets[].iocs is raw network noise — must SOAR-validate before surfacing
  - extracted[].config.c2 is high-signal parsed C2 from malware configs

File extension sources (three tiers of cost):
  1. Sample.filename (free — already in the list fetch):
       The submitted filename. Extension = last dot-segment. Unreliable for
       extensionless uploads (many orgs use bare hashes as filenames).
  2. OverviewReport.sample.target (no extra cost — already in overview fetch):
       Same filename from the completed analysis. Often the same as Sample.filename
       but may differ for URL/fetch submissions where the server derives a name.
  3. StaticReportFile.exts (extra API call per sample — fetch_sample_static_report):
       Authoritative list of extensions from Triage static analysis. Populated even
       for extensionless files (Triage identifies by magic bytes). Most reliable but
       costs one extra API call per reported sample. Use --static-exts to enable.
"""

import json
import os
import sys
import time
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path as _Path

from psengine.helpers import MultiThreadingHelper
from psengine.sandbox import SandboxMgr
from psengine.sandbox.errors import SampleOverviewError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TOKEN = os.environ.get('RF_PROD_SANDBOX_TOKEN')
if not TOKEN:
    print('ERROR: RF_PROD_SANDBOX_TOKEN not set')
    sys.exit(1)

RF_TOKEN = os.environ.get('RF_TOKEN')
if not RF_TOKEN:
    print('WARNING: RF_TOKEN not set — SOAR IOC enrichment will be skipped')

parser = ArgumentParser(description='Sandbox stats scratch')
parser.add_argument('--days', type=int, default=7)
parser.add_argument('--subset', default='org', choices=['org', 'owned', 'public'])
parser.add_argument('--max-results', type=int, default=2000)
parser.add_argument('--workers', type=int, default=50)
parser.add_argument(
    '--static-exts',
    action='store_true',
    help='Fetch static reports to collect authoritative exts[] per file (expensive: 1 extra API call per sample)',
)
args = parser.parse_args()

DAYS = args.days
SUBSET = args.subset
MAX_RESULTS = args.max_results
WORKERS = args.workers


# Triage 1-10 score scale:
#   8-10 = malicious (known malware, high confidence)
#   5-7  = suspicious (strong behavioral indicators)
#   3-4  = potentially suspicious
#   1-2  = low risk / benign
def score_bucket(score):
    if score is None:
        return 'unknown'
    if score >= 8:
        return 'malicious'
    if score >= 5:
        return 'suspicious'
    if score >= 3:
        return 'potentially_suspicious'
    return 'clean'


# Arch/file-type tag set — unnamespaced tags matching these are file-type signals
ARCH_FILE_TAGS = {
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

SOAR_ENRICH_TOP_N = 50
SOAR_MIN_RISK_SCORE = 25  # 0-100 RF scale: 25=suspicious, 65=malicious, 90=very malicious

# ---------------------------------------------------------------------------
# Step 1 — fetch sample list (free, no extra API calls)
# ---------------------------------------------------------------------------

mgr = SandboxMgr(api_token=TOKEN)

now = datetime.now(timezone.utc)
cutoff_current = now - timedelta(days=DAYS)
cutoff_prev = now - timedelta(days=DAYS * 2)

print(f'\n=== Sandbox Stats  |  subset={SUBSET}  days={DAYS} ===')
print(f'Period:      {cutoff_current.date()} → {now.date()}')
print(f'Prev period: {cutoff_prev.date()} → {cutoff_current.date()}')

t0 = time.time()
all_samples = mgr.fetch_samples(subset=SUBSET, max_results=MAX_RESULTS)
fetch_elapsed = time.time() - t0

if len(all_samples) >= MAX_RESULTS:
    print(f'[WARNING] Hit --max-results={MAX_RESULTS} cap — stats may be incomplete')

current = [s for s in all_samples if s.submitted >= cutoff_current]
prev = [s for s in all_samples if cutoff_prev <= s.submitted < cutoff_current]

reported_current = [s for s in current if s.status == 'reported']
reported_prev = [s for s in prev if s.status == 'reported']

print(f'Fetched {len(all_samples)} total in {fetch_elapsed:.1f}s')
print(f'Current {DAYS}d: {len(current)} total, {len(reported_current)} reported')
print(f'Prev {DAYS}d:    {len(prev)} total, {len(reported_prev)} reported')
print(f'By status: {dict(Counter(s.status for s in current).most_common())}')
print(f'By kind:   {dict(Counter(s.kind for s in current).most_common())}')


# --- Tier 1: extensions from Sample.filename (free) ---
def _ext(name):
    """Return lowercased extension (e.g. '.exe') or '' if no dot or name is None."""
    if not name:
        return ''
    suffix = _Path(name).suffix.lower()
    return suffix or ''


ext_counter_filename = Counter(_ext(s.filename) for s in current)
print(f'\n--- File extensions (tier-1: Sample.filename, all {len(current)} current samples) ---')
for ext, cnt in ext_counter_filename.most_common(20):
    label = ext or '(no extension)'
    print(f'  {label:20s}: {cnt}')
print(f'  Unique extensions seen: {len(ext_counter_filename)}')

if not reported_current:
    print('No reported samples in window — nothing to enrich.')
    sys.exit(0)

# ---------------------------------------------------------------------------
# Step 2 — parallel overview fetch for reported samples (50 workers)
# ---------------------------------------------------------------------------


def _safe_fetch_overview(sample_id: str):
    try:
        return mgr.fetch_sample_overview_report(sample_id)
    except SampleOverviewError:
        return None
    except Exception as e:
        print(f'  [ERROR] {sample_id}: {e}')
        return None


print(f'\nFetching {len(reported_current)} overview reports ({WORKERS} workers)...')
t1 = time.time()

raw_results = MultiThreadingHelper.multithread_it(
    WORKERS,
    _safe_fetch_overview,
    iterator=[s.id_ for s in reported_current],
)
overview_elapsed = time.time() - t1

reports = [
    (sample, report) for sample, report in zip(reported_current, raw_results) if report is not None
]
print(
    f'Done in {overview_elapsed:.1f}s '
    f'({overview_elapsed / len(reported_current) * 1000:.0f}ms/sample) — '
    f'{len(reports)} ok, {len(reported_current) - len(reports)} skipped'
)

# --- Tier 2: extensions from OverviewReport.sample.target (no extra cost) ---
ext_counter_target = Counter(_ext(r.sample.target) for _, r in reports)
print(
    f'\n--- File extensions (tier-2: OverviewReport.sample.target, {len(reports)} overview reports) ---'
)
for ext, cnt in ext_counter_target.most_common(20):
    label = ext or '(no extension)'
    print(f'  {label:20s}: {cnt}')
print(f'  Unique extensions seen: {len(ext_counter_target)}')

# Also check per-target extensions (each report can have multiple targets = unpacked children)
ext_counter_all_targets = Counter()
for _, r in reports:
    for tgt in r.targets:
        ext_counter_all_targets[_ext(tgt.target)] += 1
print('\n--- File extensions (tier-2b: all OverviewTarget.target, incl. unpacked children) ---')
for ext, cnt in ext_counter_all_targets.most_common(20):
    label = ext or '(no extension)'
    print(f'  {label:20s}: {cnt}')
print(f'  Unique extensions seen: {len(ext_counter_all_targets)}')

# --- Tier 3: StaticReportFile.exts (extra API call per sample — only if --static-exts) ---
if args.static_exts:
    from psengine.sandbox.errors import SampleStaticReportError as _StatErr

    def _safe_fetch_static(sample_id: str):
        try:
            return mgr.fetch_sample_static_report(sample_id)
        except _StatErr:
            return None
        except Exception as e:
            print(f'  [ERROR static] {sample_id}: {e}')
            return None

    print(
        f'\nFetching {len(reported_current)} static reports for authoritative exts[] ({WORKERS} workers)...'
    )
    t_static = time.time()
    raw_static = MultiThreadingHelper.multithread_it(
        WORKERS,
        _safe_fetch_static,
        iterator=[s.id_ for s in reported_current],
    )
    static_elapsed = time.time() - t_static
    static_reports = [r for r in raw_static if r is not None]
    print(f'Done in {static_elapsed:.1f}s — {len(static_reports)} static reports fetched')

    ext_counter_static = Counter()
    for sr in static_reports:
        for f in sr.files:
            for e in f.exts:
                ext_counter_static[e.lower()] += 1

    print('\n--- File extensions (tier-3: StaticReportFile.exts, authoritative) ---')
    for ext, cnt in ext_counter_static.most_common(30):
        label = ext or '(empty)'
        print(f'  {label:20s}: {cnt}')
    print(f'  Unique extensions: {len(ext_counter_static)}')
    print(f'  Full dump: {dict(ext_counter_static.most_common())}')

# ---------------------------------------------------------------------------
# Score distribution (Triage 1-10)
# ---------------------------------------------------------------------------

score_counter = Counter(score_bucket(r.analysis.score) for _, r in reports)
raw_score_hist = dict(sorted(Counter(r.analysis.score for _, r in reports).items()))

print('\n--- Score distribution (1-10 scale) ---')
print(f'  Raw histogram: {raw_score_hist}')
for bucket in ('malicious', 'suspicious', 'potentially_suspicious', 'clean', 'unknown'):
    print(f'  {bucket:25s}: {score_counter.get(bucket, 0)}')

# ---------------------------------------------------------------------------
# Platform breakdown — from OverviewTask.os (behavioral tasks only)
# Filenames are mostly extensionless in this org; task.os is the correct source.
# ---------------------------------------------------------------------------

platform_counter = Counter()
for _, r in reports:
    for task in r.tasks.values():
        if task.kind == 'behavioral' and task.os:
            platform_counter[task.os] += 1

print('\n--- Platform (OverviewTask.os, behavioral tasks) ---')
for os_val, count in platform_counter.most_common():
    print(f'  {os_val}: {count}')

# ---------------------------------------------------------------------------
# Tag taxonomy — namespaced prefixes separate signal classes
# ---------------------------------------------------------------------------

all_tags = []
for _, r in reports:
    all_tags.extend(r.analysis.tags)
tag_counter = Counter(all_tags)

family_tags = {t: c for t, c in tag_counter.items() if t.startswith('family:')}
botnet_tags = {t: c for t, c in tag_counter.items() if t.startswith('botnet:')}
brand_tags = {t: c for t, c in tag_counter.items() if t.startswith('brand:')}
os_prefix_tags = {t: c for t, c in tag_counter.items() if t.startswith('os:')}

prefixed = set(family_tags) | set(botnet_tags) | set(brand_tags) | set(os_prefix_tags)
remaining = {t: c for t, c in tag_counter.items() if t not in prefixed}

arch_file_tags = {t: c for t, c in remaining.items() if t.lower() in ARCH_FILE_TAGS}
behavioral_tags = {t: c for t, c in remaining.items() if t.lower() not in ARCH_FILE_TAGS}

print('\n--- Tag taxonomy ---')
print(f'  Malware families (family:*): {dict(Counter(family_tags).most_common(10))}')
print(f'  Botnets (botnet:*):          {dict(Counter(botnet_tags).most_common(5))}')
print(f'  Arch/file:                   {dict(sorted(arch_file_tags.items(), key=lambda x: -x[1]))}')
print(f'  Behavioral/TTP:              {dict(Counter(behavioral_tags).most_common(15))}')

# ---------------------------------------------------------------------------
# IOC extraction — two-tier approach
#   Primary:   extracted[].config.c2  (parsed from malware config — zero noise)
#   Secondary: targets[].iocs IPs+domains → SOAR-validated (filters CDN/DNS noise)
# ---------------------------------------------------------------------------

malicious_pairs = [(s, r) for s, r in reports if score_bucket(r.analysis.score) == 'malicious']
print(f'\n--- IOC extraction (malicious={len(malicious_pairs)} samples) ---')

ip_counter = Counter()
domain_counter = Counter()
hashes = set()
extracted_c2 = Counter()  # parsed from malware configs — high signal

for sample, report in malicious_pairs:
    if report.sample.sha256:
        hashes.add(report.sample.sha256)
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

print(f'  Unique SHA256:              {len(hashes)}')
print(f'  Unique IPs (raw/unverified): {len(ip_counter)} — includes CDNs, DNS resolvers')
print(f'  Unique domains (raw):        {len(domain_counter)}')
print(f'  Extracted C2 hosts:          {len(extracted_c2)} (from malware configs)')
print(f'\n  Top extracted C2s: {extracted_c2.most_common(10)}')

# SOAR-validate the raw network IOCs — keep only those with RF risk score >= threshold
verified_iocs = []  # populated below if RF_TOKEN is set

if RF_TOKEN:
    from psengine.enrich import SoarMgr
    from psengine.enrich.errors import EnrichmentSoarError

    soar = SoarMgr(rf_token=RF_TOKEN)
    candidate_ips = [ip for ip, _ in ip_counter.most_common(SOAR_ENRICH_TOP_N)]
    candidate_domains = [d for d, _ in domain_counter.most_common(SOAR_ENRICH_TOP_N)]

    print(f'\n  SOAR-enriching top {len(candidate_ips)} IPs + {len(candidate_domains)} domains...')
    t_soar = time.time()
    try:
        soar_results = soar.soar(
            ip=candidate_ips or None,
            domain=candidate_domains or None,
            max_workers=10,
        )
        soar_elapsed = time.time() - t_soar
        print(f'  Done in {soar_elapsed:.1f}s  ({len(soar_results)} entities enriched)')

        risky = sorted(
            [r for r in soar_results if r.content and r.content.risk.score >= SOAR_MIN_RISK_SCORE],
            key=lambda r: r.content.risk.score,
            reverse=True,
        )
        print(f'  Verified IOCs (RF score >= {SOAR_MIN_RISK_SCORE}): {len(risky)}')
        for r in risky:
            c = r.content
            print(f'    [{c.risk.score:3d}] {r.entity:45s}  {c.risk.rule.most_critical}')

        verified_iocs = [
            {
                'indicator': r.entity,
                'type': r.content.entity.type_,
                'rf_score': r.content.risk.score,
                'most_critical_rule': r.content.risk.rule.most_critical,
            }
            for r in risky
        ]
    except EnrichmentSoarError as e:
        print(f'  SOAR enrichment failed: {e}')
else:
    print('\n  SOAR validation skipped (RF_TOKEN not set).')

# ---------------------------------------------------------------------------
# Trend
# ---------------------------------------------------------------------------


def _trend(label, curr, prev_val):
    if prev_val == 0:
        return f'{label:22s}: {curr:4d}  vs {prev_val:4d}  (no prior data)'
    delta = curr - prev_val
    pct = (delta / prev_val) * 100
    return f'{label:22s}: {curr:4d}  vs {prev_val:4d}  {delta:+d} ({pct:+.0f}%)'


print(f'\n--- Trend (current vs prior {DAYS}d) ---')
print(_trend('Total', len(current), len(prev)))
print(_trend('Reported', len(reported_current), len(reported_prev)))
print(_trend('Malicious (8-10)', score_counter.get('malicious', 0), 0))
# Note: malicious trend vs prior period requires fetching prev overviews too (2x cost).
# For the real command: fetch prev overviews in parallel with current, or accept score
# trend is only shown when the operator explicitly requests --compare.

# ---------------------------------------------------------------------------
# Target JSON output shape
# ---------------------------------------------------------------------------

print('\n--- Target JSON output ---')
print(
    json.dumps(
        {
            'period_start': cutoff_current.isoformat(),
            'period_end': now.isoformat(),
            'period_days': DAYS,
            'total': len(current),
            'pending': sum(1 for s in current if s.status != 'reported'),
            'by_status': dict(Counter(s.status for s in current).most_common()),
            'by_kind': dict(Counter(s.kind for s in current).most_common()),
            'by_platform': dict(platform_counter.most_common()),
            'by_score': dict(score_counter),
            'top_tags': {
                'malware_families': dict(Counter(family_tags).most_common(10)),
                'botnets': dict(Counter(botnet_tags).most_common(10)),
                'arch_file': dict(Counter(arch_file_tags).most_common(5)),
                'behavioral_ttp': dict(Counter(behavioral_tags).most_common(15)),
            },
            'top_iocs': {
                'extracted_c2': extracted_c2.most_common(10),
                'verified_network': verified_iocs,  # SOAR-validated only, no raw noise
                'malicious_sha256': list(hashes)[:10],
            },
            'trend_vs_prior_period': {
                'total': {'current': len(current), 'prev': len(prev)},
                'reported': {'current': len(reported_current), 'prev': len(reported_prev)},
            },
            'timing': {
                'list_fetch_s': round(fetch_elapsed, 2),
                'overview_fetch_s': round(overview_elapsed, 2),
                'overview_count': len(reports),
            },
        },
        indent=2,
        default=str,
    )
)
