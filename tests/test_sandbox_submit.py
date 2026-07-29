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
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from psengine.sandbox.errors import SampleProfileError, SampleSubmitError
from psengine.sandbox.sandbox import (
    Profile,
    Sample,
    SampleProfileOut,
    SampleTasks,
    StaticAnalysisReport,
)

from banshee.sandbox.submit import (
    _parse_picks,
    _resolve_submission,
    interactive_profile_selection,
    poll_until_terminal,
    set_sandbox_sample_profile,
    submit_sandbox_sample,
)

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)

_SAMPLE_ID = '260501-h4p7laawme'
_SUCCESS_OUT = SampleProfileOut(success=True)
_URL = 'https://evil.com'


def _sample(status='pending', **overrides):
    data = {
        'id': _SAMPLE_ID,
        'status': status,
        'kind': 'file',
        'filename': 'malware.exe',
        'submitted': '2026-07-13T12:00:00Z',
        'user_id': 'user-1',
        **overrides,
    }
    return Sample.model_validate(data)


def _sample_tasks(status='pending', **overrides):
    return SampleTasks.model_validate(_sample(status, **overrides).json())


def _static_report(kind='file', target='malware.exe', files=()):
    return StaticAnalysisReport.model_validate(
        {
            'sample': {'sample': _SAMPLE_ID, 'kind': kind, 'target': target},
            'task': {'task': 'static1'},
            'analysis': {'score': 5},
            'files': list(files),
        }
    )


def _file(filename, relpath=None, selected=None):
    return {'filename': filename, 'relpath': relpath or f'unpack/{filename}', 'selected': selected}


def _profile(id_='prof-1', name='win10-x64'):
    return Profile.model_validate({'id': id_, 'name': name})


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
    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_auto_mode_calls_mgr_correctly(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        mock_mgr_cls.return_value.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID, auto=True, profiles=None
        )

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_auto_mode_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data == {'success': True}

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pick_mode_parses_and_calls_mgr(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=False, picks=['file.exe:win10-x64'])
        mock_mgr_cls.return_value.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID, auto=False, profiles=[{'pick': 'file.exe', 'profile': 'win10-x64'}]
        )

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
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

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pick_mode_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=False, picks=['file.exe:win10-x64'])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data == {'success': True}

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pretty_mode_outputs_text_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.return_value = _SUCCESS_OUT
        set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None, pretty=True)
        out = capsys.readouterr().out
        assert 'successfully' in out.lower()
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_sample_profile_error_exits_1(self, mock_mgr_cls):
        mock_mgr_cls.return_value.set_sample_profile.side_effect = SampleProfileError(
            'sample not in static_analysis'
        )
        with pytest.raises(SystemExit) as exc_info:
            set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        assert exc_info.value.code == 1

    @patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_sample_profile_error_message_to_stderr(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.set_sample_profile.side_effect = SampleProfileError(
            'sample not in static_analysis'
        )
        with pytest.raises(SystemExit):
            set_sandbox_sample_profile(_SAMPLE_ID, auto=True, picks=None)
        err = capsys.readouterr().err
        assert 'sample not in static_analysis' in err


class TestResolveSubmission:
    def test_existing_file_is_kind_file(self, tmp_path):
        target = tmp_path / 'malware.exe'
        target.write_bytes(b'MZ')
        assert _resolve_submission(str(target), fetch=False, import_=False) == {
            'kind': 'file',
            'file_path': Path(target),
        }

    def test_url_is_kind_url(self):
        assert _resolve_submission(_URL, fetch=False, import_=False) == {'kind': 'url', 'url': _URL}

    def test_url_with_fetch_is_kind_fetch(self):
        assert _resolve_submission(_URL, fetch=True, import_=False) == {
            'kind': 'fetch',
            'url': _URL,
        }

    def test_import_is_kind_import(self):
        assert _resolve_submission('250601-abc123', fetch=False, import_=True) == {
            'kind': 'import',
            'source_id': '250601-abc123',
        }

    def test_fetch_with_local_file_exits_1(self, tmp_path, capsys):
        target = tmp_path / 'malware.exe'
        target.write_bytes(b'MZ')
        with pytest.raises(SystemExit) as exc_info:
            _resolve_submission(str(target), fetch=True, import_=False)
        assert exc_info.value.code == 1
        assert 'URL' in capsys.readouterr().err

    def test_fetch_with_non_url_exits_1(self):
        with pytest.raises(SystemExit) as exc_info:
            _resolve_submission('not-a-url', fetch=True, import_=False)
        assert exc_info.value.code == 1

    def test_unrecognisable_target_exits_1(self, tmp_path, capsys):
        with pytest.raises(SystemExit) as exc_info:
            _resolve_submission(str(tmp_path / 'missing.exe'), fetch=False, import_=False)
        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert 'missing.exe' in err


@patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
@patch('banshee.sandbox.helpers.SandboxMgr')
@patch('banshee.sandbox.helpers.get_config', new=MagicMock())
class TestSubmitSandboxSample:
    def test_url_submission_calls_mgr(self, mock_mgr_cls):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample(kind='url')
        submit_sandbox_sample(_URL)
        mock_mgr_cls.return_value.submit_sample.assert_called_once_with(
            kind='url',
            url=_URL,
            interactive=None,
            password=None,
            profiles=None,
            user_tags=None,
            timeout=None,
            network=None,
            geolocation=None,
        )

    def test_file_submission_calls_mgr(self, mock_mgr_cls, tmp_path):
        target = tmp_path / 'malware.exe'
        target.write_bytes(b'MZ')
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        submit_sandbox_sample(str(target))
        mock_mgr_cls.return_value.submit_sample.assert_called_once_with(
            kind='file',
            file_path=Path(target),
            interactive=None,
            password=None,
            profiles=None,
            user_tags=None,
            timeout=None,
            network=None,
            geolocation=None,
        )

    def test_options_are_passed_through(self, mock_mgr_cls):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample(kind='url')
        submit_sandbox_sample(
            _URL,
            profiles=['win10-x64', 'office365'],
            timeout=120,
            network='vpn',
            geolocation='us',
            tags=['case-42'],
            password='infected',  # noqa: S106 test fixture, not a secret
        )
        mock_mgr_cls.return_value.submit_sample.assert_called_once_with(
            kind='url',
            url=_URL,
            interactive=None,
            password='infected',  # noqa: S106 test fixture, not a secret
            profiles=[{'profile': 'win10-x64'}, {'profile': 'office365'}],
            user_tags=['case-42'],
            timeout=120,
            network='vpn',
            geolocation='us',
        )

    def test_default_output_is_sample_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        submit_sandbox_sample(_URL)
        data = json.loads(capsys.readouterr().out)
        assert data['id'] == _SAMPLE_ID
        assert data['status'] == 'pending'
        assert data['kind'] == 'file'

    def test_pretty_output_is_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        submit_sandbox_sample(_URL, pretty=True)
        out = capsys.readouterr().out
        assert _SAMPLE_ID in out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_submit_error_exits_1(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.side_effect = SampleSubmitError('quota exceeded')
        with pytest.raises(SystemExit) as exc_info:
            submit_sandbox_sample(_URL)
        assert exc_info.value.code == 1
        assert 'quota exceeded' in capsys.readouterr().err

    def test_validation_error_exits_1(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.side_effect = _pydantic_error()
        with pytest.raises(SystemExit) as exc_info:
            submit_sandbox_sample(_URL)
        assert exc_info.value.code == 1
        assert capsys.readouterr().err

    @patch('banshee.sandbox.submit.fetch_overview_report')
    @patch('banshee.sandbox.submit.poll_until_terminal')
    def test_wait_reported_prints_overview(self, mock_poll, mock_overview, mock_mgr_cls):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_poll.return_value = _sample_tasks('reported')
        submit_sandbox_sample(_URL, wait=True, pretty=True)
        mock_overview.assert_called_once_with(_SAMPLE_ID, pretty=True)

    @patch('banshee.sandbox.submit.fetch_overview_report')
    @patch('banshee.sandbox.submit.poll_until_terminal')
    def test_wait_failed_exits_1(self, mock_poll, mock_overview, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_poll.return_value = _sample_tasks('failed')
        with pytest.raises(SystemExit) as exc_info:
            submit_sandbox_sample(_URL, wait=True)
        assert exc_info.value.code == 1
        assert 'failed' in capsys.readouterr().err
        mock_overview.assert_not_called()

    @patch('banshee.sandbox.submit.fetch_overview_report')
    @patch('banshee.sandbox.submit.poll_until_terminal')
    def test_wait_timeout_exits_1_with_hint(self, mock_poll, mock_overview, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_poll.return_value = None
        with pytest.raises(SystemExit) as exc_info:
            submit_sandbox_sample(_URL, wait=True)
        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert 'still running' in err
        assert _SAMPLE_ID in err
        mock_overview.assert_not_called()

    @patch('banshee.sandbox.submit.interactive_profile_selection')
    def test_interactive_refetches_and_prints_sample(self, mock_interactive, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_mgr_cls.return_value.fetch_sample.return_value = _sample_tasks('scheduled')
        submit_sandbox_sample(_URL, interactive=True)
        mock_interactive.assert_called_once_with(mock_mgr_cls.return_value, _SAMPLE_ID)
        data = json.loads(capsys.readouterr().out)
        assert data['status'] == 'scheduled'

    @patch('banshee.sandbox.submit.fetch_overview_report')
    @patch('banshee.sandbox.submit.poll_until_terminal')
    @patch('banshee.sandbox.submit.interactive_profile_selection')
    def test_interactive_with_wait_resumes_polling(
        self, mock_interactive, mock_poll, mock_overview, mock_mgr_cls
    ):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_poll.return_value = _sample_tasks('reported')
        submit_sandbox_sample(_URL, interactive=True, wait=True)
        mock_interactive.assert_called_once_with(mock_mgr_cls.return_value, _SAMPLE_ID)
        mock_overview.assert_called_once_with(_SAMPLE_ID, pretty=False)

    def test_interactive_flag_passed_to_submit(self, mock_mgr_cls):
        mock_mgr_cls.return_value.submit_sample.return_value = _sample()
        mock_mgr_cls.return_value.fetch_sample.return_value = _sample_tasks('scheduled')
        with patch('banshee.sandbox.submit.interactive_profile_selection'):
            submit_sandbox_sample(_URL, interactive=True)
        assert mock_mgr_cls.return_value.submit_sample.call_args.kwargs['interactive'] is True


def _pydantic_error():
    try:
        Sample.model_validate({})
    except Exception as exc:  # noqa: BLE001
        return exc
    raise AssertionError('expected a pydantic ValidationError')


@patch('banshee.sandbox.submit._status_spinner', new=_SPINNER_MOCK)
class TestPollUntilTerminal:
    @patch('banshee.sandbox.submit.time')
    def test_polls_until_reported(self, mock_time):
        mock_time.monotonic.side_effect = [0, 1, 2]
        mgr = MagicMock()
        mgr.fetch_sample.side_effect = [
            _sample_tasks('pending'),
            _sample_tasks('running'),
            _sample_tasks('reported'),
        ]
        result = poll_until_terminal(mgr, _SAMPLE_ID)
        assert result.status == 'reported'
        assert mgr.fetch_sample.call_count == 3
        assert mock_time.sleep.call_count == 2

    @patch('banshee.sandbox.submit.time')
    def test_returns_failed_sample(self, mock_time):
        mock_time.monotonic.side_effect = [0, 1]
        mgr = MagicMock()
        mgr.fetch_sample.side_effect = [_sample_tasks('failed')]
        result = poll_until_terminal(mgr, _SAMPLE_ID)
        assert result.status == 'failed'
        mock_time.sleep.assert_not_called()

    @patch('banshee.sandbox.submit.time')
    def test_returns_none_on_timeout(self, mock_time):
        mock_time.monotonic.side_effect = [0, 700]
        mgr = MagicMock()
        mgr.fetch_sample.return_value = _sample_tasks('running')
        assert poll_until_terminal(mgr, _SAMPLE_ID) is None


@patch('banshee.sandbox.submit.spinner', new=_SPINNER_MOCK)
@patch('banshee.sandbox.submit._status_spinner', new=_SPINNER_MOCK)
class TestInteractiveProfileSelection:
    def _mgr(self, status='static_analysis', report=None, profiles=None):
        mgr = MagicMock()
        mgr.fetch_sample.return_value = _sample_tasks(status)
        mgr.fetch_sample_static_report.return_value = report or _static_report()
        mgr.fetch_profiles.return_value = [_profile()] if profiles is None else profiles
        return mgr

    @patch('banshee.sandbox.submit.Prompt')
    def test_url_sample_skips_file_prompt(self, mock_prompt):
        mgr = self._mgr(report=_static_report(kind='url', target=_URL, files=[]))
        mock_prompt.ask.return_value = '1'
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mock_prompt.ask.assert_called_once()
        mgr.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID, auto=False, profiles=[{'pick': _URL, 'profile': 'prof-1'}]
        )

    @patch('banshee.sandbox.submit.Prompt')
    def test_single_file_skips_file_prompt(self, mock_prompt):
        mgr = self._mgr(report=_static_report(files=[_file('malware.exe')]))
        mock_prompt.ask.return_value = '1'
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mock_prompt.ask.assert_called_once()
        mgr.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID,
            auto=False,
            profiles=[{'pick': 'unpack/malware.exe', 'profile': 'prof-1'}],
        )

    @patch('banshee.sandbox.submit.Prompt')
    def test_multi_file_prompts_for_files_and_profiles(self, mock_prompt):
        report = _static_report(files=[_file('a.exe'), _file('b.exe')])
        mgr = self._mgr(report=report)
        mock_prompt.ask.side_effect = ['1,2', '1', '1']
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mgr.set_sample_profile.assert_called_once_with(
            _SAMPLE_ID,
            auto=False,
            profiles=[
                {'pick': 'unpack/a.exe', 'profile': 'prof-1'},
                {'pick': 'unpack/b.exe', 'profile': 'prof-1'},
            ],
        )

    @patch('banshee.sandbox.submit.Prompt')
    def test_blank_file_selection_uses_auto(self, mock_prompt):
        report = _static_report(
            files=[_file('a.exe', selected=True), _file('b.exe', selected=False)]
        )
        mgr = self._mgr(report=report)
        mock_prompt.ask.return_value = ''
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mgr.set_sample_profile.assert_called_once_with(_SAMPLE_ID, auto=True, pick=['unpack/a.exe'])

    @patch('banshee.sandbox.submit.Prompt')
    def test_blank_profile_selection_uses_auto(self, mock_prompt):
        mgr = self._mgr(report=_static_report(files=[_file('a.exe')]))
        mock_prompt.ask.return_value = ''
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mgr.set_sample_profile.assert_called_once_with(_SAMPLE_ID, auto=True, pick=['unpack/a.exe'])

    @patch('banshee.sandbox.submit.Prompt')
    def test_no_org_profiles_uses_auto_without_prompt(self, mock_prompt):
        mgr = self._mgr(report=_static_report(files=[_file('a.exe')]), profiles=[])
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mock_prompt.ask.assert_not_called()
        mgr.set_sample_profile.assert_called_once_with(_SAMPLE_ID, auto=True, pick=['unpack/a.exe'])

    def test_failed_sample_exits_1(self, capsys):
        mgr = self._mgr(status='failed')
        with pytest.raises(SystemExit) as exc_info:
            interactive_profile_selection(mgr, _SAMPLE_ID)
        assert exc_info.value.code == 1
        assert 'failed' in capsys.readouterr().err

    def test_sample_past_static_analysis_skips_selection(self):
        mgr = self._mgr(status='running')
        interactive_profile_selection(mgr, _SAMPLE_ID)
        mgr.set_sample_profile.assert_not_called()

    @patch('banshee.sandbox.submit.time')
    def test_waits_for_static_analysis(self, mock_time):
        mock_time.monotonic.side_effect = [0, 1]
        mgr = self._mgr()
        mgr.fetch_sample.side_effect = [
            _sample_tasks('pending'),
            _sample_tasks('static_analysis'),
        ]
        mgr.fetch_profiles.return_value = []
        interactive_profile_selection(mgr, _SAMPLE_ID)
        assert mgr.fetch_sample.call_count == 2
        mgr.set_sample_profile.assert_called_once()

    @patch('banshee.sandbox.submit.Prompt')
    def test_profile_error_exits_1(self, mock_prompt, capsys):
        mgr = self._mgr(report=_static_report(files=[_file('a.exe')]))
        mock_prompt.ask.return_value = '1'
        mgr.set_sample_profile.side_effect = SampleProfileError('boom')
        with pytest.raises(SystemExit) as exc_info:
            interactive_profile_selection(mgr, _SAMPLE_ID)
        assert exc_info.value.code == 1
        assert 'boom' in capsys.readouterr().err
