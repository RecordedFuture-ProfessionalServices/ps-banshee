# list

> 請參閱 [index.md](index.md) 以了解驗證、就緒檢查、輸出慣例及共用的 LLM 注意事項。

### `banshee list create NAME [LIST_TYPE]`

建立新清單。

| 引數／選項 | 預設值 | 說明 |
|-----------------|---------|-------------|
| `NAME`（必填） | | 清單名稱 |
| `LIST_TYPE` | `entity` | 可選值：`entity`、`source`、`text` |
| `--pretty` / `-p` | | 格式化輸出 |

```bash
banshee list create coolbeans
banshee list create coolsources source -p
```

---

### `banshee list search [NAME]`

依名稱和／或類型搜尋清單。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `NAME`（選填） | | | 依清單名稱篩選 |
| `--list-type` | `-t` | | 可選值：`entity`、`source`、`text`、`custom`、`ip`、`domain`、`tech_stack`、`industry`、`brand`、`partner`、`industry_peer`、`location`、`supplier`、`vulnerability`、`company`、`hash`、`operation`、`attacker`、`target`、`method`、`executive` |
| `--limit INTEGER` | `-l` | `1000` | 最大結果數（1–3000） |
| `--pretty` | `-p` | | 格式化輸出 |

```bash
banshee list search -l 1500 -p
banshee list search -t vulnerability
banshee list search Attacker
banshee list search ernest -t entity -p -l 3
```

**回應結構：** 回傳一個扁平的 JSON 陣列。每個項目包含以下欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.id` | 清單 ID（例如 `report:-19oM7`） |
| `.name` | 清單名稱 |
| `.type` | 清單類型：`entity`、`source`、`text` 等 |
| `.created` | 建立時間戳記（ISO 8601） |
| `.updated` | 最後更新時間戳記（ISO 8601） |
| `.owner_id` | 擁有者 uhash ID |
| `.owner_name` | 擁有者顯示名稱 |
| `.owner_organisation_details` | 組織擁有權資訊 |

---

### `banshee list info LIST_ID`

取得清單的中繼資料。

```bash
banshee list info 1b0tFN
banshee list info 1b0tFN -p
```

**回應結構：** 回傳單一 JSON 物件，欄位集與 `list search` 結果中的項目相同：`id`、`name`、`type`、`created`、`updated`、`owner_id`、`owner_name`、`organisation_id`、`organisation_name`、`owner_organisation_details`。

---

### `banshee list status LIST_ID`

取得清單的處理／同步狀態。

```bash
banshee list status 1b0tFN
```

**回應結構：** 回傳包含兩個欄位的單一 JSON 物件：

| 欄位 | 說明 |
|-------|-------------|
| `.status` | 處理狀態字串（例如 `"ready"`） |
| `.size` | 目前清單中的實體數量 |

---

### `banshee list entities LIST_ID`

擷取清單中目前所有的實體。

```bash
banshee list entities 1b0s1q
```

**回應結構：** 回傳一個扁平的 JSON 陣列。每個項目包含以下欄位：

| 欄位 | 說明 |
|-------|-------------|
| `.entity.id` | RF 實體 ID |
| `.entity.name` | 實體顯示名稱 |
| `.entity.type` | 實體類型字串 |
| `.status` | 實體在清單中的狀態（例如 `"ready"`） |
| `.added` | 實體加入時間戳記（ISO 8601） |

```bash
# Extract all entity IDs on a list
banshee list entities report:6P8708 | jq -r '.[].entity.id'

# Get entity names and types
banshee list entities report:6P8708 | jq '[.[] | {name: .entity.name, type: .entity.type}]'
```

---

### `banshee list entries LIST_ID`

擷取清單中的文字比對條目（適用於 `text` 類型的清單）。

```bash
banshee list entries 1b0s1q
```

---

### `banshee list add LIST_ID ENTITY_ID [PROPERTIES]`

將單一實體加入清單。

| 引數 | 說明 |
|----------|-------------|
| `LIST_ID`（必填） | 清單 ID |
| `ENTITY_ID`（必填） | RF 實體 ID（例如 `SoA6SP`）或 `name,type` 組合（例如 `wannacry,Malware`） |
| `PROPERTIES`（選填） | 使用 `annotation=<text>` 為該實體附加備註，備註將顯示於 Recorded Future 平台上。若值包含空格，請以引號括住。 |

```bash
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
```

---

### `banshee list bulk-add LIST_ID [ENTITY_INPUT]...`

將多個實體加入清單。接受實體 ID、`name,type` 組合或 `type:value` 組合。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | 關閉 | 覆寫模式：保留輸入中存在的實體、加入新實體，並移除目前清單中**不在**輸入範圍內的所有實體。若未啟用此選項，指令僅附加新實體，不會移除現有實體。 |

**輸入格式：**
- RF 實體 ID：`SoA6SP`
- 名稱 + 類型：`wannacry,Malware` 或 `www.duckdns.org,InternetDomainName`
- 類型前綴值：`ip:8.8.8.8`

```bash
banshee list bulk-add report:21YKUC SoA6SP lYNvCK
banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# Overwrite mode: make the list match exactly the entities supplied (adds missing, removes stale)
banshee list bulk-add 21YKUC SoA6SP lYNvCK --overwrite

# From file (one entity per line)
banshee list bulk-add 21YKUC < entities.txt
cat entities.txt | banshee list bulk-add 21YKUC
```

**回應：** 純文字，依結果分組——`ADDED:`、`REMOVED:`（僅限覆寫模式）及 `UNCHANGED:` 區塊，列出受影響的實體。非 JSON 格式；請勿透過管線傳至 `jq`。

---

### `banshee list remove LIST_ID ENTITY_ID`

從清單中移除單一實體。

```bash
banshee list remove 1b0s1q lYNvCK
```

---

### `banshee list bulk-remove LIST_ID [ENTITY_INPUT]...`

從清單中移除多個實體。輸入格式與 `bulk-add` 相同。

```bash
banshee list bulk-remove 21YKUC JLHNoH lYNvCK
banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# From file
banshee list bulk-remove 21YKUC < entities.txt
cat entities.txt | banshee list bulk-remove 21YKUC
```

---

### `banshee list copy SOURCE_LIST_ID DESTINATION_LIST_ID`

將一個清單中的實體複製至另一個清單。來源清單的實體將被讀取並加入目的地清單。

| 選項 | 縮寫 | 預設值 | 說明 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | 關閉 | 覆寫模式：保留兩個清單中共有的實體、加入新實體，並移除目的地清單中**不在**來源清單內的所有實體。若未啟用此選項，實體僅會附加至目的地清單，不會移除任何實體。 |

若來源清單為空，即使使用 `--overwrite`，指令也會直接結束而不修改目的地清單。

```bash
banshee list copy 1b0s1q 21YKUC

# Make the destination mirror the source exactly (adds missing, removes stale)
banshee list copy 1b0s1q 21YKUC --overwrite
```

**回應：** 純文字，依結果分組——`ADDED:`、`REMOVED:`（僅限覆寫模式）及 `UNCHANGED:` 區塊，列出受影響的實體。非 JSON 格式；請勿透過管線傳至 `jq`。

---

### `banshee list clear LIST_ID`

移除清單中的**所有**實體（具破壞性——請謹慎使用）。文字比對條目無法透過 API 移除。清單本身不會被刪除，僅移除其中的實體。

```bash
banshee list clear 1b0s1q
```

**回應：** 純文字。當清單已為空時顯示 `No entities to remove`；成功時顯示 `Successfully removed <N> entities`；若有任何移除失敗，則顯示 `<N> entities were not removed from the list:`，並列出仍存在的實體。非 JSON 格式。