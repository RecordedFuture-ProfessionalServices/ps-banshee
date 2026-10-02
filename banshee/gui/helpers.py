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

"""Helpers and widgets that can be used within the GUI."""

import json
import os
import sys
import threading
import tkinter as tk
from pathlib import Path

from typer.testing import CliRunner

from banshee.main import app as banshee_app

_INVOKE_LOCK = threading.Lock()


def load_image(filename: str, max_width: int | None = 1, max_height: int | None = 1):
    """Load a PNG from the assets directory."""
    path = Path(__file__).parent / 'assets' / filename
    if not path.exists():
        return None

    try:
        img = tk.PhotoImage(file=path)
    except tk.TclError:
        return None

    fx = img.width() // max_width + 1
    fy = img.height() // max_height + 1
    factor = max(fx, fy, 1)
    if factor > 1:
        img = img.subsample(factor, factor)
    return img


def test_api_token():
    return bool(os.environ.get('RF_TOKEN'))


def command_runner(args: list[str], stdin_text: str | None = None):
    """Run a banshee command and return stdout and stderr."""
    app = banshee_app

    os.environ['COLUMNS'] = '200'
    runner = CliRunner(mix_stderr=False)

    saved_hook, saved_args = sys.excepthook, sys.argv
    with _INVOKE_LOCK:
        try:
            sys.argv = ['banshee', *args]
            result = runner.invoke(app, list(args), input=stdin_text, catch_exceptions=True)
        except Exception as e:  # noqa: BLE001
            return '', f'Failed to run Banshee: {repr(e)}'
        finally:
            sys.excepthook, sys.argv = saved_hook, saved_args

    out = result.stdout or ''
    err = result.stderr or ''

    if result.exit_code != 0:
        if result.exception is not None and isinstance(exec, SystemExit):
            message = f'{type(result.exception).__name__}: {result.exception}'
            err = f'{err}\n{message}'.strip() if err.strip() else message
        elif not result.exception.strip():
            err = f'banshee exited with status code {result.exit_code}'

    return out, err


def pretty_json(raw: str):
    """Convert a JSON String to a nicely formatted string (with indentation)."""
    return json.dumps(json.loads(raw), indent=2)
