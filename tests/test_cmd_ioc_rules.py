import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_ioc import app
from banshee.indicators.rules import _filter_rules

runner = CliRunner()

COMMAND = 'rules'


def test_ioc_rules_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


IOC_RULES_BASIC_INPUT = [
    ('ip', 90),
    ('hash', 18),
    ('url', 40),
    ('domain', 78),
    ('vulnerability', 42),
]


@pytest.mark.parametrize(
    ('entity_type', 'expected_count'),
    IOC_RULES_BASIC_INPUT,
    ids=(i[0] for i in IOC_RULES_BASIC_INPUT),
)
@pytest.mark.vcr
def test_ioc_rules_args_pretty(entity_type: str, expected_count: str):
    result = runner.invoke(app, args=[COMMAND, entity_type, '-p'])
    assert result.exit_code == 0

    assert f'Total {expected_count} rules found' in result.output


@pytest.mark.parametrize(
    ('entity_type', 'expected_count'),
    IOC_RULES_BASIC_INPUT,
    ids=(i[0] for i in IOC_RULES_BASIC_INPUT),
)
@pytest.mark.vcr
def test_ioc_rules_json(entity_type: str, expected_count: str):
    result = runner.invoke(app, args=[COMMAND, entity_type])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output) == expected_count


IOC_RULES_FILTER_INPUT = [
    (['ip', '-F', 'cnc']),
    (['ip', '-F', 'nonsense']),
    (['hash', '-C', '3']),
    (['url', '-F', 'historical']),
    (['url', '-F', 'INSIKT']),
    (['domain', '-M', 'T1566']),
    (['vulnerability', '-C', '2', '-F', 'concept', '-M', 'T1587.004']),
    (['vulnerability', '-C', '5']),
]


@pytest.mark.parametrize(
    ('args'),
    IOC_RULES_FILTER_INPUT,
    ids=list(range(len(IOC_RULES_FILTER_INPUT))),
)
@pytest.mark.vcr
def test_ioc_rules_args_filters(args, vcr_cassette):
    result = runner.invoke(app, args=[COMMAND] + args)
    assert result.exit_code == 0
    json.loads(result.output)

    # Should be only 1 request
    assert len(vcr_cassette.requests) == 1


RULES_PAYLOAD = [
    {
        'criticalityLabel': 'Malicious',
        'description': 'Recent cnc server',
        'categories': [],
        'criticality': 3,
        'relatedEntities': [],
        'name': 'recentCnc',
        'count': 2019,
    },
    {
        'criticalityLabel': 'Suspicious',
        'description': 'Historical malware spreader',
        'categories': [{'name': 'T1496', 'framework': 'MITRE'}],
        'criticality': 2,
        'relatedEntities': [],
        'name': 'historicalMalware',
        'count': 1,
    },
    {
        'criticalityLabel': 'Unusual',
        'description': 'Historically Reported by DHS AIS',
        'categories': [],
        'criticality': 1,
        'relatedEntities': [],
        'name': 'dhsAis',
        'count': 12027,
    },
    {
        'criticalityLabel': 'Very Malicious',
        'description': 'Recently Validated C&C URL',
        'categories': [{'name': 'TA0011', 'framework': 'MITRE'}],
        'criticality': 4,
        'relatedEntities': [],
        'name': 'recentValidatedCnc',
        'count': 0,
    },
    {
        'criticalityLabel': 'Unusual',
        'description': 'Historically Reported Fraudulent Content',
        'categories': [{'name': 'T1566.003', 'framework': 'MITRE'}],
        'criticality': 1,
        'relatedEntities': [],
        'name': 'fraudulentContent',
        'count': 9656012,
    },
]

# freetext, mitre_code, criticality, expected_count
FILTER_TEST_CASES = [
    (None, None, None, 5),
    ('cnc', None, None, 2),
    (None, 'T1496', None, 1),
    (None, None, 3, 1),
    ('cnc', 'TA0011', 4, 1),
    ('cnc', 'TA0011', 3, 0),
]


@pytest.mark.parametrize(
    ('freetext', 'mitre_code', 'criticality', 'expected_count'),
    FILTER_TEST_CASES,
)
def test_ioc_filter_rules(freetext, mitre_code, criticality, expected_count):
    filtered_rules = _filter_rules(RULES_PAYLOAD, freetext, mitre_code, criticality)
    assert len(filtered_rules) == expected_count
