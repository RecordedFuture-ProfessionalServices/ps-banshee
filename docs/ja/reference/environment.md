# 環境変数

PS Banshee は以下のセクションで説明する環境変数を使用します。

### `RF_TOKEN`

PS Banshee が Recorded Future API に対して認証を行うには、API トークンが必要です。ユーザーはトークンを環境変数として設定することができます:


```bash
export RF_TOKEN=API-TOKEN
```

 または、`banshee` コマンドに直接 `-k` または `--api-key` 引数として渡すこともできます:

```bash
banshee -k API-TOKEN ca search
```


### `HTTP_PROXY`

組織がプロキシの使用を必要とする場合は、`HTTP_PROXY` を設定してください。例:

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
```

詳細については [requests のドキュメント](https://requests.readthedocs.io/en/latest/user/advanced/#proxies) をご参照ください。

### `HTTPS_PROXY`

組織がプロキシの使用を必要とする場合は、`HTTPS_PROXY` を設定してください。例:

```bash
export HTTPS_PROXY="http://10.10.1.10:1080"
```
詳細については [requests のドキュメント](https://requests.readthedocs.io/en/latest/user/advanced/#proxies) をご参照ください。


!!! Tip

    プロキシ環境変数のいずれかを使用する場合、SSL 検証を無効にする必要があるかもしれません。これは `banshee` コマンドに直接 `-s`、`--no-ssl-verify` フラグを渡すことで実現できます。例:

    $ banshee -s ca search
