# PS Banshee のインストール

## インストール方法

`pipx` または `pip` を使用して [ps-banshee](https://pypi.org/project/ps-banshee/) をインストールします。

## インストール

!!! tip "PS Banshee には Python 3.10 以降（3.13 まで）が必要です。"

### 推奨: pipx（隔離環境）
グローバルにインストールするには、次のコマンドを実行します:

```bash
pipx install ps-banshee
```


!!! info "pipx のインストール"
    pipx がインストールされていない場合は、[インストールガイド](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx) を参照してください。


### 代替方法: pip（現在の環境）
現在の環境にインストールするには、次のコマンドを実行します:
```bash
pip install ps-banshee
```


### 依存関係

必要な Python の依存関係はすべて `pip` によって自動的に解決されます。  
`pcap` コマンドを使用するには、以下が必要です:

- tshark 3.0.0 以降



## 認証

PS Banshee は、`RF_TOKEN` 環境変数（推奨）または各コマンドの `-k` / `--api-key` フラグから Recorded Future API キーを読み取ります。

### オプション 1: `RF_TOKEN` を設定する（推奨）

=== "macOS / Linux"

    現在のシェルのみ:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    将来のシェルにも反映させる場合（zsh — bash の場合は `~/.bashrc` に変更してください）。実行後に新しいシェルを開くか、現在のシェルに適用するには `source ~/.zshrc` を実行してください:

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    現在のセッションのみ:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    将来のセッションにも反映させる場合（実行後に新しい PowerShell を開いてください）:

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    現在のセッションのみ:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    将来のセッションにも反映させる場合（実行後に新しいコマンドプロンプトを開いてください）:

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

### オプション 2: コマンドごとに `-k` で渡す

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

これはどのプラットフォームでも動作しますが、より冗長になり、キーがシェルの履歴に残る可能性があります。

## PS Banshee のアップグレード

PS Banshee を新しいバージョンにアップグレードするには、更新されたホイールファイルを使用して再インストールします。

!!! warning "v1.0.0 以前からのアップグレード"
    v1.0.0 またはそれ以前のバージョンからアップグレードする場合は、新しいバージョンをインストールする前に既存のパッケージをアンインストールする必要があります。

    **pipx でインストールした場合:**
    ```bash
    pipx uninstall banshee 
    pipx install ps-banshee
    ```

    **pip でインストールした場合:**
    ```bash
    pip uninstall banshee
    pip install ps-banshee
    ```

**pipx でインストールした場合:**

```bash
pipx install --force ps-banshee
```

**pip でインストールした場合:**

```bash
pip install --upgrade ps-banshee
```

## シェルの自動補完

PS Banshee をインストールした後、次のコマンドでコマンドの自動補完を有効にします:

```bash
banshee --install-completion
```

インストールを完了するためにシェルを再起動してください。これで TAB キーを使用してコマンドを自動補完できます。

## アンインストール

システムから PS Banshee を削除するには、インストール方法に応じた適切なコマンドを使用してください。

**pipx でインストールした場合:**

```bash
pipx uninstall ps-banshee
```

**pip でインストールした場合:**

```bash
pip uninstall ps-banshee
```


## 次のステップ

PS Banshee の使用を開始するには、[最初のステップ](./first-steps.md) を参照してください。
