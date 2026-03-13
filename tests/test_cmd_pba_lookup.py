import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_playbook_alerts import app

runner = CliRunner()

COMMAND = 'lookup'


def test_pba_lookup_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


def test_pba_bad_lookup_args():
    result = runner.invoke(app, args=[COMMAND, 'bad_alert_id'])
    assert result.exit_code == 2
    # due to terminal truncation the output is not always printed the same
    # so we need to check it for each word :shrug:
    expected_output_as_list = [
        'Alert',
        'ID',
        'should',
        'be',
        '36',
        'characters',
        'long',
        'or',
        '41',
        'characters',
        'with',
        "'task:'",
        'prefix',
    ]
    assert all(word in result.output for word in expected_output_as_list)


ids_no_task_prefix = [
    '99a83597-3c3f-49c0-af56-c06a636532e8',  # domain abuse
    'db6b2635-28f5-49ec-b717-8372de9a96fd',  # cyber vulnerability
    'bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',  # code repo leakage
    'c89f8024-0462-4a50-88a9-f7e86056d485',  # third party risk
    'f87706b1-cea4-4765-9d50-7647ee9bda9b',  # identity novel exposures
    'a8b126d8-4c00-4716-acaa-43905d5a19f8',  # geopolitics facility
    '3b9e9afb-3e4d-4f98-93fa-031cb3088004',  # malware_report
]


@pytest.mark.vcr
@pytest.mark.parametrize('alert_id', ids_no_task_prefix)
def test_pba_lookup_no_task_prefix(alert_id):
    result = runner.invoke(app, args=[COMMAND, alert_id])
    assert result.exit_code == 0


ids_with_task_prefix = [f'task:{alert_id}' for alert_id in ids_no_task_prefix]


@pytest.mark.vcr
@pytest.mark.parametrize('alert_id', ids_with_task_prefix)
def test_pba_lookup_task_prefix(alert_id):
    result = runner.invoke(app, args=[COMMAND, alert_id])
    assert result.exit_code == 0


ids = [
    (
        '99a83597-3c3f-49c0-af56-c06a636532e8',
        'Domain Abuse',
        [
            'panel_status',
            'panel_action',
            'panel_evidence_summary',
            'panel_evidence_dns',
            'panel_evidence_whois',
            'panel_log_v2',
        ],
    ),
    (
        'db6b2635-28f5-49ec-b717-8372de9a96fd',
        'Cyber Vulnerability',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
    (
        'bd7d0c8c-f7f7-4a21-9560-1d5843e48cdc',
        'Data Leakage on Code Repository',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
    (
        'c89f8024-0462-4a50-88a9-f7e86056d485',
        'Third Party Risk',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
    (
        'f87706b1-cea4-4765-9d50-7647ee9bda9b',
        'Novel Identity Exposure',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
    (
        'a8b126d8-4c00-4716-acaa-43905d5a19f8',
        'Geopolitics Facility',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
    (
        '3b9e9afb-3e4d-4f98-93fa-031cb3088004',
        'Cobalt Strike tags',
        ['panel_status', 'panel_evidence_summary', 'panel_log_v2'],
    ),
]


@pytest.mark.vcr
@pytest.mark.parametrize(('alert_id', 'case_rule_label', 'panels'), ids)
def test_pba_lookup(alert_id, case_rule_label, panels):
    result = runner.invoke(app, args=[COMMAND, alert_id])
    assert result.exit_code == 0

    output = json.loads(result.output)
    assert output['panel_status']['case_rule_label'] == case_rule_label
    assert all(panel in output for panel in panels)
    assert 'playbook_alert_id' in output


@pytest.mark.vcr
@pytest.mark.parametrize(('alert_id'), ids_no_task_prefix)
def test_pba_lookup_args_pretty(alert_id):
    result = runner.invoke(app, args=[COMMAND, alert_id, '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)
