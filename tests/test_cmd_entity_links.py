##################################### TERMS OF USE ###########################################
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

from unittest.mock import patch

from typer.testing import CliRunner

from banshee.commands.cmd_entity import app
from banshee.entity_match.constants import LinkSource

runner = CliRunner()

_DEFAULTS = {
    'entities': None,
    'entity_types': None,
    'sources': None,
    'sections': None,
    'timeframe': None,
    'events': None,
    'connected_entities': None,
    'per_entity_type': None,
    'search_scope': 'medium',
    'skip_enrichment': False,
    'pretty': False,
}


class TestCmdLinksSearch:
    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_no_entities(self, mock_search):
        result = runner.invoke(app, ['links'])
        assert result.exit_code == 2
        assert 'No entities provided.' in result.output
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_single_entity(self, mock_search):
        result = runner.invoke(app, ['links','I60vfZ'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'entities': ['I60vfZ']})

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_multiple_entities(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', 'QCwdoU'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'entities': ['I60vfZ', 'QCwdoU']})

    @patch('banshee.commands.cmd_entity.search_links')
    def test_invalid_entity_id(self, mock_search):
        result = runner.invoke(app, ['links', '192.168.1.1'])
        assert result.exit_code == 2
        mock_search.assert_not_called()
        assert 'Invalid entity ID: 192.168.1.1' in result.output

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_valid_and_invalid_entity_id(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', 'https://example.com'])
        assert result.exit_code == 2
        mock_search.assert_not_called()
        assert 'Invalid entity ID: https://example.com' in result.output

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_valid_entities_from_stdin(self, mock_search):
        result = runner.invoke(app, ['links'], input='I60vfZ QCwdoU')
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'entities': ['I60vfZ', 'QCwdoU']})

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_invalid_entities_from_stdin(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', 'https://example.com'])
        assert result.exit_code == 2
        mock_search.assert_not_called()
        assert 'Invalid entity ID: https://example.com' in result.output

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_small_scope(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--small'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'search_scope': 'small'}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_large_scope(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--large'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'search_scope': 'large'}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_small_large_scope(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--large', '--small'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_skip_enrichment(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--skip-enrichment'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'skip_enrichment': True}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_min_limit(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--limit', '1'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'per_entity_type': 1}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_max_limit(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--limit', '1000000'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'per_entity_type': 1000000}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_limit_out_of_range_low(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--limit', '0'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_limit_out_of_range_high(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--limit', '1000001'])
        assert result.exit_code == 2
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_limit_within_range(self, mock_search):
        result = runner.invoke(app, ['links', 'I60vfZ', '--limit', '67'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'entities': ['I60vfZ'], 'per_entity_type': 67}
        )

    @patch('banshee.commands.cmd_entity.search_links')
    def test_search_all_single_values(self, mock_search):
        result = runner.invoke(
            app,
            [
                'links',
                'I60vfZ',
                '-t',
                'type:Malware',
                '-s',
                'Technical',
                '-S',
                'Indicators and Detection Rules',
                '-T',
                '-1d',
                '-e',
                'type:MalwareAnalysis',
                '-c',
                'T1005',
                '-l',
                '64',
                '-p',
            ],
        )
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{
                **_DEFAULTS,
                'entities': ['I60vfZ'],
                'entity_types': ['type:Malware'],
                'sources': LinkSource.TECHNICAL,
                'sections': ['Indicators and Detection Rules'],
                'timeframe': '-1d',
                'events': ['type:MalwareAnalysis'],
                'connected_entities': ['T1005'],
                'per_entity_type': 64,
                'pretty': True,
            }
        )

    def test_search_help_available(self):
        result = runner.invoke(app, ['links', '--help'])
        assert result.exit_code == 0
        assert '--type' in result.output
        assert '--source' in result.output
        assert '--sections' in result.output
        assert '--timeframe' in result.output
        assert '--events' in result.output
        assert '--connected-entities' in result.output
        assert '--limit' in result.output
        assert '--small' in result.output
        assert '--large' in result.output
        assert '--skip-enrichment' in result.output
        assert '--pretty' in result.output
