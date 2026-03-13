import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'remove'


def test_list_add_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_list_add():
    result = runner.invoke(app, args=[COMMAND, 'report:21YKUC', 'ip:10.10.10.10'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_list_add_dne():
    result = runner.invoke(app, args=[COMMAND, 'meow', 'ip:10.10.10.10'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == 'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: The arguments can be primitive dat'
    )


@pytest.mark.vcr
def test_list_add_invalid_entity():
    result = runner.invoke(app, args=[COMMAND, 'report:21YKUC', '123456'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == "Failed to remove entity '123456'. 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/report:21YKUC/entity/remove, Cause: Chicago Deep Dish Pizza"
    )
