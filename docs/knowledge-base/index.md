# Banshee CLI Knowledge Base

> A Recorded Future CLI for terminal-based threat intelligence investigations.
> Built by the Cyber Security Engineers at Recorded Future.
> Validated against `ps-banshee` / `banshee` version 1.2.0.

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

Last live validation: **2026-05-01** (extended audit) against `ps-banshee` / `banshee` **1.2.0** with `RF_TOKEN` authentication.

Validated successfully:

```bash
# Local toolchain and auth presence
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"
jq --version

# Read-only API access
banshee entity search wannacry -l 1
banshee entity lookup SoA6SP
banshee ioc bulk-lookup ip 8.8.8.8
banshee ioc rules ip
banshee ca rules
banshee ca search -t 1d -s New
banshee ca lookup <alert_id>
banshee list search -l 1
banshee pba search --limit 1
banshee pba lookup task:<uuid>
banshee rules search -t sigma -l 1

# Mutating workflows tested in a sandbox RF tenant
banshee list create codex_banshee_smoke_20260501 entity
banshee list info report:<list_id>
banshee list status report:<list_id>
banshee list entities report:<list_id>
banshee list add report:<list_id> SoA6SP smoke=single_add
banshee list bulk-add report:<list_id> ip:8.8.8.8 www.duckdns.org,InternetDomainName
banshee list remove report:<list_id> SoA6SP
banshee list bulk-remove report:<list_id> ip:8.8.8.8 www.duckdns.org,InternetDomainName
banshee list clear report:<list_id>
banshee list create codex_banshee_smoke_text_20260501 text
banshee list entries report:<text_list_id>
banshee ca update <alert_id> -s Pending -n "Codex smoke test"
banshee ca update <alert_id> -n "Codex append smoke test" -A
banshee pba update task:<uuid> -s InProgress -p Informational -t "Codex smoke test"
banshee pba update task:<uuid> -s Resolved -r Never -t "Codex reopen strategy smoke test"

# Local-output workflows
banshee email enrich /tmp/banshee_smoke.eml -r 1
banshee risklist fetch -e ip -l recentValidatedCnc -o /tmp/banshee_smoke_recentValidatedCnc.csv
banshee risklist create -e ip -R recentValidatedCnc -r 70 -f json -o /tmp/banshee_smoke_risklist.json
banshee risklist stat -e ip -l recentValidatedCnc
banshee rules search -t sigma --title Aesthetic --output-path /tmp/banshee_smoke_rules
```

Observed caveats:

- In restricted execution sandboxes, API calls can fail before reaching Recorded Future with DNS errors such as `Failed to resolve 'api.recordedfuture.com'`; allow network access and rerun the same command.
- `pcap enrich` was not live-tested because `tshark` was not installed. This is expected: `banshee pcap enrich --help` raises `RuntimeError: tshark is not installed or not in PATH`.
- `risklist stat -c /tmp/banshee_smoke_risklist.json` returned a Fusion API `400 Bad Request`; the verified stat form is `banshee risklist stat -e ip -l recentValidatedCnc`.

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
| `ca` | [ca.md](ca.md) | Classic Alerts — search, lookup, update |
| `email` | [email.md](email.md) | Enrich EML files with RF intelligence |
| `entity` | [entity.md](entity.md) | Entity search and lookup |
| `ioc` | [ioc.md](ioc.md) | IOC enrichment, bulk enrichment, search, rules |
| `list` | [list.md](list.md) | Manage RF Lists & Watch Lists (create, add/remove entities, entries) |
| `pcap` | [pcap.md](pcap.md) | Enrich packet captures with RF intelligence |
| `pba` | [pba.md](pba.md) | Playbook Alerts — search, lookup, update |
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
