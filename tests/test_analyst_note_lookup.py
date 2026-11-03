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
from psengine.analyst_notes.errors import AnalystNoteLookupError

from banshee.analyst_notes.note_lookup import lookup_note

_NOTE_ID = 'doc:BVTpxNx'

_PATCH_MGR = patch('banshee.analyst_notes.note_lookup.AnalystNoteMgr')
_PATCH_TIME = patch('banshee.analyst_notes.note_lookup.format_time', return_value='2026-01-01')


def _make_note():
    note = MagicMock()
    note.id_ = _NOTE_ID
    note.attributes.title = 'Note Title'
    note.attributes.text = 'A note knows its a note.'
    note.source.name = 'Source of the Note.'
    note.json.return_value = {'id': _NOTE_ID, 'attributes': {'title': note.attributes.title}}
    return note


@_PATCH_MGR
def test_lookup_call_no_args(mock_mgr):
    mock_mgr.return_value.lookup.return_value = _make_note()
    lookup_note(_NOTE_ID, tagged_text=False, pretty=False)
    mock_mgr.return_value.lookup.assert_called_once_with(note_id=_NOTE_ID, tagged_text=False)


@_PATCH_MGR
def test_lookup_tagged_text(mock_mgr):
    mock_mgr.return_value.lookup.return_value = _make_note()
    lookup_note(_NOTE_ID, tagged_text=True, pretty=False)
    mock_mgr.return_value.lookup.assert_called_once_with(note_id=_NOTE_ID, tagged_text=True)


@_PATCH_MGR
def test_lookup_json_note_found(mock_mgr, capsys):
    mock_mgr.return_value.lookup.return_value = _make_note()
    lookup_note(_NOTE_ID, tagged_text=False, pretty=False)
    assert json.loads(capsys.readouterr().out)['id'] == _NOTE_ID


@_PATCH_MGR
def test_lookup_json_note_not_found(mock_mgr, capsys):
    mock_mgr.return_value.lookup.return_value = None
    lookup_note(_NOTE_ID, tagged_text=False, pretty=False)
    assert json.loads(capsys.readouterr().out) == []


@_PATCH_TIME
@_PATCH_MGR
def test_lookup_pretty_note_found(mock_mgr, mock_time, capsys):
    mock_mgr.return_value.lookup.return_value = _make_note()
    lookup_note(_NOTE_ID, tagged_text=False, pretty=True)
    mock_time.assert_called_once()
    output = capsys.readouterr().out
    assert 'Title: Note Title' in output
    assert 'Published: 2026-01-01' in output
    assert 'Source Name: Source of the Note.' in output
    assert 'Note: A note knows its a note.' in output


@_PATCH_MGR
def test_lookup_pretty_note_not_found(mock_mgr, capsys):
    mock_mgr.return_value.lookup.return_value = None
    lookup_note(_NOTE_ID, tagged_text=False, pretty=True)
    output = capsys.readouterr().out
    assert f'Unable to find note with ID "{_NOTE_ID}"' in output


@_PATCH_MGR
def test_lookup_error_raised(mock_mgr):
    mock_mgr.return_value.lookup.side_effect = AnalystNoteLookupError('404 Not Found')
    with pytest.raises(AnalystNoteLookupError):
        lookup_note(_NOTE_ID, tagged_text=False, pretty=False)
