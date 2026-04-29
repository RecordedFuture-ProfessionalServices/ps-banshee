# Email Enrichment

## Use Case Summary
Enrich e-mail (EML) files with Recorded Future Intelligence to quickly identify malicious indicators embedded in phishing or suspicious emails, accelerating triage and incident response.

## Issue
Phishing and malicious emails contain embedded indicators — spoofed sender IPs in headers and malicious URLs in the body — that analysts must manually extract and look up across multiple tools. This is slow, error-prone, and creates gaps in coverage during high-volume phishing campaigns.

## Solution
Enrich EML files directly in PS Banshee using [`banshee email enrich`](../../reference/commands/#banshee-email-enrich). The command automatically parses the email, extracts IP addresses from the message headers and URLs from the body, and enriches each indicator with Recorded Future threat intelligence — returning risk scores, threat actor associations, malware links, and triggered risk rules in a single step.

Use `--threat-hunt` to surface indicators linked to known threat actors even when their risk score falls below the threshold, enabling retrospective threat hunting across your email data. Use `--pretty` for a human-readable summary directly in the terminal.