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
from unittest.mock import MagicMock, patch

import pytest
from psengine.sandbox.errors import SampleProfileError
from psengine.sandbox.sandbox import SampleProfileOut

from banshee.sandbox.submit import _parse_picks, set_sandbox_sample_profile

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)

_SAMPLE_ID = '260501-h4p7laawme'
_SUCCESS_OUT = SampleProfileOut(success=True)


class TestParsepicks:
    def test_single_pick(self):
        assert _parse_picks(['file.exe:win10-x64']) == [
            {'pick': 'file.exe', 'profile': 'win10-x64'}
        ]

    def test_multiple_picks(self):
        result = _parse_picks(['file.exe:win10-x64', 'doc.docx:office365'])
        assert result == [
            {'pick': 'file.exe', 'profile': 'win10-x64'},
            {'pick': 'doc.docx', 'profile': 'office365'},
        ]

    def test_profile_with_colon_splits_on_first(self):
        # Profile name containing a colon: only first colon splits
        result = _parse_picks(['file.exe:some:profile'])
        assert result == [{'pick': 'file.exe', 'profile': 'some:profile'}]


class TestSetSandboxSampleProfile:
    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_auto_mode_calls_mgr_correctly(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        mock_mgr_cls.return_value.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID, auto=True, profiles=None
        )

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_auto_mode_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data == {'success': True}

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_pick_mode_parses_and_calls_mgr(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=False, picks=['file.exe:win10-x64'])
        mock_mgr_cls.return_value.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID, auto=False, profiles=[{'pick': 'file.exe', 'profile': 'win10-x64'}]
        )

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_multi_pick_mode_calls_mgr(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(
            _SAMPLE_ID, auto=False, picks=['file.exe:win10-x64', 'doc.docx:office365']
        )
        mock_mgr_cls.return_value.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID,
            auto=False,
            profiles=[
                {'pick': 'file.exe', 'profile': 'win10-x64'},
                {'pick': 'doc.docx', 'profile': 'office365'},
            ],
        )

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_pick_mode_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=False, picks=['file.exe:win10-x64'])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data == {'success': True}

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_pretty_mode_outputs_text_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None, pretty=True)
        out = capsys.readouterr().out
        assert 'successfully' in out.lower()
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_sample_profile_error_exits_1(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.side_effect = SampleProfileError(
            'sample not in static_analysis'
        )
        with pytest.raises(SystemExit) as exc_info:
            set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        assert exc_info.value.code == 1

    @patch('banshee.sandbox.submit._spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.submit.SandboxMgr')
    @patch('banshee.sandbox.submit.get_config', new=MagicMock())
    def test_sample_profile_error_message_to_stderr(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.side_effect = SampleProfileError(
            'sample not in static_analysis'
        )
        with pytest.raises(SystemExit):
            set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        err = capsys.readouterr().err
        assert 'sample not in static_analysis' in err
