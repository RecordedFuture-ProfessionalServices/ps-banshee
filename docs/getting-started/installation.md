# Installing PS Banshee

## Installation methods

Install ps-banshee with `pipx` or `pip`.

## Installation

PS Banshee is distributed as a Python package. Contact your Recorded Future account representative to obtain it.

!!! tip "PS Banshee requires Python 3.9 or later (up to 3.13)."

### pipx (isolated environment)
To install globally, run:

```bash
pipx install ps_banshee-1.1.0-py3-none-any.whl
```


!!! info "Installing pipx"
    If you don't have pipx installed, see the [installation guide](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx).


### pip (current environment)
To install in the current environment, run:
```bash
pip install ps_banshee-1.1.0-py3-none-any.whl
```


### Dependencies

All required Python dependencies are resolved automatically by `pip`.  
To use the `pcap` command, ensure you have:

- tshark 3.0.0 or later



## Upgrading PS Banshee

To upgrade PS Banshee to a newer version, reinstall using the updated wheel file.

!!! warning "Upgrading from v1.0.0 or earlier"
    If you are upgrading from v1.0.0 or an earlier version, you must uninstall the existing package first before installing the new version.

    **If installed with pipx:**
    ```bash
    pipx uninstall banshee
    pipx install ps_banshee-<new-version>-py3-none-any.whl
    ```

    **If installed with pip:**
    ```bash
    pip uninstall banshee
    pip install ps_banshee-<new-version>-py3-none-any.whl
    ```

**If installed with pipx:**

```bash
pipx install --force ps_banshee-<new-version>-py3-none-any.whl
```

**If installed with pip:**

```bash
pip install --upgrade ps_banshee-<new-version>-py3-none-any.whl
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