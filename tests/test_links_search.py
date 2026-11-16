#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly "as-is" and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from unittest.mock import MagicMock, patch

import pytest
from psengine.enrich import EnrichmentSoarError

from banshee.links.constants import MAX_ENRICHMENT_WORKERS, LinkSource
from banshee.links.links_search import _enrich_linked_iocs, _sort_links_iocs, search_links

_PATCH_LINK_MGR = patch('banshee.links.links_search.LinksMgr')
_PATCH_LINK_SORT = patch('banshee.links.links_search._sort_links_iocs')
_PATCH_SOAR_MGR = patch('banshee.links.links_search.SoarMgr')
_PATCH_PRINT_SEARCH = patch('banshee.links.links_search._print_search')
_PATCH_PRINT_JSON = patch('banshee.links.links_search.print_json')
_PATCH_ENRICH = patch('banshee.links.links_search._enrich_linked_iocs')

_ARGS = {
    'entities': ['I60vfZ'],
    'entity_types': ['type:Malware'],
    'sources': LinkSource.INSIKT,
    'sections': ['Indicators and Detection Rules'],
    'timeframe': '-1d',
    'events': ['type:MalwareAnalysis'],
    'connected_entities': ['T1005'],
    'per_entity_type': 1,
    'search_scope': 'Medium',
    'skip_enrichment': False,
    'pretty': False,
}

_ARGS_NO_FILTER = {
    'entities': ['I60vfZ'],
    'entity_types': None,
    'sources': None,
    'sections': None,
    'timeframe': None,
    'events': None,
    'connected_entities': None,
    'per_entity_type': None,
    'search_scope': 'Medium',
    'skip_enrichment': False,
    'pretty': False,
}


# ----- Test helpers -----
def _mock_ioc(value):
    mocked = MagicMock()
    mocked.name = value
    return mocked


def _mock_result_with_iocs(ioc_by_type):
    results = MagicMock()
    results.iocs.return_value = {
        t: [_mock_ioc(n) for n in names] for t, names in ioc_by_type.items()
    }
    return results


def _mock_link_result(links=()):
    r = MagicMock()
    r.links = []
    for name in links:
        link = MagicMock()
        link.name = name
        r.links.append(link)
    r.model_dump.return_value = {'links': [{'name': n} for n in links]}
    r.entity.name = 'Entity'
    r.entity.id_ = '123'
    return r


def _mock_enriched(is_enriched=True, has_content=True):
    enriched = MagicMock()
    enriched.is_enriched = is_enriched
    if has_content:
        enriched.content.model_dump.return_value = {'risk': 99}
    else:
        enriched.content = None
    return enriched


# ----- _sort_links_ioc -----
def test_sort_map_no_limit():
    result = [
        _mock_result_with_iocs(
            {
                'type:IpAddress': ['1.1.1.1'],
                'type:InternetDomainName': ['example.com'],
                'type:Hash': ['a82639b6f8c3a6e536d8cc562c3b86ff4b012c84ab230c1e5be649aa9ad26d21'],
                'type:Url': ['https://example.com'],
                'type:CyberVulnerability': ['CVE-2022-47966'],
                'type:Other': ['x'],
            }
        )
    ]
    assert dict(_sort_links_iocs(result)) == {
        'ip': {'1.1.1.1'},
        'domain': {'example.com'},
        'hash_': {'a82639b6f8c3a6e536d8cc562c3b86ff4b012c84ab230c1e5be649aa9ad26d21'},
        'url': {'https://example.com'},
        'vulnerability': {'CVE-2022-47966'},
    }


def test_sort_map_with_limit():
    results = [_mock_result_with_iocs({'type:IpAddress': [f'10.10.10.{i}' for i in range(50)]})]
    assert len(_sort_links_iocs(results, 25)['ip']) == 25


# ----- _enrich_linked_iocs -----
@_PATCH_SOAR_MGR
def test_enrich_keys_by_entity(mock_soar):
    ip = MagicMock(entity='1.1.1.1')
    domain = MagicMock(entity='example.com')
    mock_soar.return_value.soar.return_value = [
        ip,
        domain,
    ]
    assert _enrich_linked_iocs({'ip': ['1.1.1.1'], 'domain': ['example.com']}) == {
        '1.1.1.1': ip,
        'example.com': domain,
    }


@_PATCH_SOAR_MGR
def test_enrich_passes_max_workers(mock_soar):
    mock_soar.return_value.soar.return_value = []
    _enrich_linked_iocs({'ip': ['1.1.1.1']})
    mock_soar.return_value.soar.assert_called_once_with(
        ip=['1.1.1.1'], max_workers=MAX_ENRICHMENT_WORKERS
    )


# -----search_links -----
@_PATCH_LINK_MGR
def test_search_forwards_all_args(mock_mgr):
    mock_mgr.return_value.search.return_value = []
    search_links(**_ARGS)
    mock_mgr.return_value.search.assert_called_once_with(
        entities=_ARGS['entities'],
        sections=_ARGS['sections'],
        entity_types=_ARGS['entity_types'],
        sources=_ARGS['sources'],
        timeframe=_ARGS['timeframe'],
        events=_ARGS['events'],
        connected_entities=_ARGS['connected_entities'],
        search_scope=_ARGS['search_scope'],
        per_entity_type=_ARGS['per_entity_type'],
    )


@_PATCH_LINK_MGR
def test_search_forwards_no_filters(mock_mgr):
    mock_mgr.return_value.search.return_value = []
    search_links(**_ARGS_NO_FILTER)
    mock_mgr.return_value.search.assert_called_once_with(
        entities=_ARGS_NO_FILTER['entities'],
        sections=_ARGS_NO_FILTER['sections'],
        entity_types=_ARGS_NO_FILTER['entity_types'],
        sources=_ARGS_NO_FILTER['sources'],
        timeframe=_ARGS_NO_FILTER['timeframe'],
        events=_ARGS_NO_FILTER['events'],
        connected_entities=_ARGS_NO_FILTER['connected_entities'],
        search_scope=_ARGS_NO_FILTER['search_scope'],
        per_entity_type=_ARGS_NO_FILTER['per_entity_type'],
    )


# ----- search_links: enrichment -----
@_PATCH_SOAR_MGR
def test_enrichment_failed(mock_soar, capsys):
    mock_soar.return_value.soar.side_effect = EnrichmentSoarError('Test')

    assert _enrich_linked_iocs({'ip': ['1.1.1.1']}) == {}
    captured = capsys.readouterr()
    assert 'SOAR Enrichment failed' in captured.err
    assert captured.out == ''


@_PATCH_LINK_MGR
@_PATCH_LINK_SORT
@_PATCH_SOAR_MGR
def test_skip_enrichment(mock_soar, mock_sort, mock_links):
    mock_links.return_value.search.return_value = [_mock_link_result([])]
    search_links(**{**_ARGS, 'skip_enrichment': True})
    mock_sort.assert_not_called()
    mock_soar.assert_not_called()


@_PATCH_LINK_MGR
@_PATCH_LINK_SORT
@_PATCH_SOAR_MGR
def test_no_iocs_no_enrichment(mock_soar, mock_sort, mock_links):
    mock_links.return_value.search.return_value = [_mock_link_result([])]
    mock_sort.return_value = {}
    search_links(**_ARGS)
    mock_sort.assert_called_once()
    mock_soar.assert_not_called()


# ----- search_links: output -----
@_PATCH_PRINT_SEARCH
@_PATCH_LINK_MGR
def test_pretty_prints_each_result(mock_links, mock_print_search):
    mock_links.return_value.search.return_value = [_mock_link_result(), _mock_link_result()]
    search_links(**{**_ARGS, 'pretty': True, 'skip_enrichment': True})
    assert mock_print_search.call_count == 2


@_PATCH_PRINT_JSON
@_PATCH_LINK_MGR
def test_json_empty_result_prints_empty_list(mock_links, mock_print_json):
    mock_links.return_value.search.return_value = []
    search_links(**{**_ARGS, 'skip_enrichment': True})
    mock_print_json.assert_called_once_with(data=[])


@pytest.mark.parametrize(
    ('enriched', 'expected'),
    [
        ({'1.1.1.1': _mock_enriched()}, {'risk': 99}),
        ({'1.1.1.1': _mock_enriched(is_enriched=False)}, None),
        ({'1.1.1.1': _mock_enriched(has_content=False)}, None),
        ({}, None),
    ],
    ids=['enriched', 'not_enriched', 'no_content', 'missing'],
)
@_PATCH_PRINT_JSON
@_PATCH_ENRICH
@_PATCH_LINK_SORT
@_PATCH_LINK_MGR
def test_json_enrichment_field(
    mock_links, mock_sort, mock_enrich, mock_print_json, enriched, expected
):
    mock_links.return_value.search.return_value = [_mock_link_result(['1.1.1.1'])]
    mock_sort.return_value = {'ip': ['1.1.1.1']}
    mock_enrich.return_value = enriched
    search_links(**_ARGS)
    assert mock_print_json.call_args.kwargs['data'][0]['links'][0]['enrichment'] == expected


@_PATCH_PRINT_JSON
@_PATCH_ENRICH
@_PATCH_LINK_SORT
@_PATCH_LINK_MGR
def test_json_enrichment_matches_by_link_name(mock_links, mock_sort, mock_enrich, mock_print_json):
    mock_links.return_value.search.return_value = [_mock_link_result(['1.1.1.1', '2.2.2.2'])]
    mock_sort.return_value = {'ip': {'1.1.1.1', '2.2.2.2'}}
    mock_enrich.return_value = {'2.2.2.2': _mock_enriched()}
    search_links(**_ARGS)
    links = mock_print_json.call_args.kwargs['data'][0]['links']
    assert [link['enrichment'] for link in links] == [None, {'risk': 99}]
