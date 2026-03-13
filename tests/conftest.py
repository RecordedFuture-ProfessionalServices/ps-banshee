import os
import re
import sys
from pathlib import Path

import pyshark
import pytest
from psengine.config import Config, get_config
from psengine.enrich import LookupMgr, SoarMgr

from banshee import version

from .vcr_utils import scrub_response

RF_API_KEY = 'PS_RF_TOKEN'
APP_ID = f'banshee:tests_/{version}'

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)


###############################################################################
# VCR fixtures
###############################################################################
@pytest.fixture(scope='session')
def vcr_config():
    return {
        'filter_headers': [('X-RFToken', 'bmljZSB0cnkgOikpKSk=')],
        'before_record_response': scrub_response,
    }


@pytest.fixture
def capture():
    def _capture(filters):
        p = Path(__file__).parent / 'files' / 'small.pcap'
        with pyshark.FileCapture(p, display_filter=filters, use_ek=True) as f:
            return f

    return _capture


def customer_query_param_match(r1, r2):
    query_params_1 = dict(r1.query)
    query_params_2 = dict(r2.query)

    if set(query_params_1.keys()) != set(query_params_2.keys()):
        return False

    for key in query_params_1:
        if sorted(query_params_1[key].split(',')) != sorted(query_params_2[key].split(',')):
            return False

    return True


@pytest.fixture(scope='module')
def vcr(vcr):
    vcr.register_matcher('query_param', customer_query_param_match)
    vcr.match_on = ['method', 'scheme', 'host', 'port', 'path', 'query_param']
    return vcr


###############################################################################
# PSEngine Config fixtures
###############################################################################


@pytest.fixture(scope='session', autouse=True)
def config():
    Config.init(
        rf_token=os.environ.get(RF_API_KEY),
        app_id=APP_ID,
    )
    return get_config()


###############################################################################
# Enrichment fixtures
###############################################################################


@pytest.fixture
def lookup():
    return LookupMgr()


@pytest.fixture
def soar():
    return SoarMgr()


################################################################################
# Miscellaneous fixtures
################################################################################
@pytest.fixture
def _reset_sys_excepthook():
    """Fixture to reset sys.excepthook before and after a test."""
    original_excepthook = sys.excepthook
    yield
    sys.excepthook = original_excepthook
