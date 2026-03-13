# Risk Lists

## Use Case Summary
Retrieve and build Recorded Future Risk Lists directly from the terminal to support enrichment, correlation, and automated detections. Analysts can pull risk-scored IPs, domains, URLs, hashes, or vulnerabilities on demand, or combine multiple risk rules into a single custom list, ensuring SOC workflows always use the most current intelligence.

## Issue
SOC teams often need the latest risk-scored indicators for investigations, detections, or proactive blocking. Navigating multiple platforms or manually exporting lists introduces friction and slows response. A direct retrieval method improves speed and consistency.

## Solution
Fetch Risk Lists in PS Banshee using [`banshee risklist`](../../reference/commands/#banshee-risklist) commands. Specify entity type and list name to retrieve Recorded Future's default, large, or rule-specific risk lists. Save the results locally for automated ingestion into SIEM or SOAR enrichment pipelines. Optionally append `--as-json` to output the list in JSON format for systems that support JSON-based ingestion, ensuring smooth integration without manual conversion.

Use [`banshee risklist create`](../../reference/commands/#banshee-risklist-create) to build a custom risk list by merging one or more risk rules into a single deduplicated output. Filter by minimum risk score, choose between CSV, EDL, or JSON output formats, and optionally upload the result directly to Recorded Future Fusion.