# ca

> **Classic Alerts** - レガシーなルールベースのアラートです。IDは6文字以上の短い不透明な文字列です（例: `tybakN`）。自動化/プレイブック駆動のアラート（36文字のUUID IDで、オプションで `task:` プレフィックスが付き、`domain_abuse` / `third_party_risk` などのカテゴリを持つもの）については、代わりに [`pba`](pba.md) を使用してください。
>
> 認証、準備チェック、出力規則、および共通のLLMに関するメモについては、[index.md](index.md) を参照してください。

### `banshee ca lookup ALERT_ID`

IDで単一の Classic Alert を取得します。

| 引数/オプション | 説明 |
|-----------------|------|
| `ALERT_ID` (必須) | アラートID（例: `tybakN`） |
| `--pretty` / `-p` | 整形出力 |

```bash
banshee ca lookup tybakN
banshee ca lookup tybakN -p
```

**レスポンスの形式:** 単一のJSONオブジェクトを返します。

| フィールド | 説明 |
|-----------|------|
| `.id` | アラートID |
| `.title` | アラートタイトル |
| `.type` | アラートタイプ文字列（例: `"EVENT"`） |
| `.log.triggered` | トリガーのタイムスタンプ（ISO 8601） |
| `.review.status_in_portal` | 人間が読めるステータス: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.assignee` | 担当アナリストのメールアドレス |
| `.rule.id` | アラートルールID |
| `.rule.name` | アラートルール名 |
| `.url.portal` | RFポータルのアラートへの直接リンク |
| `.ai_insights.text` | RF AIが生成したサマリー文字列 |
| `.hits[]` | アラートをトリガーしたドキュメント |
| `.hits[].id` | ヒットドキュメントID |
| `.hits[].fragment` | マッチしたテキストスニペット |
| `.hits[].language` | 言語コード（例: `"eng"`） |
| `.hits[].entities[]` | ヒット内で見つかったエンティティ: `{id, name, type}` |
| `.hits[].document.title` | ソースドキュメントのタイトル |
| `.hits[].document.url` | ソースドキュメントのURL |
| `.hits[].document.source` | ソース名の文字列 |
| `.hits[].document.authors` | 著者文字列の配列（空の場合あり） |
| `.triggered_by[]` | アラートをトリガーしたエンティティ/ルール（空の場合あり） |
| `.triggered_by[].reference_id` | 参照ドキュメントID |
| `.triggered_by[].triggered_by_strings[]` | 人間が読めるトリガーの説明 |
| `.enriched_entities[]` | RFコンテキスト付きの事前エンリッチされたエンティティオブジェクト（空の場合あり） |

```bash
# Extract all entities from alert hits for enrichment
banshee ca lookup tybakN | jq '[.hits[].entities[] | {id, name, type}] | unique_by(.id)'

# Get the AI summary
banshee ca lookup tybakN | jq -r '.ai_insights.text'

# Get portal link
banshee ca lookup tybakN | jq -r '.url.portal'
```

---

### `banshee ca search`

オプションのフィルターを使用して Classic Alerts を検索します。

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--triggered TEXT` | `-t` | `1d` | 時間範囲。相対指定（`1d`, `12h`）または絶対間隔（`[2024-08-01, 2024-08-14]`）。 |
| `--rule TEXT` | `-r` | | アラートルール名でフィルター（フリーテキスト、繰り返し可）。 |
| `--status` | `-s` | | 次のいずれか: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--pretty` | `-p` | | 整形出力 |

```bash
banshee ca search -t 1d
banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending
banshee ca search -t 12h -p
banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d
banshee ca search -r leaked -t 12h -p
```

**レスポンスの形式:** JSON配列を返します。各アラートオブジェクトには以下のトップレベルフィールドがあります:

| フィールド | 説明 |
|-----------|------|
| `.id` | アラートID（例: `tybakN`） |
| `.title` | アラートタイトル |
| `.log.triggered` | トリガーのタイムスタンプ（ISO 8601） |
| `.review.status_in_portal` | 人間が読めるステータス: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.status` | 内部ステータス文字列（`no-action` など）— jqフィルタリングには有用でない |
| `.rule.name` | 発火したアラートルールの名前 |
| `.rule.id` | アラートルールID |

**注意:** `ca search` のアラートレコードにはトップレベルの `priority` フィールドがありません。jqパイプラインでステータスをフィルタリングする場合は、`.review.status`（ではなく）`.review.status_in_portal` を使用してください。

```bash
# Extract IDs of New alerts (use status_in_portal for jq filtering)
banshee ca search -t 1d | jq -r '.[] | select(.review.status_in_portal == "New") | .id'

# When using the -s flag, status filtering happens server-side — no jq select needed
banshee ca search -t 1d -s New | jq -r '.[].id'
```

---

### `banshee ca rules [FREETEXT]`

すべての Classic Alert ルールを一覧表示し、オプションでフリーテキストでフィルタリングします。

| 引数/オプション | 説明 |
|-----------------|------|
| `FREETEXT` (省略可) | ルール名をフィルタリングする検索語 |
| `--pretty` / `-p` | 整形出力 |

```bash
banshee ca rules
banshee ca rules -p
```

**レスポンスの形式:** フラットなJSON配列を返します。各アイテムには以下のフィールドがあります:

| フィールド | 説明 |
|-----------|------|
| `.id` | ルールID（例: `k_TnPe`） |
| `.title` | ルール名 |
| `.enabled` | `true`/`false` — ルールが有効かどうか |
| `.priority` | `true` = このルールからのアラートは重大度 **High**; `false` = 重大度 **Informational**。優先度でトリアージするには、まずルールを取得し、`.rule.id` でアラートに結合します（下記の優先度トリアージワークフローを参照）。 |
| `.tags` | タグ文字列の配列 |
| `.created` | 作成タイムスタンプ（ISO 8601） |
| `.owner` | `id` と `name` を持つオブジェクト — ルールのオーナー |
| `.intelligence_goals` | `{id, name}` オブジェクトの配列 — 関連するインテリジェンス目標 |
| `.notification_settings` | `email_subscribers` 配列を持つオブジェクト |

パイプラインを構築する際は `.title` と `.id` を使用してください。`.priority` はアラートの重大度に直接対応します: `true` は High、`false` は Informational です。

---

### 優先度トリアージワークフロー

`ca search` と `ca lookup` はアラートごとの重大度フィールドを返しません。重大度でアラートをトリアージするには、まずルールリストを取得し、`.priority == true` のルールにフィルタリングして、アラートの `.rule.id` の値と照合します:

```bash
# High-priority alert IDs in the last day
PRIORITY_RULES=$(banshee ca rules | jq -r '.[] | select(.priority == true) | .id' | paste -sd'|' -)
banshee ca search -t 1d | jq --arg rules "$PRIORITY_RULES" -r '.[] | select(.rule.id | test("^(" + $rules + ")$")) | .id'
```

結果のIDをそのまま `banshee ca update` にパイプして、高優先度のアラートのみのステータスを変更します。

---

### `banshee ca update [ALERT_IDS]...`

1つまたは複数の Classic Alerts を更新します。IDは引数としてスペース区切りで渡すか、stdinからパイプで渡すことができます。

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--status` | `-s` | 新しいステータス: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--note TEXT` | `-n` | テキストメモを追加 |
| `--append` | `-A` | 上書きの代わりに既存のメモに追記 |
| `--assignee TEXT` | `-a` | アラートを再割り当て。`uhash:3aXZxdkM12` または `analyst@acme.com` を受け付けます |

**入力方法:**

```bash
# Single ID
banshee ca update 8cORlQ -s Resolved

# Multiple IDs (space-separated)
banshee ca update 8cORlQ 8biCIG -s Pending

# Pipe IDs from file
cat alerts.txt | banshee ca update -s Dismissed

# Pipe from search via jq
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"

# stdin redirect
banshee ca update -s Dismissed < alerts.txt
```

**レスポンス:** JSONではなくプレーンテキストを返します — 更新されたアラートごとに1行: `SUCCESS:\n<ALERT_ID>`。`jq` にパイプしないでください。

---

### `banshee ca export`

`ca search` で生成されたアラートの完全なアラート詳細を取得し、JSONまたはCSVとして出力します。入力は**stdinのみ**です — `banshee ca search` からJSON配列をパイプしてください。位置引数はありません。

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--csv` | | JSON | JSONの代わりにCSV（固定カラムセット）として出力します（完全なアラート詳細）。 |

```bash
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s Pending | banshee ca export --csv > alerts.csv
```

**入力:** stdinで `banshee ca search` が出力するJSON配列を受け取ります。すべての要素に `id` が必要です。パイプ入力なしで実行した場合（TTY）、`BadParameter` エラーが発生します。

**レスポンスの形式（デフォルト）:** 完全なアラートオブジェクトのJSON配列 — `banshee ca lookup` が返すものと同じアラートごとの構造（`.id`, `.title`, `.log.triggered`, `.review`, `.rule`, `.hits[]` など）。

**レスポンスの形式（`--csv`）:** ヘッダー行と以下の固定カラムを持つCSV: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Title`, `Assignee`, `URL`, `Entities`, `Recorded Future AI Insights`。`Priority` はアラートルールから導出されます（ルールが優先度ルールの場合は `High`、それ以外は `Informational`）。フィールド値内のカンマはスペースに置換されます。
