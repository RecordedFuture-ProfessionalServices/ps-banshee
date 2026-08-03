---
title: ""
---

<div style="width: 100%; text-align: center;">
    <img src="assets/rf-logo.png" alt="Recorded Future Logo" style="margin-top: -80px; margin-bottom: 16px;">
</div>
<p style="margin-top: -60px;">
PS Banshee は、セキュリティ専門家や SOC チーム向けに構築された、Recorded Future インテリジェンスへの高速かつ効率的なアクセスを提供するコマンドラインツールです。
</p>
<img src="img/welcome.gif" alt="Welcome to PS Banshee!" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

!!! tip "PSEngine で動作"
    PS Banshee は [PSEngine](https://recordedfuture-professionalservices.github.io/psengine/latest/) ライブラリを基盤として動作しています。

---

## 主な機能

- E メール（EML）のエンリッチメント
- IOC のルックアップと検索
- パケットキャプチャ（pcap）のエンリッチメント
- Recorded Future アラートの検索・ルックアップ・更新・エクスポート
- Recorded Future 検知ルール（YARA、Snort、Sigma）の検索とダウンロード
- Recorded Future エンティティの検索とルックアップ
- Recorded Future リスト・ウォッチリストの管理
- Recorded Future Playbook アラートの検索・ルックアップ・更新・エクスポート
- Recorded Future リスクリストのダウンロードと作成

## インストール

PS Banshee は [PyPI](https://pypi.org/project/ps-banshee/) で公開されており、`pip` または `pipx` を使用してインストールできます。

!!! tip "PS Banshee には Python 3.10 以降（3.13 まで）が必要です。"

### 推奨: pipx（分離環境）
グローバルにインストールするには、次のコマンドを実行してください:

```bash
pipx install ps-banshee
```


!!! info "pipx のインストール"
    pipx がインストールされていない場合は、[インストールガイド](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)を参照してください。


### 代替手段: pip（現在の環境）
現在の環境にインストールするには、次のコマンドを実行してください:
```bash
pip install ps-banshee
```

### 依存関係

必要な Python の依存関係はすべて `pipx` によって自動的に解決されます。  
`pcap` コマンドを使用するには、以下が必要です:

- tshark 3.0.0 以降

### コマンドの自動補完

PS Banshee をインストールした後、次のコマンドでコマンドの自動補完を有効にしてください:

```bash
banshee --install-completion
```

シェルを再起動してインストールを完了してください。これで TAB キーを使用してコマンドを自動補完できるようになります。

## ドキュメント

利用可能なコマンドを表示するには、次のコマンドを実行してください:

```bash
banshee
```

### 認証

--8<-- "docs/ja/_includes/authorization.md"

### プロキシ

プロキシ環境下にある場合は、`HTTP_PROXY` および `HTTPS_PROXY` 環境変数を設定してください。

SSL 検証を無効にするには、`-s` フラグを使用してください:

```bash
banshee -s ca rules
```

## 次のステップ

今すぐ PS Banshee を[使い始めましょう](getting-started/index.md)！
