# pcap

> 請參閱 [index.md](index.md) 了解認證、就緒檢查、輸出慣例及共用 LLM 說明。

> **前提條件：** `tshark` 必須已安裝且位於 `PATH` 中。在 Banshee 1.2.0 版本中，若 `tshark` 未安裝，`banshee pcap enrich --help` 亦會失敗，請先以 `command -v tshark` 確認。

### `banshee pcap enrich FILE_PATH`

解析 pcap 檔案，擷取 IP 位址與網域名稱，並透過 RF 威脅情報進行擴充分析。預設情況下，僅顯示風險評分超過門檻值（65）的指標。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | 僅顯示高於此評分的指標（1–99） |
| `--threat-hunt` | `-t` | `false` | 同時納入與威脅行為者相關的指標，即使評分低於門檻值（回溯式威脅獵捕） |
| `--pretty` | `-p` | | 美化輸出格式 |

預設 JSON 輸出為一個扁平記錄陣列，欄位包含 `ioc`、`risk_score`、`most_malicious_rule`、`rule_evidence`、`ta_names`、`malwares` 及 `wireshark_query`。

```bash
banshee pcap enrich sandbox.pcap
banshee pcap enrich honeypot-traffic.pcap -r 25 -t -p

# Summarize hits from JSON output
banshee pcap enrich sandbox.pcap -r 25 -t | jq '[.[] | {indicator: .ioc, score: .risk_score, top_rule: .most_malicious_rule, evidence_rules: [(.rule_evidence // [])[].rule]}] | sort_by(-.score)'
```