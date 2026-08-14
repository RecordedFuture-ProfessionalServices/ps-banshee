# ヘルプの取得

## ヘルプメニュー

`--help`、`-h` フラグを使用して、コマンドのヘルプメニューを表示できます。例えば、[banshee](../reference/commands.md#banshee) の場合:

```bash
banshee --help
```

特定のコマンドのヘルプメニューを表示するには、例えば [banshee pcap](../reference/commands.md#banshee-pcap) の場合:

```bash
banshee pcap --help
```

## バージョンの確認

サポートを求める際は、使用している ps-banshee パッケージのバージョンを確認することが重要です — 問題がすでに新しいバージョンで解決されている場合があります。

インストール済みのバージョンを確認するには:

```bash
banshee --version
```

## 問題のトラブルシューティング

コマンドが予期しない方法で失敗している場合にエラーの詳細を得るには、`--debug` フラグを使用できます:

```bash
banshee --debug ioc search ip -p
```

出力には、コマンドが失敗している正確な箇所が表示されます。この情報をサポートチームに提供することで、問題のトラブルシューティングに役立てることができます。

## Recorded Future サポートへのサポートケースの申請

[サポートリクエスト](https://support.recordedfuture.com/hc/en-us/requests/new)を送信してサポートを受けるか、[support@recordedfuture.com](mailto:support@recordedfuture.com) までお問い合わせください。
