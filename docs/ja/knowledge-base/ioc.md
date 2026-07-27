# ioc

> 認証、準備確認、出力規則、共通 LLM に関する注意事項については [index.md](index.md) を参照してください。

### `banshee ioc lookup ENTITY_TYPE [IOC]...`

IOC ごとの詳細なエンリッチメント。インジケーター 1 件につき API 呼び出し 1 回。深いコンテキストが必要な場合に使用してください。

**エンティティタイプ:** `ip`, `domain`, `url`, `hash`, `vulnerability`

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--verbosity INTEGER` | `-v` | `1` | 詳細レベル 1〜5（以下の詳細レベル表を参照） |
| `--ai-insights` | `-a` | | リスクルールの AI 生成サマリーを含める |
| `--pretty` | `-p` | | 整形出力 |

**エンティティタイプ別の詳細レベル:**

| レベル | ip | domain | hash | url | vulnerability |
|-------|----|--------|------|-----|---------------|
| 1 | entity, risk, timestamps | entity, risk, timestamps | entity, hashAlgorithm, risk, timestamps | entity, risk, timestamps | entity, lifecycleStage, risk, timestamps |
| 2 | + intelCard, location | + intelCard | + fileHashes, intelCard | + intelCard | + intelCard |
| 3 | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links |
| 4 | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings | + cvss, cvssv3, cvssv4, enterpriseLists, riskMapping, sightings, threatLists |
| 5 | + dnsPortCert, scanner | レベル 4 と同じ | レベル 4 と同じ | レベル 4 と同じ | + cpe, cpe22uri, nvdDescription, nvdReferences |

```bash
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p

# CSV ファイルからパイプ入力
cat test_ips.csv | banshee ioc lookup ip -p
```

**レスポンスの形式（詳細レベル 1）:** JSON 配列を返します。各アイテムには `entity`、`risk`、`timestamps` が含まれます。詳細レベルが上がると追加されるフィールド: v2 `+intelCard, location`; v3 `+analystNotes, links`; v4 `+enterpriseLists, riskMapping, sightings, threatLists`; v5 `+dnsPortCert, scanner`（ip のみ）。

`.risk.evidenceDetails[]` アイテムのフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.rule` | ルール名の文字列 |
| `.criticality` | 整数 0〜4（脆弱性の場合は 0〜5） |
| `.criticalityLabel` | 人間が読めるラベル（例: `"Unusual"`, `"Malicious"`） |
| `.evidenceString` | 人間が読めるエビデンスの説明 |
| `.mitigationString` | 緩和策のガイダンス（空文字列の場合あり） |
| `.timestamp` | 最新のエビデンスのタイムスタンプ（ISO 8601） |

**jq の応用レシピ:**

```bash
# 最も重大なルール
banshee ioc lookup ip 1.2.3.4 | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'

# トリガーされた全ルール
banshee ioc lookup ip 1.2.3.4 | jq '.[].risk.evidenceDetails[].rule'

# リスクスコア + 最も重大なルール
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | { score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] } ]'

# リスクスコア + 重大度ラベル付きの全ルール
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | { score: .risk.score, rules: [.risk.evidenceDetails[] | {rule, label: .criticalityLabel}] } ]'
```

---

### `banshee ioc bulk-lookup ENTITY_TYPE [IOC]...`

高速な一括エンリッチメント — API 呼び出し 1 回につき最大 1000 件の IOC をバッチ処理。リスクスコアとトリガーされたリスクルールのみを返します。大量のトリアージに使用してください。

| オプション | 説明 |
|--------|-------------|
| `--pretty` / `-p` | 整形出力 |

**レスポンスの形式:** JSON 配列を返します。各アイテムには `entity`（`id`、`name`、`type`）と `risk` が含まれます。注意: `ioc lookup` と異なり `timestamps` キーはありません。

`.risk` フィールド:

| フィールド | 説明 |
|-------|-------------|
| `.risk.score` | 整数のリスクスコア 0〜99 |
| `.risk.level` | 整数の重大度レベル |
| `.risk.context` | リスクドメイン別にグループ化されたコンテキストオブジェクト（`phishing`、`public`、`c2`、`malware`） |
| `.risk.rule.count` | トリガーされたルールの数 |
| `.risk.rule.maxCount` | 最大可能ルール数 |
| `.risk.rule.mostCritical` | 最も重大なルール名 |
| `.risk.rule.summary` | サマリー文字列の配列 |
| `.risk.rule.evidence[]` | トリガーされたルールオブジェクトの配列 |

`.risk.rule.evidence[]` アイテムのフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.rule` | ルール名の文字列 |
| `.level` | 整数の重大度 0〜4 |
| `.description` | HTML タグ付きのエビデンス文字列（エンティティ参照には `<e id=...>` マークアップを使用） |
| `.count` | ヒット数 |
| `.sightings` | サイティング数 |
| `.timestamp` | 最新のエビデンスのタイムスタンプ（ISO 8601） |
| `.mitigation` | 緩和策のガイダンス（空文字列の場合あり） |
| `.type` | ルールタイプの文字列（例: `linkedIntrusion`） |

一括リスクルールのエビデンスは `.risk.rule.evidence[]` 配下にあります。`ioc lookup` が `.risk.evidenceDetails[]` を使用するのとは異なります。

```bash
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877

# ファイルから読み込み（1 行につき IOC 1 件）
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability

# 名前とスコアを抽出
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

# 名前、スコア、トリガーされたルール名を抽出
banshee ioc bulk-lookup ip 92.38.178.133 | jq '[.[] | {ioc: .entity.name, score: .risk.score, rules: [(.risk.rule.evidence // [])[].rule]}]'
```

---

### `banshee ioc search ENTITY_TYPE`

フィルターを使って RF IOC コーパスを検索します。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--limit INTEGER` | `-l` | `5` | 最大件数（1〜1000） |
| `--risk-score TEXT` | `-r` | | リスクスコアの範囲（区間記法） |
| `--risk-rule TEXT` | `-R` | | リスクルール名でフィルター |
| `--verbosity INTEGER` | `-v` | `1` | 詳細レベル 1〜5（`ioc lookup` と同じ表） |
| `--pretty` | `-p` | | 整形出力 |

**リスクスコアの区間記法:**

| 記法 | 意味 |
|--------|---------|
| `'[20,90]'` | 20 ≤ スコア ≤ 90 |
| `'(20,90)'` | 20 < スコア < 90 |
| `'[20,90)'` | 20 ≤ スコア < 90 |
| `'[20,)'` | スコア ≥ 20 |
| `'[,90)'` | スコア < 90 |

デフォルトの JSON 出力はオブジェクト形式です。検索結果は `.data.results[]` 配下にあり、合計件数と返却件数は `.counts` 配下にあります。

```bash
banshee ioc search ip -l 10 -r '(,80]'
banshee ioc search domain -r '[90,)'
banshee ioc search hash -r '[80,81]' -p
banshee ioc search vulnerability --limit 1 -v 3

# 検索結果から IOC 名を抽出
banshee ioc search ip -r '[90,)' -l 100 | jq -r '.data.results[].entity.name'
```

---

### `banshee ioc rules ENTITY_TYPE`

エンティティタイプのリスクルールをオプションのフィルターとともに一覧表示します。

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--freetext TEXT` | `-F` | 名前/説明でルールをフィルター |
| `--mitre-code TEXT` | `-M` | MITRE ATT&CK コードでフィルター（例: `T1587.004`） |
| `--criticality INTEGER` | `-C` | 重大度 0〜5 でフィルター |
| `--pretty` | `-p` | 整形出力 |

**重大度の参照（IP、Domain、URL、Hash）:**

| レベル | ラベル | リスクスコア帯 |
|-------|-------|----------------|
| 4 | Very Malicious | 90〜99 |
| 3 | Malicious | 65〜89 |
| 2 | Suspicious | 25〜64 |
| 1 | Unusual | 5〜24 |
| 0 | No evidence of risk | 0 |

**重大度の参照（Vulnerability）:**

| レベル | ラベル | リスクスコア帯 |
|-------|-------|----------------|
| 5 | Very Critical | 90〜99 |
| 4 | Critical | 80〜89 |
| 3 | High | 65〜79 |
| 2 | Medium | 25〜64 |
| 1 | Low | 5〜24 |
| 0 | No evidence of risk | 0 |

```bash
banshee ioc rules ip
banshee ioc rules domain -p
banshee ioc rules hash -C 3
banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept
```

**レスポンスの形式:** フラットな JSON 配列を返します。各アイテムはリスクルール 1 件を表します:

| フィールド | 説明 |
|-------|-------------|
| `.name` | ルール名の文字列 — この値を `ioc search` や `risklist` コマンドの `--risk-rule` に使用します（例: `"recentActiveCnc"`） |
| `.criticalityLabel` | 人間が読めるラベル（例: `"Very Malicious"`） |
| `.criticality` | 整数の重大度レベル |
| `.description` | ルールの説明文字列 |
| `.categories[]` | `{name, framework}` オブジェクトの配列 — MITRE ATT&CK カテゴリ（例: `{name: "TA0011", framework: "MITRE"}`） |
| `.relatedEntities[]` | このルールが参照する RF エンティティ ID 文字列の配列 |
| `.count` | 現在このルールに一致する IOC の数 |

```bash
# エンティティタイプの全ルール名を一覧表示
banshee ioc rules ip | jq -r '.[].name'

# 重大度 3 以上のルールとその説明を検索
banshee ioc rules ip | jq '[.[] | select(.criticality >= 3) | {name, criticalityLabel, description}]'
```
