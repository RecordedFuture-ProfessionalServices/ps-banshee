# pba

> **Playbook Alerts** — 自動化によるアラートです。IDは36文字のUUIDで、`task:` プレフィックスは省略可能です（例：`d144a9ec-90e6-40fe-89b0-d85ed65d3e9c` または `task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c`）。PBA専用カテゴリー：`domain_abuse`、`cyber_vulnerability`、`third_party_risk`、`code_repo_leakage`、`identity_novel_exposures`、`geopolitics_facility`、`malware_report`。レガシーなルールベースのアラート（短い不透明なID）については、[`ca`](ca.md) を使用してください。
>
> 認証、準備確認、出力規則、および共有LLMノートについては [index.md](index.md) を参照してください。

### `banshee pba search`

豊富なフィルターオプションでPlaybook Alertsを検索します。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--created TEXT` | `-C` | | 作成日でフィルター（例：`1d`、`7d`） |
| `--updated TEXT` | `-u` | | 更新日でフィルター |
| `--category` | `-c` | all | 1つまたは複数のカテゴリー（繰り返し可）：`domain_abuse`、`cyber_vulnerability`、`third_party_risk`、`code_repo_leakage`、`identity_novel_exposures`、`geopolitics_facility`、`malware_report` |
| `--entity TEXT` | `-e` | | 関連エンティティでフィルター（繰り返し可） |
| `--priority` | `-P` | all | `Informational`、`Moderate`、`High`（繰り返し可） |
| `--status` | `-s` | all | `New`、`InProgress`、`Dismissed`、`Resolved`（繰り返し可） |
| `--org-id TEXT` | `-o` | all | 所有組織IDでフィルター（繰り返し可）。10文字のIDまたは16文字の `uhash:` 形式を受け付けます |
| `--limit INTEGER` | `-l` | `100` | 最大件数（1〜10000） |
| `--pretty` | `-p` | | プリティプリント |

**レスポンスの形式：** 3つのトップレベルキーを持つJSONオブジェクトを返します：`.data`（アラートレコードの配列）、`.counts`（`{returned, total}`）、`.status`（リクエストステータスオブジェクト：`{status_code, status_message}`）。アラートレコードは `.data[]` の下にあり、フィールドは次のとおりです：`playbook_alert_id`、`alert_rule`（`{id, label, name}`）、`category`、`priority`、`status`、`title`、`created`、`updated`、`actions_taken`、`owner_organisation_details`。

```bash
banshee pba search --created 1d
banshee pba search -C 1d -u 1d -p
banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse
banshee pba search --updated 7d --category domain_abuse --pretty
banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New
banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d
banshee pba search -o 69sKLfTGsS -o uhash:5zQaSyRpA1 -C 7d -P High
```

---

### `banshee pba lookup ALERT_ID`

IDで単一のPlaybook Alertを取得します。`task:` プレフィックスの有無にかかわらず36文字のUUIDを受け付けます — CLIはベアUUIDに自動的に `task:` を付加します。

```bash
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p
```

**レスポンスの形式：** 4つのトップレベルキーを持つ単一のJSONオブジェクトを返します：`playbook_alert_id`、`panel_status`、`panel_evidence_summary`、`panel_log_v2`。

**`.panel_status`** — アラートのメタデータと現在の状態：

| フィールド | 説明 |
|-------|-------------|
| `.panel_status.status` | 現在のステータス：`New`、`InProgress`、`Dismissed`、`Resolved` |
| `.panel_status.priority` | 優先度：`Informational`、`Moderate`、`High` |
| `.panel_status.case_rule_label` | 人間が読めるルール名（例：`"Data Leakage on Code Repository"`） |
| `.panel_status.entity_id` | 主要対象のRFエンティティID（例：`"url:https://..."`） |
| `.panel_status.entity_name` | 主要エンティティ名 |
| `.panel_status.risk_score` | RFリスクスコア（整数） |
| `.panel_status.targets[]` | `{name}` オブジェクトの配列 — 対象または影響を受けるエンティティ |
| `.panel_status.actions_taken[]` | アラートに既に記録されたアクション |
| `.panel_status.created` | 作成タイムスタンプ（ISO 8601） |
| `.panel_status.updated` | 最終更新タイムスタンプ（ISO 8601） |

**`.panel_evidence_summary`** — エビデンスの詳細。構造はアラートカテゴリーによって異なります。`code_repo_leakage` の場合：

| フィールド | 説明 |
|-------|-------------|
| `.panel_evidence_summary.repository.name` | リポジトリURL |
| `.panel_evidence_summary.repository.owner.name` | リポジトリオーナーのログイン名 |
| `.panel_evidence_summary.evidence[]` | エビデンスアイテムの配列 |
| `.panel_evidence_summary.evidence[].url` | 露出コンテンツのソースURL |
| `.panel_evidence_summary.evidence[].content` | 露出コンテンツのスニペット |
| `.panel_evidence_summary.evidence[].assessments[]` | アセスメントオブジェクト：`{id, title, value}` |
| `.panel_evidence_summary.evidence[].targets[]` | ターゲットエンティティ：`{name}` |
| `.panel_evidence_summary.evidence[].published` | 公開タイムスタンプ |

```bash
# Summary: entity, rule, status
banshee pba lookup task:<ID> | jq '{entity: .panel_status.entity_name, rule: .panel_status.case_rule_label, status: .panel_status.status, priority: .panel_status.priority}'

# Extract evidence URLs (code_repo_leakage)
banshee pba lookup task:<ID> | jq '[.panel_evidence_summary.evidence[].url]'
```

---

### `banshee pba update [ALERT_IDS]...`

1つまたは複数のPlaybook Alertsを更新します。IDは `task:` プレフィックスまたはベアUUIDを受け付けます。パイプ経由での入力も可能です。

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--status` | `-s` | 新しいステータス：`New`、`InProgress`、`Dismissed`、`Resolved` |
| `--reopen` | `-r` | 再オープン戦略（DismissedまたはResolvedのみ）：`Never`、`SignificantUpdates` |
| `--priority` | `-p` | 新しい優先度：`Informational`、`Moderate`、`High` |
| `--comment TEXT` | `-t` | コメントを追加 |
| `--assignee TEXT` | `-a` | 再割り当て（`uhash:3aXZxdkM12` を受け付けます） |

**有効なステータス/再オープンの組み合わせ：** `Dismissed → Never`、`Resolved → Never`、`Resolved → SignificantUpdates`

```bash
# Single update
banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

# Multiple IDs
banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

# Pipe from search
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

# From file
banshee pba update -s Dismissed < alerts.txt
cat alerts.txt | banshee pba update -s Dismissed

# Full example
banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
```

**レスポンス：** JSONではなくプレーンテキストを返します — 更新されたアラートごとに1行：`SUCCESS:\n<ALERT_ID>`。`jq` にパイプしないでください。

---

### `banshee pba export`

`pba search` で生成されたアラートの完全な詳細を取得し、JSONまたはCSVとして出力します。入力は **標準入力のみ** — `banshee pba search` からJSONオブジェクトをパイプしてください。位置引数はありません。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--csv` | | JSON | JSONの代わりにCSV（固定列セット）で出力します（完全なアラート詳細）。 |

```bash
banshee pba search --created 1d -l 10 | banshee pba export > alerts.json
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export --csv > identity_alerts.csv
```

**入力：** 標準入力で `banshee pba search` が出力するJSONオブジェクトを期待します — エクスポートは `.data[]` を読み取り、各レコードに `playbook_alert_id` と `category` が必要です（これらがカテゴリー固有のフェッチを駆動します）。パイプされた入力なし（TTY）で実行すると、`BadParameter` エラーが発生します。

**レスポンスの形式（デフォルト）：** 完全なPlaybook Alertオブジェクトの配列（JSON） — `banshee pba lookup` が返すのと同じアラートごとの構造（`playbook_alert_id`、`panel_status`、`panel_evidence_summary`、`panel_log_v2`）。

**レスポンスの形式（`--csv`）：** ヘッダー行と以下の固定列を持つCSV：`ID`、`Priority`、`Alert Rule`、`Status`、`Created`、`Updated`、`Subject`、`Assignee`、`Assessments`、`Entities`、`Reopen Strategy`、`Onwards Actions`。`Assessments` と `Entities` は `; ` で結合されます。フィールド値内のカンマはスペースに置換されます。
