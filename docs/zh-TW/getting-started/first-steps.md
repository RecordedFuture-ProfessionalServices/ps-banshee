# PS Banshee 入門指南

[安裝 PS Banshee](./installation.md) 後，您可以執行 [banshee](../reference/commands.md#banshee) 命令來確認相關命令是否可用：

<img src="../../img/first-steps.gif" alt="PS Banshee commands" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

您應該會看到一個列出可用命令的說明選單。

### 授權

--8<-- "_includes/authorization.md"

### 代理伺服器

若您位於代理伺服器後方，請設定 `HTTP_PROXY` 與 `HTTPS_PROXY` 環境變數。

若要停用 SSL 驗證，請使用 `-s` 旗標：

```bash
banshee -s ca rules
```

## 後續步驟

確認 PS Banshee 已成功安裝後，請前往[命令參考文件](../reference/commands.md)開始使用 PS Banshee，並了解如何在遇到任何問題時[取得協助](./help.md)。