# sandbox

> See [index.md](https://recordedfuture-professionalservices.github.io/ps-banshee/knowledge-base/index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

Sandbox commands require `RF_SANDBOX_TOKEN` in addition to `RF_TOKEN`. Set `RF_SANDBOX_CHOICE` (or the global `--sandbox-choice`) to target a specific region: `eu` (default), `usa`, `apj`, `public`, or `private`.

______________________________________________________________________

### `banshee sandbox stats`

Aggregate sandbox submissions over a configurable lookback window and print a SOC morning brief: submission volume, score distribution, top malware families, platform coverage, extracted C2s, and SOAR-validated network IOCs.

| Option           | Short | Default | Description                            |
| ---------------- | ----- | ------- | -------------------------------------- |
| `--days INTEGER` | `-d`  | `7`     | Lookback window in days (min 1)        |
| `--subset`       | `-s`  | `org`   | Sample scope: `owned`, `public`, `org` |
| `--pretty`       | `-p`  |         | Human-readable Rich layout             |

Score buckets (triage 1–10 scale):

| Bucket                   | Score Range | Meaning                        |
| ------------------------ | ----------- | ------------------------------ |
| `malicious`              | 8–10        | Known malware, high confidence |
| `suspicious`             | 5–7         | Strong behavioural indicators  |
| `potentially_suspicious` | 3–4         | Some indicators                |
| `clean`                  | 1–2         | Low risk or benign             |

```
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats -d 30 | jq '.by_score'
```

**Response shape:** Returns a single JSON object:

| Field                    | Description                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `.period_start`          | Start of the aggregation window (ISO 8601)                                                                  |
| `.period_end`            | End of the aggregation window (ISO 8601)                                                                    |
| `.period_days`           | Lookback window in days                                                                                     |
| `.subset`                | Scope used (`owned`, `public`, `org`)                                                                       |
| `.total`                 | Total submissions in the window                                                                             |
| `.pending`               | Submissions still being analysed                                                                            |
| `.failed`                | Submissions that errored                                                                                    |
| `.by_kind`               | Object mapping submission kind (`file`, `url`, etc.) to count                                               |
| `.by_platform`           | Object mapping platform tag to count                                                                        |
| `.by_score`              | Object mapping score bucket name to count                                                                   |
| `.by_file_type`          | Object mapping file extension to count                                                                      |
| `.top_tags`              | Object with keys `malware_families`, `botnets`, `arch_file`, `behavioral_ttp` — each maps tag name to count |
| `.top_iocs`              | Object with keys `extracted_c2`, `verified_network`, `malicious_sha256` — each is an array of IOC strings   |
| `.daily_by_family`       | Object mapping malware family to daily counts                                                               |
| `.trend_vs_prior_period` | Object with `total` and `reported` sub-objects, each containing `current`, `prev`, and `pct_change`         |
| `.soar_skipped`          | `true` when SOAR validation was skipped (`.top_iocs.verified_network` will be empty)                        |

______________________________________________________________________

### `banshee sandbox list`

List sandbox samples — your own, your organisation's (default), or the public feed.

| Option            | Short | Default | Description                            |
| ----------------- | ----- | ------- | -------------------------------------- |
| `--subset`        | `-s`  | `org`   | Sample scope: `owned`, `public`, `org` |
| `--limit INTEGER` | `-l`  | `20`    | Max results (1–4095)                   |
| `--pretty`        | `-p`  |         | Human-readable table                   |

```
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
```

**Response shape:** Returns a flat JSON array. Each item:

| Field        | Description                                                 |
| ------------ | ----------------------------------------------------------- |
| `.id`        | Sample ID (e.g. `260722-x8lgjahyvx`)                        |
| `.status`    | Analysis status: `pending`, `running`, `reported`, `failed` |
| `.kind`      | Submission kind: `file`, `url`, `fetch`, `import`           |
| `.filename`  | Original filename (may be empty for URL submissions)        |
| `.submitted` | Submission timestamp (ISO 8601)                             |
| `.completed` | Completion timestamp (ISO 8601; absent if still running)    |
| `.sha256`    | SHA-256 of the submitted file                               |
| `.user_id`   | UUID of the submitting user                                 |

______________________________________________________________________

### `banshee sandbox search`

Search samples matching structured filters (hash, family, tag, botnet, wallet, IP, domain, URL, submission-date window) or a raw Triage query. At least one filter or `--query` must be provided.

| Option                   | Short | Default | Description                                                          |
| ------------------------ | ----- | ------- | -------------------------------------------------------------------- |
| `--hash TEXT`            |       |         | Filter by file hash (MD5/SHA1/SHA256)                                |
| `--family TEXT`          |       |         | Filter by malware family name                                        |
| `--tag TEXT`             | `-T`  |         | Filter by tag (repeatable)                                           |
| `--botnet TEXT`          |       |         | Filter by botnet name                                                |
| `--wallet TEXT`          |       |         | Filter by wallet address                                             |
| `--ip TEXT`              |       |         | Filter by IP address                                                 |
| `--domain TEXT`          |       |         | Filter by domain                                                     |
| `--url TEXT`             |       |         | Filter by URL                                                        |
| `--from-date YYYY-MM-DD` |       |         | Submitted on or after this date                                      |
| `--to-date YYYY-MM-DD`   |       |         | Submitted on or before this date                                     |
| `--query TEXT`           | `-q`  |         | Raw Triage query string (combined with structured filters using AND) |
| `--limit INTEGER`        | `-l`  | `50`    | Max results (1–200)                                                  |
| `--pretty`               | `-p`  |         | Human-readable table                                                 |

```
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
```

**Response shape:** Returns a JSON array — same structure as `sandbox list` items.

______________________________________________________________________

### `banshee sandbox get`

Fetch a summary for a single sandbox sample by ID: current status, overall score, target, creation and completion timestamps, SHA256, and per-task breakdown. Works for both in-progress and completed samples.

| Argument/Option        | Short | Description                |
| ---------------------- | ----- | -------------------------- |
| `SAMPLE_ID` (required) |       | Sandbox sample ID          |
| `--pretty`             | `-p`  | Human-readable Rich layout |

```
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
```

**Response shape:** Returns a single JSON object:

| Field        | Description                                                                    |
| ------------ | ------------------------------------------------------------------------------ |
| `.sample`    | Sample ID                                                                      |
| `.status`    | Analysis status: `pending`, `running`, `static_analysis`, `reported`, `failed` |
| `.target`    | Primary detonation target (filename or URL)                                    |
| `.score`     | Overall triage score (1–10; `0` while analysis is in progress)                 |
| `.created`   | Submission timestamp (ISO 8601)                                                |
| `.completed` | Completion timestamp (ISO 8601; absent while still running)                    |
| `.sha256`    | SHA-256 of the submitted file (absent for URL submissions)                     |
| `.owner`     | Submitting user ID                                                             |
| `.tasks`     | Object mapping task ID → `{kind, status, score, tags, platform}`               |

______________________________________________________________________

### `banshee sandbox download` *(mutating on disk)*

Download the original submitted sample bytes for one or more sample IDs. Each sample is wrapped in an AES-encrypted ZIP archive with password `infected` to prevent accidental detonation by antivirus, secure email gateways, or file managers. Extract with `7z x -pinfected <sample-id>.zip` — standard `unzip` does not handle AES-encrypted zips reliably.

Sample IDs may be passed as positional arguments or piped on stdin (whitespace-separated). Prompts for confirmation unless `--yes` is given. Bytes exist briefly in this process's memory during download and zipping — aggressive EDR memory scanning could still fire. Run this on an analyst-owned box, not a daily-driver corporate laptop.

| Argument/Option     | Short | Default    | Description                                                        |
| ------------------- | ----- | ---------- | ------------------------------------------------------------------ |
| `SAMPLE_IDS`        |       |            | One or more sample IDs (or read from stdin)                        |
| `--output-dir PATH` | `-d`  | (required) | Directory to save encrypted zip archives into (created if missing) |
| `--yes`             | `-y`  |            | Skip confirmation prompt                                           |
| `--workers INTEGER` | `-w`  | `1`        | Parallel download workers (1–16)                                   |

```
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
```

**Response:** Warning line printed once on stderr; per-sample `[<id>] Saved: <path> (<bytes> bytes, sha256=<hex>)` lines on stderr for each successful download; `[<id>] ERROR: <msg>` for failures. A partial-failure batch continues to completion and exits 1; a fully successful batch exits 0.

Archive contents: single entry named `<sample-id>` (no extension guessing) containing the raw sample bytes.

______________________________________________________________________

### `banshee sandbox delete` *(mutating)*

Delete a sandbox sample by ID and remove all associated task artifacts. Prompts for confirmation unless `--yes` is given.

| Argument/Option        | Description              |
| ---------------------- | ------------------------ |
| `SAMPLE_ID` (required) | Sample ID to delete      |
| `--yes` / `-y`         | Skip confirmation prompt |

```
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
```

**Response:** No output on success; exits 0.

______________________________________________________________________

### `banshee sandbox submit` *(mutating)*

Submit a sample for analysis. A local file is uploaded, a URL is detonated in a browser (or downloaded first with `--fetch`), and a public sample can be imported by ID with `--import`.

| Argument/Option      | Short | Description                                                                                           |
| -------------------- | ----- | ----------------------------------------------------------------------------------------------------- |
| `TARGET` (required)  |       | File path, URL, or public sample ID (with `--import`)                                                 |
| `--fetch`            |       | Download the URL first, then analyse the file. Mutually exclusive with `--import`                     |
| `--import`           |       | Treat the target as a public sample ID. Mutually exclusive with `--fetch`                             |
| `--profile TEXT`     |       | Analysis profile name or ID (repeatable; mutually exclusive with `--interactive`)                     |
| `--timeout INTEGER`  | `-t`  | Analysis timeout in seconds (1–3600)                                                                  |
| `--network`          | `-N`  | Network mode: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx`                           |
| `--geolocation TEXT` |       | VPN exit country code; requires `--network vpn`                                                       |
| `--tags TEXT`        | `-T`  | Custom tag (repeatable)                                                                               |
| `--password TEXT`    |       | Password for protected archives                                                                       |
| `--wait`             | `-w`  | Poll until analysis finishes, then print the overview report                                          |
| `--interactive`      | `-i`  | Pause at static analysis for profile selection via `set-profile`; mutually exclusive with `--profile` |
| `--pretty`           | `-p`  | Human-readable output                                                                                 |

```
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
```

**Response shape (default):** Returns the submitted sample as a JSON object with the same fields as `sandbox list` items (`id`, `status`, `kind`, `filename`, `submitted`, `sha256`, `user_id`). Use `.id` to track or report on the submission.

**Response shape (with `--wait`):** Returns the overview report — same structure as `sandbox report overview`.

______________________________________________________________________

### `banshee sandbox set-profile` *(mutating)*

Assign analysis profiles to a sample paused at static analysis (submitted with `--interactive`). Use `--auto` to let the sandbox choose automatically, or `--pick FILE:PROFILE` for manual per-file mapping.

| Argument/Option        | Short | Description                                                                |
| ---------------------- | ----- | -------------------------------------------------------------------------- |
| `SAMPLE_ID` (required) |       | ID of the sample paused at static analysis                                 |
| `--auto`               | `-a`  | Auto-select profiles for all files. Mutually exclusive with `--pick`       |
| `--pick FILE:PROFILE`  |       | Map one file to one profile (repeatable). Mutually exclusive with `--auto` |
| `--pretty`             | `-p`  | Human-readable output                                                      |

```
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
```

______________________________________________________________________

### `banshee sandbox profile list`

List all analysis profiles available in Recorded Future Sandbox.

| Option     | Short | Description          |
| ---------- | ----- | -------------------- |
| `--pretty` | `-p`  | Human-readable table |

```
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
```

**Response shape:** Returns a flat JSON array. Each item:

| Field          | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `.id`          | Profile UUID                                                               |
| `.name`        | Profile name                                                               |
| `.tags`        | Array of OS/locale tags (e.g. `["os:windows10-2004-x64", "locale:en-us"]`) |
| `.network`     | Network mode (e.g. `"internet"`, `"tor"`, `"vpn"`)                         |
| `.geolocation` | Array of VPN exit country codes (empty when not applicable)                |
| `.timeout`     | Analysis timeout in seconds                                                |
| `.options`     | Object with optional fields such as `browser`                              |

______________________________________________________________________

### `banshee sandbox profile get`

Fetch a single analysis profile by ID or name.

| Argument/Option                 | Short | Description          |
| ------------------------------- | ----- | -------------------- |
| `PROFILE_ID_OR_NAME` (required) |       | Profile UUID or name |
| `--pretty`                      | `-p`  | Human-readable table |

```
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
```

**Response shape:** Single profile object — same fields as items in `sandbox profile list`.

______________________________________________________________________

### `banshee sandbox profile create` *(mutating)*

Create a new analysis profile. The profile name must be unique within your organisation.

| Option               | Short | Default    | Description                                                                      |
| -------------------- | ----- | ---------- | -------------------------------------------------------------------------------- |
| `--name TEXT`        | `-n`  | (required) | Profile name (must be unique)                                                    |
| `--tag TEXT`         | `-T`  | (required) | OS/locale tag (repeatable). A locale tag must be paired with at least one OS tag |
| `--timeout INTEGER`  | `-t`  | `120`      | Analysis timeout in seconds (1–3600)                                             |
| `--network`          | `-N`  |            | Network mode: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx`      |
| `--geolocation TEXT` |       |            | VPN exit country code; requires `--network vpn` (repeatable)                     |
| `--browser`          | `-b`  |            | Browser: `chrome`, `firefox`, `ie11`, `microsoft-edge`                           |
| `--pretty`           | `-p`  |            | Human-readable table                                                             |

```
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
```

**Response shape:** Returns the created profile as a JSON object — same fields as `sandbox profile list` items.

______________________________________________________________________

### `banshee sandbox profile update` *(mutating)*

Update an existing analysis profile. Only the options you supply change — omitted options keep their current value. Use `--unset` to clear `network`, `browser`, or `geolocation`.

| Argument/Option                 | Short | Description                                                                 |
| ------------------------------- | ----- | --------------------------------------------------------------------------- |
| `PROFILE_ID_OR_NAME` (required) |       | Profile UUID or name                                                        |
| `--name TEXT`                   | `-n`  | New profile name                                                            |
| `--tag TEXT`                    | `-T`  | OS/locale tag; replaces all existing tags (repeatable)                      |
| `--timeout INTEGER`             | `-t`  | Analysis timeout in seconds (1–3600)                                        |
| `--network`                     | `-N`  | Network mode: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT`            |       | VPN exit country code; requires `--network vpn` (repeatable)                |
| `--browser`                     | `-b`  | Browser: `chrome`, `firefox`, `ie11`, `microsoft-edge`                      |
| `--unset`                       |       | Clear a field: `network`, `browser`, or `geolocation` (repeatable)          |
| `--pretty`                      | `-p`  | Human-readable status message                                               |

```
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
```

**Response shape:** Returns `{"updated": true}` when the profile exists and was updated, or `{"updated": false}` when it does not exist. Exits 0 either way.

______________________________________________________________________

### `banshee sandbox profile delete` *(mutating)*

Delete an analysis profile by ID or name. Safe to repeat: deleting a profile that no longer exists prints a warning and exits 0.

| Argument/Option                 | Short | Description              |
| ------------------------------- | ----- | ------------------------ |
| `PROFILE_ID_OR_NAME` (required) |       | Profile UUID or name     |
| `--yes` / `-y`                  |       | Skip confirmation prompt |

```
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
```

**Response:** No output on success; exits 0.

______________________________________________________________________

### `banshee sandbox report overview`

Fetch the full overview report for a completed sandbox sample: verdict score, malware family, tags, hashes, detection signatures, extracted malware configs, network IOCs, and per-task results. The sample must be in `reported` status.

| Argument/Option        | Short | Description                                         |
| ---------------------- | ----- | --------------------------------------------------- |
| `SAMPLE_ID` (required) |       | Sandbox sample ID                                   |
| `--wait`               | `-w`  | Poll for up to 30 minutes until the report is ready |
| `--pretty`             | `-p`  | Human-readable summarised view                      |

```
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
```

**Response shape:** Returns a single JSON object:

| Field         | Description                                                                                        |
| ------------- | -------------------------------------------------------------------------------------------------- |
| `.version`    | Report format version                                                                              |
| `.build`      | Sandbox build info                                                                                 |
| `.analysis`   | Verdict object: score, malware family, tags                                                        |
| `.sample`     | Sample metadata: id, kind, filename, sha256, submitted, completed                                  |
| `.signatures` | Detection signatures across all tasks                                                              |
| `.targets`    | Array of detonated target objects, each with `.iocs` (network IOCs) and malware config extractions |
| `.tasks`      | Array of per-task summaries: task ID, platform, status, verdict score                              |

______________________________________________________________________

### `banshee sandbox report static`

Fetch the static (pre-detonation) analysis report for a sandbox sample: verdict score, tags, unpacked files, static detection signatures, and extracted malware configs. Available as soon as static analysis finishes — before behavioural tasks complete.

| Argument/Option        | Short | Description                                         |
| ---------------------- | ----- | --------------------------------------------------- |
| `SAMPLE_ID` (required) |       | Sandbox sample ID                                   |
| `--wait`               | `-w`  | Poll for up to 10 minutes until the report is ready |
| `--pretty`             | `-p`  | Human-readable summarised view                      |

```
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
```

**Response shape:** Returns a single JSON object:

| Field           | Description                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------- |
| `.version`      | Report format version                                                                        |
| `.build`        | Sandbox build info                                                                           |
| `.sample`       | Sample metadata: id, kind, filename, sha256, submitted                                       |
| `.task`         | Static task metadata                                                                         |
| `.analysis`     | Verdict object: score, tags, static signatures                                               |
| `.files`        | Array of unpacked files — each has `sha256`, `filename`, `size`, and static analysis details |
| `.unpack_count` | Total number of files unpacked from the submission                                           |
| `.error_count`  | Number of files that could not be unpacked                                                   |

______________________________________________________________________

### `banshee sandbox report behavioral`

Fetch the behavioral (post-detonation) reports for a completed sandbox sample, one object per completed behavioral task. Incomplete tasks are omitted from the output and noted on stderr; the command exits non-zero until every task has finished. An empty array with exit 0 is returned when the sample has no behavioral tasks.

Process command lines in `--pretty` view are truncated by default — pass `--full-cmd` if you need them in full (they are taken verbatim from the malware sample, so treat them as untrusted).

| Argument/Option        | Short | Description                                                            |
| ---------------------- | ----- | ---------------------------------------------------------------------- |
| `SAMPLE_ID` (required) |       | Sandbox sample ID                                                      |
| `--wait`               | `-w`  | Poll for up to 30 minutes until all tasks are complete                 |
| `--full-cmd`           |       | Show full untruncated process command lines (treat as untrusted input) |
| `--pretty`             | `-p`  | Human-readable summarised view per task                                |

```
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
```

**Response shape:** Returns a JSON array. Each item corresponds to one behavioral task:

| Field         | Description                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------------- |
| `.task_id`    | Behavioral task ID                                                                                               |
| `.version`    | Report format version                                                                                            |
| `.build`      | Sandbox build info                                                                                               |
| `.sample`     | Sample metadata: id, kind, filename, sha256                                                                      |
| `.task`       | Task metadata: platform, status, started, completed                                                              |
| `.analysis`   | Verdict object: score, malware family, tags                                                                      |
| `.tags`       | Array of behavioural tags (e.g. `discovery`, `execution`)                                                        |
| `.signatures` | Array of triggered detection signatures                                                                          |
| `.processes`  | Array of observed processes — each has `pid`, `name`, `cmd` (truncated unless `--full-cmd`), and child processes |
| `.network`    | Network activity: `.flows` (connection records), `.dns` (DNS queries), `.http` (HTTP requests)                   |
| `.dumped`     | Array of dumped/extracted files with their SHA-256 hashes                                                        |
