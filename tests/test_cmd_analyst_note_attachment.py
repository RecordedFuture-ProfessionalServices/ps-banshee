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

import json
from unittest.mock import patch

from typer.testing import CliRunner

from banshee.commands.cmd_analyst_notes import app

runner = CliRunner()


class TestCmdNoteAttachment:
    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_no_args(self, mock_fetch):
        result = runner.invoke(app, ['attachment'])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()
        assert '--output-dir' in result.output

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_missing_output_dir(self, mock_fetch):
        result = runner.invoke(app, ['attachment', 'doc:doc_001'])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()
        assert '--output-dir' in result.output

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_valid_id(self, mock_fetch, tmp_path):
        result = runner.invoke(app, ['attachment', 'doc:doc_001', '-d', str(tmp_path)])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(note_ids=['doc:doc_001'], output_dir=tmp_path)

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_multiple_valid_ids(self, mock_fetch, tmp_path):
        result = runner.invoke(
            app, ['attachment', 'doc:doc_001', 'doc:doc_002', '--output-dir', str(tmp_path)]
        )
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(
            note_ids=['doc:doc_001', 'doc:doc_002'], output_dir=tmp_path
        )

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_invalid_id(self, mock_fetch, tmp_path):
        result = runner.invoke(app, ['attachment', 'car:invalid_id', '-d', str(tmp_path)])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()
        assert 'Note ID' in result.output

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_one_valid_one_invalid_id(self, mock_fetch, tmp_path):
        result = runner.invoke(app, ['attachment', 'doc:doc_001', 'bad', '-d', str(tmp_path)])
        assert result.exit_code == 2
        mock_fetch.assert_not_called()

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_valid_ids_from_stdin(self, mock_fetch, tmp_path):
        result = runner.invoke(
            app, ['attachment', '-d', str(tmp_path)], input='doc:doc_001 doc:doc_002\n'
        )
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(
            note_ids=['doc:doc_001', 'doc:doc_002'], output_dir=tmp_path
        )

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_from_search_json_from_stdin(self, mock_fetch, tmp_path):
        piped = json.dumps([{'id': 'doc:doc_001'}, {'id': 'doc:doc_002'}])
        result = runner.invoke(app, ['attachment', '-d', str(tmp_path)], input=piped)
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with(
            note_ids=['doc:doc_001', 'doc:doc_002'], output_dir=tmp_path
        )

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_malformed_json_from_stdin(self, mock_fetch, tmp_path):
        result = runner.invoke(app, ['attachment', '-d', str(tmp_path)], input='[not json')
        assert result.exit_code == 2
        mock_fetch.assert_not_called()
        assert 'Malformed input' in result.output

    @patch('banshee.commands.cmd_analyst_notes.fetch_note_attachment')
    def test_attachment_empty_stdin(self, mock_fetch, tmp_path):
        result = runner.invoke(app, ['attachment', '-d', str(tmp_path)], input='')
        assert result.exit_code == 2
        mock_fetch.assert_not_called()
        assert 'No Note IDs supplied' in result.output

    def test_attachment_help_available(self):
        result = runner.invoke(app, ['attachment', '--help'])
        assert result.exit_code == 0
        assert 'output-dir' in result.output

    def test_analyst_notes_shows_attachment(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'attachment' in result.output
