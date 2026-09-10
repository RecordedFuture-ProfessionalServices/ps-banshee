# rules

> 請參閱 [index.md](index.md) 了解驗證、就緒檢查、輸出規範及共用 LLM 注意事項。

### `banshee rules search`

從 Recorded Future 搜尋並下載 Sigma、YARA 及 Snort 偵測規則。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--type` | `-t` | | 規則類型（可重複使用，OR 邏輯）：`sigma`、`yara`、`snort` |
| `--threat-actor-map` | `-T` | | 依您的 Threat Actor Map 中的威脅行為者篩選 |
| `--threat-actor-category` | `-C` | | 依威脅行為者類別篩選（可重複使用，OR 邏輯）。類別包含國家級組織、勒索軟體組織、駭客行動主義者、以財務為動機的行為者等。 |
| `--threat-malware-map` | `-M` | | 依您的 Malware Threat Map 中的惡意軟體篩選 |
| `--org-id TEXT` | `-O` | | MSSP／多組織帳戶的組織 ID（搭配 threat map 使用） |
| `--entity TEXT` | `-e` | | 依 RF 實體 ID 篩選（可重複使用，OR 邏輯）。使用 `banshee entity search` 查詢 ID。接受 MITRE 代碼（例如 `mitre:T1486`）。 |
| `--created-after TEXT` | `-a` | | 相對時間（`1d`、`7d`）或絕對時間（`2024-01-01`） |
| `--created-before TEXT` | `-b` | | 相對或絕對日期 |
| `--updated-after TEXT` | `-u` | | 相對或絕對日期 |
| `--updated-before TEXT` | `-U` | | 相對或絕對日期 |
| `--id TEXT` | `-i` | | 依 Insikt Note 文件 ID 篩選（例如 `doc:lmRPGB`） |
| `--title TEXT` | `-n` | | 對相關 Insikt Note 標題進行全文搜尋 |
| `--limit INTEGER` | `-l` | `10` | 最大結果數（1–1000） |
| `--output-path TEXT` | `-o` | | 將規則儲存至指定目錄（省略則輸出至主控台） |
| `--pretty` | `-p` | | 美化輸出 |

```bash
banshee rules search -t yara -t snort -l 20 -a 3d
banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE
banshee rules search --id doc:0uTafk
banshee rules search --title Ransomware -p
banshee rules search -t yara --output-path .
banshee rules search --threat-actor-map -o fetched_rules
```

**回應結構：** 未使用 `--output-path` 時，回傳一個扁平 JSON 陣列。每個項目代表一則附有相關偵測規則的 Insikt Note：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | Insikt Note 文件 ID（例如 `doc:o6_lui`） |
| `.type` | 規則類型：`sigma`、`yara` 或 `snort` |
| `.title` | Insikt Note 標題 |
| `.description` | Insikt Note 完整描述文字 |
| `.created` | Note 建立時間戳記（ISO 8601） |
| `.updated` | Note 最後更新時間戳記（ISO 8601） |
| `.rules[]` | 規則物件陣列——一則 Note 可能包含多條規則 |

`.rules[]` 項目欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.content` | 原始規則文字（Sigma 為 YAML，YARA／Snort 為純文字） |
| `.file_name` | 儲存規則時建議使用的檔案名稱 |
| `.entities[]` | 規則所參照的實體：`{id, name, type}`（可能包含 `display_name`） |

```bash
# List all sigma rule titles and filenames from the last 7 days
banshee rules search -t sigma -l 50 -a 7d | jq '[.[] | {title, file: .rules[0].file_name}]'

# Extract all MITRE ATT&CK IDs referenced by rules
banshee rules search -t sigma -l 20 | jq '[.[].rules[].entities[] | select(.type == "MitreAttackIdentifier") | .name] | unique'

# Print raw Sigma rule content
banshee rules search --id doc:0uTafk | jq -r '.[0].rules[0].content'
```