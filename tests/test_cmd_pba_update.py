import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_playbook_alerts import app

runner = CliRunner()

COMMAND = 'update'


def test_pba_update_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_pba_bad_update_args():
    result = runner.invoke(app, args=[COMMAND, 'bad_alert_id'])
    assert result.exit_code == 2
    # due to terminal truncation the output is not always printed the same
    # so we need to check it for each word :shrug:
    expected_output_as_list = [
        "'bad_alert_id'",
        'Alert',
        'ID',
        'should',
        'be',
        '36',
        'characters',
        'long',
        'or',
        '41',
        'characters',
        'with',
        "'task:'",
        'prefix',
    ]
    assert all(word in result.output for word in expected_output_as_list)


test_input = [
    '99a83597-3c3f-49c0-af56-c06a636532e8',
    'db6b2635-28f5-49ec-b717-8372de9a96fd',
    'bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',
    'c89f8024-0462-4a50-88a9-f7e86056d485',
    'f87706b1-cea4-4765-9d50-7647ee9bda9b',
]


@pytest.mark.vcr
@pytest.mark.parametrize('alert_id', test_input)
def test_pba_update_no_task_prefix(alert_id):
    result = runner.invoke(app, args=[COMMAND, alert_id, '-s', 'Dismissed'])
    assert result.exit_code == 0


@pytest.mark.vcr
def test_pba_update_task_prefix():
    result = runner.invoke(
        app, args=[COMMAND, 'task:99a83597-3c3f-49c0-af56-c06a636532e8', '-s', 'Dismissed']
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        args=[
            COMMAND,
            'task:db6b2635-28f5-49ec-b717-8372de9a96fd',
            '-s',
            'Resolved',
            '-r',
            'Never',
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        args=[
            COMMAND,
            'task:bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',
            '-s',
            'InProgress',
            '-p',
            'High',
            '--comment',
            'Bumping priority to High due to recent findings.',
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        args=[
            COMMAND,
            'task:c89f8024-0462-4a50-88a9-f7e86056d485',
            '-s',
            'Resolved',
            '-p',
            'Moderate',
            '--comment',
            'cool comment',
            '--assignee',
            'uhash:6dCcPQn3uO',
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app, args=[COMMAND, 'task:f87706b1-cea4-4765-9d50-7647ee9bda9b', '-s', 'InProgress']
    )
    assert result.exit_code == 0


@pytest.mark.vcr
def test_pba_update_error():
    # bad alert ID
    result = runner.invoke(
        app, args=[COMMAND, '99a83597-1111-1111-1111-c06a636532e8', '-s', 'Dismissed']
    )
    assert result.exit_code == 1

    assert (
        result.output == '\nNOT FOUND:\n99a83597-1111-1111-1111-c06a636532e8\n'  # noqa: E501
    )
