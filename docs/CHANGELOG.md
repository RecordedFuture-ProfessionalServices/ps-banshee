# Release History

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


