PS Banshee 從 `RF_TOKEN` 環境變數（建議方式）或每個指令的 `-k` / `--api-key` 旗標讀取您的 Recorded Future API 金鑰。

#### Option 1: 設定 `RF_TOKEN`（建議方式）

=== "macOS / Linux"

    僅限當前 shell：

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    持久套用至未來的 shell（zsh — bash 請改為 `~/.bashrc`）。執行後請開啟新的 shell（或執行 `source ~/.zshrc` 以在當前 shell 中套用）：

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    僅限當前工作階段：

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    持久套用至未來的工作階段（執行後請開啟新的 PowerShell）：

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    僅限當前工作階段：

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    持久套用至未來的工作階段（執行後請開啟新的命令提示字元）：

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

#### Option 2: 透過每個指令的 `-k` 傳入

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

此方式適用於任何平台，但較為繁瑣，且金鑰可能會留存於 shell 歷史記錄中。