# Detection Rules

## 使用案例摘要
允許分析師與偵測工程師根據威脅行為者、惡意軟體、MITRE ATT&CK 技術、建立日期或 Threat Map 中定義的實體，快速搜尋與篩選 Recorded Future 的偵測規則（YARA、Snort、Sigma）。結果可在終端機中檢視，或儲存為個別規則檔案以供部署使用。

## 問題
在威脅獵捕或事件回應過程中，分析師需要快速、精準地存取相關的偵測規則。跨平台或在大型規則儲存庫中進行手動搜尋耗時費力，且難以將規則與活躍威脅、優先威脅行為者或技術相互對應。

## 解決方案
直接在 PS Banshee 中使用 [`banshee rules`](../../reference/commands.md#banshee-rules) 命令搜尋、篩選並擷取偵測規則。可依規則類型、威脅行為者、惡意軟體家族、ATT&CK 技術等條件進行篩選。透過 Threat Map 篩選功能（`--threat-actor-map`、`--threat-malware-map`），將搜尋範圍聚焦於與組織相關的威脅。使用 `--limit` 最多可擷取 1000 條規則，並可選擇將規則檔案儲存起來，以便快速部署至 SIEM、IDS/IPS 或偵測工程工作流程中。