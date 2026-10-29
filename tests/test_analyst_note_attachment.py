#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from pathlib import Path
from unittest.mock import patch

import pytest
from psengine.analyst_notes import AnalystNoteAttachmentError

from banshee.analyst_notes.note_attachment import fetch_note_attachment

_PATCH_MGR = patch('banshee.analyst_notes.note_attachment.AnalystNoteMgr')
_PATCH_SAVE = patch('banshee.analyst_notes.note_attachment.save_attachment')
_OUT = Path('out')


@_PATCH_MGR
@_PATCH_SAVE
def test_all_attachment_saved(mock_save, mock_mgr, capsys):
    mock_mgr.return_value.fetch_attachment.return_value = (b'data', 'pdf')
    fetch_note_attachment(['doc:doc_001', 'doc:doc_002'], _OUT)
    assert mock_save.call_count == 2
    mock_save.assert_any_call('doc:doc_001', b'data', 'pdf', _OUT)
    assert 'Saved 2 note attachments to disk.' in capsys.readouterr().out


@_PATCH_MGR
@_PATCH_SAVE
def test_attachment_1_of_2_saved(mock_save, mock_mgr, capsys):
    mock_mgr.return_value.fetch_attachment.side_effect = [
        (b'data', 'pdf'),
        AnalystNoteAttachmentError('502 Gateway Error'),
    ]
    with pytest.raises(SystemExit) as exc:
        fetch_note_attachment(['doc:doc_001', 'doc:doc_002'], _OUT)
    assert exc.value.code == 1
    mock_save.assert_called_once_with('doc:doc_001', b'data', 'pdf', _OUT)
    assert 'Warning: 1 out of 2' in capsys.readouterr().err


@_PATCH_MGR
@_PATCH_SAVE
def test_attachment_error(mock_save, mock_mgr, capsys):
    mock_mgr.return_value.fetch_attachment.side_effect = AnalystNoteAttachmentError(
        '502 Gateway Error'
    )
    with pytest.raises(SystemExit) as exc:
        fetch_note_attachment(['doc:doc_001'], _OUT)
    assert exc.value.code == 1
    mock_save.assert_not_called()
    captured = capsys.readouterr()
    assert 'No attachment found for "doc:doc_001"' in captured.out
    assert 'Warning: 0 out of 1' in captured.err


@pytest.mark.parametrize('result', [(None, None), (b'data', None), (None, 'pdf')])
@_PATCH_MGR
@_PATCH_SAVE
def test_attachment_found_incomplete(mock_save, mock_mgr, result):
    mock_mgr.return_value.fetch_attachment.return_value = result
    with pytest.raises(SystemExit) as exc:
        fetch_note_attachment(['doc:doc_001'], _OUT)
    assert exc.value.code == 1
    mock_save.assert_not_called()
