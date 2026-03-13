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

from psengine.detection import DetectionMgr, DetectionRule, save_rule
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..threat import ThreatActorCategories, fetch_threat_actor_map, fetch_threat_malware_map


def search_detection_rules(
    types: list[str] = None,
    threat_actor_map: bool = False,
    threat_malware_map: bool = False,
    threat_actor_categories: list[ThreatActorCategories] = None,
    org_id: str = None,
    entities: list[str] = None,
    created_after: str = None,
    created_before: str = None,
    updated_after: str = None,
    updated_before: str = None,
    rule_id: str = None,
    title: str = None,
    limit: int = 10,
    output_path: str = None,
    pretty: bool = False,
):
    """Search detection rules."""
    console = Console()
    rules = []
    if entities is None:
        entities = []

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description='Processing parameters')

        if threat_actor_map:
            progress.update(task_id, description='Fetching threat actor map')
            ta_entities = _fetch_threat_actor_map(threat_actor_categories, org_id)
            entities.extend(ta_entities)

        if threat_malware_map:
            progress.update(task_id, description='Fetching threat malware map')
            malware_entities = _fetch_threat_malware_map(org_id)
            entities.extend(malware_entities)

        progress.update(task_id, description='Searching for detection rules')
        rules = _search_detection_rules(
            types,
            entities,
            created_after,
            created_before,
            updated_after,
            updated_before,
            rule_id,
            title,
            limit,
        )

        progress.update(task_id, description='Preparing results')
        rules.sort(reverse=True)

    # Save rules to files if output_path is specified and exit
    if output_path:
        _save_rules(output_path, rules)
        return

    if pretty:
        _pretty_print(console, rules)
    else:
        rule_json = [rule.json() for rule in rules]
        print_json(json.dumps(rule_json), indent=2)


def _search_detection_rules(
    types,
    entities,
    created_after,
    created_before,
    updated_after,
    updated_before,
    rule_id,
    title,
    limit,
):
    dt_mgr = DetectionMgr()
    results = []
    if rule_id and not rule_id.startswith('doc:'):
        rule_id = f'doc:{rule_id}'

    if not entities:
        results = dt_mgr.search(
            detection_rule=types,
            created_after=created_after,
            created_before=created_before,
            updated_after=updated_after,
            updated_before=updated_before,
            doc_id=rule_id,
            title=title,
            max_results=limit,
        )
    else:
        for entity in entities:
            if len(results) >= limit:
                results = results[:limit]
                break

            remaining = limit - len(results)
            search_results = dt_mgr.search(
                detection_rule=types,
                entities=[entity],
                created_after=created_after,
                created_before=created_before,
                updated_after=updated_after,
                updated_before=updated_before,
                doc_id=rule_id,
                title=title,
                max_results=remaining,
            )
            results.extend(search_results)

        results = list(set(results))

    return results


def _fetch_threat_actor_map(threat_actor_categories, org_id):
    threat_map = fetch_threat_actor_map(
        threat_actor_categories=threat_actor_categories, org_id=org_id
    )
    threat_actors_ids = [ta['id'] for ta in threat_map]
    if threat_actors_ids:
        return threat_actors_ids
    print('No threat actors found in the threat map.', file=sys.stderr)
    sys.exit(1)


def _fetch_threat_malware_map(org_id):
    threat_map = fetch_threat_malware_map(org_id=org_id)
    malware_ids = [malware['id'] for malware in threat_map]
    if malware_ids:
        return malware_ids
    print('No malware found in the threat map.', file=sys.stderr)
    sys.exit(1)


def _pretty_print(console, results: list[DetectionRule]):
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('ID', style='cyan bold', no_wrap=True)
    table.add_column('Type', style='yellow', no_wrap=True)
    table.add_column('Title', style='bold')
    table.add_column('Created', style='blue', no_wrap=True)
    table.add_column('Updated', style='green bold', no_wrap=True)
    table.add_column('Files', style='white dim')

    for rule in results:
        file_names = ', '.join(r.file_name for r in rule.rules if r.file_name)

        if len(file_names) > 50:
            file_names = file_names[:50] + '...'

        table.add_row(
            rule.id_,
            rule.type_.value,
            rule.title,
            str(rule.created)[:10],
            str(rule.updated)[:10],
            file_names or '-',
        )

    console.print(table)
    console.print(f'\n[bold]Total results:[/bold] {len(results)}')


def _save_rules(output_path, results: list[DetectionRule]):
    saved_count = 0
    for rule in results:
        try:
            save_rule(rule, output_path)
            saved_count += 1
        except Exception as e:  # noqa: PERF203, BLE001
            print(f'Error saving rule {rule.id_}: {e}', file=sys.stderr)

    if saved_count < len(results):
        print(
            f'Warning: {saved_count} out of {len(results)} rules were saved successfully.',
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        print(f'Saved {saved_count} rule files to disk')
