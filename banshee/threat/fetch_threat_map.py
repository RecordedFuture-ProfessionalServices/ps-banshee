#################################### TERMS OF USE ###########################################
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


from psengine.rf_client import RFClient

from .constants import ThreatActorCategories, get_threat_actor_category_ids
from .endpoints import (
    EP_MAIN_THREAT_ACTOR_MAP,
    EP_MAIN_THREAT_MALWARE_MAP,
    EP_ORG_THREAT_ACTOR_MAP,
    EP_ORG_THREAT_MALWARE_MAP,
)


def fetch_threat_actor_map(
    threat_actor_categories: list[ThreatActorCategories] = None, org_id: str = None
):
    rf_client = RFClient()
    payload = {}

    if threat_actor_categories:
        # Fetch the treat map for the given threat actor categories
        payload['categories'] = get_threat_actor_category_ids(threat_actor_categories)

    url = EP_MAIN_THREAT_ACTOR_MAP
    if org_id:
        if not org_id.startswith('uhash:'):
            org_id = 'uhash:' + org_id
        url = EP_ORG_THREAT_ACTOR_MAP.format(org_id)

    response = rf_client.request('post', url, data=payload).json()

    return response.get('data', {}).get('threat_map', [])


def fetch_threat_malware_map(org_id: str = None):
    rf_client = RFClient()
    payload = {}

    url = EP_MAIN_THREAT_MALWARE_MAP
    if org_id:
        if not org_id.startswith('uhash:'):
            org_id = 'uhash:' + org_id
        url = EP_ORG_THREAT_MALWARE_MAP.format(org_id)

    response = rf_client.request('post', url, data=payload).json()

    return response.get('data', {}).get('threat_map', [])
