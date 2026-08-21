# コマンドラインリファレンス

## banshee

PS Banshee は、セキュリティプロフェッショナルおよび SOC チーム向けに構築された、Recorded Future Intelligence への高速かつ効率的なアクセスを提供するコマンドラインツールです。

<h3 class="commands-reference">Usage</h3>

```
banshee [OPTIONS] <COMMAND>
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca"><code>banshee ca</code></a></dt><dd><p>Recorded Future Classic Alerts の検索、参照、更新</p></dd>
    <dt><a href="#banshee-email"><code>banshee email</code></a></dt><dd><p>メールファイル（EML）を Recorded Future インテリジェンスでエンリッチ</p></dd>
    <dt><a href="#banshee-entity"><code>banshee entity</code></a></dt><dd><p>Recorded Future エンティティの検索と参照</p></dd>
    <dt><a href="#banshee-ioc"><code>banshee ioc</code></a></dt><dd><p>侵害インジケーター（IOC）の検索と参照</p></dd>
    <dt><a href="#banshee-list"><code>banshee list</code></a></dt><dd><p>Recorded Future リストおよびウォッチリストの管理</p></dd>
    <dt><a href="#banshee-pba"><code>banshee pba</code></a></dt><dd><p>Recorded Future Playbook Alerts の検索、参照、更新</p></dd>
    <dt><a href="#banshee-pcap"><code>banshee pcap</code></a></dt><dd><p>パケットキャプチャ（pcap）ファイルを Recorded Future Intelligence でエンリッチして解析</p></dd>
    <dt><a href="#banshee-risklist"><code>banshee risklist</code></a></dt><dd><p>リスクリストの管理</p></dd>
    <dt><a href="#banshee-rules"><code>banshee rules</code></a></dt><dd><p>検知ルールの検索とダウンロード</p></dd>
</dl>

## banshee ca

Recorded Future Classic Alerts の検索、参照、更新を行います。

<h3 class="commands-reference">Usage</h3>

```
banshee ca [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca-lookup"><code>banshee ca lookup</code></a></dt><dd><p>Classic Alert を参照する</p></dd>
    <dt><a href="#banshee-ca-search"><code>banshee ca search</code></a></dt><dd><p>Classic Alerts を検索する</p></dd>
    <dt><a href="#banshee-ca-rules"><code>banshee ca rules</code></a></dt><dd><p>Classic Alert ルールを検索する</p></dd>
    <dt><a href="#banshee-ca-update"><code>banshee ca update</code></a></dt><dd><p>1 件以上の Classic Alert を更新する</p></dd>
    <dt><a href="#banshee-ca-export"><code>banshee ca export</code></a></dt><dd><p>Classic Alerts を JSON または CSV 形式でエクスポートする</p></dd>
</dl>

### banshee ca lookup

Classic Alert を参照します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ca lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--alert-id"><a href="#banshee-ca-lookup--alert-id"><code>ALERT_ID</code></a></dt><dd><p>参照するアラートの ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ca-lookup--help"><a href="#banshee-ca-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee ca search

Classic Alerts を検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ca search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-search--triggered"><a href="#banshee-ca-search--triggered"><code>--triggered</code>, <code>-t</code></a> <i>triggered</i></dt><dd>
    <p>トリガー日時でフィルタします。例: 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)</p>
    <p>デフォルト値は 1d です。</p><dd></dd>
    <dt id="banshee-ca-search--rule"><a href="#banshee-ca-search--rule"><code>--rule</code></a> <i>rule-name</i></dt><dd>
    <p>アラートルール名でフィルタします（フリーテキスト）。</p><dd></dd>
    <dt id="banshee-ca-search--status"><a href="#banshee-ca-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>アラートのステータスでフィルタします。</p>
    <p>指定可能な値: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-search--pretty"><a href="#banshee-ca-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ca-search--help"><a href="#banshee-ca-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee ca rules

Classic Alert ルールを検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ca rules [OPTIONS] [FREETEXT]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--freetext"><a href="#banshee-ca-rules--freetext"><code>FREETEXT</code></a></dt><dd><p>省略可能。アラートルールを名前でフィルタするために使用するフリーテキスト。</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--pretty"><a href="#banshee-ca-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ca-rules--help"><a href="#banshee-ca-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee ca update

1 件以上の Classic Alert を更新します。

<h3 class="commands-reference">Usage</h3>

```
banshee ca update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--alert-id"><a href="#banshee-ca-update--alert-id"<code>ALERT_IDS</code></a></dt><dd><p>スペース区切りで指定する 1 件以上のアラート ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--status"><a href="#banshee-ca-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>アラートをこのステータスに更新します。</p>
    <p>指定可能な値: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-update--note"><a href="#banshee-ca-update--note"><code>--note</code></a>,  <code>-n</code> <i>note</i></dt><dd>
    <p>アラートのノートテキスト。</p><p>ノートの文字数上限は 1000 文字です。</p><dd></dd>
    <dt id="banshee-ca-update--append"><a href="#banshee-ca-update--append"><code>--append</code></a>,  <code>-a</code></dt><dd>
    <p>アラートにすでにノートが存在する場合、このフラグを指定するとノートテキストを追記します。</p><dd></dd>
    <dt id="banshee-ca-update--assignee"><a href="#banshee-ca-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>アラートを割り当てる新しいユーザー。uhash またはユーザーのメールアドレスを指定します。例: uhash:3aXZxdkM12, analyst@acme.com</p><dd></dd>
    <dt id="banshee-ca-update--help"><a href="#banshee-ca-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>1 件以上のアラート ID（スペース区切り）を指定し、必要な更新オプションを設定します:</p>

<pre><code class="language-bash">
banshee ca update <alert id> -s Dismissed
banshee ca update <alert id> -s Dismissed -n "note text"
banshee ca update <alert id1> <alert id2>-s Dismissed -n "note text" -a analyst@acme.com
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. 引数として直接指定する（1 件または複数件）:</h4>

<pre><code class="language-bash">
banshee ca update ALERT_ID -s Resolved
banshee ca update ALERT_ID_1 ALERT_ID_2 -s Pending
</code></pre>

<h4>2. ファイルまたは標準入力から読み込む:</h4>

<p>アラート ID を 1 行ずつ記載したファイル（例: <code>alerts.txt</code>）がある場合:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>以下のコマンドで、一覧に含まれる全アラートを更新できます:</p>

<pre><code class="language-bash">
banshee ca update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee ca update -s Dismissed
</code></pre>

<h4>3. 検索コマンドからパイプで渡す:</h4>

<p><code>jq</code> などのツールを使って検索結果からアラート ID を抽出し、update コマンドにパイプで渡します:</p>

<pre><code class="language-bash">
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"
</code></pre>

<h3 class="commands-reference">Note Append</h3>

<p>Classic Alerts はノートを 1 件のみサポートします。デフォルトでは、<code>update</code> コマンドは既存のノートを新しいノートで上書きします。
既存のノートに追記したい場合は、<code>--append</code>（<code>-A</code>）オプションを使用してください。</p>

### banshee ca export

Classic Alerts を JSON または CSV 形式でエクスポートします。標準入力からアラート ID を読み込みます。通常は [`banshee ca search`](#banshee-ca-search) からパイプで渡します。

<h3 class="commands-reference">Output Formats</h3>

<p><b>JSON（デフォルト）</b> — 各 ID に対して Recorded Future API が返す<i>完全な</i>アラートオブジェクトを出力します。トップレベルのフィールドすべてに加え、ヒット、エンティティ、エビデンス、AI インサイト、レビュー履歴、ポータル URL などのネストされたデータも含みます。ダウンストリームのツール連携、<code>jq</code> パイプライン、再取り込みに最適です。</p>

<p><b>CSV（<a href="#banshee-ca-export--csv"><code>--csv</code></a>）</b> — スプレッドシートやレポート作成向けの概要サマリーを出力します。以下に示す 11 列のみを書き込みます（先頭にヘッダー行あり）。JSON レスポンスに含まれるその他のフィールドはすべて省略されます。</p>

| Field | Description |
|---|---|
| `ID` | Classic Alert ID |
| `Priority` | アラートの優先度 — アラートルールが優先ルールの場合は `High`、それ以外は `Informational` |
| `Alert Rule` | トリガーしたアラートルールの名前 |
| `Status` | ポータルのステータス（例: `New`, `Pending`, `Dismissed`, `Resolved`） |
| `Created` | トリガーされたタイムスタンプ（UTC） |
| `Updated` | 最終更新タイムスタンプ — *現在は常に空。将来の API サポートのために予約済み* |
| `Title` | アラートのタイトル |
| `Assignee` | 割り当てられたユーザー（uhash またはメールアドレス） |
| `URL` | アラートの Recorded Future ポータル URL |
| `Entities` | 主要なエンティティ名（`;` 区切り） |
| `Recorded Future AI Insights` | AI が生成したインサイトテキストまたはコメント |

<h3 class="commands-reference">Usage</h3>

```
banshee ca search [SEARCH_OPTIONS] | banshee ca export [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-export--csv"><a href="#banshee-ca-export--csv"><code>--csv</code></a></dt><dd>
    <p>上記の固定列セットで CSV として出力します。このフラグを指定しない場合、コマンドは JSON を出力します。</p><dd></dd>
    <dt id="banshee-ca-export--help"><a href="#banshee-ca-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Piped Input</h3>

<p><code>banshee ca export</code> はパイプ入力のみを受け付けます。<a href="#banshee-ca-search"><code>banshee ca search</code></a> が生成する JSON 配列を受け取り、アラート ID を抽出して各アラートの完全なデータを取得します。パイプなしでコマンドを実行するとエラーになります。</p>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s New | banshee ca export --csv > alerts.csv
</code></pre>

## banshee entity

Recorded Future エンティティの検索と参照を行います。

<h3 class="commands-reference">Usage</h3>

```
banshee entity [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-entity-lookup"><code>banshee entity lookup</code></a></dt><dd><p>ID でエンティティを参照する</p></dd>
    <dt><a href="#banshee-entity-search"><code>banshee entity search</code></a></dt><dd><p>名前やタイプでエンティティを検索する</p></dd>
</dl>

### banshee entity lookup

ID でエンティティを参照します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee entity lookup [OPTIONS] ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--entity-id"><a href="#banshee-entity-lookup--entity-id"<code>ENTITY_ID</code></a></dt><dd><p>参照するエンティティ ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--pretty"><a href="#banshee-entity-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-entity-lookup--help"><a href="#banshee-entity-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee entity search

名前やタイプでエンティティを検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee entity search [OPTIONS] NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--name"><a href="#banshee-entity-search--name"><code>NAME</code></a></dt><dd><p>検索するエンティティの名前</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--type"><a href="#banshee-entity-search--type"><code>--type</code>, <code>-t</code></a> <i>entity-type</i></dt><dd>
    <p>検索するエンティティタイプ</p>
    <p>異なるエンティティタイプに対して複数回指定できます</p>
    <p>サポートされている値:</p>
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
    <p>結果の件数を制限します</p>
    <p>最大件数は 100 件です</p>
    <p>デフォルトは 100 件です</p><dd></dd>
    <dt id="banshee-entity-search--pretty"><a href="#banshee-entity-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-entity-search--help"><a href="#banshee-entity-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>


## banshee email

メールファイル（EML）を Recorded Future インテリジェンスでエンリッチします。

<h3 class="commands-reference">Usage</h3>

```
banshee email [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-email-enrich"><code>banshee email enrich</code></a></dt><dd><p>EML ファイルを Recorded Future インテリジェンスでエンリッチする</p></dd>
</dl>

### banshee email enrich

EML ファイルを Recorded Future Intelligence でエンリッチします。このコマンドは EML ファイルを解析し、ヘッダーから IP アドレスを、本文から `http`/`https` で始まる URL を抽出し、脅威インテリジェンスデータでエンリッチします。デフォルトでは、リスクスコアのしきい値を満たすインジケーターのみが表示されるようにフィルタリングされます。`--threat-hunt` を使用すると、リスクスコアのしきい値を下回っていても、脅威アクターに関連するインジケーターを含めることができます。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">JSON Output</h3>

JSON 配列内の各結果オブジェクトには、以下のフィールドが含まれます。

| Field | Description |
|---|---|
| `ioc` | メールから抽出されたインジケーター — IP アドレスまたは URL |
| `type` | インジケーターのタイプ（例: `ip` または `url`） |
| `location` | インジケーターが検出されたメールのセクション（例: `header` または `body`） |
| `risk_score` | Recorded Future のリスクスコア |
| `ta_names` | このインジケーターに関連する脅威アクター名のリスト。不明な場合は空 |
| `malwares` | このインジケーターに関連するマルウェアファミリー名のリスト。不明な場合は空 |
| `first_seen` | 最初に記録された観測の ISO 8601 タイムスタンプ |
| `last_seen` | 最新の観測の ISO 8601 タイムスタンプ |
| `count_of_analyst_notes` | このインジケーターを参照している Recorded Future アナリストノートの件数 |
| `rule_evidence` | 個別のリスクルールエビデンスの詳細の配列。深刻度の高い順にソート済み |

`rule_evidence` 配列内の各オブジェクトには以下が含まれます。

| Field | Description |
|---|---|
| `rule` | 発動した特定の Recorded Future リスクルールの名前 |
| `level` | このルールの深刻度レベル — 整数が大きいほど深刻 |
| `timestamp` | このルールの最新の観測の ISO 8601 タイムスタンプ |
| `evidence_string` | エビデンスの人間が読みやすい要約 |

<h3 class="commands-reference">Usage</h3>

```
banshee email enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--file-path"><a href="#banshee-email-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>エンリッチする EML ファイルへのパス</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--risk-score"><a href="#banshee-email-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>このしきい値を超えるリスクスコア（0〜99）を持つインジケーターのみを表示するようにフィルタリングします</p><p>デフォルト値は 65</p></dd>
    <dt id="banshee-email-enrich--threat-hunt"><a href="#banshee-email-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>リスクスコアのしきい値に関わらず、脅威アクターに関連するインジケーターを含めます</p></dd>
    <dt id="banshee-email-enrich--pretty"><a href="#banshee-email-enrich--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-email-enrich--help"><a href="#banshee-email-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code class="language-bash">
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p
banshee email enrich suspicious.eml --threat-hunt
</code></pre>

## banshee ioc

侵害インジケーター（IOC）の検索と参照を行います。

<h3 class="commands-reference">Usage</h3>

```
banshee ioc [OPTIONS] COMMAND [ARGS]...
```
<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ioc-lookup"><code>banshee ioc lookup</code></a></dt><dd><p>設定可能な詳細度で 1 件以上の IOC を詳細エンリッチ</p></dd>
    <dt><a href="#banshee-ioc-bulk-lookup"><code>banshee ioc bulk-lookup</code></a></dt><dd><p>リスクスコアとトリガーされたルールを返す高速バルクエンリッチ — API コールごとに最大 1000 件の IOC をバッチ処理</p></dd>
    <dt><a href="#banshee-ioc-search"><code>banshee ioc search</code></a></dt><dd><p>IOC を検索する</p></dd>
    <dt><a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></dt><dd><p>IOC ルールを検索する</p></dd>
</dl>

### banshee ioc lookup

1 件以上の IOC を詳細エンリッチします。インジケーターごとに 1 回の API コールを行います。[`--verbosity`](#banshee-ioc-lookup--verbosity) を使用して、基本的なリスクスコアからリンクやアナリストノートなどを含む完全なインテリジェンスまで、返されるフィールド数を制御できます。豊富なコンテキストが必要な場合はこのコマンドを使用してください。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ioc lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>参照するエンティティタイプ</p>
    <p>サポートされている値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-lookup--ioc"><a href="#banshee-ioc-lookup--ioc"><code>IOC</code></a></dt><dd><p>参照する 1 件以上の IOC（スペース区切り）</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--ai-insights"><a href="#banshee-ioc-lookup--ai-insights"><code>--ai-insights</code></a>,  <code>-a</code></dt><dd>
    <p>関連するリスクルールと主要な参照情報を要約する、Recorded Future による AI 生成インサイトを有効にします。</p>
    <p><strong>注意:</strong> AI 処理のため、レスポンス時間がわずかに長くなる場合があります。</p<dd></dd>
    <dt id="banshee-ioc-lookup--verbosity"><a href="#banshee-ioc-lookup--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>レスポンスで返されるデータ量を制御します（1〜5）。詳細度レベルが高いほど、JSON 出力に追加フィールドと詳細が含まれます。</p>
    <p><strong>注意:</strong> 詳細度レベルが高いほど、データ取得量の増加によりレスポンス時間が遅くなる場合があります。</p>
    <p>デフォルト値: 1</p>
    <h4>詳細度レベル別の利用可能なフィールド</h4>
    <p><b>ip:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, location, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, location, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, dnsPortCert, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, scanner, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>domain:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>url:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
    </ul>

    <p><b>hash:</b></p>
    <ul>
        <li><b>1:</b> entity, hashAlgorithm, risk, timestamps</li>
        <li><b>2:</b> entity, fileHashes, hashAlgorithm, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, fileHashes, hashAlgorithm, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>vulnerability:</b></p>
    <ul>
        <li><b>1:</b> entity, lifecycleStage, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, lifecycleStage, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, lifecycleStage, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, cpe, cpe22uri, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, nvdDescription, nvdReferences, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>
    </dd>
    <dt id="banshee-ioc-lookup--pretty"><a href="#banshee-ioc-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ioc-lookup--help"><a href="#banshee-ioc-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23,139.224.189.177 -p
</code></pre>

カンマまたは改行区切りの IOC リストをパイプして参照する:

<pre><code>
cat test_ips.csv| banshee ioc lookup ip -p
</code></pre>


### banshee ioc bulk-lookup

単一タイプの任意の数の IOC を高速バルクエンリッチします。コマンドは API コールごとに最大 1000 件の IOC をバッチ処理し、バッチ処理を自動的に行うため、大量処理時に [`banshee ioc lookup`](#banshee-ioc-lookup) よりも大幅に高速です。

インジケーターごとにリスクスコアとトリガーされたリスクルールという固定フィールドセットを返します。大量トリアージに使用してください。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ioc bulk-lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--entity-type"><a href="#banshee-ioc-bulk-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>エンリッチするエンティティタイプ</p>
    <p>サポートされている値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-bulk-lookup--ioc"><a href="#banshee-ioc-bulk-lookup--ioc"><code>IOC</code></a></dt><dd><p>エンリッチする 1 件以上の IOC（スペース区切り）。標準入力からの入力も受け付けます（以下の例を参照）。</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--pretty"><a href="#banshee-ioc-bulk-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ioc-bulk-lookup--help"><a href="#banshee-ioc-bulk-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877
</code></pre>

<h4>ファイル / Stdin 入力</h4>

改行区切りの IOC ファイル（1 行に 1 件）をパイプまたはリダイレクトする:

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

<h4>名前とスコアの抽出</h4>
`jq` を使用して JSON 出力から特定のフィールドを抽出する例:

<pre><code>
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'
</code></pre>


### banshee ioc search

IOC を検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ioc search [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>参照するエンティティタイプ</p>
    <p>サポートされている値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-search--limit"><a href="#banshee-ioc-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>結果の件数を制限します</p>
    <p>最大件数は 1000 件です</p>
    <p>デフォルト値: 5</p><dd></dd>
    <dt id="banshee-ioc-search--risk-score"><a href="#banshee-ioc-search--risk-score"><code>--risk-score</code>, <code>-r</code></a> <i>risk-score</i></dt><dd>
    <p>リスクスコア範囲でフィルタリングします。例:</p>
    <p>
        <ul>
            <li><code>--risk-score '[20,90]'</code> &rarr; <code>20 &lt;= riskScore &lt;= 90</code> と同じ</li>
            <li><code>--risk-score '(20,90)'</code> &rarr; <code>20 &lt; riskScore &lt; 90</code> と同じ</li>
            <li><code>--risk-score '[20,90)'</code> &rarr; <code>20 &lt;= riskScore &lt; 90</code> と同じ</li>
            <li><code>--risk-score '[20,)'</code> &rarr; <code>20 &lt;= riskScore</code> と同じ</li>
            <li><code>--risk-score '[,90)'</code> &rarr; <code>riskScore &lt; 90</code> と同じ</li>
        </ul>
    </p>
    <p>正しく解析されるよう、リスクスコア範囲をクォートで囲んでください</p>
    <dd></dd>
    <dt id="banshee-ioc-search--risk-rule"><a href="#banshee-ioc-search--risk-rule"><code>--risk-rule</code>, <code>-R</code></a> <i>rule-name</i></dt><dd>
    <p>リスクルール名でフィルタリングします</p>
    <p>利用可能なオプションについては、この<a href="https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future" target="_blank">サポート記事</a>（特にリスクルールテーブルの <b>Machine Name</b> 列）を参照するか、<a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> コマンドを使用してください</p><dd></dd>
    <dt id="banshee-ioc-search--verbosity"><a href="#banshee-ioc-search--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>レスポンスで返されるデータ量を制御します（1〜5）。詳細度レベルが高いほど、JSON 出力に追加フィールドと詳細が含まれます。</p>
    <p><strong>注意:</strong> 詳細度レベルが高いほど、データ取得量の増加によりレスポンス時間が遅くなる場合があります。</p>
    <p>デフォルト値: 1</p>
    <h4>詳細度レベル別の利用可能なフィールド</h4>
    <p><b>ip:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, location, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, location, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, dnsPortCert, enterpriseLists, entity, intelCard, links, location, risk, riskMapping, scanner, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>domain:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>url:</b></p>
    <ul>
        <li><b>1:</b> entity, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, intelCard, links, risk, riskMapping, sightings, timestamps</li>
    </ul>

    <p><b>hash:</b></p>
    <ul>
        <li><b>1:</b> entity, hashAlgorithm, risk, timestamps</li>
        <li><b>2:</b> entity, fileHashes, hashAlgorithm, intelCard, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, fileHashes, hashAlgorithm, intelCard, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, enterpriseLists, entity, fileHashes, hashAlgorithm, intelCard, links, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>

    <p><b>vulnerability:</b></p>
    <ul>
        <li><b>1:</b> entity, lifecycleStage, risk, timestamps</li>
        <li><b>2:</b> entity, intelCard, lifecycleStage, risk, timestamps</li>
        <li><b>3:</b> analystNotes, entity, intelCard, lifecycleStage, links, risk, timestamps</li>
        <li><b>4:</b> analystNotes, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, risk, riskMapping, sightings, threatLists, timestamps</li>
        <li><b>5:</b> analystNotes, cpe, cpe22uri, cvss, cvssv3, cvssv4, enterpriseLists, entity, intelCard, lifecycleStage, links, nvdDescription, nvdReferences, risk, riskMapping, sightings, threatLists, timestamps</li>
    </ul>
    </dd>
    <dt id="banshee-ioc-search--pretty"><a href="#banshee-ioc-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ioc-search--help"><a href="#banshee-ioc-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee ioc rules

指定されたエンティティタイプの IOC ルールを検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee ioc rules [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--entity-type"><a href="#banshee-ioc-rules--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>IOC ルールのエンティティタイプ</p>
    <p>サポートされている値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--freetext"><a href="#banshee-ioc-rules--freetext"><code>--freetext</code>, <code>-F</code></a> <i>freetext-rule-name</i></dt><dd>
    <p>フリーテキスト検索でリスクルール名をフィルタリングします</p><dd></dd>
    <dt id="banshee-ioc-rules--mitre"><a href="#banshee-ioc-rules--mitre"><code>--mitre-code</code>, <code>-M</code></a> <i>mitre-code</i></dt><dd>
    <p>MITRE ATT&CK コードでフィルタリングします</p><dd></dd>
    <dt id="banshee-ioc-rules--criticality"><a href="#banshee-ioc-rules--criticality"><code>--criticality</code>, <code>-C</code></a> <i>criticality</i></dt><dd>
    <p>重要度でフィルタリングします。値が高いほど重要度が高くなります</p>
    <p>使用できる値は 1〜5 です</p>
    <p><strong>重要度レベル（IP、Domain、URL、Hash）</strong></p>
    <ul>
        <li><code>4</code> – Very Malicious（リスクスコア帯: 90〜99）</li>
        <li><code>3</code> – Malicious（リスクスコア帯: 65〜89）</li>
        <li><code>2</code> – Suspicious（リスクスコア帯: 25〜64）</li>
        <li><code>1</code> – Unusual（リスクスコア帯: 5〜24）</li>
        <li><code>0</code> – No evidence of risk（リスクスコア帯: 0）</li>
    </ul>
    <p><strong>重要度レベル（Vulnerability）</strong></p>
    <ul>
        <li><code>5</code> – Very Critical（リスクスコア帯: 90〜99）</li>
        <li><code>4</code> – Critical（リスクスコア帯: 80〜89）</li>
        <li><code>3</code> – High（リスクスコア帯: 65〜79）</li>
        <li><code>2</code> – Medium（リスクスコア帯: 25〜64）</li>
        <li><code>1</code> – Low（リスクスコア帯: 5〜24）</li>
        <li><code>0</code> – No evidence of risk（リスクスコア帯: 0）</li>
    </ul>
    <dd></dd>
    <dt id="banshee-ioc-rules--pretty"><a href="#banshee-ioc-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-ioc-rules--help"><a href="#banshee-ioc-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

## banshee list

Recorded Future のリストおよびウォッチリストを管理します。

<h3 class="commands-reference">Usage</h3>

```
banshee list [OPTIONS] COMMAND [ARGS]...
```
<dl class="commands-reference">
    <dt><a href="#banshee-list-create"><code>banshee list create</code></a></dt><dd><p>新しいリストを作成する</p></dd>
    <dt><a href="#banshee-list-info"><code>banshee list info</code></a></dt><dd><p>リストの基本情報を取得する</p></dd>
    <dt><a href="#banshee-list-search"><code>banshee list search</code></a></dt><dd><p>リストを検索する</p></dd>
    <dt><a href="#banshee-list-status"><code>banshee list status</code></a></dt><dd><p>リストのステータスを取得する</p></dd>
    <dt><a href="#banshee-list-entities"><code>banshee list entities</code></a></dt><dd><p>リスト内のエンティティを取得する</p></dd>
    <dt><a href="#banshee-list-add"><code>banshee list add</code></a></dt><dd><p>リストにエンティティを追加する</p></dd>
    <dt><a href="#banshee-list-bulk-add"><code>banshee list bulk-add</code></a></dt><dd><p>リストに複数のエンティティを一括追加する</p></dd>
    <dt><a href="#banshee-list-remove"><code>banshee list remove</code></a></dt><dd><p>リストからエンティティを削除する</p></dd>
    <dt><a href="#banshee-list-bulk-remove"><code>banshee list bulk-remove</code></a></dt><dd><p>リストから複数のエンティティを一括削除する</p></dd>
    <dt><a href="#banshee-list-copy"><code>banshee list copy</code></a></dt><dd><p>あるリストから別のリストにエンティティをコピーする</p></dd>
    <dt><a href="#banshee-list-clear"><code>banshee list clear</code></a></dt><dd><p>リストのすべてのエンティティをクリアする</p></dd>
    <dt><a href="#banshee-list-entries"><code>banshee list entries</code></a></dt><dd><p>リストからテキストエントリを取得する</p></dd>
</dl>

### banshee list create

新しいリストを作成します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list create [OPTIONS] NAME [LIST_TYPE]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>NAME</code></a></dt><dd><p>作成するリスト名</p></dd>
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>LIST_TYPE</code></a></dt><dd><p>作成するリストの種類</p>
    <p>サポートされる種類:</p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
    </ul>
    <p>デフォルトは <code>entity</code></p>
    </dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--pretty"><a href="#banshee-list-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-lookup--help"><a href="#banshee-list-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list info

リストの名前、種類、タイムスタンプ、オーナーの詳細などの情報を取得します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list info [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>情報を取得するリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list search

リストを検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list search [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--name"><a href="#banshee-list-search--name"><code>NAME</code></a></dt><dd>
    <p>検索するリスト名</p>
    <p>名前を指定しない場合はすべてのリストを返します</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--list-type"><a href="#banshee-list-search--list-type"><code>--list-type</code>, <code>-t</code></a> <i>list-type</i></dt><dd>
    <p>リストの種類でフィルタリングします</p>
    <p>サポートされる種類:</p>
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
    <p>結果件数を制限します</p>
    <p>最大件数は 3,000 件です</p>
    <p>デフォルトは 1,000 件です</p><dd></dd>
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list status

リストのステータスとエンティティ数を取得します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list status [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>ステータスを取得するリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list entities

リスト上のエンティティを取得します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list entities [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>エンティティを取得するリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>


### banshee list entries

リスト上のテキストエントリを取得します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee list entries [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>テキストエントリを取得するリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>



### banshee list clear

リストを完全にクリアし、すべてのエンティティを削除します。このコマンドはテキストエントリをクリアしないため、テキストエントリのクリアはサポートされていません。

<h3 class="commands-reference">Usage</h3>

```
banshee list clear [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>クリアするリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list add

リストにエンティティを追加します。

<h3 class="commands-reference">Usage</h3>

```
banshee list add [OPTIONS] LIST_ID ENTITY_ID [PROPERTIES]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--list-id"><a href="#banshee-list-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>追加先のリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
    <dt id="banshee-list-add--entity-id"><a href="#banshee-list-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>リストに追加するエンティティ ID または名前と種類の組み合わせ。例:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul></dd>
    <dt id="banshee-list-add--properties"><a href="#banshee-list-add--properties"><code>PROPERTIES</code></a></dt><dd>
    <p>省略可能。<code>annotation=&lt;text&gt;</code> を使用して、Recorded Future プラットフォーム上のこのエンティティに表示されるメモを添付します。</p>
    <p>値にスペースが含まれる場合は引用符で囲んでください。</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--help"><a href="#banshee-list-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
</code></pre>

### banshee list bulk-add

リストに複数のエンティティを追加します。

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-add [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--list-id"><a href="#banshee-list-bulk-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>追加先のリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
    <dt id="banshee-list-bulk-add--entity-input"><a href="#banshee-list-bulk-add--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>スペースまたは改行区切りで指定する 1 つ以上のエンティティ。例:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>このコマンドは標準入力からの入力も受け付けます。'entities.txt' が改行区切りのエンティティファイルだとすると、例えば以下のようになります:</p>
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
    <p>上記を踏まえて、以下のいずれかのコマンドでエンティティを一括追加できます:</p>
    <pre><code>
    $ banshee list bulk-add LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-add LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--overwrite"><a href="#banshee-list-bulk-add--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>上書きモードを有効にします。このオプションを指定すると、コマンドは以下の動作をします:</p>
    <ul>
        <li>指定したファイルに含まれる、現在リストにあるすべてのエンティティを保持する</li>
        <li>指定したファイルに含まれる、まだリストにない新しいエンティティを追加する</li>
        <li>指定したファイルに<strong>含まれない</strong>、現在リストにあるエンティティを削除する</li>
    </ul>
    <p>デフォルト（このフラグなし）では、既存のリストに新しいエンティティを追記するだけで、何も削除しません。</p>
    </dd>
    <dt id="banshee-list-bulk-add--help"><a href="#banshee-list-bulk-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Result Status Output</h3>

<p><code>banshee list bulk-add</code> は出力をステータス別にグループ化し、そのステータスに該当する入力エンティティをそれぞれ表示します。例:</p>

<pre><code class="language-text">
ADDED:
SoA6SP

ERROR_MULTIPLE_MATCHES:
wanna:malware
</code></pre>

<p>主なステータス:</p>
<ul>
    <li><code>ADDED</code> - エンティティがリストに正常に追加されました。</li>
    <li><code>UNCHANGED</code> - エンティティはすでにリストに存在していました（変更なし）。</li>
    <li><code>UPDATED</code> - エンティティが存在し、API によって更新されました。</li>
    <li><code>ERROR_BAD_ID</code> - 入力形式またはエンティティ参照が無効です。</li>
    <li><code>ERROR_NOT_FOUND</code> - 一致するエンティティが見つかりませんでした。</li>
    <li><code>ERROR_NOT_ALLOWED</code> - 指定したリストではそのエンティティ種類は許可されていません。</li>
    <li><code>ERROR_MULTIPLE_MATCHES</code> - 入力が複数の候補エンティティに一致しました。<strong>エンティティは追加されませんでした。</strong></li>
    <li><code>LIST_MAX_SIZE_REACHED</code> - 指定したリストが満杯のため、これ以上エンティティを追加できません。</li>
</ul>

<h3 class="commands-reference"><code>ERROR_MULTIPLE_MATCHES</code> の解決方法</h3>

<p><code>ERROR_MULTIPLE_MATCHES</code> が表示される場合、指定したエンティティ名が曖昧です。API が単一の正確なエンティティを特定できなかったため、その行はスキップされ追加されません。</p>

<p>推奨のワークフロー:</p>
<ol>
    <li>コマンド出力から曖昧な値を確認します。</li>
    <li><code>banshee entity search</code> を実行して、目的の正確なエンティティを特定します。必要に応じて検索語の表記（スペル、スペース、より具体的な表現など）を調整して結果を絞り込みます。</li>
    <li>入力ファイル内の曖昧な値を正確なエンティティ ID に置き換えます。</li>
    <li>修正したファイルで <code>banshee list bulk-add</code> を再実行します。</li>
</ol>

<p>例:</p>
<pre><code class="language-bash">
banshee entity search wannacry --type Malware
banshee list bulk-add LIST_ID &lt; entities.txt
</code></pre>

<p>ヒント: エンティティ ID（例: <code>SoA6SP</code>）がすでにわかっている場合は、曖昧さを避けるために一括ファイルで名前/種類の組み合わせよりも ID を優先してください。</p>

### banshee list remove

リストからエンティティを削除します。

<h3 class="commands-reference">Usage</h3>

```
banshee list remove [OPTIONS] LIST_ID ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--list-id"><a href="#banshee-list-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>削除元のリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
    <dt id="banshee-list-remove--entity-id"><a href="#banshee-list-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>リストから削除するエンティティ ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--help"><a href="#banshee-list-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list bulk-remove

リストから複数のエンティティを削除します。

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-remove [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--list-id"><a href="#banshee-list-bulk-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>削除元のリスト ID</p>
    <p>リスト ID は '<strong>report:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
    <dt id="banshee-list-bulk-remove--entity-input"><a href="#banshee-list-bulk-remove--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>スペースまたは改行区切りで指定する 1 つ以上のエンティティ。例:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>このコマンドは標準入力からの入力も受け付けます。'entities.txt' が改行区切りのエンティティファイルだとすると、例えば以下のようになります:</p>
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
    <p>上記を踏まえて、以下のいずれかのコマンドでエンティティを一括削除できます:</p>
    <pre><code>
    $ banshee list bulk-remove LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-remove LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--help"><a href="#banshee-list-bulk-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee list copy

あるリストから別のリストにエンティティをコピーするユーティリティコマンドです。

コピー元リストのエンティティが読み込まれ、コピー先リストに追加されます。デフォルトでは、コピー先に既存の内容はそのままに新しいエンティティが追記されます。`--overwrite` を指定すると、コピー先がコピー元を反映した状態になります。すなわち、両方に存在するエンティティは保持され、新しいエンティティは追加され、コピー元に**存在しない**コピー先のエンティティは削除されます。

コピー元リストが空の場合、`--overwrite` を指定していても、コマンドはコピー先を変更せずに終了します。

<h3 class="commands-reference">Usage</h3>

```
banshee list copy [OPTIONS] SOURCE_LIST_ID DESTINATION_LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--source-list-id"><a href="#banshee-list-copy--source-list-id"><code>SOURCE_LIST_ID</code></a></dt><dd>
    <p>エンティティのコピー元リスト ID</p></dd>
    <dt id="banshee-list-copy--destination-list-id"><a href="#banshee-list-copy--destination-list-id"><code>DESTINATION_LIST_ID</code></a></dt><dd>
    <p>エンティティのコピー先リスト ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--overwrite"><a href="#banshee-list-copy--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>上書きモード: コピー先リストにすでに存在するエンティティは保持し、新しいエンティティを追加し、コピー元リストにないコピー先のエンティティを削除します。デフォルトでは、既存のエンティティを削除せずに新しいエンティティを追記します。</p></dd>
    <dt id="banshee-list-copy--help"><a href="#banshee-list-copy--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Examples</h3>

```
$ banshee list copy 1b0s1q 21YKUC
$ banshee list copy 1b0s1q 21YKUC --overwrite
```

## banshee pba

Recorded Future Playbook Alerts の検索、参照、更新を行います。

<h3 class="commands-reference">Usage</h3>

```
banshee pba [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pba-lookup"><code>banshee pba lookup</code></a></dt><dd><p>Playbook Alert を参照する</p></dd>
    <dt><a href="#banshee-pba-search"><code>banshee pba search</code></a></dt><dd><p>Playbook Alerts を検索する</p></dd>
    <dt><a href="#banshee-pba-update"><code>banshee pba update</code></a></dt><dd><p>1 件以上の Playbook Alert を更新する</p></dd>
    <dt><a href="#banshee-pba-export"><code>banshee pba export</code></a></dt><dd><p>Playbook Alerts を JSON または CSV 形式でエクスポートする</p></dd>
</dl>

### banshee pba lookup

Playbook Alert を参照します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee pba lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--alert-id"><a href="#banshee-pba-lookup--alert-id"<code>ALERT_ID</code></a></dt><dd><p>参照するアラート ID</p>
    <p>アラート ID は '<strong>task:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--pretty"><a href="#banshee-pba-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-pba-lookup--help"><a href="#banshee-pba-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee pba search

Playbook Alerts を検索します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee pba search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-search--created"><a href="#banshee-pba-search--created"><code>--created</code>, <code>-C</code></a> <i>created-from</i></dt><dd>
    <p>作成日時でフィルタリングします（例: 1d、12h）</p><dd></dd>
    <dt id="banshee-pba-search--updated"><a href="#banshee-pba-search--updated"><code>--updated</code>, <code>-u</code></a> <i>updated-from</i></dt><dd>
    <p>更新日時でフィルタリングします（例: 1d、12h）</p><dd></dd>
    <dt id="banshee-pba-search--category"><a href="#banshee-pba-search--category"><code>--category</code>, <code>-c</code></a> <i>category</i></dt><dd>
    <p>アラートカテゴリでフィルタリングします（繰り返し指定可）</p>
    <p>サポートされているカテゴリ:</p>
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
    <p>アラート優先度でフィルタリングします（繰り返し指定可）</p>
    <p>指定可能な値: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p>
    <p>デフォルトはすべての優先度です</p><dd></dd>
    <dt id="banshee-pba-search--status"><a href="#banshee-pba-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>アラートステータスでフィルタリングします（繰り返し指定可）</p>
    <p>指定可能な値: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p>
    <p>デフォルトはすべてのステータスです</p><dd></dd>
    <dt id="banshee-pba-search--entity"><a href="#banshee-pba-search--entity"><code>--entity</code></a>,  <code>-e</code> <i>entity</i></dt><dd>
    <p>関連エンティティでアラートをフィルタリングします（繰り返し指定可）。例: <code>-e idn:recordedfuture.com -e idn:example.com</code></p><dd></dd>
    <dt id="banshee-pba-search--org-id"><a href="#banshee-pba-search--org-id"><code>--org-id</code></a>,  <code>-o</code> <i>organisation-id</i></dt><dd>
    <p>所有組織 ID でアラートをフィルタリングします（繰り返し指定可）</p>
    <p>10 文字の ID または 16 文字の <code>uhash:</code> 形式を受け付けます。例: <code>-o 69sKLfTGsS -o uhash:5zQaSyRpA1</code></p><dd></dd>
    <dt id="banshee-pba-search--limit"><a href="#banshee-pba-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>結果の件数を制限します</p>
    <p>最大件数は 10,000 件です</p>
    <p>デフォルトは 100 件です</p><dd></dd>
    <dt id="banshee-pba-search--pretty"><a href="#banshee-pba-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-pba-search--help"><a href="#banshee-pba-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

### banshee pba update

1 件以上の Playbook Alert を更新します。

<h3 class="commands-reference">Usage</h3>

```
banshee pba update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--alert-id"><a href="#banshee-pba-update--alert-id"<code>ALERT_IDS</code></a></dt><dd>
    <p>スペース区切りで指定する 1 件以上のアラート ID</p>
    <p>アラート ID は '<strong>task:</strong>' プレフィックスあり・なし両方で指定できます</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--status"><a href="#banshee-pba-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>アラートをこのステータスに更新します</p>
    <p>指定可能な値: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-pba-update--reopen"><a href="#banshee-pba-update--reopen"><code>--reopen</code></a>,  <code>-r</code> <i>reopen</i></dt><dd>
    <p>再オープン戦略はステータスが Dismissed または Resolved のアラートにのみ適用できます。使用可能なステータスと再オープンの組み合わせは次のとおりです: <code>Dismissed -> Never</code>; <code>Resolved -> Never</code>; <code>Resolved -> SignificantUpdates</code></p>
    <p>サポートされている値: <code>Never</code>, <code>SignificantUpdates</code></p><dd></dd>
    <dt id="banshee-pba-update--priority"><a href="#banshee-pba-update--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>新しいアラート優先度を設定します</p>
    <p>指定可能な値: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p><dd></dd>
    <dt id="banshee-pba-update--comment"><a href="#banshee-pba-update--comment"><code>--comment</code></a>,  <code>-t</code> <i>comment</i></dt><dd>
    <p>アラートに追加するコメント。例: "Bulk resolved via banshee"</p><dd></dd>
    <dt id="banshee-pba-update--assignee"><a href="#banshee-pba-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>アラートを割り当てる新しいユーザー。ユーザーの uhash を指定します。例: uhash:3aXZxdkM12</p><dd></dd>
    <dt id="banshee-pba-update--help"><a href="#banshee-pba-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>1 件以上のアラート ID（スペース区切り）を指定し、必要な更新オプションを設定します:</p>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Dismissed
banshee pba update ALERT_ID -s InProgress -p High -t "Escalated due to new findings"
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved -a uhash:3aXZxdkM12
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. 引数として直接指定する（1 件または複数件）:</h4>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved
</code></pre>

<h4>2. ファイルまたは標準入力から読み込む:</h4>

<p>アラート ID を 1 行ずつ記載したファイル（例: <code>alerts.txt</code>）がある場合:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>以下のコマンドで、一覧に含まれる全アラートを更新できます:</p>

<pre><code class="language-bash">
banshee pba update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee pba update -s Dismissed
</code></pre>

<h4>3. 検索コマンドからパイプで渡す:</h4>

<p><code>jq</code> などのツールを使って検索結果からアラート ID を抽出し、update コマンドにパイプで渡します:</p>

<pre><code class="language-bash">
banshee pba search | jq -r '.data[].playbook_alert_id' | banshee pba update -p High -t "Investigation started"
</code></pre>

<h3 class="commands-reference">Additional Usage Examples</h3>

<pre><code class="language-bash">
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved
banshee pba update ALERT_ID -s Resolved -r Never
banshee pba update ALERT_ID_1 ALERT_ID_2 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
banshee pba update ALERT_ID -a
</code></pre>

### banshee pba export

Playbook Alerts を JSON または CSV 形式でエクスポートします。標準入力からアラート ID とカテゴリを読み込みます。通常は [`banshee pba search`](#banshee-pba-search) からパイプで渡します。

<h3 class="commands-reference">Output Formats</h3>

<p><b>JSON（デフォルト）</b> — 各 ID に対して Recorded Future API が返す<i>完全な</i>アラートオブジェクトを出力します。トップレベルのフィールドすべてに加え、パネルステータス、ターゲット、エビデンス、担当者、タイムスタンプなどのネストされたデータも含みます。ダウンストリームのツール連携、<code>jq</code> パイプライン、再取り込みに最適です。</p>

<p><b>CSV（<a href="#banshee-pba-export--csv"><code>--csv</code></a>）</b> — スプレッドシートやレポート作成向けの概要サマリーを出力します。以下に示す 12 列のみを書き込みます（先頭にヘッダー行あり）。JSON レスポンスに含まれるその他のフィールドはすべて省略されます。</p>

| Field | Description |
|---|---|
| `ID` | Playbook Alert ID（`task:` プレフィックスを含む） |
| `Priority` | アラート優先度（例: `Informational`, `Moderate`, `High`） |
| `Alert Rule` | トリガーしたアラートルール名（ルールラベルにフォールバック） |
| `Status` | アラートステータス（例: `New`, `InProgress`, `Dismissed`, `Resolved`） |
| `Created` | 作成タイムスタンプ（UTC、`%Y-%m-%d %H:%M:%S`） |
| `Updated` | 最終更新タイムスタンプ（UTC、`%Y-%m-%d %H:%M:%S`） |
| `Subject` | アラートの件名 |
| `Assignee` | 割り当てられたユーザーの表示名 |
| `Assessments` | アラートのリスク評価/ルール（カテゴリ依存）、`;` 区切り |
| `Entities` | 重複を除いたターゲットエンティティ名、`;` 区切り |
| `Reopen Strategy` | クローズされたアラートの再オープン戦略（例: `Never`, `SignificantUpdates`） |
| `Onwards Actions` | アラートに対して行われたアクション、`;` 区切り |

<h3 class="commands-reference">Usage</h3>

```
banshee pba search [SEARCH_OPTIONS] | banshee pba export [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-export--csv"><a href="#banshee-pba-export--csv"><code>--csv</code></a></dt><dd>
    <p>上記の固定列セットで CSV として出力します。このフラグを指定しない場合、コマンドは JSON を出力します。</p><dd></dd>
    <dt id="banshee-pba-export--help"><a href="#banshee-pba-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Piped Input</h3>

<p><code>banshee pba export</code> はパイプ入力のみを受け付けます。<a href="#banshee-pba-search"><code>banshee pba search</code></a> が生成する JSON オブジェクトを受け取り、各アラートの <code>playbook_alert_id</code> と <code>category</code> を抽出して、すべてのアラートの完全なデータを取得します。パイプなしでコマンドを実行するとエラーになります。</p>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee pba search --created 1d | banshee pba export
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export > identity_alerts.json
banshee pba search --created 1d --category domain_abuse | banshee pba export --csv > domain_alerts.csv
</code></pre>


## banshee pcap

パケットキャプチャ（pcap）を Recorded Future インテリジェンスでエンリッチします。

<h3 class="commands-reference">Usage</h3>

```
banshee pcap [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pcap-enrich"><code>banshee pcap enrich</code></a></dt><dd><p>パケットキャプチャ（pcap）ファイルを Recorded Future インテリジェンスでエンリッチする</p></dd>
</dl>

### banshee pcap enrich

このコマンドは pcap ファイルを解析して IP アドレスやドメインなどのネットワークインジケーターを抽出し、脅威インテリジェンスデータでエンリッチします。デフォルトでは、リスクスコアのしきい値を満たすインジケーターのみが表示されるようにフィルタリングされます。`--threat-hunt` を使用すると、リスクスコアのしきい値を下回っていても、脅威アクターに関連するインジケーターを含めることができます。
<br>リスクスコアのしきい値を下げたり、脅威ハンティングを有効にしたりすると、結果の件数と処理時間の両方が大幅に増加する可能性があることに注意してください。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">JSON Output</h3>

JSON 配列内の各結果オブジェクトには、以下のフィールドが含まれます。

| Field | Description |
|---|---|
| `ioc` | pcap から抽出されたネットワークインジケーター（IP アドレスまたはドメイン名） |
| `risk_score` | Recorded Future のリスクスコア |
| `most_malicious_rule` | リスクスコアに寄与した最も深刻度の高いリスクルールの名前 |
| `rule_evidence` | 個別のリスクルールエビデンスの詳細の配列（深刻度の高い順にソート済み） |
| `ta_names` | この IOC に関連する脅威アクター名のリスト。不明な場合は空 |
| `malwares` | この IOC に関連するマルウェアファミリー名のリスト。不明な場合は空 |
| `wireshark_query` | この IOC のトラフィックを分離するために Wireshark にそのまま貼り付けられる表示フィルター |

`rule_evidence` 配列内の各オブジェクトには以下が含まれます。

| Field | Description |
|---|---|
| `count` | このリスクルールへの参照を提供したソースの数 |
| `description` | エビデンスの人間が読みやすい概要 |
| `level` | このルールの深刻度レベル — 整数が大きいほど深刻 |
| `mitigation` | IOC が掲載されている可能性のあるホワイトリストに関する説明（関連するリスクを軽減または緩和するもの） |
| `rule` | 発動した特定の Recorded Future リスクルールの名前 |
| `sightings` | 記録された個別のサイティング数 |
| `timestamp` | このルールの最新サイティングの ISO 8601 タイムスタンプ |
| `type` | タイプ識別子 |

<h3 class="commands-reference">Usage</h3>


```
banshee pcap enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--file-path"><a href="#banshee-pcap-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>エンリッチする pcap ファイルへのパス</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--risk-score"><a href="#banshee-pcap-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>このしきい値を超えるリスクスコア（1〜99）を持つインジケーターのみを表示するようにフィルタリングします<p>デフォルト値は 65</p></p></dd>
    <dt id="banshee-pcap-enrich--threat-hunt"><a href="#banshee-pcap-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>リスクスコアのしきい値に関わらず、脅威アクターに関連するインジケーターを含めます（遡及的脅威ハンティング）</p></dd>
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p><dd></dd>
    <dt id="banshee-pcap-enrich--help"><a href="#banshee-pcap-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

## banshee risklist

リスクリストを管理します。

<h3 class="commands-reference">Usage</h3>

```
banshee risklist [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-risklist-create"><code>banshee risklist create</code></a></dt><dd><p>1 つ以上のリスクルールを組み合わせてカスタムリスクリストを作成する</p></dd>
    <dt><a href="#banshee-risklist-fetch"><code>banshee risklist fetch</code></a></dt><dd><p>リスクリストをダウンロードする</p></dd>
    <dt><a href="#banshee-risklist-stat"><code>banshee risklist stat</code></a></dt><dd><p>リスクリストのメタデータ（etag およびタイムスタンプ）を表示する</p></dd>
</dl>

### banshee risklist create

1 つ以上の Recorded Future リスクルールを組み合わせて、重複を除去した単一のカスタムリスクリストファイルを作成します。

各 `--risk-rule` ごとにエントリが取得され、IOC 単位でマージされます（最初に出現したものが優先）。オプションで最小 `--risk-score` によるフィルタリングも可能です。出力はリスクスコアの降順にソートされ、指定したフォーマットで書き出されます。ファイアウォール、SIEM、その他のインテグレーションにそのまま利用できます。

デフォルトではローカルファイルに出力されます。`--fusion` を `--output-path` と組み合わせて使用すると、ローカルファイルを作成せずに結果を直接 Recorded Future Fusion にアップロードできます。

<h3 class="commands-reference">Usage</h3>

```
banshee risklist create [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-create--entity-type"><a href="#banshee-risklist-create--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>リスクリストのエンティティタイプ。有効な値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><strong>必須</strong></p></dd>
    <dt id="banshee-risklist-create--risk-rule"><a href="#banshee-risklist-create--risk-rule"><code>--risk-rule</code></a>, <code>-R</code> <i>risk-rule</i></dt><dd>
    <p>含めるリスクルール。<code>default</code>、<code>large</code>、または <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> に表示されるルール名を使用します。繰り返し指定可能 — 複数回指定することで複数のルールを 1 つの出力にマージできます。<br><strong>必須（少なくとも 1 つ）</strong></p></dd>
    <dt id="banshee-risklist-create--risk-score"><a href="#banshee-risklist-create--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>最低リスクスコアのしきい値（5〜99）。この値を下回るリスクスコアのエントリは出力から除外されます</p></dd>
    <dt id="banshee-risklist-create--format"><a href="#banshee-risklist-create--format"><code>--format</code></a>, <code>-f</code> <i>format</i></dt><dd>
    <p>出力フォーマット。デフォルトは <code>csv</code></p>
    <ul>
        <li><code>csv</code> — ヘッダー付きカンマ区切り形式: <code>Name</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code>。hash エンティティタイプには追加の <code>Algorithm</code> 列が含まれます: <code>Name</code>, <code>Algorithm</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code></li>
        <li><code>edl</code> — IOC の値を 1 行ずつ記載したプレーンリスト（ファイアウォールの EDL フィードに適しています）。<code>.txt</code> 拡張子で書き出されます</li>
        <li><code>json</code> — リスクリストエントリの完全な JSON 配列</li>
    </ul></dd>
    <dt id="banshee-risklist-create--output-path"><a href="#banshee-risklist-create--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>出力ファイルパス。ファイルパスまたはディレクトリを指定できます（ファイル名は <code>custom_risklist_{entity_type}.{ext}</code> として自動生成されます）。デフォルトは現在のディレクトリで、ファイル名は自動生成されます。<br><code>--fusion</code> を使用する場合は必須</p></dd>
    <dt id="banshee-risklist-create--fusion"><a href="#banshee-risklist-create--fusion"><code>--fusion</code></a>, <code>-F</code></dt><dd>
    <p><code>--output-path</code> を宛先パスとして使用し、結果を直接 Recorded Future Fusion にアップロードします。このフラグを設定するとローカルファイルは作成されません</p></dd>
    <dt id="banshee-risklist-create--help"><a href="#banshee-risklist-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

デフォルトルールから IP の CSV リスクリストを作成し、リスクスコア 70 以上でフィルタリングする

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
```

2 つのドメインルールを重複除去して 1 つの CSV にマージし、リスクスコア 80 以上でフィルタリングする

```bash
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
```

2 つの IP ルールをマージして EDL（プレーン IOC リスト）として出力する

```bash
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
```

2 つのルールからハッシュの JSON リスクリストを作成し、特定のローカルファイルパスに出力する

```bash
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
```

リスクリストを作成して直接 Recorded Future Fusion にアップロードする

```bash
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

### banshee risklist fetch

特定のエンティティタイプとリスト名のリスクリストをダウンロードするか、カスタムリスクリストファイルを使用します。

エンティティタイプ（`--entity-type`）とリスト名（`--list-name`）を指定することで、Recorded Future からリスクリストをダウンロードできます。利用可能なリスト名は `default`、`large`、または `banshee ioc rules` に表示されるルール名です。Recorded Future リスクルールの詳細については、[Risk Scoring in Recorded Future](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future) サポート記事を参照してください。

または、`--custom-list-path` を使用してカスタムリスクリストファイルのパスを指定することもできます。

<h3 class="commands-reference">Usage</h3>

```
banshee risklist fetch [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-fetch--entity-type"><a href="#banshee-risklist-fetch--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>リスクリストのエンティティタイプ。有効な値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><code>--list-name</code> を使用する場合は必須</p></dd>
    <dt id="banshee-risklist-fetch--list-name"><a href="#banshee-risklist-fetch--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>リスクリスト名: <code>default</code>、<code>large</code>、または <code>banshee ioc rules</code> のルール名<br><code>--entity-type</code> を使用する場合は必須</p></dd>
    <dt id="banshee-risklist-fetch--custom-list-path"><a href="#banshee-risklist-fetch--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>カスタムリスクリストファイルのパス。<code>--entity-type</code> または <code>--list-name</code> と同時には使用できません</p></dd>
    <dt id="banshee-risklist-fetch--output-path"><a href="#banshee-risklist-fetch--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>出力ファイルパス。デフォルトは現在のディレクトリで、ファイル名は自動生成されます</p></dd>
    <dt id="banshee-risklist-fetch--as-json"><a href="#banshee-risklist-fetch--as-json"><code>--as-json</code></a>, <code>-j</code></dt><dd>
    <p>リスクリストを JSON フォーマットに変換します。<code>--list-name</code> と <code>--entity-type</code> を使用する場合にのみ利用できます</p></dd>
    <dt id="banshee-risklist-fetch--help"><a href="#banshee-risklist-fetch--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# Download the default risk list for IP addresses
banshee risklist fetch -e ip -l default

# Download the large risk list for domains as JSON
banshee risklist fetch -e domain -l large -j

# Download a risk list for hashes that are involved in an Insikt Group Note
banshee risklist fetch -e hash -l analystNote

# Download a custom risk list file
banshee risklist fetch -c /path/to/custom_risklist.csv

# Download the default risklist for URLs and save to a specific output path
banshee risklist fetch -e url -l default -o /tmp/rf_default_url_risklist.csv
</code></pre>

### banshee risklist stat

etag およびタイムスタンプ情報を含むリスクリストのメタデータを表示します。

このコマンドは、リストの全コンテンツをダウンロードせずにリスクリストのメタデータを取得します。リスクリストが最後に更新された日時を確認するために使用できます。

<h3 class="commands-reference">Usage</h3>

```
banshee risklist stat [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-stat--entity-type"><a href="#banshee-risklist-stat--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>リスクリストのエンティティタイプ。有効な値: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><code>--list-name</code> を使用する場合は必須</p></dd>
    <dt id="banshee-risklist-stat--list-name"><a href="#banshee-risklist-stat--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>リスクリスト名: <code>default</code>、<code>large</code>、または <code>banshee ioc rules</code> のルール名<br><code>--entity-type</code> を使用する場合は必須</p></dd>
    <dt id="banshee-risklist-stat--custom-list-path"><a href="#banshee-risklist-stat--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>カスタムリスクリストファイルのパス。<code>--entity-type</code> または <code>--list-name</code> と同時には使用できません</p></dd>
    <dt id="banshee-risklist-stat--pretty"><a href="#banshee-risklist-stat--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-risklist-stat--count"><a href="#banshee-risklist-stat--count"><code>--count</code></a>, <code>-C</code></dt><dd>
    <p>リスクリスト全体の IOC 数とリスクスコア分布を表示する</p></dd>
    <dt id="banshee-risklist-stat--help"><a href="#banshee-risklist-stat--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# Check metadata for the default IP risk list
banshee risklist stat -e ip -l default

# Check metadata with pretty formatting
banshee risklist stat -e domain -l large -p

# Check metadata for a custom risk list file
banshee risklist stat -c /path/to/custom_risklist.txt

# Count indicators per risk score in the default IP risk list and pretty print
banshee risklist stat -e ip -l default -Cp
</code></pre>

## banshee rules

検知ルールを検索してダウンロードします。

<h3 class="commands-reference">Usage</h3>

```
banshee rules [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-rules-search"><code>banshee rules search</code></a></dt><dd><p>フィルターオプションに基づいて検知ルールを検索する</p></dd>
</dl>

### banshee rules search

指定されたフィルターオプションに基づいて検知ルールを検索します。結果はコンソールに表示するか、個別のルールファイルとしてディスクに保存できます。

検知ルールは、タイプ（YARA、Snort、Sigma）、関連エンティティ（脅威アクター、マルウェア、MITRE ATT&CK テクニック）、作成・更新日などでフィルタリングできます。`--threat-actor-map` または `--threat-malware-map` を使用すると、Threat Map 内のエンティティに基づいてルールを自動的にフィルタリングできます。

出力が過剰にならないよう、デフォルトでは結果は 10 件に制限されています。最大 1000 件のルールを取得するには `--limit` オプションを使用してください。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee rules search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-rules-search--type"><a href="#banshee-rules-search--type"><code>--type</code></a>, <code>-t</code> <i>type</i></dt><dd>
    <p>ルールタイプでフィルタリングします。有効な値: <code>yara</code>, <code>snort</code>, <code>sigma</code><br>複数のタイプを指定でき、論理 OR として機能します（例: <code>-t yara -t snort</code> はどちらかのタイプに一致するルールを返します）</p></dd>
    <dt id="banshee-rules-search--threat-actor-map"><a href="#banshee-rules-search--threat-actor-map"><code>--threat-actor-map</code></a>, <code>-T</code></dt><dd>
    <p>Threat Actor Map 内の脅威アクターでルールをフィルタリングします。有効にすると、Threat Actor Map 内のアクターに関連する検知ルールが返されます</p></dd>
    <dt id="banshee-rules-search--threat-actor-category"><a href="#banshee-rules-search--threat-actor-category"><code>--threat-actor-category</code></a>, <code>-C</code> <i>category</i></dt><dd>
    <p>Threat Actor Map 内の脅威アクターカテゴリでフィルタリングします。複数のカテゴリを指定でき、論理 OR として機能します（例: <code>-C nation_state_sponsored -C ransomware_and_extortion_groups</code>）</p></dd>
    <dt id="banshee-rules-search--threat-malware-map"><a href="#banshee-rules-search--threat-malware-map"><code>--threat-malware-map</code></a>, <code>-M</code></dt><dd>
    <p>Malware Threat Map 内のマルウェアでルールをフィルタリングします。有効にすると、Malware Threat Map 内のマルウェアに関連する検知ルールが返されます</p></dd>
    <dt id="banshee-rules-search--org-id"><a href="#banshee-rules-search--org-id"><code>--org-id</code></a>, <code>-O</code> <i>org-id</i></dt><dd>
    <p>Threat Maps から脅威アクターを取得する際の組織 ID を指定します（<code>--threat-actor-map</code> または <code>--threat-malware-map</code> が必要）。<code>uhash:</code> プレフィックスの有無にかかわらず値を受け付けます。MSSP およびマルチ組織アカウントに便利です</p></dd>
    <dt id="banshee-rules-search--entity"><a href="#banshee-rules-search--entity"><code>--entity</code></a>, <code>-e</code> <i>entity</i></dt><dd>
    <p>検知ルールに関連する Recorded Future エンティティ ID でフィルタリングします。複数のエンティティを指定でき、論理 OR として機能します。エンティティ ID の検索には <code>banshee entity search</code> を使用してください（例: IsaacWiper マルウェアの場合は <code>lzQ5GL</code>、データ暗号化（影響）の場合は <code>mitre:T1486</code>）</p></dd>
    <dt id="banshee-rules-search--created-after"><a href="#banshee-rules-search--created-after"><code>--created-after</code></a>, <code>-a</code> <i>time</i></dt><dd>
    <p>指定した時刻以降に作成された検知ルールでフィルタリングします。相対時間（例: <code>1d</code>, <code>3d</code>, <code>7d</code>）または絶対日付（例: <code>2024-01-01</code>）を受け付けます</p></dd>
    <dt id="banshee-rules-search--created-before"><a href="#banshee-rules-search--created-before"><code>--created-before</code></a>, <code>-b</code> <i>time</i></dt><dd>
    <p>指定した時刻以前に作成された検知ルールでフィルタリングします。相対時間（例: <code>1d</code>, <code>3d</code>, <code>7d</code>）または絶対日付（例: <code>2024-01-01</code>）を受け付けます</p></dd>
    <dt id="banshee-rules-search--updated-after"><a href="#banshee-rules-search--updated-after"><code>--updated-after</code></a>, <code>-u</code> <i>time</i></dt><dd>
    <p>指定した時刻以降に更新された検知ルールでフィルタリングします。相対時間（例: <code>1d</code>, <code>3d</code>, <code>7d</code>）または絶対日付（例: <code>2024-01-01</code>）を受け付けます</p></dd>
    <dt id="banshee-rules-search--updated-before"><a href="#banshee-rules-search--updated-before"><code>--updated-before</code></a>, <code>-U</code> <i>time</i></dt><dd>
    <p>指定した時刻以前に更新された検知ルールでフィルタリングします。相対時間（例: <code>1d</code>, <code>3d</code>, <code>7d</code>）または絶対日付（例: <code>2024-01-01</code>）を受け付けます</p></dd>
    <dt id="banshee-rules-search--id"><a href="#banshee-rules-search--id"><code>--id</code></a>, <code>-i</code> <i>document-id</i></dt><dd>
    <p>検知ルールに関連する特定の Insikt Note ドキュメント ID でフィルタリングします（例: <code>doc:lmRPGB</code>）</p></dd>
    <dt id="banshee-rules-search--title"><a href="#banshee-rules-search--title"><code>--title</code></a>, <code>-n</code> <i>title</i></dt><dd>
    <p>関連する Insikt Note のタイトルで検知ルールをフリーテキスト検索します</p></dd>
    <dt id="banshee-rules-search--limit"><a href="#banshee-rules-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>返す検知ルールの最大件数<p>デフォルトは 10</p></p></dd>
    <dt id="banshee-rules-search--output-path"><a href="#banshee-rules-search--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>検知ルールを指定したディレクトリに保存します。相対パスまたは絶対パスを指定できます。指定しない場合、結果はコンソールに出力されます</p></dd>
    <dt id="banshee-rules-search--pretty"><a href="#banshee-rules-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-rules-search--help"><a href="#banshee-rules-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# Search for YARA rules created in the last 7 days
banshee rules search -t yara -a 7d

# Search for rules associated with threat actors in your Threat Map and pretty print results
# Since --limit defaults to 10, this will return the first 10 matching rules
banshee rules search -Tp

# Combine threat actor and malware maps 
banshee rules search -TMp

# Search for rules by specific entity IDs (e.g., IsaacWiper malware)
banshee rules search -e lzQ5GL -p

# Search for Snort and Sigma rules updated in the last 3 days, save to directory
banshee rules search -t snort -t sigma -u 3d -o ./detection_rules

# Search by Insikt Note title
banshee rules search --title "APT28" -p
</code></pre>

## banshee sandbox

サンドボックスの提出分析とプロファイル管理を行います。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-stats"><code>banshee sandbox stats</code></a></dt><dd><p>設定可能なウィンドウ期間でサンドボックス提出を集計し、SOC モーニングブリーフを出力する</p></dd>
    <dt><a href="#banshee-sandbox-list"><code>banshee sandbox list</code></a></dt><dd><p>サンドボックスサンプルを一覧表示する</p></dd>
    <dt><a href="#banshee-sandbox-search"><code>banshee sandbox search</code></a></dt><dd><p>ハッシュ、ファミリー、タグ、ボットネット、ウォレット、ネットワークインジケーター、または生の Triage クエリでサンプルを検索する</p></dd>
    <dt><a href="#banshee-sandbox-get"><code>banshee sandbox get</code></a></dt><dd><p>ID で単一のサンドボックスサンプルの概要を取得する</p></dd>
    <dt><a href="#banshee-sandbox-download"><code>banshee sandbox download</code></a></dt><dd><p>1 件以上のサンプル ID の元の提出バイト列をダウンロードする（AES 暗号化 ZIP アーカイブにラップされます）</p></dd>
    <dt><a href="#banshee-sandbox-delete"><code>banshee sandbox delete</code></a></dt><dd><p>ID でサンドボックスサンプルを削除する</p></dd>
    <dt><a href="#banshee-sandbox-submit"><code>banshee sandbox submit</code></a></dt><dd><p>ファイル、URL、または公開サンプルをサンドボックス解析に提出する</p></dd>
    <dt><a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a></dt><dd><p>静的解析で一時停止しているサンプルに解析プロファイルを割り当てる</p></dd>
    <dt><a href="#banshee-sandbox-profile"><code>banshee sandbox profile</code></a></dt><dd><p>解析プロファイルを管理する</p></dd>
    <dt><a href="#banshee-sandbox-report"><code>banshee sandbox report</code></a></dt><dd><p>サンプル解析レポート</p></dd>
</dl>

### banshee sandbox stats

設定可能なウィンドウ期間でサンドボックス提出を集計し、SOC シフト引き継ぎや日次トリアージに適した「モーニングブリーフ」を出力します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Score Buckets</h3>

<p>サンドボックスはサンプルを 1〜10 のトリアージスコアで評価します。結果は以下のバケットにグループ化されます。</p>

| Bucket | Score Range | Meaning |
|---|---|---|
| `malicious` | 8–10 | 既知のマルウェア、高い確信度 |
| `suspicious` | 5–7 | 強い行動的インジケーター |
| `potentially_suspicious` | 3–4 | 一部のインジケーター |
| `clean` | 1–2 | 低リスクまたは無害 |

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox stats [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-stats--days"><a href="#banshee-sandbox-stats--days"><code>--days</code></a>, <code>-d</code> <i>days</i></dt><dd>
    <p>遡及参照するウィンドウ期間（日数）</p>
    <p>デフォルトは 7</p></dd>
    <dt id="banshee-sandbox-stats--subset"><a href="#banshee-sandbox-stats--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>集計するサンプルのスコープ</p>
    <p>指定可能な値: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>デフォルトは <code>org</code></p></dd>
    <dt id="banshee-sandbox-stats--pretty"><a href="#banshee-sandbox-stats--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-stats--help"><a href="#banshee-sandbox-stats--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats --days 30 --pretty
</code></pre>

### banshee sandbox list

サンドボックスサンプルを一覧表示します。自分のサンプル、組織のサンプル（デフォルト）、または公開フィードを対象にできます。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox list [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-list--subset"><a href="#banshee-sandbox-list--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>一覧表示するサンプルのスコープ</p>
    <p>指定可能な値: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>デフォルトは <code>org</code></p></dd>
    <dt id="banshee-sandbox-list--limit"><a href="#banshee-sandbox-list--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>返すサンプルの最大件数</p>
    <p>指定可能な範囲: 1〜4095</p>
    <p>デフォルトは 20</p></dd>
    <dt id="banshee-sandbox-list--pretty"><a href="#banshee-sandbox-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-list--help"><a href="#banshee-sandbox-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
</code></pre>

### banshee sandbox search

構造化フィルター（ハッシュ、ファミリー、タグ、ボットネット、ウォレット、IP、ドメイン、URL、提出日ウィンドウ）または生の Triage クエリに一致するサンプルを検索します。少なくとも 1 つのフィルターまたは `--query` の指定が必要です。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-search--hash"><a href="#banshee-sandbox-search--hash"><code>--hash</code></a> <i>hash</i></dt><dd>
    <p>ファイルハッシュ（MD5/SHA1/SHA256）でフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--family"><a href="#banshee-sandbox-search--family"><code>--family</code></a> <i>family</i></dt><dd>
    <p>マルウェアファミリー名でフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--tag"><a href="#banshee-sandbox-search--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>タグでフィルタリングする（繰り返し指定可）</p></dd>
    <dt id="banshee-sandbox-search--botnet"><a href="#banshee-sandbox-search--botnet"><code>--botnet</code></a> <i>botnet</i></dt><dd>
    <p>ボットネット名でフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--wallet"><a href="#banshee-sandbox-search--wallet"><code>--wallet</code></a> <i>wallet</i></dt><dd>
    <p>ウォレットアドレスでフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--ip"><a href="#banshee-sandbox-search--ip"><code>--ip</code></a> <i>ip</i></dt><dd>
    <p>IP アドレスでフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--domain"><a href="#banshee-sandbox-search--domain"><code>--domain</code></a> <i>domain</i></dt><dd>
    <p>ドメインでフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--url"><a href="#banshee-sandbox-search--url"><code>--url</code></a> <i>url</i></dt><dd>
    <p>URL でフィルタリングする</p></dd>
    <dt id="banshee-sandbox-search--from-date"><a href="#banshee-sandbox-search--from-date"><code>--from-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>この日付以降に提出されたサンプルを対象とする</p></dd>
    <dt id="banshee-sandbox-search--to-date"><a href="#banshee-sandbox-search--to-date"><code>--to-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>この日付以前に提出されたサンプルを対象とする</p></dd>
    <dt id="banshee-sandbox-search--query"><a href="#banshee-sandbox-search--query"><code>--query</code></a>, <code>-q</code> <i>query</i></dt><dd>
    <p>生の Triage クエリ文字列（構造化フィルターと AND で結合されます）</p></dd>
    <dt id="banshee-sandbox-search--limit"><a href="#banshee-sandbox-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>返すサンプルの最大件数（1〜200）</p>
    <p>デフォルトは 50</p></dd>
    <dt id="banshee-sandbox-search--pretty"><a href="#banshee-sandbox-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-search--help"><a href="#banshee-sandbox-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

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

ID で単一のサンドボックスサンプルの概要を取得します。現在のステータス、総合スコア、ターゲット、作成・完了タイムスタンプ、SHA256、タスクごとの内訳が含まれます。進行中のサンプルと完了済みサンプルの両方に対応しています。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox get [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--sample-id"><a href="#banshee-sandbox-get--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>サンドボックスサンプル ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--pretty"><a href="#banshee-sandbox-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-get--help"><a href="#banshee-sandbox-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
</code></pre>

### banshee sandbox download

1 件以上のサンプル ID の元の提出サンプルバイト列をダウンロードします。各サンプルは、ウイルス対策ソフト、セキュアメールゲートウェイ、またはファイルマネージャーによる意図しない実行を防ぐため、パスワード `infected` の AES 暗号化 ZIP アーカイブにラップされます。

展開には `7z x -pinfected <sample-id>.zip` を使用してください。標準の `unzip` は AES 暗号化 ZIP を確実に処理できません。

サンプル ID は位置引数として渡すか、標準入力からパイプで渡すことができます（スペース区切り）。`--yes` を指定しない限り、確認プロンプトが表示されます。

> **安全に関する注意:** サンプルのバイト列はダウンロードおよび ZIP 圧縮中にこのプロセスのメモリに一時的に存在します。積極的な EDR によるメモリスキャンが検知する可能性があります。日常業務で使用する社内ラップトップではなく、アナリスト専用の環境で実行してください。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox download [OPTIONS] [SAMPLE_IDS]...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--sample-ids"><a href="#banshee-sandbox-download--sample-ids"><code>SAMPLE_IDS</code></a></dt><dd><p>1 件以上のサンプル ID（または標準入力からスペース区切りで読み込み）</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--output-dir"><a href="#banshee-sandbox-download--output-dir"><code>--output-dir</code></a>, <code>-d</code> <i>DIR</i></dt><dd>
    <p>暗号化された ZIP アーカイブを保存するディレクトリ（存在しない場合は作成されます）。必須。</p></dd>
    <dt id="banshee-sandbox-download--yes"><a href="#banshee-sandbox-download--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>確認プロンプトをスキップする</p></dd>
    <dt id="banshee-sandbox-download--workers"><a href="#banshee-sandbox-download--workers"><code>--workers</code></a>, <code>-w</code> <i>N</i></dt><dd>
    <p>並列ダウンロードのワーカー数（1〜16）</p>
    <p>デフォルトは 1</p></dd>
    <dt id="banshee-sandbox-download--help"><a href="#banshee-sandbox-download--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
</code></pre>

### banshee sandbox delete

ID でサンドボックスサンプルを削除し、関連するすべてのタスクアーティファクトを削除します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox delete [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--sample-id"><a href="#banshee-sandbox-delete--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>削除するサンプル ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--yes"><a href="#banshee-sandbox-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>確認プロンプトをスキップする</p></dd>
    <dt id="banshee-sandbox-delete--help"><a href="#banshee-sandbox-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
</code></pre>

### banshee sandbox submit

サンプルを解析に提出します。ローカルファイルはアップロードされ、URL はブラウザで実行されます（`--fetch` を使用すると先にダウンロードされます）。公開サンプルは `--import` を使用して ID でインポートできます。

デフォルトでは、JSON 形式の提出受付レシートを出力します。`--wait` を使用すると、解析が完了するまでポーリングして概要レポートを出力します。

<h3 class="commands-reference">Target Kinds</h3>

| Target | Behaviour |
|---|---|
| ローカルファイルパス | アップロードされて解析される |
| URL | ブラウザで実行される |
| URL + `--fetch` | 先にダウンロードされ、ファイルとして解析される |
| 公開サンプル ID + `--import` | 組織のサンドボックスにインポートされる |

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox submit [OPTIONS] TARGET
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--target"><a href="#banshee-sandbox-submit--target"><code>TARGET</code></a></dt><dd><p>ファイルパス、URL、または公開サンプル ID（<code>--import</code> と組み合わせて使用）</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--fetch"><a href="#banshee-sandbox-submit--fetch"><code>--fetch</code></a></dt><dd>
    <p>URL ターゲットを先にダウンロードし、取得したファイルを解析します。<code>--import</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-submit--import"><a href="#banshee-sandbox-submit--import"><code>--import</code></a></dt><dd>
    <p>ターゲットを組織にインポートする公開サンプル ID として扱います。<code>--fetch</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-submit--profile"><a href="#banshee-sandbox-submit--profile"><code>--profile</code></a> <i>profile</i></dt><dd>
    <p>解析プロファイルの名前または ID。複数のプロファイルを割り当てるために繰り返し指定できます。<code>--interactive</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-submit--timeout"><a href="#banshee-sandbox-submit--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>解析タイムアウト（秒）</p>
    <p>指定可能な範囲: 1〜3600</p></dd>
    <dt id="banshee-sandbox-submit--network"><a href="#banshee-sandbox-submit--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>解析環境のネットワークモード</p>
    <p>指定可能な値: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-submit--geolocation"><a href="#banshee-sandbox-submit--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN の出口国コード。<code>--network vpn</code> が必要です</p></dd>
    <dt id="banshee-sandbox-submit--tags"><a href="#banshee-sandbox-submit--tags"><code>--tags</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>提出に付与するカスタムタグ。繰り返し指定できます</p></dd>
    <dt id="banshee-sandbox-submit--password"><a href="#banshee-sandbox-submit--password"><code>--password</code></a> <i>password</i></dt><dd>
    <p>パスワード保護されたアーカイブのパスワード</p></dd>
    <dt id="banshee-sandbox-submit--wait"><a href="#banshee-sandbox-submit--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>解析が完了するまでポーリングし、概要レポートを出力します</p></dd>
    <dt id="banshee-sandbox-submit--interactive"><a href="#banshee-sandbox-submit--interactive"><code>--interactive</code></a>, <code>-i</code></dt><dd>
    <p>静的解析で一時停止し、<a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a> でファイルとプロファイルを選択できるようにします。<code>--profile</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-submit--pretty"><a href="#banshee-sandbox-submit--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-submit--help"><a href="#banshee-sandbox-submit--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

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

静的解析で一時停止しているサンプル（`--interactive` で提出されたもの）に解析プロファイルを割り当てます。`--auto` を使用するとサンドボックスが自動的にプロファイルを選択し、`--pick` を使用すると特定のファイルに特定のプロファイルを手動でマッピングできます。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox set-profile [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--sample-id"><a href="#banshee-sandbox-set-profile--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>静的解析で一時停止しているサンプルの ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--auto"><a href="#banshee-sandbox-set-profile--auto"><code>--auto</code></a>, <code>-a</code></dt><dd>
    <p>すべてのファイルに対してサンドボックスが自動的にプロファイルを選択します。<code>--pick</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-set-profile--pick"><a href="#banshee-sandbox-set-profile--pick"><code>--pick</code></a> <i>FILE:PROFILE</i></dt><dd>
    <p>特定のファイルを特定のプロファイルにマッピングします。<code>FILE:PROFILE</code> 形式で指定します。繰り返し指定できます。<code>--auto</code> とは同時に使用できません</p></dd>
    <dt id="banshee-sandbox-set-profile--pretty"><a href="#banshee-sandbox-set-profile--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-set-profile--help"><a href="#banshee-sandbox-set-profile--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --auto -p
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
</code></pre>

### banshee sandbox profile

解析プロファイルを管理します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-profile-list"><code>banshee sandbox profile list</code></a></dt><dd><p>利用可能なすべての解析プロファイルを一覧表示する</p></dd>
    <dt><a href="#banshee-sandbox-profile-get"><code>banshee sandbox profile get</code></a></dt><dd><p>特定のプロファイルの詳細を取得する</p></dd>
    <dt><a href="#banshee-sandbox-profile-create"><code>banshee sandbox profile create</code></a></dt><dd><p>新しい解析プロファイルを作成する</p></dd>
    <dt><a href="#banshee-sandbox-profile-update"><code>banshee sandbox profile update</code></a></dt><dd><p>既存の解析プロファイルを更新する</p></dd>
    <dt><a href="#banshee-sandbox-profile-delete"><code>banshee sandbox profile delete</code></a></dt><dd><p>解析プロファイルを削除する</p></dd>
</dl>

#### banshee sandbox profile list

利用可能なすべての解析プロファイルを一覧表示します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile list [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-list--pretty"><a href="#banshee-sandbox-profile-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-profile-list--help"><a href="#banshee-sandbox-profile-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
</code></pre>

#### banshee sandbox profile get

名前または ID で特定の解析プロファイルの詳細を取得します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile get [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--profile-id-or-name"><a href="#banshee-sandbox-profile-get--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>プロファイルの UUID または表示名</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--pretty"><a href="#banshee-sandbox-profile-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-profile-get--help"><a href="#banshee-sandbox-profile-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
</code></pre>

#### banshee sandbox profile create

新しい解析プロファイルを作成します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Profile Tags</h3>

<p>タグはプロファイルのオペレーティングシステムと環境を定義します。ロケールタグは必ず 1 つ以上の <code>os</code> タグと組み合わせて指定してください。</p>

<pre><code class="language-bash">
# OS only
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64

# OS + locale
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64 -T locale:en-us
</code></pre>

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile create [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-create--name"><a href="#banshee-sandbox-profile-create--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>プロファイルの表示名。必須</p></dd>
    <dt id="banshee-sandbox-profile-create--tag"><a href="#banshee-sandbox-profile-create--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>プロファイルタグ（例: <code>os:windows10-2004-x64</code>, <code>locale:en-us</code>）。繰り返し指定できます。必須</p></dd>
    <dt id="banshee-sandbox-profile-create--timeout"><a href="#banshee-sandbox-profile-create--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>解析タイムアウト（秒）</p>
    <p>指定可能な範囲: 1〜3600</p>
    <p>デフォルトは 120</p></dd>
    <dt id="banshee-sandbox-profile-create--network"><a href="#banshee-sandbox-profile-create--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>ネットワークモード</p>
    <p>指定可能な値: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-create--geolocation"><a href="#banshee-sandbox-profile-create--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN の出口国コード。繰り返し指定できます。<code>--network vpn</code> が必要です</p></dd>
    <dt id="banshee-sandbox-profile-create--browser"><a href="#banshee-sandbox-profile-create--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>URL 実行に使用するブラウザ</p>
    <p>指定可能な値: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-create--pretty"><a href="#banshee-sandbox-profile-create--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-profile-create--help"><a href="#banshee-sandbox-profile-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
</code></pre>

#### banshee sandbox profile update

名前または ID で既存の解析プロファイルを更新します。少なくとも 1 つのオプションを指定する必要があります。

出力は `{"updated": true}` または `{"updated": false}` です（どちらの場合も終了コードは 0）。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile update [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--profile-id-or-name"><a href="#banshee-sandbox-profile-update--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>更新するプロファイルの UUID または表示名</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--name"><a href="#banshee-sandbox-profile-update--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>新しいプロファイル表示名</p></dd>
    <dt id="banshee-sandbox-profile-update--tag"><a href="#banshee-sandbox-profile-update--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>既存のすべてのタグを置き換えます。繰り返し指定できます</p></dd>
    <dt id="banshee-sandbox-profile-update--timeout"><a href="#banshee-sandbox-profile-update--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>解析タイムアウト（秒）</p>
    <p>指定可能な範囲: 1〜3600</p></dd>
    <dt id="banshee-sandbox-profile-update--network"><a href="#banshee-sandbox-profile-update--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>ネットワークモード</p>
    <p>指定可能な値: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-update--geolocation"><a href="#banshee-sandbox-profile-update--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN の出口国コード。繰り返し指定できます。<code>--network vpn</code> が必要です</p></dd>
    <dt id="banshee-sandbox-profile-update--browser"><a href="#banshee-sandbox-profile-update--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>URL 実行に使用するブラウザ</p>
    <p>指定可能な値: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-update--unset"><a href="#banshee-sandbox-profile-update--unset"><code>--unset</code></a> <i>field</i></dt><dd>
    <p>フィールドをクリアします。繰り返し指定できます</p>
    <p>指定可能な値: <code>network</code>, <code>browser</code>, <code>geolocation</code></p>
    <p>同一フィールドに対応する設定オプションとは同時に使用できません。<code>--unset network</code> は <code>--geolocation</code> と競合します</p></dd>
    <dt id="banshee-sandbox-profile-update--pretty"><a href="#banshee-sandbox-profile-update--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-profile-update--help"><a href="#banshee-sandbox-profile-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
</code></pre>

#### banshee sandbox profile delete

名前または ID で解析プロファイルを削除します。存在しないプロファイルを削除しようとすると、警告を表示して終了コード 0 で終了します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile delete [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--profile-id-or-name"><a href="#banshee-sandbox-profile-delete--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>削除するプロファイルの UUID または表示名</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--yes"><a href="#banshee-sandbox-profile-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>確認プロンプトをスキップする</p></dd>
    <dt id="banshee-sandbox-profile-delete--help"><a href="#banshee-sandbox-profile-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
</code></pre>

### banshee sandbox report

サンプル解析レポートを管理します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-report-overview"><code>banshee sandbox report overview</code></a></dt><dd><p>完了したサンプルの完全な概要レポート</p></dd>
    <dt><a href="#banshee-sandbox-report-static"><code>banshee sandbox report static</code></a></dt><dd><p>静的解析レポート — 動的タスクの完了前に取得可能</p></dd>
    <dt><a href="#banshee-sandbox-report-behavioral"><code>banshee sandbox report behavioral</code></a></dt><dd><p>動的解析レポート — 完了したタスクごとに 1 オブジェクト</p></dd>
</dl>

#### banshee sandbox report overview

完了したサンプルの完全な概要レポートです。判定スコア、マルウェアファミリー、タグ、ハッシュ、検知シグネチャ、抽出されたマルウェア設定、ネットワーク IOC、タスクごとの結果が含まれます。サンプルは `reported` ステータスである必要があります。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report overview [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--sample-id"><a href="#banshee-sandbox-report-overview--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>レポートを取得するサンプル ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--wait"><a href="#banshee-sandbox-report-overview--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>レポートが準備できるまでポーリングします（最大 30 分）。タイムアウト後も準備できていない場合は非ゼロで終了します</p></dd>
    <dt id="banshee-sandbox-report-overview--pretty"><a href="#banshee-sandbox-report-overview--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-report-overview--help"><a href="#banshee-sandbox-report-overview--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
</code></pre>

#### banshee sandbox report static

サンプルの静的解析レポートです。判定スコア、タグ、アンパックされたファイル、静的検知シグネチャ、抽出されたマルウェア設定が含まれます。動的タスクの完了前に取得できます。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report static [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--sample-id"><a href="#banshee-sandbox-report-static--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>静的レポートを取得するサンプル ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--wait"><a href="#banshee-sandbox-report-static--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>レポートが準備できるまでポーリングします（最大 10 分）</p></dd>
    <dt id="banshee-sandbox-report-static--pretty"><a href="#banshee-sandbox-report-static--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-report-static--help"><a href="#banshee-sandbox-report-static--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
</code></pre>

#### banshee sandbox report behavioral

サンプルの動的解析レポートです。完了した動的タスクごとに 1 つの JSON オブジェクトを返します。各オブジェクトには判定スコア、プラットフォーム、トリガーされたシグネチャ、観測されたプロセス、ネットワークアクティビティ、抽出されたマルウェア設定が含まれます。

未完了のタスクは出力から省略され、標準エラーに記録されます。すべてのタスクが完了するまでコマンドは非ゼロで終了します。サンプルに動的タスクが存在しない場合は、終了コード 0 で空の配列を返します。

デフォルトでは、結果を JSON 形式で出力します。

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report behavioral [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--sample-id"><a href="#banshee-sandbox-report-behavioral--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>動的解析レポートを取得するサンプル ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--wait"><a href="#banshee-sandbox-report-behavioral--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>すべてのタスクが完了するまでポーリングします（最大 30 分）</p></dd>
    <dt id="banshee-sandbox-report-behavioral--full-cmd"><a href="#banshee-sandbox-report-behavioral--full-cmd"><code>--full-cmd</code></a></dt><dd>
    <p>プロセスのコマンドラインを省略せず完全に表示します。コマンドラインの内容はマルウェアサンプルから直接取得されるため、信頼できない入力として扱ってください</p></dd>
    <dt id="banshee-sandbox-report-behavioral--pretty"><a href="#banshee-sandbox-report-behavioral--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>人間が読みやすい形式で結果を整形して表示する</p></dd>
    <dt id="banshee-sandbox-report-behavioral--help"><a href="#banshee-sandbox-report-behavioral--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>このコマンドのヘルプを表示する</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
</code></pre>