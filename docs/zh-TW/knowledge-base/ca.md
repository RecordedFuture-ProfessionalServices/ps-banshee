# ca

> **Classic Alerts** - 基於規則的傳統警報（legacy rule-based alerts）。ID 為 6 個以上字元的不透明短字串（例如 `tybakN`）。若需使用自動化/劇本驅動型警報（ID 為 36 字元 UUID，可附帶 `task:` 前綴，類別包含 `domain_abuse` / `third_party_risk` 等），請改用 [`pba`](pba.md)。
>
> 有關認證、就緒檢查、輸出慣例及共用 LLM 說明，請參閱 [index.md](index.md)。

### `banshee ca lookup ALERT_ID`

依 ID 擷取單一 Classic Alert。

| 引數/選項 | 說明 |
|-----------------|-------------|
| `ALERT_ID`（必填） | Alert ID，例如 `tybakN` |
| `--pretty` / `-p` | 格式化輸出 |

```bash
banshee ca lookup tybakN
banshee ca lookup tybakN -p
```

**回應結構：** 回傳單一 JSON 物件。

| 欄位 | 說明 |
|-------|-------------|
| `.id` | Alert ID |
| `.title` | 警報標題 |
| `.type` | 警報類型字串（例如 `"EVENT"`） |
| `.log.triggered` | 觸發時間戳記（ISO 8601） |
| `.review.status_in_portal` | 人類可讀的狀態：`New`、`Pending`、`Dismissed`、`Resolved` |
| `.review.assignee` | 指派的分析師電子郵件 |
| `.rule.id` | 警報規則 ID |
| `.rule.name` | 警報規則名稱 |
| `.url.portal` | RF 入口網站中的警報直接連結 |
| `.ai_insights.text` | RF AI 生成的摘要字串 |
| `.hits[]` | 觸發警報的文件 |
| `.hits[].id` | 命中文件 ID |
| `.hits[].fragment` | 匹配的文字片段 |
| `.hits[].language` | 語言代碼（例如 `"eng"`） |
| `.hits[].entities[]` | 命中項目中找到的實體：`{id, name, type}` |
| `.hits[].document.title` | 來源文件標題 |
| `.hits[].document.url` | 來源文件 URL |
| `.hits[].document.source` | 來源名稱字串 |
| `.hits[].document.authors` | 作者字串陣列（可能為空） |
| `.triggered_by[]` | 觸發警報的實體/規則（可能為空） |
| `.triggered_by[].reference_id` | 參考文件 ID |
| `.triggered_by[].triggered_by_strings[]` | 人類可讀的觸發說明 |
| `.enriched_entities[]` | 含有 RF 上下文的預先豐富化實體物件（可能為空） |

```bash
# Extract all entities from alert hits for enrichment
banshee ca lookup tybakN | jq '[.hits[].entities[] | {id, name, type}] | unique_by(.id)'

# Get the AI summary
banshee ca lookup tybakN | jq -r '.ai_insights.text'

# Get portal link
banshee ca lookup tybakN | jq -r '.url.portal'
```

---

### `banshee ca search`

使用可選篩選條件搜尋 Classic Alerts。

| 選項 | 短選項 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--triggered TEXT` | `-t` | `1d` | 時間範圍。相對時間（`1d`、`12h`）或絕對區間（`[2024-08-01, 2024-08-14]`）。 |
| `--rule TEXT` | `-r` | | 依警報規則名稱篩選（自由文字，可重複使用）。 |
| `--status` | `-s` | | 下列之一：`New`、`Pending`、`Dismissed`、`Resolved` |
| `--pretty` | `-p` | | 格式化輸出 |

```bash
banshee ca search -t 1d
banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending
banshee ca search -t 12h -p
banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d
banshee ca search -r leaked -t 12h -p
```

**回應結構：** 回傳 JSON 陣列。每個警報物件具有以下頂層欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | Alert ID（例如 `tybakN`） |
| `.title` | 警報標題 |
| `.log.triggered` | 觸發時間戳記（ISO 8601） |
| `.review.status_in_portal` | 人類可讀的狀態：`New`、`Pending`、`Dismissed`、`Resolved` |
| `.review.status` | 內部狀態字串（`no-action` 等）— 不適合用於 jq 篩選 |
| `.rule.name` | 觸發的警報規則名稱 |
| `.rule.id` | 警報規則 ID |

**注意：** `ca search` 的警報記錄沒有頂層 `priority` 欄位。在 jq pipeline 中依狀態篩選時，請使用 `.review.status_in_portal`（而非 `.review.status`）。

```bash
# Extract IDs of New alerts (use status_in_portal for jq filtering)
banshee ca search -t 1d | jq -r '.[] | select(.review.status_in_portal == "New") | .id'

# When using the -s flag, status filtering happens server-side — no jq select needed
banshee ca search -t 1d -s New | jq -r '.[].id'
```

---

### `banshee ca rules [FREETEXT]`

列出所有 Classic Alert 規則，可選擇性地以自由文字篩選。

| 引數/選項 | 說明 |
|-----------------|-------------|
| `FREETEXT`（選填） | 用於篩選規則名稱的搜尋詞 |
| `--pretty` / `-p` | 格式化輸出 |

```bash
banshee ca rules
banshee ca rules -p
```

**回應結構：** 回傳扁平 JSON 陣列。每個項目具有以下欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | 規則 ID（例如 `k_TnPe`） |
| `.title` | 規則名稱 |
| `.enabled` | `true`/`false` — 規則是否啟用 |
| `.priority` | `true` = 此規則產生的警報嚴重性為**高**；`false` = 嚴重性為**資訊性**。若要依優先級分類，請先擷取規則，再透過 `.rule.id` 與警報進行關聯（詳見下方的優先級分類工作流程）。 |
| `.tags` | 標籤字串陣列 |
| `.created` | 建立時間戳記（ISO 8601） |
| `.owner` | 包含 `id` 和 `name` 的物件 — 規則擁有者 |
| `.intelligence_goals` | `{id, name}` 物件陣列 — 相關情報目標 |
| `.notification_settings` | 包含 `email_subscribers` 陣列的物件 |

在建構 pipeline 時，請使用 `.title` 和 `.id`。`.priority` 直接對應警報嚴重性：`true` 為高，`false` 為資訊性。

---

### 優先級分類工作流程

`ca search` 和 `ca lookup` 不會回傳每個警報的嚴重性欄位。若要依嚴重性分類警報，請先擷取規則列表，篩選出 `.priority == true` 的規則，再與警報的 `.rule.id` 值進行交集比對：

```bash
# High-priority alert IDs in the last day
PRIORITY_RULES=$(banshee ca rules | jq -r '.[] | select(.priority == true) | .id' | paste -sd'|' -)
banshee ca search -t 1d | jq --arg rules "$PRIORITY_RULES" -r '.[] | select(.rule.id | test("^(" + $rules + ")$")) | .id'
```

將結果 ID 直接傳送至 `banshee ca update`，以僅對高優先級警報變更狀態。

---

### `banshee ca update [ALERT_IDS]...`

更新一個或多個 Classic Alerts。ID 可作為引數傳入（以空格分隔），或透過 stdin 以管道方式傳入。

| 選項 | 短選項 | 說明 |
|--------|-------|-------------|
| `--status` | `-s` | 新狀態：`New`、`Pending`、`Dismissed`、`Resolved` |
| `--note TEXT` | `-n` | 新增文字備註 |
| `--append` | `-A` | 附加至現有備註而非覆寫 |
| `--assignee TEXT` | `-a` | 重新指派警報。接受 `uhash:3aXZxdkM12` 或 `analyst@acme.com` |

**輸入方式：**

```bash
# Single ID
banshee ca update 8cORlQ -s Resolved

# Multiple IDs (space-separated)
banshee ca update 8cORlQ 8biCIG -s Pending

# Pipe IDs from file
cat alerts.txt | banshee ca update -s Dismissed

# Pipe from search via jq
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"

# stdin redirect
banshee ca update -s Dismissed < alerts.txt
```

**回應：** 回傳純文字而非 JSON — 每個已更新的警報佔一行：`SUCCESS:\n<ALERT_ID>`。請勿傳送至 `jq`。

---

### `banshee ca export`

擷取 `ca search` 產生之警報的完整詳細資料，並以 JSON 或 CSV 格式輸出。輸入**僅限 stdin** — 請以管道方式傳入來自 `banshee ca search` 的 JSON 陣列；此指令無位置引數。

| 選項 | 短選項 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--csv` | | JSON | 以 CSV（固定欄位集）輸出，而非 JSON（完整警報詳細資料）。 |

```bash
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s Pending | banshee ca export --csv > alerts.csv
```

**輸入：** 預期 stdin 為 `banshee ca search` 輸出的 JSON 陣列；每個元素必須包含 `id`。若在無管道輸入的情況下執行（TTY），將引發 `BadParameter` 錯誤。

**回應結構（預設）：** 完整警報物件的 JSON 陣列 — 與 `banshee ca lookup` 回傳的每個警報結構相同（`.id`、`.title`、`.log.triggered`、`.review`、`.rule`、`.hits[]` 等）。

**回應結構（`--csv`）：** 含標題列的 CSV，具有以下固定欄位：`ID`、`Priority`、`Alert Rule`、`Status`、`Created`、`Updated`、`Title`、`Assignee`、`URL`、`Entities`、`Recorded Future AI Insights`。`Priority` 衍生自警報規則（若為優先規則則為 `High`，否則為 `Informational`）；欄位值中的逗號會替換為空格。