# アラート管理

## ユースケースの概要
Recorded Future のアラート（Classic および Playbook）を端末から直接管理・トリアージ・一括更新することで、セキュリティオペレーションセンター（SOC）の対応および調査ワークフローを高速化します。

## 課題
アラートのたびに UI に切り替えることで調査が遅延し、アナリストの疲弊やアラート対応の不統一を招きます。手動のトリアージプロセスはインシデント対応を遅らせ、セキュリティオペレーションワークフローにボトルネックを生じさせます。

## 解決策
[`banshee ca`](../../reference/commands.md#banshee-ca) および [`banshee pba`](../../reference/commands.md#banshee-pba) コマンドを使用して、端末から直接 Recorded Future のアラートを取得・管理します。

- Classic Alerts の場合、時間フィルターを指定した [`banshee ca search`](../../reference/commands.md#banshee-ca-search) と、ステータスの一括変更・メモの追加・担当者の更新を行う [`banshee ca update`](../../reference/commands.md#banshee-ca-update) を使用します。

- Playbook Alerts の場合、カテゴリおよび優先度フィルターを指定した [`banshee pba search`](../../reference/commands.md#banshee-pba-search) を活用し、[`banshee pba update`](../../reference/commands.md#banshee-pba-update) でステータスの変更・コメントの追加・ユーザーの割り当て・再オープン戦略の設定を行います。

- いずれかの検索結果を [`banshee ca export`](../../reference/commands.md#banshee-ca-export) または [`banshee pba export`](../../reference/commands.md#banshee-pba-export) にパイプすることで、アラートの詳細を JSON として取得できます。また `--csv` を追加するとスプレッドシート形式のサマリーが出力され、オフラインでの報告や共有に利用できます。

このアプローチによりトリアージが高速化され、アラート対応の一貫性が保たれるとともに、一括操作によって複数のアラートを同時に更新することが可能になります。
