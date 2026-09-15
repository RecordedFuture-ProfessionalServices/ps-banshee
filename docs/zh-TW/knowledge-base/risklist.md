# risklist

> 請參閱 [index.md](index.md) 以了解身份驗證、就緒檢查、輸出規範及共用 LLM 說明。

### `banshee risklist fetch`

從 RF 下載 risk list（風險清單），或載入本機自訂檔案。

| 選項 | 簡寫 | 說明 |
|--------|-------|-------------|
| `--entity-type` | `-e` | 實體類型：`ip`、`domain`、`url`、`hash`、`vulnerability` |
| `--list-name TEXT` | `-l` | `default`、`large`，或 `banshee ioc rules` 中的任意規則名稱 |
| `--custom-list-path TEXT` | `-c` | 本機 risk list 檔案路徑 |
| `--output-path TEXT` | `-o` | 輸出路徑（預設為目前工作目錄，並自動產生檔名） |
| `--as-json` | `-j` | 將已下載的清單轉換為 JSON（僅限同時指定 `--list-name` 與 `--entity-type` 時使用） |

```bash
banshee risklist fetch -e domain -l default
banshee risklist fetch -c /custom/path/to/list.csv
banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv
```

---

### `banshee risklist create`

從一個或多個 risk rule（風險規則）建立自訂合併 risk list，並可選擇性地依分數篩選。可寫入本機或上傳至 RF Fusion。

| 選項 | 簡寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--entity-type` | `-e` | | 實體類型：`ip`、`domain`、`url`、`hash`、`vulnerability` |
| `--risk-rule TEXT` | `-R` | | 要納入的 risk rule（可重複指定）：`default`、`large`，或 `banshee ioc rules` 中的任意規則名稱 |
| `--risk-score INTEGER` | `-r` | | 最低 risk score（風險分數）門檻（5–99） |
| `--format` | `-f` | `csv` | 輸出格式：`csv`、`edl`、`json` |
| `--output-path TEXT` | `-o` | CWD | 輸出檔案路徑 |
| `--fusion` | `-F` | | 上傳至 RF Fusion（與 `--output-path` 搭配使用，作為 Fusion 目的地路徑） |

**輸出格式：**
- `csv` — 含標頭的逗號分隔格式：`Name, Risk, RiskString, EvidenceDetails`
- `edl` — IOC 值的純文字清單，每行一筆（供防火牆／EDL feed 使用）
- `json` — risk list 項目的完整 JSON 陣列

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

---

### `banshee risklist stat`

顯示 risk list 的元資料——包括其是否存在於 Fusion 中，以及目前的 etag。

| 選項 | 簡寫 | 說明 |
|--------|-------|-------------|
| `--entity-type` | `-e` | 實體類型 |
| `--list-name TEXT` | `-l` | 清單名稱 |
| `--custom-list-path TEXT` | `-c` | 本機 risk list 檔案路徑 |
| `--pretty` | `-p` | 美化輸出 |
| `--count` | `-C` | 顯示 risk list 中的 IOC 數量及 risk score 分布 |

```bash
banshee risklist stat -e ip -l recentValidatedCnc
banshee risklist stat -e domain -l domain_risklist
banshee risklist stat -e ip -l default --count
```

**回應結構：** 回傳單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.name` | 儲存於 Fusion 中的 risk list 名稱（例如 `"recentValidatedCnc_ip_risklist"`） |
| `.exists` | `true`／`false`——該清單是否存在於 RF Fusion 中 |
| `.etag` | 用於快取驗證的 etag 雜湊字串 |
| `.counts` | *（僅限使用 `--count` 時）* 將各 risk score 對應至其 IOC 數量的物件，例如 `{"28": 261110, "65": 6531}` |

**實測說明：** 於 2026-05-01 測試期間，`--custom-list-path /tmp/banshee_smoke_risklist.json` 觸發了 Fusion API 查詢並回傳 `400 Bad Request`；除非需要驗證已知由 Fusion 支援的自訂路徑，否則建議優先使用 `-e`／`-l`。