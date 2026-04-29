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


from typing import Union

from more_itertools import chunked
from psengine.entity_lists import EntityList, ListApiError
from psengine.helpers import MultiThreadingHelper
from rich.progress import Progress, SpinnerColumn, TextColumn, track

from .fetch_list import fetch_list
from .list_helpers import (
    handle_list_api_error,
    process_result,
)

MAX_WORKERS = 50
CHUNK_SIZE = 100


def add_helper(entity: str, entity_list: EntityList):
    try:
        result = entity_list.add(entity=entity)
    except ListApiError as err:
        return handle_list_api_error(err, entity)
    return process_result(result, entity, 'add')


def produce_results(
    chunk: list[Union[str, tuple[str, str]]],
    entity_list: EntityList,
    final_results: dict[str, list[str]],
):
    results = MultiThreadingHelper.multithread_it(
        MAX_WORKERS, add_helper, iterator=chunk, entity_list=entity_list
    )
    for result in results:
        if result[0] not in final_results:
            final_results[result[0]] = [result[1]]
        else:
            final_results[result[0]].append(result[1])

    return final_results


def bulk_add_entities(list_id: str, entities: list[Union[str, tuple[str, str]]]):
    entity_list = fetch_list(list_id)

    # Dedup
    entities = list({tuple(e) if isinstance(e, list) else e for e in entities})

    chunks = list(chunked(entities, CHUNK_SIZE))
    final_results = {}
    if len(chunks) > 1:
        for i in track(range(len(chunks)), description='Adding entities'):
            final_results = produce_results(chunks[i], entity_list, final_results)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}'),
            transient=True,
        ) as progress:
            progress.add_task(description='Adding entities')
            final_results = produce_results(chunks[0], entity_list, final_results)

    for result, entities in final_results.items():
        printable_entities = []
        for entity in entities:
            if isinstance(entity, (tuple, list)):
                printable_entities.append(f'{entity[0]}:{entity[1]}')
            else:
                printable_entities.append(entity)
        if len(entities) > 0:
            print(result.upper() + ':\n' + '\n'.join(printable_entities))
