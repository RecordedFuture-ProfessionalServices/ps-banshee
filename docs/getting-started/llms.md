# Using with AI agents

Banshee is designed to be driven from the terminal — including by AI coding agents (Claude Code, Cursor, Windsurf, Aider, Copilot CLI, Codex, and any other LLM that can run shell commands). Two artifacts are published to help an agent learn the CLI:

- **Index** — concise table of contents for selective fetches: [llms.txt](../../llms.txt)
- **Full bundle** — every command group inlined in a single document: [llms-full.txt](../../llms-full.txt)

Both follow the [llms.txt](https://llmstxt.org/) convention.

## Make `banshee` discoverable to your agent

Add a short, action-phrased instruction to whichever rules/instructions file your agent reads — `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.windsurfrules`, or the equivalent for your tool:

> When working with Recorded Future, fetch <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt> for the full `banshee` CLI reference, then use the `banshee` CLI. If that URL is unreachable, run `banshee --help` (and `banshee <group> --help`) instead.

Phrasing it as an action ("fetch … then use") is deliberate: a bare URL reference is usually ignored, and agents tend to act before reading. Pointing at `llms-full.txt` keeps it to a single fetch — there's no need to chain through the index to per-command pages. The `banshee --help` fallback keeps the workflow usable for network-restricted agents.

For agents that run fully offline, vendor a copy of `llms-full.txt` into your project (e.g. `docs/banshee-cli.md`) and reference that local path instead of the URL.

## Authorization

Set the `RF_TOKEN` environment variable in the agent's shell before invoking banshee. The env-var path is strongly preferred for agent workflows — the agent doesn't have to remember to pass `-k` on every call.

See [Installation → Authorization](installation.md#authorization) for full setup instructions (macOS, Linux, Windows).
