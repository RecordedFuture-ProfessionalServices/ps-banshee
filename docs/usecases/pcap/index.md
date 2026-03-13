# Packet Capture Enrichment

## Use Case Summary
Enrich packet capture files and observed IPs/domains with Recorded Future Intelligence to accelerate network security investigations and threat hunting activities.

## Issue
Raw PCAPs show network traffic but lack threat context. Analysts must manually look up IPs/domains to identify risk or threat activity, which is time-consuming and prone to oversight during high-volume investigations.

## Solution
Enrich network traffic directly in PS Banshee using [`banshee pcap`](../../reference/commands/#banshee-pcap) commands. Use [`banshee pcap enrich`](../../reference/commands/#banshee-pcap-enrich) to automatically parse packet captures, enrich observed indicators with threat intelligence, and display results directly in the terminal. Pipe enriched IOCs to [`banshee ioc lookup`](../../reference/commands/#banshee-ioc-lookup) for deeper analysis or add high-risk indicators to Watch Lists for long-term tracking and monitoring.