import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_risklist import app

from .conftest import strip_ansi

runner = CliRunner()

COMMAND = 'stat'


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
        == '  Name:    cncSite_domain_risklist           \n  ETag:    06c8465e3d34b4ad96da6febde8af8c5  \n'  # noqa: E501
    )


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
        'Path:',
        '/public/prevent/c2_communicating_ips_list.csv',
        'Last',
        'Modified:',
        'Feb',
        '12',
        '17:15:01',
        'UTC',
        'ETag:',
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


@patch('banshee.risklist.risklist_stat.RisklistMgr')
def test_risklist_stat_count_api(mock_mgr):
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
        env={'COLUMNS': '200'},
    )

    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert 'default_ip_risklist' in output
    assert '65' in output and '85' in output
    assert 'Total' in output
    assert '3' in output  # total count


@patch('banshee.risklist.risklist_stat.FusionMgr')
def test_risklist_stat_count_custom(mock_mgr):
    csv_bytes = (
        b'Name,Risk,RiskString,EvidenceDetails\n'
        b'1.1.1.1,85,3/8,[]\n'
        b'2.2.2.2,85,3/8,[]\n'
        b'3.3.3.3,65,2/8,[]\n'
    )
    mock_mgr.return_value.get_files.return_value = [_fake_fusion_response(csv_bytes)]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/some/list.csv', '-C'],
        env={'COLUMNS': '200'},
    )

    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert '/some/list.csv' in output
    assert '65' in output and '85' in output
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
    mock_mgr.return_value.get_files.return_value = [
        _fake_fusion_response(b'', exists=False)
    ]

    result = runner.invoke(
        app,
        args=[COMMAND, '--custom-list-path', '/missing/list.csv', '--count'],
    )

    assert result.exit_code == 1
    assert "'/missing/list.csv' not found" in result.output
