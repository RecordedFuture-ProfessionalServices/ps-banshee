# Banshee CLI ナレッジベース

> Recorded Future のターミナルベースの脅威インテリジェンス調査のための CLI ツールです。
> Recorded Future のサイバーセキュリティエンジニアが開発しました。
> `ps-banshee` / `banshee` バージョン 1.3.0 で検証済み。

このナレッジベースは LLM による利用（Claude Code、Opus、その他のエージェント型 CLI）を想定して設計されています。エージェント向けに以下の 3 つのアーティファクトが公開されています。

- **Index** — 簡潔な目次: <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms.txt>
- **Full bundle** — すべてのコマンドグループを 1 つのドキュメントにまとめたもの: <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt>
- **Per-group pages** — 選択的なフェッチ用。`https://.../latest/knowledge-base/<group>/index.md` (例: `ca`、`ioc`、`list`) で生のマークダウンとして提供されます。上記インデックスからリンクされています。

プロジェクト内でエージェントが `banshee` を発見できるようにするには、`CLAUDE.md`、`AGENTS.md`、または同等のルールファイルにアクション指向の一行を追加してください。

> Recorded Future を使用する際は、完全な `banshee` CLI リファレンスを取得するために <https://recordedfuture-professionalservices.github.io/ps-banshee/latest/llms-full.txt> をフェッチし、その後 `banshee` CLI を使用してください。その URL に到達できない場合は、代わりに `banshee --help` を実行してください。

呼び出す前にシェル環境に `RF_TOKEN` を設定してください。詳細は以下の[認証](#認証とグローバルオプション)を参照してください。

---

## 認証とグローバルオプション

```
banshee [OPTIONS] COMMAND [ARGS]...
```

| フラグ | 短縮形 | 説明 |
|------|-------|-------------|
| `--api-key TEXT` | `-k` | Recorded Future API キー。推奨: 代わりに `RF_TOKEN` 環境変数を設定してください。 |
| `--no-ssl-verify` | `-s` | SSL 検証を無効にします（`HTTP_PROXY` / `HTTPS_PROXY` 経由のプロキシで使用）。 |
| `--debug` | | デバッグモードを有効にします。 |
| `--version` | | バージョンを表示します。 |
| `--install-completion` | | シェルのタブ補完をインストールします。 |
| `--show-completion` | | 手動インストール用の補完設定を表示します。 |

**ベストプラクティス:** `RF_TOKEN=<your_api_key>` をエクスポートして、すべての呼び出しで `-k` を渡す必要がないようにしてください。

---

## 準備状態の確認

ワークフローを実行する前に、ローカルのツールチェーンと認証パスを確認してください。

```bash
# CLI がインストールされ、アクセス可能であることを確認
banshee --version
banshee --help

# Recorded Future API トークンが存在することを確認
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# jq はほとんどのパイプラインの例で必要
jq --version

# 読み取り専用 API のスモークテスト
banshee entity search wannacry -l 1
banshee ioc bulk-lookup ip 8.8.8.8 | jq '.[0] | {ioc: .entity.name, score: .risk.score}'

# pcap ワークフローでのみ必要。tshark なしでは `banshee pcap enrich --help` も失敗する可能性があります
command -v tshark
```

`banshee` が見つからない場合は、承認済みの Python パッケージワークフローを通じて Python パッケージ `ps-banshee` をインストールし、上記の確認を再実行してください。

---

## ライブ検証スナップショット

最終ライブ検証: **2026-06-12**（リリース 1.3.0 更新）、`ps-banshee` / `banshee` **1.3.0** と `RF_TOKEN` 認証で実施。

検証成功:

```bash
# ローカルツールチェーンと認証の存在確認
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# 読み取り専用 API アクセス
banshee ca rules
banshee ca rules leaked
banshee ca search -t 7d
banshee ca search -t 12h | banshee ca export
banshee ca search -t 12h | banshee ca export --csv
banshee pba search -C 60d -l 3
banshee pba search -o uhash:69sKLfTGsS -C 60d -l 3
banshee pba search -C 60d -l 3 | banshee pba export
banshee pba search -C 60d -l 3 | banshee pba export --csv
banshee ioc bulk-lookup ip 8.8.8.8
```

確認された注意点:

- `ca export` と `pba export` は **stdin からのみ** 読み込み、位置引数は取りません。`banshee ca search` / `banshee pba search` をこれらにパイプしてください。
- `pba export` は完全な `pba search` JSON オブジェクト（`.data[]` を読み込む）を消費しますが、`ca export` は `ca search` の JSON 配列を消費します。
- `ca export --csv` では `Updated` 列が現在常に空になっています（将来の API サポートのために予約済み）— 今回の実行で確認済み。
- 新しい `pba search --org-id`（`-o`）フィルターは 10 文字の ID または 16 文字の `uhash:` 形式を受け付け、繰り返し指定が可能です。
- `tshark` がインストールされていなかったため、`pcap enrich` はライブテストされていません。これは想定内です: `banshee pcap enrich --help` は `RuntimeError: tshark is not installed or not in PATH` を発生させます。

---

## 出力の規則

- すべてのコマンドはデフォルトで **JSON 出力** を stdout に出力します — パイプラインに適した設計です。
- 人間が読みやすいフォーマットの出力には、任意のコマンドに `--pretty` / `-p` を追加してください。
- ほとんどのコマンドは stdin 経由のパイプ（改行またはスペース区切りの ID/IOC）をサポートしています。
- 高度なフィルタリングには `jq` と組み合わせてください（全体を通じて例を示しています）。
- レスポンスの形状はエンドポイントによって異なります。主なパターン:
  - `ioc lookup` は JSON 配列を返し、詳細なリスク証拠には `.risk.evidenceDetails[]` を使用します。
  - `ioc bulk-lookup` は JSON 配列を返し、バルクリスク証拠には `.risk.rule.evidence[]` を使用します。
  - `ioc search` は `.data.results[]` 以下に結果を持つオブジェクトを返します。
  - `pba search` は `.data[]` 以下にアラートレコードを持つオブジェクトを返します。
  - `pcap enrich` と `email enrich` は `.ioc`、`.risk_score`、`.rule_evidence[]` などのフラットなレコードを返します。

---

## コマンドグループ

| グループ | ページ | 説明 |
|-------|------|-------------|
| `ca` | [ca.md](ca.md) | Classic Alerts — 検索、ルックアップ、更新、エクスポート |
| `email` | [email.md](email.md) | RF インテリジェンスで EML ファイルを強化 |
| `entity` | [entity.md](entity.md) | エンティティの検索とルックアップ |
| `ioc` | [ioc.md](ioc.md) | IOC の強化、バルク強化、検索、ルール |
| `list` | [list.md](list.md) | RF リストとウォッチリストの管理（作成、エンティティの追加/削除、エントリ） |
| `pcap` | [pcap.md](pcap.md) | RF インテリジェンスでパケットキャプチャを強化 |
| `pba` | [pba.md](pba.md) | Playbook Alerts — 検索、ルックアップ、更新、エクスポート |
| `risklist` | [risklist.md](risklist.md) | リスクリストの取得、作成、検査 |
| `rules` | [rules.md](rules.md) | 検出ルールの検索とダウンロード（Sigma、YARA、Snort） |

---

## LLM 向け注意事項

- **すべての ID は不透明な短い文字列**です（例: `tybakN`、`1b0s1q`）— 推測しないでください。常に最初に検索で取得してください。
- **PBA アラート ID** は UUID 形式を使用し、`pba search`（`.data[].playbook_alert_id`）によって既に `task:` プレフィックスが付いた状態で返されます。`pba lookup` と `pba update` にはそのまま渡してください — `task:` を追加しないでください。
- **`ca update` と `pba update` はプレーンテキストを返します**（JSON ではありません）— 更新されたアラートごとに `SUCCESS:\n<ALERT_ID>` です。`jq` にパイプしないでください。
- **stdin パイプ** はすべてのバルク/更新コマンドで一貫しています: 改行区切りの ID または IOC を直接パイプしてください。
- **`--pretty` は JSON ではありません** — 人間が読みやすい形式であり、`jq` でのさらなる解析には適していません。パイプラインでは省略してください。
- **リスクルール**（`ioc rules`、`risklist fetch`、`risklist create` で使用）は `recentValidatedCnc`、`analystNote`、`recentPhishing` のような名前付き文字列です。利用可能なルール名は `banshee ioc rules <entity_type>` で確認してください。
- **エンティティ ID vs. 名前とタイプのペア**: `list bulk-add` / `list bulk-remove` は両方を受け付けます — `SoA6SP`（RF ID）、`wannacry,Malware`（名前 + タイプ）、または `ip:8.8.8.8`（タイプ付きの値）。
- **`risklist create --fusion`** は結果を RF Fusion に直接アップロードします。`--output-path` はローカルパスではなく Fusion の保存先パスとして解釈されます。
- **`ioc lookup` と `ioc bulk-lookup` の証拠パスは異なります**: `ioc lookup` は `.risk.evidenceDetails[]` を使用し、`ioc bulk-lookup` は `.risk.rule.evidence[]` を使用します。これらは互換性がありません。
