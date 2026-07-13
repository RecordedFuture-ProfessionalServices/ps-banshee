# Sandbox Stats Command — Review Findings

Review of `banshee sandbox stats -d 30 -p` output, code, and documentation.
Files in scope: `banshee/commands/cmd_sandbox.py`, `banshee/sandbox/stats.py`, `banshee/sandbox/output.py`, `banshee/commands/epilogs.py`.

---

## Critical bugs / misleading data


### [x] 2. Platform counts inflate beyond submission count (`stats.py:210–213`)

`platform_counter` increments once per behavioral **task**, not per sample. A sample detonated on both Windows 10 and Windows 7 is counted twice. The pretty output shows 1,872 Windows 10 and 1,364 Windows 7 against 2,000 total submissions — that's 3,236 "platform slots" for 2,000 samples. An analyst reads these as submission counts.

Fix: count unique `(sample_id, os)` pairs, or add a note "(task count)" to the Platform table title.

---

### [x] 3. `linux` and `upx` land in "Behavioral / TTP" (`stats.py:232–233`)

`linux` is a platform/OS tag and `upx` is a packer. Neither is a TTP. They fall into `behavioral_ttp` because they lack `family:`/`botnet:`/`brand:`/`os:` prefix and aren't in `_ARCH_FILE_TAGS`. `linux` appearing at #6 with 163 hits in the TTP column is actively wrong.

Fix: add `linux`, `macos`, `android`, `windows`, `upx`, `packed`, `obfuscated` (and similar packer/platform strings) to `_ARCH_FILE_TAGS`, or add an explicit `_PLATFORM_TAGS` exclusion set.

---

### [ ] 4. Botnet column shows raw MD5-like internal profile IDs

`42f96ba38745d04084a742695fb71b7c`, `c658b5e57f4b4caf85e10a29e16f94fa` etc. are Triage-internal network profile hashes, not analyst-readable botnet names. `lzrd` (an actual named botnet) is mixed in with these.

Fix: filter out botnet tags whose value looks like a hex hash (matches `^[0-9a-f]{32}$`), or only show botnets with human-readable names. Alternatively rename the section "Network profiles" to set expectations correctly.

---

### [ ] 5. `subset` is a plain `str` with no validation (`cmd_sandbox.py:48–51`)

`--subset garbage` passes silently to the API. Per project conventions (CLAUDE.md), this must use the psengine `Literal` type so invalid values are rejected at the CLI layer.

Fix: use `SandboxSubset` (or equivalent psengine Literal) as the type annotation, same pattern as `SandboxChoice`.

---

## Actionability problems

### [ ] 6. Telegram/Steam dead-drop resolvers dominate the C2 list

`https://telegram.me/…` and `https://steamcommunity.com/…` appear as the top two C2s with 70 hits each, burying the real infrastructure. These are Vidar/stealer dead-drop patterns — the malware reads a Steam or Telegram profile to resolve the actual C2. They are not actor-controlled C2 infrastructure. RF correctly scores them at 5, but hit-count sorting makes them #1.

Fix: sort extracted C2s by RF risk score descending, then by hit count as tiebreaker. Alternatively, suppress entries where RF score < `_SOAR_MIN_SCORE` (25) and at least one entry with score >= 25 exists.

---

### [ ] 7. Cloudflare and Telegram IPs in "Verified network IOCs"

`188.114.96.0`, `188.114.97.0` (Cloudflare anycast), `149.154.166.110`, `149.154.167.99` (Telegram servers) appear with RF scores 64–74. They score high because malware routes through them, but they are not actor-controlled infrastructure. Blocking them would break Cloudflare-proxied services or Telegram. These are false positives in this context.

Fix: add a known-shared-infra allowlist (`188.114.96.0/22`, `149.154.160.0/20`, `91.108.0.0/16` etc.) to suppress from the verified IOC output, or at minimum flag them with a `[shared infra]` label.

---

### [ ] 8. `baxe.pics` / `iuta.today` appear in both C2 and Verified IOC sections

The same infrastructure appears twice: `http://baxe.pics:48261` in Extracted C2s and `baxe.pics` in Verified network IOCs. An analyst sees it as two separate findings.

Fix: when building the Verified network IOCs display, suppress domains/IPs that already appear (as host component) in the extracted C2 list, or note duplicates inline.

---

### [ ] 9. RF score 0 looks identical to low-risk scores (both grey)

`_rf_score_cell` colors scores 0–24 identically (`grey50`). Score 0 means RF has no data — that is different from "low risk." An IP with score 0 might be a novel, unindexed C2. Currently `_rf_score_cell(0)` returns `[grey50]0[/grey50]`; the `—` display only triggers when the value is `None`.

Fix: treat `rf_score == 0` the same as `None` — display `—` in grey, or add a distinct colour (e.g. `dim`) with a tooltip/footnote "no RF data".

---

### [ ] 10. `discovery` at #1 in Behavioral TTPs every run is noise

`discovery` will top the TTP list in almost every sandbox run — system enumeration is universal in malware. It carries no shift-specific signal. Same applies to `execution` and `persistence` to a lesser degree.

Fix: consider showing a delta vs prior period for each TTP (new this period vs baseline), or add a configurable exclude list for ultra-common categories.

---

## Layout / display issues

### [ ] 11. Score bar labels truncated in pretty output (`output.py:195–204`)

The terminal output shows `sus…` and `lik…` for the suspicious and likely-benign score rows. Rich is truncating the Stats column content. An analyst reading the brief loses the score labels.

Fix: shorten the labels or widen the Stats column minimum width. Also remove the dead `_SCORE_LABELS` dict (lines 37–41) which is never used in the pretty path — `_SCORE_SHORT_LABELS` is used instead.

---

### [ ] 12. File types list is unbounded, includes non-payload types (`output.py:313–329`)

All 35 file types are shown with no cap, including `.jpg`, `.png`, `.svg`, `.xml`, `.html` — embedded resources, not payloads. The bar chart is meaningless when `.js` at 2,545 makes everything else a 1-pixel bar.

Fix: cap to top 12 types (`_DISPLAY_CAP` or a dedicated `_FILE_TYPE_TOP_N = 12`). Consider filtering out pure asset extensions: `.jpg`, `.png`, `.svg`, `.xml`, `.html`, `.gif`.

---

### [ ] 13. Limit-hit warning appears only on stderr, invisible in pretty output (`stats.py:416–419`)

When the 2,000-sample cap is hit, the warning goes to stderr only. In `--pretty` mode the analyst sees no indication the data is truncated. This is particularly bad because the cap silently breaks trend arrows (prev period returns 0 when all 2,000 slots are in the current window).

Fix: include a visible `[WARNING] Sample cap hit — data may be incomplete` line in the pretty output header (e.g. in the Rule subtitle or as a `console.print` before the first section).

---

## Minor inconsistencies

### [ ] 14. `by_status` field is dead in the pretty path

`by_status` is computed, stored in `SandboxStats`, and emitted in JSON, but never rendered in `--pretty` mode. The pretty header derives `pending` and `failed` directly from the stats object. Either use `by_status` to drive the display or remove the field from the dataclass and JSON if `pending`/`failed` are sufficient.

### [ ] 15. `_SCORE_LABELS` dict is dead code (`output.py:37–41`)

`_SCORE_LABELS` is defined but never referenced; only `_SCORE_SHORT_LABELS` is used. Remove it.

### [ ] 16. Epilog score table contradicts the pretty output labels

The epilog (`epilogs.py:649–657`) correctly documents `potentially_suspicious | 3–4` and `clean | 1–2`. The `_SCORE_SHORT_LABELS` in the pretty output shows `2–4` and `(1)`. They disagree. After fixing issue #1, verify the epilog stays in sync.
