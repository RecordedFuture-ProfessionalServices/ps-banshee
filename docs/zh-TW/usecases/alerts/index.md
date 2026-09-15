# 警報管理

## 使用案例摘要
直接從終端機管理、分流及批次更新 Recorded Future 警報（Classic & Playbook），以加速安全運營中心（SOC）的應變與調查工作流程。

## 問題
每次警報都需切換至使用者介面，導致調查延誤，造成分析師疲勞與警報處理不一致。手動分流流程拖慢了事件應變速度，並在安全運營工作流程中形成瓶頸。

## 解決方案
使用 [`banshee ca`](../../reference/commands.md#banshee-ca) 與 [`banshee pba`](../../reference/commands.md#banshee-pba) 指令，直接從終端機擷取並管理 Recorded Future 警報。

- 針對 Classic Alert，請搭配時間篩選條件使用 [`banshee ca search`](../../reference/commands.md#banshee-ca-search)，並透過 [`banshee ca update`](../../reference/commands.md#banshee-ca-update) 執行批次狀態變更、新增備註及更新受指派人。

- 針對 Playbook Alert，請搭配類別與優先順序篩選條件使用 [`banshee pba search`](../../reference/commands.md#banshee-pba-search)，再透過 [`banshee pba update`](../../reference/commands.md#banshee-pba-update) 修改狀態、新增評論、指派使用者及設定重新開啟策略。

- 可將任一搜尋結果透過管道傳入 [`banshee ca export`](../../reference/commands.md#banshee-ca-export) 或 [`banshee pba export`](../../reference/commands.md#banshee-pba-export)，以 JSON 格式擷取完整警報詳情；或加上 `--csv` 選項，以試算表格式產生摘要報告，便於離線報告與分享。

此方式可加速分流作業、維持警報處理一致性，並讓分析師能透過批次操作同時更新多筆警報。