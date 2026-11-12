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

_TYPE_MAPPING = {
    'type:IpAddress': 'ip',
    'type:InternetDomainName': 'domain',
    'type:Hash': 'hash_',
    'type:Url': 'url',
    'type:CyberVulnerability': 'vulnerability',
}

MAX_ENRICHMENT_WORKERS = 20
PRETTY_IOC_DISPLAY_CAP = 20

INTEL_CARD_BASE = 'https://app.recordedfuture.com/portal/intelligence-card'


class LinkSource(Enum):
    """Enum for possible source types from links."""

    TECHNICAL = 'Technical'
    INSIKT = 'Insikt'
