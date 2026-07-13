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
from psengine.sandbox.errors import ProfileFetchError, ProfileNotFoundError
from psengine.sandbox.sandbox import Profile
from rich.console import Console

from banshee.sandbox.profiles import _profiles_table, get_sandbox_profile, list_sandbox_profiles

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
