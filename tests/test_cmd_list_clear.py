import pytest
from psengine.entity_lists import EntityListMgr
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'clear'


def test_list_clear_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_list_clear():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ'])
    assert result.exit_code == 0
    mgr = EntityListMgr()
    list_ = mgr.fetch(list_='report:wpHivJ')
    assert len(list_.entities()) == 0


@pytest.mark.vcr
def test_list_clear_dne():
    result = runner.invoke(app, args=[COMMAND, 'meow'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == 'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: The Galactic Empire is nearing com'
    )
