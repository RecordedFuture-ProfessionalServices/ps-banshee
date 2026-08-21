#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pyzipper
from psengine.sandbox.errors import SampleFileFetchError
from rich.console import Console
from rich.markup import escape

from .helpers import get_sandbox_mgr, spinner

_ZIP_PASSWORD = b'infected'
_WARNING = (
    'WARNING: Downloaded files may be malicious. Handle with care. '
    'Samples are wrapped in a ZIP archive encrypted with password `infected` '
    'to prevent accidental detonation.'
)


def _write_infected_zip(dest: Path, entry_name: str, data: bytes) -> None:
    with pyzipper.AESZipFile(
        dest,
        mode='w',
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zf:
        zf.setpassword(_ZIP_PASSWORD)
        zf.writestr(entry_name, data)


def _download_one(sample_id: str, output_dir: Path, err: Console) -> bool:
    tag = f'\\[{escape(sample_id)}]'
    mgr = get_sandbox_mgr()
    try:
        data = mgr.fetch_sample_file(sample_id)
    except SampleFileFetchError as exc:
        err.print(f'{tag} [red]ERROR:[/red] {escape(str(exc))}')
        return False
    dest = output_dir / f'{sample_id}.zip'
    _write_infected_zip(dest, sample_id, data)
    sha256 = hashlib.sha256(data).hexdigest()
    err.print(f'{tag} Saved: {dest} ({len(data)} bytes, sha256={sha256})')
    return True


def download_sandbox_samples(sample_ids: list[str], output_dir: Path, workers: int = 1) -> None:
    err = Console(stderr=True)
    err.print(_WARNING)
    output_dir.mkdir(parents=True, exist_ok=True)

    label = 'Downloading sample' if len(sample_ids) == 1 else 'Downloading samples'
    with spinner(label):
        if workers > 1 and len(sample_ids) > 1:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                results = list(
                    pool.map(lambda sid: _download_one(sid, output_dir, err), sample_ids)
                )
        else:
            results = [_download_one(sid, output_dir, err) for sid in sample_ids]

    ok = sum(results)
    failed = len(results) - ok
    if len(sample_ids) > 1:
        plural = '' if failed == 1 else 's'
        err.print(f'Downloaded {ok}/{len(sample_ids)} samples. {failed} error{plural}.')
    if failed:
        sys.exit(1)
