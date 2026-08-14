import json
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_pcap_enrich import app
from banshee.pcap_enrich.pcap_enrich import (
    _extract_entities_from_capture,
)

runner = CliRunner()

TEST_FILES = Path(__file__).parent.parent / 'test_files'
# Fixtures are trimmed to the first 200 packets — enough to cover IPv4, IPv6, and
# DNS-with-A-records paths. Regenerate: `editcap -r <src>.pcap <dst>.pcap 1-200`.
CAPTURES = [
    (
        TEST_FILES / 'small.pcap',
        (
            ['168.143.243.230', '188.225.38.247', '193.124.93.220'],
            ['api.bing.com', 'fpdownload2.macromedia.com', 'www.bing.com'],
            {
                'api.bing.com': {'13.107.13.80'},
                'fpdownload2.macromedia.com': {'168.143.243.230'},
                'www.bing.com': {'131.253.33.200'},
            },
        ),
    ),
    (
        TEST_FILES / 'demo.pcapng',
        (
            [
                '142.250.129.94',
                '142.250.151.113',
                '142.251.30.103',
                '142.251.30.104',
                '142.251.30.106',
                '172.217.16.234',
                '2.22.98.7',
                '34.107.221.82',
                '34.41.139.193',
                'ff02::2',
            ],
            ['safebrowsing.googleapis.com', 'siekis.com', 'www.google.com'],
            {
                'safebrowsing.googleapis.com': {'172.217.16.234'},
                'siekis.com': {'34.41.139.193'},
                'www.google.com': {'142.251.30.106'},
            },
        ),
    ),
]


def _make_soar_result():
    result = MagicMock()
    result.entity = '172.217.0.238'
    result.content.entity.type_ = 'IpAddress'
    result.content.risk.score = 75
    result.content.risk.rule.most_critical = 'recentAnalystNote'
    evidence = MagicMock()
    evidence.level = 3
    evidence.json.return_value = {
        'count': 1,
        'timestamp': '2024-01-01T00:00:00.000Z',
        'description': 'Test evidence',
        'rule': 'recentAnalystNote',
        'sightings': 1,
        'mitigation': 'Block',
        'level': 3,
        'type': 'Risk',
    }
    result.content.risk.rule.evidence = [evidence]
    return result


def _make_ta_item():
    item = MagicMock()
    item.json.return_value = {'ioc': '172.217.0.238', 'ta_names': []}
    return item


@pytest.mark.parametrize(('capture', 'expected'), CAPTURES)
def test_extract_entities_pcap(capture, expected):
    entities = _extract_entities_from_capture(capture)
    for elem, expected_elem in zip(entities, expected):
        assert sorted(elem) == sorted(expected_elem)


@patch('banshee.pcap_enrich.pcap_enrich._extract_entities_from_capture')
@patch('banshee.pcap_enrich.pcap_enrich.LookupMgr')
@patch('banshee.pcap_enrich.pcap_enrich.RisklistMgr')
@patch('banshee.pcap_enrich.pcap_enrich.SoarMgr')
def test_pcap_json_out(mock_soar_cls, mock_risklist_cls, mock_lookup_cls, mock_extract):
    mock_extract.return_value = (['172.217.0.238'], [], {})
    mock_soar_cls.return_value.soar.return_value = [_make_soar_result()]
    mock_risklist_cls.return_value.fetch_risklist.side_effect = lambda *_a, **_kw: iter(
        [_make_ta_item()]
    )
    mock_lookup_cls.return_value.lookup_bulk.return_value = [
        MagicMock(links=MagicMock(return_value=[]))
    ]
    result = runner.invoke(app, args=['enrich', CAPTURES[0][0].as_posix(), '-r', '40'])
    assert result.exit_code == 0
    data = json.loads(result.output)

    assert len(data) >= 1
    enriched = data[0]

    expected_number_of_fields = 7
    assert len(enriched) == expected_number_of_fields

    assert re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', enriched['ioc'])
    assert isinstance(enriched['risk_score'], int)
    assert isinstance(enriched['most_malicious_rule'], str)
    assert isinstance(enriched['rule_evidence'], list)
    expected_evidence_fields = {
        'count',
        'timestamp',
        'description',
        'rule',
        'sightings',
        'mitigation',
        'level',
        'type',
    }
    for evidence_item in enriched['rule_evidence']:
        assert set(evidence_item.keys()) == expected_evidence_fields
    assert [e['level'] for e in enriched['rule_evidence']] == sorted(
        [e['level'] for e in enriched['rule_evidence']], reverse=True
    )
    assert isinstance(enriched['ta_names'], list)
    assert isinstance(enriched['malwares'], list)
    assert re.match(
        r'^ip\.src == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} or ip\.dst == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        enriched['wireshark_query'],
    )


@patch('banshee.pcap_enrich.pcap_enrich._extract_entities_from_capture')
@patch('banshee.pcap_enrich.pcap_enrich.LookupMgr')
@patch('banshee.pcap_enrich.pcap_enrich.RisklistMgr')
@patch('banshee.pcap_enrich.pcap_enrich.SoarMgr')
def test_pcap_pretty_out(mock_soar_cls, mock_risklist_cls, mock_lookup_cls, mock_extract):
    mock_extract.return_value = (['172.217.0.238'], [], {})
    mock_soar_cls.return_value.soar.return_value = [_make_soar_result()]
    mock_risklist_cls.return_value.fetch_risklist.side_effect = lambda *_a, **_kw: iter(
        [_make_ta_item()]
    )
    mock_lookup_cls.return_value.lookup_bulk.return_value = [
        MagicMock(links=MagicMock(return_value=[]))
    ]
    result = runner.invoke(app, args=['enrich', CAPTURES[1][0].as_posix(), '-p', '-r', '40'])
    assert result.exit_code == 0

    assert re.search(r'IOC:\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result.output)
    assert re.search(r'Risk Score:\s+\d+', result.output)
    assert re.search(r'Most Malicious Risk Rule:\s+.+', result.output)
    assert re.search(
        r'Wireshark Query:\s+ip\.src == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} or ip\.dst == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        result.output,
    )
