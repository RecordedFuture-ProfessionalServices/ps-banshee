# PS Banshee をはじめる

[PS Banshee をインストール](./installation.md)したら、[banshee](../reference/commands.md#banshee) コマンドを実行してコマンドが利用可能かどうか確認できます:

<img src="../../img/first-steps.gif" alt="PS Banshee commands" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

利用可能なコマンドを一覧表示するヘルプメニューが表示されるはずです。

### 認証

--8<-- "docs/ja/_includes/authorization.md"

### プロキシ

プロキシの背後にいる場合は、`HTTP_PROXY` および `HTTPS_PROXY` 環境変数を設定してください。

SSL 検証を無効にするには、`-s` フラグを使用します:

```bash
banshee -s ca rules
```

## 次のステップ

PS Banshee がインストールされていることを確認したら、[コマンドリファレンス](../reference/commands.md)に進んで PS Banshee の使用を開始し、問題が発生した場合は[ヘルプの取得方法](./help.md)を参照してください。
