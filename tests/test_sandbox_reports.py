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
import os
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest
from psengine.sandbox import BehavioralReport, OverviewReport, StaticAnalysisReport
from psengine.sandbox.errors import (
    SampleBehavioralReportError,
    SampleOverviewError,
    SampleReportNotAvailableError,
    SampleReportNotFoundError,
    SampleStaticReportError,
)
from requests.exceptions import HTTPError

from banshee.sandbox.reports import (
    fetch_behavioral_reports,
    fetch_overview_report,
    fetch_static_report,
)

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)

_SAMPLE_ID = '251114-py23jaavtp'
_SHA256 = '5b5c276ea74e1086e4835221da50865f872fe20cfc5ea9aa6a909a0b0b9a0554'
_MD5 = '46bcf4e361cd251c958720e1198e3f0a'


def _make_report(**overrides) -> OverviewReport:
    payload = {
        'analysis': {
            'score': 10,
            'family': ['darkcomet'],
            'tags': ['family:darkcomet', 'botnet:ap', 'rat'],
        },
        'sample': {
            'id': _SAMPLE_ID,
            'score': 10,
            'md5': _MD5,
            'sha1': '57ab0765c97b230c615b43ee4ebc28b674887121',
            'sha256': _SHA256,
        },
        'signatures': [
            {'name': 'Darkcomet', 'score': 10, 'tags': ['trojan', 'rat']},
            {
                'name': 'Modifies WinLogon for persistence',
                'score': 10,
                'ttp': ['T1547.004', 'T1112'],
            },
        ],
        'extracted': [
            {
                'config': {
                    'family': 'darkcomet',
                    'c2': ['kvejo991.ddns.net:1604'],
                    'botnet': 'AP',
                },
                'tasks': ['static1'],
            },
        ],
        'targets': [
            {
                'iocs': {
                    'domains': ['kvejo991.ddns.net'],
                    'ips': ['8.8.8.8', '208.89.74.23'],
                },
            },
        ],
        'tasks': {
            'behavioral1': {'kind': 'behavioral', 'status': 'reported', 'score': 10},
            'static1': {'kind': 'static', 'status': 'reported', 'score': 10},
        },
    }
    payload.update(overrides)
    return OverviewReport.model_validate(payload)


_RICH_REPORT = _make_report()
_SPARSE_REPORT = OverviewReport.model_validate(
    {'analysis': {}, 'sample': {'id': 'sparse-id'}, 'targets': None}
)


@contextmanager
def _patched_mgr():
    with (
        patch('banshee.sandbox.reports._spinner', new=_SPINNER_MOCK),
        patch('banshee.sandbox.reports.get_config', new=MagicMock()),
        patch('banshee.sandbox.reports.SandboxMgr') as mock_mgr_cls,
    ):
        yield mock_mgr_cls


def _run(capsys, report=_RICH_REPORT, pretty=False):
    with _patched_mgr() as mock_mgr_cls:
        mock_mgr_cls.return_value.fetch_sample_overview_report.return_value = report
        fetch_overview_report(_SAMPLE_ID, pretty=pretty)
    return capsys.readouterr().out


def _run_with_error(capsys, error):
    with _patched_mgr() as mock_mgr_cls:
        mock_mgr_cls.return_value.fetch_sample_overview_report.side_effect = error
        with pytest.raises(SystemExit) as exc_info:
            fetch_overview_report(_SAMPLE_ID, pretty=False)
    return exc_info.value.code, capsys.readouterr()


class TestOverviewJson:
    def test_default_outputs_json(self, capsys):
        data = json.loads(_run(capsys))
        assert data['analysis']['score'] == 10
        assert data['analysis']['family'] == ['darkcomet']

    def test_fetch_called_with_sample_id(self, capsys):
        with _patched_mgr() as mock_mgr_cls:
            mock_mgr_cls.return_value.fetch_sample_overview_report.return_value = _RICH_REPORT
            fetch_overview_report(_SAMPLE_ID, pretty=False)
        capsys.readouterr()
        mock_mgr_cls.return_value.fetch_sample_overview_report.assert_called_once_with(_SAMPLE_ID)

    def test_serialises_by_alias(self, capsys):
        """Sample id_ field must appear as 'id' in JSON output (by_alias=True)."""
        data = json.loads(_run(capsys))
        assert data['sample']['id'] == _SAMPLE_ID
        assert 'id_' not in data['sample']

    def test_json_contains_target_iocs(self, capsys):
        data = json.loads(_run(capsys))
        assert data['targets'][0]['iocs']['domains'] == ['kvejo991.ddns.net']

    def test_none_fields_excluded(self, capsys):
        data = json.loads(_run(capsys, report=_SPARSE_REPORT))
        assert 'md5' not in data['sample']


class TestOverviewPretty:
    def test_pretty_shows_verdict_header(self, capsys):
        out = _run(capsys, pretty=True)
        assert _SAMPLE_ID in out
        assert 'SCORE 10' in out
        assert 'MALICIOUS' in out
        assert 'darkcomet' in out

    def test_pretty_shows_hashes(self, capsys):
        out = _run(capsys, pretty=True)
        assert _SHA256[:16] in out
        assert _MD5[:16] in out

    def test_pretty_shows_signatures(self, capsys):
        out = _run(capsys, pretty=True)
        assert 'Darkcomet' in out
        assert 'T1547.004' in out

    def test_pretty_shows_extracted_config(self, capsys):
        out = _run(capsys, pretty=True)
        assert 'kvejo991.ddns.net:1604' in out

    def test_pretty_shows_iocs(self, capsys):
        out = _run(capsys, pretty=True)
        assert '8.8.8.8' in out
        assert '208.89.74.23' in out

    def test_pretty_shows_tasks(self, capsys):
        out = _run(capsys, pretty=True)
        assert 'behavioral1' in out
        assert 'reported' in out

    def test_pretty_is_not_json(self, capsys):
        out = _run(capsys, pretty=True)
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_pretty_truncates_long_signature_list(self, capsys):
        signatures = [{'name': f'signature-{i:02d}', 'score': 20 - i} for i in range(1, 13)]
        out = _run(capsys, report=_make_report(signatures=signatures), pretty=True)
        assert 'signature-01' in out
        assert 'signature-10' in out
        assert 'signature-11' not in out
        assert 'more' in out

    def test_pretty_signatures_sorted_by_score(self, capsys):
        signatures = [
            {'name': 'low-scorer', 'score': 1},
            {'name': 'unscored'},
            {'name': 'top-scorer', 'score': 9},
        ]
        out = _run(capsys, report=_make_report(signatures=signatures), pretty=True)
        assert out.index('top-scorer') < out.index('low-scorer') < out.index('unscored')

    def test_pretty_elides_long_ioc_values(self, capsys):
        long_url = 'https://example.com/' + 'a' * 200
        report = _make_report(targets=[{'iocs': {'urls': [long_url]}}])
        out = _run(capsys, report=report, pretty=True)
        assert 'example.com' in out
        assert '…' in out
        assert 'a' * 45 not in out

    def test_pretty_escapes_markup_in_report_data(self, capsys):
        """Bracket-laden report values must render literally, not as Rich markup."""
        report = _make_report(
            analysis={'score': 10, 'family': ['[red]fake[/red]'], 'tags': []},
            signatures=[{'name': 'bad [/closes] tag', 'score': 5}],
            targets=[{'iocs': {'urls': ['http://evil.example/[link=http://x]hi[/link]']}}],
        )
        out = _run(capsys, report=report, pretty=True)
        assert '[red]fake[/red]' in out
        assert 'bad [/closes] tag' in out
        assert '[link=http://x]hi[/link]' in out

    def test_pretty_sparse_report_renders(self, capsys):
        out = _run(capsys, report=_SPARSE_REPORT, pretty=True)
        assert 'sparse-id' in out
        assert 'UNKNOWN' in out

    def test_pretty_sparse_report_omits_empty_sections(self, capsys):
        out = _run(capsys, report=_SPARSE_REPORT, pretty=True)
        assert 'Signatures' not in out
        assert 'IOCs' not in out
        assert 'Tasks' not in out


def _make_static_report(**overrides) -> StaticAnalysisReport:
    payload = {
        'sample': {'sample': _SAMPLE_ID, 'kind': 'file', 'size': 483523, 'target': 'invoice.zip'},
        'task': {'task': 'static1', 'target': 'invoice.zip'},
        'analysis': {'score': 8, 'tags': ['family:darkcomet', 'rat']},
        'signatures': [
            {'name': 'Suspicious packer', 'score': 5},
            {'name': 'Darkcomet', 'score': 10},
        ],
        'files': [
            {
                'filename': 'invoice.exe',
                'kind': 'pe',
                'filesize': 482000,
                'sha256': _SHA256,
                'selected': True,
            },
            {'filename': 'readme.txt', 'kind': 'txt', 'filesize': 1200},
        ],
        'extracted': [
            {'config': {'family': 'darkcomet', 'c2': ['kvejo991.ddns.net:1604'], 'botnet': 'AP'}},
        ],
        'unpack_count': 2,
        'error_count': 0,
    }
    payload.update(overrides)
    return StaticAnalysisReport.model_validate(payload)


_RICH_STATIC_REPORT = _make_static_report()
_SPARSE_STATIC_REPORT = StaticAnalysisReport.model_validate(
    {
        'sample': {'sample': 'sparse-id', 'kind': 'url'},
        'task': {'task': 'static1'},
        'analysis': {},
        'signatures': None,
        'files': None,
        'extracted': None,
    }
)


def _run_static(capsys, report=_RICH_STATIC_REPORT, pretty=False):
    with (
        _patched_mgr() as mock_mgr_cls,
        patch.dict(os.environ, {'COLUMNS': '250'}),
    ):
        mock_mgr_cls.return_value.fetch_sample_static_report.return_value = report
        fetch_static_report(_SAMPLE_ID, pretty=pretty)
    return capsys.readouterr().out


def _run_static_with_error(capsys, error, sample_id=_SAMPLE_ID):
    with _patched_mgr() as mock_mgr_cls:
        mock_mgr_cls.return_value.fetch_sample_static_report.side_effect = error
        with pytest.raises(SystemExit) as exc_info:
            fetch_static_report(sample_id, pretty=False)
    return exc_info.value.code, capsys.readouterr()


def _static_error_with_status(status_code) -> SampleStaticReportError:
    """Build the error as psengine raises it: chained from an HTTPError with a response."""
    error = SampleStaticReportError('404 Client Error: Not Found for url: …')
    error.__cause__ = HTTPError(response=MagicMock(status_code=status_code))
    return error


class TestStaticJson:
    def test_default_outputs_json(self, capsys):
        data = json.loads(_run_static(capsys))
        assert data['analysis']['score'] == 8
        assert data['unpack_count'] == 2
        assert data['error_count'] == 0

    def test_fetch_called_with_sample_id(self, capsys):
        with _patched_mgr() as mock_mgr_cls:
            mock_mgr_cls.return_value.fetch_sample_static_report.return_value = _RICH_STATIC_REPORT
            fetch_static_report(_SAMPLE_ID, pretty=False)
        capsys.readouterr()
        mock_mgr_cls.return_value.fetch_sample_static_report.assert_called_once_with(_SAMPLE_ID)

    def test_json_contains_files(self, capsys):
        data = json.loads(_run_static(capsys))
        assert data['files'][0]['filename'] == 'invoice.exe'
        assert data['files'][0]['sha256'] == _SHA256
        assert data['files'][0]['selected'] is True

    def test_json_contains_extracted_config(self, capsys):
        data = json.loads(_run_static(capsys))
        assert data['extracted'][0]['config']['c2'] == ['kvejo991.ddns.net:1604']

    def test_null_lists_serialise_as_empty(self, capsys):
        data = json.loads(_run_static(capsys, report=_SPARSE_STATIC_REPORT))
        assert data['files'] == []
        assert data['signatures'] == []
        assert data['extracted'] == []


class TestStaticPretty:
    def test_pretty_shows_verdict_header(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert _SAMPLE_ID in out
        assert 'SCORE 8' in out
        assert 'MALICIOUS' in out

    def test_pretty_shows_tags(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert 'family:darkcomet' in out

    def test_pretty_shows_target_and_counts(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert 'invoice.zip' in out
        assert 'Unpacked: 2' in out
        assert 'Errors: 0' in out

    def test_pretty_shows_files_with_full_hash_and_raw_size(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert 'invoice.exe' in out
        assert 'readme.txt' in out
        assert _SHA256 in out
        assert '482000' in out

    def test_pretty_marks_selected_files(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert '✓' in out

    def test_pretty_shows_signatures(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert 'Darkcomet' in out
        assert 'Suspicious packer' in out

    def test_pretty_signatures_sorted_by_score(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert out.index('Darkcomet') < out.index('Suspicious packer')

    def test_pretty_shows_extracted_config(self, capsys):
        out = _run_static(capsys, pretty=True)
        assert 'kvejo991.ddns.net:1604' in out
        assert 'AP' in out

    def test_pretty_is_not_json(self, capsys):
        out = _run_static(capsys, pretty=True)
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_pretty_truncates_long_file_list(self, capsys):
        files = [{'filename': f'file-{i:02d}.exe'} for i in range(1, 13)]
        out = _run_static(capsys, report=_make_static_report(files=files), pretty=True)
        assert 'file-01.exe' in out
        assert 'file-10.exe' in out
        assert 'file-11.exe' not in out
        assert 'more' in out

    def test_pretty_truncates_long_signature_list(self, capsys):
        signatures = [{'name': f'signature-{i:02d}', 'score': 20 - i} for i in range(1, 13)]
        out = _run_static(capsys, report=_make_static_report(signatures=signatures), pretty=True)
        assert 'signature-01' in out
        assert 'signature-10' in out
        assert 'signature-11' not in out
        assert 'more' in out

    def test_pretty_escapes_markup_in_report_data(self, capsys):
        report = _make_static_report(
            analysis={'score': 8, 'tags': ['[red]fake[/red]']},
            signatures=[{'name': 'bad [/closes] tag', 'score': 5}],
            files=[{'filename': 'evil[link=http://x]hi[/link].exe'}],
        )
        out = _run_static(capsys, report=report, pretty=True)
        assert '[red]fake[/red]' in out
        assert 'bad [/closes] tag' in out
        assert 'evil[link=http://x]hi[/link].exe' in out

    def test_pretty_sparse_report_renders(self, capsys):
        out = _run_static(capsys, report=_SPARSE_STATIC_REPORT, pretty=True)
        assert 'sparse-id' in out
        assert 'UNKNOWN' in out

    def test_pretty_sparse_report_omits_empty_sections(self, capsys):
        out = _run_static(capsys, report=_SPARSE_STATIC_REPORT, pretty=True)
        assert 'Files' not in out
        assert 'Signatures' not in out
        assert 'Extracted' not in out


class TestStaticErrors:
    def test_404_reports_sample_not_found(self, capsys):
        code, captured = _run_static_with_error(capsys, _static_error_with_status(404))
        assert code == 1
        assert f'Sample not found: {_SAMPLE_ID}' in captured.err

    def test_non_404_http_error_reports_failure(self, capsys):
        code, captured = _run_static_with_error(capsys, _static_error_with_status(500))
        assert code == 1
        assert 'Failed to fetch static report' in captured.err

    def test_error_without_response_reports_failure(self, capsys):
        code, captured = _run_static_with_error(capsys, SampleStaticReportError('conn refused'))
        assert code == 1
        assert 'Failed to fetch static report' in captured.err
        assert 'conn refused' in captured.err

    def test_error_messages_escape_markup(self, capsys):
        _, captured = _run_static_with_error(
            capsys, _static_error_with_status(404), sample_id='odd[/id]'
        )
        assert 'Sample not found: odd[/id]' in captured.err

    def test_errors_never_pollute_stdout(self, capsys):
        _, captured = _run_static_with_error(capsys, _static_error_with_status(500))
        assert captured.out == ''


def _make_behavioral_report(task_id='behavioral1', **overrides) -> BehavioralReport:
    payload = {
        'task_id': task_id,
        'sample': {'id': _SAMPLE_ID, 'score': 10, 'target': 'invoice.exe', 'sha256': _SHA256},
        'task': {'target': 'invoice.exe'},
        'analysis': {
            'score': 10,
            'tags': ['family:darkcomet', 'rat'],
            'ttp': ['T1547.004'],
            'platform': 'windows10-2004_x64',
        },
        'signatures': [
            {'name': 'Modifies WinLogon for persistence', 'score': 10, 'ttp': ['T1547.004']},
            {'name': 'Darkcomet', 'score': 10, 'ttp': ['T1219']},
        ],
        'processes': [
            {'pid': 1204, 'ppid': 8, 'cmd': 'cmd.exe /c start payload.exe'},
            {'pid': 3320, 'ppid': 1204, 'cmd': ['payload.exe', '-x'], 'image': 'payload.exe'},
        ],
        'network': {
            'flows': [
                {
                    'id': 1,
                    'dst': '45.9.74.12:443',
                    'proto': 'tcp',
                    'domain': 'evil.example',
                    'tls_sni': 'evil.example',
                },
            ],
            'requests': [{'flow': 1, 'dns_request': {'domains': ['evil.example']}}],
            'ips': {'45.9.74.12': {'cc': 'RU', 'asn': 'AS12345'}},
        },
        'dumped': [{'name': 'memory/1204-0.dmp', 'kind': 'region'}],
        'extracted': [
            {'config': {'family': 'darkcomet', 'c2': ['kvejo991.ddns.net:1604'], 'botnet': 'AP'}},
        ],
    }
    payload.update(overrides)
    return BehavioralReport.model_validate(payload)


_RICH_BEHAVIORAL_REPORTS = [_make_behavioral_report()]
_SPARSE_BEHAVIORAL_REPORT = BehavioralReport.model_validate(
    {
        'task_id': 'behavioral1',
        'sample': {'id': 'sparse-id'},
        'task': {},
        'analysis': {},
        'tags': None,
    }
)


def _run_behavioral(capsys, reports=_RICH_BEHAVIORAL_REPORTS, pretty=False):
    with (
        _patched_mgr() as mock_mgr_cls,
        patch.dict(os.environ, {'COLUMNS': '250'}),
    ):
        mock_mgr_cls.return_value.fetch_behavioral_reports.return_value = reports
        fetch_behavioral_reports(_SAMPLE_ID, pretty=pretty)
    return capsys.readouterr()


def _run_behavioral_with_error(capsys, error, sample_id=_SAMPLE_ID):
    with _patched_mgr() as mock_mgr_cls:
        mock_mgr_cls.return_value.fetch_behavioral_reports.side_effect = error
        with pytest.raises(SystemExit) as exc_info:
            fetch_behavioral_reports(sample_id, pretty=False)
    return exc_info.value.code, capsys.readouterr()


def _behavioral_error_with_status(status_code) -> SampleBehavioralReportError:
    """Build the error as psengine raises it: chained from an HTTPError with a response."""
    error = SampleBehavioralReportError('404 Client Error: Not Found for url: …')
    error.__cause__ = HTTPError(response=MagicMock(status_code=status_code))
    return error


class TestBehavioralJson:
    def test_default_outputs_json_array(self, capsys):
        data = json.loads(_run_behavioral(capsys).out)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['analysis']['score'] == 10

    def test_task_id_populated_on_each_report(self, capsys):
        reports = [_make_behavioral_report('behavioral1'), _make_behavioral_report('behavioral2')]
        data = json.loads(_run_behavioral(capsys, reports=reports).out)
        assert [r['task_id'] for r in data] == ['behavioral1', 'behavioral2']

    def test_fetch_called_with_sample_id_and_workers(self, capsys):
        with _patched_mgr() as mock_mgr_cls:
            mock_mgr_cls.return_value.fetch_behavioral_reports.return_value = (
                _RICH_BEHAVIORAL_REPORTS
            )
            fetch_behavioral_reports(_SAMPLE_ID, pretty=False)
        capsys.readouterr()
        mock_mgr_cls.return_value.fetch_behavioral_reports.assert_called_once_with(
            _SAMPLE_ID, max_workers=10
        )

    def test_serialises_by_alias(self, capsys):
        """Sample id_ field must appear as 'id' in JSON output (by_alias=True)."""
        data = json.loads(_run_behavioral(capsys).out)
        assert data[0]['sample']['id'] == _SAMPLE_ID
        assert 'id_' not in data[0]['sample']

    def test_json_contains_network_flows(self, capsys):
        data = json.loads(_run_behavioral(capsys).out)
        assert data[0]['network']['flows'][0]['dst'] == '45.9.74.12:443'

    def test_no_tasks_prints_empty_array_and_note(self, capsys):
        captured = _run_behavioral(capsys, reports=[])
        assert json.loads(captured.out) == []
        assert 'No behavioral tasks' in captured.err


class TestBehavioralPretty:
    def test_pretty_shows_task_header(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert 'behavioral1' in out
        assert 'SCORE 10' in out
        assert 'MALICIOUS' in out
        assert 'windows10-2004_x64' in out

    def test_pretty_shows_tags_and_counts(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert 'family:darkcomet' in out
        assert 'Requests: 1' in out
        assert 'IPs: 1' in out
        assert 'Dumped: 1' in out

    def test_pretty_shows_signatures_with_ttp(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert 'Darkcomet' in out
        assert 'T1547.004' in out

    def test_pretty_shows_processes(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert '1204' in out
        assert 'cmd.exe /c start payload.exe' in out
        assert 'payload.exe -x' in out

    def test_pretty_shows_network_flows(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert '45.9.74.12:443' in out
        assert 'evil.example' in out
        assert 'tcp' in out

    def test_pretty_shows_extracted_config(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        assert 'kvejo991.ddns.net:1604' in out

    def test_pretty_renders_block_per_task(self, capsys):
        reports = [_make_behavioral_report('behavioral1'), _make_behavioral_report('behavioral2')]
        out = _run_behavioral(capsys, reports=reports, pretty=True).out
        assert 'behavioral1' in out
        assert 'behavioral2' in out

    def test_pretty_is_not_json(self, capsys):
        out = _run_behavioral(capsys, pretty=True).out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_pretty_truncates_long_process_list(self, capsys):
        processes = [{'pid': i, 'cmd': f'proc-{i:02d}.exe'} for i in range(1, 13)]
        report = _make_behavioral_report(processes=processes)
        out = _run_behavioral(capsys, reports=[report], pretty=True).out
        assert 'proc-01.exe' in out
        assert 'proc-10.exe' in out
        assert 'proc-11.exe' not in out
        assert 'more' in out

    def test_pretty_escapes_markup_in_report_data(self, capsys):
        report = _make_behavioral_report(
            analysis={'score': 10, 'tags': ['[red]fake[/red]']},
            signatures=[{'name': 'bad [/closes] tag', 'score': 5}],
            processes=[{'pid': 1, 'cmd': 'evil [link=http://x]hi[/link].exe'}],
        )
        out = _run_behavioral(capsys, reports=[report], pretty=True).out
        assert '[red]fake[/red]' in out
        assert 'bad [/closes] tag' in out
        assert 'evil [link=http://x]hi[/link].exe' in out

    def test_pretty_sparse_report_renders(self, capsys):
        out = _run_behavioral(capsys, reports=[_SPARSE_BEHAVIORAL_REPORT], pretty=True).out
        assert 'behavioral1' in out
        assert 'UNKNOWN' in out

    def test_pretty_sparse_report_omits_empty_sections(self, capsys):
        out = _run_behavioral(capsys, reports=[_SPARSE_BEHAVIORAL_REPORT], pretty=True).out
        assert 'Signatures' not in out
        assert 'Processes' not in out
        assert 'flows' not in out
        assert 'Extracted' not in out
        assert 'Requests:' not in out

    def test_pretty_shows_failed_task_errors(self, capsys):
        report = BehavioralReport.model_validate(
            {
                'task_id': 'behavioral2',
                'sample': {'id': _SAMPLE_ID},
                'task': {},
                'analysis': {},
                'errors': [{'task': 'behavioral2', 'reason': 'detonation timed out'}],
            }
        )
        out = _run_behavioral(capsys, reports=[report], pretty=True).out
        assert 'detonation timed out' in out

    def test_pretty_no_tasks_prints_note_only(self, capsys):
        captured = _run_behavioral(capsys, reports=[], pretty=True)
        assert captured.out == ''
        assert 'No behavioral tasks' in captured.err


class TestBehavioralErrors:
    def test_404_reports_sample_not_found(self, capsys):
        code, captured = _run_behavioral_with_error(capsys, _behavioral_error_with_status(404))
        assert code == 1
        assert f'Sample not found: {_SAMPLE_ID}' in captured.err

    def test_non_404_http_error_reports_failure(self, capsys):
        code, captured = _run_behavioral_with_error(capsys, _behavioral_error_with_status(500))
        assert code == 1
        assert 'Failed to fetch behavioral reports' in captured.err

    def test_error_without_response_reports_failure(self, capsys):
        code, captured = _run_behavioral_with_error(
            capsys, SampleBehavioralReportError('conn refused')
        )
        assert code == 1
        assert 'Failed to fetch behavioral reports' in captured.err
        assert 'conn refused' in captured.err

    def test_error_messages_escape_markup(self, capsys):
        _, captured = _run_behavioral_with_error(
            capsys, _behavioral_error_with_status(404), sample_id='odd[/id]'
        )
        assert 'Sample not found: odd[/id]' in captured.err

    def test_errors_never_pollute_stdout(self, capsys):
        _, captured = _run_behavioral_with_error(capsys, _behavioral_error_with_status(500))
        assert captured.out == ''


class TestOverviewErrors:
    def test_report_not_available_exits_1_with_message(self, capsys):
        code, captured = _run_with_error(capsys, SampleReportNotAvailableError('not ready'))
        assert code == 1
        assert 'Analysis not complete' in captured.err
        assert 'reported' in captured.err

    def test_sample_not_found_exits_1_with_message(self, capsys):
        code, captured = _run_with_error(capsys, SampleReportNotFoundError('no sample'))
        assert code == 1
        assert f'Sample not found: {_SAMPLE_ID}' in captured.err

    def test_other_overview_error_exits_1_with_message(self, capsys):
        code, captured = _run_with_error(capsys, SampleOverviewError('API down'))
        assert code == 1
        assert 'Failed to fetch overview report' in captured.err
        assert 'API down' in captured.err

    def test_error_messages_escape_markup(self, capsys):
        """Bracket-laden ids/exception text must not be parsed as Rich markup."""
        with _patched_mgr() as mock_mgr_cls:
            mock_mgr_cls.return_value.fetch_sample_overview_report.side_effect = (
                SampleReportNotFoundError('nope')
            )
            with pytest.raises(SystemExit):
                fetch_overview_report('odd[/id]', pretty=False)
        assert 'Sample not found: odd[/id]' in capsys.readouterr().err

    def test_errors_never_pollute_stdout(self, capsys):
        _, captured = _run_with_error(capsys, SampleOverviewError('API down'))
        assert captured.out == ''
