# ioc

> 請參閱 [index.md](index.md) 了解身份驗證、就緒檢查、輸出慣例及共用 LLM 注意事項。

### `banshee ioc lookup ENTITY_TYPE [IOC]...`

豐富的單一 IOC 資訊增強查詢。每個指標各發出一次 API 呼叫，適用於深度情境分析。

**實體類型：** `ip`、`domain`、`url`、`hash`、`vulnerability`

| 選項 | 短選項 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--verbosity INTEGER` | `-v` | `1` | 詳細程度 1–5（請參閱下方詳細程度表格） |
| `--ai-insights` | `-a` | | 包含 AI 生成的風險規則摘要 |
| `--pretty` | `-p` | | 美化輸出 |

**各實體類型的詳細程度等級：**

| 等級 | ip | domain | hash | url | vulnerability |
|-------|----|--------|------|-----|---------------|
| 1 | entity、risk、timestamps | entity、risk、timestamps | entity、hashAlgorithm、risk、timestamps | entity、risk、timestamps | entity、lifecycleStage、risk、timestamps |
| 2 | + intelCard、location | + intelCard | + fileHashes、intelCard | + intelCard | + intelCard |
| 3 | + analystNotes、links | + analystNotes、links | + analystNotes、links | + analystNotes、links | + analystNotes、links |
| 4 | + enterpriseLists、riskMapping、sightings、threatLists | + enterpriseLists、riskMapping、sightings、threatLists | + enterpriseLists、riskMapping、sightings、threatLists | + enterpriseLists、riskMapping、sightings | + cvss、cvssv3、cvssv4、enterpriseLists、riskMapping、sightings、threatLists |
| 5 | + dnsPortCert、scanner | 同等級 4 | 同等級 4 | 同等級 4 | + cpe、cpe22uri、nvdDescription、nvdReferences |

```bash
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p

# Pipe from CSV file
cat test_ips.csv | banshee ioc lookup ip -p
```

**回應格式（詳細程度 1）：** 返回 JSON 陣列。每個項目包含 `entity`、`risk`、`timestamps`。較高詳細程度等級會新增：v2 `+intelCard, location`；v3 `+analystNotes, links`；v4 `+enterpriseLists, riskMapping, sightings, threatLists`；v5 `+dnsPortCert, scanner`（僅限 ip）。

`.risk.evidenceDetails[]` 項目欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.rule` | 規則名稱字串 |
| `.criticality` | 整數 0–4（漏洞為 0–5） |
| `.criticalityLabel` | 人類可讀標籤（例如 `"Unusual"`、`"Malicious"`） |
| `.evidenceString` | 人類可讀的證據說明 |
| `.mitigationString` | 緩解指引（可能為空字串） |
| `.timestamp` | 最新證據時間戳記（ISO 8601） |

**進階 jq 查詢範例：**

```bash
# Most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'

# All triggered rules
banshee ioc lookup ip 1.2.3.4 | jq '.[].risk.evidenceDetails[].rule'

# Risk score + most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | { score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] } ]'

# Risk score + all rules with criticality labels
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | { score: .risk.score, rules: [.risk.evidenceDetails[] | {rule, label: .criticalityLabel}] } ]'
```

---

### `banshee ioc bulk-lookup ENTITY_TYPE [IOC]...`

快速大量資訊增強查詢——每次 API 呼叫最多批次處理 1000 個 IOC。僅返回風險評分及已觸發的風險規則，適用於大量分類篩選。

| 選項 | 說明 |
|--------|-------------|
| `--pretty` / `-p` | 美化輸出 |

**回應格式：** 返回 JSON 陣列。每個項目包含 `entity`（`id`、`name`、`type`）及 `risk`。注意：不含 `timestamps` 鍵（與 `ioc lookup` 不同）。

`.risk` 欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.risk.score` | 整數風險評分 0–99 |
| `.risk.level` | 整數嚴重性等級 |
| `.risk.context` | 依風險領域分組的情境物件（`phishing`、`public`、`c2`、`malware`） |
| `.risk.rule.count` | 已觸發規則數量 |
| `.risk.rule.maxCount` | 最大可能規則數 |
| `.risk.rule.mostCritical` | 最嚴重規則名稱 |
| `.risk.rule.summary` | 摘要字串陣列 |
| `.risk.rule.evidence[]` | 已觸發規則物件陣列 |

`.risk.rule.evidence[]` 項目欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.rule` | 規則名稱字串 |
| `.level` | 整數嚴重性 0–4 |
| `.description` | 含 HTML 標記的證據字串（實體參照使用 `<e id=...>` 標記） |
| `.count` | 命中次數 |
| `.sightings` | 目擊次數 |
| `.timestamp` | 最新證據時間戳記（ISO 8601） |
| `.mitigation` | 緩解指引（可能為空字串） |
| `.type` | 規則類型字串（例如 `linkedIntrusion`） |

大量查詢的風險規則證據位於 `.risk.rule.evidence[]` 之下；此結構與 `ioc lookup` 使用 `.risk.evidenceDetails[]` 的方式不同。

```bash
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877

# From file (one IOC per line)
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability

# Extract names and scores
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

# Extract names, scores, and triggered rule names
banshee ioc bulk-lookup ip 92.38.178.133 | jq '[.[] | {ioc: .entity.name, score: .risk.score, rules: [(.risk.rule.evidence // [])[].rule]}]'
```

---

### `banshee ioc search ENTITY_TYPE`

使用篩選條件搜尋 RF IOC 資料庫。

| 選項 | 短選項 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--limit INTEGER` | `-l` | `5` | 最大結果數（1–1000） |
| `--risk-score TEXT` | `-r` | | 風險評分範圍（區間表示法） |
| `--risk-rule TEXT` | `-R` | | 依風險規則名稱篩選 |
| `--verbosity INTEGER` | `-v` | `1` | 詳細程度 1–5（同 `ioc lookup` 表格） |
| `--pretty` | `-p` | | 美化輸出 |

**風險評分區間表示法：**

| 語法 | 含義 |
|--------|---------|
| `'[20,90]'` | 20 ≤ score ≤ 90 |
| `'(20,90)'` | 20 < score < 90 |
| `'[20,90)'` | 20 ≤ score < 90 |
| `'[20,)'` | score ≥ 20 |
| `'[,90)'` | score < 90 |

預設 JSON 輸出為物件格式。搜尋結果位於 `.data.results[]` 之下，總數及返回數量位於 `.counts` 之下。

```bash
banshee ioc search ip -l 10 -r '(,80]'
banshee ioc search domain -r '[90,)'
banshee ioc search hash -r '[80,81]' -p
banshee ioc search vulnerability --limit 1 -v 3

# Extract IOC names from search results
banshee ioc search ip -r '[90,)' -l 100 | jq -r '.data.results[].entity.name'
```

---

### `banshee ioc rules ENTITY_TYPE`

列出實體類型的風險規則，並可選擇性套用篩選條件。

| 選項 | 短選項 | 說明 |
|--------|-------|-------------|
| `--freetext TEXT` | `-F` | 依名稱或說明篩選規則 |
| `--mitre-code TEXT` | `-M` | 依 MITRE ATT&CK 代碼篩選（例如 `T1587.004`） |
| `--criticality INTEGER` | `-C` | 依嚴重性 0–5 篩選 |
| `--pretty` | `-p` | 美化輸出 |

**嚴重性參照（IP、Domain、URL、Hash）：**

| 等級 | 標籤 | 風險評分區間 |
|-------|-------|----------------|
| 4 | Very Malicious | 90–99 |
| 3 | Malicious | 65–89 |
| 2 | Suspicious | 25–64 |
| 1 | Unusual | 5–24 |
| 0 | No evidence of risk | 0 |

**嚴重性參照（Vulnerability）：**

| 等級 | 標籤 | 風險評分區間 |
|-------|-------|----------------|
| 5 | Very Critical | 90–99 |
| 4 | Critical | 80–89 |
| 3 | High | 65–79 |
| 2 | Medium | 25–64 |
| 1 | Low | 5–24 |
| 0 | No evidence of risk | 0 |

```bash
banshee ioc rules ip
banshee ioc rules domain -p
banshee ioc rules hash -C 3
banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept
```

**回應格式：** 返回扁平 JSON 陣列。每個項目代表一條風險規則：

| 欄位 | 說明 |
|-------|-------------|
| `.name` | 規則名稱字串——此值可用於 `ioc search` 及 `risklist` 命令的 `--risk-rule` 參數（例如 `"recentActiveCnc"`） |
| `.criticalityLabel` | 人類可讀標籤（例如 `"Very Malicious"`） |
| `.criticality` | 整數嚴重性等級 |
| `.description` | 規則說明字串 |
| `.categories[]` | `{name, framework}` 物件陣列——MITRE ATT&CK 類別（例如 `{name: "TA0011", framework: "MITRE"}`） |
| `.relatedEntities[]` | 此規則所參照的 RF 實體 ID 字串陣列 |
| `.count` | 目前符合此規則的 IOC 數量 |

```bash
# List all rule names for an entity type
banshee ioc rules ip | jq -r '.[].name'

# Find rules above criticality 3 with their descriptions
banshee ioc rules ip | jq '[.[] | select(.criticality >= 3) | {name, criticalityLabel, description}]'
```