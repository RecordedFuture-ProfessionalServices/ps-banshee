PS Banshee reads your Recorded Future API key from the `RF_TOKEN` environment variable (recommended) or from the `-k` / `--api-key` flag on each command.

#### Option 1: Set `RF_TOKEN` (recommended)

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

#### Option 2: Pass with `-k` per command

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

This works on any platform, but is more verbose and the key may land in shell history.

#### Sandbox authorization

To use the `sandbox` commands, PS Banshee also needs a Recorded Future Sandbox API token from the `RF_SANDBOX_TOKEN` environment variable (recommended) or from the `-K` / `--sandbox-key` flag.

##### Option 1: Set `RF_SANDBOX_TOKEN` (recommended)

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

##### Option 2: Pass with `-K` per command

```bash
banshee sandbox -K <your_sandbox_api_key> <sub-command> <arguments>
```

This works on any platform, but is more verbose and the key may land in shell history.

Optionally, set the Sandbox region with the `RF_SANDBOX_CHOICE` environment variable or the `--sandbox-choice` flag. Accepted values are `eu`, `usa`, `apj`, `public`, and `private`. Defaults to `eu`.

```bash
export RF_SANDBOX_CHOICE=usa
```
