import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_sandbox import app
from banshee.sandbox.output import (
    _fmt_tags,
    _search_url,
    _to_json_dict,
    _trend_str,
)
from banshee.sandbox.stats import (
    SandboxStats,
    TopIocs,
    TopTags,
    VerifiedIoc,
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
            malicious_sha256=['abc123'],
        ),
        'trend_vs_prior_period': {
            'total': {'current': 10, 'prev': 15},
            'reported': {'current': 8, 'prev': 12},
        },
        'limit_hit': False,
        'soar_skipped': False,
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


class TestExtractRawIocs:
    def test_extracts_sha256(self):
        report = _make_report(sha256='deadbeef')
        ip_ctr, dom_ctr, hashes, c2 = _extract_raw_iocs([(MagicMock(), report)])
        assert 'deadbeef' in hashes

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
        assert hashes == set()


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
        mock_mt.multithread_it.return_value = [report]

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
        mock_mt.multithread_it.return_value = [_make_report(score=2)]

        result = fetch_sandbox_stats(days=7, subset='org')

        assert result.trend_vs_prior_period['total']['current'] == 1
        assert result.trend_vs_prior_period['total']['prev'] == 1


# ---------------------------------------------------------------------------
# Unit tests — command-level (pretty print helpers)
# ---------------------------------------------------------------------------


class TestTrendStr:
    def test_no_prior_data(self):
        assert 'no prior data' in _trend_str(10, 0)

    def test_increase(self):
        result = _trend_str(110, 100)
        assert '110' in result
        assert '▲' in result
        assert '+10%' in result

    def test_decrease(self):
        result = _trend_str(90, 100)
        assert '90' in result
        assert '▼' in result
        assert '-10%' in result


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


class TestToJsonDict:
    def test_structure(self):
        stats = _make_stats()
        d = _to_json_dict(stats)
        assert 'period_start' in d
        assert 'by_score' in d
        assert 'top_iocs' in d
        assert 'trend_vs_prior_period' in d
        assert isinstance(d['top_iocs']['extracted_c2'], list)
        assert isinstance(d['top_iocs']['verified_network'][0]['rf_score'], int)

    def test_extracted_c2_as_lists(self):
        stats = _make_stats()
        d = _to_json_dict(stats)
        assert d['top_iocs']['extracted_c2'] == [['http://c2.example.com', 5]]

    def test_json_serialisable(self):
        stats = _make_stats()
        json.dumps(_to_json_dict(stats))


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
    def test_stats_pretty_hashes_flag_shows_sha256s(self, mock_fetch):
        stats = _make_stats(
            sandbox_choice='eu',
            top_iocs=TopIocs(
                extracted_c2=[],
                verified_network=[],
                malicious_sha256=['abc' * 21, 'def' * 21],
            ),
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty', '--hashes'])
        assert result.exit_code == 0
        assert 'SHA256' in result.output
        assert 'abc' * 21 in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_pretty_hashes_flag_truncates_at_20(self, mock_fetch):
        hashes = [f'{"a" * 63}{i:x}' for i in range(25)]
        stats = _make_stats(
            sandbox_choice='eu',
            top_iocs=TopIocs(extracted_c2=[], verified_network=[], malicious_sha256=hashes),
        )
        mock_fetch.return_value = stats
        result = runner.invoke(app, args=['--pretty', '--hashes'])
        assert result.exit_code == 0
        assert '5 more' in result.output

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_stats')
    def test_stats_hashes_flag_ignored_without_pretty(self, mock_fetch):
        mock_fetch.return_value = _make_stats()
        result = runner.invoke(app, args=['--hashes'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert 'malicious_sha256' in data['top_iocs']
