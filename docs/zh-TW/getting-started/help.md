# 取得協助

## 說明選單

`--help`、`-h` 旗標可用於檢視指令的說明選單，例如 [banshee](../reference/commands.md#banshee)：

```bash
banshee --help
```

若要檢視特定指令的說明選單，例如 [banshee pcap](../reference/commands.md#banshee-pcap)：

```bash
banshee pcap --help
```

## 檢視版本

在尋求協助時，確認目前所使用的 ps-banshee 套件版本非常重要——有時問題已在較新的版本中獲得解決。

若要確認已安裝的版本：

```bash
banshee --version
```

## 疑難排解

若指令以非預期的方式失敗，可使用 `--debug` 旗標以取得更詳細的錯誤資訊：

```bash
banshee --debug ioc search ip -p
```

輸出結果將精確顯示指令失敗的位置。此資訊可提供給支援團隊，以協助排查問題。

## 向 Recorded Future Support 提交支援案例

請提交[支援請求](https://support.recordedfuture.com/hc/en-us/requests/new)以取得協助，或直接聯繫 [support@recordedfuture.com](mailto:support@recordedfuture.com)。