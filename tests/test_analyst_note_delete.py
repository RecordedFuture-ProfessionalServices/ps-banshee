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

from unittest.mock import patch

import pytest
from psengine.analyst_notes import AnalystNoteDeleteError

from banshee.analyst_notes.note_delete import delete_note

_PATCH_MGR = patch('banshee.analyst_notes.note_delete.AnalystNoteMgr')


@_PATCH_MGR
def test_delete_note_success(mock_mgr, capsys):
    mock_mgr.return_value.delete.return_value = True
    delete_note('doc:BVTpxNx')
    output = capsys.readouterr().out
    assert 'Deleted Note: doc:BVTpxNx' in output


@_PATCH_MGR
def test_delete_note_unsuccess(mock_mgr, capsys):
    mock_mgr.return_value.delete.return_value = False
    delete_note('doc:1234567')
    output = capsys.readouterr().out
    assert 'Unable to Delete Note: doc:1234567' in output


@_PATCH_MGR
def test_delete_note_error(mock_mgr):
    mock_mgr.return_value.delete.side_effect = AnalystNoteDeleteError('502 Gateway Error')
    with pytest.raises(AnalystNoteDeleteError):
        delete_note('doc:BVTpxNx')
