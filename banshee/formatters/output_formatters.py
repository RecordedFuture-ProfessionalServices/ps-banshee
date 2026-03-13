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

from datetime import datetime
from typing import Union


def format_line(label: str, value: str) -> str:
    """Format string for _human_format."""
    return f'{label:>13}: {value}'


def format_time(timestamp: Union[datetime, str]) -> str:
    """Formats a given time string by splitting it into date and time components.

    Args:
        timestamp (Union[datetime, str]): The input time string in
                                        'YYYY-MM-DDTHH:mm:ss.sssZ' format.

    Returns:
        str: The formatted time string in 'YYYY-MM-DD HH:mm:ss' format.
    """
    if isinstance(timestamp, datetime):
        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

    else:
        formatted_time = timestamp.split('T')
        formatted_time = f'{formatted_time[0]} {formatted_time[1][:-5]}'

    return formatted_time


def color_risk_score(score: int) -> str:
    color = 'red' if score >= 65 else 'yellow' if score >= 25 else 'grey50'
    return f'[{color}]{score}[/{color}]'
