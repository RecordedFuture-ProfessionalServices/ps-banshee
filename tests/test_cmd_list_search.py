import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'search'


@pytest.mark.vcr
def test_list_search_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) == 10


@pytest.mark.vcr
def test_list_search_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'Moise Test', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_list_search_args_json(vcr_cassette):
    result = runner.invoke(app, args=[COMMAND, 'Moise Test'])
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert isinstance(output, list)

    # Should be only 1 request
    assert len(vcr_cassette.requests) == 1

    expected_body = {'limit': 10, 'name': 'Moise Test'}
    body = json.loads(vcr_cassette.requests[0].body)
    assert body == expected_body


@pytest.mark.vcr
def test_list_search_args_type_Attacker(vcr_cassette):
    result = runner.invoke(app, args=[COMMAND, '-t', 'attacker'])
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert isinstance(output, list)

    # Should be only 1 request
    assert len(vcr_cassette.requests) == 1

    expected_body = {'limit': 10, 'type': 'attacker'}
    body = json.loads(vcr_cassette.requests[0].body)
    assert body == expected_body


@pytest.mark.vcr
def test_list_search_dne():
    result = runner.invoke(app, args=[COMMAND, 'aslan'])
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert len(output) == 0
