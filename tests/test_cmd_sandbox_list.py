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


class TestCmdSandboxList:
    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_defaults(self, mock_list):
        result = runner.invoke(app, ['list'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=20, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_subset_owned(self, mock_list):
        result = runner.invoke(app, ['list', '--subset', 'owned'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='owned', limit=20, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_subset_public_short_flag(self, mock_list):
        result = runner.invoke(app, ['list', '-s', 'public'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='public', limit=20, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_subset_case_insensitive(self, mock_list):
        result = runner.invoke(app, ['list', '--subset', 'OWNED'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='owned', limit=20, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_invalid_subset_rejected(self, mock_list):
        result = runner.invoke(app, ['list', '--subset', 'everything'])
        assert result.exit_code != 0
        assert 'everything' in result.output
        mock_list.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_limit_long_flag(self, mock_list):
        result = runner.invoke(app, ['list', '--limit', '5'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=5, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_limit_short_flag(self, mock_list):
        result = runner.invoke(app, ['list', '-l', '100'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=100, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_limit_below_one_rejected(self, mock_list):
        result = runner.invoke(app, ['list', '--limit', '0'])
        assert result.exit_code != 0
        mock_list.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_limit_at_max_accepted(self, mock_list):
        result = runner.invoke(app, ['list', '--limit', '4095'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=4095, pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_limit_above_max_rejected(self, mock_list):
        result = runner.invoke(app, ['list', '--limit', '4096'])
        assert result.exit_code != 0
        mock_list.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_pretty_long_flag(self, mock_list):
        result = runner.invoke(app, ['list', '--pretty'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=20, pretty=True)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_pretty_short_flag(self, mock_list):
        result = runner.invoke(app, ['list', '-p'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='org', limit=20, pretty=True)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_samples')
    def test_list_combined_options(self, mock_list):
        result = runner.invoke(app, ['list', '-s', 'owned', '-l', '3', '-p'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(subset='owned', limit=3, pretty=True)

    def test_list_help_available(self):
        result = runner.invoke(app, ['list', '--help'])
        assert result.exit_code == 0
        assert '--subset' in result.output
        assert '--limit' in result.output
        assert '--pretty' in result.output

    def test_sandbox_help_shows_list(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'list' in result.output
