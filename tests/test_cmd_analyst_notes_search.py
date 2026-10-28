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
    'published': '-1d',
    'entity': None,
    'author': None,
    'title': None,
    'topic': None,
    'label': None,
    'source': None,
    'max_results': 100,
    'pretty': False,
}


class TestCmdAnalystNotesSearch:
    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_published_with_prefix(self, mock_search):
        result = runner.invoke(app, ['search', '--published', '-2d'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'published': '-2d'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_published_without_prefix(self, mock_search):
        result = runner.invoke(app, ['search', '-P', '2y'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'published': '-2y'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_entity(self, mock_search):
        result = runner.invoke(app, ['search', '--entity', 'TestEntity'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'entity': 'TestEntity'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_author(self, mock_search):
        result = runner.invoke(app, ['search', '--author', 'TestAuthor'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'author': 'TestAuthor'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_title(self, mock_search):
        result = runner.invoke(app, ['search', '--title', 'Test Title'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'title': 'Test Title'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_topic_repeatable(self, mock_search):
        result = runner.invoke(app, ['search', '--topic', 'TestTopic_1', '-T', 'TestTopic_2'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'topic': ['TestTopic_1', 'TestTopic_2']}
        )

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_label(self, mock_search):
        result = runner.invoke(app, ['search', '--label', 'TestLabel'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'label': 'TestLabel'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_source(self, mock_search):
        result = runner.invoke(app, ['search', '--source', 'TestSource'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'source': 'TestSource'})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_valid(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', '28'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'max_results': 28})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_invalid_low(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', '0'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_invalid_high(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', '1000000'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_valid_low(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', '1'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'max_results': 1})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_valid_high(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', '1000'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'max_results': 1000})

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_max_results_non_integer(self, mock_search):
        result = runner.invoke(app, ['search', '--max_results', 'kevin'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_analyst_notes.search_notes')
    def test_search_all_single_values(self, mock_search):
        result = runner.invoke(
            app,
            [
                'search',
                '-e',
                'e',
                '-a',
                'a',
                '-t',
                't',
                '-l',
                'l',
                '-s',
                's',
                '-r',
                '76',
                '-p',
            ],
        )
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{
                **_DEFAULTS,
                'entity': 'e',
                'author': 'a',
                'title': 't',
                'label': 'l',
                'source': 's',
                'max_results': 76,
                'pretty': True,
            }
        )

    def test_search_help_available(self):
        result = runner.invoke(app, ['search', '--help'])
        assert result.exit_code == 0
        assert '--published' in result.output
        assert '--entity' in result.output
        assert '--author' in result.output
        assert '--title' in result.output
        assert '--topic' in result.output
        assert '--label' in result.output
        assert '--source' in result.output
        assert '--max_results' in result.output
        assert '--pretty' in result.output

    def test_analyst_notes_shows_search(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'search' in result.output
