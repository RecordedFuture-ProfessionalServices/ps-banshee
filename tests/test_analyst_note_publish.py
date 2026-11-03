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

from unittest.mock import MagicMock, patch

import pytest
from psengine.analyst_notes import AnalystNotePublishError

from banshee.analyst_notes.note_publish import publish_note

_PATCH_MGR = patch('banshee.analyst_notes.note_publish.AnalystNoteMgr')

_ARGS = {
    'title': 'A Note Title',
    'note_text': 'A Note for testing.',
    'topic': ['TXSFQ4'],
    'context_entities': ['idn:example_2.com'],
    'note_entities': ['idn:example.com'],
    'validation_urls': ['https://example.com'],
}


@_PATCH_MGR
def test_publish_note_success(mock_mgr, capsys):
    mock_mgr.return_value.publish.return_value = MagicMock(note_id='doc:BVTpxNx')
    publish_note(**_ARGS)
    assert 'Note published: doc:BVTpxNx' in capsys.readouterr().out


@_PATCH_MGR
def test_publish_note_passes_arguments_to_manager(mock_mgr):
    mock_mgr.return_value.publish.return_value = MagicMock(note_id='doc:BVTpxNx')
    publish_note(**_ARGS)
    mock_mgr.return_value.publish.assert_called_once_with(
        title='A Note Title',
        text='A Note for testing.',
        topic=['TXSFQ4'],
        context_entities=['idn:example_2.com'],
        note_entities=['idn:example.com'],
        validation_urls=['https://example.com'],
    )


@_PATCH_MGR
def test_publish_note_optional_args_none(mock_mgr):
    mock_mgr.return_value.publish.return_value = MagicMock(note_id='doc:BVTpxNx')
    publish_note(
        title='A Note Title',
        note_text='A Note for testing.',
        topic=None,
        context_entities=None,
        note_entities=['idn:example.com'],
        validation_urls=None,
    )
    kwargs = mock_mgr.return_value.publish.call_args.kwargs
    assert kwargs['topic'] is None
    assert kwargs['context_entities'] is None
    assert kwargs['validation_urls'] is None


@_PATCH_MGR
def test_publish_note_error_propagates(mock_mgr, capsys):
    mock_mgr.return_value.publish.side_effect = AnalystNotePublishError('502 Gateway Error')
    with pytest.raises(AnalystNotePublishError, match='502 Gateway Error'):
        publish_note(**_ARGS)
    assert 'Note published' not in capsys.readouterr().out
