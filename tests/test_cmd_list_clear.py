from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from psengine.entity_lists import EntityList, EntityListMgr, ListEntity
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'clear'


def _make_entity(id_: str, name: str, type_: str, context: dict = None) -> ListEntity:
    return ListEntity(
        entity={'id': id_, 'name': name, 'type': type_},
        status='active',
        added=datetime.now(timezone.utc),
        context=context,
    )


def test_list_clear_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_list_clear_filter_by_note():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]
    mock_entity_list.remove.return_value = MagicMock(result='removed')

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware'])

    assert result.exit_code == 0
    mock_entity_list.remove.assert_called_once_with(entity='ip:1.1.1.1')


def test_list_clear_filter_by_multiple_notes():
    malware = _make_entity('ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'})
    phishing = _make_entity(
        'ip:3.3.3.3', '3.3.3.3', 'IpAddress', context={'annotation': 'phishing'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [malware, phishing, no_annotation]
    mock_entity_list.remove.return_value = MagicMock(result='removed')

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(
            app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware', '-n', 'phishing']
        )

    assert result.exit_code == 0
    assert mock_entity_list.remove.call_count == 2


def test_list_clear_filter_by_exclude_note():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]
    mock_entity_list.remove.return_value = MagicMock(result='removed')

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-e', 'malware'])

    assert result.exit_code == 0
    mock_entity_list.remove.assert_called_once_with(entity='ip:2.2.2.2')


def test_list_clear_filter_by_multiple_exclude_notes():
    malware = _make_entity('ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'})
    phishing = _make_entity(
        'ip:3.3.3.3', '3.3.3.3', 'IpAddress', context={'annotation': 'phishing'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [malware, phishing, no_annotation]
    mock_entity_list.remove.return_value = MagicMock(result='removed')

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(
            app, args=[COMMAND, 'report:wpHivJ', '-e', 'malware', '-e', 'phishing']
        )

    assert result.exit_code == 0
    mock_entity_list.remove.assert_called_once_with(entity='ip:2.2.2.2')


def test_list_clear_filter_by_no_note():
    annotated = _make_entity(
        'ip:1.1.1.1', '1.1.1.1', 'IpAddress', context={'annotation': 'malware'}
    )
    no_annotation = _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress')

    mock_entity_list = MagicMock(spec=EntityList)
    mock_entity_list.entities.return_value = [annotated, no_annotation]
    mock_entity_list.remove.return_value = MagicMock(result='removed')

    with patch.object(EntityListMgr, 'fetch', return_value=mock_entity_list):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-N'])

    assert result.exit_code == 0
    mock_entity_list.remove.assert_called_once_with(entity='ip:2.2.2.2')


def test_list_clear_note_and_exclude_note_mutually_exclusive():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware', '-e', 'malware'])
    assert result.exit_code == 2


def test_list_clear_note_and_no_note_mutually_exclusive():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', '-n', 'malware', '-N'])
    assert result.exit_code == 2


@pytest.mark.vcr(record_mode='new_episodes')
def test_list_clear():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ'])
    assert result.exit_code == 0
    mgr = EntityListMgr()
    list_ = mgr.fetch(list_='report:wpHivJ')
    assert len(list_.entities()) == 0


@pytest.mark.vcr
def test_list_clear_dne():
    result = runner.invoke(app, args=[COMMAND, 'meow'])
    assert result.exit_code == 1
    assert (
        result.exception.message
        == 'Failed to fetch list "meow". 404 Client Error: Not Found for url: https://api.recordedfuture.com/list/meow/info, Cause: The Galactic Empire is nearing com'
    )
