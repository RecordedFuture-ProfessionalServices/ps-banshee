# Banshee CLI 知識庫

> 一款基於終端機的 Recorded Future CLI，用於威脅情報調查。
> 由 Recorded Future 的資安工程師團隊開發。
> 已針對 `ps-banshee` / `banshee` 版本 1.5.0 進行驗證。

本知識庫專為 LLM 使用（Claude Code、Opus 及其他代理型 CLI）而設計。系統為代理發布三種資產：

- **索引** — 簡潔的目錄：<https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt>
- **完整套件** — 所有指令群組內聯於單一文件：<https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>
- **各群組頁面** — 用於選擇性擷取，以原始 Markdown 形式提供，網址為 `https://.../latest/knowledge-base/<group>/index.md`（例如 `ca`、`ioc`、`list`）。連結於上方索引。

若要讓代理在專案中能夠識別 `banshee`，請在 `CLAUDE.md`、`AGENTS.md` 或等效規則檔案中加入一行以動作為導向的描述：

> 處理 Recorded Future 相關工作時，請擷取 <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt> 以取得完整的 `banshee` CLI 參考文件，然後使用 `banshee` CLI。若該 URL 無法存取，請改執行 `banshee --help`。

呼叫前請於 Shell 環境中設定 `RF_TOKEN` — 詳見下方[驗證](#authentication-global-options)說明。

---

## 驗證與全域選項

```
banshee [OPTIONS] COMMAND [ARGS]...
```

| 旗標 | 縮寫 | 說明 |
|------|-------|-------------|
| `--api-key TEXT` | `-k` | Recorded Future API 金鑰。建議改為設定 `RF_TOKEN` 環境變數。 |
| `--no-ssl-verify` | `-s` | 停用 SSL 驗證（搭配 `HTTP_PROXY` / `HTTPS_PROXY` 代理伺服器使用）。 |
| `--debug` | | 啟用除錯模式。 |
| `--version` | | 顯示版本。 |
| `--install-completion` | | 安裝 Shell 自動補全。 |
| `--show-completion` | | 列印補全設定以供手動安裝。 |

**最佳做法：** 匯出 `RF_TOKEN=<your_api_key>`，如此便無需在每次呼叫時傳入 `-k`。

---

## 就緒檢查

執行工作流程前，請先驗證本地端工具鏈與驗證路徑。

```bash
# CLI 已安裝且可存取
banshee --version
banshee --help

# Recorded Future API token 已設定
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# 大多數管線範例需要 jq
jq --version

# 唯讀 API 煙霧測試
banshee entity search wannacry -l 1
banshee ioc bulk-lookup ip 8.8.8.8 | jq '.[0] | {ioc: .entity.name, score: .risk.score}'

# 僅 pcap 工作流程需要；若未安裝 tshark，連 `banshee pcap enrich --help` 也可能失敗
command -v tshark
```

若 `banshee` 不存在，請透過核准的 Python 套件工作流程安裝 Python 套件 `ps-banshee`，然後重新執行上述檢查。

---

## 即時驗證快照

最後一次即時驗證：**2026-07-23**（1.5.0 版本刷新），針對 `ps-banshee` / `banshee` **1.5.0**，使用 `RF_TOKEN` 與 `RF_SANDBOX_TOKEN` 驗證。

驗證成功：

```bash
# 本地端工具鏈與驗證資訊確認
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"
test -n "$RF_SANDBOX_TOKEN" && echo "RF_SANDBOX_TOKEN set"

# 唯讀 API 存取
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

# 沙箱唯讀 API 存取
banshee sandbox stats --days 7
banshee sandbox list --limit 3
banshee sandbox profile list
banshee sandbox report overview 260722-x8lgjahyvx
banshee sandbox report static 260722-x8lgjahyvx
banshee sandbox report behavioral 260722-x8lgjahyvx
```

已知注意事項：

- `ca export` 與 `pba export` **僅**從 stdin 讀取，不接受位置引數。請將 `banshee ca search` / `banshee pba search` 以管線方式傳入。
- `pba export` 消費完整的 `pba search` JSON 物件（讀取 `.data[]`），而 `ca export` 消費 `ca search` JSON 陣列。
- `ca export --csv` 中的 `Updated` 欄位目前始終為空（保留供未來 API 支援），本次執行已確認。
- 新增的 `pba search --org-id`（`-o`）篩選器接受 10 個字元的 ID 或 16 個字元的 `uhash:` 格式，且可重複使用。
- `pcap enrich` 未進行即時測試，因為 `tshark` 未安裝。此為預期行為：`banshee pcap enrich --help` 會引發 `RuntimeError: tshark is not installed or not in PATH`。
- `sandbox stats` 包含 `soar_skipped` 欄位；當其為 `true` 時，`.top_iocs.verified_network` 為空（該期間未執行 SOAR 驗證）。
- 沙箱變更類指令（`submit`、`delete`、`set-profile`、`download`、`profile create/update/delete`）於本次刷新中未進行即時測試。
- `sandbox download` 產生 AES 加密的 ZIP 壓縮檔（密碼為 `infected`）；請使用 `7z x -pinfected <file>.zip` 解壓縮，標準的 `unzip` 無法可靠處理 AES 加密的 ZIP 檔案。

---

## 輸出慣例

- 所有指令預設將 **JSON 輸出**至 stdout，設計上支援管線操作。
- 在任何指令加入 `--pretty` / `-p` 可取得人類可讀的格式化輸出。
- 大多數指令支援透過 stdin 進行管線輸入（以換行或空白分隔的 ID/IOC）。
- 可結合 `jq` 進行進階篩選（全文均有範例）。
- 各端點的回應結構不同。值得注意的規律：
  - `ioc lookup` 回傳 JSON 陣列，並使用 `.risk.evidenceDetails[]` 取得詳細風險佐證。
  - `ioc bulk-lookup` 回傳 JSON 陣列，並使用 `.risk.rule.evidence[]` 取得批次風險佐證。
  - `ioc search` 回傳物件，結果位於 `.data.results[]`。
  - `pba search` 回傳物件，告警記錄位於 `.data[]`。
  - `pcap enrich` 與 `email enrich` 回傳扁平記錄，例如 `.ioc`、`.risk_score` 與 `.rule_evidence[]`。

---

## 指令群組

| 群組 | 頁面 | 說明 |
|-------|------|-------------|
| `ca` | [ca.md](ca.md) | Classic Alerts — 搜尋、查詢、更新、匯出 |
| `email` | [email.md](email.md) | 以 RF 情報豐富 EML 檔案 |
| `entity` | [entity.md](entity.md) | 實體搜尋與查詢 |
| `ioc` | [ioc.md](ioc.md) | IOC 豐富化、批次豐富化、搜尋、規則 |
| `list` | [list.md](list.md) | 管理 RF Lists 與 Watch Lists（建立、新增/移除實體、項目） |
| `pcap` | [pcap.md](pcap.md) | 以 RF 情報豐富封包擷取資料 |
| `pba` | [pba.md](pba.md) | Playbook Alerts — 搜尋、查詢、更新、匯出 |
| `risklist` | [risklist.md](risklist.md) | 擷取、建立及檢視 risk lists |
| `rules` | [rules.md](rules.md) | 搜尋並下載偵測規則（Sigma、YARA、Snort） |
| `sandbox` | [sandbox.md](sandbox.md) | 提交檔案與 URL 進行沙箱分析；擷取報告；管理設定檔；下載樣本 |

---

## LLM 注意事項

- **所有 ID 均為不透明的短字串**（例如 `tybakN`、`1b0s1q`）— 切勿猜測；請一律先透過搜尋取得。
- **PBA 告警 ID** 使用 UUID 格式，`pba search` 回傳時已包含 `task:` 前綴（`.data[].playbook_alert_id`）。請直接傳入 `pba lookup` 與 `pba update`，勿額外加上 `task:`。
- **`ca update` 與 `pba update` 回傳純文字**，而非 JSON — 每筆已更新的告警格式為 `SUCCESS:\n<ALERT_ID>`。請勿以管線傳入 `jq`。
- **stdin 管線**於所有批次/更新指令中一致適用：直接以管線傳入以換行分隔的 ID 或 IOC。
- **`--pretty` 非 JSON** — 其為人類可讀格式，不適合以 `jq` 進一步解析。管線中請勿使用。
- **Risk rules**（用於 `ioc rules`、`risklist fetch`、`risklist create`）為具名字串，例如 `recentValidatedCnc`、`analystNote`、`recentPhishing`。請使用 `banshee ioc rules <entity_type>` 探索可用的規則名稱。
- **實體 ID 與 name,type 組合**：`list bulk-add` / `list bulk-remove` 兩者皆接受 — 可使用 `SoA6SP`（RF ID）、`wannacry,Malware`（名稱 + 類型）或 `ip:8.8.8.8`（類型前綴值）。
- **`risklist create --fusion`** 會將結果直接上傳至 RF Fusion；此時 `--output-path` 被解讀為 Fusion 目的地路徑，而非本地端路徑。
- **`ioc lookup` 與 `ioc bulk-lookup` 的佐證路徑不同**：`ioc lookup` 使用 `.risk.evidenceDetails[]`；`ioc bulk-lookup` 使用 `.risk.rule.evidence[]`。兩者不可互換。