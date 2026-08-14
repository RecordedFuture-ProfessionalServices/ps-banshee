# pcap

> 認証、準備確認、出力規則、および共通の LLM に関する注意事項については [index.md](index.md) を参照してください。

> **前提条件:** `tshark` がインストールされており、`PATH` に含まれている必要があります。Banshee 1.2.0 では、`tshark` が存在しない場合 `banshee pcap enrich --help` も失敗するため、事前に `command -v tshark` で確認してください。

### `banshee pcap enrich FILE_PATH`

pcap ファイルを解析し、IP アドレスとドメインを抽出して、RF の脅威インテリジェンスでエンリッチメントします。デフォルトでは、リスクスコアのしきい値（65）を超えるインジケータのみを表示します。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | このスコアを超えるインジケータのみを表示する（1〜99） |
| `--threat-hunt` | `-t` | `false` | スコアのしきい値を下回っていても、脅威アクターに関連するインジケータを含める（遡及的な脅威ハンティング） |
| `--pretty` | `-p` | | 整形出力 |

デフォルトの JSON 出力は、`ioc`、`risk_score`、`most_malicious_rule`、`rule_evidence`、`ta_names`、`malwares`、`wireshark_query` などのフィールドを持つレコードのフラット配列です。

```bash
banshee pcap enrich sandbox.pcap
banshee pcap enrich honeypot-traffic.pcap -r 25 -t -p

# Summarize hits from JSON output
banshee pcap enrich sandbox.pcap -r 25 -t | jq '[.[] | {indicator: .ioc, score: .risk_score, top_rule: .most_malicious_rule, evidence_rules: [(.rule_evidence // [])[].rule]}] | sort_by(-.score)'
```
