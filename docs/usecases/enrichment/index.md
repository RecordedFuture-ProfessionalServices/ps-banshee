# IOC Enrichment

## Use Case Summary
Enrich Indicators of Compromise (IOCs) with Recorded Future risk scores, related entities, and analyst context to accelerate Security Operations Center (SOC) triage and threat investigations.

For further information on IOC enrichment click [here](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future).

## Issue
Analysts spend time pivoting between tools for IPs/domains/URLs/hashes/vulnerabilities, which slows investigations and increases response times. Manual correlation of threat intelligence across multiple sources creates gaps in analysis and delays incident response.

## Solution
Enrich IOCs directly in PS Banshee using [`banshee ioc`](../../reference/commands/#banshee-ioc) commands. Lookup individual indicators to get risk scores, AI insights, and threat actor/malware associations. Search for IOCs using various filtering options to identify high-risk indicators. Leverage the enriched context to understand what threats the organization is facing and accelerate incident response decisions.