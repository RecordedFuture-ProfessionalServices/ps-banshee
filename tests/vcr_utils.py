import json
import random
import re
import string

from mimesis import Algorithm, Cryptographic, Food, Internet, Text

ISO_8601_REGEX = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})'
    r'T(\d{2}):(\d{2}):(\d{2})'
    r'(?:\.(\d+))?'
    r'(Z|[+-]\d{2}:\d{2})?$'
)

DATE_REGEX = re.compile(r'^(\d{4})-(\d{2})-(\d{2})')
URL_REGEX = re.compile(r'^http[s]://')
RFID = re.compile(r'^[\w_-]{4,6}$')
IP_REGEX = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
DOMAIN_REGEX = re.compile(
    r'^(?:[a-zA-Z0-9]' r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+' r'[a-zA-Z]{2,}$'
)
MD5_REGEX = re.compile(r'^[a-fA-F0-9]{32}$')
SHA1_REGEX = re.compile(r'^[a-fA-F0-9]{40}$')
SHA256_REGEX = re.compile(r'^[a-fA-F0-9]{64}$')

DO_NOT_CHANGE = (
    'type',
    'status',
    'algorithm',
    'category',
    'playbook_alert_id',
    'next_offset',
    'offset',
    'created',
    'updated',
    'triggered',
    'status_in_portal',
    'id',
    'case_rule_label',
    'image_id',
    'trace_id',
    'report_id',
    'added',
    'removed',
    'timestamp',
    'published',
    'lastSeen',
    'firstSeen',
    'hashAlgorithm',
    'validated_on',
    'Timestamp',
    'start_date',
    'stop_date',
    'lastModified',
    'time',
    'analyzed',
    'exfiltration_date',
    'event_time',
    'note_date',
    'status_date'
)


def _obfuscate_by_pattern(value):
    food = Food()
    match value:
        case v if re.match(URL_REGEX, v):
            return Internet().url()
        case v if re.match(IP_REGEX, v):
            return Internet().ip_v4()
        case v if re.match(DOMAIN_REGEX, v):
            return Internet().hostname()
        case v if re.match(MD5_REGEX, v) or re.match(SHA1_REGEX, v) or re.match(SHA256_REGEX, v):
            return Cryptographic().hash(algorithm=Algorithm.SHA256)
        case _:
            return food.dish()[: len(value)]


def _make_obfuscation(value, key):  # noqa: C901
    text = Text()
    if isinstance(value, str):
        match key:
            case 'id':
                if value.startswith('ip:'):
                    return f'ip:{Internet().ip_v4()}'
                if value.startswith('idn:'):
                    return f'idn:{Internet().hostname()}'
                if value.startswith('url:'):
                    return f'url:{Internet().url()}'
                if value.startswith('hash:'):
                    return f'hash:{Cryptographic().hash(algorithm=Algorithm.SHA256)}'
                if value.startswith(('report:', 'doc:')):
                    return value
                if len(value) == 6:  # do not scrub alert IDs, rule IDs
                    return value
                return ''.join(random.choices(string.ascii_letters + string.digits, k=len(value)))  # noqa: S311
            case 'title':
                return text.title()[: len(value)]
            case 'name':
                return _obfuscate_by_pattern(value)
            case 'text':
                return text.text()[: len(value)]

            # dont change them
            case _ if key in DO_NOT_CHANGE:
                return value

        if value:
            return _obfuscate_by_pattern(value)

    return value


def _scrub_json_values(data, key=None):
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k] = _scrub_json_values(v, key=k)
        return new_data
    if isinstance(data, list):
        return [_scrub_json_values(v, key=key) for v in data]

    if isinstance(data, str):
        return _make_obfuscation(data, key=key)

    return data


def scrub_response(response):
    if 'body' not in response:
        return response

    if 'scrubbed' in response['headers']:
        return response

    if response['body']['string']:
        try:
            body_str = response['body']['string']
            if isinstance(body_str, bytes):
                body_str = body_str.decode('utf-8')
            body = json.loads(body_str)
            scrubbed = _scrub_json_values(body)
            response['body']['string'] = json.dumps(scrubbed).encode()
            response['headers']['scrubbed'] = '1'
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
            pass

    return response
