# 環境變數

PS Banshee 使用以下各節所述的環境變數。

### `RF_TOKEN`

為使 PS Banshee 能夠通過 Recorded Future API 的授權驗證，需要提供 API token。使用者可以將 token 設定為環境變數：

```bash
export RF_TOKEN=API-TOKEN
```

或直接以 `-k` 或 `--api-key` 引數傳遞給 `banshee` 指令：

```bash
banshee -k API-TOKEN ca search
```


### `HTTP_PROXY`

若貴組織要求使用 Proxy，請確保設定 `HTTP_PROXY`，例如：

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
```

如需更多資訊，請參閱 [requests 說明文件](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)。

### `HTTPS_PROXY`

若貴組織要求使用 Proxy，請確保設定 `HTTPS_PROXY`，例如：

```bash
export HTTPS_PROXY="http://10.10.1.10:1080"
```

如需更多資訊，請參閱 [requests 說明文件](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)。


!!! Tip

    若使用上述任一 Proxy 環境變數，可能需要停用 SSL 驗證。可透過在 `banshee` 指令中直接傳遞 `-s`、`--no-ssl-verify` 旗標來達成，例如：

    $ banshee -s ca search