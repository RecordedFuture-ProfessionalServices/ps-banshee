import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_rules import app

runner = CliRunner()


@pytest.mark.vcr
def test_rules_search_no_args():
    result = runner.invoke(app, args=[])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 10


@pytest.mark.vcr
def test_rules_search_pretty():
    result = runner.invoke(app, args=['-p', '-t', 'sigma'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)

    assert 'ID' in result.output
    assert 'Type' in result.output
    assert 'Title' in result.output
    assert 'Created' in result.output
    assert 'Updated' in result.output
    assert 'Files' in result.output


@pytest.mark.parametrize('rule_type', ['yara', 'sigma', 'snort'])
@pytest.mark.vcr
def test_rules_search_by_type(rule_type):
    result = runner.invoke(app, args=['-t', rule_type])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) > 0
    for rule in output:
        assert rule['type'] == rule_type


@pytest.mark.vcr
def test_rules_search_multiple_types():
    result = runner.invoke(app, args=['-t', 'yara', '-t', 'sigma', '-l', '100'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) > 0

    types = {rule['type'] for rule in output}
    assert 'yara' in types or 'sigma' in types


@pytest.mark.vcr
def test_rules_search_threat_actor_and_malware_map_combined():
    # First get results with just threat actor map
    result_actors = runner.invoke(app, args=['-T', '-l', '1000'])
    assert result_actors.exit_code == 0
    output_actors = json.loads(result_actors.output)
    num_actors = len(output_actors)

    # Then get results with just malware map
    result_malware = runner.invoke(app, args=['-M', '-l', '1000'])
    assert result_malware.exit_code == 0
    output_malware = json.loads(result_malware.output)
    num_malware = len(output_malware)

    # Then get results with both combined
    result_combined = runner.invoke(app, args=['-T', '-M', '-l', '1000'])
    assert result_combined.exit_code == 0
    output_combined = json.loads(result_combined.output)
    num_combined = len(output_combined)

    # Combined should have more results than either alone (unless there's complete overlap)
    assert num_combined > num_actors
    assert num_combined > num_malware


@pytest.mark.vcr
def test_rules_search_by_id():
    result = runner.invoke(app, args=['-i', 'doc:l0e9UB'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    if len(output) == 1:
        assert output[0]['id'] == 'doc:l0e9UB'


@pytest.mark.vcr
def test_rules_search_by_entity():
    result = runner.invoke(app, args=['-e', 'lzQ5GL'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 2


@pytest.mark.vcr
def test_rules_search_multiple_entities():
    result = runner.invoke(app, args=['-e', 'lzQ5GL', '-e', 'kK5UbE'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 4


@pytest.mark.vcr
def test_rules_search_by_created_after():
    result = runner.invoke(app, args=['-a', '7d', '-l', '20'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    num_results_7d = len(output)

    result = runner.invoke(app, args=['-a', '1d', '-l', '20'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) <= num_results_7d


@pytest.mark.vcr
def test_rules_search_by_created_before():
    result = runner.invoke(app, args=['-b', '2015-01-01'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 0


@pytest.mark.vcr
def test_rules_search_by_updated_before():
    result = runner.invoke(app, args=['-U', '2015-01-01'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 0


# check instead that api query was correct and not response as filtering is done on API side
@pytest.mark.vcr
def test_rules_search_by_title():
    result = runner.invoke(app, args=['-n', 'ransomware'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)


@pytest.mark.vcr
def test_rules_search_with_limit():
    result = runner.invoke(app, args=['-l', '5'])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) == 5


@pytest.mark.vcr
def test_rules_search_combined_filters():
    result = runner.invoke(
        app,
        args=['-t', 'yara', '-a', '30d', '-l', '15'],
    )
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 11
    for rule in output:
        assert rule['type'] == 'yara'


@pytest.mark.vcr
def test_rules_search_output_to_file(tmp_path):
    output_dir = tmp_path / 'rules'
    result = runner.invoke(app, args=['-l', '2', '-o', str(output_dir)])
    assert result.exit_code == 0

    assert 'Saved 2 rule files to disk' in result.output
    files = list(output_dir.glob('*'))
    assert len(files) == 2
