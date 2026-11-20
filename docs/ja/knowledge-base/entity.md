# entity

> 認証、準備チェック、出力規則、および共通 LLM ノートについては [index.md](index.md) を参照してください。

### `banshee entity lookup ENTITY_ID`

ID で Recorded Future エンティティを検索します。

| 引数/オプション | 説明 |
|-----------------|-------------|
| `ENTITY_ID` (必須) | RF エンティティ ID（例: `qf0H03`） |
| `--pretty` / `-p` | 整形出力 |

```bash
banshee entity lookup qf0H03
banshee entity lookup qf0H03 -p
```

**レスポンスの形式:** トップレベルキー `id`、`type`、`attributes` を持つ単一の JSON オブジェクトを返します。エンティティ名はトップレベルではなく `.attributes.name` の下にネストされています。

```bash
# Correct jq to extract id, type, and name:
banshee entity lookup qf0H03 | jq '{id, type, name: .attributes.name}'
```

---

### `banshee entity search NAME`

名前でエンティティを検索します。オプションでタイプによるフィルタリングが可能です。

| 引数/オプション | 短縮形 | デフォルト | 説明 |
|-----------------|-------|---------|-------------|
| `NAME` (必須) | | | 検索するエンティティ名 |
| `--type` | `-t` | | 1 つ以上のエンティティタイプ（繰り返し指定可）。完全なタイプ一覧は以下を参照。 |
| `--limit INTEGER` | `-l` | `100` | 最大件数（1〜100） |
| `--pretty` | `-p` | | 整形出力 |

**主なエンティティタイプ（一部）:** `Malware`、`IpAddress`、`InternetDomainName`、`URL`、`Hash`、`CyberVulnerability`、`CyberThreatActorCategory`、`Organization`、`Person`、`Country`、`MitreAttackIdentifier`、`YaraDetectionRule`、`SnortDetectionRule`、`SigmaDetectionRule`（他 100 種類以上）。

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**レスポンスの形式:** フラットな JSON 配列を返します。各アイテムには正確に 3 つのフィールドがあります。

| フィールド | 説明 |
|-------|-------------|
| `.id` | RF エンティティ ID（例: `SoA6SP`） |
| `.name` | エンティティの表示名 |
| `.type` | エンティティタイプ文字列（例: `Malware`、`InternetDomainName`） |

```bash
# Extract all IDs matching a name
banshee entity search "Cobalt Strike" -t Malware | jq -r '.[].id'

# Build a lookup table of id → name
banshee entity search wannacry | jq '[.[] | {(.id): .name}] | add'
```


---

### `banshee entity links ENTITY_ID...`

1 つ以上のエンティティにリンクされたエンティティ（IOC（Indicators of Compromise）、検知ルール、マルウェア、TTP（戦術・技術・手順）、脅威アクター）を取得します。エンティティ ID は Recorded Future のエンティティ ID（例: `banshee entity search` で取得したもの）であり、エンティティ名ではありません。リンクされた IOC は、`--skip-enrichment` が指定されない限り SOAR 経由でエンリッチメントされます。

エンティティ ID は空白区切りの引数として渡すか、stdin からパイプまたはリダイレクト（1 行に 1 つ）で入力できます。サブコマンド名（例: `links search`）を追加しないでください。そのようなサブコマンドは存在せず、余分な単語はエンティティ ID として扱われます。

| 引数/オプション | 短縮形 | デフォルト | 説明 |
|-----------------|-------|---------|-------------|
| `ENTITY_ID...` | | stdin | 1 つ以上のエンティティ ID |
| `--type TEXT` | `-t` | | 返すエンティティのタイプ（繰り返し指定可） |
| `--source [Technical\|Insikt]` | `-s` | | 返すリンクのソース |
| `--sections TEXT` | `-S` | | リンクタイプでフィルタリング（例: `'Indicators and Detection Rules'`）。繰り返し指定可 |
| `--timeframe TEXT` | `-T` | | リンクが作成されたタイムフレーム（例: `-1d`、最大 `-90d`） |
| `--events TEXT` | `-e` | | イベントタイプでフィルタリング（例: `type:MalwareAnalysis`）。繰り返し指定可 |
| `--connected-entities TEXT` | `-c` | | 指定したエンティティにも接続されているエンティティのみ返す。繰り返し指定可 |
| `--limit INTEGER` | `-l` | | タイプごとに返すエンティティの最大件数（1〜1,000,000） |
| `--small` | | | イベントタイプごとに参照 10 件・Insikt Note 10 件を検索 |
| `--large` | | | イベントタイプごとに参照 100 件・Insikt Note 500 件を検索 |
| `--skip-enrichment` | | | リンクされた IOC の追加エンリッチメントをスキップ |
| `--pretty` | `-p` | | 整形出力 |

`--small` と `--large` は同時に指定できません。どちらも指定しない場合、中間スコープが使用されます。

**レスポンスの形式:** 入力エンティティごとに 1 つのオブジェクトを含む JSON 配列を返します。各オブジェクトには、検索対象の `entity` とその `links` が含まれます。各リンクにはリンクされた IOC の SOAR エンリッチメントを保持する `enrichment` フィールドがあり、非 IOC リンク・未エンリッチメント IOC・`--skip-enrichment` 使用時は `null` になります。SOAR エンリッチメントが失敗した場合は、stderr にその旨が出力され、エンリッチメントはスキップされます。

整形出力（stderr に出力）では、エンティティごとにリンクされた IOC（リスクスコア、主要リスクルール、インテリジェンスカードへのリンクを含む）、TTP、マルウェア、脅威アクターのテーブルが表示されます。各テーブルは最大 20 行に制限されます。整形モードでの IOC エンリッチメントも、タイプごとに 20 件の IOC に制限されます。

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