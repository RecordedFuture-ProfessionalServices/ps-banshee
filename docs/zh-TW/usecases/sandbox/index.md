# 沙箱分析

## 使用案例摘要
透過 Recorded Future Sandbox 提交檔案與 URL 進行自動化惡意程式分析、擷取分析報告，並將已驗證的樣本移交供離線分析使用，以加速安全作業中心（SOC）的分類處理與威脅調查。

## 問題
分析師需要在安全、受控的環境中引爆可疑檔案與 URL，以判斷其意圖並提取威脅指標（IOC）。若缺乏整合式工作流程，收集與關聯分析結果——包括靜態特徵、行為活動、網路 IOC 及惡意程式設定——將需要跨多個工具進行手動操作，從而拖慢 SOC 的應變速度。

## 解決方案
透過 PS Banshee 中的 [`banshee sandbox`](../../reference/commands.md#banshee-sandbox) 命令，直接提交樣本並擷取報告。

- 使用 [`banshee sandbox submit`](../../reference/commands.md#banshee-sandbox-submit) 提交本機檔案、URL 或公開樣本進行分析。加入 [`--wait`](../../reference/commands.md#banshee-sandbox-submit--wait) 可持續輪詢至分析完成並立即輸出概覽報告；加入 [`--interactive`](../../reference/commands.md#banshee-sandbox-submit--interactive) 則可在靜態分析階段暫停，並在繼續執行前選擇引爆設定檔。

- 分析完成後，可使用 [`banshee sandbox report overview`](../../reference/commands.md#banshee-sandbox-report-overview) 取得研判結果、惡意程式家族、網路 IOC 及各項任務結果的摘要；使用 [`banshee sandbox report static`](../../reference/commands.md#banshee-sandbox-report-static) 取得引爆前分析結果及提取的惡意程式設定；使用 [`banshee sandbox report behavioral`](../../reference/commands.md#banshee-sandbox-report-behavioral) 取得引爆後的活動資訊，包括觸發的特徵規則、觀察到的處理程序及提取的 C2。

- 使用 [`banshee sandbox stats`](../../reference/commands.md#banshee-sandbox-stats) 產生 SOC 晨會摘要，顯示可設定回溯時間範圍內的提交量、評分分布、主要惡意程式家族及網路 IOC，適合用於班次交接或每日分類作業。

- 使用 [`banshee sandbox list`](../../reference/commands.md#banshee-sandbox-list) 檢視來自自身帳號、所屬組織或公開來源的近期提交記錄；使用 [`banshee sandbox get`](../../reference/commands.md#banshee-sandbox-get) 查看任一樣本的目前狀態、整體評分及各任務細項，而無需擷取完整報告。

- 使用 [`banshee sandbox search`](../../reference/commands.md#banshee-sandbox-search) 依雜湊值、惡意程式家族、標籤、殭屍網路、錢包、網路指標（IP、網域、URL）或提交日期範圍，對歷史提交記錄進行樞紐分析。可透過 `--query` 傳入原始 Triage 查詢字串，支援 `AND`/`OR`/`NOT` 運算式。

- 使用 [`banshee sandbox download`](../../reference/commands.md#banshee-sandbox-download) 擷取原始提交位元組以供離線分析（YARA/Sigma 調校、EDR 偵測測試、攻擊活動歸因）。每個樣本均以 AES 加密的 ZIP 壓縮檔封裝，密碼為 `infected`——請使用 `7z x -pinfected <sample-id>.zip` 解壓縮。位元組在下載與壓縮過程中會短暫存在於處理程序記憶體中，因此請在分析師專屬的主機上執行此操作。

- 使用 [`banshee sandbox delete`](../../reference/commands.md#banshee-sandbox-delete) 在不再需要時刪除樣本及其相關成品。

- 對於使用自訂引爆環境的團隊，[`banshee sandbox profile`](../../reference/commands.md#banshee-sandbox-profile) 命令可讓您建立、更新及刪除分析設定檔，以控制套用至每次提交的作業系統、網路設定、瀏覽器及分析逾時設定。