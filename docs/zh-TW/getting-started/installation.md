# 安裝 PS Banshee

## 安裝方式

使用 `pipx` 或 `pip` 安裝 [ps-banshee](https://pypi.org/project/ps-banshee/)。

## 安裝

!!! tip "PS Banshee 需要 Python 3.10 或更新版本（最高支援 3.13）。"

### 建議方式：pipx（隔離環境）
若要全域安裝，請執行：

```bash
pipx install ps-banshee
```


!!! info "安裝 pipx"
    若您尚未安裝 pipx，請參閱 [安裝指南](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)。


### 替代方式：pip（當前環境）
若要在當前環境中安裝，請執行：
```bash
pip install ps-banshee
```


### 相依套件

所有必要的 Python 相依套件均由 `pip` 自動解析。  
若要使用 `pcap` 指令，請確保您已安裝：

- tshark 3.0.0 或更新版本



## 授權

PS Banshee 從 `RF_TOKEN` 環境變數（建議）或每個指令的 `-k` / `--api-key` 旗標中讀取您的 Recorded Future API 金鑰。

### 選項 1：設定 `RF_TOKEN`（建議）

=== "macOS / Linux"

    僅限當前 Shell：

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    持久套用於未來的 Shell（zsh — bash 請改為 `~/.bashrc`）。執行後請開啟新的 Shell（或執行 `source ~/.zshrc` 以套用至當前 Shell）：

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    僅限當前工作階段：

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    持久套用於未來的工作階段（執行後請開啟新的 PowerShell）：

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    僅限當前工作階段：

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    持久套用於未來的工作階段（執行後請開啟新的 Command Prompt）：

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

### 選項 2：每個指令透過 `-k` 傳入

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

此方式適用於任何平台，但較為繁瑣，且金鑰可能會留存於 Shell 歷史記錄中。

## 升級 PS Banshee

若要將 PS Banshee 升級至較新版本，請使用更新後的 wheel 檔案重新安裝。

!!! warning "從 v1.0.0 或更早版本升級"
    若您正從 v1.0.0 或更早版本升級，必須先解除安裝現有套件，再安裝新版本。

    **若使用 pipx 安裝：**
    ```bash
    pipx uninstall banshee 
    pipx install ps-banshee
    ```

    **若使用 pip 安裝：**
    ```bash
    pip uninstall banshee
    pip install ps-banshee
    ```

**若使用 pipx 安裝：**

```bash
pipx install --force ps-banshee
```

**若使用 pip 安裝：**

```bash
pip install --upgrade ps-banshee
```

## Shell 自動補全

安裝 PS Banshee 後，請執行以下指令啟用指令自動補全：

```bash
banshee --install-completion
```

重新啟動 Shell 以完成安裝。現在您可以使用 TAB 鍵自動補全指令。

## 解除安裝

若要從系統移除 PS Banshee，請根據您的安裝方式執行對應的指令。

**若使用 pipx 安裝：**

```bash
pipx uninstall ps-banshee
```

**若使用 pip 安裝：**

```bash
pip uninstall ps-banshee
```


## 後續步驟

請參閱 [初始步驟](./first-steps.md) 以開始使用 PS Banshee。