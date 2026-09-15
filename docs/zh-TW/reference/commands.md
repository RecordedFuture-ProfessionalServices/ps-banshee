# 命令列參考

## banshee

PS Banshee 是一款命令列工具，專為安全專業人員與 SOC 團隊設計，提供快速、高效的 Recorded Future 情報存取能力。

<h3 class="commands-reference">用法</h3>

```
banshee [OPTIONS] <COMMAND>
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca"><code>banshee ca</code></a></dt><dd><p>搜尋、查詢及更新 Recorded Future Classic Alerts</p></dd>
    <dt><a href="#banshee-email"><code>banshee email</code></a></dt><dd><p>以 Recorded Future 情報豐富化電子郵件檔案 (EML)</p></dd>
    <dt><a href="#banshee-entity"><code>banshee entity</code></a></dt><dd><p>搜尋及查詢 Recorded Future 實體</p></dd>
    <dt><a href="#banshee-ioc"><code>banshee ioc</code></a></dt><dd><p>搜尋及查詢入侵指標（IOC）</p></dd>
    <dt><a href="#banshee-list"><code>banshee list</code></a></dt><dd><p>管理 Recorded Future 清單與監控清單（Watch list）</p></dd>
    <dt><a href="#banshee-pba"><code>banshee pba</code></a></dt><dd><p>搜尋、查詢及更新 Recorded Future Playbook Alerts</p></dd>
    <dt><a href="#banshee-pcap"><code>banshee pcap</code></a></dt><dd><p>解析封包擷取（pcap）檔案，並以 Recorded Future 情報進行豐富化分析</p></dd>
    <dt><a href="#banshee-risklist"><code>banshee risklist</code></a></dt><dd><p>管理 Risk Lists（風險清單）</p></dd>
    <dt><a href="#banshee-rules"><code>banshee rules</code></a></dt><dd><p>搜尋並下載偵測規則</p></dd>
</dl>

## banshee ca

搜尋、查詢及更新 Recorded Future Classic Alerts

<h3 class="commands-reference">用法</h3>

```
banshee ca [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca-lookup"><code>banshee ca lookup</code></a></dt><dd><p>查詢單一 Classic Alert</p></dd>
    <dt><a href="#banshee-ca-search"><code>banshee ca search</code></a></dt><dd><p>搜尋 Classic Alerts</p></dd>
    <dt><a href="#banshee-ca-rules"><code>banshee ca rules</code></a></dt><dd><p>搜尋 Classic Alert 規則</p></dd>
    <dt><a href="#banshee-ca-update"><code>banshee ca update</code></a></dt><dd><p>更新一或多筆 Classic Alert</p></dd>
    <dt><a href="#banshee-ca-export"><code>banshee ca export</code></a></dt><dd><p>將 Classic Alerts 匯出為 JSON 或 CSV 格式</p></dd>
</dl>

### banshee ca lookup

查詢單一 Classic Alert。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ca lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--alert-id"><a href="#banshee-ca-lookup--alert-id"><code>ALERT_ID</code></a></dt><dd><p>要查詢的 Alert ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ca-lookup--help"><a href="#banshee-ca-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee ca search

搜尋 Classic Alerts。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ca search [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-search--triggered"><a href="#banshee-ca-search--triggered"><code>--triggered</code>, <code>-t</code></a> <i>triggered</i></dt><dd>
    <p>依觸發時間篩選，例如：1d；12h；[2024-08-01, 2024-08-14]；[2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)</p>
    <p>預設為 1d</p><dd></dd>
    <dt id="banshee-ca-search--rule"><a href="#banshee-ca-search--rule"><code>--rule</code></a> <i>rule-name</i></dt><dd>
    <p>依警報規則名稱篩選（自由文字）</p><dd></dd>
    <dt id="banshee-ca-search--status"><a href="#banshee-ca-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>依警報狀態篩選</p>
    <p>可用值：<code>New</code>、<code>Pending</code>、<code>Dismissed</code>、<code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-search--pretty"><a href="#banshee-ca-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ca-search--help"><a href="#banshee-ca-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee ca rules

搜尋 Classic Alert 規則。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ca rules [OPTIONS] [FREETEXT]
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--freetext"><a href="#banshee-ca-rules--freetext"><code>FREETEXT</code></a></dt><dd><p>選用。用於依名稱篩選警報規則的自由文字。</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--pretty"><a href="#banshee-ca-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ca-rules--help"><a href="#banshee-ca-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee ca update

更新一或多筆 Classic Alert

<h3 class="commands-reference">用法</h3>

```
banshee ca update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--alert-id"><a href="#banshee-ca-update--alert-id"<code>ALERT_IDS</code></a></dt><dd><p>一或多個以空白字元分隔的 Alert ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--status"><a href="#banshee-ca-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>將警報更新為指定的警報狀態</p>
    <p>可用值：<code>New</code>、<code>Pending</code>、<code>Dismissed</code>、<code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-update--note"><a href="#banshee-ca-update--note"><code>--note</code></a>,  <code>-n</code> <i>note</i></dt><dd>
    <p>警報的備註文字。</p><p>備註長度限制為 1000 個字元</p><dd></dd>
    <dt id="banshee-ca-update--append"><a href="#banshee-ca-update--append"><code>--append</code></a>,  <code>-a</code></dt><dd>
    <p>若警報已有備註，此旗標將在現有備註後附加新的備註文字</p><dd></dd>
    <dt id="banshee-ca-update--assignee"><a href="#banshee-ca-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>將警報指派給新使用者。接受使用者的 uhash 或電子郵件地址，例如：uhash:3aXZxdkM12、analyst@acme.com</p><dd></dd>
    <dt id="banshee-ca-update--help"><a href="#banshee-ca-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<p>提供一或多個 Alert ID（以空白字元分隔），並指定所需的更新選項：</p>

<pre><code class="language-bash">
banshee ca update <alert id> -s Dismissed
banshee ca update <alert id> -s Dismissed -n "note text"
banshee ca update <alert id1> <alert id2>-s Dismissed -n "note text" -a analyst@acme.com
</code></pre>

<h3 class="commands-reference">提供 Alert ID 的方式</h3>

<h4>1. 直接作為引數傳入（單筆或多筆）：</h4>

<pre><code class="language-bash">
banshee ca update ALERT_ID -s Resolved
banshee ca update ALERT_ID_1 ALERT_ID_2 -s Pending
</code></pre>

<h4>2. 從檔案或標準輸入讀取：</h4>

<p>若您有一個每行一筆 Alert ID 的檔案（例如 <code>alerts.txt</code>）：</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>可使用以下命令更新所有列出的警報：</p>

<pre><code class="language-bash">
banshee ca update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee ca update -s Dismissed
</code></pre>

<h4>3. 透過搜尋命令的管道傳入：</h4>

<p>使用 <code>jq</code> 等工具從搜尋結果中提取 Alert ID，並透過管道傳入更新命令：</p>

<pre><code class="language-bash">
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"
</code></pre>

<h3 class="commands-reference">備註附加</h3>

<p>Classic Alerts 僅支援單一備註。預設情況下，<code>update</code> 命令會以新備註覆蓋現有備註。
若希望改為附加新備註，請使用 <code>--append</code>（<code>-A</code>）選項。</p>

### banshee ca export

將 Classic Alerts 匯出為 JSON 或 CSV 格式。從 stdin 讀取警報 ID——通常透過管道從 [`banshee ca search`](#banshee-ca-search) 傳入。

<h3 class="commands-reference">輸出格式</h3>

<p><b>JSON（預設）</b>——為每個 ID 輸出 Recorded Future API 回傳的<i>完整</i>警報物件：包含所有頂層欄位及巢狀的命中記錄、實體、證據、AI insights、審閱歷史記錄、入口網站 URL 等。適合用於下游工具、<code>jq</code> 管道或資料重新匯入。</p>

<p><b>CSV（<a href="#banshee-ca-export--csv"><code>--csv</code></a>）</b>——輸出適用於試算表和報告的高層次摘要。僅寫入以下十一個欄位（首行為標題列）；JSON 回應中的其他所有欄位均省略。</p>

| 欄位 | 說明 |
|---|---|
| `ID` | Classic Alert ID |
| `Priority` | 警報優先級——若警報規則為優先規則則為 `High`，否則為 `Informational` |
| `Alert Rule` | 觸發的警報規則名稱 |
| `Status` | 入口網站狀態，例如 `New`、`Pending`、`Dismissed`、`Resolved` |
| `Created` | 觸發時間戳記（UTC） |
| `Updated` | 最後更新時間戳記——*目前固定為空；保留供未來 API 支援使用* |
| `Title` | 警報標題 |
| `Assignee` | 被指派的使用者（uhash 或電子郵件） |
| `URL` | 該警報的 Recorded Future 入口網站 URL |
| `Entities` | 主要實體名稱，以 `;` 分隔 |
| `Recorded Future AI Insights` | AI 生成的 insight 文字或備註 |

<h3 class="commands-reference">用法</h3>

```
banshee ca search [SEARCH_OPTIONS] | banshee ca export [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-export--csv"><a href="#banshee-ca-export--csv"><code>--csv</code></a></dt><dd>
    <p>以上述固定欄位集輸出為 CSV。若未指定此旗標，命令將輸出 JSON。</p><dd></dd>
    <dt id="banshee-ca-export--help"><a href="#banshee-ca-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">管道輸入</h3>

<p><code>banshee ca export</code> 僅接受管道輸入。它會消費由 <a href="#banshee-ca-search"><code>banshee ca search</code></a> 產生的 JSON 陣列，提取警報 ID 後逐一完整擷取每筆警報。若未透過管道執行此命令，將回傳錯誤並拒絕執行。</p>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s New | banshee ca export --csv > alerts.csv
</code></pre>

## banshee entity

搜尋及查詢 Recorded Future 實體

<h3 class="commands-reference">用法</h3>

```
banshee entity [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-entity-lookup"><code>banshee entity lookup</code></a></dt><dd><p>依 ID 查詢實體</p></dd>
    <dt><a href="#banshee-entity-search"><code>banshee entity search</code></a></dt><dd><p>依名稱及／或類型搜尋實體</p></dd>
</dl>

### banshee entity lookup

依 ID 查詢實體

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee entity lookup [OPTIONS] ENTITY_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--entity-id"><a href="#banshee-entity-lookup--entity-id"<code>ENTITY_ID</code></a></dt><dd><p>要查詢的實體 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--pretty"><a href="#banshee-entity-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-entity-lookup--help"><a href="#banshee-entity-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee entity search

依名稱及／或類型搜尋實體

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee entity search [OPTIONS] NAME
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--name"><a href="#banshee-entity-search--name"><code>NAME</code></a></dt><dd><p>要搜尋的實體名稱</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--type"><a href="#banshee-entity-search--type"><code>--type</code>, <code>-t</code></a> <i>entity-type</i></dt><dd>
    <p>要搜尋的實體類型</p>
    <p>可重複指定以篩選不同的實體類型</p>
    <p>支援的值：</p>
    <ul>
        <li><code>ASNumber</code></li>
        <li><code>AWSAccessKey</code></li>
        <li><code>Aircraft</code></li>
        <li><code>Airport</code></li>
        <li><code>AnalystNote</code></li>
        <li><code>Anniversary</code></li>
        <li><code>AttackVector</code></li>
        <li><code>BankIdentificationNumber</code></li>
        <li><code>BitcoinAddress</code></li>
        <li><code>BusinessIdentifierCode</code></li>
        <li><code>Case</code></li>
        <li><code>Category</code></li>
        <li><code>City</code></li>
        <li><code>CodeIdentifier</code></li>
        <li><code>Commodity</code></li>
        <li><code>Company</code></li>
        <li><code>ContentType</code></li>
        <li><code>Continent</code></li>
        <li><code>Country</code></li>
        <li><code>Currency</code></li>
        <li><code>CurrencyPair</code></li>
        <li><code>CyberExploitTargetCategory</code></li>
        <li><code>CyberSecurityCategory</code></li>
        <li><code>CyberThreatActorCategory</code></li>
        <li><code>CyberVulnerability</code></li>
        <li><code>DEANumber</code></li>
        <li><code>Dataset</code></li>
        <li><code>DetectionRule</code></li>
        <li><code>Document</code></li>
        <li><code>EconomicIndicator</code></li>
        <li><code>EmailAddress</code></li>
        <li><code>Embassy</code></li>
        <li><code>Emoji</code></li>
        <li><code>EntertainmentAwardEvent</code></li>
        <li><code>Entity</code></li>
        <li><code>EntityAlias</code></li>
        <li><code>EntityList</code></li>
        <li><code>EntityRange</code></li>
        <li><code>EntityRelation</code></li>
        <li><code>ExternalIdentifier</code></li>
        <li><code>Facility</code></li>
        <li><code>FaxNumber</code></li>
        <li><code>Feature</code></li>
        <li><code>FileContent</code></li>
        <li><code>FileName</code></li>
        <li><code>FileNameExtension</code></li>
        <li><code>FileType</code></li>
        <li><code>GeoBoundingBox</code></li>
        <li><code>GeoEntity</code></li>
        <li><code>Hash</code></li>
        <li><code>HashAlgorithm</code></li>
        <li><code>Hashtag</code></li>
        <li><code>Holiday</code></li>
        <li><code>IRCNetwork</code></li>
        <li><code>Identifier</code></li>
        <li><code>Image</code></li>
        <li><code>IncidentImpactCategory</code></li>
        <li><code>Industry</code></li>
        <li><code>IndustryTerm</code></li>
        <li><code>IntegrationApplication</code></li>
        <li><code>IntegrationUser</code></li>
        <li><code>InternetDomainName</code></li>
        <li><code>IpAddress</code></li>
        <li><code>Keyword</code></li>
        <li><code>Language</code></li>
        <li><code>LinkReport</code></li>
        <li><code>Logotype</code></li>
        <li><code>MICR</code></li>
        <li><code>Malware</code></li>
        <li><code>MalwareCategory</code></li>
        <li><code>MalwareMutex</code></li>
        <li><code>MalwareSignature</code></li>
        <li><code>MarketIndex</code></li>
        <li><code>MedicalCondition</code></li>
        <li><code>MedicalTreatment</code></li>
        <li><code>MetaAttribute</code></li>
        <li><code>MetaType</code></li>
        <li><code>MilitaryBase</code></li>
        <li><code>MilitaryExercise</code></li>
        <li><code>MitreAttackIdentifier</code></li>
        <li><code>Movie</code></li>
        <li><code>MusicAlbum</code></li>
        <li><code>MusicGroup</code></li>
        <li><code>Nationality</code></li>
        <li><code>NaturalFeature</code></li>
        <li><code>Neighborhood</code></li>
        <li><code>NetworkPort</code></li>
        <li><code>NetworkProtocol</code></li>
        <li><code>NumericIdentifier</code></li>
        <li><code>OperatingSystem</code></li>
        <li><code>Operation</code></li>
        <li><code>OrgEntity</code></li>
        <li><code>Organization</code></li>
        <li><code>PaymentCardNumber</code></li>
        <li><code>Person</code></li>
        <li><code>PhoneNumber</code></li>
        <li><code>Port</code></li>
        <li><code>Position</code></li>
        <li><code>ProductIdentifier</code></li>
        <li><code>ProductModule</code></li>
        <li><code>ProductModuleAddon</code></li>
        <li><code>ProductVersion</code></li>
        <li><code>Product</code></li>
        <li><code>ProgrammingLanguage</code></li>
        <li><code>ProvinceOrState</code></li>
        <li><code>PublishedMedium</code></li>
        <li><code>RadioProgram</code></li>
        <li><code>RadioStation</code></li>
        <li><code>Region</code></li>
        <li><code>Religion</code></li>
        <li><code>ReportEntity</code></li>
        <li><code>ReportingEntity</code></li>
        <li><code>RiskContext</code></li>
        <li><code>RiskRule</code></li>
        <li><code>Sector</code></li>
        <li><code>SnortDetectionRule</code></li>
        <li><code>SocialSecurityNumber</code></li>
        <li><code>Source</code></li>
        <li><code>SourceMediaType</code></li>
        <li><code>SportsEvent</code></li>
        <li><code>SportsGame</code></li>
        <li><code>SportsLeague</code></li>
        <li><code>TVShow</code></li>
        <li><code>TVStation</code></li>
        <li><code>Task</code></li>
        <li><code>Technology</code></li>
        <li><code>TechnologyArea</code></li>
        <li><code>Thread</code></li>
        <li><code>Topic</code></li>
        <li><code>UPSTrackingNumber</code></li>
        <li><code>URL</code></li>
        <li><code>USPSTrackingNumber</code></li>
        <li><code>UUID</code></li>
        <li><code>UseCaseConfiguration</code></li>
        <li><code>UseCaseReport</code></li>
        <li><code>User</code></li>
        <li><code>UserEnterprise</code></li>
        <li><code>UserEntity</code></li>
        <li><code>UserGroup</code></li>
        <li><code>UserLabel</code></li>
        <li><code>UserModuleGroup</code></li>
        <li><code>UserModuleRoleGroup</code></li>
        <li><code>UserOrganization</code></li>
        <li><code>UserRole</code></li>
        <li><code>Username</code></li>
        <li><code>Vessel</code></li>
        <li><code>WebMoneyID</code></li>
        <li><code>WinRegKey</code></li>
        <li><code>YaraDetectionRule</code></li>
    </ul> <dd></dd>
    <dt id="banshee-entity-search--limit"><a href="#banshee-entity-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>限制結果數量</p>
    <p>最大限制為 100</p>
    <p>預設為 100</p><dd></dd>
    <dt id="banshee-entity-search--pretty"><a href="#banshee-entity-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-entity-search--help"><a href="#banshee-entity-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>


## banshee email

以 Recorded Future 情報豐富化電子郵件檔案（EML）。

<h3 class="commands-reference">用法</h3>

```
banshee email [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-email-enrich"><code>banshee email enrich</code></a></dt><dd><p>以 Recorded Future 情報豐富化電子郵件（EML）檔案</p></dd>
</dl>

### banshee email enrich

以 Recorded Future 情報豐富化電子郵件（EML）檔案。此命令會解析 EML 檔案，從標頭提取 IP 位址，並從正文中擷取 URL（以 `http`/`https` 開頭），接著以威脅情報資料進行豐富化。預設情況下，結果僅顯示符合風險分數門檻的指標。使用 `--threat-hunt` 可一併包含與威脅行為者相關聯的指標，即使其風險分數低於門檻值。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">JSON 輸出</h3>

JSON 陣列中每個結果物件包含以下欄位：

| 欄位 | 說明 |
|---|---|
| `ioc` | 從電子郵件中提取的指標——IP 位址或 URL |
| `type` | 指標類型，例如 `ip` 或 `url` |
| `location` | 指標所在的電子郵件區段，例如 `header` 或 `body` |
| `risk_score` | Recorded Future 風險分數 |
| `ta_names` | 與此指標相關聯的威脅行為者名稱清單。若無則為空 |
| `malwares` | 與此指標相關聯的惡意程式家族名稱清單。若無則為空 |
| `first_seen` | 首次記錄目擊的 ISO 8601 時間戳記 |
| `last_seen` | 最近一次記錄目擊的 ISO 8601 時間戳記 |
| `count_of_analyst_notes` | 引用此指標的 Recorded Future 分析師備註數量 |
| `rule_evidence` | 個別風險規則證據詳情的陣列，依嚴重程度由高至低排序 |

`rule_evidence` 陣列中每個物件包含：

| 欄位 | 說明 |
|---|---|
| `rule` | 觸發的特定 Recorded Future 風險規則名稱 |
| `level` | 此規則的嚴重程度等級——數值越大表示越嚴重 |
| `timestamp` | 此規則最近一次目擊的 ISO 8601 時間戳記 |
| `evidence_string` | 人類可讀的證據摘要 |

<h3 class="commands-reference">用法</h3>

```
banshee email enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--file-path"><a href="#banshee-email-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>要豐富化的 EML 檔案路徑</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--risk-score"><a href="#banshee-email-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>篩選結果，僅顯示風險分數（0 - 99）高於此門檻的指標</p><p>預設為 65</p></dd>
    <dt id="banshee-email-enrich--threat-hunt"><a href="#banshee-email-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>無論風險分數門檻為何，一併包含與威脅行為者相關聯的指標</p></dd>
    <dt id="banshee-email-enrich--pretty"><a href="#banshee-email-enrich--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-email-enrich--help"><a href="#banshee-email-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>
<pre><code class="language-bash">
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p
banshee email enrich suspicious.eml --threat-hunt
</code></pre>

### banshee email extract-attachments

從電子郵件（EML）檔案中提取附件，以密碼保護的 ZIP 壓縮檔（密碼為 `infected`）封裝，並將壓縮檔提交至 Recorded Future Sandbox 進行分析。等待沙箱分析完成後回傳摘要：目前狀態、整體分數、目標、建立和完成時間戳記、SHA256，以及各任務的詳細資訊。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee email extract-attachments [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-email-extract-attachments--file-path"><a href="#banshee-email-extract-attachments--file-path"><code>FILE_PATH</code></a></dt><dd><p>要提取附件的 EML 檔案路徑</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-email-extract-attachments--zip-path"><a href="#banshee-email-extract-attachments--zip-path"><code>--zip-path</code></a>, <code>-z</code> <i>zip-path</i></dt><dd>
    <p>指定儲存包含提取檔案的壓縮檔的自訂路徑</p>
    <p>預設為當前目錄</p></dd>
    <dt id="banshee-email-extract-attachments--pretty"><a href="#banshee-email-extract-attachments--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-email-extract-attachments--help"><a href="#banshee-email-extract-attachments--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee email extract-attachments phishing_email.eml
banshee email extract-attachments phishing_email.eml -p -z ../sandbox/files.zip
</code></pre>

## banshee ioc

搜尋及查詢入侵指標（IOC）

<h3 class="commands-reference">用法</h3>

```
banshee ioc [OPTIONS] COMMAND [ARGS]...
```
<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ioc-lookup"><code>banshee ioc lookup</code></a></dt><dd><p>對一或多個 IOC 進行詳細豐富化，可設定詳細程度</p></dd>
    <dt><a href="#banshee-ioc-bulk-lookup"><code>banshee ioc bulk-lookup</code></a></dt><dd><p>快速批次豐富化，回傳風險分數及已觸發規則——每次 API 呼叫最多可處理 1000 個 IOC</p></dd>
    <dt><a href="#banshee-ioc-search"><code>banshee ioc search</code></a></dt><dd><p>搜尋 IOC</p></dd>
    <dt><a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></dt><dd><p>搜尋 IOC 規則</p></dd>
</dl>

### banshee ioc lookup

對一或多個 IOC 進行詳細豐富化——每個指標執行一次 API 呼叫。使用 [`--verbosity`](#banshee-ioc-lookup--verbosity) 控制回傳的欄位數量，從基本風險分數到包含連結、分析師備註等完整情報皆可設定。當需要豐富的背景資訊時，請使用此命令。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ioc lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>要查詢的實體類型</p>
    <p>支援的值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-lookup--ioc"><a href="#banshee-ioc-lookup--ioc"><code>IOC</code></a></dt><dd><p>一或多個以空白字元分隔的 IOC 進行查詢</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--ai-insights"><a href="#banshee-ioc-lookup--ai-insights"><code>--ai-insights</code></a>,  <code>-a</code></dt><dd>
    <p>啟用 Recorded Future AI 生成的 insights，摘要相關風險規則與關鍵參考資料。</p>
    <p><strong>注意：</strong>由於 AI 處理所需時間，回應時間可能略有延遲。</p<dd></dd>
    <dt id="banshee-ioc-lookup--verbosity"><a href="#banshee-ioc-lookup--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>控制回應中回傳的資料量（1-5）。詳細程度越高，JSON 輸出中包含的欄位與細節越多。</p>
    <p><strong>注意：</strong>詳細程度越高，因資料擷取量增加，回應時間可能越慢。</p>
    <p>預設為 1</p>
    <h4>各詳細程度等級可用欄位</h4>
    <p><b>ip：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, location, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, location, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, dnsPortCert, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, scanner, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>domain：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>url：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
    </ul>

    <p><b>hash：</b></p>
    <ul>
        <li><b>1：</b> entity, hashAlgorithm, risk, timestamps</li>
        <li><b>2：</b> entity, fileHashes, hashAlgorithm, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, fileHashes, hashAlgorithm, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>vulnerability：</b></p>
    <ul>
        <li><b>1：</b> entity, lifecycleStage, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, lifecycleStage, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, lifecycleStage, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, cpe, cpe22uri, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, nvdDescription, nvdReferences, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>
    </dd>
    <dt id="banshee-ioc-lookup--pretty"><a href="#banshee-ioc-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ioc-lookup--help"><a href="#banshee-ioc-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>
<pre><code>
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23,139.224.189.177 -p
</code></pre>

透過管道傳入以逗號或換行符分隔的 IOC 清單進行查詢：

<pre><code>
cat test_ips.csv| banshee ioc lookup ip -p
</code></pre>


### banshee ioc bulk-lookup

對任意數量的單一類型 IOC 進行快速批次豐富化。此命令每次 API 呼叫最多可批次處理 1000 個 IOC，並自動處理分批，對於大量 IOC 的處理速度顯著快於 [`banshee ioc lookup`](#banshee-ioc-lookup)。

每個指標回傳固定欄位集：風險分數及已觸發的風險規則。適合用於大量快速篩選分類。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ioc bulk-lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--entity-type"><a href="#banshee-ioc-bulk-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>要豐富化的實體類型</p>
    <p>支援的值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-bulk-lookup--ioc"><a href="#banshee-ioc-bulk-lookup--ioc"><code>IOC</code></a></dt><dd><p>一或多個以空白字元分隔的 IOC 進行豐富化。亦接受來自 stdin 的輸入（參見下方範例）。</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--pretty"><a href="#banshee-ioc-bulk-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ioc-bulk-lookup--help"><a href="#banshee-ioc-bulk-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>
<pre><code>
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877
</code></pre>

<h4>檔案 / Stdin 輸入</h4>

透過管道或重新導向傳入以換行符分隔的 IOC 檔案（每行一筆）：

```
> cat cves.txt
CVE-2012-4792
CVE-2011-0611
CVE-2013-0422
CVE-2021-22204
CVE-2016-4557
```

<pre><code>
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability
</code></pre>

<h4>提取名稱與分數</h4>
使用 `jq` 從 JSON 輸出中提取特定欄位，例如：

<pre><code>
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'
</code></pre>


### banshee ioc search

搜尋 Classic Alerts。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ioc search [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>要查詢的實體類型</p>
    <p>支援的值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-search--limit"><a href="#banshee-ioc-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>限制結果數量</p>
    <p>最大限制為 1000</p>
    <p>預設為 5</p><dd></dd>
    <dt id="banshee-ioc-search--risk-score"><a href="#banshee-ioc-search--risk-score"><code>--risk-score</code>, <code>-r</code></a> <i>risk-score</i></dt><dd>
    <p>依風險分數範圍篩選，例如：</p>
    <p>
        <ul>
            <li><code>--risk-score '[20,90]'</code> &rarr; 等同於 <code>20 &lt;= riskScore &lt;= 90</code></li>
            <li><code>--risk-score '(20,90)'</code> &rarr; 等同於 <code>20 &lt; riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,90)'</code> &rarr; 等同於 <code>20 &lt;= riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,)'</code> &rarr; 等同於 <code>20 &lt;= riskScore</code></li>
            <li><code>--risk-score '[,90)'</code> &rarr; 等同於 <code>riskScore &lt; 90</code></li>
        </ul>
    </p>
    <p>請以引號包覆風險分數範圍，以確保正確解析</p>
    <dd></dd>
    <dt id="banshee-ioc-search--risk-rule"><a href="#banshee-ioc-search--risk-rule"><code>--risk-rule</code>, <code>-R</code></a> <i>rule-name</i></dt><dd>
    <p>依風險規則名稱篩選</p>
    <p>可用選項請參閱此<a href="https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future" target="_blank">支援文章</a>中風險規則表格的<b>機器名稱</b>欄位，或使用 <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> 命令</p><dd></dd>
    <dt id="banshee-ioc-search--verbosity"><a href="#banshee-ioc-search--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>控制回應中回傳的資料量（1-5）。詳細程度越高，JSON 輸出中包含的欄位與細節越多。</p>
    <p><strong>注意：</strong>詳細程度越高，因資料擷取量增加，回應時間可能越慢。</p>
    <p>預設為 1</p>
    <h4>各詳細程度等級可用欄位</h4>
    <p><b>ip：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, location, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, location, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, dnsPortCert, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, scanner, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>domain：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>url：</b></p>
    <ul>
        <li><b>1：</b> entity, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
    </ul>

    <p><b>hash：</b></p>
    <ul>
        <li><b>1：</b> entity, hashAlgorithm, risk, timestamps</li>
        <li><b>2：</b> entity, fileHashes, hashAlgorithm, intelCard, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, fileHashes, hashAlgorithm, intelCard, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>vulnerability：</b></p>
    <ul>
        <li><b>1：</b> entity, lifecycleStage, risk, timestamps</li>
        <li><b>2：</b> entity, intelCard, lifecycleStage, risk, timestamps</li>
        <li><b>3：</b> analystNotes, entity, intelCard, lifecycleStage, links, risk, timestamps</li>
        <li><b>4：</b> analystNotes, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5：</b> analystNotes, cpe, cpe22uri, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, nvdDescription, nvdReferences, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>
    </dd>
    <dt id="banshee-ioc-search--pretty"><a href="#banshee-ioc-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ioc-search--help"><a href="#banshee-ioc-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee ioc rules

搜尋指定實體類型的 IOC 規則。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee ioc rules [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--entity-type"><a href="#banshee-ioc-rules--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>IOC 規則的實體類型</p>
    <p>支援的值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--freetext"><a href="#banshee-ioc-rules--freetext"><code>--freetext</code>, <code>-F</code></a> <i>freetext-rule-name</i></dt><dd>
    <p>以自由文字搜尋依風險規則名稱篩選</p><dd></dd>
    <dt id="banshee-ioc-rules--mitre"><a href="#banshee-ioc-rules--mitre"><code>--mitre-code</code>, <code>-M</code></a> <i>mitre-code</i></dt><dd>
    <p>依 MITRE ATT&CK 代碼篩選</p><dd></dd>
    <dt id="banshee-ioc-rules--criticality"><a href="#banshee-ioc-rules--criticality"><code>--criticality</code>, <code>-C</code></a> <i>criticality</i></dt><dd>
    <p>依嚴重性篩選。數值越高，嚴重性越高</p>
    <p>接受值為 1 至 5</p>
    <p><strong>嚴重性等級（IP、Domain、URL、Hash）</strong></p>
    <ul>
        <li><code>4</code> – 高度惡意（Risk Score 範圍：90–99）</li>
        <li><code>3</code> – 惡意（Risk Score 範圍：65–89）</li>
        <li><code>2</code> – 可疑（Risk Score 範圍：25–64）</li>
        <li><code>1</code> – 異常（Risk Score 範圍：5–24）</li>
        <li><code>0</code> – 無風險證據（Risk Score 範圍：0）</li>
    </ul>
    <p><strong>嚴重性等級（Vulnerability）</strong></p>
    <ul>
        <li><code>5</code> – 極度嚴重（Risk Score 範圍：90–99）</li>
        <li><code>4</code> – 嚴重（Risk Score 範圍：80–89）</li>
        <li><code>3</code> – 高（Risk Score 範圍：65–79）</li>
        <li><code>2</code> – 中（Risk Score 範圍：25–64）</li>
        <li><code>1</code> – 低（Risk Score 範圍：5–24）</li>
        <li><code>0</code> – 無風險證據（Risk Score 範圍：0）</li>
    </ul>
    <dd></dd>
    <dt id="banshee-ioc-rules--pretty"><a href="#banshee-ioc-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-ioc-rules--help"><a href="#banshee-ioc-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

## banshee list

管理 Recorded Future 清單與監控清單（Watch list）

<h3 class="commands-reference">用法</h3>

```
banshee list [OPTIONS] COMMAND [ARGS]...
```
<dl class="commands-reference">
    <dt><a href="#banshee-list-create"><code>banshee list create</code></a></dt><dd><p>建立新清單</p></dd>
    <dt><a href="#banshee-list-info"><code>banshee list info</code></a></dt><dd><p>取得清單的基本資訊</p></dd>
    <dt><a href="#banshee-list-search"><code>banshee list search</code></a></dt><dd><p>搜尋清單</p></dd>
    <dt><a href="#banshee-list-status"><code>banshee list status</code></a></dt><dd><p>取得清單狀態</p></dd>
    <dt><a href="#banshee-list-entities"><code>banshee list entities</code></a></dt><dd><p>取得清單中的實體</p></dd>
    <dt><a href="#banshee-list-add"><code>banshee list add</code></a></dt><dd><p>將實體加入清單</p></dd>
    <dt><a href="#banshee-list-bulk-add"><code>banshee list bulk-add</code></a></dt><dd><p>批次將實體加入清單</p></dd>
    <dt><a href="#banshee-list-remove"><code>banshee list remove</code></a></dt><dd><p>從清單移除實體</p></dd>
    <dt><a href="#banshee-list-bulk-remove"><code>banshee list bulk-remove</code></a></dt><dd><p>批次從清單移除實體</p></dd>
    <dt><a href="#banshee-list-copy"><code>banshee list copy</code></a></dt><dd><p>將實體從一個清單複製到另一個清單</p></dd>
    <dt><a href="#banshee-list-clear"><code>banshee list clear</code></a></dt><dd><p>清除清單中的所有實體</p></dd>
    <dt><a href="#banshee-list-entries"><code>banshee list entries</code></a></dt><dd><p>取得清單中的文字條目</p></dd>
</dl>

### banshee list create

建立新清單。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list create [OPTIONS] NAME [LIST_TYPE]
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>NAME</code></a></dt><dd><p>要建立的清單名稱</p></dd>
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>LIST_TYPE</code></a></dt><dd><p>要建立的清單類型</p>
    <p>支援的類型：</p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
    </ul>
    <p>預設為 <code>entity</code></p>
    </dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--pretty"><a href="#banshee-list-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-lookup--help"><a href="#banshee-list-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list info

取得清單的相關資訊，例如名稱、類型、時間戳記及擁有者詳細資料。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list info [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要查詢資訊的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list search

搜尋清單

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list search [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--name"><a href="#banshee-list-search--name"><code>NAME</code></a></dt><dd>
    <p>要搜尋的清單名稱</p>
    <p>若不指定名稱，將回傳所有清單</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--list-type"><a href="#banshee-list-search--list-type"><code>--list-type</code>, <code>-t</code></a> <i>list-type</i></dt><dd>
    <p>依清單類型篩選</p>
    <p>支援的類型：</p>
    <p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
        <li><code>custom</code></li>
        <li><code>ip</code></li>
        <li><code>domain</code></li>
        <li><code>tech_stack</code></li>
        <li><code>industry</code></li>
        <li><code>brand</code></li>
        <li><code>partner</code></li>
        <li><code>industry_peer</code></li>
        <li><code>location</code></li>
        <li><code>supplier</code></li>
        <li><code>vulnerability</code></li>
        <li><code>company</code></li>
        <li><code>hash</code></li>
        <li><code>operation</code></li>
        <li><code>attacker</code></li>
        <li><code>target</code></li>
        <li><code>method</code></li>
        <li><code>executive</code></li>
    </ul>
    </p><dd></dd>
    <dt id="banshee-list-search--limit"><a href="#banshee-list-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>限制結果數量</p>
    <p>最大限制為 3 000</p>
    <p>預設為 1 000</p><dd></dd>
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list status

取得清單狀態及實體數量。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list status [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要查詢狀態的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list entities

取得清單中的實體

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list entities [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要擷取實體的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>


### banshee list entries

取得清單中的文字條目

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee list entries [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要擷取文字條目的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>



### banshee list clear

完全清除清單並移除所有實體。請注意，此命令不會清除文字條目，且不支援此功能。

<h3 class="commands-reference">用法</h3>

```
banshee list clear [OPTIONS] LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要清除的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list add

將實體加入清單。

<h3 class="commands-reference">用法</h3>

```
banshee list add [OPTIONS] LIST_ID ENTITY_ID [PROPERTIES]
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--list-id"><a href="#banshee-list-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要加入的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
    <dt id="banshee-list-add--entity-id"><a href="#banshee-list-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>要加入清單的實體 ID 或含類型的名稱，例如：</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul></dd>
    <dt id="banshee-list-add--properties"><a href="#banshee-list-add--properties"><code>PROPERTIES</code></a></dt><dd>
    <p>選用。使用 <code>annotation=&lt;text&gt;</code> 為此實體附加一則備註，該備註將顯示於 Recorded Future 平台上。</p>
    <p>若值包含空格，請以引號包覆。</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--help"><a href="#banshee-list-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
</code></pre>

### banshee list bulk-add

批次將多個實體加入清單

<h3 class="commands-reference">用法</h3>

```
banshee list bulk-add [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--list-id"><a href="#banshee-list-bulk-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要加入的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
    <dt id="banshee-list-bulk-add--entity-input"><a href="#banshee-list-bulk-add--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>一或多個以空格／換行符分隔的實體，例如：</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>此命令亦接受來自 stdin 的輸入。假設「entities.txt」為以換行符分隔的實體檔案，例如：</p>
    <pre><code>
    $ cat entities.txt
    verifyaccount.otzo.com,InternetDomainName
    92.38.178.133,IpAddress
    https://constructorachg.cl/eFSLb6eV/j.html,URL
    CVE-2019-1215,CyberVulnerability
    e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877,Hash
    SoA6SP
    lYNvCK
    </code></pre>
    <p>基於上述情況，可執行以下其中一個命令批次新增實體：</p>
    <pre><code>
    $ banshee list bulk-add LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-add LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--overwrite"><a href="#banshee-list-bulk-add--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>啟用覆寫模式。啟用後，命令將：</p>
    <ul>
        <li>保留清單中目前存在且同時出現在所提供檔案中的所有實體</li>
        <li>新增所提供檔案中尚未在清單中的任何新實體</li>
        <li>移除清單中<strong>未</strong>出現在所提供檔案中的任何實體</li>
    </ul>
    <p>預設情況下（未使用此旗標），命令會將新實體附加至現有清單，不移除任何內容。</p>
    </dd>
    <dt id="banshee-list-bulk-add--help"><a href="#banshee-list-bulk-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">結果狀態輸出</h3>

<p><code>banshee list bulk-add</code> 依狀態分組輸出，並在各狀態下列出對應的輸入實體，例如：</p>

<pre><code class="language-text">
ADDED:
SoA6SP

ERROR_MULTIPLE_MATCHES:
wanna:malware
</code></pre>

<p>常見狀態：</p>
<ul>
    <li><code>ADDED</code> - 實體已成功加入清單。</li>
    <li><code>UNCHANGED</code> - 實體已存在於清單中（未進行任何變更）。</li>
    <li><code>UPDATED</code> - 實體已存在且已由 API 更新。</li>
    <li><code>ERROR_BAD_ID</code> - 輸入格式無效或實體參考無效。</li>
    <li><code>ERROR_NOT_FOUND</code> - 找不到符合的實體。</li>
    <li><code>ERROR_NOT_ALLOWED</code> - 該實體類型不允許加入指定清單。</li>
    <li><code>ERROR_MULTIPLE_MATCHES</code> - 輸入符合多個可能的實體。<strong>該實體未被加入。</strong></li>
    <li><code>LIST_MAX_SIZE_REACHED</code> - 指定的清單已達上限，無法再新增實體。</li>
</ul>

<h3 class="commands-reference">如何解決 <code>ERROR_MULTIPLE_MATCHES</code></h3>

<p>當出現 <code>ERROR_MULTIPLE_MATCHES</code> 時，表示所提供的實體名稱存在歧義。API 無法選定單一確切實體，因此該筆記錄將被略過而不予加入。</p>

<p>建議的處理流程：</p>
<ol>
    <li>從命令輸出中取得有歧義的值。</li>
    <li>執行 <code>banshee entity search</code> 以找出目標確切實體。若有需要，可調整搜尋詞的寫法（例如不同拼寫、空格或更具體的變體）以縮小結果範圍。</li>
    <li>將輸入檔案中的歧義值替換為確切的實體 ID。</li>
    <li>以修正後的檔案再次執行 <code>banshee list bulk-add</code>。</li>
</ol>

<p>範例：</p>
<pre><code class="language-bash">
banshee entity search wannacry --type Malware
banshee list bulk-add LIST_ID &lt; entities.txt
</code></pre>

<p>提示：若已知實體 ID（例如 <code>SoA6SP</code>），建議在批次檔案中優先使用 ID 而非名稱／類型組合，以避免歧義。</p>

### banshee list remove

從清單移除實體。

<h3 class="commands-reference">用法</h3>

```
banshee list remove [OPTIONS] LIST_ID ENTITY_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--list-id"><a href="#banshee-list-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要移除實體的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
    <dt id="banshee-list-remove--entity-id"><a href="#banshee-list-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>要從清單中移除的實體 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--help"><a href="#banshee-list-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list bulk-remove

批次從清單移除多個實體

<h3 class="commands-reference">用法</h3>

```
banshee list bulk-remove [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--list-id"><a href="#banshee-list-bulk-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>要移除實體的清單 ID</p>
    <p>清單 ID 可附帶或不附帶「<strong>report:</strong>」前綴</p></dd>
    <dt id="banshee-list-bulk-remove--entity-input"><a href="#banshee-list-bulk-remove--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>一或多個以空格／換行符分隔的實體，例如：</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>此命令亦接受來自 stdin 的輸入。假設「entities.txt」為以換行符分隔的實體檔案，例如：</p>
    <pre><code>
    $ cat entities.txt
    verifyaccount.otzo.com,InternetDomainName
    92.38.178.133,IpAddress
    https://constructorachg.cl/eFSLb6eV/j.html,URL
    CVE-2019-1215,CyberVulnerability
    e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877,Hash
    SoA6SP
    lYNvCK
    </code></pre>
    <p>基於上述情況，可執行以下其中一個命令批次移除實體：</p>
    <pre><code>
    $ banshee list bulk-remove LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-remove LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--help"><a href="#banshee-list-bulk-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee list copy

將實體從一個清單複製到另一個清單的工具命令。

此命令會讀取來源清單的實體，並將其加入目標清單。預設情況下，新實體會附加至目標清單，不影響目標清單中現有的內容。使用 `--overwrite` 時，目標清單將與來源清單保持一致：兩者共同存在的實體將予以保留，新實體將被加入，而目標清單中**未**出現在來源清單的實體則將被移除。

若來源清單為空，即使使用 `--overwrite`，命令也將在不修改目標清單的情況下結束。

<h3 class="commands-reference">用法</h3>

```
banshee list copy [OPTIONS] SOURCE_LIST_ID DESTINATION_LIST_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--source-list-id"><a href="#banshee-list-copy--source-list-id"><code>SOURCE_LIST_ID</code></a></dt><dd>
    <p>要複製實體的來源清單 ID</p></dd>
    <dt id="banshee-list-copy--destination-list-id"><a href="#banshee-list-copy--destination-list-id"><code>DESTINATION_LIST_ID</code></a></dt><dd>
    <p>要複製實體至的目標清單 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--overwrite"><a href="#banshee-list-copy--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>覆寫模式：保留目標清單中已存在的實體，新增未存在的實體，並移除目標清單中不在來源清單中的任何實體。預設情況下，命令僅附加新實體，不移除現有實體。</p></dd>
    <dt id="banshee-list-copy--help"><a href="#banshee-list-copy--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">範例</h3>

```
$ banshee list copy 1b0s1q 21YKUC
$ banshee list copy 1b0s1q 21YKUC --overwrite
```

## banshee pba

搜尋、查詢及更新 Recorded Future Playbook Alerts

<h3 class="commands-reference">用法</h3>

```
banshee pba [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pba-lookup"><code>banshee pba lookup</code></a></dt><dd><p>查詢單一 Playbook Alert</p></dd>
    <dt><a href="#banshee-pba-search"><code>banshee pba search</code></a></dt><dd><p>搜尋 Playbook Alerts</p></dd>
    <dt><a href="#banshee-pba-update"><code>banshee pba update</code></a></dt><dd><p>更新一或多筆 Playbook Alert</p></dd>
    <dt><a href="#banshee-pba-export"><code>banshee pba export</code></a></dt><dd><p>將 Playbook Alerts 匯出為 JSON 或 CSV 格式</p></dd>
</dl>

### banshee pba lookup

查詢單一 Playbook Alert。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee pba lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--alert-id"><a href="#banshee-pba-lookup--alert-id"<code>ALERT_ID</code></a></dt><dd><p>要查詢的 Alert ID</p>
    <p>Alert ID 可附帶或不附帶「<strong>task:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--pretty"><a href="#banshee-pba-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-pba-lookup--help"><a href="#banshee-pba-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee pba search

搜尋 Playbook Alerts。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee pba search [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-search--created"><a href="#banshee-pba-search--created"><code>--created</code>, <code>-C</code></a> <i>created-from</i></dt><dd>
    <p>依建立時間篩選，例如：1d；12h</p><dd></dd>
    <dt id="banshee-pba-search--updated"><a href="#banshee-pba-search--updated"><code>--updated</code>, <code>-u</code></a> <i>updated-from</i></dt><dd>
    <p>依更新時間篩選，例如：1d；12h</p><dd></dd>
    <dt id="banshee-pba-search--category"><a href="#banshee-pba-search--category"><code>--category</code>, <code>-c</code></a> <i>category</i></dt><dd>
    <p>依警報類別篩選（可重複指定）</p>
    <p>支援的類別：</p>
    <p>
    <ul>
        <li><code>domain_abuse</code></li>
        <li><code>cyber_vulnerability</code></li>
        <li><code>third_party_risk</code></li>
        <li><code>code_repo_leakage</code></li>
        <li><code>identity_novel_exposures</code></li>
        <li><code>geopolitics_facility</code></li>
        <li><code>malware_report</code></li>
    </ul>
    </p><dd></dd>
    <dt id="banshee-pba-search--priority"><a href="#banshee-pba-search--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>依警報優先級篩選（可重複指定）</p>
    <p>可用值：<code>Informational</code>、<code>Moderate</code>、<code>High</code></p>
    <p>預設為所有優先級</p><dd></dd>
    <dt id="banshee-pba-search--status"><a href="#banshee-pba-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>依警報狀態篩選（可重複指定）</p>
    <p>可用值：<code>New</code>、<code>InProgress</code>、<code>Dismissed</code>、<code>Resolved</code></p>
    <p>預設為所有狀態</p><dd></dd>
    <dt id="banshee-pba-search--entity"><a href="#banshee-pba-search--entity"><code>--entity</code></a>,  <code>-e</code> <i>entity</i></dt><dd>
    <p>依關聯實體篩選警報（可重複指定），例如：<code>-e idn:recordedfuture.com -e idn:example.com</code></p><dd></dd>
    <dt id="banshee-pba-search--org-id"><a href="#banshee-pba-search--org-id"><code>--org-id</code></a>,  <code>-o</code> <i>organisation-id</i></dt><dd>
    <p>依所屬組織 ID 篩選警報（可重複指定）</p>
    <p>接受 10 位元字元 ID 或 16 位元字元的 <code>uhash:</code> 格式，例如：<code>-o 69sKLfTGsS -o uhash:5zQaSyRpA1</code></p><dd></dd>
    <dt id="banshee-pba-search--limit"><a href="#banshee-pba-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>限制結果數量</p>
    <p>最大限制為 10 000</p>
    <p>預設為 100</p><dd></dd>
    <dt id="banshee-pba-search--pretty"><a href="#banshee-pba-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-pba-search--help"><a href="#banshee-pba-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

### banshee pba update

更新一或多筆 Playbook Alert

<h3 class="commands-reference">用法</h3>

```
banshee pba update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--alert-id"><a href="#banshee-pba-update--alert-id"<code>ALERT_IDS</code></a></dt><dd>
    <p>一或多個以空白字元分隔的 Alert ID</p>
    <p>Alert ID 可附帶或不附帶「<strong>task:</strong>」前綴</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--status"><a href="#banshee-pba-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>將警報更新為指定的警報狀態</p>
    <p>可用值：<code>New</code>、<code>InProgress</code>、<code>Dismissed</code>、<code>Resolved</code></p><dd></dd>
    <dt id="banshee-pba-update--reopen"><a href="#banshee-pba-update--reopen"><code>--reopen</code></a>,  <code>-r</code> <i>reopen</i></dt><dd>
    <p>重新開啟策略僅適用於狀態為 Dismissed 或 Resolved 的警報。以下是允許的 status/reopen 組合：<code>Dismissed -> Never</code>；<code>Resolved -> Never</code>；<code>Resolved -> SignificantUpdates</code></p>
    <p>支援的值：<code>Never</code>、<code>SignificantUpdates</code></p><dd></dd>
    <dt id="banshee-pba-update--priority"><a href="#banshee-pba-update--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>設定新的警報優先級</p>
    <p>可用值：<code>Informational</code>、<code>Moderate</code>、<code>High</code></p><dd></dd>
    <dt id="banshee-pba-update--comment"><a href="#banshee-pba-update--comment"><code>--comment</code></a>,  <code>-t</code> <i>comment</i></dt><dd>
    <p>要新增至警報的備註，例如："Bulk resolved via banshee"</p><dd></dd>
    <dt id="banshee-pba-update--assignee"><a href="#banshee-pba-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>將警報指派給新使用者。接受使用者的 uhash，例如：uhash:3aXZxdkM12</p><dd></dd>
    <dt id="banshee-pba-update--help"><a href="#banshee-pba-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<p>提供一或多個 Alert ID（以空白字元分隔），並指定所需的更新選項：</p>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Dismissed
banshee pba update ALERT_ID -s InProgress -p High -t "Escalated due to new findings"
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved -a uhash:3aXZxdkM12
</code></pre>

<h3 class="commands-reference">提供 Alert ID 的方式</h3>

<h4>1. 直接作為引數傳入（單筆或多筆）：</h4>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved
</code></pre>

<h4>2. 從檔案或標準輸入讀取：</h4>

<p>若您有一個每行一筆 Alert ID 的檔案（例如 <code>alerts.txt</code>）：</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>可使用以下命令更新所有列出的警報：</p>

<pre><code class="language-bash">
banshee pba update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee pba update -s Dismissed
</code></pre>

<h4>3. 透過搜尋命令的管道傳入：</h4>

<p>使用 <code>jq</code> 等工具從搜尋結果中提取 Alert ID，並透過管道傳入更新命令：</p>

<pre><code class="language-bash">
banshee pba search | jq -r '.data[].playbook_alert_id' | banshee pba update -p High -t "Investigation started"
</code></pre>

<h3 class="commands-reference">其他使用範例</h3>

<pre><code class="language-bash">
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved
banshee pba update ALERT_ID -s Resolved -r Never
banshee pba update ALERT_ID_1 ALERT_ID_2 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
banshee pba update ALERT_ID -a
</code></pre>

### banshee pba export

將 Playbook Alerts 匯出為 JSON 或 CSV 格式。從 stdin 讀取警報 ID 與類別——通常透過管道從 [`banshee pba search`](#banshee-pba-search) 傳入。

<h3 class="commands-reference">輸出格式</h3>

<p><b>JSON（預設）</b>——為每個 ID 輸出 Recorded Future API 回傳的<i>完整</i>警報物件：包含所有頂層欄位及巢狀的面板狀態、目標、證據、指派人、時間戳記等。適合用於下游工具、<code>jq</code> 管道或資料重新匯入。</p>

<p><b>CSV（<a href="#banshee-pba-export--csv"><code>--csv</code></a>）</b>——輸出適用於試算表和報告的高層次摘要。僅寫入以下十二個欄位（首行為標題列）；JSON 回應中的其他所有欄位均省略。</p>

| 欄位 | 說明 |
|---|---|
| `ID` | Playbook Alert ID（含 `task:` 前綴） |
| `Priority` | 警報優先級，例如 `Informational`、`Moderate`、`High` |
| `Alert Rule` | 觸發的警報規則名稱（回退至規則標籤） |
| `Status` | 警報狀態，例如 `New`、`InProgress`、`Dismissed`、`Resolved` |
| `Created` | 建立時間戳記（UTC，`%Y-%m-%d %H:%M:%S`） |
| `Updated` | 最後更新時間戳記（UTC，`%Y-%m-%d %H:%M:%S`） |
| `Subject` | 警報主旨 |
| `Assignee` | 被指派的使用者顯示名稱 |
| `Assessments` | 警報的風險評估／規則（依類別而異），以 `;` 分隔 |
| `Entities` | 去重後的目標實體名稱，以 `;` 分隔 |
| `Reopen Strategy` | 已關閉警報的重新開啟策略，例如 `Never`、`SignificantUpdates` |
| `Onwards Actions` | 對警報採取的後續行動，以 `;` 分隔 |

<h3 class="commands-reference">用法</h3>

```
banshee pba search [SEARCH_OPTIONS] | banshee pba export [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-export--csv"><a href="#banshee-pba-export--csv"><code>--csv</code></a></dt><dd>
    <p>以上述固定欄位集輸出為 CSV。若未指定此旗標，命令將輸出 JSON。</p><dd></dd>
    <dt id="banshee-pba-export--help"><a href="#banshee-pba-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">管道輸入</h3>

<p><code>banshee pba export</code> 僅接受管道輸入。它會消費由 <a href="#banshee-pba-search"><code>banshee pba search</code></a> 產生的 JSON 物件，提取每筆警報的 <code>playbook_alert_id</code> 與 <code>category</code>，並逐一完整擷取每筆警報。若未透過管道執行此命令，將回傳錯誤並拒絕執行。</p>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee pba search --created 1d | banshee pba export
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export > identity_alerts.json
banshee pba search --created 1d --category domain_abuse | banshee pba export --csv > domain_alerts.csv
</code></pre>


## banshee pcap

以 Recorded Future 情報豐富化封包擷取（pcap）資料。

<h3 class="commands-reference">用法</h3>

```
banshee pcap [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pcap-enrich"><code>banshee pcap enrich</code></a></dt><dd><p>以 Recorded Future 情報豐富化封包擷取（pcap）檔案</p></dd>
</dl>

### banshee pcap enrich

此命令會解析 pcap 檔案，提取 IP 位址和網域等網路指標，接著以威脅情報資料進行豐富化。預設情況下，結果僅顯示符合風險分數門檻的指標。使用 `--threat-hunt` 可一併包含與威脅行為者相關聯的指標，即使其風險分數低於門檻值。
<br>請注意，降低風險分數門檻及／或啟用威脅獵捕可能會顯著增加結果數量及處理時間。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">JSON 輸出</h3>

JSON 陣列中每個結果物件包含以下欄位：

| 欄位 | 說明 |
|---|---|
| `ioc` | 從 pcap 中提取的網路指標——IP 位址或網域名稱 |
| `risk_score` | Recorded Future 風險分數 |
| `most_malicious_rule` | 對風險分數貢獻最高的風險規則名稱 |
| `rule_evidence` | 個別風險規則證據詳情的陣列，依嚴重程度由高至低排序 |
| `ta_names` | 與此 IOC 相關聯的威脅行為者名稱清單。若無則為空 |
| `malwares` | 與此 IOC 相關聯的惡意程式家族名稱清單。若無則為空 |
| `wireshark_query` | 可直接貼上的 Wireshark 顯示過濾器，用於隔離此 IOC 的流量 |

`rule_evidence` 陣列中每個物件包含：

| 欄位 | 說明 |
|---|---|
| `count` | 提供此風險規則參考資料的來源數量 |
| `description` | 人類可讀的證據摘要 |
| `level` | 此規則的嚴重程度等級——數值越大表示越嚴重 |
| `mitigation` | 說明 IOC 可能出現於哪些白名單上，進而降低（或緩解）相關風險 |
| `rule` | 觸發的特定 Recorded Future 風險規則名稱 |
| `sightings` | 記錄的個別目擊次數 |
| `timestamp` | 此規則最近一次目擊的 ISO 8601 時間戳記 |
| `type` | 類型識別碼 |

<h3 class="commands-reference">用法</h3>


```
banshee pcap enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--file-path"><a href="#banshee-pcap-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>要豐富化的 pcap 檔案路徑</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--risk-score"><a href="#banshee-pcap-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>篩選結果，僅顯示風險分數（1 - 99）高於此門檻的指標<p>預設為 65</p></p></dd>
    <dt id="banshee-pcap-enrich--threat-hunt"><a href="#banshee-pcap-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>無論風險分數門檻為何，一併包含與威脅行為者相關聯的指標（回溯式威脅獵捕）</p></dd>
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p><dd></dd>
    <dt id="banshee-pcap-enrich--help"><a href="#banshee-pcap-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

## banshee risklist

管理 Risk Lists（風險清單）。

<h3 class="commands-reference">用法</h3>

```
banshee risklist [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-risklist-create"><code>banshee risklist create</code></a></dt><dd><p>結合一或多個風險規則建立自訂 risk list</p></dd>
    <dt><a href="#banshee-risklist-fetch"><code>banshee risklist fetch</code></a></dt><dd><p>下載 risk list</p></dd>
    <dt><a href="#banshee-risklist-stat"><code>banshee risklist stat</code></a></dt><dd><p>顯示 risk list 中繼資料（etag 與時間戳記）</p></dd>
</dl>

### banshee risklist create

將一或多個 Recorded Future 風險規則合併為單一去重檔案，藉此建立自訂 risk list。

系統會為每個 `--risk-rule` 擷取條目，依 IOC 合併（以首次出現者為準），並可選擇性地依最低 `--risk-score` 進行篩選。輸出結果依風險分數降序排列，並以所選格式寫入——可直接用於防火牆、SIEM 或其他整合。

預設將輸出寫入本機檔案。使用 `--fusion` 搭配 `--output-path` 可直接將結果上傳至 Recorded Future Fusion，不在本機儲存副本。

<h3 class="commands-reference">用法</h3>

```
banshee risklist create [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-create--entity-type"><a href="#banshee-risklist-create--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list 的實體類型。有效值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code><br><strong>必填</strong></p></dd>
    <dt id="banshee-risklist-create--risk-rule"><a href="#banshee-risklist-create--risk-rule"><code>--risk-rule</code></a>, <code>-R</code> <i>risk-rule</i></dt><dd>
    <p>要包含的風險規則。使用 <code>default</code>、<code>large</code>，或 <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> 中的任何規則名稱。可重複指定——多次指定以將規則合併為單一輸出。<br><strong>必填（至少一個）</strong></p></dd>
    <dt id="banshee-risklist-create--risk-score"><a href="#banshee-risklist-create--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>最低風險分數門檻（5–99）。低於此值的條目將從輸出中排除</p></dd>
    <dt id="banshee-risklist-create--format"><a href="#banshee-risklist-create--format"><code>--format</code></a>, <code>-f</code> <i>format</i></dt><dd>
    <p>輸出格式。預設為 <code>csv</code></p>
    <ul>
        <li><code>csv</code> — 含標頭的逗號分隔格式：<code>Name</code>、<code>Risk</code>、<code>RiskString</code>、<code>EvidenceDetails</code>。Hash 實體類型包含額外的 <code>Algorithm</code> 欄位：<code>Name</code>、<code>Algorithm</code>、<code>Risk</code>、<code>RiskString</code>、<code>EvidenceDetails</code></li>
        <li><code>edl</code> — 每行一個 IOC 值的純文字清單（適用於防火牆 EDL 饋送）。以 <code>.txt</code> 副檔名寫入</li>
        <li><code>json</code> — 完整 risk list 條目的 JSON 陣列</li>
    </ul></dd>
    <dt id="banshee-risklist-create--output-path"><a href="#banshee-risklist-create--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>輸出檔案路徑。接受檔案路徑或目錄（檔案名稱將自動產生為 <code>custom_risklist_{entity_type}.{ext}</code>）。預設為當前目錄並自動產生檔案名稱。<br>使用 <code>--fusion</code> 時為必填</p></dd>
    <dt id="banshee-risklist-create--fusion"><a href="#banshee-risklist-create--fusion"><code>--fusion</code></a>, <code>-F</code></dt><dd>
    <p>使用 <code>--output-path</code> 作為目標路徑，將結果直接上傳至 Recorded Future Fusion。設定此旗標後，不會在本機寫入任何檔案</p></dd>
    <dt id="banshee-risklist-create--help"><a href="#banshee-risklist-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

從預設規則建立 IP 的 CSV risk list，篩選風險分數 70 以上

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
```

將兩個網域規則合併為單一去重 CSV，篩選風險分數 80 以上

```bash
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
```

合併兩個 IP 規則並輸出為 EDL（純 IOC 清單）

```bash
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
```

從兩個規則建立 Hash 的 JSON risk list，並輸出至指定本機檔案路徑

```bash
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
```

建立 risk list 並直接上傳至 Recorded Future Fusion

```bash
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

### banshee risklist fetch

依指定實體類型和清單名稱下載 risk list，或使用自訂 risk list 檔案。

透過指定實體類型（`--entity-type`）和清單名稱（`--list-name`），可從 Recorded Future 下載 risk list。可用清單名稱包括 `default`、`large`，或 `banshee ioc rules` 中的任何規則名稱。如需進一步了解 Recorded Future Risk Rules，請參閱 [Risk Scoring in Recorded Future](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future) 支援文章。

或者，可使用 `--custom-list-path` 提供自訂 risk list 檔案的路徑。

<h3 class="commands-reference">用法</h3>

```
banshee risklist fetch [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-fetch--entity-type"><a href="#banshee-risklist-fetch--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list 的實體類型。有效值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code><br>使用 <code>--list-name</code> 時為必填</p></dd>
    <dt id="banshee-risklist-fetch--list-name"><a href="#banshee-risklist-fetch--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>Risk list 名稱：<code>default</code>、<code>large</code>，或 <code>banshee ioc rules</code> 中的規則名稱<br>使用 <code>--entity-type</code> 時為必填</p></dd>
    <dt id="banshee-risklist-fetch--custom-list-path"><a href="#banshee-risklist-fetch--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>自訂 risk list 檔案的路徑。不可與 <code>--entity-type</code> 或 <code>--list-name</code> 同時使用</p></dd>
    <dt id="banshee-risklist-fetch--output-path"><a href="#banshee-risklist-fetch--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>輸出檔案路徑。預設為當前目錄並自動產生檔案名稱</p></dd>
    <dt id="banshee-risklist-fetch--as-json"><a href="#banshee-risklist-fetch--as-json"><code>--as-json</code></a>, <code>-j</code></dt><dd>
    <p>將 risk list 轉換為 JSON 格式。僅可與 <code>--list-name</code> 及 <code>--entity-type</code> 同時使用</p></dd>
    <dt id="banshee-risklist-fetch--help"><a href="#banshee-risklist-fetch--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
# 下載 IP 位址的預設 risk list
banshee risklist fetch -e ip -l default

# 將網域的大型 risk list 下載為 JSON
banshee risklist fetch -e domain -l large -j

# 下載涉及 Insikt Group Note 的 Hash risk list
banshee risklist fetch -e hash -l analystNote

# 下載自訂 risk list 檔案
banshee risklist fetch -c /path/to/custom_risklist.csv

# 下載 URL 的預設 risk list 並儲存至指定輸出路徑
banshee risklist fetch -e url -l default -o /tmp/rf_default_url_risklist.csv
</code></pre>

### banshee risklist stat

顯示 risk list 中繼資料，包括 etag 及時間戳記資訊。

此命令可在不下載完整清單內容的情況下擷取 risk list 的中繼資料，可用於查看 risk list 的最後更新時間。

<h3 class="commands-reference">用法</h3>

```
banshee risklist stat [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-stat--entity-type"><a href="#banshee-risklist-stat--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list 的實體類型。有效值：<code>ip</code>、<code>domain</code>、<code>url</code>、<code>hash</code>、<code>vulnerability</code><br>使用 <code>--list-name</code> 時為必填</p></dd>
    <dt id="banshee-risklist-stat--list-name"><a href="#banshee-risklist-stat--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>Risk list 名稱：<code>default</code>、<code>large</code>，或 <code>banshee ioc rules</code> 中的規則名稱<br>使用 <code>--entity-type</code> 時為必填</p></dd>
    <dt id="banshee-risklist-stat--custom-list-path"><a href="#banshee-risklist-stat--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>自訂 risk list 檔案的路徑。不可與 <code>--entity-type</code> 或 <code>--list-name</code> 同時使用</p></dd>
    <dt id="banshee-risklist-stat--pretty"><a href="#banshee-risklist-stat--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-risklist-stat--count"><a href="#banshee-risklist-stat--count"><code>--count</code></a>, <code>-C</code></dt><dd>
    <p>顯示 risk list 中的 IOC 數量及風險分數分佈。</p></dd>
    <dt id="banshee-risklist-stat--help"><a href="#banshee-risklist-stat--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
# 查看預設 IP risk list 的中繼資料
banshee risklist stat -e ip -l default

# 以美化格式查看中繼資料
banshee risklist stat -e domain -l large -p

# 查看自訂 risk list 檔案的中繼資料
banshee risklist stat -c /path/to/custom_risklist.txt

# 統計預設 IP risk list 中各風險分數的指標數量並美化輸出
banshee risklist stat -e ip -l default -Cp
</code></pre>

## banshee rules

搜尋並下載偵測規則。

<h3 class="commands-reference">用法</h3>

```
banshee rules [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-rules-search"><code>banshee rules search</code></a></dt><dd><p>依篩選選項搜尋偵測規則</p></dd>
</dl>

### banshee rules search

依所提供的篩選選項搜尋偵測規則。結果可顯示於主控台或儲存至磁碟作為個別規則檔案。

偵測規則可依類型（YARA、Snort、Sigma）、關聯實體（威脅行為者、惡意程式、MITRE ATT&CK 技術）、建立／更新日期等進行篩選。使用 `--threat-actor-map` 或 `--threat-malware-map` 可依您的威脅地圖中的實體自動篩選規則。

為避免輸出過多，預設結果限制為 10 筆。使用 `--limit` 選項可擷取最多 1000 條規則。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee rules search [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-rules-search--type"><a href="#banshee-rules-search--type"><code>--type</code></a>, <code>-t</code> <i>type</i></dt><dd>
    <p>依規則類型篩選。有效值：<code>yara</code>、<code>snort</code>、<code>sigma</code><br>可指定多個類型，以邏輯 OR 運算（例如 <code>-t yara -t snort</code> 回傳符合任一類型的規則）</p></dd>
    <dt id="banshee-rules-search--threat-actor-map"><a href="#banshee-rules-search--threat-actor-map"><code>--threat-actor-map</code></a>, <code>-T</code></dt><dd>
    <p>依您威脅行為者地圖中的威脅行為者篩選規則。啟用後，將回傳與您威脅行為者地圖中行為者相關聯的偵測規則</p></dd>
    <dt id="banshee-rules-search--threat-actor-category"><a href="#banshee-rules-search--threat-actor-category"><code>--threat-actor-category</code></a>, <code>-C</code> <i>category</i></dt><dd>
    <p>依您威脅行為者地圖中的威脅行為者類別篩選。可指定多個類別，以邏輯 OR 運算（例如 <code>-C nation_state_sponsored -C ransomware_and_extortion_groups</code>）</p></dd>
    <dt id="banshee-rules-search--threat-malware-map"><a href="#banshee-rules-search--threat-malware-map"><code>--threat-malware-map</code></a>, <code>-M</code></dt><dd>
    <p>依您惡意程式威脅地圖中的惡意程式篩選規則。啟用後，將回傳與您惡意程式威脅地圖中惡意程式相關聯的偵測規則</p></dd>
    <dt id="banshee-rules-search--org-id"><a href="#banshee-rules-search--org-id"><code>--org-id</code></a>, <code>-O</code> <i>org-id</i></dt><dd>
    <p>從威脅地圖擷取威脅行為者時指定組織 ID（需搭配 <code>--threat-actor-map</code> 或 <code>--threat-malware-map</code>）。接受附帶或不附帶 <code>uhash:</code> 前綴的值。適用於 MSSP 及多組織帳戶</p></dd>
    <dt id="banshee-rules-search--entity"><a href="#banshee-rules-search--entity"><code>--entity</code></a>, <code>-e</code> <i>entity</i></dt><dd>
    <p>依與偵測規則關聯的 Recorded Future 實體 ID 篩選。可指定多個實體，以邏輯 OR 運算。使用 <code>banshee entity search</code> 查找實體 ID（例如 <code>lzQ5GL</code> 代表 IsaacWiper 惡意程式，<code>mitre:T1486</code> 代表 Data Encrypted for Impact）</p></dd>
    <dt id="banshee-rules-search--created-after"><a href="#banshee-rules-search--created-after"><code>--created-after</code></a>, <code>-a</code> <i>time</i></dt><dd>
    <p>篩選在指定時間後建立的偵測規則。接受相對時間（例如 <code>1d</code>、<code>3d</code>、<code>7d</code>）或絕對日期（例如 <code>2024-01-01</code>）</p></dd>
    <dt id="banshee-rules-search--created-before"><a href="#banshee-rules-search--created-before"><code>--created-before</code></a>, <code>-b</code> <i>time</i></dt><dd>
    <p>篩選在指定時間前建立的偵測規則。接受相對時間（例如 <code>1d</code>、<code>3d</code>、<code>7d</code>）或絕對日期（例如 <code>2024-01-01</code>）</p></dd>
    <dt id="banshee-rules-search--updated-after"><a href="#banshee-rules-search--updated-after"><code>--updated-after</code></a>, <code>-u</code> <i>time</i></dt><dd>
    <p>篩選在指定時間後更新的偵測規則。接受相對時間（例如 <code>1d</code>、<code>3d</code>、<code>7d</code>）或絕對日期（例如 <code>2024-01-01</code>）</p></dd>
    <dt id="banshee-rules-search--updated-before"><a href="#banshee-rules-search--updated-before"><code>--updated-before</code></a>, <code>-U</code> <i>time</i></dt><dd>
    <p>篩選在指定時間前更新的偵測規則。接受相對時間（例如 <code>1d</code>、<code>3d</code>、<code>7d</code>）或絕對日期（例如 <code>2024-01-01</code>）</p></dd>
    <dt id="banshee-rules-search--id"><a href="#banshee-rules-search--id"><code>--id</code></a>, <code>-i</code> <i>document-id</i></dt><dd>
    <p>依與偵測規則關聯的特定 Insikt Note 文件 ID 篩選（例如 <code>doc:lmRPGB</code>）</p></dd>
    <dt id="banshee-rules-search--title"><a href="#banshee-rules-search--title"><code>--title</code></a>, <code>-n</code> <i>title</i></dt><dd>
    <p>依關聯 Insikt Note 標題對偵測規則進行自由文字搜尋</p></dd>
    <dt id="banshee-rules-search--limit"><a href="#banshee-rules-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>回傳的最大偵測規則數量<p>預設為 10</p></p></dd>
    <dt id="banshee-rules-search--output-path"><a href="#banshee-rules-search--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>將偵測規則儲存至指定目錄。可為相對或絕對路徑。若未指定，結果將輸出至主控台</p></dd>
    <dt id="banshee-rules-search--pretty"><a href="#banshee-rules-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-rules-search--help"><a href="#banshee-rules-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
# 搜尋過去 7 天內建立的 YARA 規則
banshee rules search -t yara -a 7d

# 搜尋與您威脅地圖中威脅行為者相關聯的規則並美化輸出結果
# 由於 --limit 預設為 10，此命令將回傳前 10 筆符合的規則
banshee rules search -Tp

# 結合威脅行為者與惡意程式地圖
banshee rules search -TMp

# 依特定實體 ID 搜尋規則（例如 IsaacWiper 惡意程式）
banshee rules search -e lzQ5GL -p

# 搜尋過去 3 天內更新的 Snort 和 Sigma 規則並儲存至目錄
banshee rules search -t snort -t sigma -u 3d -o ./detection_rules

# 依 Insikt Note 標題搜尋
banshee rules search --title "APT28" -p
</code></pre>

## banshee sandbox

沙箱提交分析與設定檔管理。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-stats"><code>banshee sandbox stats</code></a></dt><dd><p>彙整可設定時間範圍內的沙箱提交資料，並輸出適用於 SOC 晨間簡報的摘要</p></dd>
    <dt><a href="#banshee-sandbox-list"><code>banshee sandbox list</code></a></dt><dd><p>列出沙箱樣本</p></dd>
    <dt><a href="#banshee-sandbox-search"><code>banshee sandbox search</code></a></dt><dd><p>依雜湊值、家族、標籤、殭屍網路、錢包、網路指標或原始 Triage 查詢搜尋樣本</p></dd>
    <dt><a href="#banshee-sandbox-get"><code>banshee sandbox get</code></a></dt><dd><p>依 ID 擷取單一沙箱樣本的摘要</p></dd>
    <dt><a href="#banshee-sandbox-download"><code>banshee sandbox download</code></a></dt><dd><p>下載一或多個樣本 ID 的原始提交位元組（以 AES 加密的 ZIP 壓縮檔封裝）</p></dd>
    <dt><a href="#banshee-sandbox-delete"><code>banshee sandbox delete</code></a></dt><dd><p>依 ID 刪除沙箱樣本</p></dd>
    <dt><a href="#banshee-sandbox-submit"><code>banshee sandbox submit</code></a></dt><dd><p>提交檔案、URL 或公開樣本進行沙箱分析</p></dd>
    <dt><a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a></dt><dd><p>為暫停於靜態分析階段的樣本指派分析設定檔</p></dd>
    <dt><a href="#banshee-sandbox-profile"><code>banshee sandbox profile</code></a></dt><dd><p>管理分析設定檔</p></dd>
    <dt><a href="#banshee-sandbox-report"><code>banshee sandbox report</code></a></dt><dd><p>樣本分析報告</p></dd>
</dl>

### banshee sandbox stats

彙整可設定時間範圍內的沙箱提交資料，並輸出適合 SOC 交班或每日篩選分類使用的「晨間簡報」。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">分數區間</h3>

<p>沙箱以 1–10 的分類評分量表對樣本進行評分。結果分組至以下區間：</p>

| 區間 | 分數範圍 | 意義 |
|---|---|---|
| `malicious` | 8–10 | 已知惡意程式，高可信度 |
| `suspicious` | 5–7 | 行為指標強烈 |
| `potentially_suspicious` | 3–4 | 存在部分指標 |
| `clean` | 1–2 | 低風險或良性 |

<h3 class="commands-reference">用法</h3>

```
banshee sandbox stats [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-stats--days"><a href="#banshee-sandbox-stats--days"><code>--days</code></a>, <code>-d</code> <i>days</i></dt><dd>
    <p>回溯天數</p>
    <p>預設為 7</p></dd>
    <dt id="banshee-sandbox-stats--subset"><a href="#banshee-sandbox-stats--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>要彙整的樣本範圍</p>
    <p>可用值：<code>owned</code>、<code>public</code>、<code>org</code></p>
    <p>預設為 <code>org</code></p></dd>
    <dt id="banshee-sandbox-stats--pretty"><a href="#banshee-sandbox-stats--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-stats--help"><a href="#banshee-sandbox-stats--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats --days 30 --pretty
</code></pre>

### banshee sandbox list

列出沙箱樣本——您自己的、您組織的（預設），或公開饋送。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox list [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-list--subset"><a href="#banshee-sandbox-list--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>要列出的樣本範圍</p>
    <p>可用值：<code>owned</code>、<code>public</code>、<code>org</code></p>
    <p>預設為 <code>org</code></p></dd>
    <dt id="banshee-sandbox-list--limit"><a href="#banshee-sandbox-list--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>回傳的最大樣本數量</p>
    <p>接受範圍：1–4095</p>
    <p>預設為 20</p></dd>
    <dt id="banshee-sandbox-list--pretty"><a href="#banshee-sandbox-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-list--help"><a href="#banshee-sandbox-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
</code></pre>

### banshee sandbox search

搜尋符合結構化篩選條件的樣本（雜湊值、家族、標籤、殭屍網路、錢包、IP、網域、URL、提交日期範圍），或使用原始 Triage 查詢。至少須提供一個篩選條件或 `--query`。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox search [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-search--hash"><a href="#banshee-sandbox-search--hash"><code>--hash</code></a> <i>hash</i></dt><dd>
    <p>依檔案雜湊值篩選（MD5/SHA1/SHA256）</p></dd>
    <dt id="banshee-sandbox-search--family"><a href="#banshee-sandbox-search--family"><code>--family</code></a> <i>family</i></dt><dd>
    <p>依惡意程式家族名稱篩選</p></dd>
    <dt id="banshee-sandbox-search--tag"><a href="#banshee-sandbox-search--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>依標籤篩選（可重複指定）</p></dd>
    <dt id="banshee-sandbox-search--botnet"><a href="#banshee-sandbox-search--botnet"><code>--botnet</code></a> <i>botnet</i></dt><dd>
    <p>依殭屍網路名稱篩選</p></dd>
    <dt id="banshee-sandbox-search--wallet"><a href="#banshee-sandbox-search--wallet"><code>--wallet</code></a> <i>wallet</i></dt><dd>
    <p>依錢包地址篩選</p></dd>
    <dt id="banshee-sandbox-search--ip"><a href="#banshee-sandbox-search--ip"><code>--ip</code></a> <i>ip</i></dt><dd>
    <p>依 IP 位址篩選</p></dd>
    <dt id="banshee-sandbox-search--domain"><a href="#banshee-sandbox-search--domain"><code>--domain</code></a> <i>domain</i></dt><dd>
    <p>依網域篩選</p></dd>
    <dt id="banshee-sandbox-search--url"><a href="#banshee-sandbox-search--url"><code>--url</code></a> <i>url</i></dt><dd>
    <p>依 URL 篩選</p></dd>
    <dt id="banshee-sandbox-search--from-date"><a href="#banshee-sandbox-search--from-date"><code>--from-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>篩選在此日期當天或之後提交的樣本</p></dd>
    <dt id="banshee-sandbox-search--to-date"><a href="#banshee-sandbox-search--to-date"><code>--to-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>篩選在此日期當天或之前提交的樣本</p></dd>
    <dt id="banshee-sandbox-search--query"><a href="#banshee-sandbox-search--query"><code>--query</code></a>, <code>-q</code> <i>query</i></dt><dd>
    <p>原始 Triage 查詢字串（與結構化篩選條件以 AND 合併使用）</p></dd>
    <dt id="banshee-sandbox-search--limit"><a href="#banshee-sandbox-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>回傳的最大樣本數量（1–200）</p>
    <p>預設為 50</p></dd>
    <dt id="banshee-sandbox-search--pretty"><a href="#banshee-sandbox-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-search--help"><a href="#banshee-sandbox-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
</code></pre>

### banshee sandbox get

依 ID 擷取單一沙箱樣本的摘要：目前狀態、整體分數、目標、建立和完成時間戳記、SHA256，以及各任務的詳細資訊。適用於進行中和已完成的樣本。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox get [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--sample-id"><a href="#banshee-sandbox-get--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>沙箱樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--pretty"><a href="#banshee-sandbox-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-get--help"><a href="#banshee-sandbox-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
</code></pre>

### banshee sandbox download

下載一或多個樣本 ID 的原始提交樣本位元組。每個樣本均以 AES 加密的 ZIP 壓縮檔封裝，密碼為 `infected`，以防止防毒軟體、安全電子郵件閘道或檔案管理員意外引爆。

請使用 `7z x -pinfected <sample-id>.zip` 解壓縮——標準的 `unzip` 無法可靠處理 AES 加密的 ZIP 檔案。

樣本 ID 可作為位置引數傳入，或透過 stdin 以空白字元分隔的方式傳入。若未指定 `--yes`，命令將提示確認。

> **安全注意事項：** 在下載和壓縮過程中，樣本位元組會短暫存在於此進程的記憶體中。積極的 EDR 記憶體掃描仍可能觸發警報。請在分析師專用主機上執行，而非日常使用的企業筆記型電腦。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox download [OPTIONS] [SAMPLE_IDS]...
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--sample-ids"><a href="#banshee-sandbox-download--sample-ids"><code>SAMPLE_IDS</code></a></dt><dd><p>一或多個樣本 ID（或從 stdin 以空白字元分隔的方式讀取）</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--output-dir"><a href="#banshee-sandbox-download--output-dir"><code>--output-dir</code></a>, <code>-d</code> <i>DIR</i></dt><dd>
    <p>儲存加密 ZIP 壓縮檔的目錄（若不存在則自動建立）。必填。</p></dd>
    <dt id="banshee-sandbox-download--yes"><a href="#banshee-sandbox-download--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>略過確認提示</p></dd>
    <dt id="banshee-sandbox-download--workers"><a href="#banshee-sandbox-download--workers"><code>--workers</code></a>, <code>-w</code> <i>N</i></dt><dd>
    <p>平行下載工作數量（1–16）</p>
    <p>預設為 1</p></dd>
    <dt id="banshee-sandbox-download--help"><a href="#banshee-sandbox-download--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# 解壓縮
7z x -pinfected ./samples/260501-h4p7laawme.zip
</code></pre>

### banshee sandbox delete

依 ID 刪除沙箱樣本並移除所有相關任務成果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox delete [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--sample-id"><a href="#banshee-sandbox-delete--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>要刪除的樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--yes"><a href="#banshee-sandbox-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>略過確認提示</p></dd>
    <dt id="banshee-sandbox-delete--help"><a href="#banshee-sandbox-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
</code></pre>

### banshee sandbox submit

提交樣本進行分析。本機檔案將直接上傳，URL 將在瀏覽器中引爆（或先以 `--fetch` 下載），公開樣本可使用 `--import` 依 ID 匯入。

預設情況下，此命令將輸出 JSON 提交收據。使用 `--wait` 可持續輪詢直到分析完成，並輸出概覽報告。

<h3 class="commands-reference">目標類型</h3>

| 目標 | 行為 |
|---|---|
| 本機檔案路徑 | 上傳並進行分析 |
| URL | 在瀏覽器中引爆 |
| URL + `--fetch` | 先下載，再作為檔案分析 |
| 公開樣本 ID + `--import` | 匯入至您組織的沙箱 |

<h3 class="commands-reference">用法</h3>

```
banshee sandbox submit [OPTIONS] TARGET
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--target"><a href="#banshee-sandbox-submit--target"><code>TARGET</code></a></dt><dd><p>檔案路徑、URL 或公開樣本 ID（搭配 <code>--import</code>）</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--fetch"><a href="#banshee-sandbox-submit--fetch"><code>--fetch</code></a></dt><dd>
    <p>先下載 URL 目標，再分析所產生的檔案。與 <code>--import</code> 互斥</p></dd>
    <dt id="banshee-sandbox-submit--import"><a href="#banshee-sandbox-submit--import"><code>--import</code></a></dt><dd>
    <p>將目標視為要匯入至您組織的公開樣本 ID。與 <code>--fetch</code> 互斥</p></dd>
    <dt id="banshee-sandbox-submit--profile"><a href="#banshee-sandbox-submit--profile"><code>--profile</code></a> <i>profile</i></dt><dd>
    <p>分析設定檔名稱或 ID。可重複指定以指派多個設定檔。與 <code>--interactive</code> 互斥</p></dd>
    <dt id="banshee-sandbox-submit--timeout"><a href="#banshee-sandbox-submit--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>分析逾時時間（秒）</p>
    <p>接受範圍：1–3600</p></dd>
    <dt id="banshee-sandbox-submit--network"><a href="#banshee-sandbox-submit--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>分析環境的網路模式</p>
    <p>可用值：<code>internet</code>、<code>drop</code>、<code>tor</code>、<code>vpn</code>、<code>sim200</code>、<code>sim404</code>、<code>simnx</code></p></dd>
    <dt id="banshee-sandbox-submit--geolocation"><a href="#banshee-sandbox-submit--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 出口國家代碼。需搭配 <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-submit--tags"><a href="#banshee-sandbox-submit--tags"><code>--tags</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>附加至提交的自訂標籤。可重複指定</p></dd>
    <dt id="banshee-sandbox-submit--password"><a href="#banshee-sandbox-submit--password"><code>--password</code></a> <i>password</i></dt><dd>
    <p>受保護壓縮檔的密碼</p></dd>
    <dt id="banshee-sandbox-submit--wait"><a href="#banshee-sandbox-submit--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>持續輪詢直到分析完成，然後輸出概覽報告</p></dd>
    <dt id="banshee-sandbox-submit--interactive"><a href="#banshee-sandbox-submit--interactive"><code>--interactive</code></a>, <code>-i</code></dt><dd>
    <p>在靜態分析階段暫停，以便透過 <a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a> 選擇檔案和設定檔。與 <code>--profile</code> 互斥</p></dd>
    <dt id="banshee-sandbox-submit--pretty"><a href="#banshee-sandbox-submit--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-submit--help"><a href="#banshee-sandbox-submit--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
</code></pre>

### banshee sandbox set-profile

為暫停於靜態分析階段的樣本（以 `--interactive` 提交）指派分析設定檔。使用 `--auto` 讓沙箱自動選擇設定檔，或使用 `--pick` 手動將特定檔案對應至特定設定檔。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox set-profile [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--sample-id"><a href="#banshee-sandbox-set-profile--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>暫停於靜態分析階段的樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--auto"><a href="#banshee-sandbox-set-profile--auto"><code>--auto</code></a>, <code>-a</code></dt><dd>
    <p>讓沙箱自動為所有檔案選擇設定檔。與 <code>--pick</code> 互斥</p></dd>
    <dt id="banshee-sandbox-set-profile--pick"><a href="#banshee-sandbox-set-profile--pick"><code>--pick</code></a> <i>FILE:PROFILE</i></dt><dd>
    <p>以 <code>FILE:PROFILE</code> 格式將特定檔案對應至特定設定檔。可重複指定。與 <code>--auto</code> 互斥</p></dd>
    <dt id="banshee-sandbox-set-profile--pretty"><a href="#banshee-sandbox-set-profile--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-set-profile--help"><a href="#banshee-sandbox-set-profile--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --auto -p
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
</code></pre>

### banshee sandbox profile

管理分析設定檔。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-profile-list"><code>banshee sandbox profile list</code></a></dt><dd><p>列出所有可用的分析設定檔</p></dd>
    <dt><a href="#banshee-sandbox-profile-get"><code>banshee sandbox profile get</code></a></dt><dd><p>取得特定設定檔的詳細資訊</p></dd>
    <dt><a href="#banshee-sandbox-profile-create"><code>banshee sandbox profile create</code></a></dt><dd><p>建立新的分析設定檔</p></dd>
    <dt><a href="#banshee-sandbox-profile-update"><code>banshee sandbox profile update</code></a></dt><dd><p>更新現有的分析設定檔</p></dd>
    <dt><a href="#banshee-sandbox-profile-delete"><code>banshee sandbox profile delete</code></a></dt><dd><p>刪除分析設定檔</p></dd>
</dl>

#### banshee sandbox profile list

列出所有可用的分析設定檔。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile list [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-list--pretty"><a href="#banshee-sandbox-profile-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-profile-list--help"><a href="#banshee-sandbox-profile-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
</code></pre>

#### banshee sandbox profile get

依名稱或 ID 取得特定分析設定檔的詳細資訊。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile get [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--profile-id-or-name"><a href="#banshee-sandbox-profile-get--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>設定檔 UUID 或顯示名稱</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--pretty"><a href="#banshee-sandbox-profile-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-profile-get--help"><a href="#banshee-sandbox-profile-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
</code></pre>

#### banshee sandbox profile create

建立新的分析設定檔。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">設定檔標籤</h3>

<p>標籤定義設定檔的作業系統與環境。地區設定標籤必須搭配至少一個 <code>os</code> 標籤使用。</p>

<pre><code class="language-bash">
# 僅指定作業系統
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64

# 指定作業系統 + 地區設定
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64 -T locale:en-us
</code></pre>

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile create [OPTIONS]
```

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-create--name"><a href="#banshee-sandbox-profile-create--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>設定檔顯示名稱。必填</p></dd>
    <dt id="banshee-sandbox-profile-create--tag"><a href="#banshee-sandbox-profile-create--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>設定檔標籤（例如 <code>os:windows10-2004-x64</code>、<code>locale:en-us</code>）。可重複指定。必填</p></dd>
    <dt id="banshee-sandbox-profile-create--timeout"><a href="#banshee-sandbox-profile-create--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>分析逾時時間（秒）</p>
    <p>接受範圍：1–3600</p>
    <p>預設為 120</p></dd>
    <dt id="banshee-sandbox-profile-create--network"><a href="#banshee-sandbox-profile-create--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>網路模式</p>
    <p>可用值：<code>internet</code>、<code>drop</code>、<code>tor</code>、<code>vpn</code>、<code>sim200</code>、<code>sim404</code>、<code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-create--geolocation"><a href="#banshee-sandbox-profile-create--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 出口國家代碼。可重複指定。需搭配 <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-profile-create--browser"><a href="#banshee-sandbox-profile-create--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>用於 URL 引爆的瀏覽器</p>
    <p>可用值：<code>chrome</code>、<code>firefox</code>、<code>ie11</code>、<code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-create--pretty"><a href="#banshee-sandbox-profile-create--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-profile-create--help"><a href="#banshee-sandbox-profile-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
</code></pre>

#### banshee sandbox profile update

依名稱或 ID 更新現有的分析設定檔。至少須提供一個選項。

輸出為 `{"updated": true}` 或 `{"updated": false}`（兩者皆以 0 結束）。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile update [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--profile-id-or-name"><a href="#banshee-sandbox-profile-update--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>要更新的設定檔 UUID 或顯示名稱</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--name"><a href="#banshee-sandbox-profile-update--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>新的設定檔顯示名稱</p></dd>
    <dt id="banshee-sandbox-profile-update--tag"><a href="#banshee-sandbox-profile-update--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>取代所有現有標籤。可重複指定</p></dd>
    <dt id="banshee-sandbox-profile-update--timeout"><a href="#banshee-sandbox-profile-update--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>分析逾時時間（秒）</p>
    <p>接受範圍：1–3600</p></dd>
    <dt id="banshee-sandbox-profile-update--network"><a href="#banshee-sandbox-profile-update--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>網路模式</p>
    <p>可用值：<code>internet</code>、<code>drop</code>、<code>tor</code>、<code>vpn</code>、<code>sim200</code>、<code>sim404</code>、<code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-update--geolocation"><a href="#banshee-sandbox-profile-update--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 出口國家代碼。可重複指定。需搭配 <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-profile-update--browser"><a href="#banshee-sandbox-profile-update--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>用於 URL 引爆的瀏覽器</p>
    <p>可用值：<code>chrome</code>、<code>firefox</code>、<code>ie11</code>、<code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-update--unset"><a href="#banshee-sandbox-profile-update--unset"><code>--unset</code></a> <i>field</i></dt><dd>
    <p>清除某個欄位。可重複指定</p>
    <p>可用值：<code>network</code>、<code>browser</code>、<code>geolocation</code></p>
    <p>不可與同一欄位的設定選項同時使用。<code>--unset network</code> 與 <code>--geolocation</code> 衝突</p></dd>
    <dt id="banshee-sandbox-profile-update--pretty"><a href="#banshee-sandbox-profile-update--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-profile-update--help"><a href="#banshee-sandbox-profile-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
</code></pre>

#### banshee sandbox profile delete

依名稱或 ID 刪除分析設定檔。刪除不存在的設定檔將輸出警告並以 0 結束。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox profile delete [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--profile-id-or-name"><a href="#banshee-sandbox-profile-delete--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>要刪除的設定檔 UUID 或顯示名稱</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--yes"><a href="#banshee-sandbox-profile-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>略過確認提示</p></dd>
    <dt id="banshee-sandbox-profile-delete--help"><a href="#banshee-sandbox-profile-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
</code></pre>

### banshee sandbox report

樣本分析報告。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox report [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">命令</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-report-overview"><code>banshee sandbox report overview</code></a></dt><dd><p>已完成樣本的完整概覽報告</p></dd>
    <dt><a href="#banshee-sandbox-report-static"><code>banshee sandbox report static</code></a></dt><dd><p>靜態分析報告——在行為任務完成前即可取得</p></dd>
    <dt><a href="#banshee-sandbox-report-behavioral"><code>banshee sandbox report behavioral</code></a></dt><dd><p>行為分析報告——每個已完成任務各一個物件</p></dd>
</dl>

#### banshee sandbox report overview

已完成樣本的完整概覽報告。包含判定分數、惡意程式家族、標籤、雜湊值、偵測特徵、提取的惡意程式設定、網路 IOC 及各任務結果。樣本必須處於 `reported` 狀態。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox report overview [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--sample-id"><a href="#banshee-sandbox-report-overview--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>要擷取報告的樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--wait"><a href="#banshee-sandbox-report-overview--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>持續輪詢直到報告就緒（最長 30 分鐘）。若逾時後報告仍未就緒，則以非零值結束</p></dd>
    <dt id="banshee-sandbox-report-overview--pretty"><a href="#banshee-sandbox-report-overview--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-report-overview--help"><a href="#banshee-sandbox-report-overview--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
</code></pre>

#### banshee sandbox report static

樣本的靜態分析報告。包含判定分數、標籤、解包後的檔案、靜態偵測特徵及提取的惡意程式設定。在行為任務完成前即可取得。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox report static [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--sample-id"><a href="#banshee-sandbox-report-static--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>要擷取靜態報告的樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--wait"><a href="#banshee-sandbox-report-static--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>持續輪詢直到報告就緒（最長 10 分鐘）</p></dd>
    <dt id="banshee-sandbox-report-static--pretty"><a href="#banshee-sandbox-report-static--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-report-static--help"><a href="#banshee-sandbox-report-static--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
</code></pre>

#### banshee sandbox report behavioral

樣本的行為分析報告。針對每個已完成的行為任務回傳一個 JSON 物件，包含判定分數、平台、已觸發的特徵、觀察到的進程、網路活動及提取的惡意程式設定。

未完成的任務將從輸出中省略並記錄於 stderr；在所有任務完成前，命令以非零值結束。若樣本沒有行為任務，則回傳空陣列並以 0 結束。

預設情況下，此命令將以 JSON 格式輸出結果。

<h3 class="commands-reference">用法</h3>

```
banshee sandbox report behavioral [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">引數</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--sample-id"><a href="#banshee-sandbox-report-behavioral--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>要擷取行為報告的樣本 ID</p></dd>
</dl>

<h3 class="commands-reference">選項</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--wait"><a href="#banshee-sandbox-report-behavioral--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>持續輪詢直到所有任務完成（最長 30 分鐘）</p></dd>
    <dt id="banshee-sandbox-report-behavioral--full-cmd"><a href="#banshee-sandbox-report-behavioral--full-cmd"><code>--full-cmd</code></a></dt><dd>
    <p>顯示完整、未截斷的進程命令列。命令列內容直接來自惡意程式樣本，應視為不受信任的輸入</p></dd>
    <dt id="banshee-sandbox-report-behavioral--pretty"><a href="#banshee-sandbox-report-behavioral--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>以人類可讀的格式美化輸出結果</p></dd>
    <dt id="banshee-sandbox-report-behavioral--help"><a href="#banshee-sandbox-report-behavioral--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>顯示此命令的說明</p>
</dl>

<h3 class="commands-reference">使用範例</h3>

<pre><code class="language-bash">
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
</code></pre>