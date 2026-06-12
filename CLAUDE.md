# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`ps-banshee` is a Typer-based CLI (`banshee`) that wraps Recorded Future's API for terminal threat-intelligence work. All Recorded Future API access goes through the **`psengine`** SDK (`psengine~=2.6.0`) — managers (`ClassicAlertMgr`, `LookupMgr`, `RisklistMgr`, …) plus pydantic models. Banshee never calls the HTTP API directly.

Supports Python 3.10–3.13; CI runs the test suite across the full matrix, so version-specific behavior matters (e.g. `pathlib` internals differ between 3.10 and 3.11+).

## Common commands

Use the project venv at `.venv/` (the `banshee` on global PATH may be a stale install — check `banshee --version` against `pyproject.toml`).

```bash
make setup        # uv venv + uv pip install -e ".[dev,docs]" (then: source .venv/bin/activate)
make test         # review (lint) + unittests — the full gate
make unittests    # pytest with coverage (gate: --cov-fail-under=84), random order by module
make review       # ruff format --check + ruff check  (read-only, what CI enforces)
make rev          # ruff format + ruff check --fix     (auto-fix before committing)
make build        # uv build

# Run one test (tests are random-ordered, so never rely on ordering)
.venv/bin/python -m pytest tests/test_cmd_ca_search.py::test_ca_search_no_args -v

# Run the CLI from source
.venv/bin/banshee <group> <subcommand> ...
```

`RF_TOKEN` must be set in the environment for live runs (not for the test suite — see Testing). The `pcap` command additionally requires `tshark` on PATH.

## Architecture

**Command auto-discovery.** `banshee/main.py` builds the Typer app by importing every `banshee/commands/cmd_*.py` module at startup. Each such module must export `app` (a `Typer`), `CMD_NAME`, `CMD_HELP`, and `CMD_RICH_HELP`. **To add a command group, drop a new `cmd_*.py` — there is no central registry to edit.**

**Two-layer command structure.** Each `commands/cmd_*.py` is a thin Typer layer: it declares options/arguments, validates and parses input, then delegates to a sibling **feature package** that holds the real logic (psengine calls, formatting). The mapping is not 1:1 by name:

| Group | Command module | Feature package |
|---|---|---|
| `ca` | `cmd_classic_alerts.py` | `legacy_alerts/` |
| `pba` | `cmd_playbook_alerts.py` | `playbook_alerts/` |
| `ioc` | `cmd_ioc.py` | `indicators/` |
| `entity` | `cmd_entity.py` | `entity_match/` |
| `list` | `cmd_lists.py` | `lists/` |
| `risklist` | `cmd_risklist.py` | `risklist/`, `fusion_files/` |
| `rules` | `cmd_rules.py` | `detection_rules/` |
| `email` | `cmd_email.py` | `email/` |
| `pcap` | `cmd_pcap_enrich.py` | `pcap_enrich/` |

When changing a command, the option/flag definitions live in `cmd_*.py`; the behavior lives in the feature package.

**Command declaration.** Commands are registered with the `banshee_cmd(app, help_, epilog)` decorator (`branding.py`), which appends branding to help text. Long help/example blocks live centrally in `commands/epilogs.py`. Shared CLI options are reused from `commands/args.py` (`OPT_RF_API_KEY` → `RF_TOKEN` envvar, `OPT_PRETTY_PRINT`, `OPT_NO_SSL_VERIFY`).

**Auth / config is global, set once.** `main.py`'s `@app.callback` runs before any subcommand and calls `app_config.config_init(...)`, which initializes the psengine `Config` singleton (`Config.init(rf_token=..., app_id=..., client_ssl_verify=...)`). The `app_id` encodes the invoked command path (e.g. `banshee_ca-search/1.3.0`). Feature code therefore just instantiates psengine managers and they pick up the configured token — do **not** thread the token through manually.

**Output conventions.** JSON to stdout by default (pipe-friendly); `--pretty`/`-p` switches to human-readable rich output (not parseable — omit in pipelines). Several commands read IDs/IOCs from stdin; `ca export` and `pba export` are stdin-only (they consume the JSON from the matching `search`). `polars` is used for tabular enrichment data (email/pcap), `rich` for rendering.

**Error handling.** Uncaught exceptions are squelched by `squelch_uncaught_exception` to a single `ExceptionType: message` line on stderr; pass `--debug` to get full tracebacks.

## Testing

- **pytest + pytest-vcr.** API interactions are replayed from recorded cassettes in `tests/cassettes/*.yaml`, so the suite needs **no live API or real token** — `conftest.py` injects a fake token (`PS_RF_TOKEN`). The `X-RFToken` header is scrubbed from recordings. Adding or changing an API call requires recording a new cassette (with a real token), after which it replays offline.
- One test file per command: `tests/test_cmd_<group>_<sub>.py`.
- Tests run in **random order bucketed by module** — never write tests that depend on execution order.
- Coverage gate is **84%** (`--cov-fail-under=84`).

## Linting conventions (ruff, enforced in CI)

- Line length 100, **single quotes**, Google-style docstrings, large rule set with `preview = true`.
- **Copyright header is enforced (CPY001):** every non-test file under `banshee/` must begin with the exact "TERMS OF USE" notice block — copy it from any existing source file when creating a new module. Tests are exempt.
- `print()` is allowed under `banshee/*` (this is a CLI); it is flagged elsewhere.

## Docs & knowledge base

The docs are an mkdocs-material site under `docs/`.

**When you edit a command's help text or epilog, or add/rename a command, also update `docs/reference/commands.md`.** That hand-authored page is the command reference users actually read on the website, and it often carries more context than `--help` (rendered tables, field descriptions, worked examples, caveats) because it's easier to visualise there. It is not generated from the CLI, so it does not update itself — `make review`/CI will not catch the drift. `commands.md` is wired into the nav (`mkdocs.yml` → `nav` → `reference/commands.md`).

**LLM-facing instructions** live in `docs/knowledge-base/*.md` — one hand-authored page per command group plus `index.md`. They are the source for the agent artifacts published at the site root: `llms.txt` (index) and `llms-full.txt` (every page inlined). Those two files are **generated at mkdocs build time** by the `llmstxt-md` plugin (`mkdocs.yml` → `plugins` → `llmstxt-md`): the `markdown_description` is the preamble and the `sections:` list selects which `knowledge-base/*.md` pages get bundled. So to change what agents see, edit the knowledge-base pages and/or the plugin block — never hand-edit `llms*.txt`. `docs/getting-started/llms.md` is the human page explaining these artifacts and the rules-file snippet users copy into their agent.

At the end of every release, run the `/refresh-kb` workflow (`.claude/commands/refresh-kb.md`) to sync the knowledge-base pages and the `llmstxt-md` plugin block with CLI changes since the last release tag.
