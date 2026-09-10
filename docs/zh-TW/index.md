---
title: ""
---

<div style="width: 100%; text-align: center;">
    <img src="assets/rf-logo.png" alt="Recorded Future Logo" style="margin-top: -80px; margin-bottom: 16px;">
</div>
<p style="margin-top: -60px;">
PS Banshee 是一款命令列工具，專為安全專業人員與 SOC 團隊打造，可快速、高效地存取 Recorded Future Intelligence。
</p>
<img src="img/welcome.gif" alt="Welcome to PS Banshee!" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

!!! tip "Powered by PSEngine"
    PS Banshee 由 [PSEngine](https://recordedfuture-professionalservices.github.io/psengine/latest/) 程式庫驅動。

---

## 主要功能

- 電子郵件（EML）擴充分析
- IOC（入侵指標）查詢與搜尋
- 封包擷取（pcap）擴充分析
- Recorded Future Alert 搜尋、查詢、更新與匯出
- Recorded Future Detection Rules（YARA、Snort、Sigma）搜尋與下載
- Recorded Future 實體搜尋與查詢
- Recorded Future List 與 Watch List 管理
- Recorded Future Playbook Alert 搜尋、查詢、更新與匯出
- Recorded Future Risk List 下載與建立

## 安裝

PS Banshee 已發布於 [PyPI](https://pypi.org/project/ps-banshee/)，可使用 `pip` 或 `pipx` 進行安裝。

!!! tip "PS Banshee 需要 Python 3.10 或更新版本（最高支援至 3.13）。"

### 建議方式：pipx（隔離環境）
若要全域安裝，請執行：

```bash
pipx install ps-banshee
```


!!! info "安裝 pipx"
    若尚未安裝 pipx，請參閱[安裝指南](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)。


### 替代方式：pip（當前環境）
若要在當前環境中安裝，請執行：
```bash
pip install ps-banshee
```

### 相依套件

所有必要的 Python 相依套件均由 `pipx` 自動解析。  
若要使用 `pcap` 指令，請確保已安裝：

- tshark 3.0.0 或更新版本

### 指令自動補全

安裝 PS Banshee 後，可透過以下方式啟用指令自動補全：

```bash
banshee --install-completion
```

重新啟動 Shell 以完成安裝。之後即可使用 TAB 鍵自動補全指令。

## 說明文件

若要檢視可用指令，請執行：

```bash
banshee
```

### 授權驗證

--8<-- "_includes/authorization.md"

### 代理伺服器

若您位於 Proxy 後方，請設定 `HTTP_PROXY` 與 `HTTPS_PROXY` 環境變數。

若要停用 SSL 驗證，請使用 `-s` 旗標：

```bash
banshee -s ca rules
```

## 後續步驟

立即[開始使用](getting-started/index.md) PS Banshee！