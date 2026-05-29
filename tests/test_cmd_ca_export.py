import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_classic_alerts import app

runner = CliRunner()

COMMAND = 'export'

ALERTS = json.dumps([{'id': '1b6uQY'}, {'id': 'xr8cqL'}, {'id': '1ct-k8'}])
EMPTY_JSON = json.dumps([])
INVALID_JSON = json.dumps([{'name': 'kevin'}])
INVALID_ALERT_ID = json.dumps([{'id': 'bad-alert-id'}])


def test_ca_export_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_ca_export_id_non_piped():
    result = runner.invoke(app, args=[COMMAND, '1b6uQY'])
    assert result.exit_code == 2


def test_ca_export_blank_pipe():
    result = runner.invoke(app, args=[COMMAND], input='')
    assert result.exit_code == 2


def test_ca_export_invalid_json():
    result = runner.invoke(app, args=[COMMAND], input=INVALID_JSON)
    assert result.exit_code == 2


def test_ca_export_invalid_id():
    result = runner.invoke(app, args=[COMMAND], input=INVALID_ALERT_ID)
    assert result.exit_code == 1


def test_ca_export_no_alerts():
    result = runner.invoke(app, args=COMMAND, input=EMPTY_JSON)
    assert result.exit_code == 0

    assert len(json.loads(result.output.strip('\n'))) == 0


@pytest.mark.vcr
def test_ca_export_json():
    result = runner.invoke(app, args=[COMMAND], input=ALERTS)
    assert result.exit_code == 0

    alerts = json.loads(result.output.strip('\n'))
    assert len(alerts) == 3
    for alert in alerts:
        assert alert['id'] in ['1b6uQY', 'xr8cqL', '1ct-k8']


@pytest.mark.vcr(record_mode='new_episodes')
def test_ca_export_csv():
    result = runner.invoke(app, args=[COMMAND, '--csv'], input=ALERTS)
    assert result.exit_code == 0

    result_csv = result.output.strip().split('\n')
    assert len(result_csv) == 4
    assert (
        result_csv[0]
        == 'ID,Priority,Alert Rule,Status,Created,Updated,Title,Assignee,URL,Entities,Recorded Future AI Insights'
    )
    assert len(result_csv[1].split(',')) == 11
