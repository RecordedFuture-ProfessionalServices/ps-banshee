# Using with AI agents

Banshee is designed to be driven from the terminal — including by AI coding agents such as Claude Code, Codex, and any other LLM that can run shell commands. Two artifacts are published to help an agent learn the CLI:

- **Index** — concise table of contents for selective fetches: [llms.txt](../../llms.txt)
- **Full bundle** — every command group inlined in a single document: [llms-full.txt](../../llms-full.txt)

Both follow the [llms.txt](https://llmstxt.org/) convention.

## Make `banshee` discoverable to your agent

Copy the snippet below and paste it into whichever rules/instructions file your agent reads — `CLAUDE.md`, `AGENTS.md`, or the equivalent for your tool:

```markdown
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
<https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt>

If that URL is unreachable, run `banshee --help` (and `banshee <group> --help`) instead.
```

That snippet is the only thing you need to give your agent. Listing concrete task shapes (IOC risk, alert triage, list management, EML/pcap enrichment) is deliberate — users rarely say "Recorded Future" out loud, so naming the work an agent will actually be asked to do is what makes it recognize the rule applies. Phrasing it as an action ("fetch … then use") matters too: a bare URL reference is usually ignored, and agents tend to act before reading. Pointing at `llms-full.txt` keeps it to a single fetch — there's no need to chain through the index to per-command pages. The `banshee --help` fallback keeps the workflow usable when the docs URL is blocked (for example, if egress is restricted to the Recorded Future API only).

## Authorization

Set the `RF_TOKEN` environment variable in the agent's shell before invoking banshee. The env-var path is strongly preferred for agent workflows — the agent doesn't have to remember to pass `-k` on every call.

See [Installation → Authorization](installation.md#authorization) for full setup instructions (macOS, Linux, Windows).
