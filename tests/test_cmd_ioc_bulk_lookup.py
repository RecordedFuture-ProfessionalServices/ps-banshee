import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_ioc import app

runner = CliRunner()

COMMAND = 'bulk-lookup'


def test_ioc_bulk_lookup_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_ioc_bulk_lookup_missing_iocs():
    result = runner.invoke(app, args=[COMMAND, 'ip'])
    assert result.exit_code == 2


def test_ioc_bulk_lookup_invalid_entity_type():
    result = runner.invoke(app, args=[COMMAND, 'foobar', '1.1.1.1'])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_ioc_bulk_lookup_json_output():
    result = runner.invoke(app, args=[COMMAND, 'ip', '8.8.8.8'])

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0]['risk']['score'], int)


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('entity_type', 'iocs'),
    [
        ('ip', ['8.8.8.8', '203.0.113.17']),
        ('domain', ['overafazg.org', 'coolbeans.org']),
        ('vulnerability', ['CVE-2012-4792', 'CVE-2011-0611']),
        ('hash', ['e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877']),
    ],
)
def test_ioc_bulk_lookup_entity_types(entity_type, iocs):
    result = runner.invoke(app, args=[COMMAND, entity_type] + iocs)

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert isinstance(output, list)
    assert len(output) == len(iocs)
    for item in output:
        assert isinstance(item['risk']['score'], int)


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('entity_type', 'ioc', 'expect_description'),
    [
        ('vulnerability', 'CVE-2012-4792', True),
        ('ip', '8.8.8.8', False),
        ('domain', 'overafazg.org', False),
        ('hash', 'e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877', False),
    ],
)
def test_ioc_bulk_lookup_pretty(entity_type, ioc, expect_description):
    result = runner.invoke(app, args=[COMMAND, entity_type, ioc, '-p'])

    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)

    assert 'IOC' in result.output
    assert 'Risk Score' in result.output
    assert 'Top Rule' in result.output
    if expect_description:
        assert 'Description' in result.output
    else:
        assert 'Description' not in result.output
