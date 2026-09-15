# pba

> **Playbook Alerts** - 自動化驅動的警報。ID 為 36 字元的 UUID，`task:` 前綴為選用（例如 `d144a9ec-90e6-40fe-89b0-d85ed65d3e9c` 或 `task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c`）。PBA 專屬類別：`domain_abuse`、`cyber_vulnerability`、`third_party_risk`、`code_repo_leakage`、`identity_novel_exposures`、`geopolitics_facility`、`malware_report`。如需使用舊版規則型警報（短格式不透明 ID），請改用 [`ca`](ca.md)。
>
> 有關身份驗證、就緒性檢查、輸出慣例及共用 LLM 說明，請參閱 [index.md](index.md)。

### `banshee pba search`

使用豐富的篩選選項搜尋 Playbook Alerts。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--created TEXT` | `-C` | | 依建立日期篩選（例如 `1d`、`7d`） |
| `--updated TEXT` | `-u` | | 依更新日期篩選 |
| `--category` | `-c` | 全部 | 一個或多個類別（可重複指定）：`domain_abuse`、`cyber_vulnerability`、`third_party_risk`、`code_repo_leakage`、`identity_novel_exposures`、`geopolitics_facility`、`malware_report` |
| `--entity TEXT` | `-e` | | 依關聯實體篩選（可重複指定） |
| `--priority` | `-P` | 全部 | `Informational`、`Moderate`、`High`（可重複指定） |
| `--status` | `-s` | 全部 | `New`、`InProgress`、`Dismissed`、`Resolved`（可重複指定） |
| `--org-id TEXT` | `-o` | 全部 | 依擁有組織 ID 篩選（可重複指定）。接受 10 字元 ID 或 16 字元 `uhash:` 格式 |
| `--limit INTEGER` | `-l` | `100` | 最大結果數（1–10000） |
| `--pretty` | `-p` | | 美化輸出 |

**回應結構：** 傳回包含三個頂層鍵的 JSON 物件：`.data`（警報記錄陣列）、`.counts`（`{returned, total}`）及 `.status`（請求狀態物件：`{status_code, status_message}`）。警報記錄位於 `.data[]` 下，包含以下欄位：`playbook_alert_id`、`alert_rule`（`{id, label, name}`）、`category`、`priority`、`status`、`title`、`created`、`updated`、`actions_taken`、`owner_organisation_details`。

```bash
banshee pba search --created 1d
banshee pba search -C 1d -u 1d -p
banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse
banshee pba search --updated 7d --category domain_abuse --pretty
banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New
banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d
banshee pba search -o 69sKLfTGsS -o uhash:5zQaSyRpA1 -C 7d -P High
```

---

### `banshee pba lookup ALERT_ID`

依 ID 擷取單一 Playbook Alert。接受帶有或不帶有 `task:` 前綴的 36 字元 UUID — CLI 會自動在裸 UUID 前加上 `task:`。

```bash
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p
```

**回應結構：** 傳回包含四個頂層鍵的單一 JSON 物件：`playbook_alert_id`、`panel_status`、`panel_evidence_summary`、`panel_log_v2`。

**`.panel_status`** — 警報的中繼資料及當前狀態：

| 欄位 | 說明 |
|-------|-------------|
| `.panel_status.status` | 當前狀態：`New`、`InProgress`、`Dismissed`、`Resolved` |
| `.panel_status.priority` | 優先級：`Informational`、`Moderate`、`High` |
| `.panel_status.case_rule_label` | 人類可讀的規則名稱（例如 `"Data Leakage on Code Repository"`） |
| `.panel_status.entity_id` | 主要對象的 RF 實體 ID（例如 `"url:https://..."`） |
| `.panel_status.entity_name` | 主要實體名稱 |
| `.panel_status.risk_score` | RF 風險評分（整數） |
| `.panel_status.targets[]` | `{name}` 物件陣列 — 被鎖定或受影響的實體 |
| `.panel_status.actions_taken[]` | 已記錄於警報上的處置動作 |
| `.panel_status.created` | 建立時間戳記（ISO 8601） |
| `.panel_status.updated` | 最後更新時間戳記（ISO 8601） |

**`.panel_evidence_summary`** — 證據詳情；結構因警報類別而異。以 `code_repo_leakage` 為例：

| 欄位 | 說明 |
|-------|-------------|
| `.panel_evidence_summary.repository.name` | 儲存庫 URL |
| `.panel_evidence_summary.repository.owner.name` | 儲存庫擁有者的登入名稱 |
| `.panel_evidence_summary.evidence[]` | 證據項目陣列 |
| `.panel_evidence_summary.evidence[].url` | 外洩內容的來源 URL |
| `.panel_evidence_summary.evidence[].content` | 外洩內容的片段 |
| `.panel_evidence_summary.evidence[].assessments[]` | 評估物件：`{id, title, value}` |
| `.panel_evidence_summary.evidence[].targets[]` | 目標實體：`{name}` |
| `.panel_evidence_summary.evidence[].published` | 發布時間戳記 |

```bash
# 摘要：實體、規則、狀態
banshee pba lookup task:<ID> | jq '{entity: .panel_status.entity_name, rule: .panel_status.case_rule_label, status: .panel_status.status, priority: .panel_status.priority}'

# 擷取證據 URL（code_repo_leakage）
banshee pba lookup task:<ID> | jq '[.panel_evidence_summary.evidence[].url]'
```

---

### `banshee pba update [ALERT_IDS]...`

更新一個或多個 Playbook Alerts。ID 可接受 `task:` 前綴或裸 UUID，並支援管道輸入。

| 選項 | 縮寫 | 說明 |
|--------|-------|-------------|
| `--status` | `-s` | 新狀態：`New`、`InProgress`、`Dismissed`、`Resolved` |
| `--reopen` | `-r` | 重新開啟策略（僅適用於 Dismissed/Resolved）：`Never`、`SignificantUpdates` |
| `--priority` | `-p` | 新優先級：`Informational`、`Moderate`、`High` |
| `--comment TEXT` | `-t` | 新增備註 |
| `--assignee TEXT` | `-a` | 重新指派（接受 `uhash:3aXZxdkM12`） |

**有效的狀態／重新開啟組合：** `Dismissed → Never`、`Resolved → Never`、`Resolved → SignificantUpdates`

```bash
# 單筆更新
banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

# 多個 ID
banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

# 透過管道從搜尋結果輸入
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

# 從檔案輸入
banshee pba update -s Dismissed < alerts.txt
cat alerts.txt | banshee pba update -s Dismissed

# 完整範例
banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
```

**回應：** 傳回純文字而非 JSON — 每筆已更新的警報佔一行：`SUCCESS:\n<ALERT_ID>`。請勿將輸出管道至 `jq`。

---

### `banshee pba export`

擷取 `pba search` 所產生警報的完整詳情，並以 JSON 或 CSV 格式輸出。輸入**僅限 stdin** — 請將 `banshee pba search` 的 JSON 物件透過管道傳入；此命令不接受位置引數。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--csv` | | JSON | 以 CSV（固定欄位集）輸出，取代預設的 JSON（完整警報詳情）。 |

```bash
banshee pba search --created 1d -l 10 | banshee pba export > alerts.json
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export --csv > identity_alerts.csv
```

**輸入：** 預期從 stdin 接收 `banshee pba search` 所輸出的 JSON 物件 — 匯出功能讀取 `.data[]`，並要求每筆記錄包含 `playbook_alert_id` 及 `category`（用於驅動類別專屬的資料擷取）。若未透過管道提供輸入（即終端機直接執行），將引發 `BadParameter` 錯誤。

**回應結構（預設）：** 由完整 Playbook Alert 物件組成的 JSON 陣列 — 與 `banshee pba lookup` 傳回的每筆警報結構相同（`playbook_alert_id`、`panel_status`、`panel_evidence_summary`、`panel_log_v2`）。

**回應結構（`--csv`）：** 包含標題列及以下固定欄位的 CSV：`ID`、`Priority`、`Alert Rule`、`Status`、`Created`、`Updated`、`Subject`、`Assignee`、`Assessments`、`Entities`、`Reopen Strategy`、`Onwards Actions`。`Assessments` 與 `Entities` 欄位以 `; ` 連接；欄位值內的逗號均替換為空格。