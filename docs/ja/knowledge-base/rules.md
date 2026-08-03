# rules

> 認証、準備確認、出力規則、および共有 LLM に関する注意事項については [index.md](index.md) を参照してください。

### `banshee rules search`

Recorded Future から Sigma、YARA、Snort の検知ルールを検索してダウンロードします。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--type` | `-t` | | ルールの種類（繰り返し指定可、OR 論理）：`sigma`、`yara`、`snort` |
| `--threat-actor-map` | `-T` | | 脅威アクターマップ内のアクターで絞り込む |
| `--threat-actor-category` | `-C` | | 脅威アクターのカテゴリで絞り込む（繰り返し指定可、OR 論理）。カテゴリには国家系グループ、ランサムウェアグループ、ハクティビスト、金銭目的のアクターなどが含まれます。 |
| `--threat-malware-map` | `-M` | | マルウェア脅威マップ内のマルウェアで絞り込む |
| `--org-id TEXT` | `-O` | | MSSP/マルチ組織アカウントの組織 ID（脅威マップと併用） |
| `--entity TEXT` | `-e` | | RF エンティティ ID で絞り込む（繰り返し指定可、OR 論理）。ID の検索には `banshee entity search` を使用してください。MITRE コードも受け付けます（例：`mitre:T1486`）。 |
| `--created-after TEXT` | `-a` | | 相対指定（`1d`、`7d`）または絶対指定（`2024-01-01`） |
| `--created-before TEXT` | `-b` | | 相対または絶対日付 |
| `--updated-after TEXT` | `-u` | | 相対または絶対日付 |
| `--updated-before TEXT` | `-U` | | 相対または絶対日付 |
| `--id TEXT` | `-i` | | Insikt Note のドキュメント ID で絞り込む（例：`doc:lmRPGB`） |
| `--title TEXT` | `-n` | | 関連する Insikt Note のタイトルをフリーテキスト検索 |
| `--limit INTEGER` | `-l` | `10` | 最大件数（1〜1000） |
| `--output-path TEXT` | `-o` | | ルールをディレクトリに保存する（省略するとコンソールに出力） |
| `--pretty` | `-p` | | 整形出力 |

```bash
banshee rules search -t yara -t snort -l 20 -a 3d
banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE
banshee rules search --id doc:0uTafk
banshee rules search --title Ransomware -p
banshee rules search -t yara --output-path .
banshee rules search --threat-actor-map -o fetched_rules
```

**レスポンスの形式：** フラットな JSON 配列を返します（`--output-path` を使用しない場合）。各アイテムは、関連する検知ルールを持つ Insikt Note を表します：

| フィールド | 説明 |
|-------|-------------|
| `.id` | Insikt Note のドキュメント ID（例：`doc:o6_lui`） |
| `.type` | ルールの種類：`sigma`、`yara`、または `snort` |
| `.title` | Insikt Note のタイトル |
| `.description` | Insikt Note の全文説明テキスト |
| `.created` | Note の作成タイムスタンプ（ISO 8601） |
| `.updated` | Note の最終更新タイムスタンプ（ISO 8601） |
| `.rules[]` | ルールオブジェクトの配列 — 1 つの Note に複数のルールが含まれる場合があります |

`.rules[]` アイテムのフィールド：

| フィールド | 説明 |
|-------|-------------|
| `.content` | ルールの生テキスト（Sigma の場合は YAML、YARA/Snort の場合はプレーンテキスト） |
| `.file_name` | ルールを保存する際に推奨されるファイル名 |
| `.entities[]` | ルールが参照するエンティティ：`{id, name, type}`（`display_name` を含む場合あり） |

```bash
# 直近 7 日間の全 sigma ルールのタイトルとファイル名を一覧表示
banshee rules search -t sigma -l 50 -a 7d | jq '[.[] | {title, file: .rules[0].file_name}]'

# ルールが参照する全 MITRE ATT&CK ID を抽出
banshee rules search -t sigma -l 20 | jq '[.[].rules[].entities[] | select(.type == "MitreAttackIdentifier") | .name] | unique'

# Sigma ルールの生コンテンツを表示
banshee rules search --id doc:0uTafk | jq -r '.[0].rules[0].content'
```
