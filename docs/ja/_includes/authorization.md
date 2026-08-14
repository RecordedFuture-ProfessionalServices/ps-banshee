PS Banshee は、`RF_TOKEN` 環境変数（推奨）または各コマンドの `-k` / `--api-key` フラグから Recorded Future API キーを読み取ります。

#### Option 1: `RF_TOKEN` を設定する（推奨）

=== "macOS / Linux"

    現在のシェルのみ有効：

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    将来のシェルにも反映させる場合（zsh の場合。bash の場合は `~/.bashrc` に変更してください）。実行後に新しいシェルを開くか、現在のシェルに適用するには `source ~/.zshrc` を実行してください：

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    現在のセッションのみ有効：

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    将来のセッションにも反映させる場合（実行後に新しい PowerShell を開いてください）：

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    現在のセッションのみ有効：

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    将来のセッションにも反映させる場合（実行後に新しい Command Prompt を開いてください）：

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

#### Option 2: コマンドごとに `-k` で渡す

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

この方法はどのプラットフォームでも使用できますが、記述が冗長になるほか、キーがシェルの履歴に残る可能性があります。