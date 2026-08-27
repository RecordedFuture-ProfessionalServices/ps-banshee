# Using with AI agents

Banshee is designed to be driven from the terminal — including by AI coding agents such as Claude Code, Codex, and any other LLM that can run shell commands. Two artifacts are published to help an agent learn the CLI:

- **Index** — concise table of contents for selective fetches: [llms.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt)
- **Full bundle** — every command group inlined in a single document: [llms-full.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt)

Both follow the [llms.txt](https://llmstxt.org/) convention.

## Make `banshee` discoverable to your agent

Copy the snippet below and paste it into whichever rules/instructions file your agent reads — `CLAUDE.md`, `AGENTS.md`, or the equivalent for your tool:

```
## Recorded Future (banshee CLI)

When a request involves Recorded Future or threat intelligence, use the
`banshee` CLI. This covers, for example:

- checking or enriching the risk of an IOC (IP, domain, URL, file hash, or CVE)
- looking up or searching for entities
- triaging Classic or Playbook alerts
- managing RF lists and watchlists
- fetching or building risk lists
- finding or downloading detection rules (Sigma, YARA, Snort)
- enriching an email (`.eml`) or packet capture (`.pcap`)

First fetch the full command reference, then run `banshee`:
<https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>

If that URL is unreachable, or a command from the reference isn't present in your
installed version, run `banshee --help` (and `banshee <group> --help`) to confirm
the commands your binary actually supports.
```

## Authorization

Set the `RF_TOKEN` environment variable in the agent's shell before invoking banshee. The env-var path is strongly preferred for agent workflows — the agent doesn't have to remember to pass `-k` on every call.

See [Installation → Authorization](https://recordedfuture-professionalservices.github.io/ps-banshee/getting-started/installation/#authorization) for full setup instructions (macOS, Linux, Windows).
