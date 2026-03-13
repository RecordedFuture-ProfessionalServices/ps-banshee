from unittest.mock import patch

import pytest
from psengine.entity_lists import EntityList, EntityListMgr, ListApiError
from requests import HTTPError, Response
from typer.testing import CliRunner

from banshee.commands.cmd_lists import app

runner = CliRunner()

COMMAND = 'bulk-add'


def test_list_bulk_add_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 2


@pytest.mark.vcr
def test_http_errors():
    with patch.object(EntityListMgr, 'fetch', side_effect=ListApiError('Generic ListApiError')):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', 'ip:8.8.8.8'])
        assert result.exit_code == 1
    error_400 = Response()
    error_400.status_code = 400
    list_api_error = ListApiError('Mock ListApiError 400')
    list_api_error.__cause__ = HTTPError(response=error_400)
    with patch.object(EntityList, 'add', side_effect=list_api_error):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', 'ip:8.8.8.8'])
        assert 'ERROR_BAD_ID' in result.output
        assert result.exit_code == 0
    error_404 = Response()
    error_404.status_code = 404
    list_api_error = ListApiError('Mock ListApiError 404')
    list_api_error.__cause__ = HTTPError(response=error_404)
    with patch.object(EntityList, 'add', side_effect=list_api_error):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', 'ip:8.8.8.8'])
        assert 'ERROR_NOT_FOUND' in result.output
        assert result.exit_code == 0
    error_500 = Response()
    error_500.status_code = 500
    list_api_error = ListApiError('Mock ListApiError 500')
    list_api_error.__cause__ = HTTPError(response=error_500)
    with patch.object(EntityList, 'add', side_effect=list_api_error):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', 'ip:8.8.8.8'])
        assert 'ERROR_STATUS_500' in result.output
        assert result.exit_code == 0
    error_503 = Response()
    error_503.status_code = 503
    list_api_error = ListApiError('Mock ListApiError 503')
    list_api_error.__cause__ = HTTPError(response=error_503)
    with patch.object(EntityList, 'add', side_effect=list_api_error):
        result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', 'ip:8.8.8.8'])
        assert 'ERROR_STATUS_503' in result.output
        assert result.exit_code == 0


IPS_201 = [
    'ip:5.180.96.152',
    'ip:98.142.95.254',
    'ip:139.224.198.190',
    'ip:185.49.126.52',
    'ip:138.197.71.186',
    'ip:209.141.54.131',
    'ip:188.166.149.250',
    'ip:39.106.152.236',
    'ip:116.196.95.100',
    'ip:85.175.101.203',
    'ip:111.230.62.154',
    'ip:185.150.191.82',
    'ip:121.199.0.54',
    'ip:137.184.67.135',
    'ip:92.118.170.81',
    'ip:188.214.128.130',
    'ip:47.115.54.19',
    'ip:194.32.149.186',
    'ip:101.36.117.41',
    'ip:112.124.39.205',
    'ip:39.107.85.83',
    'ip:156.224.19.17',
    'ip:124.223.200.131',
    'ip:103.145.107.203',
    'ip:108.61.242.65',
    'ip:47.106.171.201',
    'ip:217.138.215.105',
    'ip:14.103.51.225',
    'ip:142.171.32.77',
    'ip:47.120.52.176',
    'ip:143.198.214.96',
    'ip:109.199.101.109',
    'ip:37.114.55.137',
    'ip:112.124.71.123',
    'ip:88.214.26.31',
    'ip:195.230.23.91',
    'ip:123.60.104.67',
    'ip:91.215.85.142',
    'ip:103.41.204.104',
    'ip:124.222.122.160',
    'ip:207.174.3.213',
    'ip:47.236.53.118',
    'ip:51.15.17.193',
    'ip:159.89.182.136',
    'ip:2.58.15.214',
    'ip:91.218.114.25',
    'ip:5.180.96.219',
    'ip:47.94.43.210',
    'ip:39.98.115.22',
    'ip:179.60.149.4',
    'ip:103.238.225.248',
    'ip:47.109.77.180',
    'ip:82.156.108.180',
    'ip:193.124.205.63',
    'ip:152.32.202.240',
    'ip:177.125.40.217',
    'ip:47.90.157.82',
    'ip:191.96.207.55',
    'ip:8.222.156.244',
    'ip:165.227.136.106',
    'ip:47.236.244.191',
    'ip:63.141.237.208',
    'ip:49.232.29.245',
    'ip:148.135.35.239',
    'ip:117.72.39.83',
    'ip:112.126.77.173',
    'ip:81.70.189.76',
    'ip:222.88.186.81',
    'ip:142.171.234.248',
    'ip:45.204.217.98',
    'ip:58.87.94.238',
    'ip:45.144.138.65',
    'ip:70.28.50.223',
    'ip:14.128.37.56',
    'ip:47.243.10.218',
    'ip:39.107.136.241',
    'ip:23.29.115.186',
    'ip:8.154.18.17',
    'ip:156.236.75.199',
    'ip:85.239.237.148',
    'ip:38.54.88.193',
    'ip:111.230.25.167',
    'ip:193.122.74.238',
    'ip:1.92.109.24',
    'ip:45.204.212.245',
    'ip:27.124.40.170',
    'ip:1.92.100.58',
    'ip:64.44.184.105',
    'ip:60.188.59.126',
    'ip:121.4.36.95',
    'ip:101.43.208.122',
    'ip:47.103.218.35',
    'ip:106.54.199.174',
    'ip:157.245.146.223',
    'ip:193.149.189.27',
    'ip:43.228.126.122',
    'ip:92.51.2.17',
    'ip:159.203.70.83',
    'ip:88.210.12.126',
    'ip:192.119.110.32',
    'ip:103.96.128.40',
    'ip:31.220.80.82',
    'ip:198.144.149.131',
    'ip:139.59.59.97',
    'ip:8.134.166.14',
    'ip:124.221.133.199',
    'ip:192.235.96.137',
    'ip:222.253.182.185',
    'ip:101.43.194.127',
    'ip:121.36.93.103',
    'ip:108.170.60.190',
    'ip:118.26.38.52',
    'ip:118.24.121.59',
    'ip:148.135.120.139',
    'ip:84.46.251.145',
    'ip:39.105.121.115',
    'ip:207.231.109.20',
    'ip:121.43.110.28',
    'ip:103.238.227.183',
    'ip:121.36.222.101',
    'ip:185.212.60.145',
    'ip:106.12.116.136',
    'ip:193.32.162.64',
    'ip:117.72.118.156',
    'ip:124.221.30.83',
    'ip:45.88.186.86',
    'ip:193.29.56.122',
    'ip:47.108.134.185',
    'ip:39.105.8.82',
    'ip:45.141.84.60',
    'ip:37.120.247.17',
    'ip:146.70.145.242',
    'ip:82.156.0.140',
    'ip:124.221.199.60',
    'ip:64.94.85.129',
    'ip:144.91.79.54',
    'ip:8.218.33.116',
    'ip:47.98.134.252',
    'ip:78.142.29.118',
    'ip:45.40.96.159',
    'ip:8.134.212.158',
    'ip:139.196.237.171',
    'ip:23.26.108.93',
    'ip:194.68.27.112',
    'ip:193.143.1.180',
    'ip:47.243.175.24',
    'ip:39.109.122.249',
    'ip:47.113.217.92',
    'ip:109.248.6.246',
    'ip:206.188.196.143',
    'ip:84.247.179.77',
    'ip:47.109.178.63',
    'ip:124.222.57.94',
    'ip:146.70.80.66',
    'ip:103.243.25.70',
    'ip:66.94.109.58',
    'ip:8.130.132.210',
    'ip:217.147.172.205',
    'ip:43.133.36.25',
    'ip:157.245.155.179',
    'ip:154.92.14.41',
    'ip:45.144.225.57',
    'ip:39.98.48.153',
    'ip:23.230.108.68',
    'ip:91.192.100.36',
    'ip:106.14.69.133',
    'ip:159.223.0.196',
    'ip:121.43.59.114',
    'ip:147.83.42.250',
    'ip:178.255.244.176',
    'ip:156.238.243.161',
    'ip:101.126.21.197',
    'ip:121.37.170.202',
    'ip:152.42.198.168',
    'ip:36.111.166.231',
    'ip:94.156.177.10',
    'ip:119.28.112.170',
    'ip:112.74.184.37',
    'ip:38.47.103.169',
    'ip:88.214.27.89',
    'ip:103.24.179.18',
    'ip:194.26.29.44',
    'ip:8.149.128.131',
    'ip:42.192.195.221',
    'ip:94.124.192.220',
    'ip:148.135.72.115',
    'ip:106.14.213.29',
    'ip:8.137.114.210',
    'ip:89.46.235.60',
    'ip:1.92.86.239',
    'ip:116.198.229.197',
    'ip:38.60.223.51',
    'ip:206.189.113.118',
    'ip:104.234.114.133',
    'ip:120.46.212.33',
    'ip:43.252.231.29',
    'ip:43.143.130.124',
    'ip:172.111.138.100',
    'ip:123.57.230.183',
    'ip:150.136.90.238',
    'ip:104.244.77.5',
]


@pytest.mark.skip(reason="This test doesn't wok correctly with multithreading")
@pytest.mark.vcr
def test_list_bulk_add_more_than_100_entities():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', *IPS_201])
    assert result.exit_code == 0
    for ip in IPS_201:
        assert ip in result.output


IPS_50 = [
    'ip:190.11.55.175',
    'ip:195.181.200.184',
    'ip:201.219.103.77',
    'ip:24.142.213.138',
    'ip:24.137.48.66',
    'ip:123.207.205.97',
    'ip:93.55.254.157',
    'ip:199.255.65.205',
    'ip:188.37.248.208',
    'ip:93.114.183.15',
    'ip:186.182.52.42',
    'ip:205.215.253.155',
    'ip:174.44.220.76',
    'ip:172.94.17.115',
    'ip:104.203.175.168',
    'ip:45.205.84.234',
    'ip:168.194.167.118',
    'ip:187.170.121.109',
    'ip:104.203.195.166',
    'ip:199.172.199.182',
    'ip:77.159.215.210',
    'ip:117.211.5.59',
    'ip:104.32.133.36',
    'ip:185.143.222.241',
    'ip:83.32.84.126',
    'ip:75.130.51.74',
    'ip:159.146.116.17',
    'ip:177.225.19.238',
    'ip:93.51.19.235',
    'ip:187.150.68.58',
    'ip:83.91.91.107',
    'ip:47.109.44.204',
    'ip:154.27.160.208',
    'ip:200.159.109.162',
    'ip:110.159.178.181',
    'ip:195.181.12.192',
    'ip:43.241.25.92',
    'ip:71.114.62.115',
    'ip:88.146.219.67',
    'ip:203.111.213.12',
    'ip:209.13.125.130',
    'ip:202.27.209.216',
    'ip:212.95.24.89',
    'ip:118.140.253.226',
    'ip:124.220.54.140',
    'ip:184.74.42.186',
    'ip:113.190.41.205',
    'ip:190.57.227.58',
    'ip:99.234.177.146',
    'ip:186.209.89.204',
]


@pytest.mark.skip(reason="This test doesn't wok correctly with multithreading")
@pytest.mark.vcr
def test_list_bulk_add_fewer_than_100_entities():
    result = runner.invoke(app, args=[COMMAND, 'report:wpHivJ', *IPS_50])
    assert result.exit_code == 0
    for ip in IPS_50:
        assert ip in result.output
