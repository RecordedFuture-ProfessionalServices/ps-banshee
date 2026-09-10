# 監看清單管理

## 使用案例摘要
使用 Recorded Future 監看清單（Watch Lists）來維護精選的高優先級實體（公司、網域、IP、漏洞、高階主管、供應商），使警報與情資聚焦於安全維運中心（SOC）最關切的事項。

如需進一步了解 Watch Lists 的相關資訊，請點擊[此處](https://support.recordedfuture.com/hc/en-us/articles/115005092427-Watch-Lists)。

## 問題
威脅環境與業務優先事項持續變化。若未主動維護 Watch Lists，警報與情資的範圍可能過於廣泛，使分析人員難以迅速聚焦於最關鍵的事項。

## 解決方案
使用 [`banshee list`](../../reference/commands.md#banshee-list) 指令，直接在 PS Banshee 中建立並維護 Watch Lists。可透過上傳 CSV 進行批量變更、逐一新增實體，或針對新實體請求人工篩選。將 Watch Lists 對應至情資目標（Intelligence Goals），確保僅觸發相關警報。在整合或重新組織清單時，可使用 [`banshee list copy`](../../reference/commands.md#banshee-list-copy) 將實體從一個清單合併至另一個清單（可選擇搭配 `--overwrite` 選項）。定期審查並更新清單內容（品牌、網域、高階主管、供應商、漏洞、地點等），以確保覆蓋範圍能反映持續演變的風險態勢。