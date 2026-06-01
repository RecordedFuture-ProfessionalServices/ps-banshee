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
