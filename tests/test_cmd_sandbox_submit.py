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

_URL = 'https://evil.com'
_IMPORT_ID = '250601-abc123'

_DEFAULTS = {
    'fetch': False,
    'import_': False,
    'profiles': None,
    'timeout': None,
    'network': None,
    'geolocation': None,
    'tags': None,
    'password': None,
    'wait': False,
    'interactive': False,
    'pretty': False,
}


def _expected(**overrides):
    return {**_DEFAULTS, **overrides}


@patch('banshee.commands.cmd_sandbox.submit_sandbox_sample')
class TestCmdSandboxSubmit:
    def test_bare_target(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected())

    def test_fetch_flag(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--fetch'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(fetch=True))

    def test_import_flag(self, mock_fn):
        result = runner.invoke(app, ['submit', _IMPORT_ID, '--import'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_IMPORT_ID, **_expected(import_=True))

    def test_fetch_and_import_mutually_exclusive(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--fetch', '--import'])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_profile_single(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--profile', 'win10-x64'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(profiles=['win10-x64']))

    def test_profile_repeatable(self, mock_fn):
        result = runner.invoke(
            app, ['submit', _URL, '--profile', 'win10-x64', '--profile', 'office365']
        )
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(profiles=['win10-x64', 'office365']))

    def test_profile_empty_fails(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--profile', ''])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_interactive_and_profile_mutually_exclusive(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--interactive', '--profile', 'win10-x64'])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_timeout_long_and_short(self, mock_fn):
        for flag in ('--timeout', '-t'):
            mock_fn.reset_mock()
            result = runner.invoke(app, ['submit', _URL, flag, '120'])
            assert result.exit_code == 0
            mock_fn.assert_called_once_with(_URL, **_expected(timeout=120))

    def test_timeout_out_of_range_fails(self, mock_fn):
        for value in ('0', '3601'):
            result = runner.invoke(app, ['submit', _URL, '--timeout', value])
            assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_network_long_and_short(self, mock_fn):
        for flag in ('--network', '-N'):
            mock_fn.reset_mock()
            result = runner.invoke(app, ['submit', _URL, flag, 'internet'])
            assert result.exit_code == 0
            mock_fn.assert_called_once_with(_URL, **_expected(network='internet'))

    def test_network_invalid_value_fails(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--network', 'bogus'])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_geolocation_requires_vpn_network(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--geolocation', 'us'])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_geolocation_with_other_network_fails(self, mock_fn):
        result = runner.invoke(
            app, ['submit', _URL, '--network', 'internet', '--geolocation', 'us']
        )
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_geolocation_with_vpn_network(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--network', 'vpn', '--geolocation', 'us'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(network='vpn', geolocation='us'))

    def test_tags_repeatable(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '-T', 'case-42', '--tags', 'phishing'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(tags=['case-42', 'phishing']))

    def test_tags_empty_fails(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--tags', ''])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_password(self, mock_fn):
        result = runner.invoke(app, ['submit', _URL, '--password', 'infected'])
        assert result.exit_code == 0
        mock_fn.assert_called_once_with(_URL, **_expected(password='infected'))  # noqa: S106 test fixture, not a secret

    def test_wait_long_and_short(self, mock_fn):
        for flag in ('--wait', '-w'):
            mock_fn.reset_mock()
            result = runner.invoke(app, ['submit', _URL, flag])
            assert result.exit_code == 0
            mock_fn.assert_called_once_with(_URL, **_expected(wait=True))

    def test_interactive_long_and_short(self, mock_fn):
        for flag in ('--interactive', '-i'):
            mock_fn.reset_mock()
            result = runner.invoke(app, ['submit', _URL, flag])
            assert result.exit_code == 0
            mock_fn.assert_called_once_with(_URL, **_expected(interactive=True))

    def test_pretty_long_and_short(self, mock_fn):
        for flag in ('--pretty', '-p'):
            mock_fn.reset_mock()
            result = runner.invoke(app, ['submit', _URL, flag])
            assert result.exit_code == 0
            mock_fn.assert_called_once_with(_URL, **_expected(pretty=True))

    def test_missing_target_fails(self, mock_fn):
        result = runner.invoke(app, ['submit'])
        assert result.exit_code != 0
        mock_fn.assert_not_called()

    def test_help_shows_options(self, mock_fn):
        result = runner.invoke(app, ['submit', '--help'])
        assert result.exit_code == 0
        for option in (
            '--fetch',
            '--import',
            '--profile',
            '--timeout',
            '--network',
            '--geolocation',
            '--tags',
            '--password',
            '--wait',
            '--interactive',
            '--pretty',
        ):
            assert option in result.output
        mock_fn.assert_not_called()

    def test_help_does_not_show_browser(self, mock_fn):
        result = runner.invoke(app, ['submit', '--help'])
        assert result.exit_code == 0
        assert '--browser' not in result.output
        mock_fn.assert_not_called()

    def test_submit_shows_in_sandbox_help(self, mock_fn):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'submit' in result.output
        mock_fn.assert_not_called()
