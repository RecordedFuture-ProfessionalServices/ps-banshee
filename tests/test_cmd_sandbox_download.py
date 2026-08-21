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

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from banshee.commands.cmd_sandbox import app

runner = CliRunner()


class TestCmdSandboxDownload:
    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_single_sample_with_yes(self, mock_dl, tmp_path):
        result = runner.invoke(app, ['download', 'id1', '--output-dir', str(tmp_path), '--yes'])
        assert result.exit_code == 0
        mock_dl.assert_called_once_with(['id1'], output_dir=Path(str(tmp_path)), workers=1)

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_multiple_samples(self, mock_dl, tmp_path):
        result = runner.invoke(app, ['download', 'id1', 'id2', 'id3', '-d', str(tmp_path), '-y'])
        assert result.exit_code == 0
        mock_dl.assert_called_once_with(
            ['id1', 'id2', 'id3'], output_dir=Path(str(tmp_path)), workers=1
        )

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_workers_flag(self, mock_dl, tmp_path):
        result = runner.invoke(
            app, ['download', 'id1', '-d', str(tmp_path), '-y', '--workers', '4']
        )
        assert result.exit_code == 0
        mock_dl.assert_called_once_with(['id1'], output_dir=Path(str(tmp_path)), workers=4)

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_missing_output_dir_rejected(self, mock_dl):
        result = runner.invoke(app, ['download', 'id1', '--yes'])
        assert result.exit_code != 0
        mock_dl.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_yes_skips_confirm(self, mock_dl, tmp_path):
        # No stdin input; --yes should bypass the confirm prompt entirely.
        result = runner.invoke(app, ['download', 'id1', '-d', str(tmp_path), '-y'])
        assert result.exit_code == 0
        mock_dl.assert_called_once()

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_workers_above_max_rejected(self, mock_dl, tmp_path):
        result = runner.invoke(app, ['download', 'id1', '-d', str(tmp_path), '-y', '-w', '17'])
        assert result.exit_code != 0
        mock_dl.assert_not_called()

    @patch('banshee.commands.cmd_sandbox.download_sandbox_samples')
    def test_workers_below_min_rejected(self, mock_dl, tmp_path):
        result = runner.invoke(app, ['download', 'id1', '-d', str(tmp_path), '-y', '-w', '0'])
        assert result.exit_code != 0
        mock_dl.assert_not_called()

    def test_download_help_available(self):
        result = runner.invoke(app, ['download', '--help'])
        assert result.exit_code == 0
        assert '--output-dir' in result.output
        assert '--yes' in result.output
        assert '--workers' in result.output
        assert 'infected' in result.output

    def test_sandbox_help_shows_download(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'download' in result.output

    def test_declines_confirm_aborts(self, tmp_path):
        with patch('banshee.commands.cmd_sandbox.download_sandbox_samples') as mock_dl:
            result = runner.invoke(app, ['download', 'id1', '-d', str(tmp_path)], input='n\n')
            assert result.exit_code != 0
            mock_dl.assert_not_called()
