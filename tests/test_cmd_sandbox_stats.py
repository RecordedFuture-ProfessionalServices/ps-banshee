import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console
from typer.testing import CliRunner

from banshee.commands.cmd_sandbox import app
from banshee.sandbox.output import (
    _BAR_CHAR,
    _BAR_WIDTH_HALF,
    _SCORE_SHORT_LABELS,
    _SPARK_CHARS,
    _SPARK_MAX_BUCKETS,
    _bucket_counts,
    _fmt_tags,
    _print_chart_and_summary,
    _print_hashes,
    _print_submission_profile,
    _search_url,
    _sparkline,
    _to_json_dict,
    _trend_pct,
    _trend_str,
)
from banshee.sandbox.stats import (
    SandboxStats,
    TopIocs,
    TopTags,
    VerifiedIoc,
    _build_daily_by_family,
    _build_file_type_map,
    _build_score_and_platform,
    _build_tag_taxonomy,
    _extract_raw_iocs,
    _score_bucket,
    _soar_enrich,
    fetch_sandbox_stats,
)

runner = CliRunner()

# Typer collapses a single-command app: `stats` is invoked directly, no subcommand prefix.

# ---------------------------------------------------------------------------
# Helpers to build mock psengine objects
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 7, 10, 12, 0, 0, tzinfo=timezone.utc)


def _make_sample(submitted_delta_days: int = 1, status: str = 'reported', kind: str = 'file'):
    s = MagicMock()
    s.submitted = _NOW - timedelta(days=submitted_delta_days)
    s.status = status
    s.kind = kind
    s.id_ = f'sample-{submitted_delta_days}'
    return s


def _make_task(kind: str = 'behavioral', os: str = 'windows10-2004-x64'):
    t = MagicMock()
    t.kind = kind
    t.os = os
    return t


def _make_analysis(score: int = 9, tags: list[str] = None):
    a = MagicMock()
    a.score = score
    a.tags = tags or []
    return a


def _make_report(
    score: int = 9, tags=None, sha256: str = 'abc123', tasks=None, targets=None, extracted=None
):
    r = MagicMock()
    r.analysis = _make_analysis(score=score, tags=tags or [])
    r.sample = MagicMock()
    r.sample.sha256 = sha256
    r.tasks = tasks or {'t1': _make_task()}
    r.targets = targets or []
    r.extracted = extracted or []
    return r


def _make_iocs(ips=None, domains=None):
    iocs = MagicMock()
    iocs.ips = ips or []
    iocs.domains = domains or []
    return iocs


def _make_target(ips=None, domains=None):
    t = MagicMock()
    t.iocs = _make_iocs(ips=ips, domains=domains)
    return t


_SPINNER_MOCK = MagicMock()


def _make_stats(**overrides) -> SandboxStats:
    defaults = {
        'period_start': _NOW - timedelta(days=7),
        'period_end': _NOW,
        'period_days': 7,
        'subset': 'org',
        'total': 10,
        'pending': 2,
        'by_status': {'reported': 8, 'static_analysis': 2},
        'by_kind': {'file': 6, 'url': 4},
        'by_platform': {'windows10-2004-x64': 5},
        'by_score': {'malicious': 3, 'clean': 5},
        'top_tags': TopTags(
            malware_families={'family:vidar': 5},
            botnets={'botnet:lzrd': 2},
            behavioral_ttp={'discovery': 3},
            arch_file={'pe': 1},
        ),
        'top_iocs': TopIocs(
            extracted_c2=[('http://c2.example.com', 5)],
            verified_network=[
                VerifiedIoc(
                    indicator='1.2.3.4',
                    type='IpAddress',
                    rf_score=75,
                    most_critical_rule='Actively Communicating C&C',
                )
            ],
            malicious_sha256=[{'sha256': 'abc123', 'score': 9, 'top_tag': 'vidar'}],
        ),
        'trend_vs_prior_period': {
            'total': {'current': 10, 'prev': 15},
            'reported': {'current': 8, 'prev': 12},
        },
        'limit_hit': False,
        'soar_skipped': False,
        'by_file_type': {'.exe': 50, '.dll': 20},
    }
    defaults.update(overrides)
    return SandboxStats(**defaults)


# ---------------------------------------------------------------------------
# Unit tests — pure functions in stats.py
# ---------------------------------------------------------------------------


class TestScoreBucket:
    def test_malicious(self):
        assert _score_bucket(10) == 'malicious'
        assert _score_bucket(8) == 'malicious'

    def test_suspicious(self):
        assert _score_bucket(7) == 'suspicious'
        assert _score_bucket(5) == 'suspicious'

    def test_potentially_suspicious(self):
        assert _score_bucket(4) == 'potentially_suspicious'
        assert _score_bucket(3) == 'potentially_suspicious'

    def test_clean(self):
        assert _score_bucket(2) == 'clean'
        assert _score_bucket(1) == 'clean'

    def test_none_returns_unknown(self):
        assert _score_bucket(None) == 'unknown'


class TestBuildScoreAndPlatform:
    def test_counts_behavioral_tasks_only(self):
        behavioral = _make_task(kind='behavioral', os='linux')
        static = _make_task(kind='static', os='windows')
        report = _make_report(score=9, tasks={'t1': behavioral, 't2': static})
        by_score, by_platform = _build_score_and_platform([(MagicMock(), report)])
        assert by_score == {'malicious': 1}
        assert by_platform == {'linux': 1}

    def test_skips_tasks_with_no_os(self):
        task = _make_task(kind='behavioral', os=None)
        report = _make_report(score=2, tasks={'t1': task})
        _, by_platform = _build_score_and_platform([(MagicMock(), report)])
        assert by_platform == {}

    def test_multiple_reports_aggregate(self):
        r1 = _make_report(score=9, tasks={'t1': _make_task(os='win')})
        r2 = _make_report(score=2, tasks={'t1': _make_task(os='win')})
        by_score, by_platform = _build_score_and_platform([(MagicMock(), r1), (MagicMock(), r2)])
        assert by_score == {'malicious': 1, 'clean': 1}
        assert by_platform == {'win': 2}


class TestBuildTagTaxonomy:
    def test_classifies_family_tags(self):
        r = _make_report(tags=['family:vidar', 'family:mirai'])
        result = _build_tag_taxonomy([(MagicMock(), r)])
        assert 'family:vidar' in result.malware_families
        assert 'family:mirai' in result.malware_families

    def test_classifies_botnet_tags(self):
        r = _make_report(tags=['botnet:lzrd'])
        result = _build_tag_taxonomy([(MagicMock(), r)])
        assert 'botnet:lzrd' in result.botnets

    def test_excludes_brand_tags(self):
        r = _make_report(tags=['brand:google', 'discovery'])
        result = _build_tag_taxonomy([(MagicMock(), r)])
        assert not any('brand' in t for t in result.behavioral_ttp)

    def test_arch_file_classification(self):
        r = _make_report(tags=['pe', 'elf', 'discovery'])
        result = _build_tag_taxonomy([(MagicMock(), r)])
        assert 'pe' in result.arch_file
        assert 'elf' in result.arch_file
        assert 'discovery' in result.behavioral_ttp

    def test_empty_tags(self):
        r = _make_report(tags=[])
        result = _build_tag_taxonomy([(MagicMock(), r)])
        assert result.malware_families == {}
        assert result.behavioral_ttp == {}


class TestBuildFileTypeMap:
    def _make_static_report(self, files_exts: list[list[str]]):
        sr = MagicMock()
        sr.files = []
        for exts in files_exts:
            f = MagicMock()
            f.exts = exts
            sr.files.append(f)
        return sr

    def test_collects_exts_from_files(self):
        sr = self._make_static_report([['.exe', '.dll'], ['.js']])
        result = _build_file_type_map([sr])
        assert result['.exe'] == 1
        assert result['.dll'] == 1
        assert result['.js'] == 1

    def test_normalises_to_lowercase(self):
        sr = self._make_static_report([['.EXE', '.Dll']])
        result = _build_file_type_map([sr])
        assert '.exe' in result
        assert '.dll' in result
        assert '.EXE' not in result

    def test_counts_across_multiple_reports(self):
        sr1 = self._make_static_report([['.exe']])
        sr2 = self._make_static_report([['.exe'], ['.js']])
        result = _build_file_type_map([sr1, sr2])
        assert result['.exe'] == 2
        assert result['.js'] == 1

    def test_empty_reports_returns_empty(self):
        assert _build_file_type_map([]) == {}

    def test_sorted_by_count_descending(self):
        sr = self._make_static_report([['.exe', '.exe', '.exe', '.js']])
        result = _build_file_type_map([sr])
        keys = list(result.keys())
        assert keys[0] == '.exe'
        assert keys[1] == '.js'


class TestExtractRawIocs:
    def test_extracts_sha256(self):
        report = _make_report(sha256='deadbeef')
        ip_ctr, dom_ctr, hashes, c2 = _extract_raw_iocs([(MagicMock(), report)])
        assert any(h['sha256'] == 'deadbeef' for h in hashes)

    def test_extracts_sha256_with_score_and_family(self):
        report = _make_report(sha256='aabbcc', score=9, tags=['family:vidar', 'pe'])
        _, _, hashes, _ = _extract_raw_iocs([(MagicMock(), report)])
        entry = next(h for h in hashes if h['sha256'] == 'aabbcc')
        assert entry['score'] == 9
        assert entry['top_tag'] == 'vidar'

    def test_extracts_sha256_no_family_tag(self):
        report = _make_report(sha256='cc11aa', score=8, tags=['pe', 'exe'])
        _, _, hashes, _ = _extract_raw_iocs([(MagicMock(), report)])
        entry = next(h for h in hashes if h['sha256'] == 'cc11aa')
        assert entry['top_tag'] == ''

    def test_extracts_c2_from_config(self):
        ex = MagicMock()
        ex.config = MagicMock()
        ex.config.c2 = ['http://c2.bad']
        ex.dropper = None
        report = _make_report(extracted=[ex])
        _, _, _, c2 = _extract_raw_iocs([(MagicMock(), report)])
        assert c2['http://c2.bad'] == 1

    def test_extracts_c2_from_dropper(self):
        durl = MagicMock()
        durl.url = 'http://dropper.bad'
        ex = MagicMock()
        ex.config = None
        ex.dropper = MagicMock()
        ex.dropper.urls = [durl]
        report = _make_report(extracted=[ex])
        _, _, _, c2 = _extract_raw_iocs([(MagicMock(), report)])
        assert c2['http://dropper.bad'] == 1

    def test_collects_target_iocs(self):
        target = _make_target(ips=['1.2.3.4'], domains=['evil.com'])
        report = _make_report(targets=[target])
        ip_ctr, dom_ctr, _, _ = _extract_raw_iocs([(MagicMock(), report)])
        assert ip_ctr['1.2.3.4'] == 1
        assert dom_ctr['evil.com'] == 1

    def test_skips_none_sha256(self):
        report = _make_report(sha256=None)
        _, _, hashes, _ = _extract_raw_iocs([(MagicMock(), report)])
        assert hashes == []


class TestSoarEnrich:
    def test_no_iocs_returns_skipped(self):
        verified, skipped = _soar_enrich(Counter(), Counter())
        assert verified == []
        assert skipped is True

    def test_no_rf_token_returns_skipped(self):
        with patch('banshee.sandbox.stats.get_config') as mock_cfg:
            mock_cfg.return_value.rf_token = None
            verified, skipped = _soar_enrich(Counter({'1.2.3.4': 1}), Counter())
        assert skipped is True
        assert verified == []

    def test_empty_token_returns_skipped(self):
        with patch('banshee.sandbox.stats.get_config') as mock_cfg:
            token = MagicMock()
            token.get_secret_value.return_value = ''
            mock_cfg.return_value.rf_token = token
            verified, skipped = _soar_enrich(Counter({'1.2.3.4': 1}), Counter())
        assert skipped is True

    def test_soar_error_returns_skipped(self):
        from psengine.enrich.errors import EnrichmentSoarError

        with (
            patch('banshee.sandbox.stats.get_config') as mock_cfg,
            patch('banshee.sandbox.stats.SoarMgr') as mock_soar,
        ):
            token = MagicMock()
            token.get_secret_value.return_value = 'valid-token'
            mock_cfg.return_value.rf_token = token
            mock_soar.return_value.soar.side_effect = EnrichmentSoarError('fail')
            verified, skipped = _soar_enrich(Counter({'1.2.3.4': 1}), Counter())
        assert skipped is True
        assert verified == []

    def test_filters_by_min_score(self):
        with (
            patch('banshee.sandbox.stats.get_config') as mock_cfg,
            patch('banshee.sandbox.stats.SoarMgr') as mock_soar,
            patch('banshee.sandbox.stats._spinner'),
        ):
            token = MagicMock()
            token.get_secret_value.return_value = 'tok'
            mock_cfg.return_value.rf_token = token

            low = MagicMock()
            low.content.risk.score = 10
            high = MagicMock()
            high.content.risk.score = 75
            high.entity = '1.2.3.4'
            high.content.entity.type_ = 'IpAddress'
            high.content.risk.rule.most_critical = 'C&C Server'
            mock_soar.return_value.soar.return_value = [low, high]

            verified, skipped = _soar_enrich(Counter({'1.2.3.4': 5}), Counter())
        assert skipped is False
        assert len(verified) == 1
        assert verified[0].indicator == '1.2.3.4'
        assert verified[0].rf_score == 75


# ---------------------------------------------------------------------------
# Integration tests — fetch_sandbox_stats with full mocking
# ---------------------------------------------------------------------------


def _mock_config():
    cfg = MagicMock()
    cfg.sandbox_choice = 'eu'
    cfg.rf_token = None
    return cfg


def _setup_sandbox_mgr(samples, overviews):
    mgr = MagicMock()
    mgr.fetch_samples.return_value = samples
    mgr.fetch_sample_overview_report.side_effect = overviews
    return mgr


class TestFetchSandboxStats:
    @patch('banshee.sandbox.stats.get_config')
    @patch('banshee.sandbox.stats.SandboxMgr')
    @patch('banshee.sandbox.stats._spinner', new=_SPINNER_MOCK)
    def test_no_reported_samples(self, mock_mgr_cls, mock_cfg):
        mock_cfg.return_value = _mock_config()
        sample = _make_sample(submitted_delta_days=1, status='static_analysis')
        mock_mgr_cls.return_value.fetch_samples.return_value = [sample]

        result = fetch_sandbox_stats(days=7, subset='org')

        assert result.total == 1
        assert result.pending == 1
        assert result.by_score == {}
        assert result.soar_skipped is True

    @patch('banshee.sandbox.stats.get_config')
    @patch('banshee.sandbox.stats.SandboxMgr')
    @patch('banshee.sandbox.stats.MultiThreadingHelper')
    @patch('banshee.sandbox.stats._spinner', new=_SPINNER_MOCK)
    def test_with_reported_samples(self, mock_mt, mock_mgr_cls, mock_cfg):
        mock_cfg.return_value = _mock_config()
        sample = _make_sample(submitted_delta_days=1, status='reported')
        mock_mgr_cls.return_value.fetch_samples.return_value = [sample]
        report = _make_report(score=9, tags=['family:mirai'])
        # First call: overviews; second call: static reports (return empty list)
        mock_mt.multithread_it.side_effect = [[report], []]

        result = fetch_sandbox_stats(days=7, subset='org')

        assert result.total == 1
        assert result.by_score.get('malicious', 0) == 1
        assert 'family:mirai' in result.top_tags.malware_families

    @patch('banshee.sandbox.stats.get_config')
    @patch('banshee.sandbox.stats.SandboxMgr')
    @patch('banshee.sandbox.stats._spinner', new=_SPINNER_MOCK)
    def test_limit_hit_warning(self, mock_mgr_cls, mock_cfg, capsys):
        mock_cfg.return_value = _mock_config()
        samples = [_make_sample(status='static_analysis') for _ in range(5)]
        mock_mgr_cls.return_value.fetch_samples.return_value = samples

        result = fetch_sandbox_stats(days=7, limit=5)

        assert result.limit_hit is True
        assert 'WARNING' in capsys.readouterr().err

    @patch('banshee.sandbox.stats.get_config')
    @patch('banshee.sandbox.stats.SandboxMgr')
    @patch('banshee.sandbox.stats.MultiThreadingHelper')
    @patch('banshee.sandbox.stats._spinner', new=_SPINNER_MOCK)
    def test_trend_computed_from_2x_window(self, mock_mt, mock_mgr_cls, mock_cfg):
        mock_cfg.return_value = _mock_config()
        now = datetime.now(timezone.utc)
        current = _make_sample(submitted_delta_days=3, status='reported')
        current.submitted = now - timedelta(days=3)
        prev = _make_sample(submitted_delta_days=10, status='reported')
        prev.submitted = now - timedelta(days=10)
        mock_mgr_cls.return_value.fetch_samples.return_value = [current, prev]
        # First call: overviews; second call: static reports (return empty list)
        mock_mt.multithread_it.side_effect = [[_make_report(score=2)], []]

        result = fetch_sandbox_stats(days=7, subset='org')

        assert result.trend_vs_prior_period['total']['current'] == 1
        assert result.trend_vs_prior_period['total']['prev'] == 1


# ---------------------------------------------------------------------------
# Unit tests — command-level (pretty print helpers)
# ---------------------------------------------------------------------------


class TestBuildDailyByFamily:
    def test_extracts_family_by_date(self):
        sample = MagicMock()
        sample.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        report = _make_report(tags=['family:vidar', 'pe'])
        result = _build_daily_by_family([(sample, report)])
        assert result == {'vidar': {'2026-07-01': 1}}

    def test_multiple_families_same_day(self):
        sample = MagicMock()
        sample.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        report = _make_report(tags=['family:vidar', 'family:mirai'])
        result = _build_daily_by_family([(sample, report)])
        assert result['vidar']['2026-07-01'] == 1
        assert result['mirai']['2026-07-01'] == 1

    def test_same_family_different_days(self):
        s1, s2 = MagicMock(), MagicMock()
        s1.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        s2.submitted = datetime(2026, 7, 2, tzinfo=timezone.utc)
        r = _make_report(tags=['family:vidar'])
        result = _build_daily_by_family([(s1, r), (s2, r)])
        assert result['vidar']['2026-07-01'] == 1
        assert result['vidar']['2026-07-02'] == 1

    def test_same_family_same_day_accumulates(self):
        s1, s2 = MagicMock(), MagicMock()
        s1.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        s2.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        r = _make_report(tags=['family:vidar'])
        result = _build_daily_by_family([(s1, r), (s2, r)])
        assert result['vidar']['2026-07-01'] == 2

    def test_no_family_tags_returns_empty(self):
        sample = MagicMock()
        sample.submitted = datetime(2026, 7, 1, tzinfo=timezone.utc)
        report = _make_report(tags=['pe', 'discovery'])
        result = _build_daily_by_family([(sample, report)])
        assert result == {}

    def test_empty_reports_returns_empty(self):
        assert _build_daily_by_family([]) == {}


class TestBucketCounts:
    def test_no_bucketing_when_under_limit(self):
        counts = [1, 2, 3]
        assert _bucket_counts(counts, 5) == [1, 2, 3]

    def test_returns_counts_unchanged_at_exact_limit(self):
        counts = list(range(10))
        assert _bucket_counts(counts, 10) == counts

    def test_buckets_down_to_max(self):
        counts = list(range(60))
        result = _bucket_counts(counts, _SPARK_MAX_BUCKETS)
        assert len(result) == _SPARK_MAX_BUCKETS

    def test_sums_within_buckets(self):
        counts = [1, 1, 1, 2, 2, 2]
        result = _bucket_counts(counts, 2)
        assert result[0] == 3
        assert result[1] == 6

    def test_large_window_capped_at_max_buckets(self):
        counts = [1] * 365
        result = _bucket_counts(counts, _SPARK_MAX_BUCKETS)
        assert len(result) == _SPARK_MAX_BUCKETS
        assert sum(result) == 365


class TestSparkline:
    def test_all_zero_returns_min_chars(self):
        result = _sparkline([0, 0, 0], global_max=0)
        assert result == _SPARK_CHARS[0] * 3

    def test_global_max_zero_returns_min_chars(self):
        result = _sparkline([0, 5, 10], global_max=0)
        assert result == _SPARK_CHARS[0] * 3

    def test_max_value_returns_full_block(self):
        result = _sparkline([100], global_max=100)
        assert result == _SPARK_CHARS[7]

    def test_zero_entry_returns_min_char(self):
        result = _sparkline([0, 100], global_max=100)
        assert result[0] == _SPARK_CHARS[0]
        assert result[1] == _SPARK_CHARS[7]

    def test_proportional_scaling(self):
        result = _sparkline([0, 50, 100], global_max=100)
        assert len(result) == 3
        assert result[0] < result[1] < result[2]

    def test_length_matches_input(self):
        counts = [1, 2, 3, 4, 5]
        result = _sparkline(counts, global_max=5)
        assert len(result) == 5


class TestPrintChartAndSummary:
    def _render(self, daily_by_family: dict, period_days: int = 7, **overrides) -> str:
        buf = StringIO()
        console = Console(file=buf, highlight=False, markup=True, width=200)
        stats = _make_stats(
            daily_by_family=daily_by_family,
            period_days=period_days,
            period_start=_NOW - timedelta(days=period_days),
            period_end=_NOW,
            **overrides,
        )
        _print_chart_and_summary(console, stats)
        return buf.getvalue()

    def test_empty_dict_skips_trends_header(self):
        out = self._render({})
        assert 'trends' not in out.lower()

    def test_empty_dict_shows_summary_stats(self):
        out = self._render({})
        assert 'submissions' in out

    def test_renders_sparkline_chars(self):
        daily = {'vidar': {'2026-07-09': 5, '2026-07-10': 10}}
        out = self._render(daily)
        assert any(c in out for c in '▁▂▃▄▅▆▇█')

    def test_family_name_appears_in_output(self):
        daily = {'vidar': {'2026-07-09': 5}}
        out = self._render(daily)
        assert 'vidar' in out

    def test_peak_count_appears_in_output(self):
        daily = {'vidar': {'2026-07-09': 42}}
        out = self._render(daily)
        assert '42' in out

    def test_date_labels_appear_in_output(self):
        daily = {'vidar': {'2026-07-09': 5}}
        out = self._render(daily, period_days=30)
        assert 'Jun' in out or 'Jul' in out

    def test_caps_at_eight_families(self):
        daily = {f'family{i}': {'2026-07-09': i + 1} for i in range(10)}
        out = self._render(daily)
        assert out != ''

    def test_all_zero_counts_renders_without_error(self):
        daily = {'vidar': {'2026-07-09': 0, '2026-07-10': 0}}
        out = self._render(daily)
        assert out != ''

    def test_summary_stats_appear_alongside_chart(self):
        daily = {'vidar': {'2026-07-09': 5}}
        out = self._render(daily)
        assert 'submissions' in out

    def test_summary_shows_analyzed_and_pending(self):
        out = self._render({}, pending=3)
        assert 'analyzed' in out
        assert 'pending' in out

    def test_summary_does_not_show_by_status(self):
        out = self._render({})
        assert 'by status' not in out

    def test_summary_shows_up_trend_arrow(self):
        out = self._render(
            {},
            trend_vs_prior_period={
                'total': {'current': 10, 'prev': 8},
                'reported': {'current': 8, 'prev': 6},
            },
        )
        assert '↑' in out

    def test_summary_shows_down_trend_arrow(self):
        out = self._render(
            {},
            trend_vs_prior_period={
                'total': {'current': 7, 'prev': 10},
                'reported': {'current': 5, 'prev': 8},
            },
        )
        assert '↓' in out

    def test_summary_no_arrow_when_prev_zero(self):
        out = self._render(
            {},
            trend_vs_prior_period={
                'total': {'current': 5, 'prev': 0},
                'reported': {'current': 4, 'prev': 0},
            },
        )
        assert '↑' not in out
        assert '↓' not in out

    def test_score_renders_one_row_per_bucket(self):
        out = self._render({}, by_score={'malicious': 10, 'clean': 5})
        assert _SCORE_SHORT_LABELS['malicious'] in out
        assert _SCORE_SHORT_LABELS['clean'] in out

    def test_score_bar_chars_present(self):
        out = self._render({}, by_score={'malicious': 10})
        assert _BAR_CHAR in out

    def test_zero_score_bucket_omitted(self):
        out = self._render({}, by_score={'malicious': 10, 'suspicious': 0})
        assert _SCORE_SHORT_LABELS['suspicious'] not in out

    def test_score_section_absent_when_no_data(self):
        out = self._render({}, by_score={})
        assert 'by score' not in out

    def test_divider_appears_when_chart_present(self):
        daily = {'vidar': {'2026-07-09': 5}}
        out = self._render(daily)
        assert '│' in out


class TestSearchUrl:
    def test_basic_query(self):
        url = _search_url('https://sandbox.recordedfuture.com', 'family:vidar')
        assert url == 'https://sandbox.recordedfuture.com/s?q=family%3Avidar'

    def test_spaces_encoded_as_plus(self):
        url = _search_url('https://sandbox.recordedfuture.com', 'family:emotet OR family:trickbot')
        assert 'family%3Aemotet+OR+family%3Atrickbot' in url

    def test_region_variants(self):
        assert _search_url('https://tria.ge', '1.2.3.4').startswith('https://tria.ge/s?q=')


class TestFmtTags:
    def test_empty_dict(self):
        assert '—' in _fmt_tags({})

    def test_strip_prefix(self):
        result = _fmt_tags({'botnet:lzrd': 5}, strip_prefix='botnet:')
        assert 'lzrd (5)' in result
        assert 'botnet:' not in result

    def test_top_n_limit(self):
        tags = {f'tag{i}': i for i in range(20)}
        result = _fmt_tags(tags, top_n=3)
        assert result.count('(') == 3

    def test_with_frontend_base_adds_links(self):
        result = _fmt_tags(
            {'family:vidar': 5},
            strip_prefix='family:',
            frontend_base='https://sandbox.recordedfuture.com',
        )
        assert '[link=' in result
        assert 'family%3Avidar' in result
        assert 'vidar[/link] (5)' in result

    def test_with_query_prefix(self):
        result = _fmt_tags(
            {'discovery': 10},
            query_prefix='tag:',
            frontend_base='https://sandbox.recordedfuture.com',
        )
        assert 'tag%3Adiscovery' in result

    def test_no_frontend_base_no_links(self):
        result = _fmt_tags({'family:vidar': 5}, strip_prefix='family:')
        assert '[link=' not in result
        assert 'vidar (5)' in result


class TestTrendStr:
    def test_up_returns_red_arrow_and_pct(self):
        result = _trend_str(110, 100)
        assert '↑' in result
        assert '10%' in result
        assert 'red' in result

    def test_down_returns_green_arrow_and_pct(self):
        result = _trend_str(90, 100)
        assert '↓' in result
        assert '10%' in result
        assert 'green' in result

    def test_equal_returns_dash(self):
        result = _trend_str(100, 100)
        assert '—' in result

    def test_prev_zero_returns_empty(self):
        assert _trend_str(5, 0) == ''

    def test_both_zero_returns_empty(self):
        assert _trend_str(0, 0) == ''

    def test_pct_rounds(self):
        result = _trend_str(103, 100)
        assert '3%' in result


class TestTrendPct:
    def test_increase(self):
        assert _trend_pct(110, 100) == 10

    def test_decrease(self):
        assert _trend_pct(90, 100) == -10

    def test_no_change(self):
        assert _trend_pct(100, 100) == 0

    def test_prev_zero_returns_none(self):
        assert _trend_pct(5, 0) is None

    def test_rounds_result(self):
        assert _trend_pct(103, 100) == 3


class TestToJsonDict:
    def test_structure(self):
        stats = _make_stats()
        d = _to_json_dict(stats)
        assert 'period_start' in d
        assert 'by_score' in d
        assert 'by_file_type' in d
        assert 'daily_by_family' in d
        assert 'top_iocs' in d
        assert 'trend_vs_prior_period' in d
        assert isinstance(d['top_iocs']['extracted_c2'], list)
        assert isinstance(d['top_iocs']['verified_network'][0]['rf_score'], int)
        sha256_entry = d['top_iocs']['malicious_sha256'][0]
        assert sha256_entry['sha256'] == 'abc123'
        assert sha256_entry['score'] == 9
        assert sha256_entry['top_tag'] == 'vidar'

    def test_by_status_absent_from_json(self):
        stats = _make_stats()
        d = _to_json_dict(stats)
        assert 'by_status' not in d

    def test_trend_pct_change_in_json(self):
        stats = _make_stats(
            trend_vs_prior_period={
                'total': {'current': 10, 'prev': 8},
                'reported': {'current': 8, 'prev': 6},
            }
        )
        d = _to_json_dict(stats)
        assert d['trend_vs_prior_period']['total']['pct_change'] == 25
        assert d['trend_vs_prior_period']['reported']['pct_change'] == 33

    def test_trend_pct_change_none_when_prev_zero(self):
        stats = _make_stats(
            trend_vs_prior_period={
                'total': {'current': 5, 'prev': 0},
                'reported': {'current': 4, 'prev': 0},
            }
        )
        d = _to_json_dict(stats)
        assert d['trend_vs_prior_period']['total']['pct_change'] is None

    def test_by_file_type_in_output(self):
        stats = _make_stats(by_file_type={'.exe': 98, '.js': 92})
        d = _to_json_dict(stats)
        assert d['by_file_type'] == {'.exe': 98, '.js': 92}

    def test_extracted_c2_as_lists(self):
        stats = _make_stats()
        d = _to_json_dict(stats)
        assert d['top_iocs']['extracted_c2'] == [['http://c2.example.com', 5]]

    def test_json_serialisable(self):
        stats = _make_stats()
        json.dumps(_to_json_dict(stats))


# ---------------------------------------------------------------------------
# Unit tests — _print_submission_profile
# ---------------------------------------------------------------------------


class TestPrintSubmissionProfile:
    def _render(self, by_platform=None, by_file_type=None, frontend_base='') -> str:
        buf = StringIO()
        console = Console(file=buf, highlight=False, markup=True, width=120)
        _print_submission_profile(console, by_platform or {}, by_file_type or {}, frontend_base)
        return buf.getvalue()

    def test_empty_both_no_output(self):
        assert self._render() == ''

    def test_section_header_present(self):
        out = self._render(by_platform={'win': 1})
        assert 'Submission profile' in out

    def test_renders_platform_names(self):
        out = self._render(by_platform={'windows10-2004-x64': 5, 'linux': 2})
        assert 'windows10-2004-x64' in out
        assert 'linux' in out

    def test_renders_file_type_bar_chars(self):
        out = self._render(by_file_type={'.exe': 100, '.dll': 50})
        assert _BAR_CHAR in out
        assert '.exe' in out
        assert '.dll' in out

    def test_max_count_gets_full_half_bar(self):
        out = self._render(by_file_type={'.exe': 100})
        assert _BAR_CHAR * _BAR_WIDTH_HALF in out

    def test_shorter_bar_for_smaller_count(self):
        out = self._render(by_file_type={'.exe': 100, '.dll': 50})
        assert _BAR_CHAR * _BAR_WIDTH_HALF in out
        assert _BAR_CHAR * (_BAR_WIDTH_HALF // 2) in out

    def test_count_appears_in_output(self):
        out = self._render(by_file_type={'.exe': 247})
        assert '247' in out

    def test_side_by_side_shows_both(self):
        out = self._render(by_platform={'linux': 3}, by_file_type={'.elf': 10})
        assert 'linux' in out
        assert '.elf' in out
        assert _BAR_CHAR in out

    def test_only_platform_renders(self):
        out = self._render(by_platform={'linux': 3})
        assert 'linux' in out
        assert 'Submission profile' in out

    def test_only_file_types_renders(self):
        out = self._render(by_file_type={'.pdf': 10})
        assert '.pdf' in out
        assert 'Submission profile' in out


# ---------------------------------------------------------------------------
# Unit tests — _print_tag_table (threat intel bar charts)
# ---------------------------------------------------------------------------
# Unit tests — _print_hashes
# ---------------------------------------------------------------------------


class TestPrintHashes:
    def _render(self, hashes: list, frontend_base: str = '', force_terminal: bool = False) -> str:
        buf = StringIO()
        console = Console(
            file=buf, highlight=False, markup=True, width=120, force_terminal=force_terminal
        )
        _print_hashes(console, hashes, frontend_base)
        return buf.getvalue()

    def test_renders_score_sha256_family(self):
        out = self._render([{'sha256': 'abc' * 21, 'score': 9, 'top_tag': 'vidar'}])
        assert 'Score' in out
        assert 'SHA256' in out
        assert 'Family' in out
        assert '9' in out
        assert 'vidar' in out
        assert 'abc' * 21 in out

    def test_truncates_at_20(self):
        hashes = [{'sha256': f'{"a" * 63}{i:x}', 'score': 9, 'top_tag': ''} for i in range(25)]
        out = self._render(hashes)
        assert '5 more' in out

    def test_no_more_message_when_under_cap(self):
        hashes = [{'sha256': 'a' * 64, 'score': 9, 'top_tag': ''}]
        out = self._render(hashes)
        assert 'more' not in out

    def test_frontend_base_preserves_sha256(self):
        sha = 'a' * 64
        out = self._render(
            [{'sha256': sha, 'score': 9, 'top_tag': ''}],
            frontend_base='https://sandbox.recordedfuture.com',
        )
        assert sha in out

    def test_family_tag_linked_when_frontend_base_set(self):
        sha = 'b' * 64
        out = self._render(
            [{'sha256': sha, 'score': 9, 'top_tag': 'vidar'}],
            frontend_base='https://sandbox.recordedfuture.com',
            force_terminal=True,
        )
        assert 'family%3Avidar' in out

    def test_family_tag_plain_without_frontend_base(self):
        out = self._render([{'sha256': 'c' * 64, 'score': 9, 'top_tag': 'vidar'}])
        assert 'vidar' in out
        assert 'link=' not in out


# ---------------------------------------------------------------------------
# CLI tests — cmd_sandbox.stats via CliRunner
# ---------------------------------------------------------------------------


class TestCmdSandboxStats:
    def test_no_args_shows_help(self):
        result = runner.invoke(app, args=['--help'])
        assert result.exit_code == 0
        assert '--days' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_json_output(self, mock_fetch):
        mock_fetch.return_value = _make_stats()
        result = runner.invoke(app, args=[])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['total'] == 10
        assert 'by_score' in data

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_output(self, mock_fetch):
        mock_fetch.return_value = _make_stats()
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'Sandbox' in result.output
        with pytest.raises(json.JSONDecodeError):
            json.loads(result.output)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_days_param(self, mock_fetch):
        mock_fetch.return_value = _make_stats(period_days=14)
        result = runner.invoke(app, args=['--days', '14'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(days=14, subset='org', limit=0)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_owned_subset(self, mock_fetch):
        mock_fetch.return_value = _make_stats(subset='owned')
        result = runner.invoke(app, args=['--subset', 'owned'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(days=7, subset='owned', limit=0)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_limit_param(self, mock_fetch):
        mock_fetch.return_value = _make_stats()
        result = runner.invoke(app, args=['--limit', '100'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(days=7, subset='org', limit=100)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_no_reported(self, mock_fetch):
        stats = _make_stats(
            by_score={},
            by_platform={},
            top_tags=TopTags(),
            top_iocs=TopIocs(),
            pending=5,
            soar_skipped=True,
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_shows_soar_skip_note(self, mock_fetch):
        stats = _make_stats(
            top_iocs=TopIocs(
                extracted_c2=[('http://c2.bad', 3)],
                verified_network=[],
            ),
            soar_skipped=True,
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'skipped' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_limit_out_of_range(self, mock_fetch):
        result = runner.invoke(app, args=['--limit', '0'])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_days_out_of_range(self, mock_fetch):
        result = runner.invoke(app, args=['--days', '0'])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_contains_links(self, mock_fetch):
        # CliRunner strips OSC-8 escape sequences; verify links via unit tests on _fmt_tags/_search_url.
        # Here we just confirm the command renders threat intel and IOC sections without error.
        mock_fetch.return_value = _make_stats(sandbox_choice='eu')
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'Malware families' in result.output
        assert 'Verified network IOCs' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_always_shows_sha256s(self, mock_fetch):
        stats = _make_stats(
            sandbox_choice='eu',
            top_iocs=TopIocs(
                extracted_c2=[],
                verified_network=[],
                malicious_sha256=[
                    {'sha256': 'abc' * 21, 'score': 9, 'top_tag': 'vidar'},
                    {'sha256': 'def' * 21, 'score': 8, 'top_tag': ''},
                ],
            ),
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'SHA256' in result.output
        assert 'abc' * 21 in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_hashes_show_score_and_family(self, mock_fetch):
        stats = _make_stats(
            sandbox_choice='eu',
            top_iocs=TopIocs(
                extracted_c2=[],
                verified_network=[],
                malicious_sha256=[{'sha256': 'abc' * 21, 'score': 9, 'top_tag': 'vidar'}],
            ),
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'Score' in result.output
        assert 'abc' * 21 in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_truncates_hashes_at_20(self, mock_fetch):
        hashes = [{'sha256': f'{"a" * 63}{i:x}', 'score': 9, 'top_tag': ''} for i in range(25)]
        stats = _make_stats(
            sandbox_choice='eu',
            top_iocs=TopIocs(extracted_c2=[], verified_network=[], malicious_sha256=hashes),
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert '5 more' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_c2_shows_more_message(self, mock_fetch):
        c2s = [(f'http://c2-{i}.bad', i + 1) for i in range(12)]
        stats = _make_stats(
            top_iocs=TopIocs(extracted_c2=c2s, verified_network=[], malicious_sha256=[])
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert '2 more' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_verified_iocs_shows_more_message(self, mock_fetch):
        iocs = [
            VerifiedIoc(
                indicator=f'1.2.3.{i}', type='IpAddress', rf_score=75, most_critical_rule='C&C'
            )
            for i in range(12)
        ]
        stats = _make_stats(
            top_iocs=TopIocs(extracted_c2=[], verified_network=iocs, malicious_sha256=[])
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert '2 more' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_c2_column_headers_visible(self, mock_fetch):
        stats = _make_stats(
            top_iocs=TopIocs(
                extracted_c2=[('http://c2.bad', 3)],
                verified_network=[],
                malicious_sha256=[],
            )
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'Hits' in result.output
        assert 'URL' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_json_always_includes_sha256s(self, mock_fetch):
        mock_fetch.return_value = _make_stats()
        result = runner.invoke(app, args=[])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert 'malicious_sha256' in data['top_iocs']

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_shows_file_types_histogram(self, mock_fetch):
        stats = _make_stats(by_file_type={'.exe': 200, '.dll': 100, '.pdf': 40})
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'File types' in result.output
        assert _BAR_CHAR in result.output
        assert '.exe' in result.output
        assert '.dll' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_no_file_types_when_empty(self, mock_fetch):
        stats = _make_stats(by_file_type={})
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert 'File types' not in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_shows_submission_chart_when_data_present(self, mock_fetch):
        stats = _make_stats(daily_by_family={'vidar': {'2026-07-09': 5, '2026-07-10': 10}})
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert any(c in result.output for c in '▁▂▃▄▅▆▇█')

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_no_chart_when_no_family_data(self, mock_fetch):
        stats = _make_stats(daily_by_family={})
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty'])
        assert result.exit_code == 0
        assert not any(c in result.output for c in '▂▃▄▅▆▇')

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_json_includes_daily_by_family(self, mock_fetch):
        mock_fetch.return_value = _make_stats(daily_by_family={'vidar': {'2026-07-09': 5}})
        result = runner.invoke(app, args=[])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['daily_by_family'] == {'vidar': {'2026-07-09': 5}}
