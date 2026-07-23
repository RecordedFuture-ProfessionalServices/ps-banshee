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

from unittest.mock import MagicMock, patch

import pytest
from psengine.sandbox.errors import SampleDeleteError
from psengine.sandbox.sandbox import SampleDeleteOut

from banshee.sandbox.delete import delete_sandbox_sample

_SAMPLE_ID = '260501-h4p7laawme'

_PROGRESS_MOCK = MagicMock()
_SPINNER_MOCK = MagicMock(
    return_value=MagicMock(
        __enter__=MagicMock(return_value=_PROGRESS_MOCK),
        __exit__=MagicMock(return_value=False),
    )
)

_PATCH_SPINNER = patch('banshee.sandbox.delete._spinner', _SPINNER_MOCK)
_PATCH_MGR = patch('banshee.sandbox.delete.SandboxMgr')
_PATCH_CFG = patch('banshee.sandbox.delete.get_config')


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_success_prints_deleted(mock_cfg, mock_mgr, capsys):  # noqa: ARG001
    mock_mgr.return_value.delete_sample.return_value = SampleDeleteOut(deleted=True)
    delete_sandbox_sample(_SAMPLE_ID)
    assert f'Deleted: {_SAMPLE_ID}' in capsys.readouterr().out


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_success_uses_sandbox_choice(mock_cfg, mock_mgr):
    mock_cfg.return_value.sandbox_choice = 'eu'
    mock_mgr.return_value.delete_sample.return_value = SampleDeleteOut(deleted=True)
    delete_sandbox_sample(_SAMPLE_ID)
    mock_mgr.assert_called_once_with(sandbox_choice='eu')


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_success_calls_delete_sample_with_id(mock_cfg, mock_mgr):  # noqa: ARG001
    mock_mgr.return_value.delete_sample.return_value = SampleDeleteOut(deleted=True)
    delete_sandbox_sample(_SAMPLE_ID)
    mock_mgr.return_value.delete_sample.assert_called_once_with(_SAMPLE_ID)


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_delete_error_exits_1(mock_cfg, mock_mgr):  # noqa: ARG001
    mock_mgr.return_value.delete_sample.side_effect = SampleDeleteError('401 Unauthorized')
    with pytest.raises(SystemExit) as exc_info:
        delete_sandbox_sample(_SAMPLE_ID)
    assert exc_info.value.code == 1


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_delete_error_prints_to_stderr(mock_cfg, mock_mgr, capsys):  # noqa: ARG001
    mock_mgr.return_value.delete_sample.side_effect = SampleDeleteError('401 Unauthorized')
    with pytest.raises(SystemExit):
        delete_sandbox_sample(_SAMPLE_ID)
    assert '401 Unauthorized' in capsys.readouterr().err


@_PATCH_SPINNER
@_PATCH_MGR
@_PATCH_CFG
def test_delete_error_nothing_on_stdout(mock_cfg, mock_mgr, capsys):  # noqa: ARG001
    mock_mgr.return_value.delete_sample.side_effect = SampleDeleteError('401 Unauthorized')
    with pytest.raises(SystemExit):
        delete_sandbox_sample(_SAMPLE_ID)
    assert capsys.readouterr().out == ''
