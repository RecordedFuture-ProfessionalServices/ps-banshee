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


class TestCmdSandboxProfileDelete:
    @patch('banshee.commands.cmd_sandbox.delete_sandbox_profile')
    def test_delete_with_yes_long_flag(self, mock_delete):
        result = runner.invoke(app, ['profile', 'delete', 'w7-long', '--yes'])
        assert result.exit_code == 0
        mock_delete.assert_called_once_with('w7-long')

    @patch('banshee.commands.cmd_sandbox.delete_sandbox_profile')
    def test_delete_with_yes_short_flag(self, mock_delete):
        result = runner.invoke(app, ['profile', 'delete', 'w7-long', '-y'])
        assert result.exit_code == 0
        mock_delete.assert_called_once_with('w7-long')

    @patch('banshee.commands.cmd_sandbox.delete_sandbox_profile')
    def test_delete_prompts_and_proceeds_on_confirm(self, mock_delete):
        result = runner.invoke(app, ['profile', 'delete', 'w7-long'], input='y\n')
        assert result.exit_code == 0
        mock_delete.assert_called_once_with('w7-long')

    @patch('banshee.commands.cmd_sandbox.delete_sandbox_profile')
    def test_delete_prompts_and_aborts_on_decline(self, mock_delete):
        result = runner.invoke(app, ['profile', 'delete', 'w7-long'], input='n\n')
        assert result.exit_code != 0
        mock_delete.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.delete_sandbox_profile')
    def test_delete_aborts_on_eof_without_yes(self, mock_delete):
        """Non-interactive use without --yes must abort, not hang or delete."""
        result = runner.invoke(app, ['profile', 'delete', 'w7-long'])
        assert result.exit_code != 0
        mock_delete.assert_not_called()

    def test_delete_help_available(self):
        result = runner.invoke(app, ['profile', 'delete', '--help'])
        assert result.exit_code == 0
        assert '--yes' in result.output

    def test_profile_subcommand_shows_delete(self):
        result = runner.invoke(app, ['profile', '--help'])
        assert result.exit_code == 0
        assert 'delete' in result.output

    def test_delete_missing_argument_fails(self):
        result = runner.invoke(app, ['profile', 'delete'])
        assert result.exit_code != 0
