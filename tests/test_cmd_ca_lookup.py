import json

import pytest
from psengine.classic_alerts.errors import AlertFetchError
from typer.testing import CliRunner

from banshee.commands.cmd_classic_alerts import app

runner = CliRunner()

COMMAND = 'lookup'


def test_ca_lookup_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_ca_lookup_bad_id():
    result = runner.invoke(app, args=[COMMAND, 'bad-alert-id'])
    assert result.exit_code == 1
    assert isinstance(result.exception, AlertFetchError)


def test_ca_lookup_invalid_id():
    result = runner.invoke(app, args=[COMMAND, '1234'])
    assert result.exit_code == 2

    expected_output_as_list = [
        '1234',
        'Alert',
        'ID',
        'should',
        'be',
        'at',
        'least',
        '6',
        'characters',
        'long',
    ]
    assert all(word in result.output for word in expected_output_as_list)


@pytest.mark.vcr
def test_ca_lookup_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'xr8cqL', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
@pytest.mark.parametrize(('alert_id'), ['1b6uQY', 'xr8cqL', '1ct-k8'])
def test_ca_lookup_json_response(alert_id):
    result = runner.invoke(app, args=[COMMAND, alert_id])
    assert result.exit_code == 0

    json.loads(result.output)
