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


import csv
import json
import sys
from pathlib import Path

from psengine.fusion import FusionMgr
from psengine.risklists import RisklistMgr
from psengine.risklists.models import DefaultRiskList
from rich.progress import Progress, SpinnerColumn, TextColumn


def fetch_risklist(
    entity_type: str = None,
    list_: str = None,
    custom_list_path: str = None,
    output_path: str = None,
    as_json: str = None,
):
    if as_json:
        ext = '.json'
    else:
        ext = f'.{custom_list_path.split(".")[-1]}' if custom_list_path else '.csv'

    entity_type = getattr(entity_type, 'value', None) or entity_type or 'custom'
    file_name = list_ or custom_list_path.split('/')[-1].split('.')[0]

    if output_path:
        file_path = Path(output_path)
        if file_path.is_dir():
            file_path = file_path / f'{entity_type}_{file_name}{ext}'
    else:
        file_path = Path.cwd() / f'{entity_type}_{file_name}{ext}'

    try:
        file_path.touch(exist_ok=True)
    except Exception as err:  # noqa: BLE001
        print(f'Unable to create {file_path.as_posix()}. Error: {err}', file=sys.stderr)
        sys.exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description='Fetching risklist')

        if list_:
            mgr = RisklistMgr()
            # Increase CSV field size limit to handle large evidenceDetails (4x default)
            csv.field_size_limit(4 * 131072)  # 512KB
            if as_json:
                risklist = list(mgr.fetch_risklist(list_, entity_type, validate=DefaultRiskList))
                progress.update(
                    task_id, description=f'Writing {len(risklist)} entries to {str(file_path)}'
                )
                file_path.write_text(json.dumps([r.json() for r in risklist], indent=4))
            else:
                risklist = list(mgr.fetch_risklist(list_, entity_type, headers=False))
                progress.update(
                    task_id, description=f'Writing {len(risklist) - 1} entries to {str(file_path)}'
                )
                with file_path.open('w') as f:
                    writer = csv.writer(f)
                    writer.writerows(risklist)
        else:
            mgr = FusionMgr()
            risklist = mgr.get_files(custom_list_path)[0]
            if not risklist.exists:
                print(f"Risklist '{custom_list_path}' not found", file=sys.stderr)
                sys.exit(1)

            progress.update(task_id, description='Writing risklist to disk')
            file_path.write_bytes(risklist.content)

    print(f'File written to: {str(file_path)}')
