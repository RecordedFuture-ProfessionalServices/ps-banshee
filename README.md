# PS Banshee

PS Banshee is a command-line interface (CLI) tool designed to provide quick and efficient access to Recorded Future Intelligence. Built for security professionals, PS Banshee helps streamline investigations and automate common security operations tasks.

![Welcome](docs/img/welcome.gif)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development Environment Setup](#development-environment-setup)
- [Documentation](#documentation)
- [Support](#support)

---

## Key Features

- IOC lookup and search
- Packet capture (pcap) analysis
- Recorded Future Alert search, lookup, and update
- Recorded Future Detection Rules (YARA, Snort, Sigma) search and download
- Recorded Future Entity search and lookup
- Recorded Future List & Watch List management
- Recorded Future Playbook Alert search, lookup, and update
- Recorded Future Risk List download, and creation

## Installation

PS Banshee is available on PyPI and can be installed using `pip` or `pipx`.

!!! tip "PS Banshee requires Python 3.9 or later (up to 3.13)."

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

PS Banshee requires a Recorded Future API key, which can be provided as the `-k` or `--api-key` argument, or set as the `RF_TOKEN` environment variable.

```bash
banshee -k <RF_TOKEN> <command> <sub-command> <arguments>
```

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