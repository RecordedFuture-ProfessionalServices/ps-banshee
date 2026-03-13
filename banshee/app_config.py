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


from psengine.config import Config
from pydantic import ValidationError

from ._version import __version__
from .commands.errors import InitConfigError


def config_init(cmd: str, rf_token: str = None, no_ssl_verify: bool = False) -> Config:
    """Global configuration for the CLI.

    Args:
        cmd (str): The command name + sub command, used to generate the app_id,
            typically will be the name one of the banshee commands,
            confor example: 'ca-search', or 'entity-lookup'.
        rf_token (str, optional): The Recorded Future API token.
        no_ssl_verify (bool, optional): Disable SSL verification.
    """
    # invert no_ssl_verify
    ssl_verify = not no_ssl_verify
    app_id = f'banshee_{cmd}/{__version__}'
    try:
        Config.init(rf_token=rf_token, app_id=app_id, client_ssl_verify=ssl_verify)
    except ValidationError as e:
        if 'rf_token' in e.errors()[0]['loc']:
            raise InitConfigError('Invalid Recorded Future API key')  # noqa: B904
        raise InitConfigError(e.errors()[0]['msg'])  # noqa: B904
