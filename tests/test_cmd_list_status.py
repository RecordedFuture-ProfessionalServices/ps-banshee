import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'status'


def test_list_status_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_list_status_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_list_status_args_json():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ'])
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert isinstance(output, dict)
    assert output['size'] == 2
    assert output['status'] == 'ready'


@pytest.mark.vcr
def test_list_status_dne():
    result = runner.invoke(app, args=[COMMAND, 'meow'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == 'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: The sequential subset of Erlang su'
    )
