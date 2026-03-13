import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_entity import app
from banshee.entity_match.errors import EntityNotFoundError

runner = CliRunner()

COMMAND = 'search'


def test_entity_search_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_entity_search_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'wannacry', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_entity_search_args_limit():
    result = runner.invoke(app, args=[COMMAND, 'wannacry', '-l', '5'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    num_of_entities_first_search = len(output)
    assert num_of_entities_first_search > 0

    # The subsequent query should have fewer results
    result = runner.invoke(app, args=[COMMAND, 'wannacry', '-l', '3'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) < num_of_entities_first_search


@pytest.mark.parametrize(
    ('entity_name', 'entity_type'),
    [('wannacry', 'Malware'), ('Windows', 'Product'), ('Amazon', 'Company')],
)
@pytest.mark.vcr
def test_entity_search_args_type(entity_name, entity_type):
    result = runner.invoke(app, args=[COMMAND, entity_name, '-t', entity_type, '-l', 1])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) > 0

    assert output[0]['type'].lower() == entity_type.lower()


@pytest.mark.vcr
def test_entity_search_entity_not_found():
    result = runner.invoke(app, args=[COMMAND, 'usdfgbuisfdgbdf'])
    assert result.exit_code == 1
    assert isinstance(result.exception, EntityNotFoundError)
    assert result.exception.args[0] == "Entity 'usdfgbuisfdgbdf' not found"


@pytest.mark.vcr
def test_entity_search_entity_not_found_pretty():
    result = runner.invoke(app, args=[COMMAND, 'usdfgbuisfdgbdf', '-p'])
    assert result.exit_code == 1
    assert isinstance(result.exception, EntityNotFoundError)
    assert result.exception.args[0] == "Entity 'usdfgbuisfdgbdf' not found"
