# list

> 認証、準備確認、出力規則、共有LLMノートについては [index.md](index.md) を参照してください。

### `banshee list create NAME [LIST_TYPE]`

新しいリストを作成します。

| 引数/オプション | デフォルト | 説明 |
|-----------------|---------|-------------|
| `NAME` (必須) | | リストの名前 |
| `LIST_TYPE` | `entity` | 次のいずれか: `entity`, `source`, `text` |
| `--pretty` / `-p` | | 整形出力 |

```bash
banshee list create coolbeans
banshee list create coolsources source -p
```

---

### `banshee list search [NAME]`

名前やタイプでリストを検索します。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `NAME` (任意) | | | リスト名でフィルタリング |
| `--list-type` | `-t` | | 次のいずれか: `entity`, `source`, `text`, `custom`, `ip`, `domain`, `tech_stack`, `industry`, `brand`, `partner`, `industry_peer`, `location`, `supplier`, `vulnerability`, `company`, `hash`, `operation`, `attacker`, `target`, `method`, `executive` |
| `--limit INTEGER` | `-l` | `1000` | 最大結果数（1〜3000） |
| `--pretty` | `-p` | | 整形出力 |

```bash
banshee list search -l 1500 -p
banshee list search -t vulnerability
banshee list search Attacker
banshee list search ernest -t entity -p -l 3
```

**レスポンス形式:** フラットなJSON配列を返します。各アイテムのフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.id` | リストID（例: `report:-19oM7`） |
| `.name` | リスト名 |
| `.type` | リストタイプ: `entity`, `source`, `text` など |
| `.created` | 作成タイムスタンプ（ISO 8601） |
| `.updated` | 最終更新タイムスタンプ（ISO 8601） |
| `.owner_id` | オーナーのuhash ID |
| `.owner_name` | オーナーの表示名 |
| `.owner_organisation_details` | 組織オーナーシップ情報 |

---

### `banshee list info LIST_ID`

リストのメタデータを取得します。

```bash
banshee list info 1b0tFN
banshee list info 1b0tFN -p
```

**レスポンス形式:** 単一のJSONオブジェクトを返します — `list search` のアイテムと同じフィールドセット: `id`, `name`, `type`, `created`, `updated`, `owner_id`, `owner_name`, `organisation_id`, `organisation_name`, `owner_organisation_details`。

---

### `banshee list status LIST_ID`

リストの処理/同期ステータスを取得します。

```bash
banshee list status 1b0tFN
```

**レスポンス形式:** 2つのフィールドを持つ単一のJSONオブジェクトを返します:

| フィールド | 説明 |
|-------|-------------|
| `.status` | 処理ステータス文字列（例: `"ready"`） |
| `.size` | リストに現在登録されているエンティティ数 |

---

### `banshee list entities LIST_ID`

リストに現在登録されているすべてのエンティティを取得します。

```bash
banshee list entities 1b0s1q
```

**レスポンス形式:** フラットなJSON配列を返します。各アイテムのフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.entity.id` | RFエンティティID |
| `.entity.name` | エンティティの表示名 |
| `.entity.type` | エンティティタイプ文字列 |
| `.status` | リスト上のエンティティステータス（例: `"ready"`） |
| `.added` | エンティティが追加されたタイムスタンプ（ISO 8601） |

```bash
# リスト上のすべてのエンティティIDを抽出
banshee list entities report:6P8708 | jq -r '.[].entity.id'

# エンティティ名とタイプを取得
banshee list entities report:6P8708 | jq '[.[] | {name: .entity.name, type: .entity.type}]'
```

---

### `banshee list entries LIST_ID`

リスト上のテキストマッチエントリを取得します（`text`タイプのリスト用）。

```bash
banshee list entries 1b0s1q
```

---

### `banshee list add LIST_ID ENTITY_ID [PROPERTIES]`

リストに単一のエンティティを追加します。

| 引数 | 説明 |
|----------|-------------|
| `LIST_ID` (必須) | リストID |
| `ENTITY_ID` (必須) | RFエンティティID（例: `SoA6SP`）または `name,type` ペア（例: `wannacry,Malware`） |
| `PROPERTIES` (任意) | `annotation=<text>` を使用して、Recorded Futureプラットフォーム上でこのエンティティに表示されるノートを添付します。スペースを含む場合は値を引用符で囲んでください。 |

```bash
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
```

---

### `banshee list bulk-add LIST_ID [ENTITY_INPUT]...`

リストに複数のエンティティを追加します。エンティティID、`name,type` ペア、または `type:value` ペアを受け付けます。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | off | 上書きモード: 入力に含まれるエンティティを保持し、新しいものを追加し、入力に**含まれない**リスト上の既存エンティティを削除します。このオプションなしでは、コマンドは新しいエンティティの追加のみを行い、既存のものを削除しません。 |

**入力形式:**
- RFエンティティID: `SoA6SP`
- 名前 + タイプ: `wannacry,Malware` または `www.duckdns.org,InternetDomainName`
- タイプ付き値: `ip:8.8.8.8`

```bash
banshee list bulk-add report:21YKUC SoA6SP lYNvCK
banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# 上書きモード: リストを指定したエンティティと完全に一致させる（不足分を追加、古いものを削除）
banshee list bulk-add 21YKUC SoA6SP lYNvCK --overwrite

# ファイルから（1行につき1エンティティ）
banshee list bulk-add 21YKUC < entities.txt
cat entities.txt | banshee list bulk-add 21YKUC
```

**レスポンス:** 結果別にグループ化されたプレーンテキスト — `ADDED:`, `REMOVED:`（上書きモードのみ）、`UNCHANGED:` ブロックに影響を受けたエンティティが一覧表示されます。JSONではないため、`jq` にパイプしないでください。

---

### `banshee list remove LIST_ID ENTITY_ID`

リストから単一のエンティティを削除します。

```bash
banshee list remove 1b0s1q lYNvCK
```

---

### `banshee list bulk-remove LIST_ID [ENTITY_INPUT]...`

リストから複数のエンティティを削除します。`bulk-add` と同じ入力形式です。

```bash
banshee list bulk-remove 21YKUC JLHNoH lYNvCK
banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# ファイルから
banshee list bulk-remove 21YKUC < entities.txt
cat entities.txt | banshee list bulk-remove 21YKUC
```

---

### `banshee list copy SOURCE_LIST_ID DESTINATION_LIST_ID`

あるリストから別のリストにエンティティをコピーします。ソースリストのエンティティが読み込まれ、宛先リストに追加されます。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | off | 上書きモード: 両リストに存在するエンティティを保持し、新しいものを追加し、ソースに**含まれない**宛先上のエンティティを削除します。このオプションなしでは、エンティティは宛先に追加されるのみで、削除は行われません。 |

ソースリストが空の場合、`--overwrite` を指定しても、コマンドは宛先を変更せずに終了します。

```bash
banshee list copy 1b0s1q 21YKUC

# 宛先をソースと完全に一致させる（不足分を追加、古いものを削除）
banshee list copy 1b0s1q 21YKUC --overwrite
```

**レスポンス:** 結果別にグループ化されたプレーンテキスト — `ADDED:`, `REMOVED:`（上書きモードのみ）、`UNCHANGED:` ブロックに影響を受けたエンティティが一覧表示されます。JSONではないため、`jq` にパイプしないでください。

---

### `banshee list clear LIST_ID`

リストから**すべて**のエンティティを削除します（破壊的操作 — 注意して使用してください）。テキストマッチエントリはAPIで削除できません。リスト自体は削除されず、エンティティのみが削除されます。

```bash
banshee list clear 1b0s1q
```

**レスポンス:** プレーンテキスト。リストがすでに空の場合は `No entities to remove` を出力し、成功時は `Successfully removed <N> entities` を出力します。削除に失敗した場合は `<N> entities were not removed from the list:` に続いてまだ存在するエンティティが表示されます。JSONではありません。
