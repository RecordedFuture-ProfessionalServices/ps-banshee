# Release History

## 1.5.0 - 2026-08-21

### Added
- New [`sandbox`](reference/commands.md#banshee-sandbox) command group for Recorded Future Sandbox. Requires `RF_SANDBOX_TOKEN`; region selectable via [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) or `RF_SANDBOX_CHOICE` (`eu` default, `usa`, `apj`, `public`, `private`).
- New [`sandbox submit`](reference/commands.md#banshee-sandbox-submit) sub-command to submit a local file, URL, public sample ID (`--import`), or URL-to-download (`--fetch`) for analysis. Supports profile assignment, custom tags, timeout, network mode (including VPN with geolocation), archive password, [`--wait`](reference/commands.md#banshee-sandbox-submit--wait) to poll until analysis completes and print the overview report, and [`--interactive`](reference/commands.md#banshee-sandbox-submit--interactive) to pause at static analysis and pick profiles per file before detonation.
- New [`sandbox report overview`](reference/commands.md#banshee-sandbox-report-overview), [`sandbox report static`](reference/commands.md#banshee-sandbox-report-static), and [`sandbox report behavioral`](reference/commands.md#banshee-sandbox-report-behavioral) sub-commands to fetch the combined verdict report, the pre-detonation static analysis, or the per-task post-detonation reports for a sample. Each supports [`--wait`](reference/commands.md#banshee-sandbox-report-overview--wait) to poll until the report is ready.
- New [`sandbox list`](reference/commands.md#banshee-sandbox-list) sub-command to list samples in your own, your organisation's, or the public feed.
- New [`sandbox search`](reference/commands.md#banshee-sandbox-search) sub-command to pivot across historical submissions by hash, malware family, tag, botnet, wallet, network indicator (IP, domain, URL), or a submission-date window. Also accepts raw Triage query strings via [`--query`](reference/commands.md#banshee-sandbox-search--query) for `AND`/`OR`/`NOT` expressions.
- New [`sandbox get`](reference/commands.md#banshee-sandbox-get) sub-command to fetch the current status, overall score, and per-task breakdown for a sample without pulling a full report. Works for both in-progress and completed samples.
- New [`sandbox download`](reference/commands.md#banshee-sandbox-download) sub-command to retrieve the original submitted bytes for one or more sample IDs. Each sample is wrapped in an AES-encrypted ZIP archive with password `infected` (matching the MalwareBazaar/VirusTotal/Triage convention) to prevent accidental detonation by antivirus, secure email gateways, or file managers. Sample IDs may be passed as positional arguments or piped on stdin. Extract with `7z x -pinfected <sample-id>.zip`.
- New [`sandbox delete`](reference/commands.md#banshee-sandbox-delete) sub-command to remove a sample and its task artifacts (prompts for confirmation unless `--yes` is given).
- New [`sandbox set-profile`](reference/commands.md#banshee-sandbox-set-profile) sub-command to assign analysis profiles to a sample paused at static analysis (either `--auto` or per-file `--pick FILE:PROFILE`).
- New [`sandbox profile`](reference/commands.md#banshee-sandbox-profile) sub-command group to manage custom detonation profiles: [`list`](reference/commands.md#banshee-sandbox-profile-list), [`get`](reference/commands.md#banshee-sandbox-profile-get), [`create`](reference/commands.md#banshee-sandbox-profile-create), [`update`](reference/commands.md#banshee-sandbox-profile-update) (with `--unset` to clear fields), and [`delete`](reference/commands.md#banshee-sandbox-profile-delete).
- New [`sandbox stats`](reference/commands.md#banshee-sandbox-stats) sub-command producing a SOC morning brief: submission volume, score distribution (1–10 triage scale bucketed as malicious / suspicious / potentially suspicious / clean), platform coverage, top malware families and botnets, behavioural TTPs, extracted C2s, and SOAR-validated network IOCs across a configurable lookback window.
- Docs: Korean (`ko`) language infrastructure. Content ships in a follow-up PR; the missing-translation banner is shown until then.
- Docs: `scripts/docs.py` — `build-all`, `dev`, `check-translations`, `translate` commands.
- Docs: CI drift enforcement for every non-English translation. Contributors run the LLM translator locally (`uv sync --group translations && scripts/docs.py translate --lang <code> --all`); CI never calls an LLM.

### Changed
- Configuration: added `BansheeConfig(psengine.ConfigModel)` subclass to carry banshee-specific global fields (`sandbox_choice`). New root-level [`--sandbox-key`](reference/commands.md#banshee--sandbox-key) / `RF_SANDBOX_TOKEN` and [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) / `RF_SANDBOX_CHOICE` options make sandbox authentication available to any command that needs it.
- Docs: dropped `mike` versioned deploys; the site now deploys at the root URL. Previously versioned URLs (`/1.x/…`) no longer resolve; use the root URL instead.
- Docs: replaced `mkdocs-static-i18n` with a fastapi-style per-language build orchestrated by `scripts/docs.py`. One authoritative `docs/mkdocs.yml`; translated languages own only their translated markdown files.
- Docs: swapped `noklam/mkdocs-llmstxt-md` for `pawamoy/mkdocs-llmstxt`; `llms.txt` / `llms-full.txt` are English-only and live at the site root.


## v.1.4.1 - 2026-07-13

### Changed
- Bump `psengine` dependencies.


## v.1.4.0 - 2026-07-13

### Added
- New [`-C`/`--count`](reference/commands.md#banshee-risklist-stat--count) option for [`risklist stat`](reference/commands.md#banshee-risklist-stat) to download the risk list and print a table of indicator counts per risk score.

## v1.3.1 - 2026-06-30

### Changed
- Bump dependencies.

## 1.3.0 - 2026-06-15

### Added
- New [`email enrich`](reference/commands.md#banshee-email-enrich) sub-command to enrich EML files by extracting header IPs and body URLs, then returning Recorded Future intelligence including risk score, threat actor associations, malware links, and risk rule evidence.
- New [`ca export`](reference/commands.md#banshee-ca-export) sub-command to export Classic Alerts as full JSON or a summary CSV. Reads alert IDs piped from [`ca search`](reference/commands.md#banshee-ca-search).
- New [`pba export`](reference/commands.md#banshee-pba-export) sub-command to export Playbook Alerts as full JSON or a summary CSV. Reads the search results piped from [`pba search`](reference/commands.md#banshee-pba-search).
- New [`-o`/`--org-id`](reference/commands.md#banshee-pba-search--org-id) option for [`pba search`](reference/commands.md#banshee-pba-search) to filter Playbook Alerts by owning organisation ID (repeatable).
- New [`-o`/`--overwrite`](reference/commands.md#banshee-list-bulk-add--overwrite) option for [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) to make the list match the supplied entities exactly — adding new entities and removing any currently on the list that were not provided.
- New [`list copy`](reference/commands.md#banshee-list-copy) sub-command to copy entities from one list to another. Appends by default, or use [`-o`/`--overwrite`](reference/commands.md#banshee-list-copy--overwrite) to make the destination mirror the source exactly.
- Support for [using banshee with AI agents](getting-started/llms.md), so coding assistants can discover and run the CLI.

### Changed
- [`list clear`](reference/commands.md#banshee-list-clear) now removes entities concurrently (much faster on large lists), matching [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove): it reports what was removed, grouping output by outcome (`REMOVED`, and any that could not be removed) and sorting it for readability.
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) now skips entities already on the list instead of attempting to re-add them, reporting them as `UNCHANGED`. This is a significant speed-up when repeatedly re-running the same input file to add and remove entities.
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) and [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) now group their output by outcome (`ADDED`, `REMOVED`, `UNCHANGED`) and sort it for readability.
- [`ca search`](reference/commands.md#banshee-ca-search) and [`pba search`](reference/commands.md#banshee-pba-search) now write progress indicators to stderr, keeping stdout clean for piping into the new `export` commands.
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) and [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) pretty output (`-p`, `--pretty`) now colour-codes the risk score based on maliciousness.
- Upgraded PSEngine to ~v2.8.1.

### Fixed
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) and [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) now ignore blank input lines and report a clear error when no entities are supplied.

## 1.1.3 - 2026-03-18

### Fixed
- Fixed an issue in [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) where multithreading was not being used in SOAR enrichment. The risk score enrichment is now faster for large captures.


## 1.1.0 - 2026-03-13

### Added
- New [`risklist create`](reference/commands.md#banshee-risklist-create) sub-command to build a custom risk list by merging one or more Recorded Future risk rules into a single deduplicated file. Supports CSV, JSON, and EDL output formats, optional minimum risk score filtering, and direct upload to Recorded Future Fusion.
- New [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) sub-command for fast bulk enrichment of IOCs. Batches up to 1,000 indicators per API call and returns risk score and triggered risk rules for each indicator. Supports all IOC types: IP, domain, URL, hash, and vulnerability.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON output now includes risk rule evidence details which details the specific evidence that caused the risk rule to trigger.

### Changed
- [`entity search`](reference/commands.md#banshee-entity-search) default limit increased to 100 results.
- [`list search`](reference/commands.md#banshee-list-search) default limit increased to 1,000 results.
- [`pba search`](reference/commands.md#banshee-pba-search) default limit increased to 50 results.
- [`pba search`](reference/commands.md#banshee-pba-search) maximum limit increased to 10,000 results.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) now accepts risk scores as low as 1.

### Fixed
- Fixed an issue in [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) where multithreading was not being used, causing bulk lookups to run sequentially. Lookups are now up to 20x faster when enriching multiple indicators.
- Fixed an issue in [`risklist fetch`](reference/commands.md#banshee-risklist-fetch) where the command would fail when parsing unusually large column values in CSV files.
- Fixed an issue where [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) would fail when parsing empty IOC links.
- Fixed an issue in [`list`](reference/commands.md#banshee-list) commands where the error cause was not always printed correctly when an API error occurred.

## 1.0.0 - 2025-12-05

### Added

- New [`risklist`](reference/commands.md#banshee-risklist) command to download and check metadata for Recorded Future Risk Lists.
- New [`rules`](reference/commands.md#banshee-rules) command to search for and download detection rules (YARA, Snort, Sigma).
- CVSS v4 field support in [`ioc search`](reference/commands.md#banshee-ioc-search) and [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) commands.

### Fixed

- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) and [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) now deduplicate user-supplied entities.
- Fixed an issue where entity names with spaces were not parsing correctly in [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) and [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove).
- [`pba lookup`](reference/commands.md#banshee-pba-lookup) now correctly handles alerts when image retrieval fails.

### Changed

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON output now includes risk rule evidence details and all risk rules the IOC triggered.
- Upgraded PSEngine to v2.4.0.


## 0.0.5 - 2025-11-12

## Fixed

- Fixed an issue in [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) where the program would exit unexpectedly if no IPs or domains were found in the pcap file.

## 0.0.4 - 2025-11-07

### Added

- Added support for filtering by alert status in the [`ca search`](reference/commands.md#banshee-ca-search) command.
- Added support for filtering by entity in the [`pba search`](reference/commands.md#banshee-pba-search) command.
- Added support for the `malware_report` category to all `pba` commands.
- Pretty output (`-p`, `--pretty`) for [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) and [`ioc search`](reference/commands.md#banshee-ioc-search) now includes the hash algorithm for hashes.
- Pretty output (`-p`, `--pretty`) for [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) and [`ioc search`](reference/commands.md#banshee-ioc-search) now includes the lifecycle stage for vulnerabilities.
- Added `-r`/`--risk-score` option to [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) to filter results by risk score.
- Added `-t`/`--threat-hunt` option to [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) to enable threat hunting.

### Changed

- Optimized field selection for each verbosity level in [`ioc lookup`](reference/commands.md#banshee-ioc-lookup).
- Extended [`ioc search`](reference/commands.md#banshee-ioc-search) to support verbosity levels 1 through 5 (default is 1).
- Renamed the `pcap analyze` sub-command to [`pcap enrich`](reference/commands.md#banshee-pcap-enrich).
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) now produces a refined JSON output, including a Wireshark-compatible filter query.
- Upgraded PSEngine to v2.3.0.

### Fixed

- Fixed an issue where [`ca rules`](reference/commands.md#banshee-ca-rules) would truncate results at 10 alerting rules.
- Fixed an error in [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) when an IOC had no evidence details.

### Removed

- Removed interactive TUI output from `pba enrich`; replaced with pretty output (`--pretty`, `-p`).


## 0.0.3 - 2025-09-02

### Added

- New [`ca update`](reference/commands.md#banshee-ca-update) sub-command to update one or more Classic Alerts.
- New [`pba update`](reference/commands.md#banshee-pba-update) sub-command to update one or more Playbook Alerts.
- [`pba`](reference/commands.md#banshee-pba) commands now support `geopolitics_facility` category.
- Python 3.13 compatibility.
- `tshark` version check now enforces minimum version 4.4.5.

### Fixed

- `pcap analyze` no longer crashes due to version mismatch.
- Improved exception handling throughout the CLI.

### Changed

- `ioc search ENTITY_TYPE IOC` now accepts whitespace separatated IOCs, instead of a comma-separated string.
- `pba lookup ALERT_ID -p` output formatting improved.
- `ca search --triggered` now supports time ranges.
- `ca search -r` now accepts multiple rules by repeating `-r` (e.g. `-r rule1 -r rule2`), instead of a comma-separated string.
- Upgraded PSEngine to v2.0.6.


## 0.0.2 - 2025-02-20

### Added

- New [`entity`](reference/commands.md#banshee-entity) command to search and lookup entities
- New [`list`](reference/commands.md#banshee-list) command to manage Recorded Future Lists & Watch Lists
- New [`ioc rules`](reference/commands.md#banshee-ioc-rules) sub-command to search and filter IOC rules
- New ``--debug`` option for enhanced troubleshooting


### Changed

- Sub-command [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) option ``-v`` now allows the user to pick a level of verbosity (from 1 to 5)
- Sub-command [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) now requires an entity type as an argument, for example ``banshee ioc lookup ip 8.8.8.8``
- Sub-command [`ca lookup`](reference/commands.md#banshee-ca-lookup) now returns a refined pretty alert
- PSEngine upgraded to v2.0.2


## 0.0.1 - 2024-09-01

### Added

- Beta release

---

🚀 Brought to you by the Cyber Security Engineers at Recorded


