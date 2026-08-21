# 명령줄 레퍼런스

## banshee

PS Banshee는 보안 전문가 및 SOC 팀을 위해 설계된, Recorded Future Intelligence에 빠르고 효율적으로 접근할 수 있는 명령줄 도구입니다.

<h3 class="commands-reference">사용법</h3>

```
banshee [OPTIONS] <COMMAND>
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca"><code>banshee ca</code></a></dt><dd><p>Recorded Future Classic Alerts 검색, 조회 및 업데이트</p></dd>
    <dt><a href="#banshee-email"><code>banshee email</code></a></dt><dd><p>이메일 파일(EML)을 Recorded Future 인텔리전스로 보강</p></dd>
    <dt><a href="#banshee-entity"><code>banshee entity</code></a></dt><dd><p>Recorded Future 엔티티 검색 및 조회</p></dd>
    <dt><a href="#banshee-ioc"><code>banshee ioc</code></a></dt><dd><p>침해 지표(IOC) 검색 및 조회</p></dd>
    <dt><a href="#banshee-list"><code>banshee list</code></a></dt><dd><p>Recorded Future 목록 및 Watch list 관리</p></dd>
    <dt><a href="#banshee-pba"><code>banshee pba</code></a></dt><dd><p>Recorded Future Playbook Alerts 검색, 조회 및 업데이트</p></dd>
    <dt><a href="#banshee-pcap"><code>banshee pcap</code></a></dt><dd><p>Recorded Future Intelligence로 패킷 캡처(pcap) 파일을 보강하여 분석</p></dd>
    <dt><a href="#banshee-risklist"><code>banshee risklist</code></a></dt><dd><p>Risk List 관리</p></dd>
    <dt><a href="#banshee-rules"><code>banshee rules</code></a></dt><dd><p>탐지 규칙 검색 및 다운로드</p></dd>
</dl>

## banshee ca

Recorded Future Classic Alerts 검색, 조회 및 업데이트

<h3 class="commands-reference">사용법</h3>

```
banshee ca [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca-lookup"><code>banshee ca lookup</code></a></dt><dd><p>Classic Alert 조회</p></dd>
    <dt><a href="#banshee-ca-search"><code>banshee ca search</code></a></dt><dd><p>Classic Alerts 검색</p></dd>
    <dt><a href="#banshee-ca-rules"><code>banshee ca rules</code></a></dt><dd><p>Classic Alert 규칙 검색</p></dd>
    <dt><a href="#banshee-ca-update"><code>banshee ca update</code></a></dt><dd><p>하나 이상의 Classic Alert 업데이트</p></dd>
    <dt><a href="#banshee-ca-export"><code>banshee ca export</code></a></dt><dd><p>Classic Alerts를 JSON 또는 CSV로 내보내기</p></dd>
</dl>

### banshee ca lookup

Classic Alert를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ca lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--alert-id"><a href="#banshee-ca-lookup--alert-id"><code>ALERT_ID</code></a></dt><dd><p>조회할 Alert ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ca-lookup--help"><a href="#banshee-ca-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee ca search

Classic Alerts를 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ca search [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-search--triggered"><a href="#banshee-ca-search--triggered"><code>--triggered</code>, <code>-t</code></a> <i>triggered</i></dt><dd>
    <p>트리거 시간 기준으로 필터링, 예: 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)</p>
    <p>기본값: 1d</p><dd></dd>
    <dt id="banshee-ca-search--rule"><a href="#banshee-ca-search--rule"><code>--rule</code></a> <i>rule-name</i></dt><dd>
    <p>알림 규칙 이름으로 필터링 (자유 텍스트)</p><dd></dd>
    <dt id="banshee-ca-search--status"><a href="#banshee-ca-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>알림 상태로 필터링</p>
    <p>가능한 값: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-search--pretty"><a href="#banshee-ca-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ca-search--help"><a href="#banshee-ca-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee ca rules

Classic Alert 규칙을 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ca rules [OPTIONS] [FREETEXT]
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--freetext"><a href="#banshee-ca-rules--freetext"><code>FREETEXT</code></a></dt><dd><p>선택 사항. 알림 규칙을 이름으로 필터링하는 데 사용되는 자유 텍스트.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--pretty"><a href="#banshee-ca-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ca-rules--help"><a href="#banshee-ca-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee ca update

하나 이상의 Classic Alert를 업데이트합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ca update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--alert-id"><a href="#banshee-ca-update--alert-id"<code>ALERT_IDS</code></a></dt><dd><p>공백으로 구분된 하나 이상의 Alert ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--status"><a href="#banshee-ca-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>알림을 지정한 상태로 업데이트</p>
    <p>가능한 값: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-update--note"><a href="#banshee-ca-update--note"><code>--note</code></a>,  <code>-n</code> <i>note</i></dt><dd>
    <p>알림에 추가할 노트 텍스트.</p><p>노트의 최대 길이는 1000자입니다.</p><dd></dd>
    <dt id="banshee-ca-update--append"><a href="#banshee-ca-update--append"><code>--append</code></a>,  <code>-a</code></dt><dd>
    <p>알림에 이미 노트가 있는 경우 노트 텍스트를 추가(append)합니다.</p><dd></dd>
    <dt id="banshee-ca-update--assignee"><a href="#banshee-ca-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>알림을 할당할 새 사용자. uhash 또는 이메일 주소를 허용합니다. 예: uhash:3aXZxdkM12, analyst@acme.com</p><dd></dd>
    <dt id="banshee-ca-update--help"><a href="#banshee-ca-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<p>하나 이상의 Alert ID(공백으로 구분)를 제공하고 원하는 업데이트 옵션을 지정합니다:</p>

<pre><code class="language-bash">
banshee ca update <alert id> -s Dismissed
banshee ca update <alert id> -s Dismissed -n "note text"
banshee ca update <alert id1> <alert id2>-s Dismissed -n "note text" -a analyst@acme.com
</code></pre>

<h3 class="commands-reference">Alert ID 입력 방법</h3>

<h4>1. 인수로 직접 입력 (단일 또는 복수):</h4>

<pre><code class="language-bash">
banshee ca update ALERT_ID -s Resolved
banshee ca update ALERT_ID_1 ALERT_ID_2 -s Pending
</code></pre>

<h4>2. 파일 또는 표준 입력에서 읽기:</h4>

<p>한 줄에 하나의 Alert ID가 있는 파일(예: <code>alerts.txt</code>)이 있는 경우:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>다음 명령어로 목록에 있는 모든 알림을 업데이트할 수 있습니다:</p>

<pre><code class="language-bash">
banshee ca update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee ca update -s Dismissed
</code></pre>

<h4>3. 검색 명령어에서 파이프로 연결:</h4>

<p><code>jq</code>와 같은 도구를 사용하여 검색 결과에서 Alert ID를 추출하고 업데이트 명령어로 파이프합니다:</p>

<pre><code class="language-bash">
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"
</code></pre>

<h3 class="commands-reference">노트 추가(Append)</h3>

<p>Classic Alerts는 단일 노트만 지원합니다. 기본적으로 <code>update</code> 명령어는 기존 노트를 새 노트로 덮어씁니다.
새 노트를 추가하려면 <code>--append</code> (<code>-A</code>) 옵션을 사용하십시오.</p>

### banshee ca export

Classic Alerts를 JSON 또는 CSV로 내보냅니다. 일반적으로 [`banshee ca search`](#banshee-ca-search)에서 파이프로 연결하여 stdin에서 Alert ID를 읽습니다.

<h3 class="commands-reference">출력 형식</h3>

<p><b>JSON (기본값)</b> — Recorded Future API가 반환하는 각 ID의 <i>전체</i> 알림 객체를 출력합니다. 모든 최상위 필드와 중첩된 hits, 엔티티, 증거, AI 인사이트, 검토 기록, 포털 URL 등이 포함됩니다. 다운스트림 도구, <code>jq</code> 파이프라인 또는 재수집에 적합합니다.</p>

<p><b>CSV (<a href="#banshee-ca-export--csv"><code>--csv</code></a>)</b> — 스프레드시트 및 보고용으로 설계된 요약 정보를 출력합니다. 아래에 나열된 11개 열만 작성되며(헤더 행 포함), JSON 응답에 있는 다른 모든 필드는 제외됩니다.</p>

| 필드 | 설명 |
|---|---|
| `ID` | Classic Alert ID |
| `Priority` | 알림 우선순위 — 알림 규칙이 우선순위 규칙인 경우 `High`, 그렇지 않으면 `Informational` |
| `Alert Rule` | 트리거된 알림 규칙의 이름 |
| `Status` | 포털 상태, 예: `New`, `Pending`, `Dismissed`, `Resolved` |
| `Created` | 트리거 타임스탬프 (UTC) |
| `Updated` | 마지막 업데이트 타임스탬프 — *현재 항상 비어 있음; 향후 API 지원을 위해 예약됨* |
| `Title` | 알림 제목 |
| `Assignee` | 담당자 (uhash 또는 이메일) |
| `URL` | 해당 알림의 Recorded Future 포털 URL |
| `Entities` | 기본 엔티티 이름, `;`로 구분 |
| `Recorded Future AI Insights` | AI가 생성한 인사이트 텍스트 또는 코멘트 |

<h3 class="commands-reference">사용법</h3>

```
banshee ca search [SEARCH_OPTIONS] | banshee ca export [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-export--csv"><a href="#banshee-ca-export--csv"><code>--csv</code></a></dt><dd>
    <p>위에서 설명한 고정 열 집합으로 CSV 형식으로 출력합니다. 이 플래그가 없으면 JSON으로 출력됩니다.</p><dd></dd>
    <dt id="banshee-ca-export--help"><a href="#banshee-ca-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">파이프 입력</h3>

<p><code>banshee ca export</code>는 파이프 입력만 허용합니다. <a href="#banshee-ca-search"><code>banshee ca search</code></a>가 생성한 JSON 배열을 소비하여 Alert ID를 추출하고 각 알림을 전체 내용으로 가져옵니다. 파이프 없이 명령어를 실행하면 오류가 발생합니다.</p>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s New | banshee ca export --csv > alerts.csv
</code></pre>

## banshee entity

Recorded Future 엔티티 검색 및 조회

<h3 class="commands-reference">사용법</h3>

```
banshee entity [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-entity-lookup"><code>banshee entity lookup</code></a></dt><dd><p>ID로 엔티티 조회</p></dd>
    <dt><a href="#banshee-entity-search"><code>banshee entity search</code></a></dt><dd><p>이름 및/또는 유형으로 엔티티 검색</p></dd>
</dl>

### banshee entity lookup

ID로 엔티티를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee entity lookup [OPTIONS] ENTITY_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--entity-id"><a href="#banshee-entity-lookup--entity-id"<code>ENTITY_ID</code></a></dt><dd><p>조회할 엔티티 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--pretty"><a href="#banshee-entity-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-entity-lookup--help"><a href="#banshee-entity-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee entity search

이름 및/또는 유형으로 엔티티를 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee entity search [OPTIONS] NAME
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--name"><a href="#banshee-entity-search--name"><code>NAME</code></a></dt><dd><p>검색할 엔티티 이름</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--type"><a href="#banshee-entity-search--type"><code>--type</code>, <code>-t</code></a> <i>entity-type</i></dt><dd>
    <p>검색할 엔티티 유형</p>
    <p>다른 엔티티 유형에 대해 여러 번 지정 가능</p>
    <p>지원 값:</p>
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
    <p>결과 수 제한</p>
    <p>최대 제한: 100</p>
    <p>기본값: 100</p><dd></dd>
    <dt id="banshee-entity-search--pretty"><a href="#banshee-entity-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-entity-search--help"><a href="#banshee-entity-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>


## banshee email

이메일 파일(EML)을 Recorded Future 인텔리전스로 보강합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee email [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-email-enrich"><code>banshee email enrich</code></a></dt><dd><p>이메일(EML) 파일을 Recorded Future 인텔리전스로 보강</p></dd>
</dl>

### banshee email enrich

이메일(EML) 파일을 Recorded Future Intelligence로 보강합니다. 이 명령어는 EML 파일을 파싱하여 헤더에서 IP 주소를 추출하고, 본문에서 `http`/`https`로 시작하는 URL을 추출한 후 위협 인텔리전스 데이터로 보강합니다. 기본적으로 결과는 위험 점수 임계값을 충족하는 지표만 표시되도록 필터링됩니다. 위험 점수 임계값 미만이더라도 위협 행위자와 연결된 지표를 포함하려면 `--threat-hunt`를 사용하십시오.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">JSON 출력</h3>

JSON 배열의 각 결과 객체에는 다음 필드가 포함됩니다:

| 필드 | 설명 |
|---|---|
| `ioc` | 이메일에서 추출된 지표 — IP 주소 또는 URL |
| `type` | 지표 유형, 예: `ip` 또는 `url` |
| `location` | 지표가 발견된 이메일 섹션, 예: `header` 또는 `body` |
| `risk_score` | Recorded Future 위험 점수 |
| `ta_names` | 이 지표와 연관된 위협 행위자 이름 목록. 없으면 빈 값 |
| `malwares` | 이 지표와 연결된 악성코드 패밀리 이름 목록. 없으면 빈 값 |
| `first_seen` | 최초 관측 시각의 ISO 8601 타임스탬프 |
| `last_seen` | 가장 최근 관측 시각의 ISO 8601 타임스탬프 |
| `count_of_analyst_notes` | 이 지표를 참조하는 Recorded Future 애널리스트 노트 수 |
| `rule_evidence` | 개별 위험 규칙 증거 세부 정보 배열, 심각도 높은 순으로 정렬 |

`rule_evidence` 배열의 각 객체에는 다음이 포함됩니다:

| 필드 | 설명 |
|---|---|
| `rule` | 트리거된 특정 Recorded Future 위험 규칙의 이름 |
| `level` | 이 규칙의 심각도 수준 — 숫자가 높을수록 더 심각 |
| `timestamp` | 이 규칙에 대한 가장 최근 관측 시각의 ISO 8601 타임스탬프 |
| `evidence_string` | 증거에 대한 사람이 읽을 수 있는 요약 |

<h3 class="commands-reference">사용법</h3>

```
banshee email enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--file-path"><a href="#banshee-email-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>보강할 EML 파일 경로</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--risk-score"><a href="#banshee-email-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>이 임계값보다 높은 위험 점수(0 - 99)를 가진 지표만 결과로 표시</p><p>기본값: 65</p></dd>
    <dt id="banshee-email-enrich--threat-hunt"><a href="#banshee-email-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>위험 점수 임계값에 관계없이 위협 행위자와 연결된 지표 포함</p></dd>
    <dt id="banshee-email-enrich--pretty"><a href="#banshee-email-enrich--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-email-enrich--help"><a href="#banshee-email-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>
<pre><code class="language-bash">
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p
banshee email enrich suspicious.eml --threat-hunt
</code></pre>

## banshee ioc

침해 지표(IOC) 검색 및 조회

<h3 class="commands-reference">사용법</h3>

```
banshee ioc [OPTIONS] COMMAND [ARGS]...
```
<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ioc-lookup"><code>banshee ioc lookup</code></a></dt><dd><p>하나 이상의 IOC에 대한 상세 보강 — API 호출당 하나의 지표, 상세도 설정 가능</p></dd>
    <dt><a href="#banshee-ioc-bulk-lookup"><code>banshee ioc bulk-lookup</code></a></dt><dd><p>위험 점수 및 트리거된 규칙을 반환하는 빠른 대량 보강 — API 호출당 최대 1000개의 IOC를 배치 처리</p></dd>
    <dt><a href="#banshee-ioc-search"><code>banshee ioc search</code></a></dt><dd><p>IOC 검색</p></dd>
    <dt><a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></dt><dd><p>IOC 규칙 검색</p></dd>
</dl>

### banshee ioc lookup

하나 이상의 IOC에 대한 상세 보강 — 지표당 API 호출 1회. [`--verbosity`](#banshee-ioc-lookup--verbosity)를 사용하여 기본 위험 점수부터 링크, 애널리스트 노트 등을 포함한 전체 인텔리전스까지 반환할 필드 수를 제어합니다. 풍부한 컨텍스트가 필요할 때 사용하십시오.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ioc lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>조회할 엔티티 유형</p>
    <p>지원 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-lookup--ioc"><a href="#banshee-ioc-lookup--ioc"><code>IOC</code></a></dt><dd><p>공백으로 구분된 하나 이상의 조회할 IOC</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--ai-insights"><a href="#banshee-ioc-lookup--ai-insights"><code>--ai-insights</code></a>,  <code>-a</code></dt><dd>
    <p>관련 위험 규칙 및 주요 참조를 요약하는 Recorded Future의 AI 생성 인사이트를 활성화합니다.</p>
    <p><strong>참고:</strong> AI 처리로 인해 응답 시간이 다소 길어질 수 있습니다.</p<dd></dd>
    <dt id="banshee-ioc-lookup--verbosity"><a href="#banshee-ioc-lookup--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>응답에서 반환되는 데이터 양을 제어합니다(1-5). 상세도 수준이 높을수록 JSON 출력에 더 많은 필드와 세부 정보가 포함됩니다.</p>
    <p><strong>참고:</strong> 상세도 수준이 높을수록 데이터 검색량 증가로 응답 시간이 느려질 수 있습니다.</p>
    <p>기본값: 1</p>
    <h4>상세도 수준별 사용 가능 필드</h4>
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
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ioc-lookup--help"><a href="#banshee-ioc-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>
<pre><code>
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23,139.224.189.177 -p
</code></pre>

조회할 IOC 목록을 쉼표 또는 줄 바꿈으로 구분하여 파이프로 전달합니다:

<pre><code>
cat test_ips.csv| banshee ioc lookup ip -p
</code></pre>


### banshee ioc bulk-lookup

단일 유형의 모든 수량의 IOC에 대한 빠른 대량 보강. API 호출당 최대 1000개의 IOC를 자동으로 배치 처리하므로, 대량 처리 시 [`banshee ioc lookup`](#banshee-ioc-lookup)보다 훨씬 빠릅니다.

지표당 고정 필드 집합(위험 점수 및 트리거된 위험 규칙)을 반환합니다. 대용량 트리아지(triage)에 사용하십시오.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ioc bulk-lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--entity-type"><a href="#banshee-ioc-bulk-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>보강할 엔티티 유형</p>
    <p>지원 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-bulk-lookup--ioc"><a href="#banshee-ioc-bulk-lookup--ioc"><code>IOC</code></a></dt><dd><p>보강할 공백으로 구분된 하나 이상의 IOC. stdin에서 입력도 허용합니다(아래 예시 참조).</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--pretty"><a href="#banshee-ioc-bulk-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ioc-bulk-lookup--help"><a href="#banshee-ioc-bulk-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>
<pre><code>
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877
</code></pre>

<h4>파일 / Stdin 입력</h4>

줄 바꿈으로 구분된 IOC 파일(한 줄에 하나씩)을 파이프 또는 리디렉션합니다:

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

<h4>이름 및 점수 추출</h4>
`jq`를 사용하여 JSON 출력에서 특정 필드를 추출합니다. 예:

<pre><code>
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'
</code></pre>


### banshee ioc search

Classic Alerts를 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ioc search [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>조회할 엔티티 유형</p>
    <p>지원 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-search--limit"><a href="#banshee-ioc-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>결과 수 제한</p>
    <p>최대 제한: 1000</p>
    <p>기본값: 5</p><dd></dd>
    <dt id="banshee-ioc-search--risk-score"><a href="#banshee-ioc-search--risk-score"><code>--risk-score</code>, <code>-r</code></a> <i>risk-score</i></dt><dd>
    <p>위험 점수 범위로 필터링, 예:</p>
    <p>
        <ul>
            <li><code>--risk-score '[20,90]'</code> &rarr; <code>20 &lt;= riskScore &lt;= 90</code>과 동일</li>
            <li><code>--risk-score '(20,90)'</code> &rarr; <code>20 &lt; riskScore &lt; 90</code>과 동일</li>
            <li><code>--risk-score '[20,90)'</code> &rarr; <code>20 &lt;= riskScore &lt; 90</code>과 동일</li>
            <li><code>--risk-score '[20,)'</code> &rarr; <code>20 &lt;= riskScore</code>와 동일</li>
            <li><code>--risk-score '[,90)'</code> &rarr; <code>riskScore &lt; 90</code>과 동일</li>
        </ul>
    </p>
    <p>올바른 파싱을 위해 위험 점수 범위를 따옴표로 감싸십시오.</p>
    <dd></dd>
    <dt id="banshee-ioc-search--risk-rule"><a href="#banshee-ioc-search--risk-rule"><code>--risk-rule</code>, <code>-R</code></a> <i>rule-name</i></dt><dd>
    <p>위험 규칙 이름으로 필터링</p>
    <p>사용 가능한 옵션은 이 <a href="https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future" target="_blank">지원 문서</a>의 위험 규칙 표에서 <b>Machine Name</b> 열을 참조하거나, <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> 명령어를 사용하십시오.</p><dd></dd>
    <dt id="banshee-ioc-search--verbosity"><a href="#banshee-ioc-search--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>응답에서 반환되는 데이터 양을 제어합니다(1-5). 상세도 수준이 높을수록 JSON 출력에 더 많은 필드와 세부 정보가 포함됩니다.</p>
    <p><strong>참고:</strong> 상세도 수준이 높을수록 데이터 검색량 증가로 응답 시간이 느려질 수 있습니다.</p>
    <p>기본값: 1</p>
    <h4>상세도 수준별 사용 가능 필드</h4>
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
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ioc-search--help"><a href="#banshee-ioc-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee ioc rules

특정 엔티티 유형에 대한 IOC 규칙을 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee ioc rules [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--entity-type"><a href="#banshee-ioc-rules--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>IOC 규칙의 엔티티 유형</p>
    <p>지원 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--freetext"><a href="#banshee-ioc-rules--freetext"><code>--freetext</code>, <code>-F</code></a> <i>freetext-rule-name</i></dt><dd>
    <p>자유 텍스트 검색으로 위험 규칙 이름 필터링</p><dd></dd>
    <dt id="banshee-ioc-rules--mitre"><a href="#banshee-ioc-rules--mitre"><code>--mitre-code</code>, <code>-M</code></a> <i>mitre-code</i></dt><dd>
    <p>MITRE ATT&CK 코드로 필터링</p><dd></dd>
    <dt id="banshee-ioc-rules--criticality"><a href="#banshee-ioc-rules--criticality"><code>--criticality</code>, <code>-C</code></a> <i>criticality</i></dt><dd>
    <p>위험도로 필터링. 값이 높을수록 위험도가 높음</p>
    <p>허용 값: 1~5</p>
    <p><strong>위험도 수준 (IP, Domain, URL, Hash)</strong></p>
    <ul>
        <li><code>4</code> – 매우 악성 (위험 점수 범위: 90–99)</li>
        <li><code>3</code> – 악성 (위험 점수 범위: 65–89)</li>
        <li><code>2</code> – 의심스러움 (위험 점수 범위: 25–64)</li>
        <li><code>1</code> – 비정상 (위험 점수 범위: 5–24)</li>
        <li><code>0</code> – 위험 증거 없음 (위험 점수 범위: 0)</li>
    </ul>
    <p><strong>위험도 수준 (Vulnerability)</strong></p>
    <ul>
        <li><code>5</code> – 매우 심각 (위험 점수 범위: 90–99)</li>
        <li><code>4</code> – 심각 (위험 점수 범위: 80–89)</li>
        <li><code>3</code> – 높음 (위험 점수 범위: 65–79)</li>
        <li><code>2</code> – 보통 (위험 점수 범위: 25–64)</li>
        <li><code>1</code> – 낮음 (위험 점수 범위: 5–24)</li>
        <li><code>0</code> – 위험 증거 없음 (위험 점수 범위: 0)</li>
    </ul>
    <dd></dd>
    <dt id="banshee-ioc-rules--pretty"><a href="#banshee-ioc-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-ioc-rules--help"><a href="#banshee-ioc-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

## banshee list

Recorded Future 목록 및 Watch list 관리

<h3 class="commands-reference">사용법</h3>

```
banshee list [OPTIONS] COMMAND [ARGS]...
```
<dl class="commands-reference">
    <dt><a href="#banshee-list-create"><code>banshee list create</code></a></dt><dd><p>새 목록 생성</p></dd>
    <dt><a href="#banshee-list-info"><code>banshee list info</code></a></dt><dd><p>목록에 대한 기본 정보 조회</p></dd>
    <dt><a href="#banshee-list-search"><code>banshee list search</code></a></dt><dd><p>목록 검색</p></dd>
    <dt><a href="#banshee-list-status"><code>banshee list status</code></a></dt><dd><p>목록 상태 조회</p></dd>
    <dt><a href="#banshee-list-entities"><code>banshee list entities</code></a></dt><dd><p>목록의 엔티티 조회</p></dd>
    <dt><a href="#banshee-list-add"><code>banshee list add</code></a></dt><dd><p>목록에 엔티티 추가</p></dd>
    <dt><a href="#banshee-list-bulk-add"><code>banshee list bulk-add</code></a></dt><dd><p>목록에 엔티티 대량 추가</p></dd>
    <dt><a href="#banshee-list-remove"><code>banshee list remove</code></a></dt><dd><p>목록에서 엔티티 제거</p></dd>
    <dt><a href="#banshee-list-bulk-remove"><code>banshee list bulk-remove</code></a></dt><dd><p>목록에서 엔티티 대량 제거</p></dd>
    <dt><a href="#banshee-list-copy"><code>banshee list copy</code></a></dt><dd><p>한 목록에서 다른 목록으로 엔티티 복사</p></dd>
    <dt><a href="#banshee-list-clear"><code>banshee list clear</code></a></dt><dd><p>목록의 모든 엔티티 삭제</p></dd>
    <dt><a href="#banshee-list-entries"><code>banshee list entries</code></a></dt><dd><p>목록에서 텍스트 항목 조회</p></dd>
</dl>

### banshee list create

새 목록을 생성합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list create [OPTIONS] NAME [LIST_TYPE]
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>NAME</code></a></dt><dd><p>생성할 목록 이름</p></dd>
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>LIST_TYPE</code></a></dt><dd><p>생성할 목록 유형</p>
    <p>지원 유형:</p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
    </ul>
    <p>기본값: <code>entity</code></p>
    </dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--pretty"><a href="#banshee-list-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-lookup--help"><a href="#banshee-list-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list info

이름, 유형, 타임스탬프, 소유자 정보 등 목록에 대한 정보를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list info [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>정보를 조회할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list search

목록을 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list search [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--name"><a href="#banshee-list-search--name"><code>NAME</code></a></dt><dd>
    <p>검색할 목록 이름</p>
    <p>이름을 지정하지 않으면 모든 목록이 반환됩니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--list-type"><a href="#banshee-list-search--list-type"><code>--list-type</code>, <code>-t</code></a> <i>list-type</i></dt><dd>
    <p>목록 유형으로 필터링</p>
    <p>지원 유형:</p>
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
    <p>결과 수 제한</p>
    <p>최대 제한: 3,000</p>
    <p>기본값: 1,000</p><dd></dd>
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list status

목록 상태와 엔티티 수를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list status [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>상태를 조회할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list entities

목록의 엔티티를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list entities [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>엔티티를 가져올 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>


### banshee list entries

목록의 텍스트 항목을 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list entries [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>텍스트 항목을 가져올 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>



### banshee list clear

목록을 완전히 초기화하고 모든 엔티티를 제거합니다. 이 명령어는 텍스트 항목을 삭제하지 않으며 지원되지 않습니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list clear [OPTIONS] LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>초기화할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list add

목록에 엔티티를 추가합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list add [OPTIONS] LIST_ID ENTITY_ID [PROPERTIES]
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--list-id"><a href="#banshee-list-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>추가할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
    <dt id="banshee-list-add--entity-id"><a href="#banshee-list-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>목록에 추가할 엔티티 ID 또는 유형과 함께 지정한 이름, 예:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul></dd>
    <dt id="banshee-list-add--properties"><a href="#banshee-list-add--properties"><code>PROPERTIES</code></a></dt><dd>
    <p>선택 사항. <code>annotation=&lt;text&gt;</code>를 사용하여 이 엔티티에 대해 Recorded Future 플랫폼에 표시되는 노트를 첨부합니다.</p>
    <p>값에 공백이 포함된 경우 따옴표로 감싸십시오.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--help"><a href="#banshee-list-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
</code></pre>

### banshee list bulk-add

목록에 여러 엔티티를 추가합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list bulk-add [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--list-id"><a href="#banshee-list-bulk-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>추가할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
    <dt id="banshee-list-bulk-add--entity-input"><a href="#banshee-list-bulk-add--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>공백 또는 줄 바꿈으로 구분된 하나 이상의 엔티티, 예:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>이 명령어는 stdin에서도 입력을 허용합니다. 'entities.txt'가 줄 바꿈으로 구분된 엔티티 파일이라고 가정합니다. 예:</p>
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
    <p>위를 참고하여 다음 명령어 중 하나를 실행하여 엔티티를 대량 추가할 수 있습니다:</p>
    <pre><code>
    $ banshee list bulk-add LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-add LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--overwrite"><a href="#banshee-list-bulk-add--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>덮어쓰기 모드를 활성화합니다. 설정 시 다음 작업이 수행됩니다:</p>
    <ul>
        <li>현재 목록에 있으면서 제공된 파일에도 있는 엔티티는 유지</li>
        <li>제공된 파일에 있지만 목록에 없는 새 엔티티는 추가</li>
        <li>현재 목록에 있지만 제공된 파일에 <strong>없는</strong> 엔티티는 제거</li>
    </ul>
    <p>기본적으로(이 플래그 없이) 명령어는 기존 목록에 새 엔티티를 추가하며 아무것도 제거하지 않습니다.</p>
    </dd>
    <dt id="banshee-list-bulk-add--help"><a href="#banshee-list-bulk-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">결과 상태 출력</h3>

<p><code>banshee list bulk-add</code>는 출력을 상태별로 그룹화하고 해당 상태 아래에 일치하는 입력 엔티티를 출력합니다. 예:</p>

<pre><code class="language-text">
ADDED:
SoA6SP

ERROR_MULTIPLE_MATCHES:
wanna:malware
</code></pre>

<p>일반적인 상태값:</p>
<ul>
    <li><code>ADDED</code> - 엔티티가 목록에 성공적으로 추가되었습니다.</li>
    <li><code>UNCHANGED</code> - 엔티티가 이미 목록에 존재합니다(변경 없음).</li>
    <li><code>UPDATED</code> - 엔티티가 존재하며 API에 의해 업데이트되었습니다.</li>
    <li><code>ERROR_BAD_ID</code> - 잘못된 입력 형식 또는 유효하지 않은 엔티티 참조입니다.</li>
    <li><code>ERROR_NOT_FOUND</code> - 일치하는 엔티티를 찾을 수 없습니다.</li>
    <li><code>ERROR_NOT_ALLOWED</code> - 지정된 목록에서 해당 엔티티 유형이 허용되지 않습니다.</li>
    <li><code>ERROR_MULTIPLE_MATCHES</code> - 입력이 여러 엔티티와 일치합니다. <strong>엔티티가 추가되지 않았습니다.</strong></li>
    <li><code>LIST_MAX_SIZE_REACHED</code> - 지정된 목록이 가득 찼으며 더 이상 엔티티를 추가할 수 없습니다.</li>
</ul>

<h3 class="commands-reference"><code>ERROR_MULTIPLE_MATCHES</code> 해결 방법</h3>

<p><code>ERROR_MULTIPLE_MATCHES</code>가 표시되면 제공된 엔티티 이름이 모호합니다. API가 정확한 단일 엔티티를 선택할 수 없어 해당 항목이 건너뛰어지고 추가되지 않습니다.</p>

<p>권장 워크플로:</p>
<ol>
    <li>명령어 출력에서 모호한 값을 확인합니다.</li>
    <li><code>banshee entity search</code>를 실행하여 의도한 정확한 엔티티를 찾습니다. 필요한 경우 검색어의 이름 표기 방식(예: 다른 철자, 띄어쓰기, 더 구체적인 변형)을 조정하여 결과를 좁힙니다.</li>
    <li>입력 파일에서 모호한 값을 정확한 엔티티 ID로 교체합니다.</li>
    <li>수정된 파일로 <code>banshee list bulk-add</code>를 다시 실행합니다.</li>
</ol>

<p>예시:</p>
<pre><code class="language-bash">
banshee entity search wannacry --type Malware
banshee list bulk-add LIST_ID &lt; entities.txt
</code></pre>

<p>팁: 엔티티 ID(예: <code>SoA6SP</code>)를 이미 알고 있다면 모호성을 피하기 위해 대량 파일에서 이름/유형 쌍 대신 ID를 사용하는 것을 권장합니다.</p>

### banshee list remove

목록에서 엔티티를 제거합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list remove [OPTIONS] LIST_ID ENTITY_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--list-id"><a href="#banshee-list-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>제거할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
    <dt id="banshee-list-remove--entity-id"><a href="#banshee-list-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>목록에서 제거할 엔티티 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--help"><a href="#banshee-list-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list bulk-remove

목록에서 여러 엔티티를 제거합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list bulk-remove [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--list-id"><a href="#banshee-list-bulk-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>제거할 목록 ID</p>
    <p>목록 ID는 '<strong>report:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
    <dt id="banshee-list-bulk-remove--entity-input"><a href="#banshee-list-bulk-remove--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>공백 또는 줄 바꿈으로 구분된 하나 이상의 엔티티, 예:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>이 명령어는 stdin에서도 입력을 허용합니다. 'entities.txt'가 줄 바꿈으로 구분된 엔티티 파일이라고 가정합니다. 예:</p>
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
    <p>위를 참고하여 다음 명령어 중 하나를 실행하여 엔티티를 대량 제거할 수 있습니다:</p>
    <pre><code>
    $ banshee list bulk-remove LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-remove LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--help"><a href="#banshee-list-bulk-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee list copy

한 목록에서 다른 목록으로 엔티티를 복사하는 유틸리티 명령어입니다.

소스 목록의 엔티티를 읽어 대상 목록에 추가합니다. 기본적으로 새 엔티티는 대상의 기존 내용을 건드리지 않고 추가됩니다. `--overwrite`를 사용하면 대상이 소스를 미러링하도록 만들어집니다. 두 목록 모두에 있는 엔티티는 유지되고, 새 엔티티는 추가되며, 소스에 **없는** 대상 엔티티는 제거됩니다.

소스 목록이 비어 있으면 `--overwrite`를 사용하더라도 대상을 수정하지 않고 명령어가 종료됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee list copy [OPTIONS] SOURCE_LIST_ID DESTINATION_LIST_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--source-list-id"><a href="#banshee-list-copy--source-list-id"><code>SOURCE_LIST_ID</code></a></dt><dd>
    <p>엔티티를 복사할 소스 목록 ID</p></dd>
    <dt id="banshee-list-copy--destination-list-id"><a href="#banshee-list-copy--destination-list-id"><code>DESTINATION_LIST_ID</code></a></dt><dd>
    <p>엔티티를 복사할 대상 목록 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--overwrite"><a href="#banshee-list-copy--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>덮어쓰기 모드: 대상 목록에 이미 있는 엔티티는 유지하고, 새 엔티티는 추가하며, 소스 목록에 없는 대상 엔티티는 제거합니다. 기본적으로 명령어는 기존 엔티티를 제거하지 않고 새 엔티티를 추가합니다.</p></dd>
    <dt id="banshee-list-copy--help"><a href="#banshee-list-copy--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">예시</h3>

```
$ banshee list copy 1b0s1q 21YKUC
$ banshee list copy 1b0s1q 21YKUC --overwrite
```

## banshee pba

Recorded Future Playbook Alerts 검색, 조회 및 업데이트

<h3 class="commands-reference">사용법</h3>

```
banshee pba [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pba-lookup"><code>banshee pba lookup</code></a></dt><dd><p>Playbook Alert 조회</p></dd>
    <dt><a href="#banshee-pba-search"><code>banshee pba search</code></a></dt><dd><p>Playbook Alerts 검색</p></dd>
    <dt><a href="#banshee-pba-update"><code>banshee pba update</code></a></dt><dd><p>하나 이상의 Playbook Alert 업데이트</p></dd>
    <dt><a href="#banshee-pba-export"><code>banshee pba export</code></a></dt><dd><p>Playbook Alerts를 JSON 또는 CSV로 내보내기</p></dd>
</dl>

### banshee pba lookup

Playbook Alert를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee pba lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--alert-id"><a href="#banshee-pba-lookup--alert-id"<code>ALERT_ID</code></a></dt><dd><p>조회할 Alert ID</p>
    <p>Alert ID는 '<strong>task:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--pretty"><a href="#banshee-pba-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-pba-lookup--help"><a href="#banshee-pba-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee pba search

Playbook Alerts를 검색합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee pba search [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-search--created"><a href="#banshee-pba-search--created"><code>--created</code>, <code>-C</code></a> <i>created-from</i></dt><dd>
    <p>생성 시간 기준으로 필터링, 예: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--updated"><a href="#banshee-pba-search--updated"><code>--updated</code>, <code>-u</code></a> <i>updated-from</i></dt><dd>
    <p>업데이트 시간 기준으로 필터링, 예: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--category"><a href="#banshee-pba-search--category"><code>--category</code>, <code>-c</code></a> <i>category</i></dt><dd>
    <p>알림 카테고리로 필터링 (반복 가능)</p>
    <p>지원 카테고리:</p>
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
    <p>알림 우선순위로 필터링 (반복 가능)</p>
    <p>가능한 값: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p>
    <p>기본값: 모든 우선순위</p><dd></dd>
    <dt id="banshee-pba-search--status"><a href="#banshee-pba-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>알림 상태로 필터링 (반복 가능)</p>
    <p>가능한 값: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p>
    <p>기본값: 모든 상태</p><dd></dd>
    <dt id="banshee-pba-search--entity"><a href="#banshee-pba-search--entity"><code>--entity</code></a>,  <code>-e</code> <i>entity</i></dt><dd>
    <p>연관된 엔티티로 알림 필터링 (반복 가능), 예: <code>-e idn:recordedfuture.com -e idn:example.com</code></p><dd></dd>
    <dt id="banshee-pba-search--org-id"><a href="#banshee-pba-search--org-id"><code>--org-id</code></a>,  <code>-o</code> <i>organisation-id</i></dt><dd>
    <p>소유 조직 ID로 알림 필터링 (반복 가능)</p>
    <p>10자리 ID 또는 16자리 <code>uhash:</code> 형식을 허용합니다. 예: <code>-o 69sKLfTGsS -o uhash:5zQaSyRpA1</code></p><dd></dd>
    <dt id="banshee-pba-search--limit"><a href="#banshee-pba-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>결과 수 제한</p>
    <p>최대 제한: 10,000</p>
    <p>기본값: 100</p><dd></dd>
    <dt id="banshee-pba-search--pretty"><a href="#banshee-pba-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-pba-search--help"><a href="#banshee-pba-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

### banshee pba update

하나 이상의 Playbook Alert를 업데이트합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee pba update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--alert-id"><a href="#banshee-pba-update--alert-id"<code>ALERT_IDS</code></a></dt><dd>
    <p>공백으로 구분된 하나 이상의 Alert ID</p>
    <p>Alert ID는 '<strong>task:</strong>' 접두사 포함 여부와 관계없이 입력 가능합니다.</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--status"><a href="#banshee-pba-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>알림을 지정한 상태로 업데이트</p>
    <p>가능한 값: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-pba-update--reopen"><a href="#banshee-pba-update--reopen"><code>--reopen</code></a>,  <code>-r</code> <i>reopen</i></dt><dd>
    <p>재오픈 전략은 Dismissed 또는 Resolved 상태의 알림에만 적용할 수 있습니다. 허용되는 status/reopen 조합은 다음과 같습니다: <code>Dismissed -> Never</code>; <code>Resolved -> Never</code>; <code>Resolved -> SignificantUpdates</code></p>
    <p>지원 값: <code>Never</code>, <code>SignificantUpdates</code></p><dd></dd>
    <dt id="banshee-pba-update--priority"><a href="#banshee-pba-update--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>새 알림 우선순위 설정</p>
    <p>가능한 값: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p><dd></dd>
    <dt id="banshee-pba-update--comment"><a href="#banshee-pba-update--comment"><code>--comment</code></a>,  <code>-t</code> <i>comment</i></dt><dd>
    <p>알림에 추가할 코멘트, 예: "Bulk resolved via banshee"</p><dd></dd>
    <dt id="banshee-pba-update--assignee"><a href="#banshee-pba-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>알림을 할당할 새 사용자. 사용자의 uhash를 허용합니다. 예: uhash:3aXZxdkM12</p><dd></dd>
    <dt id="banshee-pba-update--help"><a href="#banshee-pba-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<p>하나 이상의 Alert ID(공백으로 구분)를 제공하고 원하는 업데이트 옵션을 지정합니다:</p>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Dismissed
banshee pba update ALERT_ID -s InProgress -p High -t "Escalated due to new findings"
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved -a uhash:3aXZxdkM12
</code></pre>

<h3 class="commands-reference">Alert ID 입력 방법</h3>

<h4>1. 인수로 직접 입력 (단일 또는 복수):</h4>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved
</code></pre>

<h4>2. 파일 또는 표준 입력에서 읽기:</h4>

<p>한 줄에 하나의 Alert ID가 있는 파일(예: <code>alerts.txt</code>)이 있는 경우:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>다음 명령어로 목록에 있는 모든 알림을 업데이트할 수 있습니다:</p>

<pre><code class="language-bash">
banshee pba update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee pba update -s Dismissed
</code></pre>

<h4>3. 검색 명령어에서 파이프로 연결:</h4>

<p><code>jq</code>와 같은 도구를 사용하여 검색 결과에서 Alert ID를 추출하고 업데이트 명령어로 파이프합니다:</p>

<pre><code class="language-bash">
banshee pba search | jq -r '.data[].playbook_alert_id' | banshee pba update -p High -t "Investigation started"
</code></pre>

<h3 class="commands-reference">추가 사용 예시</h3>

<pre><code class="language-bash">
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved
banshee pba update ALERT_ID -s Resolved -r Never
banshee pba update ALERT_ID_1 ALERT_ID_2 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
banshee pba update ALERT_ID -a
</code></pre>

### banshee pba export

Playbook Alerts를 JSON 또는 CSV로 내보냅니다. 일반적으로 [`banshee pba search`](#banshee-pba-search)에서 파이프로 연결하여 stdin에서 Alert ID와 카테고리를 읽습니다.

<h3 class="commands-reference">출력 형식</h3>

<p><b>JSON (기본값)</b> — Recorded Future API가 반환하는 각 ID의 <i>전체</i> 알림 객체를 출력합니다. 모든 최상위 필드와 중첩된 패널 상태, 대상, 증거, 담당자, 타임스탬프 등이 포함됩니다. 다운스트림 도구, <code>jq</code> 파이프라인 또는 재수집에 적합합니다.</p>

<p><b>CSV (<a href="#banshee-pba-export--csv"><code>--csv</code></a>)</b> — 스프레드시트 및 보고용으로 설계된 요약 정보를 출력합니다. 아래에 나열된 12개 열만 작성되며(헤더 행 포함), JSON 응답에 있는 다른 모든 필드는 제외됩니다.</p>

| 필드 | 설명 |
|---|---|
| `ID` | Playbook Alert ID (`task:` 접두사 포함) |
| `Priority` | 알림 우선순위, 예: `Informational`, `Moderate`, `High` |
| `Alert Rule` | 트리거된 알림 규칙의 이름 (없으면 규칙 레이블로 대체) |
| `Status` | 알림 상태, 예: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `Created` | 생성 타임스탬프 (UTC, `%Y-%m-%d %H:%M:%S`) |
| `Updated` | 마지막 업데이트 타임스탬프 (UTC, `%Y-%m-%d %H:%M:%S`) |
| `Subject` | 알림 제목 |
| `Assignee` | 담당자 표시 이름 |
| `Assessments` | 알림에 대한 위험 평가/규칙 (카테고리에 따라 다름), `;`로 구분 |
| `Entities` | 중복 제거된 대상 엔티티 이름, `;`로 구분 |
| `Reopen Strategy` | 종료된 알림의 재오픈 전략, 예: `Never`, `SignificantUpdates` |
| `Onwards Actions` | 알림에 수행된 조치, `;`로 구분 |

<h3 class="commands-reference">사용법</h3>

```
banshee pba search [SEARCH_OPTIONS] | banshee pba export [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-export--csv"><a href="#banshee-pba-export--csv"><code>--csv</code></a></dt><dd>
    <p>위에서 설명한 고정 열 집합으로 CSV 형식으로 출력합니다. 이 플래그가 없으면 JSON으로 출력됩니다.</p><dd></dd>
    <dt id="banshee-pba-export--help"><a href="#banshee-pba-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">파이프 입력</h3>

<p><code>banshee pba export</code>는 파이프 입력만 허용합니다. <a href="#banshee-pba-search"><code>banshee pba search</code></a>가 생성한 JSON 객체를 소비하여 각 알림의 <code>playbook_alert_id</code>와 <code>category</code>를 추출하고, 모든 알림을 전체 내용으로 가져옵니다. 파이프 없이 명령어를 실행하면 오류가 발생합니다.</p>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee pba search --created 1d | banshee pba export
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export > identity_alerts.json
banshee pba search --created 1d --category domain_abuse | banshee pba export --csv > domain_alerts.csv
</code></pre>


## banshee pcap

패킷 캡처(pcap)를 Recorded Future 인텔리전스로 보강합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee pcap [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pcap-enrich"><code>banshee pcap enrich</code></a></dt><dd><p>패킷 캡처(pcap) 파일을 Recorded Future 인텔리전스로 보강</p></dd>
</dl>

### banshee pcap enrich

이 명령어는 pcap 파일을 파싱하여 IP 주소 및 도메인과 같은 네트워크 지표를 추출한 후 위협 인텔리전스 데이터로 보강합니다. 기본적으로 결과는 위험 점수 임계값을 충족하는 지표만 표시되도록 필터링됩니다. 위험 점수 임계값 미만이더라도 위협 행위자와 연결된 지표를 포함하려면 `--threat-hunt`를 사용하십시오.
<br>위험 점수 임계값을 낮추거나 위협 헌팅을 활성화하면 결과 수와 처리 시간이 크게 증가할 수 있습니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">JSON 출력</h3>

JSON 배열의 각 결과 객체에는 다음 필드가 포함됩니다:

| 필드 | 설명 |
|---|---|
| `ioc` | pcap에서 추출된 네트워크 지표 — IP 주소 또는 도메인 이름 |
| `risk_score` | Recorded Future 위험 점수 |
| `most_malicious_rule` | 위험 점수에 기여한 가장 높은 심각도 위험 규칙의 이름 |
| `rule_evidence` | 개별 위험 규칙 증거 세부 정보 배열, 심각도 높은 순으로 정렬 |
| `ta_names` | 이 IOC와 연관된 위협 행위자 이름 목록. 없으면 빈 값 |
| `malwares` | 이 IOC와 연결된 악성코드 패밀리 이름 목록. 없으면 빈 값 |
| `wireshark_query` | 이 IOC의 트래픽을 격리하기 위해 바로 붙여넣을 수 있는 Wireshark 디스플레이 필터 |

`rule_evidence` 배열의 각 객체에는 다음이 포함됩니다:

| 필드 | 설명 |
|---|---|
| `count` | 이 위험 규칙에 대한 참조를 제공한 소스 수 |
| `description` | 증거에 대한 사람이 읽을 수 있는 요약 |
| `level` | 이 규칙의 심각도 수준 — 숫자가 높을수록 더 심각 |
| `mitigation` | IOC가 포함될 수 있는 화이트리스트를 설명하며, 이는 관련 위험을 줄이거나 완화합니다. |
| `rule` | 트리거된 특정 Recorded Future 위험 규칙의 이름 |
| `sightings` | 기록된 개별 관측 수 |
| `timestamp` | 이 규칙에 대한 가장 최근 관측 시각의 ISO 8601 타임스탬프 |
| `type` | 유형 식별자 |

<h3 class="commands-reference">사용법</h3>


```
banshee pcap enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--file-path"><a href="#banshee-pcap-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>보강할 pcap 파일 경로</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--risk-score"><a href="#banshee-pcap-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>이 임계값보다 높은 위험 점수(1 - 99)를 가진 지표만 결과로 표시<p>기본값: 65</p></p></dd>
    <dt id="banshee-pcap-enrich--threat-hunt"><a href="#banshee-pcap-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>위험 점수 임계값에 관계없이 위협 행위자와 연결된 지표 포함 (소급 위협 헌팅)</p></dd>
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p><dd></dd>
    <dt id="banshee-pcap-enrich--help"><a href="#banshee-pcap-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

## banshee risklist

Risk List를 관리합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee risklist [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-risklist-create"><code>banshee risklist create</code></a></dt><dd><p>하나 이상의 위험 규칙을 결합하여 사용자 지정 risk list 생성</p></dd>
    <dt><a href="#banshee-risklist-fetch"><code>banshee risklist fetch</code></a></dt><dd><p>risk list 다운로드</p></dd>
    <dt><a href="#banshee-risklist-stat"><code>banshee risklist stat</code></a></dt><dd><p>risk list 메타데이터 표시 (etag 및 타임스탬프)</p></dd>
</dl>

### banshee risklist create

하나 이상의 Recorded Future 위험 규칙을 하나의 중복 제거된 파일로 결합하여 사용자 지정 risk list를 생성합니다.

각 `--risk-rule`에 대해 항목을 가져오고, IOC 기준으로 병합하며(첫 번째 발생이 우선), 선택적으로 최소 `--risk-score`로 필터링합니다. 출력은 위험 점수 내림차순으로 정렬되며, 선택한 형식으로 작성됩니다 — 방화벽, SIEM 또는 기타 통합에 바로 사용할 수 있습니다.

출력은 기본적으로 로컬 파일에 저장됩니다. `--fusion`과 `--output-path`를 함께 사용하면 로컬 파일을 저장하지 않고 결과를 Recorded Future Fusion에 직접 업로드할 수 있습니다.

<h3 class="commands-reference">사용법</h3>

```
banshee risklist create [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-create--entity-type"><a href="#banshee-risklist-create--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list의 엔티티 유형. 유효한 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><strong>필수</strong></p></dd>
    <dt id="banshee-risklist-create--risk-rule"><a href="#banshee-risklist-create--risk-rule"><code>--risk-rule</code></a>, <code>-R</code> <i>risk-rule</i></dt><dd>
    <p>포함할 위험 규칙. <code>default</code>, <code>large</code> 또는 <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a>의 규칙 이름을 사용합니다. 반복 가능 — 여러 번 지정하여 규칙을 하나의 출력으로 병합합니다.<br><strong>필수 (최소 하나)</strong></p></dd>
    <dt id="banshee-risklist-create--risk-score"><a href="#banshee-risklist-create--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>최소 위험 점수 임계값(5–99). 이 값보다 낮은 위험 점수의 항목은 출력에서 제외됩니다.</p></dd>
    <dt id="banshee-risklist-create--format"><a href="#banshee-risklist-create--format"><code>--format</code></a>, <code>-f</code> <i>format</i></dt><dd>
    <p>출력 형식. 기본값: <code>csv</code></p>
    <ul>
        <li><code>csv</code> — 헤더가 있는 쉼표 구분 형식: <code>Name</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code>. Hash 엔티티 유형에는 <code>Algorithm</code> 열이 추가됩니다: <code>Name</code>, <code>Algorithm</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code></li>
        <li><code>edl</code> — 한 줄에 하나의 IOC 값을 가진 일반 목록 (방화벽 EDL 피드에 적합). <code>.txt</code> 확장자로 저장됩니다.</li>
        <li><code>json</code> — 전체 risk list 항목의 JSON 배열</li>
    </ul></dd>
    <dt id="banshee-risklist-create--output-path"><a href="#banshee-risklist-create--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>출력 파일 경로. 파일 경로 또는 디렉토리를 허용합니다(파일 이름은 <code>custom_risklist_{entity_type}.{ext}</code>로 자동 생성됩니다). 기본값: 자동 생성된 파일 이름으로 현재 디렉토리.<br><code>--fusion</code> 사용 시 필수</p></dd>
    <dt id="banshee-risklist-create--fusion"><a href="#banshee-risklist-create--fusion"><code>--fusion</code></a>, <code>-F</code></dt><dd>
    <p><code>--output-path</code>를 대상 경로로 사용하여 결과를 Recorded Future Fusion에 직접 업로드합니다. 이 플래그가 설정되면 로컬 파일이 저장되지 않습니다.</p></dd>
    <dt id="banshee-risklist-create--help"><a href="#banshee-risklist-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

기본 규칙으로 IP용 CSV risk list 생성, 위험 점수 70 이상으로 필터링

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
```

두 도메인 규칙을 하나의 중복 제거된 CSV로 병합, 위험 점수 80 이상으로 필터링

```bash
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
```

두 IP 규칙을 병합하여 EDL(일반 IOC 목록) 형식으로 출력

```bash
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
```

두 규칙에서 해시용 JSON risk list 생성 후 특정 로컬 파일 경로로 출력

```bash
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
```

risk list 생성 후 Recorded Future Fusion에 직접 업로드

```bash
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

### banshee risklist fetch

특정 엔티티 유형 및 목록 이름에 대한 risk list를 다운로드하거나, 사용자 지정 risk list 파일을 사용합니다.

엔티티 유형(`--entity-type`)과 목록 이름(`--list-name`)을 지정하여 Recorded Future에서 risk list를 다운로드할 수 있습니다. 사용 가능한 목록 이름으로는 `default`, `large` 또는 `banshee ioc rules`의 규칙 이름이 있습니다. Recorded Future Risk Rules에 대한 자세한 내용은 [Risk Scoring in Recorded Future](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future) 지원 문서를 참조하십시오.

또는 `--custom-list-path`를 사용하여 사용자 지정 risk list 파일 경로를 직접 지정할 수 있습니다.

<h3 class="commands-reference">사용법</h3>

```
banshee risklist fetch [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-fetch--entity-type"><a href="#banshee-risklist-fetch--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list의 엔티티 유형. 유효한 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><code>--list-name</code> 사용 시 필수</p></dd>
    <dt id="banshee-risklist-fetch--list-name"><a href="#banshee-risklist-fetch--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>risk list 이름: <code>default</code>, <code>large</code> 또는 <code>banshee ioc rules</code>의 규칙 이름<br><code>--entity-type</code> 사용 시 필수</p></dd>
    <dt id="banshee-risklist-fetch--custom-list-path"><a href="#banshee-risklist-fetch--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>사용자 지정 risk list 파일 경로. <code>--entity-type</code> 또는 <code>--list-name</code>과 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-risklist-fetch--output-path"><a href="#banshee-risklist-fetch--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>출력 파일 경로. 기본값: 자동 생성된 파일 이름으로 현재 디렉토리</p></dd>
    <dt id="banshee-risklist-fetch--as-json"><a href="#banshee-risklist-fetch--as-json"><code>--as-json</code></a>, <code>-j</code></dt><dd>
    <p>risk list를 JSON 형식으로 변환합니다. <code>--list-name</code> 및 <code>--entity-type</code>과 함께만 사용 가능합니다.</p></dd>
    <dt id="banshee-risklist-fetch--help"><a href="#banshee-risklist-fetch--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
# IP 주소에 대한 기본 risk list 다운로드
banshee risklist fetch -e ip -l default

# 도메인의 large risk list를 JSON으로 다운로드
banshee risklist fetch -e domain -l large -j

# Insikt Group Note에 포함된 해시에 대한 risk list 다운로드
banshee risklist fetch -e hash -l analystNote

# 사용자 지정 risk list 파일 다운로드
banshee risklist fetch -c /path/to/custom_risklist.csv

# URL의 기본 risklist를 다운로드하고 특정 출력 경로에 저장
banshee risklist fetch -e url -l default -o /tmp/rf_default_url_risklist.csv
</code></pre>

### banshee risklist stat

etag 및 타임스탬프 정보를 포함한 risk list 메타데이터를 표시합니다.

이 명령어는 전체 목록 내용을 다운로드하지 않고 risk list의 메타데이터를 조회합니다. risk list가 마지막으로 업데이트된 시간을 확인하는 데 사용할 수 있습니다.

<h3 class="commands-reference">사용법</h3>

```
banshee risklist stat [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-stat--entity-type"><a href="#banshee-risklist-stat--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>risk list의 엔티티 유형. 유효한 값: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><code>--list-name</code> 사용 시 필수</p></dd>
    <dt id="banshee-risklist-stat--list-name"><a href="#banshee-risklist-stat--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>risk list 이름: <code>default</code>, <code>large</code> 또는 <code>banshee ioc rules</code>의 규칙 이름<br><code>--entity-type</code> 사용 시 필수</p></dd>
    <dt id="banshee-risklist-stat--custom-list-path"><a href="#banshee-risklist-stat--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>사용자 지정 risk list 파일 경로. <code>--entity-type</code> 또는 <code>--list-name</code>과 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-risklist-stat--pretty"><a href="#banshee-risklist-stat--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-risklist-stat--count"><a href="#banshee-risklist-stat--count"><code>--count</code></a>, <code>-C</code></dt><dd>
    <p>risk list 전체의 IOC 수 및 위험 점수 분포를 표시합니다.</p></dd>
    <dt id="banshee-risklist-stat--help"><a href="#banshee-risklist-stat--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
# 기본 IP risk list의 메타데이터 확인
banshee risklist stat -e ip -l default

# 보기 좋은 형식으로 메타데이터 확인
banshee risklist stat -e domain -l large -p

# 사용자 지정 risk list 파일의 메타데이터 확인
banshee risklist stat -c /path/to/custom_risklist.txt

# 기본 IP risk list의 위험 점수별 지표 수 집계 후 보기 좋게 출력
banshee risklist stat -e ip -l default -Cp
</code></pre>

## banshee rules

탐지 규칙을 검색하고 다운로드합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee rules [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-rules-search"><code>banshee rules search</code></a></dt><dd><p>필터 옵션을 기반으로 탐지 규칙 검색</p></dd>
</dl>

### banshee rules search

제공된 필터 옵션을 기반으로 탐지 규칙을 검색합니다. 결과는 콘솔에 표시하거나 개별 규칙 파일로 디스크에 저장할 수 있습니다.

탐지 규칙은 유형(YARA, Snort, Sigma), 연관된 엔티티(위협 행위자, 악성코드, MITRE ATT&CK 기법), 생성/업데이트 날짜 등으로 필터링할 수 있습니다. `--threat-actor-map` 또는 `--threat-malware-map`을 사용하면 Threat Map의 엔티티를 기반으로 규칙을 자동으로 필터링합니다.

결과는 기본적으로 10개로 제한됩니다. 최대 1000개의 규칙을 검색하려면 `--limit` 옵션을 사용하십시오.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee rules search [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-rules-search--type"><a href="#banshee-rules-search--type"><code>--type</code></a>, <code>-t</code> <i>type</i></dt><dd>
    <p>규칙 유형으로 필터링. 유효한 값: <code>yara</code>, <code>snort</code>, <code>sigma</code><br>여러 유형을 지정할 수 있으며 논리적 OR로 동작합니다(예: <code>-t yara -t snort</code>는 두 유형 중 하나에 일치하는 규칙을 반환).</p></dd>
    <dt id="banshee-rules-search--threat-actor-map"><a href="#banshee-rules-search--threat-actor-map"><code>--threat-actor-map</code></a>, <code>-T</code></dt><dd>
    <p>Threat Actor Map의 위협 행위자를 기반으로 규칙 필터링. 활성화되면 Threat Actor Map의 행위자와 연관된 탐지 규칙이 반환됩니다.</p></dd>
    <dt id="banshee-rules-search--threat-actor-category"><a href="#banshee-rules-search--threat-actor-category"><code>--threat-actor-category</code></a>, <code>-C</code> <i>category</i></dt><dd>
    <p>Threat Actor Map의 위협 행위자 카테고리로 필터링. 여러 카테고리를 지정할 수 있으며 논리적 OR로 동작합니다(예: <code>-C nation_state_sponsored -C ransomware_and_extortion_groups</code>).</p></dd>
    <dt id="banshee-rules-search--threat-malware-map"><a href="#banshee-rules-search--threat-malware-map"><code>--threat-malware-map</code></a>, <code>-M</code></dt><dd>
    <p>Malware Threat Map의 악성코드를 기반으로 규칙 필터링. 활성화되면 Malware Threat Map의 악성코드와 연관된 탐지 규칙이 반환됩니다.</p></dd>
    <dt id="banshee-rules-search--org-id"><a href="#banshee-rules-search--org-id"><code>--org-id</code></a>, <code>-O</code> <i>org-id</i></dt><dd>
    <p>Threat Map에서 위협 행위자를 가져올 때 조직 ID를 지정합니다(<code>--threat-actor-map</code> 또는 <code>--threat-malware-map</code> 필요). <code>uhash:</code> 접두사 포함 여부와 관계없이 허용됩니다. MSSP 및 다중 조직 계정에 유용합니다.</p></dd>
    <dt id="banshee-rules-search--entity"><a href="#banshee-rules-search--entity"><code>--entity</code></a>, <code>-e</code> <i>entity</i></dt><dd>
    <p>탐지 규칙과 연관된 Recorded Future 엔티티 ID로 필터링. 여러 엔티티를 지정할 수 있으며 논리적 OR로 동작합니다. 엔티티 ID를 찾으려면 <code>banshee entity search</code>를 사용하십시오(예: IsaacWiper 악성코드의 경우 <code>lzQ5GL</code>, Data Encrypted for Impact의 경우 <code>mitre:T1486</code>).</p></dd>
    <dt id="banshee-rules-search--created-after"><a href="#banshee-rules-search--created-after"><code>--created-after</code></a>, <code>-a</code> <i>time</i></dt><dd>
    <p>지정한 시간 이후에 생성된 탐지 규칙 필터링. 상대 시간(예: <code>1d</code>, <code>3d</code>, <code>7d</code>) 또는 절대 날짜(예: <code>2024-01-01</code>) 허용.</p></dd>
    <dt id="banshee-rules-search--created-before"><a href="#banshee-rules-search--created-before"><code>--created-before</code></a>, <code>-b</code> <i>time</i></dt><dd>
    <p>지정한 시간 이전에 생성된 탐지 규칙 필터링. 상대 시간(예: <code>1d</code>, <code>3d</code>, <code>7d</code>) 또는 절대 날짜(예: <code>2024-01-01</code>) 허용.</p></dd>
    <dt id="banshee-rules-search--updated-after"><a href="#banshee-rules-search--updated-after"><code>--updated-after</code></a>, <code>-u</code> <i>time</i></dt><dd>
    <p>지정한 시간 이후에 업데이트된 탐지 규칙 필터링. 상대 시간(예: <code>1d</code>, <code>3d</code>, <code>7d</code>) 또는 절대 날짜(예: <code>2024-01-01</code>) 허용.</p></dd>
    <dt id="banshee-rules-search--updated-before"><a href="#banshee-rules-search--updated-before"><code>--updated-before</code></a>, <code>-U</code> <i>time</i></dt><dd>
    <p>지정한 시간 이전에 업데이트된 탐지 규칙 필터링. 상대 시간(예: <code>1d</code>, <code>3d</code>, <code>7d</code>) 또는 절대 날짜(예: <code>2024-01-01</code>) 허용.</p></dd>
    <dt id="banshee-rules-search--id"><a href="#banshee-rules-search--id"><code>--id</code></a>, <code>-i</code> <i>document-id</i></dt><dd>
    <p>탐지 규칙과 연관된 특정 Insikt Note 문서 ID로 필터링(예: <code>doc:lmRPGB</code>).</p></dd>
    <dt id="banshee-rules-search--title"><a href="#banshee-rules-search--title"><code>--title</code></a>, <code>-n</code> <i>title</i></dt><dd>
    <p>연관된 Insikt Note 제목으로 탐지 규칙을 자유 텍스트 검색</p></dd>
    <dt id="banshee-rules-search--limit"><a href="#banshee-rules-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>반환할 탐지 규칙의 최대 수<p>기본값: 10</p></p></dd>
    <dt id="banshee-rules-search--output-path"><a href="#banshee-rules-search--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>탐지 규칙을 지정한 디렉토리에 저장합니다. 상대 경로 또는 절대 경로를 사용할 수 있습니다. 지정하지 않으면 결과가 콘솔에 출력됩니다.</p></dd>
    <dt id="banshee-rules-search--pretty"><a href="#banshee-rules-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-rules-search--help"><a href="#banshee-rules-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
# 최근 7일 이내에 생성된 YARA 규칙 검색
banshee rules search -t yara -a 7d

# Threat Map의 위협 행위자와 연관된 규칙 검색 후 보기 좋게 출력
# --limit 기본값이 10이므로 처음 10개의 일치 규칙이 반환됩니다.
banshee rules search -Tp

# 위협 행위자 및 악성코드 맵 결합
banshee rules search -TMp

# 특정 엔티티 ID로 규칙 검색 (예: IsaacWiper 악성코드)
banshee rules search -e lzQ5GL -p

# 최근 3일 이내에 업데이트된 Snort 및 Sigma 규칙 검색 후 디렉토리에 저장
banshee rules search -t snort -t sigma -u 3d -o ./detection_rules

# Insikt Note 제목으로 검색
banshee rules search --title "APT28" -p
</code></pre>

## banshee sandbox

샌드박스 제출 분석 및 프로파일 관리.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-stats"><code>banshee sandbox stats</code></a></dt><dd><p>설정 가능한 기간 동안의 샌드박스 제출을 집계하여 SOC 모닝 브리핑을 출력</p></dd>
    <dt><a href="#banshee-sandbox-list"><code>banshee sandbox list</code></a></dt><dd><p>샌드박스 샘플 목록 조회</p></dd>
    <dt><a href="#banshee-sandbox-search"><code>banshee sandbox search</code></a></dt><dd><p>해시, 패밀리, 태그, 봇넷, 지갑, 네트워크 지표 또는 원시 Triage 쿼리로 샘플 검색</p></dd>
    <dt><a href="#banshee-sandbox-get"><code>banshee sandbox get</code></a></dt><dd><p>ID로 단일 샌드박스 샘플 요약 조회</p></dd>
    <dt><a href="#banshee-sandbox-download"><code>banshee sandbox download</code></a></dt><dd><p>하나 이상의 샘플 ID에 대한 원본 제출 바이트를 다운로드 (AES 암호화 ZIP 아카이브로 래핑)</p></dd>
    <dt><a href="#banshee-sandbox-delete"><code>banshee sandbox delete</code></a></dt><dd><p>ID로 샌드박스 샘플 삭제</p></dd>
    <dt><a href="#banshee-sandbox-submit"><code>banshee sandbox submit</code></a></dt><dd><p>파일, URL 또는 공개 샘플을 샌드박스 분석을 위해 제출</p></dd>
    <dt><a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a></dt><dd><p>정적 분석에서 일시 중지된 샘플에 분석 프로파일 할당</p></dd>
    <dt><a href="#banshee-sandbox-profile"><code>banshee sandbox profile</code></a></dt><dd><p>분석 프로파일 관리</p></dd>
    <dt><a href="#banshee-sandbox-report"><code>banshee sandbox report</code></a></dt><dd><p>샘플 분석 보고서</p></dd>
</dl>

### banshee sandbox stats

설정 가능한 기간 동안의 샌드박스 제출을 집계하여 SOC 교대 인수인계 또는 일일 트리아지에 적합한 "모닝 브리핑"을 출력합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">점수 버킷</h3>

<p>샌드박스는 샘플을 1–10 트리아지 척도로 점수를 매깁니다. 결과는 다음 버킷으로 그룹화됩니다:</p>

| 버킷 | 점수 범위 | 의미 |
|---|---|---|
| `malicious` | 8–10 | 알려진 악성코드, 높은 신뢰도 |
| `suspicious` | 5–7 | 강한 행위 기반 지표 |
| `potentially_suspicious` | 3–4 | 일부 지표 존재 |
| `clean` | 1–2 | 낮은 위험 또는 양성 |

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox stats [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-stats--days"><a href="#banshee-sandbox-stats--days"><code>--days</code></a>, <code>-d</code> <i>days</i></dt><dd>
    <p>조회 기간(일 단위)</p>
    <p>기본값: 7</p></dd>
    <dt id="banshee-sandbox-stats--subset"><a href="#banshee-sandbox-stats--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>집계할 샘플 범위</p>
    <p>가능한 값: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>기본값: <code>org</code></p></dd>
    <dt id="banshee-sandbox-stats--pretty"><a href="#banshee-sandbox-stats--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-stats--help"><a href="#banshee-sandbox-stats--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats --days 30 --pretty
</code></pre>

### banshee sandbox list

샌드박스 샘플을 나열합니다 — 본인 소유, 조직 소유(기본값), 또는 공개 피드.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox list [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-list--subset"><a href="#banshee-sandbox-list--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>나열할 샘플 범위</p>
    <p>가능한 값: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>기본값: <code>org</code></p></dd>
    <dt id="banshee-sandbox-list--limit"><a href="#banshee-sandbox-list--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>반환할 샘플의 최대 수</p>
    <p>허용 범위: 1–4095</p>
    <p>기본값: 20</p></dd>
    <dt id="banshee-sandbox-list--pretty"><a href="#banshee-sandbox-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-list--help"><a href="#banshee-sandbox-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
</code></pre>

### banshee sandbox search

구조화된 필터(해시, 패밀리, 태그, 봇넷, 지갑, IP, 도메인, URL, 제출 날짜 범위) 또는 원시 Triage 쿼리에 일치하는 샘플을 검색합니다. 최소 하나의 필터 또는 `--query`를 제공해야 합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox search [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-search--hash"><a href="#banshee-sandbox-search--hash"><code>--hash</code></a> <i>hash</i></dt><dd>
    <p>파일 해시(MD5/SHA1/SHA256)로 필터링</p></dd>
    <dt id="banshee-sandbox-search--family"><a href="#banshee-sandbox-search--family"><code>--family</code></a> <i>family</i></dt><dd>
    <p>악성코드 패밀리 이름으로 필터링</p></dd>
    <dt id="banshee-sandbox-search--tag"><a href="#banshee-sandbox-search--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>태그로 필터링 (반복 가능)</p></dd>
    <dt id="banshee-sandbox-search--botnet"><a href="#banshee-sandbox-search--botnet"><code>--botnet</code></a> <i>botnet</i></dt><dd>
    <p>봇넷 이름으로 필터링</p></dd>
    <dt id="banshee-sandbox-search--wallet"><a href="#banshee-sandbox-search--wallet"><code>--wallet</code></a> <i>wallet</i></dt><dd>
    <p>지갑 주소로 필터링</p></dd>
    <dt id="banshee-sandbox-search--ip"><a href="#banshee-sandbox-search--ip"><code>--ip</code></a> <i>ip</i></dt><dd>
    <p>IP 주소로 필터링</p></dd>
    <dt id="banshee-sandbox-search--domain"><a href="#banshee-sandbox-search--domain"><code>--domain</code></a> <i>domain</i></dt><dd>
    <p>도메인으로 필터링</p></dd>
    <dt id="banshee-sandbox-search--url"><a href="#banshee-sandbox-search--url"><code>--url</code></a> <i>url</i></dt><dd>
    <p>URL로 필터링</p></dd>
    <dt id="banshee-sandbox-search--from-date"><a href="#banshee-sandbox-search--from-date"><code>--from-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>이 날짜 이후에 제출된 샘플</p></dd>
    <dt id="banshee-sandbox-search--to-date"><a href="#banshee-sandbox-search--to-date"><code>--to-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>이 날짜 이전에 제출된 샘플</p></dd>
    <dt id="banshee-sandbox-search--query"><a href="#banshee-sandbox-search--query"><code>--query</code></a>, <code>-q</code> <i>query</i></dt><dd>
    <p>원시 Triage 쿼리 문자열 (구조화된 필터와 AND로 결합)</p></dd>
    <dt id="banshee-sandbox-search--limit"><a href="#banshee-sandbox-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>반환할 샘플의 최대 수 (1–200)</p>
    <p>기본값: 50</p></dd>
    <dt id="banshee-sandbox-search--pretty"><a href="#banshee-sandbox-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-search--help"><a href="#banshee-sandbox-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

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

단일 샌드박스 샘플의 요약 정보를 ID로 조회합니다: 현재 상태, 전체 점수, 대상, 생성 및 완료 타임스탬프, SHA256, 태스크별 세부 내용. 진행 중이거나 완료된 샘플 모두에 적용됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox get [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--sample-id"><a href="#banshee-sandbox-get--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>샌드박스 샘플 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--pretty"><a href="#banshee-sandbox-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-get--help"><a href="#banshee-sandbox-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
</code></pre>

### banshee sandbox download

하나 이상의 샘플 ID에 대한 원본 제출 샘플 바이트를 다운로드합니다. 각 샘플은 바이러스 백신, 보안 이메일 게이트웨이, 파일 관리자에 의한 의도치 않은 실행을 방지하기 위해 비밀번호 `infected`로 AES 암호화된 ZIP 아카이브로 래핑됩니다.

압축 해제 시 `7z x -pinfected <sample-id>.zip`을 사용하십시오 — 표준 `unzip`은 AES 암호화 ZIP을 안정적으로 처리하지 못합니다.

샘플 ID는 위치 인수로 전달하거나 stdin에서 파이프로 입력(공백 구분)할 수 있습니다. `--yes`를 지정하지 않으면 확인 프롬프트가 표시됩니다.

> **안전 참고:** 샘플 바이트는 다운로드 및 압축 과정 중 이 프로세스의 메모리에 잠깐 존재합니다. 공격적인 EDR 메모리 스캐닝이 여전히 감지할 수 있습니다. 일반 업무용 기업 노트북이 아닌 분석가 전용 장비에서 실행하십시오.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox download [OPTIONS] [SAMPLE_IDS]...
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--sample-ids"><a href="#banshee-sandbox-download--sample-ids"><code>SAMPLE_IDS</code></a></dt><dd><p>하나 이상의 샘플 ID (또는 stdin에서 공백 구분으로 읽기)</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--output-dir"><a href="#banshee-sandbox-download--output-dir"><code>--output-dir</code></a>, <code>-d</code> <i>DIR</i></dt><dd>
    <p>암호화된 ZIP 아카이브를 저장할 디렉토리 (없으면 생성됨). 필수.</p></dd>
    <dt id="banshee-sandbox-download--yes"><a href="#banshee-sandbox-download--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>확인 프롬프트 건너뛰기</p></dd>
    <dt id="banshee-sandbox-download--workers"><a href="#banshee-sandbox-download--workers"><code>--workers</code></a>, <code>-w</code> <i>N</i></dt><dd>
    <p>병렬 다운로드 워커 수 (1–16)</p>
    <p>기본값: 1</p></dd>
    <dt id="banshee-sandbox-download--help"><a href="#banshee-sandbox-download--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# 압축 해제
7z x -pinfected ./samples/260501-h4p7laawme.zip
</code></pre>

### banshee sandbox delete

ID로 샌드박스 샘플을 삭제하고 연관된 모든 태스크 아티팩트를 제거합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox delete [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--sample-id"><a href="#banshee-sandbox-delete--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>삭제할 샘플 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--yes"><a href="#banshee-sandbox-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>확인 프롬프트 건너뛰기</p></dd>
    <dt id="banshee-sandbox-delete--help"><a href="#banshee-sandbox-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
</code></pre>

### banshee sandbox submit

분석을 위해 샘플을 제출합니다. 로컬 파일은 업로드되고, URL은 브라우저에서 실행(detonation)되거나 `--fetch`로 먼저 다운로드되며, 공개 샘플은 `--import`를 사용하여 ID로 가져올 수 있습니다.

기본적으로 JSON 제출 영수증을 출력합니다. `--wait`를 사용하면 분석이 완료될 때까지 폴링한 후 개요 보고서를 출력합니다.

<h3 class="commands-reference">대상 유형</h3>

| 대상 | 동작 |
|---|---|
| 로컬 파일 경로 | 업로드 후 분석 |
| URL | 브라우저에서 실행 |
| URL + `--fetch` | 먼저 다운로드한 후 파일로 분석 |
| 공개 샘플 ID + `--import` | 조직의 샌드박스로 가져오기 |

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox submit [OPTIONS] TARGET
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--target"><a href="#banshee-sandbox-submit--target"><code>TARGET</code></a></dt><dd><p>파일 경로, URL 또는 공개 샘플 ID (<code>--import</code> 사용 시)</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--fetch"><a href="#banshee-sandbox-submit--fetch"><code>--fetch</code></a></dt><dd>
    <p>URL 대상을 먼저 다운로드한 후 결과 파일을 분석합니다. <code>--import</code>와 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-submit--import"><a href="#banshee-sandbox-submit--import"><code>--import</code></a></dt><dd>
    <p>대상을 조직으로 가져올 공개 샘플 ID로 취급합니다. <code>--fetch</code>와 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-submit--profile"><a href="#banshee-sandbox-submit--profile"><code>--profile</code></a> <i>profile</i></dt><dd>
    <p>분석 프로파일 이름 또는 ID. 여러 번 지정하여 둘 이상의 프로파일을 할당할 수 있습니다. <code>--interactive</code>와 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-submit--timeout"><a href="#banshee-sandbox-submit--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>분석 타임아웃(초 단위)</p>
    <p>허용 범위: 1–3600</p></dd>
    <dt id="banshee-sandbox-submit--network"><a href="#banshee-sandbox-submit--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>분석 환경의 네트워크 모드</p>
    <p>가능한 값: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-submit--geolocation"><a href="#banshee-sandbox-submit--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 출구 국가 코드. <code>--network vpn</code> 필요</p></dd>
    <dt id="banshee-sandbox-submit--tags"><a href="#banshee-sandbox-submit--tags"><code>--tags</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>제출에 첨부할 사용자 지정 태그. 여러 번 지정 가능</p></dd>
    <dt id="banshee-sandbox-submit--password"><a href="#banshee-sandbox-submit--password"><code>--password</code></a> <i>password</i></dt><dd>
    <p>보호된 아카이브의 비밀번호</p></dd>
    <dt id="banshee-sandbox-submit--wait"><a href="#banshee-sandbox-submit--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>분석이 완료될 때까지 폴링한 후 개요 보고서 출력</p></dd>
    <dt id="banshee-sandbox-submit--interactive"><a href="#banshee-sandbox-submit--interactive"><code>--interactive</code></a>, <code>-i</code></dt><dd>
    <p>정적 분석에서 일시 중지하여 <a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a>을 통해 파일 및 프로파일을 선택할 수 있도록 합니다. <code>--profile</code>과 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-submit--pretty"><a href="#banshee-sandbox-submit--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-submit--help"><a href="#banshee-sandbox-submit--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

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

정적 분석에서 일시 중지된 샘플(`--interactive`로 제출)에 분석 프로파일을 할당합니다. `--auto`를 사용하면 샌드박스가 자동으로 프로파일을 선택하고, `--pick`을 사용하면 특정 파일을 특정 프로파일에 수동으로 매핑할 수 있습니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox set-profile [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--sample-id"><a href="#banshee-sandbox-set-profile--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>정적 분석에서 일시 중지된 샘플의 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--auto"><a href="#banshee-sandbox-set-profile--auto"><code>--auto</code></a>, <code>-a</code></dt><dd>
    <p>모든 파일에 대해 샌드박스가 자동으로 프로파일을 선택하도록 합니다. <code>--pick</code>과 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-set-profile--pick"><a href="#banshee-sandbox-set-profile--pick"><code>--pick</code></a> <i>FILE:PROFILE</i></dt><dd>
    <p>특정 파일을 특정 프로파일에 <code>FILE:PROFILE</code> 형식으로 매핑합니다. 여러 번 지정 가능. <code>--auto</code>와 함께 사용할 수 없습니다.</p></dd>
    <dt id="banshee-sandbox-set-profile--pretty"><a href="#banshee-sandbox-set-profile--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-set-profile--help"><a href="#banshee-sandbox-set-profile--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --auto -p
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
</code></pre>

### banshee sandbox profile

분석 프로파일을 관리합니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-profile-list"><code>banshee sandbox profile list</code></a></dt><dd><p>사용 가능한 모든 분석 프로파일 목록 조회</p></dd>
    <dt><a href="#banshee-sandbox-profile-get"><code>banshee sandbox profile get</code></a></dt><dd><p>특정 프로파일의 세부 정보 조회</p></dd>
    <dt><a href="#banshee-sandbox-profile-create"><code>banshee sandbox profile create</code></a></dt><dd><p>새 분석 프로파일 생성</p></dd>
    <dt><a href="#banshee-sandbox-profile-update"><code>banshee sandbox profile update</code></a></dt><dd><p>기존 분석 프로파일 업데이트</p></dd>
    <dt><a href="#banshee-sandbox-profile-delete"><code>banshee sandbox profile delete</code></a></dt><dd><p>분석 프로파일 삭제</p></dd>
</dl>

#### banshee sandbox profile list

사용 가능한 모든 분석 프로파일을 나열합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile list [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-list--pretty"><a href="#banshee-sandbox-profile-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-profile-list--help"><a href="#banshee-sandbox-profile-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
</code></pre>

#### banshee sandbox profile get

이름 또는 ID로 특정 분석 프로파일의 세부 정보를 조회합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile get [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--profile-id-or-name"><a href="#banshee-sandbox-profile-get--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>프로파일 UUID 또는 표시 이름</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--pretty"><a href="#banshee-sandbox-profile-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-profile-get--help"><a href="#banshee-sandbox-profile-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
</code></pre>

#### banshee sandbox profile create

새 분석 프로파일을 생성합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">프로파일 태그</h3>

<p>태그는 프로파일의 운영 체제 및 환경을 정의합니다. locale 태그를 사용할 경우 반드시 하나 이상의 <code>os</code> 태그가 함께 있어야 합니다.</p>

<pre><code class="language-bash">
# OS만 지정
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64

# OS + locale 지정
banshee sandbox profile create -n my-profile -T os:windows10-2004-x64 -T locale:en-us
</code></pre>

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile create [OPTIONS]
```

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-create--name"><a href="#banshee-sandbox-profile-create--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>프로파일 표시 이름. 필수</p></dd>
    <dt id="banshee-sandbox-profile-create--tag"><a href="#banshee-sandbox-profile-create--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>프로파일 태그 (예: <code>os:windows10-2004-x64</code>, <code>locale:en-us</code>). 여러 번 지정 가능. 필수</p></dd>
    <dt id="banshee-sandbox-profile-create--timeout"><a href="#banshee-sandbox-profile-create--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>분석 타임아웃(초 단위)</p>
    <p>허용 범위: 1–3600</p>
    <p>기본값: 120</p></dd>
    <dt id="banshee-sandbox-profile-create--network"><a href="#banshee-sandbox-profile-create--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>네트워크 모드</p>
    <p>가능한 값: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-create--geolocation"><a href="#banshee-sandbox-profile-create--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 출구 국가 코드. 여러 번 지정 가능. <code>--network vpn</code> 필요</p></dd>
    <dt id="banshee-sandbox-profile-create--browser"><a href="#banshee-sandbox-profile-create--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>URL 실행에 사용할 브라우저</p>
    <p>가능한 값: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-create--pretty"><a href="#banshee-sandbox-profile-create--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-profile-create--help"><a href="#banshee-sandbox-profile-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
</code></pre>

#### banshee sandbox profile update

이름 또는 ID로 기존 분석 프로파일을 업데이트합니다. 최소 하나의 옵션을 제공해야 합니다.

출력은 `{"updated": true}` 또는 `{"updated": false}`입니다 (어느 경우든 종료 코드 0).

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile update [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--profile-id-or-name"><a href="#banshee-sandbox-profile-update--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>업데이트할 프로파일 UUID 또는 표시 이름</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--name"><a href="#banshee-sandbox-profile-update--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>새 프로파일 표시 이름</p></dd>
    <dt id="banshee-sandbox-profile-update--tag"><a href="#banshee-sandbox-profile-update--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>기존 태그를 모두 교체합니다. 여러 번 지정 가능</p></dd>
    <dt id="banshee-sandbox-profile-update--timeout"><a href="#banshee-sandbox-profile-update--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>분석 타임아웃(초 단위)</p>
    <p>허용 범위: 1–3600</p></dd>
    <dt id="banshee-sandbox-profile-update--network"><a href="#banshee-sandbox-profile-update--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>네트워크 모드</p>
    <p>가능한 값: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-update--geolocation"><a href="#banshee-sandbox-profile-update--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>VPN 출구 국가 코드. 여러 번 지정 가능. <code>--network vpn</code> 필요</p></dd>
    <dt id="banshee-sandbox-profile-update--browser"><a href="#banshee-sandbox-profile-update--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>URL 실행에 사용할 브라우저</p>
    <p>가능한 값: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-update--unset"><a href="#banshee-sandbox-profile-update--unset"><code>--unset</code></a> <i>field</i></dt><dd>
    <p>필드를 초기화합니다. 여러 번 지정 가능</p>
    <p>가능한 값: <code>network</code>, <code>browser</code>, <code>geolocation</code></p>
    <p>동일 필드에 대한 설정 옵션과 함께 사용할 수 없습니다. <code>--unset network</code>는 <code>--geolocation</code>과 충돌합니다.</p></dd>
    <dt id="banshee-sandbox-profile-update--pretty"><a href="#banshee-sandbox-profile-update--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-profile-update--help"><a href="#banshee-sandbox-profile-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
</code></pre>

#### banshee sandbox profile delete

이름 또는 ID로 분석 프로파일을 삭제합니다. 존재하지 않는 프로파일을 삭제하면 경고를 출력하고 종료 코드 0으로 종료됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox profile delete [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--profile-id-or-name"><a href="#banshee-sandbox-profile-delete--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>삭제할 프로파일 UUID 또는 표시 이름</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--yes"><a href="#banshee-sandbox-profile-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>확인 프롬프트 건너뛰기</p></dd>
    <dt id="banshee-sandbox-profile-delete--help"><a href="#banshee-sandbox-profile-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
</code></pre>

### banshee sandbox report

샘플 분석 보고서.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox report [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">명령어</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-report-overview"><code>banshee sandbox report overview</code></a></dt><dd><p>완료된 샘플의 전체 개요 보고서</p></dd>
    <dt><a href="#banshee-sandbox-report-static"><code>banshee sandbox report static</code></a></dt><dd><p>정적 분석 보고서 — 행위 기반 태스크 완료 전에도 사용 가능</p></dd>
    <dt><a href="#banshee-sandbox-report-behavioral"><code>banshee sandbox report behavioral</code></a></dt><dd><p>행위 기반 분석 보고서 — 완료된 태스크당 하나의 객체</p></dd>
</dl>

#### banshee sandbox report overview

완료된 샘플의 전체 개요 보고서. 판정 점수, 악성코드 패밀리, 태그, 해시, 탐지 시그니처, 추출된 악성코드 설정, 네트워크 IOC, 태스크별 결과가 포함됩니다. 샘플은 `reported` 상태여야 합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox report overview [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--sample-id"><a href="#banshee-sandbox-report-overview--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>보고서를 조회할 샘플 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--wait"><a href="#banshee-sandbox-report-overview--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>보고서가 준비될 때까지 폴링합니다 (최대 30분). 타임아웃 후에도 준비되지 않으면 비정상 종료</p></dd>
    <dt id="banshee-sandbox-report-overview--pretty"><a href="#banshee-sandbox-report-overview--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-report-overview--help"><a href="#banshee-sandbox-report-overview--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
</code></pre>

#### banshee sandbox report static

샘플의 정적 분석 보고서. 판정 점수, 태그, 언패킹된 파일, 정적 탐지 시그니처, 추출된 악성코드 설정이 포함됩니다. 행위 기반 태스크 완료 전에도 사용 가능합니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox report static [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--sample-id"><a href="#banshee-sandbox-report-static--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>정적 보고서를 조회할 샘플 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--wait"><a href="#banshee-sandbox-report-static--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>보고서가 준비될 때까지 폴링합니다 (최대 10분)</p></dd>
    <dt id="banshee-sandbox-report-static--pretty"><a href="#banshee-sandbox-report-static--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-report-static--help"><a href="#banshee-sandbox-report-static--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
</code></pre>

#### banshee sandbox report behavioral

샘플의 행위 기반 분석 보고서. 완료된 행위 기반 태스크당 하나의 JSON 객체를 반환하며, 판정 점수, 플랫폼, 트리거된 시그니처, 관찰된 프로세스, 네트워크 활동, 추출된 악성코드 설정이 포함됩니다.

미완료 태스크는 출력에서 제외되고 stderr에 기록되며, 모든 태스크가 완료될 때까지 비정상 종료됩니다. 샘플에 행위 기반 태스크가 없으면 빈 배열과 함께 종료 코드 0으로 반환됩니다.

기본적으로 결과는 JSON 형식으로 출력됩니다.

<h3 class="commands-reference">사용법</h3>

```
banshee sandbox report behavioral [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">인수</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--sample-id"><a href="#banshee-sandbox-report-behavioral--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>행위 기반 보고서를 조회할 샘플 ID</p></dd>
</dl>

<h3 class="commands-reference">옵션</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--wait"><a href="#banshee-sandbox-report-behavioral--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>모든 태스크가 완료될 때까지 폴링합니다 (최대 30분)</p></dd>
    <dt id="banshee-sandbox-report-behavioral--full-cmd"><a href="#banshee-sandbox-report-behavioral--full-cmd"><code>--full-cmd</code></a></dt><dd>
    <p>프로세스 명령줄을 전체 표시합니다(잘림 없음). 명령줄 내용은 악성코드 샘플에서 직접 가져오므로 신뢰할 수 없는 입력으로 취급해야 합니다.</p></dd>
    <dt id="banshee-sandbox-report-behavioral--pretty"><a href="#banshee-sandbox-report-behavioral--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>결과를 사람이 읽기 쉬운 형식으로 보기 좋게 출력</p></dd>
    <dt id="banshee-sandbox-report-behavioral--help"><a href="#banshee-sandbox-report-behavioral--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>이 명령어의 도움말 표시</p>
</dl>

<h3 class="commands-reference">사용 예시</h3>

<pre><code class="language-bash">
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
</code></pre>