# sandbox

> 請參閱 [index.md](index.md) 了解驗證方式、就緒狀態檢查、輸出規範及共用 LLM 說明。

Sandbox 指令除 `RF_TOKEN` 外，還需要 `RF_SANDBOX_TOKEN`。設定 `RF_SANDBOX_CHOICE`（或全域的 `--sandbox-choice`）以指定目標區域：`eu`（預設）、`usa`、`apj`、`public` 或 `private`。

---

### `banshee sandbox stats`

在可設定的回顧時間窗口內彙整 sandbox 提交記錄，並輸出 SOC 晨間簡報：提交量、分數分布、熱門惡意軟體家族、平台覆蓋率、萃取的 C2 及經 SOAR 驗證的網路 IOC（網路入侵指標）。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--days INTEGER` | `-d` | `7` | 回顧時間窗口（天數，最少 1 天） |
| `--subset` | `-s` | `org` | 樣本範圍：`owned`、`public`、`org` |
| `--pretty` | `-p` | | 人類可讀的 Rich 排版 |

分數區間（分類評分 1–10 級）：

| 區間 | 分數範圍 | 含義 |
|--------|-------------|---------|
| `malicious` | 8–10 | 已知惡意軟體，高信賴度 |
| `suspicious` | 5–7 | 強烈行為指標 |
| `potentially_suspicious` | 3–4 | 部分指標 |
| `clean` | 1–2 | 低風險或無害 |

```bash
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats -d 30 | jq '.by_score'
```

**回應結構：** 回傳單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.period_start` | 彙整時間窗口的起始時間（ISO 8601） |
| `.period_end` | 彙整時間窗口的結束時間（ISO 8601） |
| `.period_days` | 回顧時間窗口（天數） |
| `.subset` | 使用的範圍（`owned`、`public`、`org`） |
| `.total` | 時間窗口內的總提交數 |
| `.pending` | 仍在分析中的提交數 |
| `.failed` | 發生錯誤的提交數 |
| `.by_kind` | 以提交類型（`file`、`url` 等）為鍵、件數為值的物件 |
| `.by_platform` | 以平台標籤為鍵、件數為值的物件 |
| `.by_score` | 以分數區間名稱為鍵、件數為值的物件 |
| `.by_file_type` | 以副檔名為鍵、件數為值的物件 |
| `.top_tags` | 包含 `malware_families`、`botnets`、`arch_file`、`behavioral_ttp` 等鍵的物件，每個鍵映射標籤名稱至件數 |
| `.top_iocs` | 包含 `extracted_c2`、`verified_network`、`malicious_sha256` 等鍵的物件，每個值為 IOC 字串陣列 |
| `.daily_by_family` | 以惡意軟體家族為鍵、每日件數為值的物件 |
| `.trend_vs_prior_period` | 包含 `total` 與 `reported` 子物件的物件，各子物件含 `current`、`prev` 及 `pct_change` |
| `.soar_skipped` | 當 SOAR 驗證被略過時為 `true`（`.top_iocs.verified_network` 將為空） |

---

### `banshee sandbox list`

列出 sandbox 樣本——您自己的、您所屬組織的（預設）或公開資料。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--subset` | `-s` | `org` | 樣本範圍：`owned`、`public`、`org` |
| `--limit INTEGER` | `-l` | `20` | 最大結果數（1–4095） |
| `--pretty` | `-p` | | 人類可讀的表格 |

```bash
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
```

**回應結構：** 回傳一個扁平 JSON 陣列，每個項目包含：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | 樣本 ID（例如 `260722-x8lgjahyvx`） |
| `.status` | 分析狀態：`pending`、`running`、`reported`、`failed` |
| `.kind` | 提交類型：`file`、`url`、`fetch`、`import` |
| `.filename` | 原始檔案名稱（URL 提交時可能為空） |
| `.submitted` | 提交時間戳記（ISO 8601） |
| `.completed` | 完成時間戳記（ISO 8601；仍在執行時不存在） |
| `.sha256` | 提交檔案的 SHA-256 雜湊值 |
| `.user_id` | 提交使用者的 UUID |

---

### `banshee sandbox search`

依結構化篩選條件（雜湊值、家族、標籤、殭屍網路、錢包、IP、網域、URL、提交日期範圍）或原始 Triage 查詢字串搜尋樣本。至少須提供一個篩選條件或 `--query`。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--hash TEXT` | | | 依檔案雜湊值篩選（MD5/SHA1/SHA256） |
| `--family TEXT` | | | 依惡意軟體家族名稱篩選 |
| `--tag TEXT` | `-T` | | 依標籤篩選（可重複） |
| `--botnet TEXT` | | | 依殭屍網路名稱篩選 |
| `--wallet TEXT` | | | 依錢包地址篩選 |
| `--ip TEXT` | | | 依 IP 位址篩選 |
| `--domain TEXT` | | | 依網域篩選 |
| `--url TEXT` | | | 依 URL 篩選 |
| `--from-date YYYY-MM-DD` | | | 篩選此日期（含）之後提交的樣本 |
| `--to-date YYYY-MM-DD` | | | 篩選此日期（含）之前提交的樣本 |
| `--query TEXT` | `-q` | | 原始 Triage 查詢字串（與結構化篩選條件以 AND 合併） |
| `--limit INTEGER` | `-l` | `50` | 最大結果數（1–200） |
| `--pretty` | `-p` | | 人類可讀的表格 |

```bash
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
```

**回應結構：** 回傳 JSON 陣列——結構與 `sandbox list` 的項目相同。

---

### `banshee sandbox get`

依 ID 擷取單一 sandbox 樣本的摘要：目前狀態、整體分數、目標、建立與完成時間戳記、SHA256 及各任務細項。對進行中及已完成的樣本均適用。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必填） | | Sandbox 樣本 ID |
| `--pretty` | `-p` | 人類可讀的 Rich 排版 |

```bash
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
```

**回應結構：** 回傳單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.sample` | 樣本 ID |
| `.status` | 分析狀態：`pending`、`running`、`static_analysis`、`reported`、`failed` |
| `.target` | 主要引爆目標（檔案名稱或 URL） |
| `.score` | 整體分類評分（1–10；分析進行中時為 `0`） |
| `.created` | 提交時間戳記（ISO 8601） |
| `.completed` | 完成時間戳記（ISO 8601；仍在執行時不存在） |
| `.sha256` | 提交檔案的 SHA-256 雜湊值（URL 提交時不存在） |
| `.owner` | 提交使用者 ID |
| `.tasks` | 以任務 ID 為鍵、值為 `{kind, status, score, tags, platform}` 的物件 |

---

### `banshee sandbox download` *(對磁碟具有變更效果)*

下載一個或多個樣本 ID 的原始提交樣本位元組。每個樣本會被封裝於以 AES 加密的 ZIP 壓縮檔中，密碼為 `infected`，以防止防毒軟體、安全電子郵件閘道或檔案管理員意外引爆。請使用 `7z x -pinfected <sample-id>.zip` 解壓縮——標準的 `unzip` 無法可靠地處理 AES 加密的 zip 檔案。

樣本 ID 可作為位置引數傳入，或透過 stdin 以管道輸入（以空白字元分隔）。除非指定 `--yes`，否則會提示確認。位元組在下載與壓縮過程中會短暫存在於此程序的記憶體中——積極的 EDR 記憶體掃描仍可能觸發警報。請在分析人員專屬的機器上執行此指令，而非日常使用的公司筆記型電腦。

| 引數/選項 | 縮寫 | 預設值 | 說明 |
|-----------------|-------|---------|-------------|
| `SAMPLE_IDS` | | | 一個或多個樣本 ID（或從 stdin 讀取） |
| `--output-dir PATH` | `-d` | （必填） | 儲存加密 zip 壓縮檔的目錄（不存在時自動建立） |
| `--yes` | `-y` | | 略過確認提示 |
| `--workers INTEGER` | `-w` | `1` | 平行下載的執行緒數（1–16） |

```bash
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
```

**回應：** stderr 輸出一次警告訊息；每個成功下載的樣本在 stderr 輸出 `[<id>] Saved: <path> (<bytes> bytes, sha256=<hex>)` 訊息；失敗時輸出 `[<id>] ERROR: <msg>`。部分失敗的批次會繼續執行至完成並以退出碼 1 結束；完全成功的批次以退出碼 0 結束。

壓縮檔內容：包含單一項目，命名為 `<sample-id>`（不猜測副檔名），內含原始樣本位元組。

---

### `banshee sandbox delete` *(具有變更效果)*

依 ID 刪除 sandbox 樣本並移除所有相關任務產出物。除非指定 `--yes`，否則會提示確認。

| 引數/選項 | 說明 |
|-----------------|-------------|
| `SAMPLE_ID`（必填） | 要刪除的樣本 ID |
| `--yes` / `-y` | 略過確認提示 |

```bash
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
```

**回應：** 成功時無輸出；以退出碼 0 結束。

---

### `banshee sandbox submit` *(具有變更效果)*

提交樣本進行分析。本機檔案會被上傳；URL 會在瀏覽器中引爆（或使用 `--fetch` 先行下載）；公開樣本可透過 `--import` 以 ID 匯入。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `TARGET`（必填） | | 檔案路徑、URL 或公開樣本 ID（搭配 `--import`） |
| `--fetch` | | 先下載 URL，再分析檔案。與 `--import` 互斥 |
| `--import` | | 將目標視為公開樣本 ID。與 `--fetch` 互斥 |
| `--profile TEXT` | | 分析設定檔名稱或 ID（可重複；與 `--interactive` 互斥） |
| `--timeout INTEGER` | `-t` | 分析逾時時間（秒，1–3600） |
| `--network` | `-N` | 網路模式：`internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | VPN 出口國家代碼；需搭配 `--network vpn` |
| `--tags TEXT` | `-T` | 自訂標籤（可重複） |
| `--password TEXT` | | 受保護壓縮檔的密碼 |
| `--wait` | `-w` | 輪詢直至分析完成，然後輸出概覽報告 |
| `--interactive` | `-i` | 在靜態分析階段暫停，以便透過 `set-profile` 選擇設定檔；與 `--profile` 互斥 |
| `--pretty` | `-p` | 人類可讀的輸出 |

```bash
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
```

**回應結構（預設）：** 回傳已提交的樣本 JSON 物件，欄位與 `sandbox list` 項目相同（`id`、`status`、`kind`、`filename`、`submitted`、`sha256`、`user_id`）。使用 `.id` 追蹤或查詢提交狀態。

**回應結構（搭配 `--wait`）：** 回傳概覽報告——結構與 `sandbox report overview` 相同。

---

### `banshee sandbox set-profile` *(具有變更效果)*

為暫停於靜態分析階段的樣本（以 `--interactive` 提交）指派分析設定檔。使用 `--auto` 讓 sandbox 自動選擇，或使用 `--pick FILE:PROFILE` 手動逐檔對應。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必填） | | 暫停於靜態分析階段的樣本 ID |
| `--auto` | `-a` | 自動為所有檔案選擇設定檔。與 `--pick` 互斥 |
| `--pick FILE:PROFILE` | | 將一個檔案對應至一個設定檔（可重複）。與 `--auto` 互斥 |
| `--pretty` | `-p` | 人類可讀的輸出 |

```bash
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
```

---

### `banshee sandbox profile list`

列出 Recorded Future Sandbox 中所有可用的分析設定檔。

| 選項 | 縮寫 | 說明 |
|--------|-------|-------------|
| `--pretty` | `-p` | 人類可讀的表格 |

```bash
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
```

**回應結構：** 回傳一個扁平 JSON 陣列，每個項目包含：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | 設定檔 UUID |
| `.name` | 設定檔名稱 |
| `.tags` | OS/地區標籤陣列（例如 `["os:windows10-2004-x64", "locale:en-us"]`） |
| `.network` | 網路模式（例如 `"internet"`、`"tor"`、`"vpn"`） |
| `.geolocation` | VPN 出口國家代碼陣列（不適用時為空） |
| `.timeout` | 分析逾時時間（秒） |
| `.options` | 包含選用欄位（如 `browser`）的物件 |

---

### `banshee sandbox profile get`

依 ID 或名稱擷取單一分析設定檔。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必填） | | 設定檔 UUID 或名稱 |
| `--pretty` | `-p` | 人類可讀的表格 |

```bash
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
```

**回應結構：** 單一設定檔物件——欄位與 `sandbox profile list` 的項目相同。

---

### `banshee sandbox profile create` *(具有變更效果)*

建立新的分析設定檔。設定檔名稱在您的組織內必須唯一。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--name TEXT` | `-n` | （必填） | 設定檔名稱（必須唯一） |
| `--tag TEXT` | `-T` | （必填） | OS/地區標籤（可重複）。地區標籤必須搭配至少一個 OS 標籤 |
| `--timeout INTEGER` | `-t` | `120` | 分析逾時時間（秒，1–3600） |
| `--network` | `-N` | | 網路模式：`internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | | VPN 出口國家代碼；需搭配 `--network vpn`（可重複） |
| `--browser` | `-b` | | 瀏覽器：`chrome`、`firefox`、`ie11`、`microsoft-edge` |
| `--pretty` | `-p` | | 人類可讀的表格 |

```bash
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
```

**回應結構：** 回傳已建立的設定檔 JSON 物件——欄位與 `sandbox profile list` 的項目相同。

---

### `banshee sandbox profile update` *(具有變更效果)*

更新現有的分析設定檔。僅您所提供的選項會被更新——未指定的選項保留原有值。使用 `--unset` 清除 `network`、`browser` 或 `geolocation`。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必填） | | 設定檔 UUID 或名稱 |
| `--name TEXT` | `-n` | 新的設定檔名稱 |
| `--tag TEXT` | `-T` | OS/地區標籤；取代所有現有標籤（可重複） |
| `--timeout INTEGER` | `-t` | 分析逾時時間（秒，1–3600） |
| `--network` | `-N` | 網路模式：`internet`、`drop`、`tor`、`vpn`、`sim200`、`sim404`、`simnx` |
| `--geolocation TEXT` | | VPN 出口國家代碼；需搭配 `--network vpn`（可重複） |
| `--browser` | `-b` | 瀏覽器：`chrome`、`firefox`、`ie11`、`microsoft-edge` |
| `--unset` | | 清除欄位：`network`、`browser` 或 `geolocation`（可重複） |
| `--pretty` | `-p` | 人類可讀的狀態訊息 |

```bash
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
```

**回應結構：** 設定檔存在且已更新時回傳 `{"updated": true}`；不存在時回傳 `{"updated": false}`。兩種情況均以退出碼 0 結束。

---

### `banshee sandbox profile delete` *(具有變更效果)*

依 ID 或名稱刪除分析設定檔。操作可安全重複執行：刪除不存在的設定檔時會輸出警告並以退出碼 0 結束。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME`（必填） | | 設定檔 UUID 或名稱 |
| `--yes` / `-y` | | 略過確認提示 |

```bash
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
```

**回應：** 成功時無輸出；以退出碼 0 結束。

---

### `banshee sandbox report overview`

擷取已完成 sandbox 樣本的完整概覽報告：判決分數、惡意軟體家族、標籤、雜湊值、偵測簽章、萃取的惡意軟體設定、網路 IOC 及各任務結果。樣本必須處於 `reported` 狀態。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必填） | | Sandbox 樣本 ID |
| `--wait` | `-w` | 輪詢最長 30 分鐘，直至報告就緒 |
| `--pretty` | `-p` | 人類可讀的摘要檢視 |

```bash
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
```

**回應結構：** 回傳單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.version` | 報告格式版本 |
| `.build` | Sandbox 建置資訊 |
| `.analysis` | 判決物件：分數、惡意軟體家族、標籤 |
| `.sample` | 樣本中繼資料：id、kind、filename、sha256、submitted、completed |
| `.signatures` | 所有任務的偵測簽章 |
| `.targets` | 引爆目標物件陣列，每個物件含 `.iocs`（網路 IOC）及惡意軟體設定萃取結果 |
| `.tasks` | 各任務摘要陣列：任務 ID、平台、狀態、判決分數 |

---

### `banshee sandbox report static`

擷取 sandbox 樣本的靜態（引爆前）分析報告：判決分數、標籤、解包檔案、靜態偵測簽章及萃取的惡意軟體設定。此報告於靜態分析完成後即可取得——無需等待行為任務完成。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必填） | | Sandbox 樣本 ID |
| `--wait` | `-w` | 輪詢最長 10 分鐘，直至報告就緒 |
| `--pretty` | `-p` | 人類可讀的摘要檢視 |

```bash
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
```

**回應結構：** 回傳單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.version` | 報告格式版本 |
| `.build` | Sandbox 建置資訊 |
| `.sample` | 樣本中繼資料：id、kind、filename、sha256、submitted |
| `.task` | 靜態任務中繼資料 |
| `.analysis` | 判決物件：分數、標籤、靜態簽章 |
| `.files` | 解包檔案陣列——每個項目含 `sha256`、`filename`、`size` 及靜態分析詳情 |
| `.unpack_count` | 從提交樣本中解包的檔案總數 |
| `.error_count` | 無法解包的檔案數量 |

---

### `banshee sandbox report behavioral`

擷取已完成 sandbox 樣本的行為（引爆後）報告，每個已完成的行為任務對應一個物件。未完成的任務會從輸出中省略並於 stderr 中注記；指令在所有任務完成前會以非零退出碼結束。當樣本無行為任務時，回傳空陣列並以退出碼 0 結束。

`--pretty` 檢視中的程序命令列預設會被截斷——若需要完整內容，請傳入 `--full-cmd`（命令列直接取自惡意軟體樣本，請視為不受信任的輸入）。

| 引數/選項 | 縮寫 | 說明 |
|-----------------|-------|-------------|
| `SAMPLE_ID`（必填） | | Sandbox 樣本 ID |
| `--wait` | `-w` | 輪詢最長 30 分鐘，直至所有任務完成 |
| `--full-cmd` | | 顯示完整未截斷的程序命令列（請視為不受信任的輸入） |
| `--pretty` | `-p` | 每個任務的人類可讀摘要檢視 |

```bash
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
```

**回應結構：** 回傳 JSON 陣列，每個項目對應一個行為任務：

| 欄位 | 說明 |
|-------|-------------|
| `.task_id` | 行為任務 ID |
| `.version` | 報告格式版本 |
| `.build` | Sandbox 建置資訊 |
| `.sample` | 樣本中繼資料：id、kind、filename、sha256 |
| `.task` | 任務中繼資料：platform、status、started、completed |
| `.analysis` | 判決物件：分數、惡意軟體家族、標籤 |
| `.tags` | 行為標籤陣列（例如 `discovery`、`execution`） |
| `.signatures` | 已觸發的偵測簽章陣列 |
| `.processes` | 觀察到的程序陣列——每個項目含 `pid`、`name`、`cmd`（除非使用 `--full-cmd` 否則截斷）及子程序 |
| `.network` | 網路活動：`.flows`（連線記錄）、`.dns`（DNS 查詢）、`.http`（HTTP 請求） |
| `.dumped` | 已傾印/萃取的檔案陣列，含各自的 SHA-256 雜湊值 |