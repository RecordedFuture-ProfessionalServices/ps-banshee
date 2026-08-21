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


from psengine.config import Config, ConfigModel
from psengine.sandbox.sandbox_mgr import SandboxChoice
from pydantic import ValidationError, field_validator

from ._version import __version__
from .commands.errors import InitConfigError


class BansheeConfig(ConfigModel):
    """Banshee-specific config extending psengine's ConfigModel.

    Adds ``sandbox_choice`` (reads ``RF_SANDBOX_CHOICE`` via env prefix ``RF_``).
    ``sandbox_token`` is already provided by the parent ``ConfigModel`` via ``RF_SANDBOX_TOKEN``.
    """

    sandbox_choice: SandboxChoice = 'eu'

    @field_validator('sandbox_choice', mode='before')
    @classmethod
    def _normalise_sandbox_choice(cls, v):
        return v.lower() if isinstance(v, str) else v


def config_init(
    cmd: str,
    rf_token: str = None,
    no_ssl_verify: bool = False,
    sandbox_key: str = None,
    sandbox_choice: SandboxChoice = 'eu',
) -> Config:
    """Global configuration for the CLI.

    Args:
        cmd (str): The command name + sub command, used to generate the app_id,
            typically will be the name one of the banshee commands,
            for example: 'ca-search', or 'entity-lookup'.
        rf_token (str, optional): The Recorded Future API token.
        no_ssl_verify (bool, optional): Disable SSL verification.
        sandbox_key (str, optional): The Recorded Future Sandbox API token.
        sandbox_choice (SandboxChoice, optional): Sandbox region. Default: 'eu'.
    """
    ssl_verify = not no_ssl_verify
    app_id = f'banshee_{cmd}/{__version__}'
    try:
        Config.init(
            config_class=BansheeConfig,
            rf_token=rf_token,
            app_id=app_id,
            client_ssl_verify=ssl_verify,
            sandbox_token=sandbox_key,
            sandbox_choice=sandbox_choice,
        )
    except ValidationError as e:
        if 'rf_token' in e.errors()[0]['loc']:
            raise InitConfigError('Invalid Recorded Future API key')  # noqa: B904
        raise InitConfigError(e.errors()[0]['msg'])  # noqa: B904
