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
from psengine.entity_lists import EntityList, ListApiError, ListEntity
from psengine.helpers import MultiThreadingHelper
from rich.progress import Progress, SpinnerColumn, TextColumn

from .fetch_list import fetch_list
from .list_bulk_remove import produce_results as produce_remove_results
from .list_helpers import (
    UNCHANGED,
    handle_list_api_error,
    print_list_results,
    process_result,
)

MAX_WORKERS = 50
CHUNK_SIZE = 100


def add_helper(entity: Union[str, tuple[str, str]], entity_list: EntityList):
    try:
        result = entity_list.add(entity=entity)
    except ListApiError as err:
        return handle_list_api_error(err, entity)
    return process_result(result, entity, 'add')


def produce_results(
    chunk: list[Union[str, tuple[str, str]]],
    entity_list: EntityList,
    final_results: dict[str, list[Union[str, tuple[str, str]]]],
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


def _find_entities_to_remove(
    pre_existing_entities: list[ListEntity],
    provided_entities: list[Union[str, tuple[str, str]]],
) -> list[str]:
    provided_ids = {entity for entity in provided_entities if isinstance(entity, str)}
    provided_name_type = {
        (entity[0], entity[1].lower())
        for entity in provided_entities
        if isinstance(entity, (tuple, list))
    }

    to_remove = []
    for existing_entity in pre_existing_entities:
        in_provided = (
            existing_entity.entity.id_ in provided_ids
            or (existing_entity.entity.name, existing_entity.entity.type_.lower())
            in provided_name_type
        )
        if not in_provided:
            to_remove.append(existing_entity.entity.id_)

    return to_remove


def _find_entities_to_add(
    pre_existing_entities: list[ListEntity],
    provided_entities: list[Union[str, tuple[str, str]]],
) -> list[Union[str, tuple[str, str]]]:
    existing_ids = {existing_entity.entity.id_ for existing_entity in pre_existing_entities}
    existing_name_type = {
        (existing_entity.entity.name, existing_entity.entity.type_.lower())
        for existing_entity in pre_existing_entities
    }

    to_add = []
    for entity in provided_entities:
        if isinstance(entity, (tuple, list)):
            if (entity[0], entity[1].lower()) not in existing_name_type:
                to_add.append(entity)
        else:
            if entity not in existing_ids:
                to_add.append(entity)

    return to_add


def bulk_add_entities(
    list_id: str, entities: list[Union[str, tuple[str, str]]], overwrite: bool = False
):
    entity_list = fetch_list(list_id)
    pre_existing_entities = entity_list.entities()

    # Dedup user input
    entities = list({tuple(e) if isinstance(e, list) else e for e in entities})

    # Filter for entities to add and remove based on pre-existing entities in the list.
    # This is done to provide more accurate reporting at the end,
    # and to speed up the command (we dont waste time trying to add)
    entities_to_add = _find_entities_to_add(pre_existing_entities, entities)
    existing_entities = [entity for entity in entities if entity not in entities_to_add]

    add_chunks = list(chunked(entities_to_add, CHUNK_SIZE))
    final_results = {}
    if existing_entities:
        final_results[UNCHANGED] = existing_entities

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description='Adding entities', total=len(add_chunks))
        for chunk in add_chunks:
            final_results = produce_results(chunk, entity_list, final_results)

        if overwrite and pre_existing_entities:
            entities_to_remove = _find_entities_to_remove(pre_existing_entities, entities)
            if entities_to_remove:
                remove_chunks = list(chunked(entities_to_remove, CHUNK_SIZE))
                progress.update(task_id, description='Removing stale entities')
                for chunk in remove_chunks:
                    produce_remove_results(chunk, entity_list, final_results)

    print_list_results(final_results)
