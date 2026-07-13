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

import json
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from psengine.sandbox import ProfileUpdateOut
from psengine.sandbox.errors import (
    ProfileDeleteError,
    ProfileFetchError,
    ProfileNotFoundError,
    ProfileUpdateError,
)
from psengine.sandbox.sandbox import Profile, ProfileDeleteOut
from rich.console import Console

from banshee.sandbox.profiles import (
    _profiles_table,
    delete_sandbox_profile,
    get_sandbox_profile,
    list_sandbox_profiles,
    update_sandbox_profile,
)

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)


def _make_profile(**kwargs) -> Profile:
    defaults = {
        'id': 'w7-long',
        'name': 'Windows 7 Long',
        'tags': ['os:windows7-x64', 'locale:en-us'],
        'timeout': 300,
    }
    defaults.update(kwargs)
    return Profile.model_validate(defaults)


_PROFILE_A = _make_profile()
_PROFILE_B = _make_profile(id='w10-short', name='Windows 10 Short', timeout=120)


def _render_table(profiles) -> str:
    buf = StringIO()
    console = Console(file=buf, highlight=False, markup=False, no_color=True, width=200)
    console.print(_profiles_table(profiles))
    return buf.getvalue()


class TestProfilesTable:
    def test_table_contains_name(self):
        out = _render_table([_PROFILE_A])
        assert 'Windows 7 Long' in out

    def test_table_contains_id(self):
        out = _render_table([_PROFILE_A])
        assert 'w7-long' in out

    def test_table_contains_timeout(self):
        out = _render_table([_PROFILE_A])
        assert '300s' in out

    def test_table_dash_for_missing_network(self):
        out = _render_table([_PROFILE_A])  # network=None
        assert '—' in out

    def test_table_contains_tags(self):
        out = _render_table([_PROFILE_A])
        assert 'os:windows7-x64' in out

    def test_tags_are_last_column(self):
        out = _render_table([_PROFILE_A])
        # Tags column header appears after Browser column header
        assert out.index('Browser') < out.index('Tags')

    def test_table_shows_network_when_present(self):
        profile = _make_profile(network='internet')
        out = _render_table([profile])
        assert 'internet' in out

    def test_table_multiple_rows(self):
        out = _render_table([_PROFILE_A, _PROFILE_B])
        assert 'Windows 7 Long' in out
        assert 'Windows 10 Short' in out

    def test_empty_list_renders_headers_only(self):
        out = _render_table([])
        assert 'Name' in out

    def test_table_shows_geolocation_when_present(self):
        profile = _make_profile(geolocation=['us', 'eu'])
        out = _render_table([profile])
        assert 'us' in out
        assert 'eu' in out

    def test_table_dash_for_missing_geolocation(self):
        out = _render_table([_PROFILE_A])  # geolocation=[] by default
        assert '—' in out

    def test_geolocation_before_browser_column(self):
        out = _render_table([_PROFILE_A])
        assert out.index('Geolocation') < out.index('Browser')


class TestListSandboxProfiles:
    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_default_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profiles.return_value = [_PROFILE_A, _PROFILE_B]
        list_sandbox_profiles(pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data) == 2
        assert data[0]['id'] == 'w7-long'
        assert data[1]['id'] == 'w10-short'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_pretty_renders_table_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profiles.return_value = [_PROFILE_A]
        list_sandbox_profiles(pretty=True)
        out = capsys.readouterr().out
        assert 'Windows 7 Long' in out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_default_empty_list(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profiles.return_value = []
        list_sandbox_profiles(pretty=False)
        out = capsys.readouterr().out
        assert json.loads(out) == []

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_pretty_empty_list_shows_headers(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profiles.return_value = []
        list_sandbox_profiles(pretty=True)
        out = capsys.readouterr().out
        assert 'Name' in out

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_fetch_error_propagates(self, mock_mgr_cls):
        mock_mgr_cls.return_value.fetch_profiles.side_effect = ProfileFetchError('API down')
        with pytest.raises(ProfileFetchError):
            list_sandbox_profiles(pretty=False)

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_default_serialises_by_alias(self, mock_mgr_cls, capsys):
        """Profile id_ field must appear as 'id' in JSON output (by_alias=True)."""
        mock_mgr_cls.return_value.fetch_profiles.return_value = [_PROFILE_A]
        list_sandbox_profiles(pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'id' in data[0]
        assert 'id_' not in data[0]

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_default_none_fields_excluded(self, mock_mgr_cls, capsys):
        """None-valued fields (network, options) must be omitted from JSON."""
        profile = _make_profile()  # network=None, options=None by default
        mock_mgr_cls.return_value.fetch_profiles.return_value = [profile]
        list_sandbox_profiles(pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'network' not in data[0]
        assert 'options' not in data[0]


class TestGetSandboxProfile:
    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_default_outputs_compact_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profile.return_value = _PROFILE_A
        get_sandbox_profile('w7-long', pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data['id'] == 'w7-long'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_pretty_renders_table_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profile.return_value = _PROFILE_A
        get_sandbox_profile('w7-long', pretty=True)
        out = capsys.readouterr().out
        assert 'Windows 7 Long' in out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_serialises_by_alias(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profile.return_value = _PROFILE_A
        get_sandbox_profile('w7-long', pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'id' in data
        assert 'id_' not in data

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_none_fields_excluded(self, mock_mgr_cls, capsys):
        profile = _make_profile()  # network=None, options=None
        mock_mgr_cls.return_value.fetch_profile.return_value = profile
        get_sandbox_profile('w7-long', pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'network' not in data
        assert 'options' not in data

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_profile_not_found_exits_1(self, mock_mgr_cls):
        mock_mgr_cls.return_value.fetch_profile.side_effect = ProfileNotFoundError(
            'no such profile'
        )
        with pytest.raises(SystemExit) as exc_info:
            get_sandbox_profile('unknown-id', pretty=False)
        assert exc_info.value.code == 1

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_profile_not_found_error_to_stderr(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profile.side_effect = ProfileNotFoundError(
            'no such profile'
        )
        with pytest.raises(SystemExit):
            get_sandbox_profile('unknown-id', pretty=False)
        err = capsys.readouterr().err
        assert 'not found' in err.lower() or 'no such profile' in err.lower()


_FULL_PROFILE = _make_profile(
    network='internet',
    geolocation=[],
    options={'browser': 'firefox'},
)


def _mock_update_mgr(mock_mgr_cls, profile=_FULL_PROFILE):
    mgr = mock_mgr_cls.return_value
    mgr.fetch_profile.return_value = profile
    mgr.update_profile.return_value = ProfileUpdateOut(updated=True)
    return mgr


class TestUpdateSandboxProfile:
    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_name_only_keeps_existing_fields(self, mock_mgr_cls):
        mgr = _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('w7-long', name='renamed')
        mgr.update_profile.assert_called_once_with(
            'w7-long',
            name='renamed',
            tags=['os:windows7-x64', 'locale:en-us'],
            timeout=300,
            network='internet',
            geolocation=None,
            browser='firefox',
        )

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_supplied_fields_overwrite(self, mock_mgr_cls):
        mgr = _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('w7-long', tags=['os:windows10-2004-x64'], timeout=120)
        kwargs = mgr.update_profile.call_args.kwargs
        assert kwargs['tags'] == ['os:windows10-2004-x64']
        assert kwargs['timeout'] == 120
        assert kwargs['name'] == 'Windows 7 Long'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_unset_browser_sends_none(self, mock_mgr_cls):
        mgr = _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('w7-long', unset=['browser'])
        assert mgr.update_profile.call_args.kwargs['browser'] is None

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_unset_network_and_geolocation(self, mock_mgr_cls):
        profile = _make_profile(network='vpn', geolocation=['us'])
        mgr = _mock_update_mgr(mock_mgr_cls, profile)
        update_sandbox_profile('w7-long', unset=['network', 'geolocation'])
        kwargs = mgr.update_profile.call_args.kwargs
        assert kwargs['network'] is None
        assert kwargs['geolocation'] is None

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_put_uses_fetched_id_not_name(self, mock_mgr_cls):
        mgr = _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('Windows 7 Long', timeout=200)
        assert mgr.update_profile.call_args.args[0] == 'w7-long'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_not_found_outputs_updated_false_exit_0(self, mock_mgr_cls, capsys):
        mgr = mock_mgr_cls.return_value
        mgr.fetch_profile.side_effect = ProfileNotFoundError('no such profile')
        update_sandbox_profile('unknown-id', name='x')
        out = capsys.readouterr().out
        assert json.loads(out) == {'updated': False}
        mgr.update_profile.assert_not_called()

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_not_found_pretty_message(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_profile.side_effect = ProfileNotFoundError('nope')
        update_sandbox_profile('unknown-id', name='x', pretty=True)
        out = capsys.readouterr().out
        assert 'not found' in out.lower()
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_supplied_geolocation_without_vpn_exits_1(self, mock_mgr_cls, capsys):
        mgr = _mock_update_mgr(mock_mgr_cls)  # network='internet'
        with pytest.raises(SystemExit) as exc_info:
            update_sandbox_profile('w7-long', geolocation=['us'])
        assert exc_info.value.code == 1
        assert 'vpn' in capsys.readouterr().err.lower()
        mgr.update_profile.assert_not_called()

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_inherited_geolocation_does_not_block_update(self, mock_mgr_cls):
        """A profile already holding geolocation with a non-vpn network updates fine."""
        profile = _make_profile(network='drop', geolocation=['us'])
        mgr = _mock_update_mgr(mock_mgr_cls, profile)
        update_sandbox_profile('w7-long', timeout=150)
        kwargs = mgr.update_profile.call_args.kwargs
        assert kwargs['timeout'] == 150
        assert kwargs['geolocation'] == ['us']
        assert kwargs['network'] == 'drop'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_geolocation_ok_when_profile_already_vpn(self, mock_mgr_cls):
        profile = _make_profile(network='vpn', geolocation=['de'])
        mgr = _mock_update_mgr(mock_mgr_cls, profile)
        update_sandbox_profile('w7-long', geolocation=['us'])
        assert mgr.update_profile.call_args.kwargs['geolocation'] == ['us']

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_update_error_exits_1(self, mock_mgr_cls, capsys):
        mgr = _mock_update_mgr(mock_mgr_cls)
        mgr.update_profile.side_effect = ProfileUpdateError('API down')
        with pytest.raises(SystemExit) as exc_info:
            update_sandbox_profile('w7-long', name='x')
        assert exc_info.value.code == 1
        assert 'api down' in capsys.readouterr().err.lower()

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_success_outputs_updated_true_json(self, mock_mgr_cls, capsys):
        _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('w7-long', name='x')
        out = capsys.readouterr().out
        assert json.loads(out) == {'updated': True}

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_success_pretty_message_not_json(self, mock_mgr_cls, capsys):
        _mock_update_mgr(mock_mgr_cls)
        update_sandbox_profile('w7-long', name='x', pretty=True)
        out = capsys.readouterr().out
        assert 'updated' in out.lower()
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)


class TestDeleteSandboxProfile:
    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_deleted_prints_confirmation(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.delete_profile.return_value = ProfileDeleteOut(deleted=True)
        delete_sandbox_profile('w7-long')
        out = capsys.readouterr().out
        assert out == 'Deleted profile: w7-long\n'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_not_found_prints_warning_and_returns(self, mock_mgr_cls, capsys):
        """404 is idempotent: warning on stdout, normal return (exit 0)."""
        mock_mgr_cls.return_value.delete_profile.return_value = ProfileDeleteOut(deleted=False)
        delete_sandbox_profile('unknown-id')
        out = capsys.readouterr().out
        assert out == 'Profile not found: unknown-id\n'

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_delete_called_with_argument(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.delete_profile.return_value = ProfileDeleteOut(deleted=True)
        delete_sandbox_profile('w7-long')
        capsys.readouterr()
        mock_mgr_cls.return_value.delete_profile.assert_called_once_with('w7-long')

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_delete_error_propagates(self, mock_mgr_cls):
        mock_mgr_cls.return_value.delete_profile.side_effect = ProfileDeleteError('API down')
        with pytest.raises(ProfileDeleteError):
            delete_sandbox_profile('w7-long')

    @patch('banshee.sandbox.profiles._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.profiles.SandboxMgr')
    @patch('banshee.sandbox.profiles.get_config', new=MagicMock())
    def test_output_is_plain_text_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.delete_profile.return_value = ProfileDeleteOut(deleted=True)
        delete_sandbox_profile('w7-long')
        out = capsys.readouterr().out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)
