import json

import pytest
from psengine.classic_alerts import NoRulesFoundError
from typer.testing import CliRunner

from banshee.commands.cmd_classic_alerts import app

runner = CliRunner()

COMMAND = 'search'


@pytest.mark.vcr
def test_ca_search_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 0

    # We expect JSON output by default
    json.loads(result.output)


@pytest.mark.vcr
def test_ca_search_args_pretty():
    result = runner.invoke(app, args=[COMMAND, '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_ca_search_args_triggered():
    result = runner.invoke(app, args=[COMMAND, '-t', '2d'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    num_of_alerts_first_search = len(output)
    assert num_of_alerts_first_search > 0

    # The subsequent query should have fewer results
    result = runner.invoke(app, args=[COMMAND, '-t', '1d'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) < num_of_alerts_first_search


@pytest.mark.vcr
def test_ca_search_args_triggered_range():
    result = runner.invoke(app, args=[COMMAND, '-t', '[2025-05-01, 2025-05-05]'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) == 231


@pytest.mark.vcr
def test_ca_search_args_status():
    result = runner.invoke(app, args=[COMMAND, '-s', 'Pending', '-t', '[2025-09-15, 2025-09-16]'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) == 1

    assert output[0]['review']['status_in_portal'] == 'Pending'


@pytest.mark.vcr
def test_ca_search_args_rules():
    result = runner.invoke(app, args=[COMMAND, '-r', 'leaked'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) > 0


@pytest.mark.vcr
def test_ca_search_args_rules_not_found():
    result = runner.invoke(app, args=[COMMAND, '-r', 'non_existing_rule'])
    assert result.exit_code == 1
    assert isinstance(result.exception, NoRulesFoundError)
    assert result.exception.message == "No matching rules found for rule IDs: ['non_existing_rule']"


@pytest.mark.vcr
def test_ca_search_args_rules_multiple(vcr_cassette):
    rule_names = ['Leaked Credential Monitoring', 'Brand Mentions with Cyber entities']

    result = runner.invoke(
        app,
        args=[COMMAND] + [arg for rule in rule_names for arg in ['-r', rule]],
    )
    assert result.exit_code == 0

    # Instead of checking the response, check what was requested
    found_rules = set()
    for request in vcr_cassette.requests:
        url = request.uri
        for rule_name in rule_names:
            if rule_name.replace(' ', '+') in url:
                found_rules.add(rule_name)

    assert found_rules == set(rule_names)
