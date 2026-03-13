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


import json

from psengine.rf_client import RFClient
from rich import print_json
from rich.console import Console
from rich.table import Table

from ..fusion_files import stat_fusion_file


def stat_risklist(
    entity_type: str = None, list_: str = None, custom_list_path: str = None, pretty: bool = False
):
    if custom_list_path:
        stat_fusion_file(file_path=custom_list_path, pretty=pretty)
    else:
        entity_type = entity_type.value
        rf_client = RFClient()
        url = f'https://api.recordedfuture.com/v2/{entity_type}/risklist'
        params = {'list': list_}

        response = rf_client.request('HEAD', url, params=params)

        if not pretty:
            filtered_headers = {
                'name': f'{list_}_{entity_type}_risklist',
                'exists': response.status_code == 200,
                'etag': response.headers.get('etag', '').strip('"'),
            }
            print_json(json.dumps(filtered_headers, indent=2))
        else:
            console = Console()
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column('Property', style='cyan bold', no_wrap=True)
            table.add_column('Value', style='white')

            if list_:
                table.add_row('Name:', f'{list_}_{entity_type}_risklist')

            if 'etag' in response.headers:
                etag = response.headers['etag'].strip('"')
                table.add_row('ETag:', f'[yellow]{etag}[/yellow]')

            console.print(table)
