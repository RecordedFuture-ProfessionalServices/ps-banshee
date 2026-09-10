# 與 AI 代理搭配使用

Banshee 設計為可從終端機驅動，包括由 Claude Code、Codex 及其他任何可執行 shell 指令的 LLM 等 AI 編碼代理驅動。此處發布了兩個輔助文件，協助代理學習 CLI：

- **Index** — 簡明的目錄，可供選擇性擷取：[llms.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt)
- **Full bundle** — 所有指令群組內嵌於單一文件中：[llms-full.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt)

兩者皆遵循 [llms.txt](https://llmstxt.org/) 慣例。

## 讓代理能夠探索到 `banshee`

複製以下程式碼片段，並貼入代理所讀取的規則／指示檔案中，例如 `CLAUDE.md`、`AGENTS.md` 或對應工具的同等檔案：

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

## 授權驗證

在呼叫 banshee 之前，請於代理的 shell 中設定 `RF_TOKEN` 環境變數。在代理工作流程中，強烈建議使用環境變數方式，如此代理便無需在每次呼叫時都記得傳遞 `-k` 參數。

完整的設定說明（macOS、Linux、Windows）請參閱[安裝 → 授權驗證](installation.md#authorization)。