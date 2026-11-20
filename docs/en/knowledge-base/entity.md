# entity

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee entity lookup ENTITY_ID`

Look up a Recorded Future entity by its ID.

| Argument/Option | Description |
|-----------------|-------------|
| `ENTITY_ID` (required) | RF entity ID, e.g. `qf0H03` |
| `--pretty` / `-p` | Pretty print |

```bash
banshee entity lookup qf0H03
banshee entity lookup qf0H03 -p
```

**Response shape:** Returns a single JSON object with top-level keys `id`, `type`, and `attributes`. The entity name is nested under `.attributes.name`, not at the top level.

```bash
# Correct jq to extract id, type, and name:
banshee entity lookup qf0H03 | jq '{id, type, name: .attributes.name}'
```

---

### `banshee entity search NAME`

Search entities by name, optionally filtered by type.

| Argument/Option | Short | Default | Description |
|-----------------|-------|---------|-------------|
| `NAME` (required) | | | Entity name to search |
| `--type` | `-t` | | One or more entity types (repeatable). See full type list below. |
| `--limit INTEGER` | `-l` | `100` | Max results (1–100) |
| `--pretty` | `-p` | | Pretty print |

**Common entity types (partial list):** `Malware`, `IpAddress`, `InternetDomainName`, `URL`, `Hash`, `CyberVulnerability`, `CyberThreatActorCategory`, `Organization`, `Person`, `Country`, `MitreAttackIdentifier`, `YaraDetectionRule`, `SnortDetectionRule`, `SigmaDetectionRule` (plus 100+ more).

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**Response shape:** Returns a flat JSON array. Each item has exactly three fields:

| Field | Description |
|-------|-------------|
| `.id` | RF entity ID (e.g. `SoA6SP`) |
| `.name` | Entity display name |
| `.type` | Entity type string (e.g. `Malware`, `InternetDomainName`) |

```bash
# Extract all IDs matching a name
banshee entity search "Cobalt Strike" -t Malware | jq -r '.[].id'

# Build a lookup table of id → name
banshee entity search wannacry | jq '[.[] | {(.id): .name}] | add'
```


---

### `banshee entity links ENTITY_ID...`

Fetch entities linked to one or more entities (IOCs, detection rules, malware, TTPs, threat actors). Entity IDs are Recorded Future entity IDs (e.g. from `banshee entity search`), not entity names. Linked IOCs are enriched via SOAR unless `--skip-enrichment` is set.

Entity IDs can be passed as whitespace-separated arguments, or piped / redirected on stdin (one per line). Do not add a subcommand word (e.g. `links search`): there is none, and any extra word is treated as an entity ID.

| Argument/Option | Short | Default | Description |
|-----------------|-------|---------|-------------|
| `ENTITY_ID...` | | stdin | One or more entity IDs |
| `--type TEXT` | `-t` | | Type of entity to return. Repeatable |
| `--source [Technical\|Insikt]` | `-s` | | Source of the links to return |
| `--sections TEXT` | `-S` | | Filter by link type, e.g. `'Indicators and Detection Rules'`. Repeatable |
| `--timeframe TEXT` | `-T` | | Timeframe the link was made in, e.g. `-1d` (max `-90d`) |
| `--events TEXT` | `-e` | | Filter by event type, e.g. `type:MalwareAnalysis`. Repeatable |
| `--connected-entities TEXT` | `-c` | | Only return entities also connected to these entities. Repeatable |
| `--limit INTEGER` | `-l` | | Max entities returned per type (1–1,000,000) |
| `--small` | | | Search 10 references and 10 Insikt Notes per event type |
| `--large` | | | Search 100 references and 500 Insikt Notes per event type |
| `--skip-enrichment` | | | Skip additional enrichment of linked IOCs |
| `--pretty` | `-p` | | Pretty print |

`--small` and `--large` are mutually exclusive; with neither, a medium scope is used.

**Response shape:** Returns a JSON array with one object per input entity. Each object contains the searched `entity` and its `links`. Each link carries an `enrichment` field holding the SOAR enrichment for linked IOCs, or `null` for non-IOC links, unenriched IOCs, or when `--skip-enrichment` is used. If SOAR enrichment fails, a note is printed to stderr and enrichment is skipped.

Pretty output (printed to stderr) shows per-entity tables of linked IOCs (with risk score, top risk rule and intelligence card link), TTPs, malware and threat actors, each capped at 20 rows. IOC enrichment in pretty mode is likewise limited to 20 IOCs per type.

```bash
banshee entity links BUl6R5r
banshee entity links BUl6R5r -T -10d --small -p
banshee entity links BUl6R5r sIG7Rn -T -10d --large > links.json

# Skip enrichment for faster results
banshee entity links BUl6R5r --skip-enrichment

# Entity IDs from a file or pipe
banshee entity links -T -1d < link_entities.txt
cat link_entities.txt | banshee entity links -T -1d --large > links_out.json

# Find an entity ID first, then search its links
banshee entity search wannacry -t Malware -l 1 | jq -r '.[].id' | banshee entity links --small
```
