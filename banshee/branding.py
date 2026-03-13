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


from typer import Typer

BRANDING = ':rocket: \033[93mBrought to you by the Cyber Security Engineers at Recorded Future\033[0m :rocket:'  # noqa: E501


def banshee_cmd(app: Typer, help_: str, epilog: str, *args, **kwargs):
    """Main decorator create banshee commands.
    Under the hood, it adds branding to the help text of the command.


    Args:
        app (Typer): The Typer app instance
        help_ (str): The help text for the command
        epilog (str): The epilog text for the command
        *args: Additional arguments to pass to the command
        **kwargs: Additional keyword arguments to pass to the command

    Returns:
        Typer: The updated Typer app instance
    """
    help_ += f'\n\n{BRANDING}'
    return app.command(help=help_, epilog=epilog, *args, **kwargs)  # noqa: B026
