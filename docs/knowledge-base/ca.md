# ca

> **Classic Alerts** - legacy rule-based alerts. IDs are short opaque strings of 6+ chars (e.g. `tybakN`). For automation/playbook-driven alerts (36-char UUID IDs with optional `task:` prefix, categories like `domain_abuse` / `third_party_risk` / etc.), use [`pba`](pba.md) instead.
>
> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee ca lookup ALERT_ID`

Retrieve a single Classic Alert by ID.

| Argument/Option | Description |
|-----------------|-------------|
| `ALERT_ID` (required) | Alert ID, e.g. `tybakN` |
| `--pretty` / `-p` | Pretty print |

```bash
banshee ca lookup tybakN
banshee ca lookup tybakN -p
```

**Response shape:** Returns a single JSON object.

| Field | Description |
|-------|-------------|
| `.id` | Alert ID |
| `.title` | Alert title |
| `.type` | Alert type string (e.g. `"EVENT"`) |
| `.log.triggered` | Trigger timestamp (ISO 8601) |
| `.review.status_in_portal` | Human-readable status: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.assignee` | Assigned analyst email |
| `.rule.id` | Alert rule ID |
| `.rule.name` | Alert rule name |
| `.url.portal` | Direct link to alert in RF portal |
| `.ai_insights.text` | RF AI-generated summary string |
| `.hits[]` | Documents that triggered the alert |
| `.hits[].id` | Hit document ID |
| `.hits[].fragment` | Text snippet that matched |
| `.hits[].language` | Language code (e.g. `"eng"`) |
| `.hits[].entities[]` | Entities found in the hit: `{id, name, type}` |
| `.hits[].document.title` | Source document title |
| `.hits[].document.url` | Source document URL |
| `.hits[].document.source` | Source name string |
| `.hits[].document.authors` | Array of author strings (may be empty) |
| `.triggered_by[]` | Entities/rules that triggered the alert (may be empty) |
| `.triggered_by[].reference_id` | Reference document ID |
| `.triggered_by[].triggered_by_strings[]` | Human-readable trigger descriptions |
| `.enriched_entities[]` | Pre-enriched entity objects with RF context (may be empty) |

```bash
# Extract all entities from alert hits for enrichment
banshee ca lookup tybakN | jq '[.hits[].entities[] | {id, name, type}] | unique_by(.id)'

# Get the AI summary
banshee ca lookup tybakN | jq -r '.ai_insights.text'

# Get portal link
banshee ca lookup tybakN | jq -r '.url.portal'
```

---

### `banshee ca search`

Search Classic Alerts with optional filters.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--triggered TEXT` | `-t` | `1d` | Time range. Relative (`1d`, `12h`) or absolute interval (`[2024-08-01, 2024-08-14]`). |
| `--rule TEXT` | `-r` | | Filter by alert rule name (freetext, repeatable). |
| `--status` | `-s` | | One of: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--pretty` | `-p` | | Pretty print |

```bash
banshee ca search -t 1d
banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending
banshee ca search -t 12h -p
banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d
banshee ca search -r leaked -t 12h -p
```

**Response shape:** Returns a JSON array. Each alert object has the following top-level fields:

| Field | Description |
|-------|-------------|
| `.id` | Alert ID (e.g. `tybakN`) |
| `.title` | Alert title |
| `.log.triggered` | Trigger timestamp (ISO 8601) |
| `.review.status_in_portal` | Human-readable status: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.status` | Internal status string (`no-action`, etc.) — not useful for jq filtering |
| `.rule.name` | Name of the alert rule that fired |
| `.rule.id` | Alert rule ID |

**Note:** There is no top-level `priority` field on `ca search` alert records. Use `.review.status_in_portal` (not `.review.status`) when filtering by status in jq pipelines.

```bash
# Extract IDs of New alerts (use status_in_portal for jq filtering)
banshee ca search -t 1d | jq -r '.[] | select(.review.status_in_portal == "New") | .id'

# When using the -s flag, status filtering happens server-side — no jq select needed
banshee ca search -t 1d -s New | jq -r '.[].id'
```

---

### `banshee ca rules [FREETEXT]`

List all Classic Alert rules, optionally filtered by freetext.

| Argument/Option | Description |
|-----------------|-------------|
| `FREETEXT` (optional) | Search term to filter rule names |
| `--pretty` / `-p` | Pretty print |

```bash
banshee ca rules
banshee ca rules -p
```

**Response shape:** Returns a flat JSON array. Each item has the following fields:

| Field | Description |
|-------|-------------|
| `.id` | Rule ID (e.g. `k_TnPe`) |
| `.title` | Rule name |
| `.enabled` | `true`/`false` — whether the rule is active |
| `.priority` | `true` = alerts from this rule are severity **High**; `false` = severity **Informational**. To triage by priority, fetch rules first and join to alerts via `.rule.id` (see Priority triage workflow below). |
| `.tags` | Array of tag strings |
| `.created` | Creation timestamp (ISO 8601) |
| `.owner` | Object with `id` and `name` — rule owner |
| `.intelligence_goals` | Array of `{id, name}` objects — associated intelligence goals |
| `.notification_settings` | Object with `email_subscribers` array |

Use `.title` and `.id` when constructing pipelines. `.priority` maps directly to alert severity: `true` is High, `false` is Informational.

---

### Priority triage workflow

`ca search` and `ca lookup` do not return a per-alert severity field. To triage alerts by severity, fetch the rules list first, filter to rules where `.priority == true`, and intersect against alert `.rule.id` values:

```bash
# High-priority alert IDs in the last day
PRIORITY_RULES=$(banshee ca rules | jq -r '.[] | select(.priority == true) | .id' | paste -sd'|' -)
banshee ca search -t 1d | jq --arg rules "$PRIORITY_RULES" -r '.[] | select(.rule.id | test("^(" + $rules + ")$")) | .id'
```

Pipe the resulting IDs straight into `banshee ca update` to status-change only the high-priority alerts.

---

### `banshee ca update [ALERT_IDS]...`

Update one or more Classic Alerts. IDs can be passed as arguments, space-separated, or piped via stdin.

| Option | Short | Description |
|--------|-------|-------------|
| `--status` | `-s` | New status: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--note TEXT` | `-n` | Add a text note |
| `--append` | `-A` | Append to existing note instead of overwriting |
| `--assignee TEXT` | `-a` | Reassign alert. Accepts `uhash:3aXZxdkM12` or `analyst@acme.com` |

**Input methods:**

```bash
# Single ID
banshee ca update 8cORlQ -s Resolved

# Multiple IDs (space-separated)
banshee ca update 8cORlQ 8biCIG -s Pending

# Pipe IDs from file
cat alerts.txt | banshee ca update -s Dismissed

# Pipe from search via jq
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"

# stdin redirect
banshee ca update -s Dismissed < alerts.txt
```

**Response:** Returns plain text, not JSON — one line per updated alert: `SUCCESS:\n<ALERT_ID>`. Do not pipe to `jq`.

---

### `banshee ca export`

Fetch full alert details for the alerts produced by `ca search` and emit them as JSON or CSV. Input is **stdin only** — pipe the JSON array from `banshee ca search`; there are no positional arguments.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--csv` | | JSON | Output as CSV (fixed column set) instead of JSON (full alert details). |

```bash
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s Pending | banshee ca export --csv > alerts.csv
```

**Input:** Expects the JSON array emitted by `banshee ca search` on stdin; every element must have an `id`. Running with no piped input (a TTY) raises a `BadParameter` error.

**Response shape (default):** A JSON array of full alert objects — the same per-alert structure returned by `banshee ca lookup` (`.id`, `.title`, `.log.triggered`, `.review`, `.rule`, `.hits[]`, etc.).

**Response shape (`--csv`):** CSV with a header row and these fixed columns: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Title`, `Assignee`, `URL`, `Entities`, `Recorded Future AI Insights`. `Priority` is derived from the alert rule (`High` when the rule is a priority rule, otherwise `Informational`); commas inside field values are replaced with spaces.
