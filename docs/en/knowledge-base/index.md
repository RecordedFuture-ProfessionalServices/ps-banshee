# Banshee CLI Knowledge Base

> A Recorded Future CLI for terminal-based threat intelligence investigations.
> Built by the Cyber Security Engineers at Recorded Future.
> Validated against `ps-banshee` / `banshee` version 1.5.0.

This knowledge base is designed for LLM consumption (Claude Code, Opus, and other agentic CLIs). Three artifacts are published for agents:

- **Index** — concise table of contents: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt>
- **Full bundle** — every command group inlined in one document: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>
- **Per-group pages** — for selective fetches, served as raw markdown at `https://.../latest/knowledge-base/<group>/index.md` (e.g. `ca`, `ioc`, `list`). Linked from the index above.

To make `banshee` discoverable to your agent in a project, add an action-phrased line to your `CLAUDE.md`, `AGENTS.md`, or equivalent rules file:

> When working with Recorded Future, fetch <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt> for the full `banshee` CLI reference, then use the `banshee` CLI. If that URL is unreachable, run `banshee --help` instead.

Set `RF_TOKEN` in the shell environment before invoking — see [Authentication](#authentication-global-options) below.

---

## Authentication & Global Options

```
banshee [OPTIONS] COMMAND [ARGS]...
```

| Flag | Short | Description |
|------|-------|-------------|
| `--api-key TEXT` | `-k` | Recorded Future API key. Preferred: set `RF_TOKEN` env var instead. |
| `--no-ssl-verify` | `-s` | Disable SSL verification (use with proxies via `HTTP_PROXY` / `HTTPS_PROXY`). |
| `--debug` | | Enable debug mode. |
| `--version` | | Show version. |
| `--install-completion` | | Install shell tab completion. |
| `--show-completion` | | Print completion config for manual install. |

**Best practice:** Export `RF_TOKEN=<your_api_key>` so you never pass `-k` on every call.

---

## Readiness Checks

Before running workflows, verify the local toolchain and authentication path.

```bash
# CLI is installed and reachable
banshee --version
banshee --help

# Recorded Future API token is present
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# jq is required for most pipeline examples
jq --version

# Read-only API smoke tests
banshee entity search wannacry -l 1
banshee ioc bulk-lookup ip 8.8.8.8 | jq '.[0] | {ioc: .entity.name, score: .risk.score}'

# Required only for pcap workflows; without tshark, even `banshee pcap enrich --help` can fail
command -v tshark
```

If `banshee` is missing, install the Python package `ps-banshee` through your approved Python package workflow, then re-run the checks above.

---

## Live Validation Snapshot

Last live validation: **2026-07-23** (release 1.5.0 refresh) against `ps-banshee` / `banshee` **1.5.0** with `RF_TOKEN` and `RF_SANDBOX_TOKEN` authentication.

Validated successfully:

```bash
# Local toolchain and auth presence
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"
test -n "$RF_SANDBOX_TOKEN" && echo "RF_SANDBOX_TOKEN set"

# Read-only API access
banshee ca rules
banshee ca rules leaked
banshee ca search -t 7d
banshee ca search -t 12h | banshee ca export
banshee ca search -t 12h | banshee ca export --csv
banshee pba search -C 60d -l 3
banshee pba search -o uhash:69sKLfTGsS -C 60d -l 3
banshee pba search -C 60d -l 3 | banshee pba export
banshee pba search -C 60d -l 3 | banshee pba export --csv
banshee ioc bulk-lookup ip 8.8.8.8

# Sandbox read-only API access
banshee sandbox stats --days 7
banshee sandbox list --limit 3
banshee sandbox profile list
banshee sandbox report overview 260722-x8lgjahyvx
banshee sandbox report static 260722-x8lgjahyvx
banshee sandbox report behavioral 260722-x8lgjahyvx
```

Observed caveats:

- `ca export` and `pba export` read **only** from stdin and take no positional arguments. Pipe `banshee ca search` / `banshee pba search` into them.
- `pba export` consumes the full `pba search` JSON object (it reads `.data[]`), whereas `ca export` consumes the `ca search` JSON array.
- In `ca export --csv` the `Updated` column is currently always empty (reserved for future API support) - confirmed in this run.
- The new `pba search --org-id` (`-o`) filter accepts a 10-character ID or the 16-character `uhash:` form and is repeatable.
- `pcap enrich` was not live-tested because `tshark` was not installed. This is expected: `banshee pcap enrich --help` raises `RuntimeError: tshark is not installed or not in PATH`.
- `sandbox stats` includes a `soar_skipped` field; when `true`, `.top_iocs.verified_network` is empty (SOAR validation was not run for the period).
- Sandbox mutating commands (`submit`, `delete`, `set-profile`, `download`, `profile create/update/delete`) were not live-tested in this refresh.
- `sandbox download` produces AES-encrypted ZIP archives (password `infected`); extract with `7z x -pinfected <file>.zip` — standard `unzip` does not handle AES zips reliably.

---

## Output Conventions

- All commands default to **JSON output** to stdout — pipe-friendly by design.
- Add `--pretty` / `-p` to any command for human-readable formatted output.
- Most commands support piping via stdin (newline- or whitespace-separated IDs/IOCs).
- Combine with `jq` for advanced filtering (examples throughout).
- Response shapes differ by endpoint. Notable patterns:
  - `ioc lookup` returns a JSON array and uses `.risk.evidenceDetails[]` for detailed risk evidence.
  - `ioc bulk-lookup` returns a JSON array and uses `.risk.rule.evidence[]` for bulk risk evidence.
  - `ioc search` returns an object with results under `.data.results[]`.
  - `pba search` returns an object with alert records under `.data[]`.
  - `pcap enrich` and `email enrich` return flat records such as `.ioc`, `.risk_score`, and `.rule_evidence[]`.

---

## Command Groups

| Group | Page | Description |
|-------|------|-------------|
| `ca` | [ca.md](ca.md) | Classic Alerts — search, lookup, update, export |
| `email` | [email.md](email.md) | Enrich EML files with RF intelligence |
| `entity` | [entity.md](entity.md) | Entity search and lookup |
| `ioc` | [ioc.md](ioc.md) | IOC enrichment, bulk enrichment, search, rules |
| `list` | [list.md](list.md) | Manage RF Lists & Watch Lists (create, add/remove entities, entries) |
| `pcap` | [pcap.md](pcap.md) | Enrich packet captures with RF intelligence |
| `pba` | [pba.md](pba.md) | Playbook Alerts — search, lookup, update, export |
| `risklist` | [risklist.md](risklist.md) | Fetch, create, and inspect risk lists |
| `rules` | [rules.md](rules.md) | Search and download detection rules (Sigma, YARA, Snort) |
| `sandbox` | [sandbox.md](sandbox.md) | Submit files and URLs for sandbox analysis; retrieve reports; manage profiles; download samples |

---

## Notes for LLMs

- **All IDs are opaque short strings** (e.g. `tybakN`, `1b0s1q`) — never guess them; always retrieve via search first.
- **PBA alert IDs** use UUID format and are returned with the `task:` prefix already included by `pba search` (`.data[].playbook_alert_id`). Pass them as-is to `pba lookup` and `pba update` — do not add an extra `task:`.
- **`ca update` and `pba update` return plain text**, not JSON — `SUCCESS:\n<ALERT_ID>` per updated alert. Do not pipe to `jq`.
- **stdin piping** is consistent across all bulk/update commands: pipe newline-separated IDs or IOCs directly.
- **`--pretty` is not JSON** — it's human-readable and unsuitable for further parsing with `jq`. Omit it in pipelines.
- **Risk rules** (used in `ioc rules`, `risklist fetch`, `risklist create`) are named strings like `recentValidatedCnc`, `analystNote`, `recentPhishing`. Discover available rule names with `banshee ioc rules <entity_type>`.
- **Entity IDs vs. name,type pairs**: `list bulk-add` / `list bulk-remove` accept both — use `SoA6SP` (RF ID) or `wannacry,Malware` (name + type) or `ip:8.8.8.8` (type-prefixed value).
- **`risklist create --fusion`** uploads the result directly to RF Fusion; `--output-path` is then interpreted as a Fusion destination path, not a local path.
- **`ioc lookup` vs `ioc bulk-lookup` evidence paths differ**: `ioc lookup` uses `.risk.evidenceDetails[]`; `ioc bulk-lookup` uses `.risk.rule.evidence[]`. They are not interchangeable.
