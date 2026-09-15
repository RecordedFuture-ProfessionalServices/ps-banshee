# email

> 請參閱 [index.md](index.md) 以了解驗證、就緒性檢查、輸出慣例及共用 LLM 注意事項。

### `banshee email enrich FILE_PATH`

解析 EML 檔案，從標頭中擷取 IP 位址、從本文中擷取 URL/網域，以及附件雜湊值，然後使用 RF 威脅情報對這些指標進行豐富化處理。預設情況下，僅顯示風險分數超過閾值（65）的指標。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | 僅顯示分數高於此值的指標（0–99） |
| `--threat-hunt` | `-t` | `false` | 同時包含與威脅行為者相關的指標，即使分數低於閾值 |
| `--pretty` | `-p` | | 美化輸出 |

預設 JSON 輸出為一個扁平記錄陣列，欄位包含 `ioc`、`type`、`location`、`risk_score`、`first_seen`、`last_seen`、`rule_evidence`、`analyst_notes`、`malwares`、`count_of_analyst_notes` 及 `ta_names`。

```bash
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p

# Extract the highest-risk indicators from an enriched EML
banshee email enrich phishing_email.eml -r 1 | jq '[.[] | {ioc, type, location, score: .risk_score, top_rule: (.rule_evidence[0].rule // "")}] | sort_by(-.score)'
```