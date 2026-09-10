# Risk Lists

## 使用案例摘要
直接從終端機擷取並建立 Recorded Future Risk Lists（風險清單），以支援豐富化、關聯分析及自動化偵測。分析師可依需求提取具風險評分的 IP、網域、URL、雜湊值或漏洞，或將多條風險規則合併為單一自訂清單，確保 SOC 工作流程始終使用最新的威脅情資。

## 問題
SOC 團隊在進行調查、偵測或主動封鎖時，往往需要取得最新的風險評分指標。在多個平台之間切換或手動匯出清單會造成摩擦，並拖慢回應速度。一套直接擷取的方法可提升速度與一致性。

## 解決方案
使用 [`banshee risklist`](../../reference/commands.md#banshee-risklist) 指令在 PS Banshee 中擷取 Risk Lists。指定實體類型與清單名稱，即可取得 Recorded Future 的預設、大型或特定規則的風險清單。將結果儲存至本機，以便自動匯入 SIEM 或 SOAR 豐富化管線。可選擇附加 `--as-json` 參數，以 JSON 格式輸出清單，供支援 JSON 匯入的系統使用，確保整合流程順暢，無需手動轉換。

使用 [`banshee risklist create`](../../reference/commands.md#banshee-risklist-create) 將一條或多條風險規則合併為單一去重複化輸出，藉此建立自訂風險清單。可依最低風險評分進行篩選、選擇 CSV、EDL 或 JSON 等輸出格式，並可選擇將結果直接上傳至 Recorded Future Fusion。