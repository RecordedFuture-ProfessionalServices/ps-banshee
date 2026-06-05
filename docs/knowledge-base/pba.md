# pba

> **Playbook Alerts** - automation-driven alerts. IDs are 36-char UUIDs and the `task:` prefix is optional (e.g. `d144a9ec-90e6-40fe-89b0-d85ed65d3e9c` or `task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c`). PBA-exclusive categories: `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report`. For legacy rule-based alerts (short opaque IDs), use [`ca`](ca.md) instead.
>
> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee pba search`

Search Playbook Alerts with rich filter options.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--created TEXT` | `-C` | | Filter by created date (e.g. `1d`, `7d`) |
| `--updated TEXT` | `-u` | | Filter by updated date |
| `--category` | `-c` | all | One or more categories (repeatable): `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report` |
| `--entity TEXT` | `-e` | | Filter by associated entity (repeatable) |
| `--priority` | `-P` | all | `Informational`, `Moderate`, `High` (repeatable) |
| `--status` | `-s` | all | `New`, `InProgress`, `Dismissed`, `Resolved` (repeatable) |
| `--org-id TEXT` | `-o` | all | Filter by owning organisation ID (repeatable). Accepts a 10-char ID or a 16-char `uhash:` form |
| `--limit INTEGER` | `-l` | `100` | Max results (1–10000) |
| `--pretty` | `-p` | | Pretty print |

**Response shape:** Returns a JSON object with three top-level keys: `.data` (array of alert records), `.counts` (`{returned, total}`), and `.status` (request status string). Alert records are under `.data[]` with fields: `playbook_alert_id`, `category`, `priority`, `status`, `title`, `created`, `updated`, `actions_taken`, `owner_organisation_details`.

```bash
banshee pba search --created 1d
banshee pba search -C 1d -u 1d -p
banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse
banshee pba search --updated 7d --category domain_abuse --pretty
banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New
banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d
banshee pba search -o 69sKLfTGsS -o uhash:5zQaSyRpA1 -C 7d -P High
```

---

### `banshee pba lookup ALERT_ID`

Retrieve a single Playbook Alert by ID. Accepts a 36-char UUID with or without the `task:` prefix — the CLI auto-prepends `task:` to bare UUIDs.

```bash
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p
```

**Response shape:** Returns a single JSON object with four top-level keys: `playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`.

**`.panel_status`** — alert metadata and current disposition:

| Field | Description |
|-------|-------------|
| `.panel_status.status` | Current status: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `.panel_status.priority` | Priority: `Informational`, `Moderate`, `High` |
| `.panel_status.case_rule_label` | Human-readable rule name (e.g. `"Data Leakage on Code Repository"`) |
| `.panel_status.entity_id` | RF entity ID of the primary subject (e.g. `"url:https://..."`) |
| `.panel_status.entity_name` | Primary entity name |
| `.panel_status.risk_score` | RF risk score integer |
| `.panel_status.targets[]` | Array of `{name}` objects — entities targeted or affected |
| `.panel_status.actions_taken[]` | Actions already recorded on the alert |
| `.panel_status.created` | Creation timestamp (ISO 8601) |
| `.panel_status.updated` | Last updated timestamp (ISO 8601) |

**`.panel_evidence_summary`** — evidence detail; structure varies by alert category. For `code_repo_leakage`:

| Field | Description |
|-------|-------------|
| `.panel_evidence_summary.repository.name` | Repository URL |
| `.panel_evidence_summary.repository.owner.name` | Repository owner login |
| `.panel_evidence_summary.evidence[]` | Array of evidence items |
| `.panel_evidence_summary.evidence[].url` | Source URL of the exposed content |
| `.panel_evidence_summary.evidence[].content` | Snippet of the exposed content |
| `.panel_evidence_summary.evidence[].assessments[]` | Assessment objects: `{id, title, value}` |
| `.panel_evidence_summary.evidence[].targets[]` | Target entities: `{name}` |
| `.panel_evidence_summary.evidence[].published` | Publication timestamp |

```bash
# Summary: entity, rule, status
banshee pba lookup task:<ID> | jq '{entity: .panel_status.entity_name, rule: .panel_status.case_rule_label, status: .panel_status.status, priority: .panel_status.priority}'

# Extract evidence URLs (code_repo_leakage)
banshee pba lookup task:<ID> | jq '[.panel_evidence_summary.evidence[].url]'
```

---

### `banshee pba update [ALERT_IDS]...`

Update one or more Playbook Alerts. IDs accept `task:` prefix or bare UUID. Can be piped.

| Option | Short | Description |
|--------|-------|-------------|
| `--status` | `-s` | New status: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `--reopen` | `-r` | Reopen strategy (for Dismissed/Resolved only): `Never`, `SignificantUpdates` |
| `--priority` | `-p` | New priority: `Informational`, `Moderate`, `High` |
| `--comment TEXT` | `-t` | Add a comment |
| `--assignee TEXT` | `-a` | Reassign (accepts `uhash:3aXZxdkM12`) |

**Valid status/reopen combinations:** `Dismissed → Never`, `Resolved → Never`, `Resolved → SignificantUpdates`

```bash
# Single update
banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

# Multiple IDs
banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

# Pipe from search
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

# From file
banshee pba update -s Dismissed < alerts.txt
cat alerts.txt | banshee pba update -s Dismissed

# Full example
banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
```

**Response:** Returns plain text, not JSON — one line per updated alert: `SUCCESS:\n<ALERT_ID>`. Do not pipe to `jq`.

---

### `banshee pba export`

Fetch full alert details for the alerts produced by `pba search` and emit them as JSON or CSV. Input is **stdin only** — pipe the JSON object from `banshee pba search`; there are no positional arguments.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--csv` | | JSON | Output as CSV (fixed column set) instead of JSON (full alert details). |

```bash
banshee pba search --created 1d -l 10 | banshee pba export > alerts.json
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export --csv > identity_alerts.csv
```

**Input:** Expects the JSON object emitted by `banshee pba search` on stdin — the export reads `.data[]` and requires `playbook_alert_id` and `category` on each record (these drive the category-specific fetch). Running with no piped input (a TTY) raises a `BadParameter` error.

**Response shape (default):** A JSON array of full Playbook Alert objects — the same per-alert structure returned by `banshee pba lookup` (`playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`).

**Response shape (`--csv`):** CSV with a header row and these fixed columns: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Subject`, `Assignee`, `Assessments`, `Entities`, `Reopen Strategy`, `Onwards Actions`. `Assessments` and `Entities` are `; `-joined; commas inside field values are replaced with spaces.
