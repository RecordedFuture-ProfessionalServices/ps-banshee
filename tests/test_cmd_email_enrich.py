import json
import re
from pathlib import Path

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_email import app
from banshee.email.email_enrich import _extract_entities
from banshee.email.helpers import parse_eml

runner = CliRunner()

TEST_FILES = Path(__file__).parent.parent / 'test_files'
EML_FILES = [
    (
        TEST_FILES / 'simple.eml',
        (
            [
                {'entity': 'email_domain.com', 'type': 'domain', 'location': 'header'},
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
                {'entity': '192.168.0.24', 'type': 'ip', 'location': 'header'},
                {'entity': '39.62.178.92', 'type': 'ip', 'location': 'header'},
                {'entity': 'email_domain.com', 'type': 'domain', 'location': 'header'},
                {'entity': 'email_domain.com', 'type': 'domain', 'location': 'header'},
                {
                    'entity': 'https://netfimarketing.com/xad64735f0526b49a3u892a3ff0q4884737e.html',
                    'location': 'body',
                    'type': 'url',
                },
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
    headers, body, attachments = parse_eml(eml_path)
    entities = _extract_entities(headers, body, attachments)
    assert entities == expected


@pytest.mark.parametrize(
    ('url', 'expected'),
    [
        ("Hello, this is the link https://example.com/path'", ["https://example.com/path'"]),
        (
            'Hello, this is the link https://example.com/path#section!',
            ['https://example.com/path#section!'],
        ),
        (
            'Hello, this is the link https://example.com/path?q=test&',
            ['https://example.com/path?q=test&'],
        ),
        (
            'Hello, this is the link https://example.com/path?q=test=',
            ['https://example.com/path?q=test='],
        ),
        (
            'Hello, this is the link https://example.com/path?q=test+',
            ['https://example.com/path?q=test+'],
        ),
        (
            'Hello, this is the link https://example.com/path?redirect=https://bank.example/login',
            ['https://example.com/path?redirect=https://bank.example/login'],
        ),
        (
            'Hello, this is the link https://example.com/path?x=1;',
            ['https://example.com/path?x=1;'],
        ),
        (
            'Hello, this is the link https://example.com/path?x=1,',
            ['https://example.com/path?x=1,'],
        ),
        (
            'Hello, this is the link https://example.com/path?x=1.',
            ['https://example.com/path?x=1.'],
        ),
        (
            'Hello, this is the link https://example.com/path#frag.',
            ['https://example.com/path#frag.'],
        ),
        (
            'Hello, this is the link https://example.com/path#frag,',
            ['https://example.com/path#frag,'],
        ),
        (
            'Hello, this is the link https://example.com/path#frag;',
            ['https://example.com/path#frag;'],
        ),
        (
            'Hello, this is the link https://example.com/path(foo)',
            ['https://example.com/path(foo)'],
        ),
        (
            'Hello, this is the link https://example.com/path[abc]',
            ['https://example.com/path[abc]'],
        ),
        ('Hello, this is the link https://example.com/a(b)c', ['https://example.com/a(b)c']),
        ('Hello, this is the link https://example.com/a,b', ['https://example.com/a,b']),
        ('Hello, this is the link https://example.com/a;b', ['https://example.com/a;b']),
        ('Hello, this is the link https://example.com/a=1', ['https://example.com/a=1']),
        ('Hello, this is the link https://example.com/a+b', ['https://example.com/a+b']),
        ('Hello, this is the link https://example.com/a&b', ['https://example.com/a&b']),
        ("Hello, this is the link https://example.com/a'b", ["https://example.com/a'b"]),
        ('Hello, this is the link https://example.com/a!b', ['https://example.com/a!b']),
        ('Hello, this is the link https://example.com/a*b', ['https://example.com/a*b']),
        ('Hello, this is the link https://example.com/a%20', ['https://example.com/a%20']),
        ('Hello, this is the link https://example.com/%7Euser', ['https://example.com/%7Euser']),
        (
            'Hello, this is the link https://example.com/%7Euser for review',
            ['https://example.com/%7Euser'],
        ),
        (
            'Hello, this is the link https://example.com/path?email=user%40example.com',
            ['https://example.com/path?email=user%40example.com'],
        ),
        (
            'Hello, this is the link https://example.com/path?next=%2Flogin%3Ftoken%3Dabc',
            ['https://example.com/path?next=%2Flogin%3Ftoken%3Dabc'],
        ),
        ('Hello, this is the link https://example.com/path#', ['https://example.com/path#']),
    ],
)
def test_extract_entities_plain(url, expected):
    entities = _extract_entities({}, {'text/plain': url}, {})
    urls = [e['entity'] for e in entities]
    assert urls == expected


@pytest.mark.parametrize(
    ('url', 'expected'),
    [
        ('<a href=https://example.com/path>Click</a>', ['https://example.com/path']),
        (
            '<a href="https://example.com/login?token=abc&next=/dashboard">Click here</a>',
            ['https://example.com/login?token=abc&next=/dashboard'],
        ),
        (
            '<a href="https://evil.example/login">https://bank.example/login</a>',
            ['https://evil.example/login', 'https://bank.example/login'],
        ),
        (
            "<a href='https://example.com/reset?token=abc&next=/login'>Reset password</a>",
            ['https://example.com/reset?token=abc&next=/login'],
        ),
    ],
)
def test_extract_entities_html(url, expected):
    entities = _extract_entities({}, {'text/html': url}, {})
    urls = [e['entity'] for e in entities]
    assert urls == expected


def test_email_json_out():
    result = runner.invoke(app, args=[EML_FILES[0][0].as_posix(), '-r', '50'])
    assert result.exit_code == 0
    data = json.loads(result.output)

    assert len(data) >= 1
    enriched = data[0]

    expected_number_of_fields = 11
    assert len(enriched) == expected_number_of_fields

    assert re.match(r'^https:\/\/.+?\/.+$', enriched['ioc'])
    assert isinstance(enriched['risk_score'], int)
    assert isinstance(enriched['rule_evidence'], list)

    expected_evidence_fields = {'rule', 'level', 'timestamp', 'evidence_string'}
    for evidence_item in enriched['rule_evidence']:
        assert set(evidence_item.keys()) == expected_evidence_fields
    assert [e['level'] for e in enriched['rule_evidence']] == sorted(
        [e['level'] for e in enriched['rule_evidence']], reverse=True
    )

    assert isinstance(enriched['type'], str)
    assert re.match(r'^body$', enriched['location'])
    assert isinstance(enriched['ta_names'], list)
    assert isinstance(enriched['malwares'], list)
