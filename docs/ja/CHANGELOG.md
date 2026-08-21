# リリース履歴

## 1.5.0 - 2026-08-21

### 追加
- Recorded Future Sandbox 向けの新しい [`sandbox`](reference/commands.md#banshee-sandbox) コマンドグループを追加。`RF_SANDBOX_TOKEN` が必要。リージョンは [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) または `RF_SANDBOX_CHOICE` で選択可能（デフォルト: `eu`、その他: `usa`、`apj`、`public`、`private`）。
- ローカルファイル、URL、公開サンプル ID（`--import`）、またはダウンロード対象 URL（`--fetch`）を解析のために送信する新しい [`sandbox submit`](reference/commands.md#banshee-sandbox-submit) サブコマンドを追加。プロファイルの割り当て、カスタムタグ、タイムアウト、ネットワークモード（ジオロケーション付き VPN を含む）、アーカイブパスワード、解析完了まで待機して概要レポートを表示する [`--wait`](reference/commands.md#banshee-sandbox-submit--wait)、および静的解析で一時停止して起爆前にファイルごとにプロファイルを選択する [`--interactive`](reference/commands.md#banshee-sandbox-submit--interactive) をサポート。
- サンプルの統合判定レポート、起爆前静的解析、またはタスクごとの起爆後レポートを取得する新しい [`sandbox report overview`](reference/commands.md#banshee-sandbox-report-overview)、[`sandbox report static`](reference/commands.md#banshee-sandbox-report-static)、および [`sandbox report behavioral`](reference/commands.md#banshee-sandbox-report-behavioral) サブコマンドを追加。各コマンドはレポートが準備完了になるまで待機する [`--wait`](reference/commands.md#banshee-sandbox-report-overview--wait) をサポート。
- 自身、組織、または公開フィードのサンプル一覧を表示する新しい [`sandbox list`](reference/commands.md#banshee-sandbox-list) サブコマンドを追加。
- ハッシュ、マルウェアファミリー、タグ、ボットネット、ウォレット、ネットワークインジケーター（IP、ドメイン、URL）、または送信日時ウィンドウで過去の送信履歴を横断検索する新しい [`sandbox search`](reference/commands.md#banshee-sandbox-search) サブコマンドを追加。`AND`/`OR`/`NOT` 式向けに [`--query`](reference/commands.md#banshee-sandbox-search--query) でも raw の Triage クエリ文字列を受け入れる。
- 完全なレポートを取得せずに、サンプルの現在のステータス、総合スコア、およびタスクごとの内訳を取得する新しい [`sandbox get`](reference/commands.md#banshee-sandbox-get) サブコマンドを追加。処理中および完了済みのサンプルの両方で動作する。
- 1 つ以上のサンプル ID の元の送信バイトデータを取得する新しい [`sandbox download`](reference/commands.md#banshee-sandbox-download) サブコマンドを追加。各サンプルはパスワード `infected` の AES 暗号化 ZIP アーカイブにラップされ（MalwareBazaar/VirusTotal/Triage の慣例に準拠）、ウイルス対策ソフト、セキュアメールゲートウェイ、またはファイルマネージャーによる誤起爆を防止する。サンプル ID は位置引数として渡すか、stdin からパイプ入力できる。`7z x -pinfected <sample-id>.zip` で展開すること。
- サンプルとそのタスクアーティファクトを削除する新しい [`sandbox delete`](reference/commands.md#banshee-sandbox-delete) サブコマンドを追加（`--yes` を指定しない限り確認プロンプトが表示される）。
- 静的解析で一時停止中のサンプルに解析プロファイルを割り当てる新しい [`sandbox set-profile`](reference/commands.md#banshee-sandbox-set-profile) サブコマンドを追加（`--auto` またはファイルごとの `--pick FILE:PROFILE` を指定）。
- カスタム起爆プロファイルを管理する新しい [`sandbox profile`](reference/commands.md#banshee-sandbox-profile) サブコマンドグループを追加: [`list`](reference/commands.md#banshee-sandbox-profile-list)、[`get`](reference/commands.md#banshee-sandbox-profile-get)、[`create`](reference/commands.md#banshee-sandbox-profile-create)、[`update`](reference/commands.md#banshee-sandbox-profile-update)（フィールドをクリアする `--unset` を含む）、および [`delete`](reference/commands.md#banshee-sandbox-profile-delete)。
- SOC モーニングブリーフを生成する新しい [`sandbox stats`](reference/commands.md#banshee-sandbox-stats) サブコマンドを追加。設定可能なルックバックウィンドウにわたる送信件数、スコア分布（悪意あり / 疑わしい / 疑わしい可能性あり / クリーンにバケット化された 1〜10 の Triage スケール）、プラットフォームカバレッジ、上位マルウェアファミリーおよびボットネット、行動 TTP、抽出済み C2、および SOAR 検証済みネットワーク IOC を出力する。
- Docs: 韓国語（`ko`）言語インフラストラクチャーを追加。コンテンツはフォローアップ PR で提供され、それまでは未翻訳バナーが表示される。
- Docs: `scripts/docs.py` — `build-all`、`dev`、`check-translations`、`translate` コマンドを追加。
- Docs: 英語以外のすべての翻訳に対する CI ドリフト検出を追加。コントリビューターはローカルで LLM 翻訳ツールを実行する（`uv sync --group translations && scripts/docs.py translate --lang <code> --all`）。CI は LLM を呼び出さない。

### 変更
- 設定: banshee 固有のグローバルフィールド（`sandbox_choice`）を保持する `BansheeConfig(psengine.ConfigModel)` サブクラスを追加。新しいルートレベルの [`--sandbox-key`](reference/commands.md#banshee--sandbox-key) / `RF_SANDBOX_TOKEN` および [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) / `RF_SANDBOX_CHOICE` オプションにより、必要なコマンドからサンドボックス認証を利用できるようになった。
- Docs: `mike` によるバージョン管理デプロイを廃止。サイトはルート URL にデプロイされるようになった。以前のバージョン管理 URL（`/1.x/…`）は解決されなくなったため、ルート URL を使用すること。
- Docs: `mkdocs-static-i18n` を `scripts/docs.py` によって管理される fastapi スタイルの言語ごとのビルドに置き換え。権威ある `docs/mkdocs.yml` を 1 つ維持し、翻訳済み言語は翻訳済み Markdown ファイルのみを所有する。
- Docs: `noklam/mkdocs-llmstxt-md` を `pawamoy/mkdocs-llmstxt` に変更。`llms.txt` / `llms-full.txt` は英語のみとなり、サイトルートに配置される。


## v.1.4.1 - 2026-07-13

### 変更
- `psengine` の依存関係を更新。


## v.1.4.0 - 2026-07-13

### 追加
- [`risklist stat`](reference/commands.md#banshee-risklist-stat) コマンドに、リスクリストをダウンロードしてリスクスコアごとのインジケーター数のテーブルを表示する新しい [`-C`/`--count`](reference/commands.md#banshee-risklist-stat--count) オプションを追加。

## v1.3.1 - 2026-06-30

### 変更
- 依存関係を更新。

## 1.3.0 - 2026-06-15

### 追加
- EML ファイルをエンリッチするための新しい [`email enrich`](reference/commands.md#banshee-email-enrich) サブコマンドを追加。ヘッダーの IP とボディの URL を抽出し、リスクスコア、脅威アクターの関連付け、マルウェアのリンク、リスクルールの根拠を含む Recorded Future インテリジェンスを返す。
- Classic Alert を完全な JSON またはサマリー CSV としてエクスポートするための新しい [`ca export`](reference/commands.md#banshee-ca-export) サブコマンドを追加。[`ca search`](reference/commands.md#banshee-ca-search) からパイプされたアラート ID を読み込む。
- Playbook Alert を完全な JSON またはサマリー CSV としてエクスポートするための新しい [`pba export`](reference/commands.md#banshee-pba-export) サブコマンドを追加。[`pba search`](reference/commands.md#banshee-pba-search) からパイプされた検索結果を読み込む。
- [`pba search`](reference/commands.md#banshee-pba-search) コマンドに、Playbook Alert を所有組織 ID でフィルタリングするための新しい [`-o`/`--org-id`](reference/commands.md#banshee-pba-search--org-id) オプションを追加（繰り返し指定可能）。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) コマンドに、指定したエンティティとリストを完全に一致させる（新しいエンティティを追加し、指定されなかった既存のエンティティを削除する）新しい [`-o`/`--overwrite`](reference/commands.md#banshee-list-bulk-add--overwrite) オプションを追加。
- あるリストから別のリストへエンティティをコピーするための新しい [`list copy`](reference/commands.md#banshee-list-copy) サブコマンドを追加。デフォルトでは追加モードで動作し、[`-o`/`--overwrite`](reference/commands.md#banshee-list-copy--overwrite) を使用するとコピー先をコピー元と完全に一致させることができる。
- コーディングアシスタントが CLI を検出・実行できるよう、[AI エージェントでの banshee の使用](getting-started/llms.md)のサポートを追加。

### 変更
- [`list clear`](reference/commands.md#banshee-list-clear) が [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) と同様に並列でエンティティを削除するようになった（大きなリストでは大幅に高速化）。削除内容を結果ごとにグループ化（`REMOVED` および削除できなかったもの）して報告し、可読性のためにソートする。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) が、すでにリストに存在するエンティティの再追加を試みる代わりにスキップし、`UNCHANGED` として報告するようになった。同じ入力ファイルを繰り返し実行してエンティティを追加・削除する場合に大幅な速度向上となる。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) と [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) が、出力を結果ごとにグループ化（`ADDED`、`REMOVED`、`UNCHANGED`）して可読性のためにソートするようになった。
- [`ca search`](reference/commands.md#banshee-ca-search) と [`pba search`](reference/commands.md#banshee-pba-search) が進捗インジケーターを stderr に出力するようになり、新しい `export` コマンドへのパイプ用に stdout をクリーンな状態に保つ。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) と [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) のプリティ出力（`-p`、`--pretty`）が、悪意のレベルに基づいてリスクスコアを色分け表示するようになった。
- PSEngine を ~v2.8.1 にアップグレード。

### 修正
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) と [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) が空白の入力行を無視し、エンティティが指定されなかった場合に明確なエラーを報告するようになった。

## 1.1.3 - 2026-03-18

### 修正
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) において、SOAR エンリッチメントでマルチスレッドが使用されていなかった問題を修正。大規模なキャプチャでのリスクスコアエンリッチメントが高速化された。


## 1.1.0 - 2026-03-13

### 追加
- 1 つ以上の Recorded Future リスクルールを単一の重複排除済みファイルにマージしてカスタムリスクリストを構築するための新しい [`risklist create`](reference/commands.md#banshee-risklist-create) サブコマンドを追加。CSV、JSON、EDL 出力フォーマット、オプションの最低リスクスコアフィルタリング、Recorded Future Fusion への直接アップロードをサポート。
- IOC (Indicator of Compromise) の高速バルクエンリッチメントのための新しい [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) サブコマンドを追加。API 呼び出しごとに最大 1,000 件のインジケーターをバッチ処理し、各インジケーターのリスクスコアとトリガーされたリスクルールを返す。IP、ドメイン、URL、ハッシュ、脆弱性のすべての IOC タイプをサポート。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) の JSON 出力に、リスクルールがトリガーされた原因となった具体的な根拠を詳述するリスクルール根拠の詳細を追加。

### 変更
- [`entity search`](reference/commands.md#banshee-entity-search) のデフォルト上限を 100 件に増加。
- [`list search`](reference/commands.md#banshee-list-search) のデフォルト上限を 1,000 件に増加。
- [`pba search`](reference/commands.md#banshee-pba-search) のデフォルト上限を 50 件に増加。
- [`pba search`](reference/commands.md#banshee-pba-search) の最大上限を 10,000 件に増加。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) が最低 1 のリスクスコアを受け入れるようになった。

### 修正
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) においてマルチスレッドが使用されておらず、バルクルックアップが順次実行されていた問題を修正。複数のインジケーターをエンリッチする際のルックアップが最大 20 倍高速化された。
- [`risklist fetch`](reference/commands.md#banshee-risklist-fetch) において、CSV ファイル内の異常に大きな列の値を解析する際にコマンドが失敗していた問題を修正。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) において、空の IOC リンクを解析する際に失敗していた問題を修正。
- [`list`](reference/commands.md#banshee-list) コマンドにおいて、API エラー発生時にエラー原因が常に正しく表示されない問題を修正。

## 1.0.0 - 2025-12-05

### 追加

- Recorded Future リスクリストのメタデータをダウンロードして確認するための新しい [`risklist`](reference/commands.md#banshee-risklist) コマンドを追加。
- 検出ルール（YARA、Snort、Sigma）を検索・ダウンロードするための新しい [`rules`](reference/commands.md#banshee-rules) コマンドを追加。
- [`ioc search`](reference/commands.md#banshee-ioc-search) および [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) コマンドに CVSS v4 フィールドのサポートを追加。

### 修正

- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) と [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) がユーザー指定のエンティティを重複排除するようになった。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) と [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) においてスペースを含むエンティティ名が正しく解析されていなかった問題を修正。
- [`pba lookup`](reference/commands.md#banshee-pba-lookup) が画像取得に失敗した場合もアラートを正しく処理するようになった。

### 変更

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) の JSON 出力にリスクルール根拠の詳細と IOC がトリガーしたすべてのリスクルールを含めるようになった。
- PSEngine を v2.4.0 にアップグレード。


## 0.0.5 - 2025-11-12

## 修正

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) において、pcap ファイルに IP またはドメインが見つからない場合にプログラムが予期せず終了していた問題を修正。

## 0.0.4 - 2025-11-07

### 追加

- [`ca search`](reference/commands.md#banshee-ca-search) コマンドでアラートステータスによるフィルタリングのサポートを追加。
- [`pba search`](reference/commands.md#banshee-pba-search) コマンドでエンティティによるフィルタリングのサポートを追加。
- すべての `pba` コマンドに `malware_report` カテゴリのサポートを追加。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) と [`ioc search`](reference/commands.md#banshee-ioc-search) のプリティ出力（`-p`、`--pretty`）にハッシュのハッシュアルゴリズムを追加。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) と [`ioc search`](reference/commands.md#banshee-ioc-search) のプリティ出力（`-p`、`--pretty`）に脆弱性のライフサイクルステージを追加。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) にリスクスコアで結果をフィルタリングするための `-r`/`--risk-score` オプションを追加。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) にスレットハンティングを有効にするための `-t`/`--threat-hunt` オプションを追加。

### 変更

- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) の各詳細レベルのフィールド選択を最適化。
- [`ioc search`](reference/commands.md#banshee-ioc-search) を詳細レベル 1 から 5 までサポートするように拡張（デフォルトは 1）。
- `pcap analyze` サブコマンドを [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) に名称変更。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) が Wireshark 互換フィルタークエリを含む洗練された JSON 出力を生成するようになった。
- PSEngine を v2.3.0 にアップグレード。

### 修正

- [`ca rules`](reference/commands.md#banshee-ca-rules) が結果を 10 件のアラートルールで打ち切っていた問題を修正。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) において IOC に根拠の詳細がない場合のエラーを修正。

### 削除

- `pba enrich` からインタラクティブ TUI 出力を削除し、プリティ出力（`--pretty`、`-p`）に置き換え。


## 0.0.3 - 2025-09-02

### 追加

- 1 つ以上の Classic Alert を更新するための新しい [`ca update`](reference/commands.md#banshee-ca-update) サブコマンドを追加。
- 1 つ以上の Playbook Alert を更新するための新しい [`pba update`](reference/commands.md#banshee-pba-update) サブコマンドを追加。
- [`pba`](reference/commands.md#banshee-pba) コマンドが `geopolitics_facility` カテゴリをサポートするようになった。
- Python 3.13 互換性を追加。
- `tshark` のバージョンチェックで最低バージョン 4.4.5 を強制するようになった。

### 修正

- `pcap analyze` がバージョン不一致によるクラッシュをしなくなった。
- CLI 全体の例外処理を改善。

### 変更

- `ioc search ENTITY_TYPE IOC` がカンマ区切りの文字列の代わりに空白区切りの IOC を受け入れるようになった。
- `pba lookup ALERT_ID -p` の出力フォーマットを改善。
- `ca search --triggered` が時間範囲をサポートするようになった。
- `ca search -r` がカンマ区切りの文字列の代わりに `-r` を繰り返すことで複数のルールを受け入れるようになった（例: `-r rule1 -r rule2`）。
- PSEngine を v2.0.6 にアップグレード。


## 0.0.2 - 2025-02-20

### 追加

- エンティティを検索・参照するための新しい [`entity`](reference/commands.md#banshee-entity) コマンドを追加。
- Recorded Future リストとウォッチリストを管理するための新しい [`list`](reference/commands.md#banshee-list) コマンドを追加。
- IOC ルールを検索・フィルタリングするための新しい [`ioc rules`](reference/commands.md#banshee-ioc-rules) サブコマンドを追加。
- トラブルシューティングを強化するための新しい ``--debug`` オプションを追加。


### 変更

- サブコマンド [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) の ``-v`` オプションで詳細レベル（1 から 5）を選択できるようになった。
- サブコマンド [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) が引数としてエンティティタイプを必要とするようになった（例: ``banshee ioc lookup ip 8.8.8.8``）。
- サブコマンド [`ca lookup`](reference/commands.md#banshee-ca-lookup) が洗練されたプリティアラートを返すようになった。
- PSEngine を v2.0.2 にアップグレード。


## 0.0.1 - 2024-09-01

### 追加

- ベータリリース

---

🚀 Recorded Future のサイバーセキュリティエンジニアチームによってお届けします。