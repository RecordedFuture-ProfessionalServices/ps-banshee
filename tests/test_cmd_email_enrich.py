import json
import re
from pathlib import Path

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_email import app
from banshee.email.email_enrich import _extract_entities, _parse_eml

runner = CliRunner()

TEST_FILES = Path(__file__).parent.parent / 'test_files'
EML_FILES = [
    (
        TEST_FILES / 'simple.eml',
        (
            [
                {'entity': 'email_domain.com', 'type': 'domain', 'location': 'header'},
                {
                    'entity': 'https://lunar-ossified-mosquito.glitch.me/xavi.html',
                    'type': 'url',
                    'location': 'body',
                },
            ]
        ),
    ),
    (
        TEST_FILES / 'demo.eml',
        (
            [
                {'entity': 'email_domain.com', 'type': 'domain', 'location': 'header'},
                {'entity': '192.168.0.24', 'type': 'ip', 'location': 'header'},
                {'entity': '39.62.178.92', 'type': 'ip', 'location': 'header'},
                {
                    'entity': 'e13c4a2f06ef91f9eaed524a30ab2e2ce1ec8b7d88828c4ebecf43ca3aa265b6',
                    'type': 'hash',
                    'location': 'attachments/image.png',
                },
            ]
        ),
    ),
]


@pytest.mark.parametrize(('eml_path', 'expected'), EML_FILES)
def test_parse_eml(eml_path, expected):
    headers, body, attachments = _parse_eml(eml_path)
    entities = _extract_entities(headers, body, attachments)
    for elem, expected_elem in zip(entities, expected):
        assert sorted(elem) == sorted(expected_elem)


def test_email_json_out():
    result = runner.invoke(app, args=[EML_FILES[0][0].as_posix(), '-r', '50'])
    assert result.exit_code == 0
    data = json.loads(result.output)

    assert len(data) >= 1
    enriched = data[0]

    expected_number_of_fields = 8
    assert len(enriched) == expected_number_of_fields

    assert re.match(r'^https:\/\/.+?\/.+$', enriched['ioc'])
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

    assert isinstance(enriched['type'], str)
    assert re.match(r'^body$', enriched['location'])
    assert isinstance(enriched['ta_names'], list)
    assert isinstance(enriched['malwares'], list)
