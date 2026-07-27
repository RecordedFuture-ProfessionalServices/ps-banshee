# risklist

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee risklist fetch`

Download a risk list from RF or load a local custom file.

| Option | Short | Description |
|--------|-------|-------------|
| `--entity-type` | `-e` | Entity type: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--list-name TEXT` | `-l` | `default`, `large`, or any rule name from `banshee ioc rules` |
| `--custom-list-path TEXT` | `-c` | Path to a local risk list file |
| `--output-path TEXT` | `-o` | Output path (defaults to CWD with auto-generated name) |
| `--as-json` | `-j` | Convert downloaded list to JSON (only with `--list-name` + `--entity-type`) |

```bash
banshee risklist fetch -e domain -l default
banshee risklist fetch -c /custom/path/to/list.csv
banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv
```

---

### `banshee risklist create`

Build a custom merged risk list from one or more risk rules, with optional score filtering. Can write locally or upload to RF Fusion.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--entity-type` | `-e` | | Entity type: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--risk-rule TEXT` | `-R` | | Risk rule to include (repeatable): `default`, `large`, or any rule name from `banshee ioc rules` |
| `--risk-score INTEGER` | `-r` | | Minimum risk score threshold (5–99) |
| `--format` | `-f` | `csv` | Output format: `csv`, `edl`, `json` |
| `--output-path TEXT` | `-o` | CWD | Output file path |
| `--fusion` | `-F` | | Upload to RF Fusion (use with `--output-path` as Fusion destination path) |

**Output formats:**
- `csv` — Comma-separated with headers: `Name, Risk, RiskString, EvidenceDetails`
- `edl` — Plain list of IOC values, one per line (for firewall/EDL feeds)
- `json` — Full JSON array of risk list entries

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

---

### `banshee risklist stat`

Show metadata for a risk list — whether it exists in Fusion and its current etag.

| Option | Short | Description |
|--------|-------|-------------|
| `--entity-type` | `-e` | Entity type |
| `--list-name TEXT` | `-l` | List name |
| `--custom-list-path TEXT` | `-c` | Path to local risk list file |
| `--pretty` | `-p` | Pretty print |
| `--count` | `-C` | Show IOC counts and risk score distribution across the risk list |

```bash
banshee risklist stat -e ip -l recentValidatedCnc
banshee risklist stat -e domain -l domain_risklist
banshee risklist stat -e ip -l default --count
```

**Response shape:** Returns a single JSON object:

| Field | Description |
|-------|-------------|
| `.name` | Risk list name as stored in Fusion (e.g. `"recentValidatedCnc_ip_risklist"`) |
| `.exists` | `true`/`false` — whether the list exists in RF Fusion |
| `.etag` | Etag hash string for cache validation |
| `.counts` | *(only with `--count`)* Object mapping each risk score to its IOC count, e.g. `{"28": 261110, "65": 6531}` |

**Live-test note:** During 2026-05-01 testing, `--custom-list-path /tmp/banshee_smoke_risklist.json` attempted a Fusion API lookup and returned `400 Bad Request`; prefer `-e`/`-l` unless validating a known Fusion-backed custom path.
