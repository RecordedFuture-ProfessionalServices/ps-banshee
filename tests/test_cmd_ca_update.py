import pytest
from psengine.classic_alerts.errors import AlertUpdateError
from typer.testing import CliRunner

from banshee.commands.cmd_classic_alerts import app

runner = CliRunner()

COMMAND = 'update'


def test_ca_update_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_ca_update_bad_id():
    result = runner.invoke(app, args=[COMMAND, 'bad-alert-id', '-s', 'Pending'])
    assert result.exit_code == 1
    assert isinstance(result.exception, AlertUpdateError)


def test_ca_update_invalid_id():
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
@pytest.mark.parametrize(('alert_id'), ['1b6uQY', 'xr8cqL', '1ct-k8'])
def test_ca_update_one_alert(alert_id):
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            alert_id,
            '-s',
            'Pending',
            '-n',
            'Test note',
            '-A',
            '-a',
            'ernest.bartosevic+psdevm@recordedfuture.com',
        ],
    )
    assert result.exit_code == 0

    assert 'SUCCESS' in result.output
    assert alert_id in result.output


@pytest.mark.vcr
def test_ca_update_multiple_alerts():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '1b6uQY',
            'xr8cqL',
            '1ct-k8',
            '-s',
            'Pending',
            '-n',
            'Test note',
            '-A',
            '-a',
            'ernest.bartosevic+psdevm@recordedfuture.com',
        ],
    )
    assert result.exit_code == 0

    assert 'SUCCESS' in result.output
    assert '1b6uQY' in result.output
    assert 'xr8cqL' in result.output
    assert '1ct-k8' in result.output


@pytest.mark.vcr
def test_ca_update_error():
    result = runner.invoke(app, args=[COMMAND, '123456', '-s', 'Pending'])
    assert result.exit_code == 1
