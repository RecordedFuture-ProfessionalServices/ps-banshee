# Detection Rules

## Use Case Summary
Allow analysts and detection engineers to quickly search and filter Recorded Future detection rules (YARA, Snort, Sigma) based on threat actors, malware, MITRE ATT&CK techniques, creation dates, or entities defined in the Threat Map. Results can be viewed in the terminal or saved as individual rule files for deployment.

## Issue
During threat hunting or incident response, analysts need fast, targeted access to relevant detection rules. Searching manually across platforms or large rule repositories is time-consuming and makes it difficult to align rules with active threats, priority actors, or techniques.

## Solution
Search, filter, and retrieve detection rules directly in PS Banshee using [`banshee rules`](../../reference/commands/#banshee-rules) commands. Filter by rule type, threat actors, malware families, ATT&CK techniques, and more. Leverage Threat Map filtering (`--threat-actor-map`, `--threat-malware-map`) to focus searches on threats relevant to the organization. Use `--limit` to retrieve up to 1000 rules and optionally save rule files for rapid deployment into SIEM, IDS/IPS, or detection engineering workflows.