# Sandbox Analysis

## ユースケースの概要
ファイルおよび URL を Recorded Future Sandbox に送信して自動マルウェア解析を実行し、生成されたレポートを取得するとともに、検証済みサンプルをオフライン解析に引き渡すことで、Security Operations Center（SOC）のトリアージおよび脅威調査を加速します。

## 課題
アナリストは、疑わしいファイルや URL を安全・制御された環境で実行（デトネーション）し、その意図を特定して脅威インジケーターを抽出する必要があります。統合されたワークフローが存在しない場合、静的シグネチャ、挙動アクティビティ、ネットワーク IOC（侵害の痕跡）、マルウェア設定情報といった解析結果を収集・相関させるには複数のツールにまたがる手作業が必要となり、SOC の対応速度が低下します。

## 解決策
[`banshee sandbox`](../../reference/commands.md#banshee-sandbox) コマンドを使用して、PS Banshee から直接サンプルを送信しレポートを取得できます。

- [`banshee sandbox submit`](../../reference/commands.md#banshee-sandbox-submit) を使用して、ローカルファイル、URL、またはパブリックサンプルを解析のために送信します。[`--wait`](../../reference/commands.md#banshee-sandbox-submit--wait) を追加すると解析完了までポーリングを行い、概要レポートをすぐに表示します。[`--interactive`](../../reference/commands.md#banshee-sandbox-submit--interactive) を追加すると静的解析の完了時点で一時停止し、デトネーションプロファイルを選択してから処理を続行できます。

- 解析完了後は、[`banshee sandbox report overview`](../../reference/commands.md#banshee-sandbox-report-overview) で判定結果、マルウェアファミリー、ネットワーク IOC、タスクごとの結果の概要を確認できます。[`banshee sandbox report static`](../../reference/commands.md#banshee-sandbox-report-static) ではデトネーション前の解析および抽出されたマルウェア設定情報を、[`banshee sandbox report behavioral`](../../reference/commands.md#banshee-sandbox-report-behavioral) ではデトネーション後のアクティビティ（トリガーされたシグネチャ、観測されたプロセス、抽出された C2 など）を確認できます。

- [`banshee sandbox stats`](../../reference/commands.md#banshee-sandbox-stats) を使用すると、設定可能なルックバックウィンドウ内の送信件数、スコア分布、上位マルウェアファミリー、ネットワーク IOC を示す SOC モーニングブリーフを生成できます。シフト引き継ぎや日次トリアージに適しています。

- [`banshee sandbox list`](../../reference/commands.md#banshee-sandbox-list) を使用して、自身のアカウント、組織、またはパブリックフィードからの最近の送信履歴を確認できます。また、[`banshee sandbox get`](../../reference/commands.md#banshee-sandbox-get) を使用すると、フルレポートを取得することなく、任意の単一サンプルの現在のステータス、総合スコア、タスクごとの内訳を確認できます。

- [`banshee sandbox search`](../../reference/commands.md#banshee-sandbox-search) を使用して、ハッシュ値、マルウェアファミリー、タグ、ボットネット、ウォレット、ネットワークインジケーター（IP、ドメイン、URL）、または送信日時ウィンドウによって過去の送信履歴をピボット検索できます。`AND`/`OR`/`NOT` 式を使用する場合は `--query` でローの Triage クエリ文字列を渡してください。

- [`banshee sandbox download`](../../reference/commands.md#banshee-sandbox-download) を使用して、オフライン解析（YARA/Sigma チューニング、EDR 検知テスト、キャンペーン帰属分析）のために送信済みの元バイト列を取得できます。各サンプルはパスワード `infected` の AES 暗号化 ZIP アーカイブにラップされており、`7z x -pinfected <sample-id>.zip` で展開してください。バイト列はダウンロードおよび ZIP 化の処理中、短時間プロセスメモリ上に存在するため、アナリストが管理するマシンで実行してください。

- [`banshee sandbox delete`](../../reference/commands.md#banshee-sandbox-delete) を使用して、不要になったサンプルおよびその関連アーティファクトを削除できます。

- カスタムデトネーション環境を使用するチームの場合、[`banshee sandbox profile`](../../reference/commands.md#banshee-sandbox-profile) コマンドを使用して、各送信に適用される OS、ネットワーク設定、ブラウザー、解析タイムアウトを制御する解析プロファイルを作成・更新・削除できます。