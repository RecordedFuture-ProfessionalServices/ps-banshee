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

from typing import Annotated, Optional

from typer import Option

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
