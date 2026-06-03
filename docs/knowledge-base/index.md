# Banshee CLI Knowledge Base

> A Recorded Future CLI for terminal-based threat intelligence investigations.
> Built by the Cyber Security Engineers at Recorded Future.
> Validated against `ps-banshee` / `banshee` version 1.3.0.

This knowledge base is designed for LLM consumption (Claude Code, Opus, and other agentic CLIs). Three artifacts are published for agents:

- **Index** — concise table of contents: <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms.txt>
- **Full bundle** — every command group inlined in one document: <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt>
- **Per-group pages** — for selective fetches, served as raw markdown at `https://.../latest/knowledge-base/<group>/index.md` (e.g. `ca`, `ioc`, `list`). Linked from the index above.

To make `banshee` discoverable to your agent in a project, add an action-phrased line to your `CLAUDE.md`, `AGENTS.md`, or equivalent rules file:

> When working with Recorded Future, fetch <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt> for the full `banshee` CLI reference, then use the `banshee` CLI. If that URL is unreachable, run `banshee --help` instead.

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

Last live validation: **2026-06-03** (release 1.3.0 refresh) against `ps-banshee` / `banshee` **1.3.0** with `RF_TOKEN` authentication. This run focused on the surfaces new or changed since 1.2.0: `ca export`, `pba export`, the `pba search --org-id` filter, `list bulk-add --overwrite`, the reworked `list clear`, and the `list add` annotation property.

Validated successfully:

```bash
# Local toolchain and auth presence
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# Read-only API access
banshee ca rules
banshee ca search -t 1d
banshee ca search -t 1d | banshee ca export
banshee ca search -t 2d | banshee ca export --csv
banshee pba search -C 30d -l 5
banshee pba search -C 30d -o uhash:69sKLfTGsS -l 2
banshee pba search -C 30d -l 5 | banshee pba export --csv

# Mutating workflows tested in a sandbox RF tenant
banshee list create banshee_kb_refresh_20260603 entity
banshee list bulk-add report:<list_id> SoA6SP lYNvCK
banshee list bulk-add report:<list_id> SoA6SP --overwrite
banshee list entities report:<list_id>
banshee list clear report:<list_id>
```

Observed caveats:

- `ca export` and `pba export` read **only** from stdin and take no positional arguments. Pipe `banshee ca search` / `banshee pba search` into them; invoking with a TTY (no piped input) raises a `BadParameter` error.
- `pba export` consumes the full `pba search` JSON object (it reads `.data[]`), whereas `ca export` consumes the `ca search` JSON array.
- `list clear` removes a list's entities but does not delete the list itself, and there is no `list delete` command; the sandbox list created above remains (empty) after clearing.
- `pcap enrich` was not live-tested because `tshark` was not installed. This is expected: `banshee pcap enrich --help` raises `RuntimeError: tshark is not installed or not in PATH`.

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
