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
    'title': 'A Note Title',
    'note_text': 'A Note for testing.',
    'topic': None,
    'context_entities': None,
    'note_entities': None,
    'validation_urls': None,
}


class TestCmdAnalystNotePublish:
    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_no_args(self, mock_publish):
        result = runner.invoke(app, ['publish'])
        assert result.exit_code == 2
        mock_publish.assert_not_called()
        assert "Missing argument 'TITLE'." in result.output

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_no_entities(self, mock_publish):
        result = runner.invoke(app, ['publish', 'A Note Title', 'A Note for testing.'])
        assert result.exit_code == 2
        mock_publish.assert_not_called()
        assert '--context_entities' in result.output
        assert '--note_entities' in result.output

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_note_withnote_entities(self, mock_publish):
        result = runner.invoke(
            app,
            [
                'publish',
                'A Note Title',
                'A Note for testing.',
                '--note_entities',
                'idn:example.com',
            ],
        )
        assert result.exit_code == 0
        mock_publish.assert_called_once_with(**{**_DEFAULTS, 'note_entities': ['idn:example.com']})

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_note_with_context_entities(self, mock_publish):
        result = runner.invoke(
            app,
            [
                'publish',
                'A Note Title',
                'A Note for testing.',
                '--context_entities',
                'idn:example.com',
            ],
        )
        assert result.exit_code == 0
        mock_publish.assert_called_once_with(
            **{**_DEFAULTS, 'context_entities': ['idn:example.com']}
        )

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_note_all_singular_options(self, mock_publish):
        result = runner.invoke(
            app,
            [
                'publish',
                'A Note Title',
                'A Note for testing.',
                '-t',
                'TXSFQ4',
                '-t',
                'ZjnoP0',
                '-e',
                'idn:example.com',
                '-c',
                'idn:example_2.com',
                '-v',
                'https://example.com',
            ],
        )
        assert result.exit_code == 0
        mock_publish.assert_called_once_with(
            **{
                **_DEFAULTS,
                'topic': ['TXSFQ4', 'ZjnoP0'],
                'note_entities': ['idn:example.com'],
                'context_entities': ['idn:example_2.com'],
                'validation_urls': ['https://example.com'],
            }
        )

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_note_text_from_stdin(self, mock_publish):
        result = runner.invoke(
            app, ['publish', 'A Note Title', '-e', 'idn:example.com'], input='Piped note text\n'
        )
        assert result.exit_code == 0
        mock_publish.assert_called_once_with(
            **{**_DEFAULTS, 'note_text': 'Piped note text', 'note_entities': ['idn:example.com']}
        )

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_note_text_arg_wins_over_stdin(self, mock_publish):
        result = runner.invoke(
            app,
            ['publish', 'A Note Title', 'From arg', '-e', 'idn:example.com'],
            input='From stdin',
        )
        assert result.exit_code == 0
        assert mock_publish.call_args.kwargs['note_text'] == 'From arg'

    @patch('banshee.commands.cmd_analyst_notes.publish_note')
    def test_publish_empty_stdin(self, mock_publish):
        result = runner.invoke(app, ['publish', 'A Note Title', '-e', 'idn:example.com'], input='')
        assert result.exit_code == 2
        mock_publish.assert_not_called()
        assert 'No note text supplied' in result.output

    def test_publish_help_available(self):
        result = runner.invoke(app, ['publish', '--help'])
        assert result.exit_code == 0
        assert 'title' in result.output
        assert 'note_text' in result.output
        assert '--topic' in result.output
        assert '--note_entities' in result.output
        assert '--context_entities' in result.output
        assert '--validation_urls' in result.output
        assert '--help' in result.output

    def test_analyst_notes_shows_publish(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'publish' in result.output
