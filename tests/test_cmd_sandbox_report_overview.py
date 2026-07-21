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


class TestCmdSandboxReportOverview:
    @patch('banshee.commands.cmd_sandbox.fetch_overview_report')
    def test_overview_default(self, mock_fetch):
        result = runner.invoke(app, ['report', 'overview', '251114-py23jaavtp'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('251114-py23jaavtp', pretty=False, wait=False)

    @patch('banshee.commands.cmd_sandbox.fetch_overview_report')
    def test_overview_pretty_long_flag(self, mock_fetch):
        result = runner.invoke(app, ['report', 'overview', '251114-py23jaavtp', '--pretty'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('251114-py23jaavtp', pretty=True, wait=False)

    @patch('banshee.commands.cmd_sandbox.fetch_overview_report')
    def test_overview_pretty_short_flag(self, mock_fetch):
        result = runner.invoke(app, ['report', 'overview', '251114-py23jaavtp', '-p'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('251114-py23jaavtp', pretty=True, wait=False)

    @patch('banshee.commands.cmd_sandbox.fetch_overview_report')
    def test_overview_wait_long_flag(self, mock_fetch):
        result = runner.invoke(app, ['report', 'overview', '251114-py23jaavtp', '--wait'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('251114-py23jaavtp', pretty=False, wait=True)

    @patch('banshee.commands.cmd_sandbox.fetch_overview_report')
    def test_overview_wait_short_flag(self, mock_fetch):
        result = runner.invoke(app, ['report', 'overview', '251114-py23jaavtp', '-w'])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with('251114-py23jaavtp', pretty=False, wait=True)

    def test_overview_help_available(self):
        result = runner.invoke(app, ['report', 'overview', '--help'])
        assert result.exit_code == 0
        assert '--pretty' in result.output
        assert '--wait' in result.output

    def test_report_subcommand_shows_overview(self):
        result = runner.invoke(app, ['report', '--help'])
        assert result.exit_code == 0
        assert 'overview' in result.output

    def test_overview_missing_argument_fails(self):
        result = runner.invoke(app, ['report', 'overview'])
        assert result.exit_code != 0
