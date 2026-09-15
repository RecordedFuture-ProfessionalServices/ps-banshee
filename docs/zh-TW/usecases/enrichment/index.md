# IOC Enrichment

## Use Case Summary
以 Recorded Future 風險評分、相關實體及分析師情境資訊豐富化入侵指標（IOC），以加速安全運作中心（SOC）的分類作業與威脅調查。

如需更多有關 IOC enrichment 的資訊，請點擊[此處](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future)。

## Issue
分析師需在多項工具之間來回查找 IP 位址、網域、URL、雜湊值及漏洞資訊，導致調查速度減慢並延長回應時間。手動比對來自多個來源的威脅情資，易造成分析缺口並延誤事件回應。

## Solution
使用 [`banshee ioc`](../../reference/commands.md#banshee-ioc) 指令，直接在 PS Banshee 中豐富化 IOC 資訊。查詢個別指標以取得風險評分、AI 洞察，以及威脅行為者與惡意程式的關聯。透過多種篩選選項搜尋 IOC，以識別高風險指標。善用豐富化後的情境資訊，了解組織所面臨的威脅，並加速事件回應決策。