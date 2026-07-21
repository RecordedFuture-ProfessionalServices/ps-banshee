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

from typing import Annotated, Literal, Optional, get_args

import click
from psengine.sandbox.sandbox import Browser, NetworkMode
from psengine.sandbox.sandbox_mgr import SandboxChoice, SandboxSubset
from typer import Option

# Profile fields that `sandbox profile update --unset` can clear.
UnsetField = Literal['network', 'browser', 'geolocation']

################################
# Global options / arguments
################################

# How to use: api_key: RF_API_KEY = None
OPT_RF_API_KEY = Annotated[
    Optional[str],
    Option(
        '--api-key', '-k', help='Recorded Future API Key', envvar='RF_TOKEN', show_default=False
    ),
]

# How to use: pretty: PRETTY_PRINT = False
OPT_PRETTY_PRINT = Annotated[
    bool, Option('--pretty', '-p', help='Pretty print the results in a human readable format')
]


OPT_NO_SSL_VERIFY = Annotated[
    Optional[bool],
    Option(
        '--no-ssl-verify',
        '-s',
        help="""Disable SSL Verification. Useful when using proxies. To
            utilize a proxy set the environment variable HTTP_PROXY or HTTPS_PROXY.""",
    ),
]

OPT_SANDBOX_KEY = Annotated[
    Optional[str],
    Option(
        '--sandbox-key',
        '-K',
        envvar='RF_SANDBOX_TOKEN',
        help='Recorded Future Sandbox API token.',
        show_default=False,
    ),
]

OPT_SANDBOX_CHOICE = Annotated[
    str,
    Option(
        '--sandbox-choice',
        envvar='RF_SANDBOX_CHOICE',
        help='Sandbox region.',
        click_type=click.Choice(get_args(SandboxChoice), case_sensitive=False),
    ),
]

OPT_SANDBOX_SUBSET = Annotated[
    str,
    Option(
        '--subset',
        '-s',
        help='Sample scope.',
        click_type=click.Choice(get_args(SandboxSubset), case_sensitive=False),
    ),
]

OPT_SANDBOX_NETWORK = Annotated[
    Optional[str],
    Option(
        '--network',
        '-N',
        help='The type of networking used during analysis.',
        show_default=False,
        click_type=click.Choice(get_args(NetworkMode), case_sensitive=False),
    ),
]

OPT_SANDBOX_BROWSER = Annotated[
    Optional[str],
    Option(
        '--browser',
        '-b',
        help='Browser used by analyses.',
        show_default=False,
        click_type=click.Choice(get_args(Browser), case_sensitive=False),
    ),
]

OPT_PROFILE_UNSET = Annotated[
    Optional[list[str]],
    Option(
        '--unset',
        help='Clear a field on the profile (repeatable).',
        show_default=False,
        click_type=click.Choice(get_args(UnsetField), case_sensitive=False),
    ),
]
