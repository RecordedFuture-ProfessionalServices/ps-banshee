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