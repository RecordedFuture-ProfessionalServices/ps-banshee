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

PATCH_TARGET = 'banshee.commands.cmd_sandbox.update_sandbox_profile'


class TestCmdSandboxProfileUpdatePassthrough:
    @patch(PATCH_TARGET)
    def test_name_only(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-n', 'ernie-v2'])
        assert result.exit_code == 0
        mock_update.assert_called_once_with(
            'ernie',
            name='ernie-v2',
            tags=None,
            timeout=None,
            network=None,
            geolocation=None,
            browser=None,
            unset=None,
            pretty=False,
        )

    @patch(PATCH_TARGET)
    def test_all_fields(self, mock_update):
        result = runner.invoke(
            app,
            [
                'profile',
                'update',
                'ernie',
                '--name',
                'ernie-v2',
                '--tags',
                'os:windows10-2004-x64',
                '--tags',
                'locale:en-us',
                '--timeout',
                '300',
                '--network',
                'vpn',
                '--geolocation',
                'us',
                '--geolocation',
                'gb',
                '--browser',
                'firefox',
                '--pretty',
            ],
        )
        assert result.exit_code == 0
        mock_update.assert_called_once_with(
            'ernie',
            name='ernie-v2',
            tags=['os:windows10-2004-x64', 'locale:en-us'],
            timeout=300,
            network='vpn',
            geolocation=['us', 'gb'],
            browser='firefox',
            unset=None,
            pretty=True,
        )

    @patch(PATCH_TARGET)
    def test_short_flags(self, mock_update):
        result = runner.invoke(
            app,
            ['profile', 'update', 'ernie', '-T', 'os:windows7-x64', '-t', '120', '-b', 'chrome'],
        )
        assert result.exit_code == 0
        kwargs = mock_update.call_args.kwargs
        assert kwargs['tags'] == ['os:windows7-x64']
        assert kwargs['timeout'] == 120
        assert kwargs['browser'] == 'chrome'

    @patch(PATCH_TARGET)
    def test_unset_browser(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '--unset', 'browser'])
        assert result.exit_code == 0
        assert mock_update.call_args.kwargs['unset'] == ['browser']

    @patch(PATCH_TARGET)
    def test_unset_repeatable(self, mock_update):
        result = runner.invoke(
            app,
            ['profile', 'update', 'ernie', '--unset', 'network', '--unset', 'geolocation'],
        )
        assert result.exit_code == 0
        assert mock_update.call_args.kwargs['unset'] == ['network', 'geolocation']

    @patch(PATCH_TARGET)
    def test_unset_case_insensitive(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '--unset', 'BROWSER'])
        assert result.exit_code == 0
        assert mock_update.call_args.kwargs['unset'] == ['browser']

    @patch(PATCH_TARGET)
    def test_network_case_insensitive(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-N', 'VPN'])
        assert result.exit_code == 0
        assert mock_update.call_args.kwargs['network'] == 'vpn'

    @patch(PATCH_TARGET)
    def test_geolocation_with_vpn_ok(self, mock_update):
        result = runner.invoke(
            app, ['profile', 'update', 'ernie', '-N', 'vpn', '--geolocation', 'us']
        )
        assert result.exit_code == 0
        mock_update.assert_called_once()

    @patch(PATCH_TARGET)
    def test_geolocation_alone_deferred_to_domain(self, mock_update):
        """Without an explicit --network the vpn check depends on the fetched profile."""
        result = runner.invoke(app, ['profile', 'update', 'ernie', '--geolocation', 'us'])
        assert result.exit_code == 0
        mock_update.assert_called_once()


class TestCmdSandboxProfileUpdateValidation:
    @patch(PATCH_TARGET)
    def test_no_flags_errors(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie'])
        assert result.exit_code != 0
        assert 'nothing to update' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_set_and_unset_conflict(self, mock_update):
        result = runner.invoke(
            app, ['profile', 'update', 'ernie', '-N', 'vpn', '--unset', 'network']
        )
        assert result.exit_code != 0
        assert 'set and unset' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_geolocation_with_non_vpn_network(self, mock_update):
        result = runner.invoke(
            app, ['profile', 'update', 'ernie', '--geolocation', 'us', '-N', 'internet']
        )
        assert result.exit_code != 0
        assert 'vpn' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_geolocation_with_unset_network(self, mock_update):
        result = runner.invoke(
            app, ['profile', 'update', 'ernie', '--geolocation', 'us', '--unset', 'network']
        )
        assert result.exit_code != 0
        assert 'vpn' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_timeout_out_of_range(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-t', '5000'])
        assert result.exit_code != 0
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_timeout_zero_rejected(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-t', '0'])
        assert result.exit_code != 0
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_empty_name_rejected(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-n', '', '-t', '300'])
        assert result.exit_code != 0
        assert 'empty' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_empty_tag_value_rejected(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-T', ''])
        assert result.exit_code != 0
        assert 'empty' in result.output.lower()
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_invalid_unset_field(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '--unset', 'name'])
        assert result.exit_code != 0
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_invalid_network_value(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-N', 'wifi'])
        assert result.exit_code != 0
        mock_update.assert_not_called()

    @patch(PATCH_TARGET)
    def test_invalid_browser_value(self, mock_update):
        result = runner.invoke(app, ['profile', 'update', 'ernie', '-b', 'safari'])
        assert result.exit_code != 0
        mock_update.assert_not_called()

    def test_missing_argument_fails(self):
        result = runner.invoke(app, ['profile', 'update'])
        assert result.exit_code != 0


class TestCmdSandboxProfileUpdateHelp:
    def test_help_available(self):
        result = runner.invoke(app, ['profile', 'update', '--help'])
        assert result.exit_code == 0
        assert '--unset' in result.output

    def test_help_documents_merge_semantics(self):
        result = runner.invoke(app, ['profile', 'update', '--help'])
        assert result.exit_code == 0
        assert 'unchanged' in result.output.lower() or 'current value' in result.output.lower()

    def test_profile_subcommand_shows_update(self):
        result = runner.invoke(app, ['profile', '--help'])
        assert result.exit_code == 0
        assert 'update' in result.output
