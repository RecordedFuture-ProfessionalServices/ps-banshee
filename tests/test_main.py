import sys
from unittest.mock import call, patch

import pytest
import typer
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app as list_app
from banshee.commands.errors import InitConfigError
from banshee.main import app, squelch_uncaught_exception

from .conftest import strip_ansi

runner = CliRunner()


def test_main_no_args():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert 'Usage: root [OPTIONS] COMMAND [ARGS]...' in strip_ansi(result.output)


@pytest.mark.vcr
def test_main_no_debug():
    cases = [
        (
            ['bulk-add', 'meow', 'ip:8.8.8.8'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Spaghetti Bolognese',
        ),
        (
            ['bulk-remove', 'meow', 'ip:8.8.8.8'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Caviar',
        ),
        (
            ['add', 'meow', 'ip:8.8.8.8'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Home fries',
        ),
        (
            ['remove', 'meow', 'ip:8.8.8.8'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Chocolate Brownie',
        ),
        (
            ['add', 'report:wpHivJ', 'not_a_real_entity'],
            "Failed to add entity 'not_a_real_entity'. 400 Client Error: Bad Request for url: https://api.recordedfuture.com/list/report:wpHivJ/entity/add, Cause: Succotash",
        ),
        (
            ['remove', 'report:wpHivJ', 'not_a_real_entity'],
            "Failed to remove entity 'not_a_real_entity'. 400 Client Error: Bad Request for url: https://api.recordedfuture.com/list/report:wpHivJ/entity/remove, Cause: Mozzarella sticks",
        ),
        (
            ['info', 'meow'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Mission burrito',
        ),
        (
            ['status', 'meow'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Blue cheese dressing',
        ),
        (
            ['entities', 'meow'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Prawn Pizza',
        ),
        (
            ['entries', 'meow'],
            'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: Hot Chicken sandwich',
        ),
    ]
    for case in cases:
        args, expected = case
        result = runner.invoke(list_app, args=args)
        assert result.exception.message == expected
        assert result.exit_code == 1


@pytest.mark.usefixtures('_reset_sys_excepthook')
def test_main_debug_off_set_squelch_exception():
    result = runner.invoke(app, args=['ioc'])
    assert result.exit_code == 0
    assert sys.excepthook == squelch_uncaught_exception


@pytest.mark.usefixtures('_reset_sys_excepthook')
def test_main_debug_on_dont_set_squelch_exception():
    result = runner.invoke(app, args=['--debug', 'ioc'])
    assert result.exit_code == 0
    assert sys.excepthook != squelch_uncaught_exception


def test_main_bad_token():
    result = runner.invoke(app, args=['-k', 'bad_token_01'])
    assert result.exit_code == 1
    assert isinstance(result.exception, InitConfigError)
    assert str(result.exception) == 'Invalid Recorded Future API key'


@pytest.mark.parametrize(
    ('argv', 'expected'),
    [
        # ioc
        (['banshee', 'ioc', 'lookup', '1.1.1.1'], 'ioc-lookup'),
        (['banshee', 'ioc', 'bulk-lookup', '1.1.1.1', '8.8.8.8'], 'ioc-bulk-lookup'),
        (['banshee', 'ioc', 'search', '--entity-type', 'ip', '--risk-score', '90'], 'ioc-search'),
        (['banshee', 'ioc', 'rules', 'ip'], 'ioc-rules'),
        (['banshee', 'ioc'], 'ioc'),
        # entity
        (['banshee', 'entity', 'lookup', 'ip:1.1.1.1'], 'entity-lookup'),
        (['banshee', 'entity', 'search', 'somequery'], 'entity-search'),
        # list
        (['banshee', 'list', 'info', 'mylist-id'], 'list-info'),
        (['banshee', 'list', 'add', 'mylist-id', 'ip:1.1.1.1'], 'list-add'),
        (['banshee', 'list', 'bulk-add', 'mylist-id'], 'list-bulk-add'),
        (['banshee', 'list', 'remove', 'mylist-id', 'ip:1.1.1.1'], 'list-remove'),
        (['banshee', 'list', 'bulk-remove', 'mylist-id'], 'list-bulk-remove'),
        (['banshee', 'list', 'entities', 'mylist-id'], 'list-entities'),
        (['banshee', 'list', 'entries', 'mylist-id'], 'list-entries'),
        (['banshee', 'list', 'status', 'mylist-id'], 'list-status'),
        (['banshee', 'list', 'clear', 'mylist-id'], 'list-clear'),
        # classic alerts
        (['banshee', 'ca', 'lookup', 'alert-abc123'], 'ca-lookup'),
        (['banshee', 'ca', 'search', '-r', 'malware'], 'ca-search'),
        (['banshee', 'ca', 'rules'], 'ca-rules'),
        (['banshee', 'ca', 'update', '123456', '--status', 'New'], 'ca-update'),
        # playbook alerts
        (['banshee', 'pba', 'search', '--status', 'New'], 'pba-search'),
        (['banshee', 'pba', 'lookup', 'alert-xyz789'], 'pba-lookup'),
        (['banshee', 'pba', 'update', 'alert-xyz789', '--status', 'Resolved'], 'pba-update'),
        # risklist
        (['banshee', 'risklist', 'fetch', '--entity-type', 'ip'], 'risklist-fetch'),
        (['banshee', 'risklist', 'stat', '--entity-type', 'domain'], 'risklist-stat'),
        # rules
        (['banshee', 'rules', 'search', '--title', 'phishing'], 'rules-search'),
        # pcap
        (['banshee', 'pcap', 'enrich', 'capture.pcap'], 'pcap-enrich'),
        # global flags mixed in
        (['banshee', '--debug', 'ioc', 'lookup', '1.1.1.1'], 'ioc-lookup'),
        (['banshee', '-k', 'mytoken', 'pba', 'search', '--status', 'new'], 'pba-search'),
        (['banshee', '--no-ssl-verify', 'risklist', 'fetch'], 'risklist-fetch'),
        # no subcommand
        (['banshee'], ''),
        (['banshee', '--debug'], ''),
    ],
)
def test_config_init_called_with_correct_command(argv, expected):
    captured = {}

    def mock_config_init(cmd, *_):
        captured['cmd'] = cmd
        raise typer.Exit()

    with patch('banshee.main.config_init', side_effect=mock_config_init), patch('sys.argv', argv):
        runner.invoke(app, args=argv[1:])

    assert captured.get('cmd', '') == expected


def test_main_squelch_uncaught_exception_prints_to_stderr():
    with patch('sys.stderr') as mock_stderr:
        exc_type = ValueError
        exc_value = ValueError('Test error message')
        exc_traceback = None

        squelch_uncaught_exception(exc_type, exc_value, exc_traceback)

        # sys.stderr.write is called 2 times: once for the content and once for the newline
        mock_stderr.write.assert_has_calls(
            [
                call('ValueError: Test error message'),
                call('\n'),
            ]
        )
