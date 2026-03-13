import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_playbook_alerts import app

runner = CliRunner()

COMMAND = 'search'


@pytest.mark.vcr
def test_pba_search_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 0

    # We expect JSON output by default
    json.loads(result.output)


@pytest.mark.vcr
def test_pba_search_args_pretty():
    result = runner.invoke(app, args=[COMMAND, '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_pba_search_args():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '-C',
            '10d',
            '-c',
            'identity_novel_exposures',
            '-c',
            'domain_abuse',
            '-l',
            '100',
            '-P',
            'High',
            '-s',
            'New',
        ],
    )
    assert result.exit_code == 0

    output = json.loads(result.output)
    num_of_alerts = len(output['data'])
    assert num_of_alerts == 100

    # The subsequent query should have fewer results
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '-C',
            '10d',
            '-c',
            'identity_novel_exposures',
            '-P',
            'High',
            '-P',
            'Moderate',
            '-l',
            '100',
        ],
    )
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output['data']) < num_of_alerts


test_input = [
    (['-C', '2010-01-01'], 1),
    (['-u', '2010-01-01'], 1),
    (['-c', 'bad_category'], 2),
    (['-P', 'informational'], 2),
    (['-s', 'inprogress'], 2),
]


@pytest.mark.parametrize(('args', 'exit_code'), test_input)
def test_pba_search_bad_search_args(args, exit_code):
    result = runner.invoke(app, args=[COMMAND] + args)
    assert result.exit_code == exit_code
