# risklist

> 認証、準備確認、出力規則、および共有LLMノートについては [index.md](index.md) を参照してください。

### `banshee risklist fetch`

RFからリスクリストをダウンロードするか、ローカルのカスタムファイルを読み込みます。

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--entity-type` | `-e` | エンティティタイプ: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--list-name TEXT` | `-l` | `default`、`large`、または `banshee ioc rules` に含まれる任意のルール名 |
| `--custom-list-path TEXT` | `-c` | ローカルリスクリストファイルへのパス |
| `--output-path TEXT` | `-o` | 出力パス（デフォルトはカレントディレクトリに自動生成されたファイル名） |
| `--as-json` | `-j` | ダウンロードしたリストをJSONに変換（`--list-name` + `--entity-type` との組み合わせのみ） |

```bash
banshee risklist fetch -e domain -l default
banshee risklist fetch -c /custom/path/to/list.csv
banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv
```

---

### `banshee risklist create`

1つ以上のリスクルールからカスタムのマージ済みリスクリストを作成します。スコアフィルタリングも可能です。ローカルに書き込むか、RF Fusionにアップロードできます。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--entity-type` | `-e` | | エンティティタイプ: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--risk-rule TEXT` | `-R` | | 含めるリスクルール（繰り返し指定可）: `default`、`large`、または `banshee ioc rules` に含まれる任意のルール名 |
| `--risk-score INTEGER` | `-r` | | リスクスコアの最小閾値（5〜99） |
| `--format` | `-f` | `csv` | 出力形式: `csv`, `edl`, `json` |
| `--output-path TEXT` | `-o` | カレントディレクトリ | 出力ファイルパス |
| `--fusion` | `-F` | | RF Fusionにアップロード（`--output-path` をFusionの保存先パスとして使用） |

**出力形式:**
- `csv` — ヘッダー付きカンマ区切り形式: `Name, Risk, RiskString, EvidenceDetails`
- `edl` — IOC値を1行ずつ記述したプレーンリスト（ファイアウォール/EDLフィード用）
- `json` — リスクリストエントリの完全なJSON配列

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

---

### `banshee risklist stat`

リスクリストのメタデータを表示します。Fusionに存在するかどうか、および現在のetagを確認できます。

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--entity-type` | `-e` | エンティティタイプ |
| `--list-name TEXT` | `-l` | リスト名 |
| `--custom-list-path TEXT` | `-c` | ローカルリスクリストファイルへのパス |
| `--pretty` | `-p` | 整形して出力 |
| `--count` | `-C` | リスクリスト全体のIOC数とリスクスコア分布を表示 |

```bash
banshee risklist stat -e ip -l recentValidatedCnc
banshee risklist stat -e domain -l domain_risklist
banshee risklist stat -e ip -l default --count
```

**レスポンスの形式:** 単一のJSONオブジェクトを返します:

| フィールド | 説明 |
|-------|-------------|
| `.name` | Fusionに保存されているリスクリスト名（例: `"recentValidatedCnc_ip_risklist"`） |
| `.exists` | `true`/`false` — リストがRF Fusionに存在するかどうか |
| `.etag` | キャッシュ検証用のetagハッシュ文字列 |
| `.counts` | *（`--count` 指定時のみ）* 各リスクスコアとそのIOC数のマッピングオブジェクト（例: `{"28": 261110, "65": 6531}`） |

**実行テストに関する注意:** 2026-05-01のテスト中、`--custom-list-path /tmp/banshee_smoke_risklist.json` はFusion APIルックアップを試み、`400 Bad Request` を返しました。Fusionに紐付けられた既知のカスタムパスを検証する場合を除き、`-e`/`-l` を優先して使用してください。
