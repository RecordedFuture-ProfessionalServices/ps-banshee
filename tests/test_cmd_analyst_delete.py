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


class TestCmdAnalystNoteDelete:
    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_no_args(self, mock_delete):
        result = runner.invoke(app, ['delete'])
        assert result.exit_code == 2
        mock_delete.assert_not_called()
        assert "Missing argument 'NOTE_ID'." in result.output

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_valid_id_with_valid_prefix(self, mock_delete):
        result = runner.invoke(app, ['delete', 'doc:doc_001'])
        assert result.exit_code == 0
        mock_delete.assert_called_once_with('doc:doc_001')

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_invalid_id_with_valid_prefix(self, mock_delete):
        result = runner.invoke(app, ['delete', 'doc:invalid_id'])
        assert result.exit_code == 2
        mock_delete.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_valid_id_with_invalid_prefix(self, mock_delete):
        result = runner.invoke(app, ['delete', 'car:doc_001'])
        assert result.exit_code == 2
        mock_delete.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_invalid_id_with_invalid_prefix(self, mock_delete):
        result = runner.invoke(app, ['delete', 'car:invalid_id'])
        assert result.exit_code == 2
        mock_delete.assert_not_called()
        assert "Invalid value for 'NOTE_ID': Note ID" in result.output

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_invalid_id_without_prefix(self, mock_delete):
        result = runner.invoke(app, ['delete', 'doc_001'])
        assert result.exit_code == 0
        mock_delete.assert_called_once_with('doc:doc_001')

    @patch('banshee.commands.cmd_analyst_notes.delete_note')
    def test_delete_too_many_ids(self, mock_delete):
        result = runner.invoke(app, ['delete', 'doc:doc_001', 'doc:doc_002'])
        assert result.exit_code == 2
        mock_delete.assert_not_called()

    def test_lookup_help_available(self):
        result = runner.invoke(app, ['delete', '--help'])
        assert result.exit_code == 0
        assert 'note_id' in result.output

    def test_analyst_notes_shows_lookup(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'lookup' in result.output
