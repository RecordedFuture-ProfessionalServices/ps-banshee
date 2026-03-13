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

from psengine.entity_lists import EntityListMgr, ListApiError
from rich.progress import Progress, SpinnerColumn, TextColumn

from .list_helpers import api_error_cause


def fetch_list(list_id: str):
    """Clears the list of all entities (text entries can't be removed via API)."""
    list_mgr = EntityListMgr()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(description='Fetching list information...', total=None)
        try:
            entity_list = list_mgr.fetch(list_=list_id)
        except ListApiError as err:
            err.message = f'Failed to fetch list "{list_id}". {api_error_cause(err)}'
            raise err
        return entity_list
