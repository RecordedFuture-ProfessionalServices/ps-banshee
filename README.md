# PS Banshee

**PS Banshee** is a command-line interface (CLI) tool designed to provide quick and efficient access to Recorded Future Intelligence. Built for security professionals, PS Banshee helps streamline investigations and automate common security operations tasks.

---

## Key Features

- E-mail (EML) enrichment
- IOC lookup and search
- Packet capture (pcap) enrichment
- Recorded Future Alert search, lookup, update and export
- Recorded Future Detection Rules (YARA, Snort, Sigma) search and download
- Recorded Future Entity search and lookup
- Recorded Future List & Watch List management
- Recorded Future Playbook Alert search, lookup, update and export
- Recorded Future Risk List download, and creation

## Installation

PS Banshee is available on [PyPI](https://pypi.org/project/ps-banshee/) and can be installed using `pip` or `pipx`.

> **Note:** PS Banshee requires Python 3.10 or later (up to 3.13).

### Recommended: pipx (isolated environment)
To install globally, run:

```bash
pipx install ps-banshee
```


> **Note:** If you don't have pipx installed, see the [installation guide](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx).


### Alternative: pip (current environment)
To install in the current environment, run:
```bash
pip install ps-banshee
```

### Dependencies

`pipx` will automatically resolve all Python dependencies.  
If you want to use the `pcap` command, you will also need:

- tshark 3.0.0 or later

### Command Auto Completion

After installing PS Banshee, you can enable command auto completion:

```bash
banshee --install-completion
```

Restart your shell to complete the installation. You can now use TAB to auto-complete commands.

## Usage

To see the list of available commands, run:

```bash
banshee -h
```

### Authorization

PS Banshee reads your Recorded Future API key from the `RF_TOKEN` environment variable (recommended) or from the `-k` / `--api-key` flag on each command.

#### Option 1: Set `RF_TOKEN` (recommended)

**macOS / Linux**

Current shell only:

```bash
export RF_TOKEN=<your_api_key>
```

Persist for future shells (zsh — adjust to `~/.bashrc` for bash). Open a new shell after running this (or run `source ~/.zshrc` to apply in the current shell):

```bash
echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
```

**Windows (PowerShell)**

Current session only:

```powershell
$env:RF_TOKEN = '<your_api_key>'
```

Persist for future sessions (open a new PowerShell after running this):

```powershell
setx RF_TOKEN <your_api_key>
```

**Windows (Command Prompt)**

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

### Proxies

If you are behind a proxy, set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables.

To disable SSL verification, use the `-s` flag:

```bash
banshee -s ca rules
```

### Command Help

All commands support the `--help` (`-h`) option:

```bash
banshee -h
banshee ca --help
banshee ioc lookup --help
banshee list bulk-add -h
```

## Support

Submit a [support request](https://support.recordedfuture.com/hc/en-us/requests/new) for help alternatively reach out to [support@recordedfuture.com](mailto:support@recordedfuture.com).

---

**PS Banshee is developed and maintained by the Recorded Future Professional Services Cyber Security Engineers  🚀**