import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_risklist import app
from banshee.fusion_files.feed_stat import (
    _bar,
    _compute_stats,
    _summary_line,
)

from .conftest import strip_ansi

runner = CliRunner()

COMMAND = 'stat'


###############################################################################
# Pure helpers
###############################################################################


def test_bar_zero_count_returns_empty():
    assert _bar(0, 100) == ''


def test_bar_max_count_maps_to_full_width():
    assert _bar(100, 100, width=24) == '█' * 24


def test_bar_below_one_char_returns_fractional_or_empty():
    # 1/100 * 24 = 0.24 -> 0 full, remainder * 8 = 1.92 -> idx 0 -> '▏'
    assert _bar(1, 100, width=24) == '▏'
    # rounds to zero full and no fractional block
    assert _bar(1, 100000, width=24) == ''


def test_compute_stats_weighted_percentiles_do_not_expand_array():
    counts = {68: 26676, 69: 33891, 70: 12430, 90: 27003}
    stats = _compute_stats(counts)
    assert stats['total'] == 100000
    assert stats['mode'] == 69
    # median: cum reaches 60567 at score 69 (>= ceil(50000))
    assert stats['median'] == 69
    assert stats['p95'] == 90
    assert stats['p99'] == 90


def test_compute_stats_empty_returns_empty_dict():
    assert _compute_stats({}) == {}


def test_compute_stats_single_row():
    stats = _compute_stats({85: 3})
    assert stats == {
        'total': 3,
        'mean': '85.0',
        'median': 85,
        'mode': 85,
        'p95': 85,
        'p99': 85,
    }


def test_summary_line_empty_is_empty_string():
    assert _summary_line({}) == ''


def test_summary_line_uses_thousands_separator():
    line = _summary_line({50: 1234, 60: 5678})
    assert line.startswith('6,912 entries')


def _fake_fusion_response(content: bytes, exists: bool = True):
    resp = MagicMock()
    resp.exists = exists
    resp.content = content
    return resp


@pytest.mark.vcr
def test_risklist_stat():
    result = runner.invoke(app, args=[COMMAND, '--list-name', 'cncSite', '--entity-type', 'domain'])
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert output == {
        'etag': '06c8465e3d34b4ad96da6febde8af8c5',
        'exists': True,
        'name': 'cncSite_domain_risklist',
    }


@pytest.mark.vcr
def test_risklist_stat_pretty():
    result = runner.invoke(
        app, args=[COMMAND, '--list-name', 'cncSite', '--entity-type', 'domain', '--pretty']
    )
    assert result.exit_code == 0
    assert (
        result.output
        == '  Name  cncSite_domain_risklist\n  ETag  06c8465e3d34b4ad96da6febde8af8c5\n'
    )


@patch('banshee.risklist.risklist_stat.RFClient')
def test_risklist_stat_name_matches_list_name(mock_client):
    """When --list-name already ends with _risklist, the name should not be double-suffixed."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'etag': '"abc123"'}
    mock_client.return_value.request.return_value = mock_response

    result = runner.invoke(
        app, args=[COMMAND, '--list-name', 'domain_risklist', '--entity-type', 'domain']
    )
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output['name'] == 'domain_risklist'


@pytest.mark.vcr
def test_risklist_stat_fusion():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/c2_communicating_ips_list.csv']
    )
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert output == {
        'etag': 'c1b3f0d7220a21fdada5c27d8070255f1dde8f4dbb69c07ee83470ccfafd6907',
        'exists': True,
        'last-modified': 'Thu, 12 Feb 2026 17:15:01 GMT',
        'path': '/public/prevent/c2_communicating_ips_list.csv',
    }


@pytest.mark.vcr
def test_risklist_stat_fusion_pretty():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/public/prevent/c2_communicating_ips_list.csv',
            '--pretty',
        ],
        env={'COLUMNS': '200'},
    )
    assert result.exit_code == 0
    assert strip_ansi(result.output).split()[:-1] == [
        'Path',
        '/public/prevent/c2_communicating_ips_list.csv',
        'Last',
        'Modified',
        'Feb',
        '12',
        '17:15:01',
        'UTC',
        'ETag',
    ]
    assert 'c1b3f0d7220a21fdada5c27d8070255f1dde8f4dbb69c07ee83470ccfafd6907' in strip_ansi(
        result.output
    ).strip('\n')


@pytest.mark.vcr
def test_risklist_stat_fusion_not_found():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/bad-list4040404.csv']
    )
    assert result.exit_code == 1

    output = json.loads(result.output)

    assert output == {'path': '/public/prevent/bad-list4040404.csv', 'exists': False}


@pytest.mark.vcr
def test_risklist_stat_fusion_not_found_pretty():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/bad-list4040404.csv', '--pretty']
    )
    assert result.exit_code == 1
    assert result.output == 'File not found /public/prevent/bad-list4040404.csv\n'


###############################################################################
# --count / -C
###############################################################################


def _mock_rfclient(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'etag': '"abc123"'}
    mock_client.return_value.request.return_value = mock_response


@patch('banshee.risklist.risklist_stat.RFClient')
@patch('banshee.risklist.risklist_stat.RisklistMgr')
def test_risklist_stat_count_api_json(mock_mgr, mock_client):
    _mock_rfclient(mock_client)
    mock_mgr.return_value.fetch_risklist.return_value = iter(
        [
            ['Name', 'Risk', 'RiskString', 'EvidenceDetails'],
            ['1.1.1.1', '85', '3/8', '[]'],
            ['2.2.2.2', '85', '3/8', '[]'],
            ['3.3.3.3', '65', '2/8', '[]'],
        ]
    )

    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--list-name', 'default', '--count'],
    )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output['name'] == 'default_ip_risklist'
    assert output['exists'] is True
    assert output['etag'] == 'abc123'
    assert output['counts'] == {'65': 1, '85': 2}


@patch('banshee.risklist.risklist_stat.RFClient')
@patch('banshee.risklist.risklist_stat.RisklistMgr')
def test_risklist_stat_count_api_pretty(mock_mgr, mock_client):
    _mock_rfclient(mock_client)
    mock_mgr.return_value.fetch_risklist.return_value = iter(
        [
            ['Name', 'Risk', 'RiskString', 'EvidenceDetails'],
            ['1.1.1.1', '85', '3/8', '[]'],
            ['2.2.2.2', '85', '3/8', '[]'],
            ['3.3.3.3', '65', '2/8', '[]'],
        ]
    )

    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--list-name', 'default', '--count', '--pretty'],
        env={'COLUMNS': '200'},
    )

    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert 'default_ip_risklist' in output
    assert 'abc123' in output
    # summary line: 3 rows total, computed stats
    assert '3 entries · mean 78.3 · median 85 · mode 85 · p95 85 · p99 85' in output
    # table headers, thousands-separator formatting and percentages
    assert 'Score' in output and 'Count' in output and 'Pct' in output
    assert 'Cum%' not in output
    assert '65' in output and '85' in output
    assert '33.33 %' in output and '66.67 %' in output
    # inline bar for the largest row
    assert '█' in output


def _fake_head_response():
    resp = MagicMock()
    resp.exists = True
    resp.last_modified = 'Thu, 12 Feb 2026 17:15:01 GMT'
    resp.etag = 'abc123'
    resp.json.return_value = {
        'exists': True,
        'etag': 'abc123',
        'last-modified': 'Thu, 12 Feb 2026 17:15:01 GMT',
        'path': '/some/list.csv',
    }
    return resp


@patch('banshee.fusion_files.feed_stat.FusionMgr')
@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom_json(mock_count_mgr, mock_stat_mgr):
    csv_bytes = (
        b'Name,Risk,RiskString,EvidenceDetails\n'
        b'1.1.1.1,85,3/8,[]\n'
        b'2.2.2.2,85,3/8,[]\n'
        b'3.3.3.3,65,2/8,[]\n'
    )
    mock_count_mgr.return_value.get_files.return_value = [_fake_fusion_response(csv_bytes)]
    mock_stat_mgr.return_value.head_files.return_value = [_fake_head_response()]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/some/list.csv', '-C'],
    )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output['path'] == '/some/list.csv'
    assert output['counts'] == {'65': 1, '85': 2}


@patch('banshee.fusion_files.feed_stat.FusionMgr')
@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom_pretty(mock_count_mgr, mock_stat_mgr):
    csv_bytes = (
        b'Name,Risk,RiskString,EvidenceDetails\n'
        b'1.1.1.1,85,3/8,[]\n'
        b'2.2.2.2,85,3/8,[]\n'
        b'3.3.3.3,65,2/8,[]\n'
    )
    mock_count_mgr.return_value.get_files.return_value = [_fake_fusion_response(csv_bytes)]
    mock_stat_mgr.return_value.head_files.return_value = [_fake_head_response()]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/some/list.csv', '-C', '--pretty'],
        env={'COLUMNS': '200'},
    )

    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert '/some/list.csv' in output
    assert '65' in output
    assert '85' in output
    assert 'Total' in output


@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom_missing_risk_column(mock_mgr):
    csv_bytes = b'Name,Score,EvidenceDetails\n1.1.1.1,85,[]\n'
    mock_mgr.return_value.get_files.return_value = [_fake_fusion_response(csv_bytes)]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/some/list.csv', '--count'],
    )

    assert result.exit_code == 1
    assert "Risk list has no 'Risk' column" in result.output


@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom_empty_file(mock_mgr):
    mock_mgr.return_value.get_files.return_value = [_fake_fusion_response(b'')]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/some/list.csv', '--count'],
    )

    assert result.exit_code == 1
    assert 'Risk list is empty' in result.output


@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom_not_found(mock_mgr):
    mock_mgr.return_value.get_files.return_value = [_fake_fusion_response(b'', exists=False)]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/missing/list.csv', '--count'],
    )

    assert result.exit_code == 1
    assert "'/missing/list.csv' not found" in result.output
