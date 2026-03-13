##################################### TERMS OF USE ###########################################
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


import json
import sys
from email.utils import parsedate_to_datetime

from psengine.fusion import FusionMgr
from rich import print_json
from rich.console import Console
from rich.table import Table


def _format_datetime(date_str: str) -> str:
    """Format datetime from HTTP date format to include seconds and timezone."""
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime('%b %d %H:%M:%S %Z')

    except Exception:  # noqa: BLE001
        return date_str


def stat_fusion_file(file_path: str, pretty: bool = False):
    fusion_mgr = FusionMgr()

    head_response = fusion_mgr.head_files(file_paths=file_path)
    response = head_response[0]

    if not pretty:
        response_data = response.json()
        response_data.pop('content-disposition', None)
        response_data.pop('Content-Length', None)
        print_json(json.dumps(response_data), indent=2)

        if not response.exists:
            sys.exit(1)
    else:
        console = Console()

        if not response.exists:
            print(f'File not found {file_path}', file=sys.stderr)
            sys.exit(1)

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row('Path:', file_path)

        if hasattr(response, 'last_modified') and response.last_modified:
            date_str = _format_datetime(response.last_modified)
            table.add_row('Last Modified:', f'[blue]{date_str}[/blue]')

        if hasattr(response, 'etag') and response.etag:
            table.add_row('ETag:', f'[yellow]{response.etag}[/yellow]')

        console.print(table)
