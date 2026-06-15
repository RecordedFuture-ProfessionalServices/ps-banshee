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


"""Shared helper functions and constants for entity list operations."""

from collections.abc import Mapping, Sequence
from typing import Union

from psengine.entity_lists import ListApiError
from rich.console import Console

# Shared constants
ADDED = 'added'
REMOVED = 'removed'
UNCHANGED = 'unchanged'
UPDATED = 'updated'
ERROR_BAD_ID = 'error_bad_id'
ERROR_NOT_FOUND = 'error_not_found'
ERROR_NOT_ALLOWED = 'error_not_allowed'
ERROR_MULTIPLE_MATCHES = 'error_multiple_matches'
LIST_MAX_SIZE_REACHED = 'list_max_size_reached'


def print_list_results(final_results: Mapping[str, Sequence[Union[str, tuple[str, str]]]]) -> None:
    """Print grouped operation results in a stable, readable format."""
    console = Console()
    first_block = True
    for result in sorted(final_results):
        entities = final_results[result]
        if len(entities) == 0:
            continue

        if not first_block:
            console.print()
        first_block = False

        printable_entities = []
        for entity in entities:
            if isinstance(entity, (tuple, list)):
                printable_entities.append(f'{entity[0]},{entity[1]}')
            else:
                printable_entities.append(entity)

        printable_entities = sorted(printable_entities, key=str.lower)
        console.print(f'[bold]{result.upper()}:[/bold]')
        console.print('\n'.join(printable_entities), highlight=False)


def api_error_cause(err: ListApiError) -> str:
    """Safely extract a human-readable cause string from a ListApiError.

    Args:
        err: The ListApiError exception

    Returns:
        A string describing the cause (status code + message, or fallback to err.message)
    """
    cause = getattr(err, '__cause__', None)
    if cause is None:
        return getattr(err, 'message', str(err))
    return str(cause).replace('\n', ' ')


def handle_list_api_error(err: ListApiError, entity: str) -> tuple[str, str]:
    """Handle ListApiError exceptions and return appropriate error status.

    Args:
        err: The ListApiError exception
        entity: The entity that was being operated on

    Returns:
        A tuple of (error_status, entity)
    """
    # Check if the error has a response attribute (network errors like timeouts don't)
    if hasattr(err.__cause__, 'response') and err.__cause__.response is not None:
        if err.__cause__.response.status_code == 404:
            return (ERROR_NOT_FOUND, entity)
        if err.__cause__.response.status_code == 400:
            # Check if the error is due to max size limit
            response_text = (
                err.__cause__.response.text if hasattr(err.__cause__.response, 'text') else str(err)
            )
            # We might want to move this to PSEngine _list_op() in the future
            if 'max size' in response_text.lower():
                return (LIST_MAX_SIZE_REACHED, entity)
            if 'not allowed to be added' in response_text.lower():
                return (ERROR_NOT_ALLOWED, entity)
            return (ERROR_BAD_ID, entity)
        return ('error_status_' + str(err.__cause__.response.status_code), entity)
    # Handle timeout and other network errors
    error_msg = str(err)
    if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
        return ('error_timeout', entity)
    return ('error_network', entity)


def process_result(result, entity: str, operation: str) -> tuple[str, str]:
    """Process the result from an entity list operation (add or remove).

    Args:
        result: The result object from entity_list.add() or entity_list.remove()
        entity: The entity that was operated on
        operation: The operation being performed ('add' or 'remove')

    Returns:
        A tuple of (status, entity)
    """
    if result.result == ADDED:
        return (ADDED, entity)
    if result.result == REMOVED:
        return (REMOVED, entity)
    if result.result == UNCHANGED:
        return (UNCHANGED, entity)
    if result.result == UPDATED:
        return (UPDATED, entity)
    if result.result.startswith('Multiple matches found'):
        return (ERROR_MULTIPLE_MATCHES, entity)
    if result.result == 'Entity ID not found':
        return (ERROR_NOT_FOUND, entity)
    print(f'Error {operation}ing {entity}: {result.result}')
    return ('error_unknown', entity)
