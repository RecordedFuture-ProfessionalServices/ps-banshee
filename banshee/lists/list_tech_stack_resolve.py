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

import csv
import sys
from pathlib import Path

from psengine.entity_match import EntityMatchMgr
from psengine.helpers import MultiThreadingHelper
from psengine.rf_client import RFClient
from rich.console import Console
from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn, TextColumn

# from .list_bulk_add import bulk_add_entities

ENTITY_TYPES = ['Product', 'ProductIdentifier']
MAX_WORKERS = 20


def _print_resolution_summary(
    output_file: str, supplied_count: int, found_count: int, not_found_count: int
):
    console = Console()
    output_path = Path(output_file).resolve().as_posix()
    not_found_style = 'green' if not_found_count == 0 else 'red'
    status_text = (
        '[bold green]SUCCESS[/bold green]'
        if not_found_count == 0
        else '[bold yellow]COMPLETED WITH WARNINGS[/bold yellow]'
    )

    console.print('[bold]Tech Stack Resolution Summary[/bold]')
    console.print(f'Status                 {status_text}')
    console.print(f'Output file            {output_path}')
    console.print(f'Technologies supplied  [cyan]{supplied_count}[/cyan]')
    console.print(f'Technologies found     [green]{found_count}[/green]')
    console.print(
        f'Technologies not found [{not_found_style}]{not_found_count}[/{not_found_style}]'
    )


def _load_tech_rows(infile: Path) -> list[str]:
    with infile.open(newline='') as f:
        reader = csv.reader(f)
        return [row[0].strip() for row in reader if row and row[0].strip()]


def _fallback_queries(value: str) -> list[str]:
    queries = [value]
    candidate = value

    while True:
        parts = candidate.split()
        if len(parts) <= 1:
            break

        candidate = ' '.join(parts[:-1])

        if candidate in queries:
            break

        queries.append(candidate)

    return queries


def _find_product_matches(match_mgr: EntityMatchMgr, value: str, limit: int):
    for query in _fallback_queries(value):
        results = match_mgr.match(query, ENTITY_TYPES, limit)
        if not results:
            continue
        if results[0].is_found is False:
            continue
        return query, results

    return value, []


# TODO - we will fail if VULN module is not available. So need to ignore that failure
def _fetch_vulnerability_count(rf_client: RFClient, product_id: str) -> int:
    response = rf_client.request(
        method='get',
        url='https://api.recordedfuture.com/v2/vulnerability/search',
        params={'limit': 1000, 'product': product_id},
    )
    payload = response.json()
    return payload.get('counts', {}).get('total', 0)


def _build_row_with_cve_count(match_data: dict, rf_client: RFClient) -> dict:
    """Build a complete row with CVE count fetched from API.

    Args:
        match_data: dict with 'supplied_input', 'search_term', 'match' keys
        rf_client: RFClient instance for API calls

    Returns:
        Complete row dict with all fields including CVE count
    """
    supplied_input = match_data['supplied_input']
    search_term = match_data['search_term']
    match = match_data['match']
    entity_id = match.content.id_

    return {
        'Supplied Input': supplied_input,
        'Search Term Used': search_term,
        'Resolved Entity': match.entity,
        'Type': match.content.type_,
        'Entity ID': entity_id,
        'Mapped CVEs': _fetch_vulnerability_count(rf_client, entity_id),
    }


# TODO - refactor so the whole process is multi threaded
# TODO - exclude N/A matches if an option --exclude is set?
# TODO - send to watchlist immediatelly ?
def resolve_tech_stack(
    list_id: str,
    infile: str,
    possible_matches: int,
    output_file: str,
    list_overwrite: bool,
):
    output_path = Path(output_file).resolve()
    tech_rows = _load_tech_rows(Path(infile))
    rows = []
    unmatched_rows = []
    matches_to_fetch = []
    supplied_count = 0
    found_count = 0
    not_found_count = 0
    match_mgr = EntityMatchMgr()
    rf_client = RFClient()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        MofNCompleteColumn(),
        transient=True,
        disable=not sys.stdout.isatty(),
    ) as progress:
        task_id = progress.add_task(
            description='Resolving technologies against Recorded Future entities...',
            total=len(tech_rows),
        )

        for tech in tech_rows:
            supplied_count += 1
            progress.update(task_id, description=f"Resolving '{tech}'")
            matched_input, matches = _find_product_matches(match_mgr, tech, possible_matches)

            if not matches:
                not_found_count += 1
                unmatched_rows.append(
                    {
                        'Supplied Input': tech,
                        'Search Term Used': 'N/A',
                        'Resolved Entity': 'N/A',
                        'Type': 'N/A',
                        'Entity ID': 'N/A',
                        'Mapped CVEs': 0,
                    }
                )
                progress.advance(task_id)
                continue

            found_count += 1
            # Collect matches for parallel CVE fetching
            for match in matches:
                matches_to_fetch.append(
                    {
                        'supplied_input': tech,
                        'search_term': matched_input,
                        'match': match,
                    }
                )

            progress.advance(task_id)

    if matches_to_fetch:
        with Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}'),
            MofNCompleteColumn(),
            transient=True,
            disable=not sys.stdout.isatty(),
        ) as progress:
            task_id = progress.add_task(
                description='Fetching CVE counts for matched entities...',
                total=len(matches_to_fetch),
            )

            def fetch_with_progress(match_data: dict) -> dict:
                result = _build_row_with_cve_count(match_data, rf_client)
                progress.advance(task_id)
                return result

            matched_rows = MultiThreadingHelper.multithread_it(
                MAX_WORKERS,
                fetch_with_progress,
                iterator=matches_to_fetch,
            )
            rows.extend(matched_rows)

    rows.extend(unmatched_rows)

    fieldnames = [
        'Supplied Input',
        'Search Term Used',
        'Resolved Entity',
        'Type',
        'Entity ID',
        'Mapped CVEs',
    ]
    with output_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # if matched_ids:
    #     # list_bulk_add deduplicates internally.
    #     bulk_add_entities(list_id=list_id, entities=matched_ids)

    _print_resolution_summary(
        output_file=output_path.as_posix(),
        supplied_count=supplied_count,
        found_count=found_count,
        not_found_count=not_found_count,
    )
