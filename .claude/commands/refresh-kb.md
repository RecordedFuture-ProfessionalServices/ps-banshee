---
description: Refresh the LLM knowledge base from CLI changes since the last release tag. Run at the end of every release; review the diff in your IDE before committing.
---

You are refreshing `docs/knowledge-base/` and the related `mkdocs.yml` plugin sections so they reflect the current state of the `banshee` CLI. This command is invoked at the end of every release. The user reviews your edits in their IDE and commits them — you must **not** run any git write operation.

## Step 1 — Baseline

Run `git describe --tags --abbrev=0` to find the last release tag (`BASE_TAG`). If it returns nothing, stop and tell the user to tag the previous release first.

## Step 2 — Gather signals

In parallel:

- `git diff $BASE_TAG..HEAD -- banshee/` — CLI source changes (new groups, new subcommands, changed options/args, removed surface).
- `git log $BASE_TAG..HEAD -- CHANGELOG.md` and read `CHANGELOG.md` itself for the new release's bullets.
- Read the `version` field in `pyproject.toml` — this is the new release line. You'll need it for the Validation Snapshot.
- Run `banshee --help` to enumerate the live command groups.
- For every command group, run `banshee <group> --help` and `banshee <group> <sub> --help` for each subcommand. Capture the live option tables. This is the **authoritative source** for option/flag documentation — KB pages must match.

If `banshee` is not on PATH, tell the user to install `ps-banshee` in the active environment, then stop.

## Step 3 — Categorize required updates

For each item:

| Detected change | Required updates |
|----|----|
| New command group `X` | Create `docs/knowledge-base/X.md` (use existing pages as template), add entry to `mkdocs.yml` plugin `sections.Commands` list, add a row to the cmd-group table in `docs/knowledge-base/index.md`. |
| Removed command group `X` | Delete `docs/knowledge-base/X.md`, remove the corresponding entry from `mkdocs.yml`, drop the row from the cmd-group table. |
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

**Do not touch:** `docs/getting-started/llms.md`, any other docs, source code, CHANGELOG, pyproject.toml, or any git state.

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
- Anything you couldn't auto-derive (e.g. ambiguous response shape, behavioral changes that need a human call) — list these so the reviewer knows what to inspect manually

Then stop. The user reviews the diff in their IDE and commits.
