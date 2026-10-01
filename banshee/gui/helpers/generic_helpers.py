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

import os
import tkinter as tk
from pathlib import Path


def load_image(filename: str, max_width: int | None = 1, max_height: int | None = 1):
    """Load a PNG from the assets directory."""
    path = Path(__file__).parent.parent / 'assets' / filename
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
