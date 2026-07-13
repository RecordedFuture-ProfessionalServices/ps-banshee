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

PATCH_TARGET = 'banshee.commands.cmd_sandbox.create_sandbox_profile'

_REQUIRED = ['-n', 'fresh', '-T', 'os:windows10-2004-x64', '-t', '120']


class TestCmdSandboxProfileCreatePassthrough:
    @patch(PATCH_TARGET)
    def test_required_only(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', *_REQUIRED])
        assert result.exit_code == 0
        mock_create.assert_called_once_with(
            name='fresh',
            tags=['os:windows10-2004-x64'],
            timeout=120,
            network=None,
            geolocation=None,
            browser=None,
            pretty=False,
        )

    @patch(PATCH_TARGET)
    def test_all_fields_long_flags(self, mock_create):
        result = runner.invoke(
            app,
            [
                'profile',
                'create',
                '--name',
                'fresh',
                '--tags',
                'os:windows10-2004-x64',
                '--tags',
                'locale:en-us',
                '--timeout',
                '300',
                '--network',
                'vpn',
                '--geolocation',
                'se',
                '--geolocation',
                'us',
                '--browser',
                'firefox',
                '--pretty',
            ],
        )
        assert result.exit_code == 0
        mock_create.assert_called_once_with(
            name='fresh',
            tags=['os:windows10-2004-x64', 'locale:en-us'],
            timeout=300,
            network='vpn',
            geolocation=['se', 'us'],
            browser='firefox',
            pretty=True,
        )

    @patch(PATCH_TARGET)
    def test_short_flags(self, mock_create):
        result = runner.invoke(
            app,
            ['profile', 'create', *_REQUIRED, '-N', 'internet', '-b', 'chrome', '-p'],
        )
        assert result.exit_code == 0
        kwargs = mock_create.call_args.kwargs
        assert kwargs['network'] == 'internet'
        assert kwargs['browser'] == 'chrome'
        assert kwargs['pretty'] is True

    @patch(PATCH_TARGET)
    def test_network_case_insensitive(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', *_REQUIRED, '-N', 'VPN'])
        assert result.exit_code == 0
        assert mock_create.call_args.kwargs['network'] == 'vpn'

    @patch(PATCH_TARGET)
    def test_geolocation_with_vpn_ok(self, mock_create):
        result = runner.invoke(
            app, ['profile', 'create', *_REQUIRED, '-N', 'vpn', '--geolocation', 'se']
        )
        assert result.exit_code == 0
        assert mock_create.call_args.kwargs['geolocation'] == ['se']


class TestCmdSandboxProfileCreateValidation:
    @patch(PATCH_TARGET)
    def test_missing_name_fails(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', '-T', 'os:windows7-x64', '-t', '120'])
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_missing_tags_fails(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', '-n', 'fresh', '-t', '120'])
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_missing_timeout_fails(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', '-n', 'fresh', '-T', 'os:windows7-x64'])
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_timeout_zero_rejected(self, mock_create):
        result = runner.invoke(
            app, ['profile', 'create', '-n', 'fresh', '-T', 'os:windows7-x64', '-t', '0']
        )
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_timeout_over_max_rejected(self, mock_create):
        result = runner.invoke(
            app, ['profile', 'create', '-n', 'fresh', '-T', 'os:windows7-x64', '-t', '3601']
        )
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_geolocation_without_network_fails(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', *_REQUIRED, '--geolocation', 'se'])
        assert result.exit_code != 0
        assert 'vpn' in result.output.lower()
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_geolocation_with_non_vpn_network_fails(self, mock_create):
        result = runner.invoke(
            app, ['profile', 'create', *_REQUIRED, '-N', 'internet', '--geolocation', 'se']
        )
        assert result.exit_code != 0
        assert 'vpn' in result.output.lower()
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_empty_name_rejected(self, mock_create):
        result = runner.invoke(
            app, ['profile', 'create', '-n', '', '-T', 'os:windows7-x64', '-t', '120']
        )
        assert result.exit_code != 0
        assert 'empty' in result.output.lower()
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_empty_tag_value_rejected(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', '-n', 'fresh', '-T', '', '-t', '120'])
        assert result.exit_code != 0
        assert 'empty' in result.output.lower()
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_invalid_network_value(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', *_REQUIRED, '-N', 'wifi'])
        assert result.exit_code != 0
        mock_create.assert_not_called()

    @patch(PATCH_TARGET)
    def test_invalid_browser_value(self, mock_create):
        result = runner.invoke(app, ['profile', 'create', *_REQUIRED, '-b', 'safari'])
        assert result.exit_code != 0
        mock_create.assert_not_called()


class TestCmdSandboxProfileCreateHelp:
    def test_help_available(self):
        result = runner.invoke(app, ['profile', 'create', '--help'])
        assert result.exit_code == 0
        assert '--name' in result.output
        assert '--tags' in result.output
        assert '--timeout' in result.output

    def test_help_lists_browser_choices(self):
        result = runner.invoke(app, ['profile', 'create', '--help'])
        assert result.exit_code == 0
        assert 'chrome' in result.output
        assert 'firefox' in result.output

    def test_profile_subcommand_shows_create(self):
        result = runner.invoke(app, ['profile', '--help'])
        assert result.exit_code == 0
        assert 'create' in result.output
