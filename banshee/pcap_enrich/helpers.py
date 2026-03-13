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
import re
import subprocess
from typing import Annotated

from psengine.common_models import RFBaseModel
from pydantic import BeforeValidator, Field

from .constants import MIN_TSHARK_VERSION


def arrange_data(data) -> list[str]:
    data = json.loads(data)
    return sorted(data.values())


class TARisklist(RFBaseModel):
    """Custom TA Risklist validator."""

    ioc: str = Field(validation_alias='Name')
    ta_names: Annotated[list[str], BeforeValidator(arrange_data)] = Field(
        validation_alias='ThreatActorNames'
    )


def get_tshark_version() -> str:
    try:
        result = subprocess.run(
            ['tshark', '--version'],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract the version from the output
        version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
        if not version_match:
            raise RuntimeError(f'Unable to parse tshark version from output: {result.stdout}')
        return version_match.group(1)  # Return only the version number
    except FileNotFoundError:
        raise RuntimeError('tshark is not installed or not in PATH.') from None
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Failed to verify tshark version: {e.stderr}') from e


def check_tshark_version() -> bool:
    """Check if the installed tshark version is greater than or equal to MIN_TSHARK_VERSION."""
    current_version = get_tshark_version()
    if not current_version >= MIN_TSHARK_VERSION:
        raise RuntimeError(
            f'tshark version {current_version} is installed, but version {MIN_TSHARK_VERSION} or higher is required by this command. Please update tshark to meet the minimum version requirement.'  # noqa: E501
        )
