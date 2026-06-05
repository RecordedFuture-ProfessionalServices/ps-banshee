import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_playbook_alerts import app

runner = CliRunner()

COMMAND = 'export'

ALERTS = json.dumps(
    {
        'data': [
            {
                'playbook_alert_id': 'task:99a83597-3c3f-49c0-af56-c06a636532e8',
                'category': 'domain_abuse',
            },
            {
                'playbook_alert_id': 'task:db6b2635-28f5-49ec-b717-8372de9a96fd',
                'category': 'cyber_vulnerability',
            },
            {
                'playbook_alert_id': 'task:bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',
                'category': 'code_repo_leakage',
            },
            {
                'playbook_alert_id': 'task:c89f8024-0462-4a50-88a9-f7e86056d485',
                'category': 'third_party_risk',
            },
            {
                'playbook_alert_id': 'task:f87706b1-cea4-4765-9d50-7647ee9bda9b',
                'category': 'identity_novel_exposures',
            },
            {
                'playbook_alert_id': 'task:a8b126d8-4c00-4716-acaa-43905d5a19f8',
                'category': 'geopolitics_facility',
            },
            {
                'playbook_alert_id': 'task:3b9e9afb-3e4d-4f98-93fa-031cb3088004',
                'category': 'malware_report',
            },
        ]
    }
)
EMPTY_JSON = json.dumps([])
INVALID_JSON_CA_ALERT = json.dumps([{'name': 'kevin'}])
INVALID_JSON = json.dumps({'data': [{'name': 'steven'}]})
INVALID_ALERT_ID = json.dumps({'data': [{'playbook_alert_id': 'bad-alert-id'}]})


def test_pba_export_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_pba_export_id_non_piped():
    result = runner.invoke(app, args=[COMMAND, '99a83597-3c3f-49c0-af56-c06a636532e8'])
    assert result.exit_code == 2


def test_pba_export_blank_pipe():
    result = runner.invoke(app, args=[COMMAND], input='')
    assert result.exit_code == 2


def test_pba_export_invalid_json():
    result = runner.invoke(app, args=[COMMAND], input=INVALID_JSON)
    assert result.exit_code == 2


def test_pba_export_invalid_id():
    result = runner.invoke(app, args=[COMMAND], input=INVALID_ALERT_ID)
    assert result.exit_code == 2


def test_pba_export_empty_json():
    result = runner.invoke(app, args=[COMMAND], input=EMPTY_JSON)
    assert result.exit_code == 2


@pytest.mark.vcr
def test_pba_export_json():
    result = runner.invoke(app, args=[COMMAND], input=ALERTS)
    assert result.exit_code == 0

    alerts = json.loads(result.output.strip('\n'))
    assert len(alerts) == 7
    for alert in alerts:
        assert alert['playbook_alert_id'] in [
            'task:99a83597-3c3f-49c0-af56-c06a636532e8',
            'task:db6b2635-28f5-49ec-b717-8372de9a96fd',
            'task:bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',
            'task:c89f8024-0462-4a50-88a9-f7e86056d485',
            'task:f87706b1-cea4-4765-9d50-7647ee9bda9b',
            'task:a8b126d8-4c00-4716-acaa-43905d5a19f8',
            'task:3b9e9afb-3e4d-4f98-93fa-031cb3088004',
        ]


@pytest.mark.vcr
def test_pba_export_csv():
    result = runner.invoke(app, args=[COMMAND, '--csv'], input=ALERTS)
    assert result.exit_code == 0

    result_csv = result.output.strip().split('\n')
    assert len(result_csv) == 8
    assert (
        result_csv[0]
        == 'ID,Priority,Alert Rule,Status,Created,Updated,Subject,Assignee,Assessments,Entities,Reopen Strategy,Onwards Actions'
    )
    assert len(result_csv[1].split(',')) == 12
