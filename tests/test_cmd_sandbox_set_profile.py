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

_SAMPLE_ID = '260501-h4p7laawme'


class TestCmdSandboxSetProfile:
    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_auto_long_flag(self, mock_fn):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--auto'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_SAMPLE_ID, auto=True, picks=None, pretty=False)

    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_auto_short_flag(self, mock_fn):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '-a'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_SAMPLE_ID, auto=True, picks=None, pretty=False)

    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_single_pick(self, mock_fn):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--pick', 'file.exe:win10-x64'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(
            _SAMPLE_ID, auto=False, picks=['file.exe:win10-x64'], pretty=False
        )

    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_pick_is_repeatable(self, mock_fn):
        result = runner.invoke(
            app,
            [
                'set-profile',
                _SAMPLE_ID,
                '--pick',
                'file.exe:win10-x64',
                '--pick',
                'doc.docx:office365',
            ],
        )
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(
            _SAMPLE_ID,
            auto=False,
            picks=['file.exe:win10-x64', 'doc.docx:office365'],
            pretty=False,
        )

    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_pretty_long_flag(self, mock_fn):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--auto', '--pretty'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_SAMPLE_ID, auto=True, picks=None, pretty=True)

    @patch('banshee.commands.cmd_sandbox.set_sandbox_sample_profile')
    def test_pretty_short_flag(self, mock_fn):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--auto', '-p'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_SAMPLE_ID, auto=True, picks=None, pretty=True)

    def test_neither_auto_nor_pick_fails(self):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID])
        assert result.exit_code != 0

    def test_both_auto_and_pick_fails(self):
        result = runner.invoke(
            app, ['set-profile', _SAMPLE_ID, '--auto', '--pick', 'file.exe:win10-x64']
        )
        assert result.exit_code != 0

    def test_missing_sample_id_fails(self):
        result = runner.invoke(app, ['set-profile'])
        assert result.exit_code != 0

    def test_pick_missing_colon_fails(self):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--pick', 'nocolon'])
        assert result.exit_code != 0

    def test_pick_missing_file_fails(self):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--pick', ':win10-x64'])
        assert result.exit_code != 0

    def test_pick_missing_profile_fails(self):
        result = runner.invoke(app, ['set-profile', _SAMPLE_ID, '--pick', 'file.exe:'])
        assert result.exit_code != 0

    def test_help_shows_auto_option(self):
        result = runner.invoke(app, ['set-profile', '--help'])
        assert result.exit_code == 0
        assert '--auto' in result.output

    def test_help_shows_pick_option(self):
        result = runner.invoke(app, ['set-profile', '--help'])
        assert result.exit_code == 0
        assert '--pick' in result.output

    def test_help_shows_pretty_option(self):
        result = runner.invoke(app, ['set-profile', '--help'])
        assert result.exit_code == 0
        assert '--pretty' in result.output

    def test_set_profile_shows_in_sandbox_help(self):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'set-profile' in result.output
