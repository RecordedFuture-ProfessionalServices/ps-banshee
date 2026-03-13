import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_risklist import app

from .conftest import strip_ansi

runner = CliRunner()

COMMAND = 'create'

FAKE_CSV_ROW = {'Name': '1.2.3.4', 'Risk': '85', 'RiskString': '3/8', 'EvidenceDetails': '[]'}


def _fake_entry():
    entry = MagicMock()
    entry.ioc = '1.2.3.4'
    entry.risk_score = 85
    entry.json.return_value = {'Name': '1.2.3.4', 'Risk': 85}
    return entry


def _fake_fetch(_rule, _entity_type, validate=None, **_kwargs):
    if validate is not None:
        return [_fake_entry()]
    return [FAKE_CSV_ROW]


def test_risklist_create_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_risklist_create_missing_entity_type():
    result = runner.invoke(
        app,
        args=[COMMAND, '--risk-rule', 'default'],
    )
    assert result.exit_code == 2
    assert '--entity-type is required' in strip_ansi(result.output)


def test_risklist_create_missing_risk_rule():
    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip'],
    )
    assert result.exit_code == 2
    assert 'At least one --risk-rule is required' in strip_ansi(result.output)


def test_risklist_create_fusion_without_output_path():
    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default', '--fusion'],
    )
    assert result.exit_code == 2
    assert '--output-path is required when using --fusion' in strip_ansi(result.output)


def test_risklist_create_risk_score_out_of_range():
    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default', '--risk-score', '100'],
    )
    assert result.exit_code == 2


def test_risklist_create_invalid_format():
    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default', '--format', 'xml'],
    )
    assert result.exit_code == 2


@patch('banshee.risklist.risklist_create.RisklistMgr')
def test_risklist_create_default_output_path(mock_mgr, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_mgr.return_value.fetch_risklist.side_effect = _fake_fetch

    result = runner.invoke(app, args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default'])

    out_file = tmp_path / 'custom_risklist_ip.csv'
    assert result.exit_code == 0
    assert out_file.exists()
    assert str(out_file) in strip_ansi(result.output)


@patch('banshee.risklist.risklist_create.RisklistMgr')
def test_risklist_create_output_path_dir(mock_mgr, tmp_path):
    mock_mgr.return_value.fetch_risklist.side_effect = _fake_fetch

    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'domain', '--risk-rule', 'default', '-o', str(tmp_path)],
    )

    out_file = tmp_path / 'custom_risklist_domain.csv'
    assert result.exit_code == 0
    assert out_file.exists()
    assert str(out_file) in strip_ansi(result.output)


@patch('banshee.risklist.risklist_create.RisklistMgr')
def test_risklist_create_output_path_explicit_file(mock_mgr, tmp_path):
    mock_mgr.return_value.fetch_risklist.side_effect = _fake_fetch
    out_file = tmp_path / 'my_risklist.csv'

    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default', '-o', str(out_file)],
    )

    assert result.exit_code == 0
    assert out_file.exists()
    assert str(out_file) in strip_ansi(result.output)


@pytest.mark.parametrize(
    ('format_', 'expected_ext'),
    [
        ('csv', '.csv'),
        ('json', '.json'),
        ('edl', '.txt'),
    ],
)
@patch('banshee.risklist.risklist_create.RisklistMgr')
def test_risklist_create_output_extension(mock_mgr, tmp_path, monkeypatch, format_, expected_ext):
    monkeypatch.chdir(tmp_path)
    mock_mgr.return_value.fetch_risklist.side_effect = _fake_fetch

    result = runner.invoke(
        app,
        args=[COMMAND, '--entity-type', 'ip', '--risk-rule', 'default', '-f', format_],
    )

    out_file = tmp_path / f'custom_risklist_ip{expected_ext}'
    assert result.exit_code == 0
    assert out_file.exists()


@patch('banshee.risklist.risklist_create.FusionMgr')
@patch('banshee.risklist.risklist_create.RisklistMgr')
def test_risklist_create_fusion_upload(mock_mgr, mock_fusion):
    mock_mgr.return_value.fetch_risklist.side_effect = _fake_fetch
    mock_fusion.return_value.post_file.return_value = MagicMock()

    fusion_path = '/home/risklists/ip_list.csv'
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--entity-type',
            'ip',
            '--risk-rule',
            'default',
            '--fusion',
            '-o',
            fusion_path,
        ],
    )

    assert result.exit_code == 0
    mock_fusion.return_value.post_file.assert_called_once()
    _, called_fusion_path = mock_fusion.return_value.post_file.call_args[0]
    assert called_fusion_path == fusion_path
    assert 'Risklist uploaded to Fusion' in strip_ansi(result.output)


@pytest.mark.parametrize(
    ('entity_type', 'risk_rules', 'format_', 'ext', 'risk_score'),
    [
        ('ip', ['recentActiveCnc', 'recentAnalystNote'], 'csv', '.csv', None),
        ('ip', ['recentActiveCnc', 'recentAnalystNote'], 'json', '.json', 80),
        ('ip', ['recentActiveCnc', 'recentAnalystNote'], 'edl', '.txt', None),
        ('domain', ['recentCncSite', 'recentAnalystNote'], 'csv', '.csv', 25),
        ('hash', ['observedTelemetry'], 'csv', '.csv', None),
        ('url', ['recentBotnetUrl', 'recentRelatedNote'], 'csv', '.csv', 5),
    ],
)
def test_risklist_create_multiple_rules(
    tmp_path, monkeypatch, entity_type, risk_rules, format_, ext, risk_score
):
    monkeypatch.chdir(tmp_path)

    args = [COMMAND, '--entity-type', entity_type, '-f', format_]
    for rule in risk_rules:
        args += ['-R', rule]
    if risk_score is not None:
        args += ['-r', str(risk_score)]

    result = runner.invoke(app, args=args)

    out_file = tmp_path / f'custom_risklist_{entity_type}{ext}'
    assert result.exit_code == 0
    assert out_file.exists()
    assert out_file.stat().st_size > 0
    assert str(out_file) in strip_ansi(result.output)

    content = out_file.read_text().strip()

    if format_ == 'csv':
        lines = content.splitlines()
        if entity_type == 'hash':
            assert lines[0].split(',') == [
                'Name',
                'Algorithm',
                'Risk',
                'RiskString',
                'EvidenceDetails',
            ]
        else:
            assert lines[0].split(',') == ['Name', 'Risk', 'RiskString', 'EvidenceDetails']
        assert len(lines) > 1

    elif format_ == 'json':
        json.loads(content)

    elif format_ == 'edl':
        lines = content.splitlines()
        assert all(line and ',' not in line for line in lines)
