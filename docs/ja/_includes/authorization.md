PS Banshee は、`RF_TOKEN` 環境変数（推奨）または各コマンドの `-k` / `--api-key` フラグから Recorded Future APIキーを読み取ります。

#### オプション 1: `RF_TOKEN` を設定する（推奨）

=== "macOS / Linux"

    現在のシェルのみ:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    将来のシェルに永続化する（zsh — bash の場合は `~/.bashrc` に変更してください）。実行後に新しいシェルを開くか、`source ~/.zshrc` を実行して現在のシェルに適用してください:

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    現在のセッションのみ:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    将来のセッションに永続化する（実行後に新しい PowerShell を開いてください）:

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    現在のセッションのみ:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    将来のセッションに永続化する（実行後に新しいコマンドプロンプトを開いてください）:

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

#### オプション 2: コマンドごとに `-k` で渡す

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

これはどのプラットフォームでも動作しますが、記述が冗長になり、キーがシェルの履歴に残る可能性があります。
