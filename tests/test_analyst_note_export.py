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
from psengine.analyst_notes import AnalystNoteLookupError

from banshee.analyst_notes.note_export import export_notes

_PATCH_MGR = patch('banshee.analyst_notes.note_export.AnalystNoteMgr')
_PATCH_CSV = patch('banshee.analyst_notes.note_export.format_as_csv')
_PATCH_JSON = patch('banshee.analyst_notes.note_export.print_json')

_IDS = ['doc:doc_001', 'doc:doc_002']


@_PATCH_MGR
@_PATCH_CSV
def test_export_notes_csv(mock_csv, mock_mgr):
    notes = [MagicMock(), MagicMock()]
    mock_mgr.return_value.lookup.side_effect = notes
    export_notes(_IDS, csv_flag=True)
    mock_csv.assert_called_once_with(notes)


@_PATCH_MGR
@_PATCH_JSON
def test_export_notes_json(mock_print_json, mock_mgr):
    notes = [MagicMock(), MagicMock()]
    notes[0].json.return_value = {'id': 'doc:doc_001'}
    notes[1].json.return_value = {'id': 'doc:doc_002'}
    mock_mgr.return_value.lookup.side_effect = notes
    export_notes(_IDS, csv_flag=False)
    mock_print_json.assert_called_once()
    printed = json.loads(mock_print_json.call_args.args[0])
    assert printed == [{'id': 'doc:doc_001'}, {'id': 'doc:doc_002'}]


@_PATCH_MGR
def test_export_notes_looks_up_each_id(mock_mgr):
    mock_mgr.return_value.lookup.return_value = MagicMock()
    export_notes(_IDS, csv_flag=True)
    assert mock_mgr.return_value.lookup.call_count == 2
    mock_mgr.return_value.lookup.assert_any_call('doc:doc_001')
    mock_mgr.return_value.lookup.assert_any_call('doc:doc_002')


@_PATCH_MGR
@_PATCH_CSV
def test_export_notes_lookup_error(mock_csv, mock_mgr):
    mock_mgr.return_value.lookup.side_effect = AnalystNoteLookupError('404 Not Found')
    with pytest.raises(AnalystNoteLookupError):
        export_notes(_IDS, csv_flag=True)
    mock_csv.assert_not_called()
