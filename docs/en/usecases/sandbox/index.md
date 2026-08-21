# Sandbox Analysis

## Use Case Summary
Submit files and URLs for automated malware analysis in Recorded Future Sandbox, retrieve the resulting reports, and hand-off validated samples for offline analysis, to accelerate Security Operations Center (SOC) triage and threat investigations.

## Issue
Analysts need to detonate suspicious files and URLs in a safe, controlled environment to determine intent and extract threat indicators. Without an integrated workflow, collecting and correlating the resulting reports — static signatures, behavioral activity, network IOCs, and malware configs — requires manual steps across multiple tools, slowing SOC response.

## Solution
Submit samples and retrieve reports directly in PS Banshee using [`banshee sandbox`](../../reference/commands.md#banshee-sandbox) commands.

- Use [`banshee sandbox submit`](../../reference/commands.md#banshee-sandbox-submit) to submit a local file, URL, or public sample for analysis. Add [`--wait`](../../reference/commands.md#banshee-sandbox-submit--wait) to poll until analysis completes and print the overview report immediately, or [`--interactive`](../../reference/commands.md#banshee-sandbox-submit--interactive) to pause at static analysis and choose detonation profiles before proceeding.

- Once analysis finishes, use [`banshee sandbox report overview`](../../reference/commands.md#banshee-sandbox-report-overview) for a summary of the verdict, malware family, network IOCs, and per-task results; [`banshee sandbox report static`](../../reference/commands.md#banshee-sandbox-report-static) for pre-detonation analysis and extracted malware configs; and [`banshee sandbox report behavioral`](../../reference/commands.md#banshee-sandbox-report-behavioral) for post-detonation activity including triggered signatures, observed processes, and extracted C2s.

- Use [`banshee sandbox stats`](../../reference/commands.md#banshee-sandbox-stats) to generate a SOC morning brief showing submission volume, score distribution, top malware families, and network IOCs across a configurable lookback window — suitable for shift handover or daily triage.

- Use [`banshee sandbox list`](../../reference/commands.md#banshee-sandbox-list) to review recent submissions from your own account, your organisation, or the public feed, and [`banshee sandbox get`](../../reference/commands.md#banshee-sandbox-get) to check the current status, overall score, and per-task breakdown of any single sample without pulling a full report.

- Use [`banshee sandbox search`](../../reference/commands.md#banshee-sandbox-search) to pivot across historical submissions by hash, malware family, tag, botnet, wallet, network indicator (IP, domain, URL), or a submission-date window. Pass raw Triage query strings with `--query` for `AND`/`OR`/`NOT` expressions.

- Use [`banshee sandbox download`](../../reference/commands.md#banshee-sandbox-download) to retrieve the original submitted bytes for offline analysis (YARA/Sigma tuning, EDR detection testing, campaign attribution). Each sample is wrapped in an AES-encrypted ZIP archive with password `infected` — extract with `7z x -pinfected <sample-id>.zip`. Bytes exist briefly in process memory during download and zipping, so run this on an analyst-owned box.

- Use [`banshee sandbox delete`](../../reference/commands.md#banshee-sandbox-delete) to remove samples and their associated artifacts when no longer needed.

- For teams using custom detonation environments, [`banshee sandbox profile`](../../reference/commands.md#banshee-sandbox-profile) commands let you create, update, and delete analysis profiles that control the OS, network configuration, browser, and analysis timeout applied to each submission.
