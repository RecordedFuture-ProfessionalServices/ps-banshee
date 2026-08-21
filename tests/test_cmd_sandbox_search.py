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

from banshee.commands.cmd_sandbox import app

runner = CliRunner()


_DEFAULTS = {
    'file_hash': None,
    'family': None,
    'tag': None,
    'botnet': None,
    'wallet': None,
    'ip': None,
    'domain': None,
    'url': None,
    'from_date': None,
    'to_date': None,
    'query': None,
    'limit': 50,
    'pretty': False,
}


class TestCmdSandboxSearch:
    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_by_hash(self, mock_search):
        result = runner.invoke(app, ['search', '--hash', 'abc123'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'file_hash': 'abc123'})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_by_family(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet'})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_tag_repeatable(self, mock_search):
        result = runner.invoke(app, ['search', '--tag', 'ransomware', '-T', 'persistence'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'tag': ['ransomware', 'persistence']})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_combined_ip_and_domain(self, mock_search):
        result = runner.invoke(app, ['search', '--ip', '1.2.3.4', '--domain', 'evil.example'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{**_DEFAULTS, 'ip': '1.2.3.4', 'domain': 'evil.example'}
        )

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_raw_query_long_flag(self, mock_search):
        result = runner.invoke(app, ['search', '--query', 'NOT family:emotet'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'query': 'NOT family:emotet'})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_raw_query_short_flag(self, mock_search):
        result = runner.invoke(app, ['search', '-q', 'NOT family:emotet'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'query': 'NOT family:emotet'})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_from_and_to_date(self, mock_search):
        result = runner.invoke(
            app,
            ['search', '--from-date', '2026-07-01', '--to-date', '2026-07-31', '--family', 'vidar'],
        )
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{
                **_DEFAULTS,
                'family': 'vidar',
                'from_date': '2026-07-01',
                'to_date': '2026-07-31',
            }
        )

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_all_single_value_filters(self, mock_search):
        result = runner.invoke(
            app,
            [
                'search',
                '--hash',
                'h',
                '--family',
                'f',
                '--botnet',
                'b',
                '--wallet',
                'w',
                '--ip',
                'i',
                '--domain',
                'd',
                '--url',
                'u',
            ],
        )
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            **{
                **_DEFAULTS,
                'file_hash': 'h',
                'family': 'f',
                'botnet': 'b',
                'wallet': 'w',
                'ip': 'i',
                'domain': 'd',
                'url': 'u',
            }
        )

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_limit_long_flag(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '--limit', '100'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet', 'limit': 100})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_limit_short_flag(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '-l', '10'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet', 'limit': 10})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_limit_below_one_rejected(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '--limit', '0'])
        assert result.exit_code != 0
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_limit_at_max_accepted(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '--limit', '200'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet', 'limit': 200})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_limit_above_max_rejected(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '--limit', '201'])
        assert result.exit_code != 0
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_pretty_long_flag(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '--pretty'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet', 'pretty': True})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_pretty_short_flag(self, mock_search):
        result = runner.invoke(app, ['search', '--family', 'emotet', '-p'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'family': 'emotet', 'pretty': True})

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_no_filters_rejected(self, mock_search):
        result = runner.invoke(app, ['search'])
        assert result.exit_code != 0
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_empty_filter_rejected(self, mock_search):
        result = runner.invoke(app, ['search', '--family', ''])
        assert result.exit_code != 0
        mock_search.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.search_sandbox_samples')
    def test_search_from_date_alone_is_sufficient(self, mock_search):
        result = runner.invoke(app, ['search', '--from-date', '2026-07-01'])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(**{**_DEFAULTS, 'from_date': '2026-07-01'})

    def test_search_help_available(self):
        result = runner.invoke(app, ['search', '--help'])
        assert result.exit_code == 0
        assert '--hash' in result.output
        assert '--family' in result.output
        assert '--tag' in result.output
        assert '--botnet' in result.output
        assert '--wallet' in result.output
        assert '--ip' in result.output
        assert '--domain' in result.output
        assert '--url' in result.output
        assert '--from-date' in result.output
        assert '--to-date' in result.output
        assert '--query' in result.output
        assert '--limit' in result.output
        assert '--pretty' in result.output

    def test_sandbox_help_shows_search(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'search' in result.output
