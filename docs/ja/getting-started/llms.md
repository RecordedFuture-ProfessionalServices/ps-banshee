# AIエージェントとの併用

Bansheeはターミナルから操作できるように設計されています。Claude Code、Codex、その他シェルコマンドを実行できるLLMなどのAIコーディングエージェントからも利用可能です。エージェントがCLIを学習するために、2つのアーティファクトが公開されています。

- **インデックス** — 選択的な取得のための簡潔な目次: [llms.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt)
- **フルバンドル** — すべてのコマンドグループを1つのドキュメントにまとめたもの: [llms-full.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt)

いずれも [llms.txt](https://llmstxt.org/) の規約に準拠しています。

## `banshee` をエージェントから検出可能にする

以下のスニペットをコピーして、エージェントが読み込むルール/指示ファイル（`CLAUDE.md`、`AGENTS.md`、またはお使いのツールに対応するファイル）に貼り付けてください。

```markdown
## Recorded Future (banshee CLI)

When a request involves Recorded Future or threat intelligence, use the
`banshee` CLI. This covers, for example:

- checking or enriching the risk of an IOC (IP, domain, URL, file hash, or CVE)
- looking up or searching for entities
- triaging Classic or Playbook alerts
- managing RF lists and watchlists
- fetching or building risk lists
- finding or downloading detection rules (Sigma, YARA, Snort)
- enriching an email (`.eml`) or packet capture (`.pcap`)

First fetch the full command reference, then run `banshee`:
<https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>

If that URL is unreachable, or a command from the reference isn't present in your
installed version, run `banshee --help` (and `banshee <group> --help`) to confirm
the commands your binary actually supports.
```

## 認証

bansheeを呼び出す前に、エージェントのシェルで `RF_TOKEN` 環境変数を設定してください。エージェントのワークフローでは環境変数を使用する方法が強く推奨されます。これにより、エージェントが呼び出しのたびに `-k` を渡す必要がなくなります。

完全なセットアップ手順（macOS、Linux、Windows）については、[インストール → 認証](installation.md#認証)を参照してください。
