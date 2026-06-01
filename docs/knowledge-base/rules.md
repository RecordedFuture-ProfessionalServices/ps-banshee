# rules

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee rules search`

Search and download Sigma, YARA, and Snort detection rules from Recorded Future.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--type` | `-t` | | Rule type (repeatable, OR logic): `sigma`, `yara`, `snort` |
| `--threat-actor-map` | `-T` | | Filter by actors in your Threat Actor Map |
| `--threat-actor-category` | `-C` | | Filter by threat actor category (repeatable, OR logic). Categories include nation-state groups, ransomware groups, hacktivists, financially motivated actors, and more. |
| `--threat-malware-map` | `-M` | | Filter by malware in your Malware Threat Map |
| `--org-id TEXT` | `-O` | | Organization ID for MSSP/multi-org accounts (for use with threat maps) |
| `--entity TEXT` | `-e` | | Filter by RF entity ID (repeatable, OR logic). Use `banshee entity search` to find IDs. MITRE codes accepted (e.g. `mitre:T1486`). |
| `--created-after TEXT` | `-a` | | Relative (`1d`, `7d`) or absolute (`2024-01-01`) |
| `--created-before TEXT` | `-b` | | Relative or absolute date |
| `--updated-after TEXT` | `-u` | | Relative or absolute date |
| `--updated-before TEXT` | `-U` | | Relative or absolute date |
| `--id TEXT` | `-i` | | Filter by Insikt Note document ID (e.g. `doc:lmRPGB`) |
| `--title TEXT` | `-n` | | Freetext search on associated Insikt Note titles |
| `--limit INTEGER` | `-l` | `10` | Max results (1–1000) |
| `--output-path TEXT` | `-o` | | Save rules to directory (omit to print to console) |
| `--pretty` | `-p` | | Pretty print |

```bash
banshee rules search -t yara -t snort -l 20 -a 3d
banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE
banshee rules search --id doc:0uTafk
banshee rules search --title Ransomware -p
banshee rules search -t yara --output-path .
banshee rules search --threat-actor-map -o fetched_rules
```

**Response shape:** Returns a flat JSON array (when not using `--output-path`). Each item represents an Insikt Note with associated detection rules:

| Field | Description |
|-------|-------------|
| `.id` | Insikt Note document ID (e.g. `doc:o6_lui`) |
| `.type` | Rule type: `sigma`, `yara`, or `snort` |
| `.title` | Insikt Note title |
| `.description` | Full Insikt Note description text |
| `.created` | Note creation timestamp (ISO 8601) |
| `.updated` | Note last updated timestamp (ISO 8601) |
| `.rules[]` | Array of rule objects — one note may have multiple rules |

`.rules[]` item fields:

| Field | Description |
|-------|-------------|
| `.content` | Raw rule text (YAML for Sigma, plain text for YARA/Snort) |
| `.file_name` | Suggested filename for saving the rule |
| `.entities[]` | Entities referenced by the rule: `{id, name, type}` (may include `display_name`) |

```bash
# List all sigma rule titles and filenames from the last 7 days
banshee rules search -t sigma -l 50 -a 7d | jq '[.[] | {title, file: .rules[0].file_name}]'

# Extract all MITRE ATT&CK IDs referenced by rules
banshee rules search -t sigma -l 20 | jq '[.[].rules[].entities[] | select(.type == "MitreAttackIdentifier") | .name] | unique'

# Print raw Sigma rule content
banshee rules search --id doc:0uTafk | jq -r '.[0].rules[0].content'
```
