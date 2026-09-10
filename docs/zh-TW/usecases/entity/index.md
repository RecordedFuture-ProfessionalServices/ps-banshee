# 實體比對

## 使用案例摘要
搜尋並解析 Recorded Future 實體（公司、惡意軟體、威脅行為者等），以確保在安全運營中心（SOC）工具與工作流程中保持一致的參照方式。

如需進一步了解 Recorded Future 實體，請點擊[此處](https://support.recordedfuture.com/hc/en-us/articles/115001359567-What-is-an-Entity)。

## 問題
自由文字名稱可能導致工具與 Recorded Future 之間產生不符的情況。威脅行為者實體可能與使用者名稱實體擁有相同名稱，但其實體 ID 將有所不同，進而造成混淆並導致錯誤的威脅情報關聯。

## 解決方案
直接在 PS Banshee 中使用 [`banshee entity`](../../reference/commands.md#banshee-entity) 命令來搜尋並解析實體。

- 當您擁有實體名稱和／或類型，且需要找到對應的實體 ID 時，請使用 [`banshee entity search`](../../reference/commands.md#banshee-entity-search)。

- 當您擁有實體 ID，且需要取得名稱與類型時，請使用 [`banshee entity lookup`](../../reference/commands.md#banshee-entity-lookup)。

取得正確的實體 ID 後，請將其用於後續的 PS Banshee 命令，例如 [`banshee list add`](../../reference/commands.md#banshee-list-add)，以確保在貴組織的監控清單（watchlist）中準確參照實體。