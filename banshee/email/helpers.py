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

import json
from typing import Annotated

from psengine.common_models import RFBaseModel
from pydantic import BeforeValidator, Field


def arrange_data(data) -> list[str]:
    data = json.loads(data)
    return sorted(data.values())


class TARisklist(RFBaseModel):
    """Custom TA Risklist validator."""

    ioc: str = Field(validation_alias='Name')
    ta_names: Annotated[list[str], BeforeValidator(arrange_data)] = Field(
        validation_alias='ThreatActorNames'
    )
