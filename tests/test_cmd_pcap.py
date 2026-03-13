import json
import re
from pathlib import Path

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_pcap_enrich import app
from banshee.pcap_enrich.pcap_enrich import (
    _extract_entities_from_capture,
)

runner = CliRunner()

TEST_FILES = Path(__file__).parent.parent / 'test_files'
CAPTURES = [
    (
        TEST_FILES / 'small.pcap',
        (
            [
                '172.217.0.238',
                '193.124.93.220',
                '168.143.243.230',
                '204.79.197.200',
                '188.225.38.247',
                '72.21.81.200',
                '194.87.110.230',
                '224.0.0.252',
                '239.255.255.250',
                '172.217.0.227',
                '217.20.116.142',
            ],
            [
                'wcvxsyjfpiovmptigu.com',
                'juuegdhb5196yhd.com',
                'yxogwyndvwp.com',
                'fpdownload2.macromedia.com',
                'qhvofnudibriut.com',
                'qcucafoiu.com',
                'update.googleapis.com',
                'vuykgvnfe.com',
                'bing.com',
                'xxvtuycm.com',
                'fkgobmphqlfdophk.com',
                'luoydxqlqfdwsl.com',
                'xslsexpxhkaynrvy.com',
                'api.bing.com',
                'bnajaaph.com',
                'vhkyyerhh.com',
                'gmtajuepmx.com',
                'bchqmvbgknljayqb.com',
                'gwwrolfyfxtq.com',
                'hxwadlkmebgpojatq.com',
                'ieonline.microsoft.com',
                'bpgfpkyl.com',
                'cqqkroagthpvpj.com',
                'nupppywpufdndt.com',
                'google.com',
                'ojkmfguoeyrvundpkj.com',
                'sgllbjnsljeltl.com',
                'wttqdjftcjmoynl.com',
                'teredo.ipv6.microsoft.com',
                'assvrihswsep.com',
                'tqokxeyihf.com',
                'xyqrydep.com',
                'klovgfiy.com',
                'qagoauqyuqmyqqq.com',
                'mgmqeogvjaydt.com',
                'dns.msftncsi.com',
                'oatlakwbs.com',
                'aniedtnojvdtpv.com',
                'smqrbewtndlartnmq.com',
                'fmmyicwbc.com',
                'vbxdcfcotng.com',
                'dcfifjdtuvbsljji.com',
                'uuhyoifmsolvriphywp.com',
                'tpjtejqldccu.com',
                'xjkokskukjidriemx.com',
                'btpvoepdgdwdv.com',
                'nalqudfenonbatenv.com',
                'fkjvmeprgktateanj.com',
                'slyxqupy.com',
                'acjrleouie.com',
                'hkugaabhnwaymgh.com',
                'sjvishymfmbmtyrvry.com',
                'gcqltysgeybouffocm.com',
                'jiqduciucqqggalieq.com',
                'hceoqxahppy.com',
                'qgcftjlfa.com',
                'ebnastiuaiufo.com',
                'hqelbpqhvkjmpbyd.com',
                'osrifxcfy.com',
                'iecvlist.microsoft.com',
                'www.bing.com',
            ],
            {
                'api.bing.com': {'13.107.13.80'},
                'bing.com': {'204.79.197.200'},
                'dns.msftncsi.com': {'131.107.255.255'},
                'fpdownload2.macromedia.com': {'168.143.243.230'},
                'google.com': {'172.217.0.238'},
                'iecvlist.microsoft.com': {'72.21.81.200'},
                'ieonline.microsoft.com': {'204.79.197.200'},
                'juuegdhb5196yhd.com': {'194.87.110.230'},
                'nupppywpufdndt.com': {'194.87.110.230'},
                'qhvofnudibriut.com': {'217.20.116.142'},
                'smqrbewtndlartnmq.com': {'217.20.116.142'},
                'update.googleapis.com': {'172.217.0.227'},
                'www.bing.com': {'131.253.33.200'},
            },
        ),
    ),
    (
        TEST_FILES / 'demo.pcapng',
        (
            [
                '142.251.30.104',
                '34.160.144.191',
                '34.107.221.82',
                '142.250.151.94',
                '23.215.0.136',
                '142.250.129.94',
                '151.101.193.91',
                '2.22.98.7',
                '34.120.208.123',
                '34.41.139.193',
                '142.250.117.95',
                '142.250.151.113',
                '142.251.30.106',
                '198.98.57.26',
                '142.251.30.141',
                '172.217.16.234',
                'ff02::2',
                '142.251.30.103',
            ],
            [
                'example.com',
                'detectportal.firefox.com',
                'example.org',
                'o.pki.goog',
                'www.google.com',
                'ipv4only.arpa',
                'siekis.com',
                'safebrowsing.googleapis.com',
            ],
            {
                'detectportal.firefox.com': {'34.107.221.82'},
                'example.com': {'23.215.0.136'},
                'example.org': {'23.220.75.238'},
                'ipv4only.arpa': {'192.0.0.170'},
                'o.pki.goog': {'142.250.129.94'},
                'safebrowsing.googleapis.com': {'172.217.16.234'},
                'siekis.com': {'34.41.139.193'},
                'www.google.com': {'142.251.30.106'},
            },
        ),
    ),
]


@pytest.mark.parametrize(('capture', 'expected'), CAPTURES)
def test_extract_entities_pcap(capture, expected):
    entities = _extract_entities_from_capture(capture)
    for elem, expected_elem in zip(entities, expected):
        assert sorted(elem) == sorted(expected_elem)


def test_pcap_json_out():
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


def test_pcap_pretty_out():
    result = runner.invoke(app, args=['enrich', CAPTURES[1][0].as_posix(), '-p', '-r', '40'])
    assert result.exit_code == 0

    assert re.search(r'IOC:\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result.output)
    assert re.search(r'Risk Score:\s+\d+', result.output)
    assert re.search(r'Most Malicious Risk Rule:\s+.+', result.output)
    assert re.search(
        r'Wireshark Query:\s+ip\.src == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} or ip\.dst == \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        result.output,
    )
