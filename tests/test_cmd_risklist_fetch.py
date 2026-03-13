from pathlib import Path

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_risklist import app

from .conftest import strip_ansi

runner = CliRunner()

COMMAND = 'fetch'

DATA = [
    (
        '--list-name cncSite --entity-type domain -o {}',
        'domain_cncSite.csv',
        'File written to: {}',
    ),
    (
        '--list-name cncSite --entity-type domain -j -o {}',
        'domain_cncSite.json',
        'File written to: {}',
    ),
    (
        '--custom-list-path /public/SNOW/templates/domain_header.tpl -o {}',
        'custom_domain_header.tpl',
        'File written to: {}',
    ),
    (
        '--custom-list-path /public/opencti/threat_actor_bundle.json -o {}',
        'custom_threat_actor_bundle.json',
        'File written to: {}',
    ),
    (
        '--custom-list-path /home/moise/ruff.toml -o {}',
        'custom_ruff.toml',
        'File written to: {}',
    ),
    (
        '--custom-list-path /public/Archer/ArcherVulns.csv -o {}',
        'custom_ArcherVulns.csv',
        'File written to: {}',
    ),
]


@pytest.mark.parametrize(('command', 'filename', 'expected_output'), DATA, ids=[d[1] for d in DATA])
def test_risklist_fetch(tmp_path, command, filename, expected_output):
    result = runner.invoke(app, args=[COMMAND] + command.format(tmp_path).split())
    out_file = tmp_path / filename
    assert strip_ansi(result.output).strip('\n') == expected_output.format(out_file).strip('\n')
    assert out_file.exists()
    assert out_file.stat().st_size > 0


def test_risklist_fetch_cwd():
    result = runner.invoke(app, args=[COMMAND, '--list-name', 'cncSite', '--entity-type', 'domain'])
    out_file = Path.cwd() / 'domain_cncSite.csv'
    assert result.exit_code == 0

    assert strip_ansi(result.output) == f'\nFile written to: {str(out_file)}\n'
    assert out_file.exists()
    assert out_file.stat().st_size > 0
    out_file.unlink(missing_ok=True)


# Validation tests
def test_risklist_fetch_custom_path_with_list_name():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/path/to/file.csv',
            '--list-name',
            'default',
        ],
    )
    assert result.exit_code == 2
    assert '--custom-list-path must be specified alone' in strip_ansi(result.output)


def test_risklist_fetch_custom_path_with_entity_type():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/path/to/file.csv',
            '--entity-type',
            'ip',
        ],
    )
    assert result.exit_code == 2
    assert '--custom-list-path must be specified alone' in strip_ansi(result.output)


def test_risklist_fetch_custom_path_with_both():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/path/to/file.csv',
            '--list-name',
            'default',
            '--entity-type',
            'ip',
        ],
    )
    assert result.exit_code == 2
    assert '--custom-list-path must be specified alone' in strip_ansi(result.output)


def test_risklist_fetch_list_name_without_entity_type():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--list-name',
            'default',
        ],
    )
    assert result.exit_code == 2
    assert '--entity-type is required when using --list-name' in strip_ansi(result.output)


def test_risklist_fetch_entity_type_without_list_name():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--entity-type',
            'ip',
        ],
    )
    assert result.exit_code == 2
    assert '--list-name is required when using --entity-type' in strip_ansi(result.output)


def test_risklist_fetch_no_arguments():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2
    assert 'Either --custom-list-path or (--list-name and --entity-type)' in strip_ansi(
        result.output
    )


def test_risklist_fetch_custom_path_with_as_json():
    result = runner.invoke(
        app,
        args=[
            COMMAND,
            '--custom-list-path',
            '/path/to/file.csv',
            '--as-json',
        ],
    )
    assert result.exit_code == 2
    assert '--as-json can only be used with --list-name and --entity-type' in strip_ansi(
        result.output
    )
