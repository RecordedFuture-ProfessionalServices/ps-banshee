# 封包擷取豐富化

## 使用案例摘要
使用 Recorded Future 情報對封包擷取檔案及觀測到的 IP/網域進行豐富化，以加速網路安全調查與威脅獵捕活動。

## 問題
原始 PCAP 顯示網路流量，但缺乏威脅情境。分析師必須手動查詢 IP/網域以識別風險或威脅活動，此過程耗時且在大量調查期間容易產生疏漏。

## 解決方案
直接在 PS Banshee 中使用 [`banshee pcap`](../../reference/commands.md#banshee-pcap) 指令對網路流量進行豐富化。使用 [`banshee pcap enrich`](../../reference/commands.md#banshee-pcap-enrich) 自動解析封包擷取檔案、以威脅情報對觀測到的指標進行豐富化，並直接在終端機中顯示結果。將豐富化後的 IOC（入侵指標）透過管道傳輸至 [`banshee ioc lookup`](../../reference/commands.md#banshee-ioc-lookup) 以進行深入分析，或將高風險指標加入 Watch List 以進行長期追蹤與監控。