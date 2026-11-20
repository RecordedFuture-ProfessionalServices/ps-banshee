# entity

> 有關身份驗證、就緒檢查、輸出規範及共用 LLM 注意事項，請參閱 [index.md](index.md)。

### `banshee entity lookup ENTITY_ID`

依 ID 查詢 Recorded Future 實體。

| 引數/選項 | 說明 |
|-----------------|-------------|
| `ENTITY_ID`（必填） | RF 實體 ID，例如 `qf0H03` |
| `--pretty` / `-p` | 格式化輸出 |

```bash
banshee entity lookup qf0H03
banshee entity lookup qf0H03 -p
```

**回應結構：** 回傳單一 JSON 物件，頂層鍵為 `id`、`type` 及 `attributes`。實體名稱位於 `.attributes.name` 之下，而非頂層。

```bash
# Correct jq to extract id, type, and name:
banshee entity lookup qf0H03 | jq '{id, type, name: .attributes.name}'
```

---

### `banshee entity search NAME`

依名稱搜尋實體，可選擇依類型篩選。

| 引數/選項 | 縮寫 | 預設值 | 說明 |
|-----------------|-------|---------|-------------|
| `NAME`（必填） | | | 欲搜尋的實體名稱 |
| `--type` | `-t` | | 一或多個實體類型（可重複指定）。完整類型清單請見下方。 |
| `--limit INTEGER` | `-l` | `100` | 最大結果數（1–100） |
| `--pretty` | `-p` | | 格式化輸出 |

**常見實體類型（部分清單）：** `Malware`、`IpAddress`、`InternetDomainName`、`URL`、`Hash`、`CyberVulnerability`、`CyberThreatActorCategory`、`Organization`、`Person`、`Country`、`MitreAttackIdentifier`、`YaraDetectionRule`、`SnortDetectionRule`、`SigmaDetectionRule`（以及 100 種以上其他類型）。

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**回應結構：** 回傳扁平 JSON 陣列。每個項目包含以下三個欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | RF 實體 ID（例如 `SoA6SP`） |
| `.name` | 實體顯示名稱 |
| `.type` | 實體類型字串（例如 `Malware`、`InternetDomainName`） |

```bash
# Extract all IDs matching a name
banshee entity search "Cobalt Strike" -t Malware | jq -r '.[].id'

# Build a lookup table of id → name
banshee entity search wannacry | jq '[.[] | {(.id): .name}] | add'
```


---

### `banshee entity links ENTITY_ID...`

擷取與一或多個實體相關聯的實體（IOC（入侵指標）、偵測規則、惡意軟體、TTP（戰術、技術與程序）、威脅行為者）。實體 ID 為 Recorded Future 實體 ID（例如來自 `banshee entity search`），而非實體名稱。除非指定 `--skip-enrichment`，否則已關聯的 IOC 將透過 SOAR 進行豐富化處理。

實體 ID 可以空白分隔的引數形式傳入，亦可透過管道或重新導向從 stdin 逐行輸入。請勿加入子命令字詞（例如 `links search`）：此子命令不存在，任何多餘的字詞均會被視為實體 ID。

| 引數/選項 | 縮寫 | 預設值 | 說明 |
|-----------------|-------|---------|-------------|
| `ENTITY_ID...` | | stdin | 一或多個實體 ID |
| `--type TEXT` | `-t` | | 欲回傳的實體類型，可重複指定 |
| `--source [Technical\|Insikt]` | `-s` | | 欲回傳關聯的來源 |
| `--sections TEXT` | `-S` | | 依關聯類型篩選，例如 `'Indicators and Detection Rules'`，可重複指定 |
| `--timeframe TEXT` | `-T` | | 關聯建立的時間範圍，例如 `-1d`（最長 `-90d`） |
| `--events TEXT` | `-e` | | 依事件類型篩選，例如 `type:MalwareAnalysis`，可重複指定 |
| `--connected-entities TEXT` | `-c` | | 僅回傳同時與這些實體相連的實體，可重複指定 |
| `--limit INTEGER` | `-l` | | 每種類型回傳的最大實體數（1–1,000,000） |
| `--small` | | | 每種事件類型搜尋 10 筆參考資料及 10 筆 Insikt Notes |
| `--large` | | | 每種事件類型搜尋 100 筆參考資料及 500 筆 Insikt Notes |
| `--skip-enrichment` | | | 略過已關聯 IOC 的額外豐富化處理 |
| `--pretty` | `-p` | | 格式化輸出 |

`--small` 與 `--large` 互斥；若兩者均未指定，則使用中等範圍。

**回應結構：** 回傳 JSON 陣列，每個輸入實體對應一個物件。每個物件包含所查詢的 `entity` 及其 `links`。每筆關聯均帶有 `enrichment` 欄位，存放已關聯 IOC 的 SOAR 豐富化結果；若為非 IOC 關聯、未豐富化的 IOC，或使用 `--skip-enrichment` 時，則為 `null`。若 SOAR 豐富化失敗，將於 stderr 輸出提示訊息並略過豐富化處理。

格式化輸出（列印至 stderr）會以每個實體為單位，顯示已關聯 IOC（含風險分數、最高風險規則及情報卡連結）、TTP、惡意軟體及威脅行為者的表格，每張表格最多顯示 20 列。格式化模式下的 IOC 豐富化同樣限制為每種類型最多 20 筆。

```bash
banshee entity links BUl6R5r
banshee entity links BUl6R5r -T -10d --small -p
banshee entity links BUl6R5r sIG7Rn -T -10d --large > links.json

# Skip enrichment for faster results
banshee entity links BUl6R5r --skip-enrichment

# Entity IDs from a file or pipe
banshee entity links -T -1d < link_entities.txt
cat link_entities.txt | banshee entity links -T -1d --large > links_out.json

# Find an entity ID first, then search its links
banshee entity search wannacry -t Malware -l 1 | jq -r '.[].id' | banshee entity links --small
```


---