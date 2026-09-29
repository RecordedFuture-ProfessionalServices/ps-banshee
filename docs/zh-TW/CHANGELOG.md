# 發行歷程

## 1.6.0 - 2026-09-15
### 新增
- 新增 [`email extract-attachments`](reference/commands.md#banshee-email-extract-attachments) 子指令，可從 EML 檔案中擷取附件、儲存至受密碼保護的壓縮檔，並提交至 Recorded Future Sandbox 進行分析。

## 1.5.0 - 2026-08-21

### 新增
- 新增 [`sandbox`](reference/commands.md#banshee-sandbox) 指令，用於與 Recorded Future sandbox 互動。


## v.1.4.1 - 2026-07-13

### 變更
- 更新 `psengine` 相依套件版本。


## v.1.4.0 - 2026-07-13

### 新增
- 為 [`risklist stat`](reference/commands.md#banshee-risklist-stat) 新增 [`-C`/`--count`](reference/commands.md#banshee-risklist-stat--count) 選項，可下載 risk list（風險清單）並列印每個風險分數對應的指標數量表格。

## v1.3.1 - 2026-06-30

### 變更
- 更新相依套件版本。

## 1.3.0 - 2026-06-15

### 新增
- 新增 [`email enrich`](reference/commands.md#banshee-email-enrich) 子指令，透過擷取 EML 檔案中的標頭 IP 及內文 URL 來進行豐富化，並回傳 Recorded Future 情報，包含風險分數、威脅行為者關聯、惡意軟體連結及風險規則證據。
- 新增 [`ca export`](reference/commands.md#banshee-ca-export) 子指令，可將 Classic Alerts 匯出為完整 JSON 或摘要 CSV 格式。從 [`ca search`](reference/commands.md#banshee-ca-search) 透過管道傳入的告警 ID 讀取資料。
- 新增 [`pba export`](reference/commands.md#banshee-pba-export) 子指令，可將 Playbook Alerts 匯出為完整 JSON 或摘要 CSV 格式。從 [`pba search`](reference/commands.md#banshee-pba-search) 透過管道傳入的搜尋結果讀取資料。
- 為 [`pba search`](reference/commands.md#banshee-pba-search) 新增 [`-o`/`--org-id`](reference/commands.md#banshee-pba-search--org-id) 選項，可依擁有者組織 ID 篩選 Playbook Alerts（可重複使用）。
- 為 [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 新增 [`-o`/`--overwrite`](reference/commands.md#banshee-list-bulk-add--overwrite) 選項，使清單內容完全符合所提供的實體——新增未存在的實體，並移除目前清單中未提供的實體。
- 新增 [`list copy`](reference/commands.md#banshee-list-copy) 子指令，可將實體從一個清單複製到另一個清單。預設為附加模式，或使用 [`-o`/`--overwrite`](reference/commands.md#banshee-list-copy--overwrite) 使目標清單完全鏡像來源清單。
- 支援[與 AI 代理程式搭配使用 banshee](getting-started/llms.md)，讓程式碼輔助工具能夠探索並執行此 CLI。

### 變更
- [`list clear`](reference/commands.md#banshee-list-clear) 現在以並發方式移除實體（在大型清單上速度顯著提升），與 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) 行為一致：回報已移除的實體，依結果（`REMOVED` 及無法移除的項目）分組輸出，並排序以提升可讀性。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 現在會略過已在清單中的實體，而非嘗試重新新增，並將其回報為 `UNCHANGED`。這在重複執行相同輸入檔案以新增及移除實體時，可大幅提升速度。
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 和 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) 現在依結果（`ADDED`、`REMOVED`、`UNCHANGED`）分組輸出，並排序以提升可讀性。
- [`ca search`](reference/commands.md#banshee-ca-search) 和 [`pba search`](reference/commands.md#banshee-pba-search) 現在將進度指示寫入 stderr，保持 stdout 整潔以便管道傳入新的 `export` 指令。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 和 [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) 的美化輸出（`-p`、`--pretty`）現在依惡意程度對風險分數進行色彩標示。
- 升級 PSEngine 至 ~v2.8.1。

### 修正
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 和 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) 現在會忽略空白輸入行，並在未提供任何實體時回報明確的錯誤訊息。

## 1.1.3 - 2026-03-18

### 修正
- 修正 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) 中多執行緒未用於 SOAR 豐富化的問題。大型封包擷取的風險分數豐富化速度現已提升。


## 1.1.0 - 2026-03-13

### 新增
- 新增 [`risklist create`](reference/commands.md#banshee-risklist-create) 子指令，可透過合併一個或多個 Recorded Future 風險規則來建立自訂 risk list，並產生去重複的單一檔案。支援 CSV、JSON 及 EDL 輸出格式、可選的最低風險分數篩選，以及直接上傳至 Recorded Future Fusion。
- 新增 [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) 子指令，可快速批次豐富化 IOC（入侵指標）。每次 API 呼叫最多批次處理 1,000 個指標，並回傳每個指標的風險分數及觸發的風險規則。支援所有 IOC 類型：IP、網域、URL、雜湊值及漏洞。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON 輸出現在包含風險規則證據詳細資訊，說明導致風險規則觸發的具體證據。

### 變更
- [`entity search`](reference/commands.md#banshee-entity-search) 預設結果上限提升至 100 筆。
- [`list search`](reference/commands.md#banshee-list-search) 預設結果上限提升至 1,000 筆。
- [`pba search`](reference/commands.md#banshee-pba-search) 預設結果上限提升至 50 筆。
- [`pba search`](reference/commands.md#banshee-pba-search) 最大結果上限提升至 10,000 筆。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) 現在接受低至 1 的風險分數。

### 修正
- 修正 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 中多執行緒未被使用的問題，該問題導致批次查詢依序執行。豐富化多個指標時，查詢速度最高可提升 20 倍。
- 修正 [`risklist fetch`](reference/commands.md#banshee-risklist-fetch) 在解析 CSV 檔案中異常大的欄位值時指令失敗的問題。
- 修正 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) 在解析空白 IOC 連結時失敗的問題。
- 修正 [`list`](reference/commands.md#banshee-list) 指令在發生 API 錯誤時未能正確印出錯誤原因的問題。

## 1.0.0 - 2025-12-05

### 新增

- 新增 [`risklist`](reference/commands.md#banshee-risklist) 指令，用於下載及查看 Recorded Future Risk Lists 的中繼資料。
- 新增 [`rules`](reference/commands.md#banshee-rules) 指令，用於搜尋及下載偵測規則（YARA、Snort、Sigma）。
- 在 [`ioc search`](reference/commands.md#banshee-ioc-search) 和 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 指令中新增 CVSS v4 欄位支援。

### 修正

- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 和 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) 現在會對使用者提供的實體進行去重複處理。
- 修正 [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 和 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) 中含有空格的實體名稱未能正確解析的問題。
- [`pba lookup`](reference/commands.md#banshee-pba-lookup) 現在能正確處理圖片擷取失敗的告警。

### 變更

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON 輸出現在包含風險規則證據詳細資訊，以及 IOC 所觸發的所有風險規則。
- 升級 PSEngine 至 v2.4.0。


## 0.0.5 - 2025-11-12

## 修正

- 修正 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) 在 pcap 檔案中找不到任何 IP 或網域時程式意外結束的問題。

## 0.0.4 - 2025-11-07

### 新增

- 新增在 [`ca search`](reference/commands.md#banshee-ca-search) 指令中依告警狀態篩選的支援。
- 新增在 [`pba search`](reference/commands.md#banshee-pba-search) 指令中依實體篩選的支援。
- 新增所有 `pba` 指令對 `malware_report` 類別的支援。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 和 [`ioc search`](reference/commands.md#banshee-ioc-search) 的美化輸出（`-p`、`--pretty`）現在包含雜湊值的雜湊演算法資訊。
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 和 [`ioc search`](reference/commands.md#banshee-ioc-search) 的美化輸出（`-p`、`--pretty`）現在包含漏洞的生命週期階段資訊。
- 新增 `-r`/`--risk-score` 選項至 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)，可依風險分數篩選結果。
- 新增 `-t`/`--threat-hunt` 選項至 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)，可啟用威脅獵捕功能。

### 變更

- 最佳化 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 各詳細程度等級的欄位選擇。
- 擴充 [`ioc search`](reference/commands.md#banshee-ioc-search) 以支援詳細程度等級 1 至 5（預設為 1）。
- 將子指令 `pcap analyze` 更名為 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)。
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) 現在產生精煉後的 JSON 輸出，包含相容於 Wireshark 的篩選查詢。
- 升級 PSEngine 至 v2.3.0。

### 修正

- 修正 [`ca rules`](reference/commands.md#banshee-ca-rules) 將結果截斷至 10 條告警規則的問題。
- 修正 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 在 IOC 無證據詳細資訊時發生錯誤的問題。

### 移除

- 移除 `pba enrich` 的互動式 TUI 輸出，改以美化輸出（`--pretty`、`-p`）取代。


## 0.0.3 - 2025-09-02

### 新增

- 新增 [`ca update`](reference/commands.md#banshee-ca-update) 子指令，用於更新一個或多個 Classic Alerts。
- 新增 [`pba update`](reference/commands.md#banshee-pba-update) 子指令，用於更新一個或多個 Playbook Alerts。
- [`pba`](reference/commands.md#banshee-pba) 指令現在支援 `geopolitics_facility` 類別。
- 相容於 Python 3.13。
- `tshark` 版本檢查現在強制要求最低版本 4.4.5。

### 修正

- `pcap analyze` 不再因版本不符而發生崩潰。
- 改善整個 CLI 的例外處理機制。

### 變更

- `ioc search ENTITY_TYPE IOC` 現在接受以空白字元分隔的 IOC，而非逗號分隔字串。
- `pba lookup ALERT_ID -p` 輸出格式已改善。
- `ca search --triggered` 現在支援時間範圍。
- `ca search -r` 現在接受透過重複 `-r` 指定多個規則（例如 `-r rule1 -r rule2`），而非逗號分隔字串。
- 升級 PSEngine 至 v2.0.6。


## 0.0.2 - 2025-02-20

### 新增

- 新增 [`entity`](reference/commands.md#banshee-entity) 指令，用於搜尋及查詢實體。
- 新增 [`list`](reference/commands.md#banshee-list) 指令，用於管理 Recorded Future Lists 與 Watch Lists。
- 新增 [`ioc rules`](reference/commands.md#banshee-ioc-rules) 子指令，用於搜尋及篩選 IOC 規則。
- 新增 `--debug` 選項，提供進階疑難排解功能。


### 變更

- 子指令 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 的 ``-v`` 選項現在允許使用者選擇詳細程度等級（1 至 5）。
- 子指令 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 現在需要實體類型作為引數，例如 ``banshee ioc lookup ip 8.8.8.8``。
- 子指令 [`ca lookup`](reference/commands.md#banshee-ca-lookup) 現在回傳精煉後的美化告警內容。
- PSEngine 升級至 v2.0.2。


## 0.0.1 - 2024-09-01

### 新增

- Beta 版本發行。

---

🚀 由 Recorded Future 的網路安全工程師團隊為您呈現。