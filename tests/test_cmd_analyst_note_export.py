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

_SEARCH_OUTPUT = json.dumps([{'id': 'doc:doc_001'}, {'id': 'doc:doc_002'}])


class TestCmdAnalystNoteExport:
    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_no_stdin(self, mock_export):
        result = runner.invoke(app, ['export'])
        assert result.exit_code == 2
        mock_export.assert_not_called()
        assert 'No input received' in result.output

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_valid_stdin(self, mock_export):
        result = runner.invoke(app, ['export'], input=_SEARCH_OUTPUT)
        assert result.exit_code == 0
        mock_export.assert_called_once_with(note_ids=['doc:doc_001', 'doc:doc_002'], csv_flag=False)

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_csv_short_flag(self, mock_export):
        result = runner.invoke(app, ['export', '-c'], input=_SEARCH_OUTPUT)
        assert result.exit_code == 0
        mock_export.assert_called_once_with(note_ids=['doc:doc_001', 'doc:doc_002'], csv_flag=True)

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_csv_long_flag(self, mock_export):
        result = runner.invoke(app, ['export', '--csv'], input=_SEARCH_OUTPUT)
        assert result.exit_code == 0
        assert mock_export.call_args.kwargs['csv_flag'] is True

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_ignores_extra_note_fields(self, mock_export):
        piped = json.dumps([{'id': 'doc:doc_001', 'title': 'A Title', 'source': 'x'}])
        result = runner.invoke(app, ['export'], input=piped)
        assert result.exit_code == 0
        mock_export.assert_called_once_with(note_ids=['doc:doc_001'], csv_flag=False)

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_malformed_json(self, mock_export):
        result = runner.invoke(app, ['export'], input='[not json')
        assert result.exit_code == 2
        mock_export.assert_not_called()
        assert 'Malformed input' in result.output

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_json_not_a_list(self, mock_export):
        result = runner.invoke(app, ['export'], input=json.dumps({'id': 'doc:doc_001'}))
        assert result.exit_code == 2
        mock_export.assert_not_called()
        assert 'expected a JSON array' in result.output

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_note_missing_id(self, mock_export):
        result = runner.invoke(app, ['export'], input=json.dumps([{'title': 'No id'}]))
        assert result.exit_code == 2
        mock_export.assert_not_called()
        assert 'Malformed input' in result.output

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_invalid_note_id(self, mock_export):
        result = runner.invoke(app, ['export'], input=json.dumps([{'id': 'car:invalid_id'}]))
        assert result.exit_code == 2
        mock_export.assert_not_called()
        assert 'Note ID' in result.output

    @patch('banshee.commands.cmd_analyst_notes.export_notes')
    def test_export_one_invalid_id_among_valid(self, mock_export):
        piped = json.dumps([{'id': 'doc:doc_001'}, {'id': 'bad'}])
        result = runner.invoke(app, ['export'], input=piped)
        assert result.exit_code == 2
        mock_export.assert_not_called()

    def test_export_help_available(self):
        result = runner.invoke(app, ['export', '--help'])
        assert result.exit_code == 0
        assert '--csv' in result.output

    def test_analyst_notes_shows_export(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'export' in result.output
