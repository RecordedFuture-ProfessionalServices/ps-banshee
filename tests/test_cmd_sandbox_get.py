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


class TestCmdSandboxGet:
    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_sample_summary')
    def test_get_default(self, mock_fetch):
        result = runner.invoke(app, ['get', '260501-h4p7laawme'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('260501-h4p7laawme', pretty=False)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_sample_summary')
    def test_get_pretty_long_flag(self, mock_fetch):
        result = runner.invoke(app, ['get', '260501-h4p7laawme', '--pretty'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('260501-h4p7laawme', pretty=True)

    @patch('banshee.commands.cmd_sandbox.fetch_sandbox_sample_summary')
    def test_get_pretty_short_flag(self, mock_fetch):
        result = runner.invoke(app, ['get', '260501-h4p7laawme', '-p'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('260501-h4p7laawme', pretty=True)

    def test_get_help_available(self):
        result = runner.invoke(app, ['get', '--help'])
        assert result.exit_code == 0
        assert '--pretty' in result.output

    def test_sandbox_help_shows_get(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'get' in result.output

    def test_get_missing_argument_fails(self):
        result = runner.invoke(app, ['get'])
        assert result.exit_code != 0
