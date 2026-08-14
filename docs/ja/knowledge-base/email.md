# email

> 認証、準備確認、出力規則、および共通 LLM に関する注意事項については [index.md](index.md) を参照してください。

### `banshee email enrich FILE_PATH`

EML ファイルを解析し、ヘッダーから IP アドレスを、本文から URL/ドメインを、添付ファイルからハッシュ値を抽出し、RF の脅威インテリジェンスでインジケーターをエンリッチします。デフォルトでは、リスクスコアのしきい値（65）を超えるインジケーターのみを表示します。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | このスコア（0〜99）を超えるインジケーターのみを表示する |
| `--threat-hunt` | `-t` | `false` | スコアのしきい値を下回っていても、脅威アクターに関連するインジケーターも含める |
| `--pretty` | `-p` | | 整形表示 |

デフォルトの JSON 出力は、`ioc`、`type`、`location`、`risk_score`、`first_seen`、`last_seen`、`rule_evidence`、`analyst_notes`、`malwares`、`count_of_analyst_notes`、`ta_names` などのフィールドを持つレコードのフラット配列です。

```bash
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p

# Extract the highest-risk indicators from an enriched EML
banshee email enrich phishing_email.eml -r 1 | jq '[.[] | {ioc, type, location, score: .risk_score, top_rule: (.rule_evidence[0].rule // "")}] | sort_by(-.score)'
```
