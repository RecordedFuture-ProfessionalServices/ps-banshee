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

from typer.testing import CliRunner

from banshee.commands.cmd_analyst_notes import app

runner = CliRunner()

_DEFAULTS = {
    'tagged_text': False,
    'pretty': False,
}


class TestCmdAnalystNotesLookup:
    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_no_args(self, mock_lookup):
        result = runner.invoke(app, ['lookup'])
        assert result.exit_code == 2
        mock_lookup.assert_not_called()
        assert "Missing argument 'NOTE_ID'." in result.output

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_valid_id_with_valid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc:doc_001'])
        assert result.exit_code == 0
        mock_lookup.assert_called_once_with(**{**_DEFAULTS, 'note_id': 'doc:doc_001'})

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_invalid_id_with_valid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc:invalid_id'])
        assert result.exit_code == 2
        mock_lookup.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_valid_id_without_valid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc_001'])
        assert result.exit_code == 0
        mock_lookup.assert_called_once_with(**{**_DEFAULTS, 'note_id': 'doc:doc_001'})

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_invalid_id_without_valid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'invalid_id'])
        assert result.exit_code == 2
        mock_lookup.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_valid_id_with_invalid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'kevin:doc_001'])
        assert result.exit_code == 2
        mock_lookup.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_invalid_id_with_invalid_prefix(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'kevin:invalid_id'])
        assert result.exit_code == 2
        mock_lookup.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_tagged_text(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc_001', '--tagged_text'])
        assert result.exit_code == 0
        mock_lookup.assert_called_once_with(
            **{**_DEFAULTS, 'note_id': 'doc:doc_001', 'tagged_text': True}
        )

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_pretty(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc_001', '--pretty'])
        assert result.exit_code == 0
        mock_lookup.assert_called_once_with(
            **{**_DEFAULTS, 'note_id': 'doc:doc_001', 'pretty': True}
        )

    @patch('banshee.commands.cmd_analyst_notes.lookup_note')
    def test_lookup_all_single_values(self, mock_lookup):
        result = runner.invoke(app, ['lookup', 'doc_001', '-t', '-p'])
        assert result.exit_code == 0
        mock_lookup.assert_called_once_with(
            **{
                **_DEFAULTS,
                'note_id': 'doc:doc_001',
                'tagged_text': True,
                'pretty': True,
            }
        )

    def test_lookup_help_available(self):
        result = runner.invoke(app, ['lookup', '--help'])
        assert result.exit_code == 0
        assert 'note_id' in result.output
        assert '--tagged_text' in result.output
        assert '--pretty' in result.output

    def test_analyst_notes_shows_lookup(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'lookup' in result.output
