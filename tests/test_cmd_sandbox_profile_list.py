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


class TestCmdSandboxProfileList:
    @patch('banshee.commands.cmd_sandbox.list_sandbox_profiles')
    def test_profile_list_default(self, mock_list):
        result = runner.invoke(app, ['profile', 'list'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(pretty=False)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_profiles')
    def test_profile_list_pretty_long_flag(self, mock_list):
        result = runner.invoke(app, ['profile', 'list', '--pretty'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(pretty=True)

    @patch('banshee.commands.cmd_sandbox.list_sandbox_profiles')
    def test_profile_list_pretty_short_flag(self, mock_list):
        result = runner.invoke(app, ['profile', 'list', '-p'])
        assert result.exit_code == 0
        mock_list.assert_called_once_with(pretty=True)

    def test_profile_list_help_available(self):
        result = runner.invoke(app, ['profile', 'list', '--help'])
        assert result.exit_code == 0
        assert '--pretty' in result.output

    def test_profile_subcommand_help(self):
        result = runner.invoke(app, ['profile', '--help'])
        assert result.exit_code == 0
        assert 'list' in result.output
