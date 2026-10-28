#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly "as-is" and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

import json
from unittest.mock import MagicMock, patch

import pytest
from psengine.analyst_notes.errors import AnalystNoteSearchError

from banshee.analyst_notes.note_search import search_notes

_PATCH_MGR = patch('banshee.analyst_notes.note_search.AnalystNoteMgr')
_PATCH_TIME = patch('banshee.analyst_notes.note_search.format_time', return_value='2026-01-01')

_ARGS = {
    'published': '-1d',
    'entity': 'ip:1.1.1.1',
    'author': 'abc123',
    'title': 'A title',
    'topic': ['topic1', 'topic2'],
    'label': 'a label',
    'source': 'a source',
    'max_results': 50,
    'pretty': False,
}

_NO_FILTERS = {
    'published': '-1d',
    'entity': None,
    'author': None,
    'title': None,
    'topic': None,
    'label': None,
    'source': None,
    'max_results': 100,
    'pretty': False,
}


def _make_note(index: int):
    note = MagicMock()
    note.id_ = f'doc:note_{index:03d}'
    note.attributes.title = f'Note Title {index}'
    note.attributes.text = f'Note text {index}.'
    note.source.name = f'Source {index}'
    note.json.return_value = {'id': note.id_, 'attributes': {'title': note.attributes.title}}
    return note


@_PATCH_MGR
def test_search_forwards_all_args(mock_mgr):
    mock_mgr.return_value.search.return_value = []
    search_notes(**_ARGS)
    mock_mgr.return_value.search.assert_called_once_with(
        published='-1d',
        entity='ip:1.1.1.1',
        author='abc123',
        title='A title',
        topic=['topic1', 'topic2'],
        label='a label',
        source='a source',
        max_results=50,
    )


@_PATCH_MGR
def test_search_forwards_none_filters(mock_mgr):
    mock_mgr.return_value.search.return_value = []
    search_notes(**_NO_FILTERS)
    mock_mgr.return_value.search.assert_called_once_with(
        published='-1d',
        entity=None,
        author=None,
        title=None,
        topic=None,
        label=None,
        source=None,
        max_results=100,
    )


@_PATCH_MGR
def test_search_json_multiple_notes(mock_mgr, capsys):
    mock_mgr.return_value.search.return_value = [_make_note(1), _make_note(2)]
    search_notes(**_NO_FILTERS)
    output = json.loads(capsys.readouterr().out)
    assert [note['id'] for note in output] == ['doc:note_001', 'doc:note_002']


@_PATCH_MGR
def test_search_json_no_notes(mock_mgr, capsys):
    mock_mgr.return_value.search.return_value = []
    search_notes(**_NO_FILTERS)
    assert json.loads(capsys.readouterr().out) == []


@_PATCH_TIME
@_PATCH_MGR
def test_search_pretty_multiple_notes(mock_mgr, mock_time, capsys):  # noqa: ARG001
    mock_mgr.return_value.search.return_value = [_make_note(1), _make_note(2)]
    search_notes(**{**_NO_FILTERS, 'pretty': True})
    output = capsys.readouterr().out
    for index in (1, 2):
        assert f'Title: Note Title {index}' in output
        assert f'Source: Source {index}' in output
        assert f'Note: Note text {index}.' in output
    assert output.count('Published: 2026-01-01') == 2


@_PATCH_MGR
def test_search_pretty_no_notes(mock_mgr, capsys):
    mock_mgr.return_value.search.return_value = []
    search_notes(**{**_NO_FILTERS, 'pretty': True})
    assert capsys.readouterr().out == ''


@_PATCH_MGR
def test_search_error_raised(mock_mgr):
    mock_mgr.return_value.search.side_effect = AnalystNoteSearchError('500 Server Error')
    with pytest.raises(AnalystNoteSearchError, match='500 Server Error'):
        search_notes(**_NO_FILTERS)
