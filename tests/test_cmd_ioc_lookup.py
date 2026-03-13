import json
from urllib.parse import quote

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_ioc import app

runner = CliRunner()

COMMAND = 'lookup'


@pytest.mark.vcr
def test_ioc_lookup_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_ioc_lookup_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'ip', '117.72.35.30', '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_ioc_lookup_args_pretty_with_ai():
    result = runner.invoke(app, args=[COMMAND, 'ip', '209.74.66.25', '-p', '-a'])
    assert result.exit_code == 0

    assert 'AI Insights:' in result.stdout


@pytest.mark.vcr
def test_ioc_lookup_with_ai():
    result = runner.invoke(app, args=[COMMAND, 'ip', '209.74.66.25', '-a'])
    assert result.exit_code == 0

    assert json.loads(result.output)[0]['aiInsights']['text']


@pytest.mark.vcr
def test_ioc_lookup_verbose_with_ai():
    result = runner.invoke(app, args=[COMMAND, 'ip', '209.74.66.25', '-v', '3', '-a'])
    assert result.exit_code == 0

    assert json.loads(result.output)[0]['aiInsights']['text']


@pytest.mark.vcr
def test_ioc_lookup_bad_iocs():
    result = runner.invoke(app, args=[COMMAND, 'ip', '117.72.35.30', '8.8.898753', '-p'])
    assert result.exit_code == 0

    assert '404' in result.output


@pytest.mark.vcr
def test_ioc_lookup_non_existing_ioc_pretty_print():
    # A scenario where the API returns a 404
    result = runner.invoke(app, args=[COMMAND, 'domain', 'wowzasomethng.com', '-p'])
    assert result.exit_code == 0

    assert '404 received. Nothing known on this entity' in result.output


@pytest.mark.vcr
def test_ioc_lookup_non_existing_ioc_json_print():
    # A scenario where the API returns a 404
    result = runner.invoke(app, args=[COMMAND, 'domain', 'wowzasomethng.com'])
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert output == [
        {
            'entity': 'wowzasomethng.com',
            'entity_type': 'domain',
            'is_enriched': False,
            'content': '404 received. Nothing known on this entity',
        }
    ]


@pytest.mark.parametrize(
    ('entity_type', 'iocs'),
    [
        ('ip', ['185.49.126.52', '139.224.198.190', '98.142.95.254']),
        ('domain', ['aewrhprres.com', 'avsvmcloud.com']),
        ('url', ['http://alphastand.win/alien/fre.php', 'http://alphastand.top/alien/fre.php']),
        ('vulnerability', ['CVE-2020-1362', 'CVE-2011-0611']),
        (
            'hash',
            [
                '4e586d008dc06d3c77d590393b4e565273b30ef2b536a193976c9a82353878bf',
                'fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92',
            ],
        ),
        ('ip', ['117.72.35.30']),
    ],
)
@pytest.mark.vcr
def test_ioc_lookup_json(entity_type, iocs, vcr_cassette):
    result = runner.invoke(app, args=[COMMAND, entity_type] + iocs)
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert isinstance(output, list)
    assert all(isinstance(x, dict) for x in output)
    assert len(output) == len(iocs)
    for ioc in output:
        assert ioc['risk'] is not None
        assert isinstance(ioc['risk']['score'], int)

    assert len(vcr_cassette.requests) == len(iocs)

    # Check that each IOC appears in at least one request URI
    all_uris = [request.uri for request in vcr_cassette.requests]
    for ioc in iocs:
        assert any(quote(ioc, safe='') in uri for uri in all_uris), (
            f'IOC {ioc} not found in any request URI'
        )


@pytest.mark.vcr
@pytest.mark.parametrize(
    ('entity_type', 'args', 'expected_field_count'),
    [
        ('ip', ['45.134.26.41'], 3),
        ('ip', ['45.134.26.41', '-v', '1'], 3),
        ('ip', ['45.134.26.41', '-v', '2'], 5),
        ('ip', ['45.134.26.41', '-v', '3'], 7),
        ('ip', ['45.134.26.41', '-v', '4'], 11),
        ('ip', ['45.134.26.41', '-v', '5'], 13),
        ('domain', ['digitalcollege.org'], 3),
        ('domain', ['digitalcollege.org', '-v', '1'], 3),
        ('domain', ['digitalcollege.org', '-v', '2'], 4),
        ('domain', ['digitalcollege.org', '-v', '3'], 6),
        ('domain', ['digitalcollege.org', '-v', '4'], 10),
        ('domain', ['digitalcollege.org', '-v', '5'], 10),
        ('hash', ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92'], 4),
        (
            'hash',
            ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92', '-v', '1'],
            4,
        ),
        (
            'hash',
            ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92', '-v', '2'],
            6,
        ),
        (
            'hash',
            ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92', '-v', '3'],
            8,
        ),
        (
            'hash',
            ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92', '-v', '4'],
            12,
        ),
        (
            'hash',
            ['fa54c4e34732b611921820be56dd690a4de98285828e4be487b904679a855a92', '-v', '5'],
            12,
        ),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7'], 3),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7', '-v', '1'], 3),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7', '-v', '2'], 4),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7', '-v', '3'], 6),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7', '-v', '4'], 9),
        ('url', ['https://webhook.site/bb8ca5f6-4175-45d2-b042-fc9ebb8170b7', '-v', '5'], 9),
        ('vulnerability', ['CVE-2012-4792'], 4),
        ('vulnerability', ['CVE-2012-4792', '-v', '1'], 4),
        ('vulnerability', ['CVE-2012-4792', '-v', '2'], 5),
        ('vulnerability', ['CVE-2012-4792', '-v', '3'], 7),
        ('vulnerability', ['CVE-2012-4792', '-v', '4'], 14),
        ('vulnerability', ['CVE-2012-4792', '-v', '5'], 18),
    ],
)
def test_ioc_lookup_verbose(entity_type, args, expected_field_count):
    result = runner.invoke(app, args=[COMMAND, entity_type] + args)
    assert result.exit_code == 0

    output = json.loads(result.output)
    for result in output:
        assert len(result.keys()) == expected_field_count
