# ioc

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee ioc lookup ENTITY_TYPE [IOC]...`

Rich, per-IOC enrichment. One API call per indicator. Use for deep context.

**Entity types:** `ip`, `domain`, `url`, `hash`, `vulnerability`

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbosity INTEGER` | `-v` | `1` | Detail level 1–5 (see verbosity table below) |
| `--ai-insights` | `-a` | | Include AI-generated summaries of risk rules |
| `--pretty` | `-p` | | Pretty print |

**Verbosity levels by entity type:**

| Level | ip | domain | hash | url | vulnerability |
|-------|----|--------|------|-----|---------------|
| 1 | entity, risk, timestamps | entity, risk, timestamps | entity, hashAlgorithm, risk, timestamps | entity, risk, timestamps | entity, lifecycleStage, risk, timestamps |
| 2 | + intelCard, location | + intelCard | + fileHashes, intelCard | + intelCard | + intelCard |
| 3 | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links |
| 4 | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings | + cvss, cvssv3, cvssv4, enterpriseLists, riskMapping, sightings, threatLists |
| 5 | + dnsPortCert, scanner | same as 4 | same as 4 | same as 4 | + cpe, cpe22uri, nvdDescription, nvdReferences |

```bash
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p

# Pipe from CSV file
cat test_ips.csv | banshee ioc lookup ip -p
```

**Response shape (verbosity 1):** Returns a JSON array. Each item has `entity`, `risk`, `timestamps`. Higher verbosity levels add: v2 `+intelCard, location`; v3 `+analystNotes, links`; v4 `+enterpriseLists, riskMapping, sightings, threatLists`; v5 `+dnsPortCert, scanner` (ip only).

`.risk.evidenceDetails[]` item fields:

| Field | Description |
|-------|-------------|
| `.rule` | Rule name string |
| `.criticality` | Integer 0–4 (0–5 for vulnerabilities) |
| `.criticalityLabel` | Human-readable label (e.g. `"Unusual"`, `"Malicious"`) |
| `.evidenceString` | Human-readable evidence description |
| `.mitigationString` | Mitigation guidance (may be empty string) |
| `.timestamp` | Most recent evidence timestamp (ISO 8601) |

**Advanced jq recipes:**

```bash
# Most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'

# All triggered rules
banshee ioc lookup ip 1.2.3.4 | jq '.[].risk.evidenceDetails[].rule'

# Risk score + most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | { score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] } ]'

# Risk score + all rules with criticality labels
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | { score: .risk.score, rules: [.risk.evidenceDetails[] | {rule, label: .criticalityLabel}] } ]'
```

---

### `banshee ioc bulk-lookup ENTITY_TYPE [IOC]...`

Fast bulk enrichment — batches up to 1000 IOCs per API call. Returns risk score and triggered risk rules only. Use for high-volume triage.

| Option | Description |
|--------|-------------|
| `--pretty` / `-p` | Pretty print |

**Response shape:** Returns a JSON array. Each item has `entity` (`id`, `name`, `type`) and `risk`. Note: no `timestamps` key (unlike `ioc lookup`).

`.risk` fields:

| Field | Description |
|-------|-------------|
| `.risk.score` | Integer risk score 0–99 |
| `.risk.level` | Integer criticality level |
| `.risk.context` | Context object grouped by risk domain (`phishing`, `public`, `c2`, `malware`) |
| `.risk.rule.count` | Number of triggered rules |
| `.risk.rule.maxCount` | Max possible rules |
| `.risk.rule.mostCritical` | Most critical rule name |
| `.risk.rule.summary` | Array of summary strings |
| `.risk.rule.evidence[]` | Array of triggered rule objects |

`.risk.rule.evidence[]` item fields:

| Field | Description |
|-------|-------------|
| `.rule` | Rule name string |
| `.level` | Integer criticality 0–4 |
| `.description` | HTML-tagged evidence string (entity refs use `<e id=...>` markup) |
| `.count` | Hit count |
| `.sightings` | Sighting count |
| `.timestamp` | Most recent evidence timestamp (ISO 8601) |
| `.mitigation` | Mitigation guidance (may be empty string) |
| `.type` | Rule type string (e.g. `linkedIntrusion`) |

Bulk risk rule evidence is under `.risk.rule.evidence[]`; this differs from `ioc lookup`, which uses `.risk.evidenceDetails[]`.

```bash
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877

# From file (one IOC per line)
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability

# Extract names and scores
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

# Extract names, scores, and triggered rule names
banshee ioc bulk-lookup ip 92.38.178.133 | jq '[.[] | {ioc: .entity.name, score: .risk.score, rules: [(.risk.rule.evidence // [])[].rule]}]'
```

---

### `banshee ioc search ENTITY_TYPE`

Search the RF IOC corpus with filters.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--limit INTEGER` | `-l` | `5` | Max results (1–1000) |
| `--risk-score TEXT` | `-r` | | Risk score range (interval notation) |
| `--risk-rule TEXT` | `-R` | | Filter by risk rule name |
| `--verbosity INTEGER` | `-v` | `1` | Detail level 1–5 (same table as `ioc lookup`) |
| `--pretty` | `-p` | | Pretty print |

**Risk score interval notation:**

| Syntax | Meaning |
|--------|---------|
| `'[20,90]'` | 20 ≤ score ≤ 90 |
| `'(20,90)'` | 20 < score < 90 |
| `'[20,90)'` | 20 ≤ score < 90 |
| `'[20,)'` | score ≥ 20 |
| `'[,90)'` | score < 90 |

Default JSON output is an object. Search results are under `.data.results[]`, and total/returned counts are under `.counts`.

```bash
banshee ioc search ip -l 10 -r '(,80]'
banshee ioc search domain -r '[90,)'
banshee ioc search hash -r '[80,81]' -p
banshee ioc search vulnerability --limit 1 -v 3

# Extract IOC names from search results
banshee ioc search ip -r '[90,)' -l 100 | jq -r '.data.results[].entity.name'
```

---

### `banshee ioc rules ENTITY_TYPE`

List risk rules for an entity type, with optional filters.

| Option | Short | Description |
|--------|-------|-------------|
| `--freetext TEXT` | `-F` | Filter rules by name/description |
| `--mitre-code TEXT` | `-M` | Filter by MITRE ATT&CK code (e.g. `T1587.004`) |
| `--criticality INTEGER` | `-C` | Filter by criticality 0–5 |
| `--pretty` | `-p` | Pretty print |

**Criticality reference (IP, Domain, URL, Hash):**

| Level | Label | Risk Score Band |
|-------|-------|----------------|
| 4 | Very Malicious | 90–99 |
| 3 | Malicious | 65–89 |
| 2 | Suspicious | 25–64 |
| 1 | Unusual | 5–24 |
| 0 | No evidence of risk | 0 |

**Criticality reference (Vulnerability):**

| Level | Label | Risk Score Band |
|-------|-------|----------------|
| 5 | Very Critical | 90–99 |
| 4 | Critical | 80–89 |
| 3 | High | 65–79 |
| 2 | Medium | 25–64 |
| 1 | Low | 5–24 |
| 0 | No evidence of risk | 0 |

```bash
banshee ioc rules ip
banshee ioc rules domain -p
banshee ioc rules hash -C 3
banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept
```

**Response shape:** Returns a flat JSON array. Each item represents one risk rule:

| Field | Description |
|-------|-------------|
| `.name` | Rule name string — use this value with `--risk-rule` in `ioc search` and `risklist` commands (e.g. `"recentActiveCnc"`) |
| `.criticalityLabel` | Human-readable label (e.g. `"Very Malicious"`) |
| `.criticality` | Integer criticality level |
| `.description` | Rule description string |
| `.categories[]` | Array of `{name, framework}` objects — MITRE ATT&CK categories (e.g. `{name: "TA0011", framework: "MITRE"}`) |
| `.relatedEntities[]` | Array of RF entity ID strings referenced by this rule |
| `.count` | Number of IOCs currently matching this rule |

```bash
# List all rule names for an entity type
banshee ioc rules ip | jq -r '.[].name'

# Find rules above criticality 3 with their descriptions
banshee ioc rules ip | jq '[.[] | select(.criticality >= 3) | {name, criticalityLabel, description}]'
```
