---
description: Refresh the LLM knowledge base from CLI changes since the last release tag. Run at the end of every release; review the diff in your IDE before committing.
---

You are refreshing `docs/knowledge-base/` and the related `mkdocs.yml` plugin sections so they reflect the current state of the `banshee` CLI. This command is invoked at the end of every release. The user reviews your edits in their IDE and commits them — you must **not** run any git write operation.

## Step 1 — Baseline

Run `git describe --tags --abbrev=0` to find the last release tag (`BASE_TAG`). If it returns nothing, stop and tell the user to tag the previous release first.

## Step 2 — Gather signals

In parallel:

- `git diff $BASE_TAG..HEAD -- banshee/` — CLI source changes (new groups, new subcommands, changed options/args, removed surface).
- `git diff $BASE_TAG..HEAD -- docs/reference/commands.md` — the hand-authored command reference. It is **read-only context for this skill** (never edit it), but it often carries detail that `--help` does not: per-field response tables, CSV column semantics, caveats ("reserved for future API support"), verbosity/criticality breakdowns, and worked examples. Read the changed sections in full and mine them for prose the KB pages should reflect.
- `git log $BASE_TAG..HEAD -- CHANGELOG.md` and read `CHANGELOG.md` itself for the new release's bullets. (If `CHANGELOG.md` does not exist, note that and rely on the diffs above.)
- Read the `version` field in `pyproject.toml` — this is the new release line. You'll need it for the Validation Snapshot.
- Run `banshee --help` to enumerate the live command groups.
- For every command group, run `banshee <group> --help` and `banshee <group> <sub> --help` for each subcommand. Capture the live option tables.

**Source precedence.** Live `--help` plus the output you observe in Step 4 is **authoritative** for which options/flags/args exist, their names, and response shape — KB pages must match it. `docs/reference/commands.md` is a **supplementary context source** for richer prose and field-level detail. When `commands.md` and live behavior disagree (e.g. a column documented as "always empty" that is actually populated), trust the live behavior, document that, and flag the discrepancy in the Step 7 summary so the reviewer can fix `commands.md` separately.

Use `banshee` install from the local .venv at the ROOT of the repo, if it is not present tell the user to install `ps-banshee` in the active environment, then stop.

## Step 3 — Categorize required updates

For each item:

| Detected change | Required updates |
|----|----|
| New command group `X` | Create `docs/knowledge-base/X.md` (use existing pages as template), add entry to `mkdocs.yml` plugin `sections.Commands` list, add a row to the cmd-group table in `docs/knowledge-base/index.md`, add a bullet to the use-case list in `docs/getting-started/llms.md` (see Step 6). |
| Removed command group `X` | Delete `docs/knowledge-base/X.md`, remove the corresponding entry from `mkdocs.yml`, drop the row from the cmd-group table, remove the corresponding bullet from `docs/getting-started/llms.md`. |
| New subcommand under existing group | Add a `### \`banshee <group> <sub>\`` section (same shape as existing sections). |
| Changed options/args on existing subcommand | Update the option table of that subcommand on the existing page. |
| Renamed subcommand | Update heading + every reference in the page body. |

## Step 4 — Run new/affected commands

For every new or changed command, run **2–3 representative permutations** to capture the real output shape and update the "Response shape" section on the matching KB page.

**Mutation rule:** Any command that creates, updates, deletes, adds, removes, clears, bulk-adds, or bulk-removes state is a mutation. Before running each mutation, **STOP** and ask the user with the exact command shown, e.g.:

> About to run a mutating command: `banshee list create banshee_refresh_test entity`. Proceed?

Only run after explicit user approval. Read-only commands (search, lookup, rules, fetch, stat, info, status, entries, --help) may be run without asking.

If `RF_TOKEN` is not set, warn and skip the runtime portion — the user can re-run after exporting it.

## Step 5 — Rewrite the Live Validation Snapshot

In `docs/knowledge-base/index.md`, replace the entire `## Live Validation Snapshot` section:

- Update the date to today's date (ISO).
- Update the version (`banshee X.Y.Z`) from `pyproject.toml`.
- Replace the validated-commands block with the actual commands you successfully ran in Step 4, grouped under the existing subheadings ("Local toolchain and auth presence", "Read-only API access", "Mutating workflows tested in a sandbox RF tenant", "Local-output workflows"). Use ASCII hyphens, not em dashes, in any new prose.

## Step 6 — Apply file edits

Edit files in place using the Edit tool. Allowed file scope:

- `docs/knowledge-base/*.md` (per-command pages + index)
- `mkdocs.yml` (only the `llmstxt-md` plugin's `sections:` block and `markdown_description`)
- `docs/getting-started/llms.md` (only the bullet list inside the `## Make \`banshee\` discoverable to your agent` section — see below)

**`docs/getting-started/llms.md` update rule:** When a new command group is added, append one bullet to the list inside the fenced markdown snippet in the "Make `banshee` discoverable to your agent" section. The bullet must be a plain English phrase describing the user-facing job the group performs (e.g. `- submitting files and URLs to sandbox for malware analysis and retrieving the resulting reports`). Match the existing phrasing style: lowercase, action-oriented, no implementation detail. When a command group is removed, delete its bullet. Do not touch any other part of the file.

**Do not touch:** `docs/reference/commands.md` (read-only context only), any other docs, source code, CHANGELOG, pyproject.toml, or any git state.

## Conventions to follow (must match existing files)

- H1 of each KB page is the bare command name: `# ca`, `# email`, etc.
- The first blockquote on each page is a short type-disambiguation line (when relevant), referencing sibling groups by name.
- The second blockquote is the literal: `> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.`
- Each subcommand section uses `### \`banshee <group> <sub>\`` followed by a one-sentence purpose line.
- Option tables use one of these two shapes:
  - `| Option | Short | Default | Description |` (for flag-rich commands)
  - `| Argument/Option | Description |` (for simple commands)
- Code examples are in `bash` fenced blocks. JSON shape sections use `| Field | Description |` tables.
- `mkdocs.yml` plugin entries follow `- knowledge-base/<group>.md: "Sentence-cased description ending with a period."` — ASCII only, no em dashes.

## Step 7 — Summary report

End with a concise summary:

- Pages updated / created / deleted
- New entries added to `mkdocs.yml`
- Commands run during validation (read-only count + mutations approved)
- Validation Snapshot date now set to: `<date>`
- Context pulled from `docs/reference/commands.md` (which sections informed the KB edits), plus any **discrepancies** found between `commands.md` and live `--help`/observed output — list these so the reviewer can correct `commands.md` separately.
- Anything you couldn't auto-derive (e.g. ambiguous response shape, behavioral changes that need a human call) — list these so the reviewer knows what to inspect manually

Then stop. The user reviews the diff in their IDE and commits.
