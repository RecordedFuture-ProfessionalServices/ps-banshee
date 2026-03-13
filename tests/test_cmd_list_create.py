import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'create'


def test_list_create_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_list_create_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'meow', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_list_create_args_json(vcr_cassette):
    result = runner.invoke(app, args=[COMMAND, 'meow'])
    assert result.exit_code == 0
    json.loads(result.output)

    # Should be only 1 request
    assert len(vcr_cassette.requests) == 1

    expected_body = {'name': 'meow', 'type': 'entity'}
    body = json.loads(vcr_cassette.requests[0].body)
    assert body == expected_body


ARGS = ['entity', 'source', 'text']


@pytest.mark.vcr
@pytest.mark.parametrize('list_type', ARGS)
def test_list_create_with_type(list_type):
    result = runner.invoke(app, args=[COMMAND, 'meow', list_type])
    assert result.exit_code == 0


@pytest.mark.vcr
def test_list_create_bad_type():
    result = runner.invoke(app, args=[COMMAND, 'meow', 'bad_type'])
    assert result.exit_code == 2
    assert 'Invalid value' in result.output
