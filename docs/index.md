---
title: ""
---

<div style="width: 100%; text-align: center;">
    <img src="assets/rf-logo.png" alt="Recorded Future Logo" style="margin-top: -80px; margin-bottom: 16px;">
</div>
<p style="margin-top: -60px;">
PS Banshee is a command-line tool for fast, efficient access to Recorded Future Intelligence, built for security professionals and SOC teams.
</p>
<img src="img/welcome.gif" alt="Welcome to PS Banshee!" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

!!! tip "Powered by PSEngine"
    PS Banshee is powered by the [PSEngine](https://recordedfuture-professionalservices.github.io/psengine/latest/) library.

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

All required Python dependencies are resolved automatically by `pipx`.  
To use the `pcap` command, ensure you have:

- tshark 3.0.0 or later

### Command Auto Completion

After installing PS Banshee, enable command auto completion with:

```bash
banshee --install-completion
```

Restart your shell to complete the installation. You can now use TAB to auto-complete commands.

## Documentation

To view available commands, just run:

```bash
banshee
```

### Authorization

Provide your Recorded Future API key using the `-k` or `--api-key` argument, or set it as the `RF_TOKEN` environment variable:

```bash
banshee -k <RF_TOKEN> <command> <sub-command> <arguments>
```

### Proxies

If you are behind a proxy, set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables.

To disable SSL verification, use the `-s` flag:

```bash
banshee -s ca rules
```

## Next steps

[Get started](getting-started/index.md) using PS Banshee now!