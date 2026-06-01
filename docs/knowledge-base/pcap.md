# pcap

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

> **Prerequisite:** `tshark` must be installed and in `PATH`. In Banshee 1.2.0, `banshee pcap enrich --help` also fails if `tshark` is missing, so verify with `command -v tshark` first.

### `banshee pcap enrich FILE_PATH`

Parse a pcap file, extract IPs and domains, enrich with RF threat intelligence. By default, only shows indicators above the risk score threshold (65).

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | Show only indicators above this score (1–99) |
| `--threat-hunt` | `-t` | `false` | Also include indicators linked to threat actors even if below the score threshold (retrospective threat hunting) |
| `--pretty` | `-p` | | Pretty print |

Default JSON output is a flat array of records with fields such as `ioc`, `risk_score`, `most_malicious_rule`, `rule_evidence`, `ta_names`, `malwares`, and `wireshark_query`.

```bash
banshee pcap enrich sandbox.pcap
banshee pcap enrich honeypot-traffic.pcap -r 25 -t -p

# Summarize hits from JSON output
banshee pcap enrich sandbox.pcap -r 25 -t | jq '[.[] | {indicator: .ioc, score: .risk_score, top_rule: .most_malicious_rule, evidence_rules: [(.rule_evidence // [])[].rule]}] | sort_by(-.score)'
```
