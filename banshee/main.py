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


import importlib
import sys
from collections import namedtuple
from pathlib import Path
from typing import Annotated, Optional

import typer
import urllib3

from ._version import __version__
from .app_config import config_init
from .branding import BRANDING
from .commands.args import OPT_NO_SSL_VERIFY, OPT_RF_API_KEY

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Command = namedtuple('Command', ['cmd', 'name', 'cmd_help', 'cmd_rich_help'])

PKG_NAME = __name__.split('.')[0]
CMD_FOLDER = (Path(__file__).parent / 'commands').resolve()

APP_DESCRIPTION = f"""A Recorded Future based CLI application providing quick functioning tools to easily interact with APIs and perform basic terminal based investigations. {BRANDING}"""  # noqa: E501


def get_commands() -> list[Command]:
    commands = []
    for filename in sorted(p.name for p in CMD_FOLDER.iterdir()):
        if filename.endswith('.py') and filename.startswith('cmd_'):
            module_name = filename[:-3]
            module = importlib.import_module(f'.commands.{module_name}', package=PKG_NAME)
            commands.append(
                Command(
                    module.app,
                    module.CMD_NAME,
                    module.CMD_HELP + f'\n\n{BRANDING}\n\n',
                    module.CMD_RICH_HELP,
                )
            )

    return commands


app = typer.Typer(
    pretty_exceptions_enable=False,
    no_args_is_help=True,
    rich_markup_mode='markdown',
    context_settings={'help_option_names': ['-h', '--help']},
    help=APP_DESCRIPTION,
)

for command in get_commands():
    app.add_typer(
        command.cmd, name=command.name, help=command.cmd_help, rich_help_panel=command.cmd_rich_help
    )


def version_callback(value: bool):
    if value:
        print(f'PS Banshee version: {__version__}')
        raise typer.Exit()


def squelch_uncaught_exception(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print(f'{exc_type.__name__}: {exc_value}', file=sys.stderr)


def get_called_commands(ctx: typer.Context) -> str:
    # banshee ioc lookup 1.1.1.1 will return `ioc-lookup`
    command = ctx.command
    parts = []
    for arg in sys.argv[1:]:
        # Discard cmd options
        if arg.startswith('-'):
            continue
        if hasattr(command, 'commands') and arg in command.commands:
            parts.append(arg)
            command = command.commands[arg]
    return '-'.join(parts)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[  # noqa: ARG001
        Optional[bool],
        typer.Option(
            '--version', callback=version_callback, is_eager=True, help='Show version information.'
        ),
    ] = None,
    debug: Annotated[
        Optional[bool],
        typer.Option('--debug', help='Run banshee in debug mode.', is_eager=True),
    ] = False,
    api_key: OPT_RF_API_KEY = None,
    no_ssl_verify: OPT_NO_SSL_VERIFY = False,
):
    if not debug:
        sys.excepthook = squelch_uncaught_exception

    config_init(get_called_commands(ctx), api_key, no_ssl_verify)
