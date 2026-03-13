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

from enum import Enum
from itertools import chain

MAX_ENRICHMENT_WORKERS = 20


class IOCType(str, Enum):
    """Enum for possible ioc types."""

    ip = 'ip'
    domain = 'domain'
    url = 'url'
    hash = 'hash'
    vulnerability = 'vulnerability'


def cumulative_fields(levels: dict[int, list[str]]) -> dict[int, list[str]]:
    """Given a mapping of level → fields, return cumulative fields per level."""
    result = {}
    for i in sorted(levels):
        combined = chain.from_iterable(levels[j] for j in range(1, i + 1))
        result[i] = sorted(set(combined))
    return result


IP_LEVELS = {
    1: ['entity', 'risk', 'timestamps'],
    2: ['intelCard', 'location'],
    3: ['links', 'analystNotes'],
    4: ['riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
    5: ['dnsPortCert', 'scanner'],
}

DOMAIN_LEVELS = {
    1: ['entity', 'risk', 'timestamps'],
    2: ['intelCard'],
    3: ['links', 'analystNotes'],
    4: ['riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
    5: ['riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
}

HASH_LEVELS = {
    1: ['entity', 'risk', 'timestamps', 'hashAlgorithm'],
    2: ['intelCard', 'fileHashes'],
    3: ['links', 'analystNotes'],
    4: ['riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
    5: ['riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
}

URL_LEVELS = {
    1: ['entity', 'risk', 'timestamps'],
    2: ['intelCard'],
    3: ['links', 'analystNotes'],
    4: ['riskMapping', 'sightings', 'enterpriseLists'],
    5: ['riskMapping', 'sightings', 'enterpriseLists'],
}

VULN_LEVELS = {
    1: ['entity', 'risk', 'timestamps', 'lifecycleStage'],
    2: ['intelCard'],
    3: ['links', 'analystNotes'],
    4: ['cvss', 'cvssv3', 'cvssv4', 'riskMapping', 'sightings', 'threatLists', 'enterpriseLists'],
    5: ['cpe', 'cpe22uri', 'nvdReferences', 'nvdDescription'],
}

IP_FIELDS = cumulative_fields(IP_LEVELS)
DOMAIN_FIELDS = cumulative_fields(DOMAIN_LEVELS)
HASH_FIELDS = cumulative_fields(HASH_LEVELS)
URL_FIELDS = cumulative_fields(URL_LEVELS)
VULN_FIELDS = cumulative_fields(VULN_LEVELS)

ENTITY_FIELD_MAP = {
    'ip': IP_FIELDS,
    'domain': DOMAIN_FIELDS,
    'hash': HASH_FIELDS,
    'url': URL_FIELDS,
    'vulnerability': VULN_FIELDS,
}


def get_entity_field_map_epilog():
    epilog_str = ''
    for entity_type, verbose_map in ENTITY_FIELD_MAP.items():
        epilog_str += f'\n\n{entity_type}:\n\n'
        for verbose, fields in verbose_map.items():
            joined_fields = ', '.join(sorted(fields))
            epilog_str += f'\n\n* {verbose} {joined_fields}\n\n'
        epilog_str += '\n'

    return epilog_str
