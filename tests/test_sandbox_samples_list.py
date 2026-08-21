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
from psengine.sandbox.errors import SamplesFetchError
from psengine.sandbox.sandbox import Sample
from rich.console import Console

from banshee.sandbox.samples_list import (
    _samples_table,
    list_sandbox_samples,
    search_sandbox_samples,
)

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)

_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


def _make_sample(**kwargs) -> Sample:
    defaults = {
        'id': '260501-h4p7laawme',
        'status': 'reported',
        'kind': 'file',
        'filename': 'dropper.exe',
        'submitted': '2026-07-01T10:00:00Z',
        'completed': '2026-07-01T10:05:00Z',
        'sha256': _SHA256,
        'user_id': 'u-1',
    }
    defaults.update(kwargs)
    return Sample.model_validate(defaults)


_FILE_SAMPLE = _make_sample()
_URL_SAMPLE = _make_sample(
    id='260502-url9zzbbxx',
    kind='url',
    filename=None,
    sha256=None,
    url='https://evil.example/payload',
)


def _render_table(samples) -> str:
    buf = StringIO()
    console = Console(file=buf, highlight=False, markup=False, no_color=True, width=250)
    console.print(_samples_table(samples))
    return buf.getvalue()


class TestSamplesTable:
    def test_target_shows_filename_for_file_sample(self):
        out = _render_table([_FILE_SAMPLE])
        assert 'dropper.exe' in out

    def test_target_shows_url_for_url_sample(self):
        out = _render_table([_URL_SAMPLE])
        assert 'https://evil.example/payload' in out

    def test_target_dash_when_no_filename_or_url(self):
        sample = _make_sample(filename=None, url=None)
        out = _render_table([sample])
        assert '-' in out

    def test_table_contains_status(self):
        out = _render_table([_FILE_SAMPLE])
        assert 'reported' in out

    def test_table_contains_kind(self):
        out = _render_table([_FILE_SAMPLE])
        assert 'file' in out

    def test_table_contains_id(self):
        out = _render_table([_FILE_SAMPLE])
        assert '260501-h4p7laawme' in out

    def test_table_contains_full_sha256(self):
        out = _render_table([_FILE_SAMPLE])
        assert _SHA256 in out

    def test_table_dash_for_missing_sha256(self):
        out = _render_table([_URL_SAMPLE])
        assert '-' in out

    def test_table_contains_submitted_date(self):
        out = _render_table([_FILE_SAMPLE])
        assert '2026-07-01 10:00' in out

    def test_table_contains_completed_date(self):
        out = _render_table([_FILE_SAMPLE])
        assert '2026-07-01 10:05' in out

    def test_table_dash_for_missing_completed(self):
        sample = _make_sample(completed=None)
        out = _render_table([sample])
        assert '-' in out

    def test_table_multiple_rows(self):
        out = _render_table([_FILE_SAMPLE, _URL_SAMPLE])
        assert 'dropper.exe' in out
        assert 'https://evil.example/payload' in out

    def test_empty_list_renders_headers_only(self):
        out = _render_table([])
        assert 'Target' in out


class TestListSandboxSamples:
    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_default_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_samples.return_value = [_FILE_SAMPLE, _URL_SAMPLE]
        list_sandbox_samples(subset='org', limit=20, pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data) == 2
        assert data[0]['id'] == '260501-h4p7laawme'
        assert data[1]['id'] == '260502-url9zzbbxx'

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_fetch_called_with_subset_and_limit(self, mock_mgr_cls):
        mock_mgr_cls.return_value.fetch_samples.return_value = []
        list_sandbox_samples(subset='public', limit=50, pretty=False)
        mock_mgr_cls.return_value.fetch_samples.assert_called_once_with(
            subset='public', max_results=50
        )

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pretty_renders_table_not_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_samples.return_value = [_FILE_SAMPLE]
        list_sandbox_samples(subset='org', limit=20, pretty=True)
        out = capsys.readouterr().out
        assert 'dropper.exe' in out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_default_empty_list(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_samples.return_value = []
        list_sandbox_samples(subset='org', limit=20, pretty=False)
        out = capsys.readouterr().out
        assert json.loads(out) == []

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pretty_empty_list_shows_headers(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.fetch_samples.return_value = []
        list_sandbox_samples(subset='org', limit=20, pretty=True)
        out = capsys.readouterr().out
        assert 'Target' in out

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_fetch_error_propagates(self, mock_mgr_cls):
        mock_mgr_cls.return_value.fetch_samples.side_effect = SamplesFetchError('API down')
        with pytest.raises(SamplesFetchError):
            list_sandbox_samples(subset='org', limit=20, pretty=False)

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_default_serialises_by_alias(self, mock_mgr_cls, capsys):
        """Sample id_ field must appear as 'id' in JSON output (by_alias=True)."""
        mock_mgr_cls.return_value.fetch_samples.return_value = [_FILE_SAMPLE]
        list_sandbox_samples(subset='org', limit=20, pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'id' in data[0]
        assert 'id_' not in data[0]

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_default_none_fields_excluded(self, mock_mgr_cls, capsys):
        """None-valued fields (url, completed) must be omitted from JSON."""
        sample = _make_sample(completed=None)  # url=None by default
        mock_mgr_cls.return_value.fetch_samples.return_value = [sample]
        list_sandbox_samples(subset='org', limit=20, pretty=False)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert 'url' not in data[0]
        assert 'completed' not in data[0]


class TestSearchSandboxSamples:
    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_default_outputs_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.search_samples.return_value = [_FILE_SAMPLE, _URL_SAMPLE]
        search_sandbox_samples(family='emotet')
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data) == 2
        assert data[0]['id'] == '260501-h4p7laawme'

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_search_called_with_all_filters(self, mock_mgr_cls):
        mock_mgr_cls.return_value.search_samples.return_value = []
        search_sandbox_samples(
            file_hash='h',
            family='f',
            tag=['t1', 't2'],
            botnet='b',
            wallet='w',
            ip='1.2.3.4',
            domain='d',
            url='u',
            from_date='2026-07-01',
            to_date='2026-07-31',
            query='NOT family:emotet',
            limit=100,
        )
        mock_mgr_cls.return_value.search_samples.assert_called_once_with(
            file_hash='h',
            family='f',
            tag=['t1', 't2'],
            botnet='b',
            wallet='w',
            ip='1.2.3.4',
            domain='d',
            url='u',
            from_date='2026-07-01',
            to_date='2026-07-31',
            query='NOT family:emotet',
            results_per_page=100,
            max_results=100,
        )

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_results_per_page_capped_at_200(self, mock_mgr_cls):
        """results_per_page is a hard 200 cap; max_results is the true limit."""
        mock_mgr_cls.return_value.search_samples.return_value = []
        search_sandbox_samples(family='emotet', limit=200)
        kwargs = mock_mgr_cls.return_value.search_samples.call_args.kwargs
        assert kwargs['results_per_page'] == 200
        assert kwargs['max_results'] == 200

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.samples_list.get_config')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_pretty_renders_table_not_json(self, mock_get_config, mock_mgr_cls, capsys):
        mock_get_config.return_value.sandbox_choice = 'eu'
        mock_mgr_cls.return_value.search_samples.return_value = [_FILE_SAMPLE]
        search_sandbox_samples(family='emotet', pretty=True)
        out = capsys.readouterr().out
        assert 'Sandbox search' in out
        assert '1 result' in out
        assert '260501-h' in out  # ID prefix — survives table width truncation
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_empty_result_json(self, mock_mgr_cls, capsys):
        mock_mgr_cls.return_value.search_samples.return_value = []
        search_sandbox_samples(family='emotet')
        out = capsys.readouterr().out
        assert json.loads(out) == []

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.samples_list.get_config')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_empty_result_pretty_shows_no_results_header(
        self, mock_get_config, mock_mgr_cls, capsys
    ):
        mock_get_config.return_value.sandbox_choice = 'eu'
        mock_mgr_cls.return_value.search_samples.return_value = []
        search_sandbox_samples(family='emotet', pretty=True)
        out = capsys.readouterr().out
        assert 'Sandbox search' in out
        assert '0 results' in out
        assert 'family:emotet' in out
        assert 'No matching samples.' in out

    @patch('banshee.sandbox.samples_list.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_search_error_propagates(self, mock_mgr_cls):
        mock_mgr_cls.return_value.search_samples.side_effect = SamplesFetchError('API down')
        with pytest.raises(SamplesFetchError):
            search_sandbox_samples(family='emotet')
