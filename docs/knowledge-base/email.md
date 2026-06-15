# email

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee email enrich FILE_PATH`

Parse an EML file, extract IPs from headers, URLs/domains from the body, and attachment hashes, then enrich the indicators with RF threat intelligence. By default, only shows indicators above the risk score threshold (65).

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | Show only indicators above this score (0–99) |
| `--threat-hunt` | `-t` | `false` | Also include indicators linked to threat actors even if below the score threshold |
| `--pretty` | `-p` | | Pretty print |

Default JSON output is a flat array of records with fields such as `ioc`, `type`, `location`, `risk_score`, `first_seen`, `last_seen`, `rule_evidence`, `analyst_notes`, `malwares`, `count_of_analyst_notes`, and `ta_names`.

```bash
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p

# Extract the highest-risk indicators from an enriched EML
banshee email enrich phishing_email.eml -r 1 | jq '[.[] | {ioc, type, location, score: .risk_score, top_rule: (.rule_evidence[0].rule // "")}] | sort_by(-.score)'
```
