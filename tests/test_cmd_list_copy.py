from datetime import datetime, timezone
from unittest.mock import MagicMock, call, patch

from psengine.entity_lists import EntityList, EntityListMgr, ListEntity
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'copy'
SOURCE_ID = 'src123'
DEST_ID = 'dst456'


def _make_entity(id_: str, name: str, type_: str) -> ListEntity:
    return ListEntity(
        entity={'id': id_, 'name': name, 'type': type_},
        status='active',
        added=datetime.now(timezone.utc),
    )


def _make_result(status: str) -> MagicMock:
    mock = MagicMock()
    mock.result = status
    return mock


def _fetch_side_effect(source_mock, dest_mock):
    def _inner(list_):
        return source_mock if list_ == SOURCE_ID else dest_mock

    return _inner


def test_list_copy_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_list_copy_missing_destination():
    result = runner.invoke(app, args=[COMMAND, SOURCE_ID])
    assert result.exit_code == 2


def test_list_copy_copies_entities_to_empty_destination():
    source = MagicMock(spec=EntityList)
    source.name = 'Source List'
    source.entities.return_value = [
        _make_entity('ip:1.1.1.1', '1.1.1.1', 'IpAddress'),
        _make_entity('ip:2.2.2.2', '2.2.2.2', 'IpAddress'),
    ]

    dest = MagicMock(spec=EntityList)
    dest.name = 'Destination List'
    dest.entities.return_value = []
    dest.add.return_value = _make_result('added')

    with patch.object(EntityListMgr, 'fetch', side_effect=_fetch_side_effect(source, dest)):
        result = runner.invoke(app, args=[COMMAND, SOURCE_ID, DEST_ID])

    assert result.exit_code == 0
    dest.add.assert_has_calls(
        [call(entity='ip:1.1.1.1'), call(entity='ip:2.2.2.2')], any_order=True
    )
    assert dest.add.call_count == 2
    dest.remove.assert_not_called()
    assert 'ADDED' in result.output
    assert 'ip:1.1.1.1' in result.output
    assert 'ip:2.2.2.2' in result.output


def test_list_copy_empty_source_is_noop():
    source = MagicMock(spec=EntityList)
    source.name = 'Source List'
    source.entities.return_value = []

    dest = MagicMock(spec=EntityList)
    dest.entities.return_value = []

    with patch.object(EntityListMgr, 'fetch', side_effect=_fetch_side_effect(source, dest)):
        result = runner.invoke(app, args=[COMMAND, SOURCE_ID, DEST_ID])

    assert result.exit_code == 0
    assert 'is empty' in result.output
    dest.add.assert_not_called()
    dest.remove.assert_not_called()


def test_list_copy_overwrite_removes_stale_destination_entities():
    source = MagicMock(spec=EntityList)
    source.name = 'Source List'
    source.entities.return_value = [_make_entity('ip:1.1.1.1', '1.1.1.1', 'IpAddress')]

    stale = _make_entity('ip:9.9.9.9', '9.9.9.9', 'IpAddress')
    dest = MagicMock(spec=EntityList)
    dest.name = 'Destination List'
    dest.entities.return_value = [stale]
    dest.add.return_value = _make_result('added')
    dest.remove.return_value = _make_result('removed')

    with patch.object(EntityListMgr, 'fetch', side_effect=_fetch_side_effect(source, dest)):
        result = runner.invoke(app, args=[COMMAND, '--overwrite', SOURCE_ID, DEST_ID])

    assert result.exit_code == 0
    dest.add.assert_called_once_with(entity='ip:1.1.1.1')
    dest.remove.assert_called_once_with(entity='ip:9.9.9.9')
    assert 'ADDED' in result.output
    assert 'ip:1.1.1.1' in result.output
    assert 'REMOVED' in result.output
    assert 'ip:9.9.9.9' in result.output


def test_list_copy_without_overwrite_does_not_remove():
    source = MagicMock(spec=EntityList)
    source.name = 'Source List'
    source.entities.return_value = [_make_entity('ip:1.1.1.1', '1.1.1.1', 'IpAddress')]

    stale = _make_entity('ip:9.9.9.9', '9.9.9.9', 'IpAddress')
    dest = MagicMock(spec=EntityList)
    dest.name = 'Destination List'
    dest.entities.return_value = [stale]
    dest.add.return_value = _make_result('added')

    with patch.object(EntityListMgr, 'fetch', side_effect=_fetch_side_effect(source, dest)):
        result = runner.invoke(app, args=[COMMAND, SOURCE_ID, DEST_ID])

    assert result.exit_code == 0
    dest.add.assert_called_once_with(entity='ip:1.1.1.1')
    dest.remove.assert_not_called()
    assert 'REMOVED' not in result.output
