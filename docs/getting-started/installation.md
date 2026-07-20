# Installing PS Banshee

## Installation methods

Install [ps-banshee](https://pypi.org/project/ps-banshee/) with `pipx` or `pip`.

## Installation

!!! tip "PS Banshee requires Python 3.10 or later (up to 3.13)."

### Recommended: pipx (isolated environment)
To install globally, run:

```bash
pipx install ps-banshee
```


!!! info "Installing pipx"
    If you don't have pipx installed, see the [installation guide](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx).


### Alternative: pip (current environment)
To install in the current environment, run:
```bash
pip install ps-banshee
```


### Dependencies

All required Python dependencies are resolved automatically by `pip`.  
To use the `pcap` command, ensure you have:

- tshark 3.0.0 or later



## Authorization

PS Banshee reads your Recorded Future API key from the `RF_TOKEN` environment variable (recommended) or from the `-k` / `--api-key` flag on each command.

### Option 1: Set `RF_TOKEN` (recommended)

=== "macOS / Linux"

    Current shell only:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    Persist for future shells (zsh — adjust to `~/.bashrc` for bash). Open a new shell after running this (or run `source ~/.zshrc` to apply in the current shell):

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    Current session only:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    Persist for future sessions (open a new PowerShell after running this):

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    Current session only:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    Persist for future sessions (open a new Command Prompt after running this):

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

### Option 2: Pass with `-k` per command

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

This works on any platform, but is more verbose and the key may land in shell history.

### Sandbox authorization

To use the `sandbox` commands, PS Banshee also needs a Recorded Future Sandbox API token from the `RF_SANDBOX_TOKEN` environment variable (recommended) or from the `-K` / `--sandbox-key` flag.

#### Option 1: Set `RF_SANDBOX_TOKEN` (recommended)

=== "macOS / Linux"

    Current shell only:

    ```bash
    export RF_SANDBOX_TOKEN=<your_sandbox_api_key>
    ```

    Persist for future shells (zsh — adjust to `~/.bashrc` for bash). Open a new shell after running this (or run `source ~/.zshrc` to apply in the current shell):

    ```bash
    echo 'export RF_SANDBOX_TOKEN=<your_sandbox_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    Current session only:

    ```powershell
    $env:RF_SANDBOX_TOKEN = '<your_sandbox_api_key>'
    ```

    Persist for future sessions (open a new PowerShell after running this):

    ```powershell
    setx RF_SANDBOX_TOKEN <your_sandbox_api_key>
    ```

=== "Windows (Command Prompt)"

    Current session only:

    ```cmd
    set RF_SANDBOX_TOKEN=<your_sandbox_api_key>
    ```

    Persist for future sessions (open a new Command Prompt after running this):

    ```cmd
    setx RF_SANDBOX_TOKEN <your_sandbox_api_key>
    ```

#### Option 2: Pass with `-K` per command

```bash
banshee sandbox -K <your_sandbox_api_key> <sub-command> <arguments>
```

This works on any platform, but is more verbose and the key may land in shell history.

Optionally, set the Sandbox region with the `RF_SANDBOX_CHOICE` environment variable or the `--sandbox-choice` flag. Accepted values are `eu`, `usa`, `apj`, `public`, and `private`. Defaults to `eu`.

```bash
export RF_SANDBOX_CHOICE=usa
```

## Upgrading PS Banshee

To upgrade PS Banshee to a newer version, reinstall using the updated wheel file.

!!! warning "Upgrading from v1.0.0 or earlier"
    If you are upgrading from v1.0.0 or an earlier version, you must uninstall the existing package first before installing the new version.

    **If installed with pipx:**
    ```bash
    pipx uninstall banshee 
    pipx install ps-banshee
    ```

    **If installed with pip:**
    ```bash
    pip uninstall banshee
    pip install ps-banshee
    ```

**If installed with pipx:**

```bash
pipx install --force ps-banshee
```

**If installed with pip:**

```bash
pip install --upgrade ps-banshee
```

## Shell autocompletion

After installing PS Banshee, enable command auto completion with:

```bash
banshee --install-completion
```

Restart your shell to complete the installation. You can now use TAB to auto-complete commands.

## Uninstallation

To remove PS Banshee from your system, use the appropriate command based on your installation method.

**If installed with pipx:**

```bash
pipx uninstall ps-banshee
```

**If installed with pip:**

```bash
pip uninstall ps-banshee
```


## Next steps

See the [first steps](./first-steps.md) to start using PS Banshee.