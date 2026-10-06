import json
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from psengine.entity_lists import EntityList, EntityListMgr, ListEntity
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'entities'


def test_list_entities_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_list_entities_args_pretty():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-p'])
    assert result.exit_code == 0
    assert 'Total entities' in result.output

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)


@pytest.mark.vcr
def test_list_entities_args_json():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ'])
    assert result.exit_code == 0

    output = json.loads(result.output)

    assert isinstance(output, list)
    assert len(output) == 2
    assert all('entity' in entity for entity in output)
    assert all('status' in entity for entity in output)
    assert all('added' in entity for entity in output)


@pytest.mark.vcr
def test_list_entities_dne():
    result = runner.invoke(app, args=[COMMAND, 'meow'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == 'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: The syntax {D1,D2,...,Dn} denotes '
    )


def _make_entity(id_: str, name: str, type_: str, context: dict = None) -> ListEntity:
    return ListEntity(
        entity={'id': id_, 'name': name, 'type': type_},
        status='active',
        added=datetime.now(timezone.utc),
        context=context,
    )


def test_list_entities_filter_by_note():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware'])

    assert result.exit_code == 0
    assert 'ip:1.1.1.1' in result.output
    assert 'ip:2.2.2.2' not in result.output


def test_list_entities_filter_by_invert():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-i', 'malware'])

    assert result.exit_code == 0
    assert 'ip:1.1.1.1' not in result.output
    assert 'ip:2.2.2.2' in result.output


def test_list_entities_filter_by_empty():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-e'])

    assert result.exit_code == 0
    assert 'ip:1.1.1.1' not in result.output
    assert 'ip:2.2.2.2' in result.output


def test_list_entities_note_and_invert_mutually_exclusive():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware', '-i', 'malware'])
    assert result.exit_code == 2


def test_list_entities_note_and_empty_mutually_exclusive():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware', '-e'])
    assert result.exit_code == 2
