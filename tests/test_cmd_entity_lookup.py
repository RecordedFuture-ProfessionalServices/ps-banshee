import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_entity import app

runner = CliRunner()

COMMAND = 'lookup'


def test_entity_lookup_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_entity_lookup_bad_id():
    result = runner.invoke(app, args=[COMMAND, 'bad-entity-id-cgssdgsd'])
    assert result.exit_code == 1


@pytest.mark.vcr
def test_entity_lookup_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'SoA6SP', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
@pytest.mark.parametrize(('entity_id'), ['SoA6SP', 'ME4QX', 'JLHNoH'])
def test_entity_lookup_json_response(entity_id):
    result = runner.invoke(app, args=[COMMAND, entity_id])
    assert result.exit_code == 0

    json.loads(result.output)
