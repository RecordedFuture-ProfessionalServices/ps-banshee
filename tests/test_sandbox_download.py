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

import hashlib
from unittest.mock import MagicMock, patch

import pytest
import pyzipper
from psengine.sandbox.errors import SampleFileFetchError

from banshee.sandbox.download import _write_infected_zip, download_sandbox_samples

_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=None),
        __exit__=MagicMock(return_value=False),
    )
)

_SAMPLE_BYTES = b'MZ\x90\x00' + b'\x00' * 60 + b'fake-pe-payload'
_SAMPLE_ID = '260821-mky3lsys2f'


class TestWriteInfectedZip:
    def test_zip_created_with_expected_name(self, tmp_path):
        dest = tmp_path / f'{_SAMPLE_ID}.zip'
        _write_infected_zip(dest, _SAMPLE_ID, _SAMPLE_BYTES)
        assert dest.exists()

    def test_zip_contents_match_input_bytes(self, tmp_path):
        dest = tmp_path / f'{_SAMPLE_ID}.zip'
        _write_infected_zip(dest, _SAMPLE_ID, _SAMPLE_BYTES)
        with pyzipper.AESZipFile(dest) as zf:
            zf.setpassword(b'infected')
            assert zf.read(_SAMPLE_ID) == _SAMPLE_BYTES

    def test_zip_refuses_wrong_password(self, tmp_path):
        dest = tmp_path / f'{_SAMPLE_ID}.zip'
        _write_infected_zip(dest, _SAMPLE_ID, _SAMPLE_BYTES)
        with pyzipper.AESZipFile(dest) as zf:
            zf.setpassword(b'wrong')
            with pytest.raises(RuntimeError):
                zf.read(_SAMPLE_ID)

    def test_zip_refuses_no_password(self, tmp_path):
        dest = tmp_path / f'{_SAMPLE_ID}.zip'
        _write_infected_zip(dest, _SAMPLE_ID, _SAMPLE_BYTES)
        with pyzipper.AESZipFile(dest) as zf, pytest.raises(RuntimeError):
            zf.read(_SAMPLE_ID)


class TestDownloadSandboxSamples:
    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_single_sample_creates_encrypted_zip(self, mock_mgr_cls, tmp_path):
        mock_mgr_cls.return_value.fetch_sample_file.return_value = _SAMPLE_BYTES
        download_sandbox_samples([_SAMPLE_ID], output_dir=tmp_path)
        dest = tmp_path / f'{_SAMPLE_ID}.zip'
        assert dest.exists()
        with pyzipper.AESZipFile(dest) as zf:
            zf.setpassword(b'infected')
            assert zf.read(_SAMPLE_ID) == _SAMPLE_BYTES

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_output_dir_created_if_missing(self, mock_mgr_cls, tmp_path):
        mock_mgr_cls.return_value.fetch_sample_file.return_value = _SAMPLE_BYTES
        target = tmp_path / 'new' / 'nested' / 'dir'
        download_sandbox_samples([_SAMPLE_ID], output_dir=target)
        assert target.exists()
        assert (target / f'{_SAMPLE_ID}.zip').exists()

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_warning_and_sha256_line_written_to_stderr(self, mock_mgr_cls, tmp_path, capsys):
        mock_mgr_cls.return_value.fetch_sample_file.return_value = _SAMPLE_BYTES
        download_sandbox_samples([_SAMPLE_ID], output_dir=tmp_path)
        err = capsys.readouterr().err
        assert 'WARNING' in err
        assert 'infected' in err
        assert _SAMPLE_ID in err
        assert hashlib.sha256(_SAMPLE_BYTES).hexdigest() in err

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_all_success_exits_zero(self, mock_mgr_cls, tmp_path):
        mock_mgr_cls.return_value.fetch_sample_file.return_value = _SAMPLE_BYTES
        download_sandbox_samples(['id1', 'id2'], output_dir=tmp_path)
        assert (tmp_path / 'id1.zip').exists()
        assert (tmp_path / 'id2.zip').exists()

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_partial_failure_continues_batch_and_exits_1(self, mock_mgr_cls, tmp_path, capsys):
        def fetch(sid):
            if sid == 'bad':
                raise SampleFileFetchError('404 not found')
            return _SAMPLE_BYTES

        mock_mgr_cls.return_value.fetch_sample_file.side_effect = fetch
        with pytest.raises(SystemExit) as exc:
            download_sandbox_samples(['id1', 'bad', 'id2'], output_dir=tmp_path)
        assert exc.value.code == 1
        assert (tmp_path / 'id1.zip').exists()
        assert (tmp_path / 'id2.zip').exists()
        assert not (tmp_path / 'bad.zip').exists()
        err = capsys.readouterr().err
        assert '[bad]' in err
        assert 'ERROR' in err
        assert 'Downloaded 2/3 samples' in err

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_all_failed_exits_1(self, mock_mgr_cls, tmp_path):
        mock_mgr_cls.return_value.fetch_sample_file.side_effect = SampleFileFetchError('404')
        with pytest.raises(SystemExit) as exc:
            download_sandbox_samples(['id1'], output_dir=tmp_path)
        assert exc.value.code == 1

    @patch('banshee.sandbox.download.spinner', new=_SPINNER_MOCK)
    @patch('banshee.sandbox.helpers.SandboxMgr')
    @patch('banshee.sandbox.helpers.get_config', new=MagicMock())
    def test_workers_parallel_executes_all(self, mock_mgr_cls, tmp_path):
        mock_mgr_cls.return_value.fetch_sample_file.return_value = _SAMPLE_BYTES
        download_sandbox_samples(['id1', 'id2', 'id3'], output_dir=tmp_path, workers=3)
        assert (tmp_path / 'id1.zip').exists()
        assert (tmp_path / 'id2.zip').exists()
        assert (tmp_path / 'id3.zip').exists()
