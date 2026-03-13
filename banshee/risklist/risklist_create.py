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
import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Optional

from psengine.fusion import FusionMgr
from psengine.risklists import RisklistMgr
from psengine.risklists.models import DefaultRiskList
from rich.progress import Progress, SpinnerColumn, TextColumn


def _collect_csv_rows(
    mgr: RisklistMgr,
    risk_rules: list[str],
    entity_type: str,
    risk_score: Optional[int],
    progress,
    task_id,
) -> list[dict]:
    seen = {}
    for rule in risk_rules:
        progress.update(task_id, description=f'Collecting IOCs for risk rule: {rule}')
        for row in mgr.fetch_risklist(rule, entity_type):
            seen.setdefault(row['Name'], row)
    rows = list(seen.values())
    if risk_score is not None:
        rows = [r for r in rows if int(r['Risk']) >= risk_score]
    rows.sort(key=lambda r: int(r['Risk']), reverse=True)
    return rows


def _collect_entries(
    mgr: RisklistMgr,
    risk_rules: list[str],
    entity_type: str,
    risk_score: Optional[int],
    progress,
    task_id,
) -> list[DefaultRiskList]:
    seen = {}
    for rule in risk_rules:
        progress.update(task_id, description=f'Collecting IOCs for rule: {rule}')
        for entry in mgr.fetch_risklist(rule, entity_type, validate=DefaultRiskList):
            seen.setdefault(entry.ioc, entry)
    entries = list(seen.values())
    if risk_score is not None:
        entries = [e for e in entries if e.risk_score >= risk_score]
    entries.sort(key=lambda e: e.risk_score, reverse=True)
    return entries


def _serialize_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    if rows:
        writer.writerow(rows[0].keys())
    writer.writerows(r.values() for r in rows)
    return buf.getvalue()


def _serialize_entries(entries: list[DefaultRiskList], format_: str) -> str:
    if format_ == 'json':
        return json.dumps([e.json() for e in entries], indent=4)
    return '\n'.join(e.ioc for e in entries)


def _write(
    content: str,
    file_path: Optional[Path],
    fusion: bool,
    fusion_path: Optional[str],
    progress,
    task_id,
) -> None:
    if fusion:
        progress.update(task_id, description=f'Uploading to Fusion: {fusion_path}')
        _upload_to_fusion(content.encode(), fusion_path)
    else:
        progress.update(task_id, description=f'Writing to: {file_path}')
        file_path.write_text(content)
        print(f'Risklist written to: {str(file_path)}')


def _upload_to_fusion(content: bytes, fusion_path: str):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    try:
        FusionMgr().post_file(tmp_path, fusion_path)
    finally:
        tmp_path.unlink(missing_ok=True)
    print(f'Risklist uploaded to Fusion: {fusion_path}')


def create_risklist(
    entity_type: str,
    risk_rules: list[str],
    risk_score: int = None,
    output_path: str = None,
    fusion: bool = False,
    format_: str = 'csv',
):
    file_path = None
    if not fusion:
        ext = 'txt' if format_ == 'edl' else format_
        if output_path:
            file_path = Path(output_path)
            if file_path.is_dir():
                file_path = file_path / f'custom_risklist_{entity_type}.{ext}'
        else:
            file_path = Path.cwd() / f'custom_risklist_{entity_type}.{ext}'

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
        task_id = progress.add_task(description='Fetching risklist entries')

        mgr = RisklistMgr()
        csv.field_size_limit(4 * 131072)  # 512KB

        if format_ == 'csv':
            rows = _collect_csv_rows(mgr, risk_rules, entity_type, risk_score, progress, task_id)
            progress.update(task_id, description=f'Preparing {len(rows):,} entries')
            content = _serialize_csv(rows)
        else:  # JSON / EDL
            entries = _collect_entries(mgr, risk_rules, entity_type, risk_score, progress, task_id)
            progress.update(task_id, description=f'Preparing {len(entries):,} entries')
            content = _serialize_entries(entries, format_)

        _write(content, file_path, fusion, output_path, progress, task_id)
