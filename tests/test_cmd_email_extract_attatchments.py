from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import pyzipper
from typer.testing import CliRunner

from banshee.commands.cmd_email import app
from banshee.email.attatchments_sandbox import (
    _ZIP_PASSWORD,
    extract_attatchments,
    sandbox_attatchments,
)

runner = CliRunner()

TEST_FILES = Path(__file__).parent.parent / 'test_files'
DEMO_EML = TEST_FILES / 'demo.eml'
SIMPLE_EML = TEST_FILES / 'simple.eml'


class TestExtractAttatchments:
    def test_extracts_attachment_and_writes_encrypted_zip(self, tmp_path):
        zip_path = tmp_path / 'out.zip'

        result = extract_attatchments(DEMO_EML, zip_path)

        assert result == ['image.png']
        assert zip_path.exists()

        with pyzipper.AESZipFile(zip_path) as zf:
            zf.setpassword(_ZIP_PASSWORD)
            assert zf.namelist() == ['image.png']
            assert len(zf.read('image.png')) > 0

    def test_zip_requires_password(self, tmp_path):
        zip_path = tmp_path / 'out.zip'
        extract_attatchments(DEMO_EML, zip_path)

        with pyzipper.AESZipFile(zip_path) as zf, pytest.raises(RuntimeError):
            zf.read('image.png')

    def test_no_attachments_returns_empty_list(self, tmp_path):
        zip_path = tmp_path / 'out.zip'

        result = extract_attatchments(SIMPLE_EML, zip_path)

        assert result == []
        assert zip_path.exists()

        with pyzipper.AESZipFile(zip_path) as zf:
            assert zf.namelist() == []

class TestSandboxAttatchments:
    @patch('banshee.email.attatchments_sandbox.SandboxMgr')
    def test_no_attachments_json_output(self, mock_sandbox_cls, tmp_path, capsys):
        sandbox_attatchments(str(SIMPLE_EML), tmp_path, pretty=False)

        captured = capsys.readouterr()
        assert captured.out.strip() == '[]'
        mock_sandbox_cls.assert_not_called()

    @patch('banshee.email.attatchments_sandbox.SandboxMgr')
    def test_no_attachments_pretty_output(self, mock_sandbox_cls, tmp_path, capsys):
        sandbox_attatchments(str(SIMPLE_EML), tmp_path, pretty=True)

        captured = capsys.readouterr()
        assert f'No files were extracted from {SIMPLE_EML}' in captured.out
        mock_sandbox_cls.assert_not_called()

    @patch('banshee.email.attatchments_sandbox.time.sleep')
    @patch('banshee.email.attatchments_sandbox.time.monotonic')
    @patch('banshee.email.attatchments_sandbox.SandboxMgr')
    def test_polling_timeout_reports_failure(
        self, mock_sandbox_cls, mock_monotonic, mock_sleep, tmp_path, capsys
    ):
        mock_monotonic.side_effect = [0, 0, 1000]
        mock_mgr = mock_sandbox_cls.return_value
        mock_mgr.submit_sample.return_value = MagicMock(id_='sample-1')
        mock_mgr.fetch_sample.return_value = MagicMock(status='pending')

        sandbox_attatchments(str(DEMO_EML), tmp_path, pretty=True)

        captured = capsys.readouterr()
        assert 'Failed to get report for submission sample-1. Timed out.' in captured.out
        mock_sleep.assert_called_once()
        mock_mgr.fetch_sample_summary.assert_not_called()


class TestCmdEmailExtractAttatchments:
    @patch('banshee.commands.cmd_email.sandbox_attatchments')
    def test_invokes_sandbox_attatchments_with_defaults(self, mock_sandbox, tmp_path):
        result = runner.invoke(app, ['extract-attatchments', str(DEMO_EML), "-z", str(tmp_path)])

        assert result.exit_code == 0
        mock_sandbox.assert_called_once_with(str(DEMO_EML), tmp_path, False)

    @patch('banshee.commands.cmd_email.sandbox_attatchments')
    def test_invokes_sandbox_attatchments_with_pretty(self, mock_sandbox, tmp_path):

        result = runner.invoke(app, ['extract-attatchments', str(DEMO_EML), '-z', str(tmp_path), '-p'])

        assert result.exit_code == 0
        mock_sandbox.assert_called_once_with(str(DEMO_EML), tmp_path, True)

    def test_help_available(self):
        result = runner.invoke(app, ['extract-attatchments', '--help'])

        assert result.exit_code == 0
        assert 'Path to eml file' in result.output

