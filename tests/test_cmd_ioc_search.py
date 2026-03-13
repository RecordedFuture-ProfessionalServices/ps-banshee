import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_ioc import app

runner = CliRunner()

COMMAND = 'search'


def test_ioc_search_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('command', 'args', 'expected'),
    [
        ('ip', ['-l 11'], 11),
        ('domain', ['-l 6'], 6),
        ('hash', ['-l 1'], 1),
        ('url', ['-l 20'], 20),
        ('vulnerability', None, 5),
    ],
)
def test_ioc_search_works(command, args, expected):
    result = runner.invoke(app, args=[COMMAND, command] + args if args else [COMMAND, command])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert len(output.get('data').get('results', [])) == expected


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('command', 'args', 'expected'),
    [
        ('ip', ['-l', '1', '-r', '[66,66]'], 66),
        ('domain', ['-l', '1', '-r', '(50,61]'], 58),
        ('hash', ['-l', '1', '-r', '(80,)'], 89),
        ('url', ['-l', '1', '-r', '[20,]'], 89),
        ('vulnerability', ['-l', '1', '-r', '[,90)'], 89),
    ],
)
def test_ioc_search_args_score(command, args, expected):
    result = runner.invoke(app, args=[COMMAND, command] + args)
    assert result.exit_code == 0

    output = json.loads(result.output)
    risk_score = output.get('data').get('results')[0].get('risk').get('score')
    assert risk_score == expected


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('command', 'args', 'expected_field_count'),
    [
        ('ip', ['-l 5'], 3),
        ('ip', ['-l 5', '-v', '1'], 3),
        ('ip', ['-l 5', '-v', '2'], 5),
        ('ip', ['-l 5', '-v', '3'], 7),
        ('ip', ['-l 5', '-v', '4'], 11),
        ('ip', ['-l 5', '-v', '5'], 13),
        ('domain', ['-l 5'], 3),
        ('domain', ['-l 5', '-v', '1'], 3),
        ('domain', ['-l 5', '-v', '2'], 4),
        ('domain', ['-l 5', '-v', '3'], 6),
        ('domain', ['-l 5', '-v', '4'], 10),
        ('domain', ['-l 5', '-v', '5'], 10),
        ('hash', ['-l 5'], 4),
        ('hash', ['-l 5', '-v', '1'], 4),
        ('hash', ['-l 5', '-v', '2'], 6),
        ('hash', ['-l 5', '-v', '3'], 8),
        ('hash', ['-l 5', '-v', '4'], 12),
        ('hash', ['-l 5', '-v', '5'], 12),
        ('url', ['-l 5'], 3),
        ('url', ['-l 5', '-v', '1'], 3),
        ('url', ['-l 5', '-v', '2'], 4),
        ('url', ['-l 5', '-v', '3'], 6),
        ('url', ['-l 5', '-v', '4'], 9),
        ('url', ['-l 5', '-v', '5'], 9),
        ('vulnerability', ['-l 5'], 4),
        ('vulnerability', ['-l 5', '-v', '1'], 4),
        ('vulnerability', ['-l 5', '-v', '2'], 5),
        ('vulnerability', ['-l 5', '-v', '3'], 7),
        ('vulnerability', ['-l 5', '-v', '4'], 14),
        ('vulnerability', ['-l 5', '-v', '5'], 18),
    ],
)
def test_ioc_search_verbose(command, args, expected_field_count):
    result = runner.invoke(app, args=[COMMAND, command] + args)
    assert result.exit_code == 0

    output = json.loads(result.output)
    for result in output.get('data').get('results'):
        assert len(result.keys()) == expected_field_count


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('command', 'args'),
    [
        ('ip', ['-l 5', '-p']),
        ('domain', ['-l 5', '-p']),
        ('hash', ['-l 5', '-p']),
        ('url', ['-l 5', '-p']),
        ('vulnerability', ['-l 5', '-p']),
    ],
)
def test_ioc_search_pretty_print(command, args):
    result = runner.invoke(app, args=[COMMAND, command] + args)
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.parametrize(
    ('command', 'args'),
    [
        ('ip', ['-lap']),
        ('domainz', ['-l 5', '-p']),
        ('hash', ['-u']),
        ('url', ['-l 1500']),
        ('vulnerability', ['-l 5w']),
    ],
)
def test_ioc_search_fails(command, args):
    result = runner.invoke(app, args=[COMMAND, command] + args)
    assert result.exit_code == 2
