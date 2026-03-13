import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_risklist import app

from .conftest import strip_ansi

runner = CliRunner()

COMMAND = 'stat'


@pytest.mark.vcr
def test_risklist_stat():
    result = runner.invoke(app, args=[COMMAND, '--list-name', 'cncSite', '--entity-type', 'domain'])
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert output == {
        'etag': '06c8465e3d34b4ad96da6febde8af8c5',
        'exists': True,
        'name': 'cncSite_domain_risklist',
    }


@pytest.mark.vcr
def test_risklist_stat_pretty():
    result = runner.invoke(
        app, args=[COMMAND, '--list-name', 'cncSite', '--entity-type', 'domain', '--pretty']
    )
    assert result.exit_code == 0
    assert (
        result.output
        == '  Name:    cncSite_domain_risklist           \n  ETag:    06c8465e3d34b4ad96da6febde8af8c5  \n'  # noqa: E501
    )


@pytest.mark.vcr
def test_risklist_stat_fusion():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/c2_communicating_ips_list.csv']
    )
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert output == {
        'etag': 'c1b3f0d7220a21fdada5c27d8070255f1dde8f4dbb69c07ee83470ccfafd6907',
        'exists': True,
        'last-modified': 'Thu, 12 Feb 2026 17:15:01 GMT',
        'path': '/public/prevent/c2_communicating_ips_list.csv',
    }


@pytest.mark.vcr
def test_risklist_stat_fusion_pretty():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/public/prevent/c2_communicating_ips_list.csv',
            '--pretty',
        ],
        env={'COLUMNS': '200'},
    )
    assert result.exit_code == 0
    assert strip_ansi(result.output).split()[:-1] == [
        'Path:',
        '/public/prevent/c2_communicating_ips_list.csv',
        'Last',
        'Modified:',
        'Feb',
        '12',
        '17:15:01',
        'UTC',
        'ETag:',
    ]
    assert 'c1b3f0d7220a21fdada5c27d8070255f1dde8f4dbb69c07ee83470ccfafd6907' in strip_ansi(
        result.output
    ).strip('\n')


@pytest.mark.vcr
def test_risklist_stat_fusion_not_found():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/bad-list4040404.csv']
    )
    assert result.exit_code == 1

    output = json.loads(result.output)

    assert output == {'path': '/public/prevent/bad-list4040404.csv', 'exists': False}


@pytest.mark.vcr
def test_risklist_stat_fusion_not_found_pretty():
    result = runner.invoke(
        app, args=[COMMAND, '--custom-list-path', '/public/prevent/bad-list4040404.csv', '--pretty']
    )
    assert result.exit_code == 1
    assert result.output == 'File not found /public/prevent/bad-list4040404.csv\n'
