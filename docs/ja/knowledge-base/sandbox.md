# sandbox

> 認証、準備確認、出力規則、および共有 LLM に関する注意事項については、[index.md](index.md) を参照してください。

Sandbox コマンドには、`RF_TOKEN` に加えて `RF_SANDBOX_TOKEN` が必要です。特定のリージョンを対象とするには、`RF_SANDBOX_CHOICE`（またはグローバルオプション `--sandbox-choice`）を設定してください。指定可能な値は `eu`（デフォルト）、`usa`、`apj`、`public`、`private` です。

---

### `banshee sandbox stats`

設定可能なルックバックウィンドウ内のサンドボックス送信を集計し、SOC の朝次ブリーフを出力します。出力内容は、送信件数、スコア分布、マルウェアファミリーの上位一覧、プラットフォームのカバレッジ、抽出済み C2、および SOAR 検証済みネットワーク IOC（侵害の指標）です。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--days INTEGER` | `-d` | `7` | ルックバックウィンドウの日数（最小 1） |
| `--subset` | `-s` | `org` | サンプルスコープ: `owned`、`public`、`org` |
| `--pretty` | `-p` | | 人間が読みやすい Rich レイアウト |

スコアバケット（トリアージ 1〜10 スケール）:

| バケット | スコア範囲 | 意味 |
|--------|-------------|---------|
| `malicious` | 8〜10 | 既知のマルウェア、高い信頼度 |
| `suspicious` | 5〜7 | 強い挙動的指標 |
| `potentially_suspicious` | 3〜4 | 一部の指標あり |
| `clean` | 1〜2 | 低リスクまたは無害 |

```bash
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats -d 30 | jq '.by_score'
```

**レスポンスの形式:** 単一の JSON オブジェクトを返します。

| フィールド | 説明 |
|-------|-------------|
| `.period_start` | 集計ウィンドウの開始日時（ISO 8601） |
| `.period_end` | 集計ウィンドウの終了日時（ISO 8601） |
| `.period_days` | ルックバックウィンドウの日数 |
| `.subset` | 使用されたスコープ（`owned`、`public`、`org`） |
| `.total` | ウィンドウ内の総送信件数 |
| `.pending` | 分析中の送信件数 |
| `.failed` | エラーが発生した送信件数 |
| `.by_kind` | 送信種別（`file`、`url` など）を件数にマッピングするオブジェクト |
| `.by_platform` | プラットフォームタグを件数にマッピングするオブジェクト |
| `.by_score` | スコアバケット名を件数にマッピングするオブジェクト |
| `.by_file_type` | ファイル拡張子を件数にマッピングするオブジェクト |
| `.top_tags` | `malware_families`、`botnets`、`arch_file`、`behavioral_ttp` のキーを持つオブジェクト — それぞれタグ名を件数にマッピング |
| `.top_iocs` | `extracted_c2`、`verified_network`、`malicious_sha256` のキーを持つオブジェクト — それぞれ IOC 文字列の配列 |
| `.daily_by_family` | マルウェアファミリーを日別件数にマッピングするオブジェクト |
| `.trend_vs_prior_period` | `total` および `reported` サブオブジェクトを持つオブジェクト。それぞれ `current`、`prev`、`pct_change` を含む |
| `.soar_skipped` | SOAR 検証がスキップされた場合に `true`（`.top_iocs.verified_network` は空になります） |

---

### `banshee sandbox list`

サンドボックスサンプルを一覧表示します。対象は自分のサンプル、自組織のサンプル（デフォルト）、またはパブリックフィードです。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--subset` | `-s` | `org` | サンプルスコープ: `owned`、`public`、`org` |
| `--limit INTEGER` | `-l` | `20` | 最大件数（1〜4095） |
| `--pretty` | `-p` | | 人間が読みやすいテーブル |

```bash
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
```

**レスポンスの形式:** フラットな JSON 配列を返します。各要素のフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.id` | サンプル ID（例: `260722-x8lgjahyvx`） |
| `.status` | 分析ステータス: `pending`、`running`、`reported`、`failed` |
| `.kind` | 送信種別: `file`、`url`、`fetch`、`import` |
| `.filename` | 元のファイル名（URL 送信の場合は空になることがあります） |
| `.submitted` | 送信日時（ISO 8601） |
| `.completed` | 完了日時（ISO 8601。まだ実行中の場合は存在しません） |
| `.sha256` | 送信ファイルの SHA-256 |
| `.user_id` | 送信ユーザーの UUID |

---

### `banshee sandbox search`

構造化フィルター（ハッシュ、ファミリー、タグ、ボットネット、ウォレット、IP、ドメイン、URL、送信日付ウィンドウ）またはロールの Triage クエリに一致するサンプルを検索します。少なくとも 1 つのフィルターまたは `--query` の指定が必要です。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--hash TEXT` | | | ファイルハッシュでフィルター（MD5/SHA1/SHA256） |
| `--family TEXT` | | | マルウェアファミリー名でフィルター |
| `--tag TEXT` | `-T` | | タグでフィルター（繰り返し指定可） |
| `--botnet TEXT` | | | ボットネット名でフィルター |
| `--wallet TEXT` | | | ウォレットアドレスでフィルター |
| `--ip TEXT` | | | IP アドレスでフィルター |
| `--domain TEXT` | | | ドメインでフィルター |
| `--url TEXT` | | | URL でフィルター |
| `--from-date YYYY-MM-DD` | | | この日付以降に送信されたものを対象 |
| `--to-date YYYY-MM-DD` | | | この日付以前に送信されたものを対象 |
| `--query TEXT` | `-q` | | ロールの Triage クエリ文字列（構造化フィルターと AND で結合） |
| `--limit INTEGER` | `-l` | `50` | 最大件数（1〜200） |
| `--pretty` | `-p` | | 人間が読みやすいテーブル |

```bash
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
```

**レスポンスの形式:** JSON 配列を返します。構造は `sandbox list` の各要素と同一です。

---

### `banshee sandbox get`

サンドボックスサンプルの ID を指定して、単一サンプルのサマリーを取得します。取得内容は、現在のステータス、総合スコア、ターゲット、作成および完了日時、SHA256、タスクごとの内訳です。実行中および完了済みのサンプルどちらにも対応しています。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必須） | | サンドボックスサンプル ID |
| `--pretty` | `-p` | 人間が読みやすい Rich レイアウト |

```bash
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
```

**レスポンスの形式:** 単一の JSON オブジェクトを返します。

| フィールド | 説明 |
|-------|-------------|
| `.sample` | サンプル ID |
| `.status` | 分析ステータス: `pending`、`running`、`static_analysis`、`reported`、`failed` |
| `.target` | 主要な実行ターゲット（ファイル名または URL） |
| `.score` | 総合トリアージスコア（1〜10。分析中は `0`） |
| `.created` | 送信日時（ISO 8601） |
| `.completed` | 完了日時（ISO 8601。まだ実行中の場合は存在しません） |
| `.sha256` | 送信ファイルの SHA-256（URL 送信の場合は存在しません） |
| `.owner` | 送信ユーザー ID |
| `.tasks` | タスク ID → `{kind, status, score, tags, platform}` にマッピングするオブジェクト |

---

### `banshee sandbox download` *(ディスクへの書き込みを伴う操作)*

1 つ以上のサンプル ID に対して、元の送信サンプルのバイトデータをダウンロードします。各サンプルは、アンチウイルス、セキュアメールゲートウェイ、またはファイルマネージャーによる誤った実行を防ぐため、パスワード `infected` を使用した AES 暗号化 ZIP アーカイブにラップされます。展開には `7z x -pinfected <sample-id>.zip` を使用してください。標準の `unzip` は AES 暗号化 ZIP を確実に処理できません。

サンプル ID は位置引数として渡すか、stdin からパイプ（空白区切り）で渡すことができます。`--yes` を指定しない場合は確認プロンプトが表示されます。ダウンロードおよび ZIP 化の際、バイトデータは一時的にこのプロセスのメモリ上に存在します。EDR（Endpoint Detection and Response）による積極的なメモリスキャンが反応する可能性があります。日常業務で使用する企業のノート PC ではなく、アナリスト専用のマシンで実行してください。

| 引数/オプション | 短縮形 | デフォルト | 説明 |
|-----------------|-------|---------|-------------|
| `SAMPLE_IDS` | | | 1 つ以上のサンプル ID（または stdin から読み取り） |
| `--output-dir PATH` | `-d` | （必須） | 暗号化 ZIP アーカイブを保存するディレクトリ（存在しない場合は作成されます） |
| `--yes` | `-y` | | 確認プロンプトをスキップ |
| `--workers INTEGER` | `-w` | `1` | 並列ダウンロードのワーカー数（1〜16） |

```bash
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
```

**レスポンス:** 警告行が stderr に 1 回出力されます。成功したダウンロードごとに、`[<id>] Saved: <path> (<bytes> bytes, sha256=<hex>)` 形式の行が stderr に出力されます。失敗した場合は `[<id>] ERROR: <msg>` が出力されます。一部失敗のバッチ処理は最後まで続行され、終了コード 1 で終了します。全件成功の場合は終了コード 0 で終了します。

アーカイブの内容: `<sample-id>`（拡張子の推測なし）という名前の単一エントリで、サンプルの生バイトデータを含みます。

---

### `banshee sandbox delete` *(変更を伴う操作)*

サンドボックスサンプルを ID で削除し、関連するすべてのタスクのアーティファクトを削除します。`--yes` を指定しない場合は確認プロンプトが表示されます。

| 引数/オプション | 説明 |
|-----------------|-------------|
| `SAMPLE_ID`（必須） | 削除するサンプル ID |
| `--yes` / `-y` | 確認プロンプトをスキップ |

```bash
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
```

**レスポンス:** 成功時は出力なし。終了コード 0 で終了します。

---

### `banshee sandbox submit` *(変更を伴う操作)*

分析のためにサンプルを送信します。ローカルファイルはアップロードされ、URL はブラウザで実行されます（または `--fetch` を使用してファイルとしてダウンロードしてから分析します）。`--import` を使用してパブリックサンプルを ID でインポートすることも可能です。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `TARGET`（必須） | | ファイルパス、URL、またはパブリックサンプル ID（`--import` 使用時） |
| `--fetch` | | URL を先にダウンロードしてからファイルとして分析。`--import` と相互排他 |
| `--import` | | ターゲットをパブリックサンプル ID として扱う。`--fetch` と相互排他 |
| `--profile TEXT` | | 分析プロファイル名または ID（繰り返し指定可。`--interactive` と相互排他） |
| `--timeout INTEGER` | `-t` | 分析タイムアウト（秒単位、1〜3600） |
| `--network` | `-N` | ネットワークモード: `internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | VPN 出口の国コード。`--network vpn` が必要 |
| `--tags TEXT` | `-T` | カスタムタグ（繰り返し指定可） |
| `--password TEXT` | | 保護されたアーカイブのパスワード |
| `--wait` | `-w` | 分析が完了するまでポーリングし、概要レポートを出力 |
| `--interactive` | `-i` | 静的分析後に一時停止し、`set-profile` によるプロファイル選択を待機。`--profile` と相互排他 |
| `--pretty` | `-p` | 人間が読みやすい出力 |

```bash
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
```

**レスポンスの形式（デフォルト）:** 送信済みサンプルを JSON オブジェクトとして返します。フィールドは `sandbox list` の各要素と同一です（`id`、`status`、`kind`、`filename`、`submitted`、`sha256`、`user_id`）。`.id` を使用して送信をトラッキングまたはレポートしてください。

**レスポンスの形式（`--wait` 使用時）:** 概要レポートを返します。構造は `sandbox report overview` と同一です。

---

### `banshee sandbox set-profile` *(変更を伴う操作)*

静的分析で一時停止中のサンプル（`--interactive` で送信されたもの）に分析プロファイルを割り当てます。`--auto` を使用するとサンドボックスが自動的に選択し、`--pick FILE:PROFILE` を使用すると手動でファイルごとにマッピングを指定できます。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必須） | | 静的分析で一時停止中のサンプル ID |
| `--auto` | `-a` | すべてのファイルのプロファイルを自動選択。`--pick` と相互排他 |
| `--pick FILE:PROFILE` | | 1 つのファイルを 1 つのプロファイルにマッピング（繰り返し指定可）。`--auto` と相互排他 |
| `--pretty` | `-p` | 人間が読みやすい出力 |

```bash
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
```

---

### `banshee sandbox profile list`

Recorded Future Sandbox で利用可能なすべての分析プロファイルを一覧表示します。

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--pretty` | `-p` | 人間が読みやすいテーブル |

```bash
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
```

**レスポンスの形式:** フラットな JSON 配列を返します。各要素のフィールド:

| フィールド | 説明 |
|-------|-------------|
| `.id` | プロファイルの UUID |
| `.name` | プロファイル名 |
| `.tags` | OS/ロケールタグの配列（例: `["os:windows10-2004-x64", "locale:en-us"]`） |
| `.network` | ネットワークモード（例: `"internet"`、`"tor"`、`"vpn"`） |
| `.geolocation` | VPN 出口の国コードの配列（該当しない場合は空） |
| `.timeout` | 分析タイムアウト（秒単位） |
| `.options` | `browser` などのオプションフィールドを持つオブジェクト |

---

### `banshee sandbox profile get`

ID または名前で単一の分析プロファイルを取得します。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必須） | | プロファイルの UUID または名前 |
| `--pretty` | `-p` | 人間が読みやすいテーブル |

```bash
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
```

**レスポンスの形式:** 単一のプロファイルオブジェクトを返します。フィールドは `sandbox profile list` の各要素と同一です。

---

### `banshee sandbox profile create` *(変更を伴う操作)*

新しい分析プロファイルを作成します。プロファイル名は組織内で一意である必要があります。

| オプション | 短縮形 | デフォルト | 説明 |
|--------|-------|---------|-------------|
| `--name TEXT` | `-n` | （必須） | プロファイル名（一意である必要があります） |
| `--tag TEXT` | `-T` | （必須） | OS/ロケールタグ（繰り返し指定可）。ロケールタグには少なくとも 1 つの OS タグとの組み合わせが必要 |
| `--timeout INTEGER` | `-t` | `120` | 分析タイムアウト（秒単位、1〜3600） |
| `--network` | `-N` | | ネットワークモード: `internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | | VPN 出口の国コード。`--network vpn` が必要（繰り返し指定可） |
| `--browser` | `-b` | | ブラウザ: `chrome`、`firefox`、`ie11`、`microsoft-edge` |
| `--pretty` | `-p` | | 人間が読みやすいテーブル |

```bash
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
```

**レスポンスの形式:** 作成されたプロファイルを JSON オブジェクトとして返します。フィールドは `sandbox profile list` の各要素と同一です。

---

### `banshee sandbox profile update` *(変更を伴う操作)*

既存の分析プロファイルを更新します。指定したオプションのみが変更され、省略したオプションは現在の値が維持されます。`--unset` を使用して `network`、`browser`、または `geolocation` をクリアできます。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必須） | | プロファイルの UUID または名前 |
| `--name TEXT` | `-n` | 新しいプロファイル名 |
| `--tag TEXT` | `-T` | OS/ロケールタグ。既存のすべてのタグを置き換えます（繰り返し指定可） |
| `--timeout INTEGER` | `-t` | 分析タイムアウト（秒単位、1〜3600） |
| `--network` | `-N` | ネットワークモード: `internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | VPN 出口の国コード。`--network vpn` が必要（繰り返し指定可） |
| `--browser` | `-b` | ブラウザ: `chrome`、`firefox`、`ie11`、`microsoft-edge` |
| `--unset` | | フィールドをクリア: `network`、`browser`、または `geolocation`（繰り返し指定可） |
| `--pretty` | `-p` | 人間が読みやすいステータスメッセージ |

```bash
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
```

**レスポンスの形式:** プロファイルが存在し更新された場合は `{"updated": true}` を返し、存在しない場合は `{"updated": false}` を返します。いずれの場合も終了コード 0 で終了します。

---

### `banshee sandbox profile delete` *(変更を伴う操作)*

分析プロファイルを ID または名前で削除します。冪等な操作です。すでに存在しないプロファイルを削除しようとした場合は警告を出力し、終了コード 0 で終了します。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必須） | | プロファイルの UUID または名前 |
| `--yes` / `-y` | | 確認プロンプトをスキップ |

```bash
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
```

**レスポンス:** 成功時は出力なし。終了コード 0 で終了します。

---

### `banshee sandbox report overview`

完了したサンドボックスサンプルの完全な概要レポートを取得します。取得内容は、判定スコア、マルウェアファミリー、タグ、ハッシュ、検出シグネチャ、抽出されたマルウェア設定、ネットワーク IOC、およびタスクごとの結果です。サンプルは `reported` ステータスである必要があります。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必須） | | サンドボックスサンプル ID |
| `--wait` | `-w` | レポートが準備できるまで最大 30 分間ポーリング |
| `--pretty` | `-p` | 人間が読みやすい要約ビュー |

```bash
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
```

**レスポンスの形式:** 単一の JSON オブジェクトを返します。

| フィールド | 説明 |
|-------|-------------|
| `.version` | レポートフォーマットのバージョン |
| `.build` | サンドボックスのビルド情報 |
| `.analysis` | 判定オブジェクト: スコア、マルウェアファミリー、タグ |
| `.sample` | サンプルメタデータ: id、kind、filename、sha256、submitted、completed |
| `.signatures` | すべてのタスクにわたる検出シグネチャ |
| `.targets` | 実行ターゲットオブジェクトの配列。各オブジェクトには `.iocs`（ネットワーク IOC）とマルウェア設定の抽出結果が含まれます |
| `.tasks` | タスクごとのサマリーの配列: タスク ID、プラットフォーム、ステータス、判定スコア |

---

### `banshee sandbox report static`

サンドボックスサンプルの静的（実行前）分析レポートを取得します。取得内容は、判定スコア、タグ、展開されたファイル、静的検出シグネチャ、および抽出されたマルウェア設定です。挙動タスクの完了前であっても、静的分析が完了した時点で取得可能です。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必須） | | サンドボックスサンプル ID |
| `--wait` | `-w` | レポートが準備できるまで最大 10 分間ポーリング |
| `--pretty` | `-p` | 人間が読みやすい要約ビュー |

```bash
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
```

**レスポンスの形式:** 単一の JSON オブジェクトを返します。

| フィールド | 説明 |
|-------|-------------|
| `.version` | レポートフォーマットのバージョン |
| `.build` | サンドボックスのビルド情報 |
| `.sample` | サンプルメタデータ: id、kind、filename、sha256、submitted |
| `.task` | 静的タスクのメタデータ |
| `.analysis` | 判定オブジェクト: スコア、タグ、静的シグネチャ |
| `.files` | 展開されたファイルの配列 — 各要素に `sha256`、`filename`、`size`、および静的分析の詳細が含まれます |
| `.unpack_count` | 送信ファイルから展開されたファイルの総数 |
| `.error_count` | 展開できなかったファイルの数 |

---

### `banshee sandbox report behavioral`

完了したサンドボックスサンプルの挙動（実行後）レポートを取得します。完了した挙動タスクごとに 1 オブジェクトが返されます。未完了のタスクは出力から除外され、stderr に通知されます。すべてのタスクが完了するまで、コマンドは非ゼロの終了コードで終了します。サンプルに挙動タスクがない場合は、終了コード 0 で空の配列が返されます。

`--pretty` ビューでのプロセスのコマンドラインはデフォルトで省略されます。完全な内容が必要な場合は `--full-cmd` を使用してください（コマンドラインはマルウェアサンプルからそのまま取得されるため、信頼できない入力として扱ってください）。

| 引数/オプション | 短縮形 | 説明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必須） | | サンドボックスサンプル ID |
| `--wait` | `-w` | すべてのタスクが完了するまで最大 30 分間ポーリング |
| `--full-cmd` | | プロセスのコマンドラインを省略せず完全に表示（信頼できない入力として扱うこと） |
| `--pretty` | `-p` | タスクごとの人間が読みやすい要約ビュー |

```bash
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
```

**レスポンスの形式:** JSON 配列を返します。各要素は 1 つの挙動タスクに対応します。

| フィールド | 説明 |
|-------|-------------|
| `.task_id` | 挙動タスク ID |
| `.version` | レポートフォーマットのバージョン |
| `.build` | サンドボックスのビルド情報 |
| `.sample` | サンプルメタデータ: id、kind、filename、sha256 |
| `.task` | タスクメタデータ: platform、status、started、completed |
| `.analysis` | 判定オブジェクト: スコア、マルウェアファミリー、タグ |
| `.tags` | 挙動タグの配列（例: `discovery`、`execution`） |
| `.signatures` | トリガーされた検出シグネチャの配列 |
| `.processes` | 観測されたプロセスの配列 — 各要素に `pid`、`name`、`cmd`（`--full-cmd` を指定しない場合は省略）、および子プロセスが含まれます |
| `.network` | ネットワークアクティビティ: `.flows`（接続レコード）、`.dns`（DNS クエリ）、`.http`（HTTP リクエスト） |
| `.dumped` | ダンプ/抽出されたファイルとその SHA-256 ハッシュの配列 |