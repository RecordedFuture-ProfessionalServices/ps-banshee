# entity

> 認証、準備チェック、出力規則、および共通 LLM ノートについては [index.md](index.md) を参照してください。

### `banshee entity lookup ENTITY_ID`

IDで Recorded Future エンティティを検索します。

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
| `--type` | `-t` | | 1つ以上のエンティティタイプ（繰り返し指定可）。完全なタイプ一覧は以下を参照。 |
| `--limit INTEGER` | `-l` | `100` | 最大件数（1〜100） |
| `--pretty` | `-p` | | 整形出力 |

**主なエンティティタイプ（一部）:** `Malware`、`IpAddress`、`InternetDomainName`、`URL`、`Hash`、`CyberVulnerability`、`CyberThreatActorCategory`、`Organization`、`Person`、`Country`、`MitreAttackIdentifier`、`YaraDetectionRule`、`SnortDetectionRule`、`SigmaDetectionRule`（他 100 種類以上）。

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**レスポンスの形式:** フラットな JSON 配列を返します。各アイテムには正確に 3 つのフィールドがあります:

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
