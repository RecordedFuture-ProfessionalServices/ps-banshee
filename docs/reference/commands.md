# Command Line Reference

## banshee

PS Banshee is a command-line tool for fast, efficient access to Recorded Future Intelligence, built for security professionals and SOC teams.

<h3 class="commands-reference">Usage</h3>

```
banshee [OPTIONS] <COMMAND>
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca"><code>banshee ca</code></a></dt><dd><p>Search, lookup and update Recorded Future Classic Alerts</p></dd>
    <dt><a href="#banshee-email"><code>banshee email</code></a></dt><dd><p>Enrich e-mail files (EML) with Recorded Future intelligence</p></dd>
    <dt><a href="#banshee-entity"><code>banshee entity</code></a></dt><dd><p>Search and lookup Recorded Future entities</p></dd>
    <dt><a href="#banshee-ioc"><code>banshee ioc</code></a></dt><dd><p>Search and lookup Indicators of Compromise (IOCs)</p></dd>
    <dt><a href="#banshee-list"><code>banshee list</code></a></dt><dd><p>Manage Recorded Future lists and Watch lists</p></dd>
    <dt><a href="#banshee-pba"><code>banshee pba</code></a></dt><dd><p>Search, lookup and update Recorded Future Playbook Alerts</p></dd>
    <dt><a href="#banshee-pcap"><code>banshee pcap</code></a></dt><dd><p>Analyze packet capture (pcap) files by enriching them with Recorded Future Intelligence</p></dd>
    <dt><a href="#banshee-risklist"><code>banshee risklist</code></a></dt><dd><p>Manage Risk Lists</p></dd>
    <dt><a href="#banshee-rules"><code>banshee rules</code></a></dt><dd><p>Search for and download detection rules</p></dd>
</dl>

## banshee ca

Search, lookup and update Recorded Future Classic Alerts

<h3 class="commands-reference">Usage</h3>

```
banshee ca [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca-lookup"><code>banshee ca lookup</code></a></dt><dd><p>Lookup a Classic Alert</p></dd>
    <dt><a href="#banshee-ca-search"><code>banshee ca search</code></a></dt><dd><p>Search for Classic Alerts</p></dd>
    <dt><a href="#banshee-ca-rules"><code>banshee ca rules</code></a></dt><dd><p>Search for Classic Alert rules</p></dd>
    <dt><a href="#banshee-ca-update"><code>banshee ca update</code></a></dt><dd><p>Update one or more Classic Alert</p></dd>
</dl>

### banshee ca lookup

Lookup a Classic Alert.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ca lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--alert-id"><a href="#banshee-ca-lookup--alert-id"<code>ALER_ID</code></a></dt><dd><p>Alert ID to lookup</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ca-lookup--help"><a href="#banshee-ca-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee ca search

Search for Classic Alerts.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ca search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-search--triggered"><a href="#banshee-ca-search--triggered"><code>--triggered</code>, <code>-t</code></a> <i>triggered</i></dt><dd>
    <p>Filter on triggered time, for example: 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)</p>
    <p>Defaults to 1d</p><dd></dd>
    <dt id="banshee-ca-search--rule"><a href="#banshee-ca-search--rule"><code>--rule</code></a> <i>rule-name</i></dt><dd>
    <p>Filter by an alert rule name (freetext)</p><dd></dd>
    <dt id="banshee-ca-search--status"><a href="#banshee-ca-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>Filter by alert status</p>
    <p>Possible values are: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-search--pretty"><a href="#banshee-ca-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ca-search--help"><a href="#banshee-ca-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee ca rules

Search for Classic Alert rules.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ca rules [OPTIONS] [FREETEXT]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--pretty"><a href="#banshee-ca-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ca-rules--help"><a href="#banshee-ca-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee ca update

Update one or more Classic Alert

<h3 class="commands-reference">Usage</h3>

```
banshee ca update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--alert-id"><a href="#banshee-ca-update--alert-id"<code>ALERT_IDS</code></a></dt><dd><p>One or more whitespace separated Alert ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--status"><a href="#banshee-ca-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>Update the alert(s) to this alert status</p>
    <p>Possible values are: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-update--note"><a href="#banshee-ca-update--note"><code>--note</code></a>,  <code>-n</code> <i>note</i></dt><dd>
    <p>Note text for the alert.</p><p>The length limit for the note is 1000 characters</p><dd></dd>
    <dt id="banshee-ca-update--append"><a href="#banshee-ca-update--append"><code>--append</code></a>,  <code>-a</code></dt><dd>
    <p>This flag will append the note text if the alert already has a note</p><dd></dd>
    <dt id="banshee-ca-update--assignee"><a href="#banshee-ca-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>New user to assign the alert(s) to. Accepts uhash or email address of the user, for example: uhash:3aXZxdkM12, analyst@acme.com</p><dd></dd>
    <dt id="banshee-ca-update--help"><a href="#banshee-ca-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>Provide one or more Alert IDs (whitespace separated) and specify the desired update options:</p>

<pre><code class="language-bash">
banshee ca update <alert id> -s Dismissed
banshee ca update <alert id> -s Dismissed -n "note text"
banshee ca update <alert id1> <alert id2>-s Dismissed -n "note text" -a analyst@acme.com
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. Directly as arguments (single or multiple):</h4>

<pre><code class="language-bash">
banshee ca update ALERT_ID -s Resolved
banshee ca update ALERT_ID_1 ALERT_ID_2 -s Pending
</code></pre>

<h4>2. From a file or standard input:</h4>

<p>If you have a file (e.g., <code>alerts.txt</code>) with one Alert ID per line:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>You can update all listed alerts using:</p>

<pre><code class="language-bash">
banshee ca update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee ca update -s Dismissed
</code></pre>

<h4>3. By piping from a search command:</h4>

<p>Use tools like <code>jq</code> to extract Alert IDs from search results and pipe them into the update command:</p>

<pre><code class="language-bash">
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"
</code></pre>

<h3 class="commands-reference">Note Append</h3>

<p>Classic Alerts support only a single note. By default, the <code>update</code> command will overwrite the existing note with the new one.
If you wish to append a new note instead, use the <code>--append</code> (<code>-A</code>) option.</p>

## banshee entity

Search and lookup Recorded Future entities

<h3 class="commands-reference">Usage</h3>

```
banshee entity [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-entity-lookup"><code>banshee entity lookup</code></a></dt><dd><p>Lookup an entity by its ID</p></dd>
    <dt><a href="#banshee-entity-search"><code>banshee entity search</code></a></dt><dd><p>Search entities by name and/or type</p></dd>
</dl>

### banshee entity lookup

 Lookup an entity by its ID

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee entity lookup [OPTIONS] ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--entity-id"><a href="#banshee-entity-lookup--entity-id"<code>ENTITY_ID</code></a></dt><dd><p>Entity ID to lookup</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--pretty"><a href="#banshee-entity-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-entity-lookup--help"><a href="#banshee-entity-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee entity search

Search for entities by name and/or type

By default the command will print results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee entity search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--type"><a href="#banshee-entity-search--type"><code>--type</code>, <code>-t</code></a> <i>entity-type</i></dt><dd>
    <p>Entity type to search for</p>
    <p>Can be supplied multiple times for different entity types</p>
    <p>Supported values are:</p>
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
    <p>Limit the number of results</p>
    <p>The maximum limit is 100</p>
    <p>Defaults to 100</p><dd></dd>
    <dt id="banshee-entity-search--pretty"><a href="#banshee-entity-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-entity-search--help"><a href="#banshee-entity-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>


## banshee email

Enrich e-mail files (EML) with Recorded Future intelligence.

<h3 class="commands-reference">Usage</h3>

```
banshee email [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-email-enrich"><code>banshee email enrich</code></a></dt><dd><p>Enrich an e-mail (EML) file with Recorded Future intelligence</p></dd>
</dl>

### banshee email enrich

Enrich an e-mail (EML) file with Recorded Future Intelligence. This command parses the EML file to extract IP addresses from the header and URLs (prefixed with `http`/`https`) found in the body, then enriches them with threat intelligence data. By default, results are filtered to show only indicators that meet your risk score threshold. Use `--threat-hunt` to also include indicators linked to threat actors, even if they fall below the risk score threshold.

By default the command will print the results in JSON format.

<h3 class="commands-reference">JSON Output</h3>

Each result object in the JSON array contains the following fields:

| Field | Description |
|---|---|
| `ioc` | The indicator extracted from the e-mail — either an IP address or a URL |
| `type` | The indicator type, e.g. `ip` or `url` |
| `location` | The section of the e-mail where the indicator was found, e.g. `header` or `body` |
| `risk_score` | Recorded Future risk score |
| `ta_names` | List of threat actor names associated with this indicator. Empty if none known |
| `malwares` | List of malware family names linked to this indicator. Empty if none known |
| `first_seen` | ISO 8601 timestamp of the first recorded sighting |
| `last_seen` | ISO 8601 timestamp of the most recent recorded sighting |
| `count_of_analyst_notes` | Number of Recorded Future analyst notes referencing this indicator |
| `rule_evidence` | Array of individual risk rule evidence details, sorted highest severity first |

Each object in the `rule_evidence` array contains:

| Field | Description |
|---|---|
| `rule` | Name of the specific Recorded Future risk rule that fired |
| `level` | Severity level of this rule — higher integers mean more severe |
| `timestamp` | ISO 8601 timestamp of the most recent sighting for this rule |
| `evidence_string` | Human-readable summary of the evidence |

<h3 class="commands-reference">Usage</h3>

```
banshee email enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--file-path"><a href="#banshee-email-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>Path to the EML file to enrich</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--risk-score"><a href="#banshee-email-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>Filter results to show only indicators with risk score (0 - 99) above this threshold</p><p>Defaults to 65</p></dd>
    <dt id="banshee-email-enrich--threat-hunt"><a href="#banshee-email-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>Include indicators linked to threat actors regardless of risk score threshold</p></dd>
    <dt id="banshee-email-enrich--pretty"><a href="#banshee-email-enrich--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-email-enrich--help"><a href="#banshee-email-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code class="language-bash">
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p
banshee email enrich suspicious.eml --threat-hunt
</code></pre>

## banshee ioc

Search and lookup Indicators of Compromise (IOCs)

<h3 class="commands-reference">Usage</h3>

```
banshee ioc [OPTIONS] COMMAND [ARGS]...
```
<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ioc-lookup"><code>banshee ioc lookup</code></a></dt><dd><p>Detailed enrichment for one or more IOCs with configurable verbosity</p></dd>
    <dt><a href="#banshee-ioc-bulk-lookup"><code>banshee ioc bulk-lookup</code></a></dt><dd><p>Fast bulk enrichment returning risk score and triggered rules — batches up to 1000 IOCs per API call</p></dd>
    <dt><a href="#banshee-ioc-search"><code>banshee ioc search</code></a></dt><dd><p>Search for IOCs</p></dd>
    <dt><a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></dt><dd><p>Search for IOC rules</p></dd>
</dl>

### banshee ioc lookup

Detailed enrichment for one or more IOCs — one API call per indicator. Use [`--verbosity`](#banshee-ioc-lookup--verbosity) to control how many fields are returned, from basic risk score up to full intel including links, analyst notes, etc.. Use this when you need rich context.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ioc lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>Entity type to lookup</p>
    <p>Supported values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-lookup--ioc"><a href="#banshee-ioc-lookup--ioc"><code>IOC</code></a></dt><dd><p>One or more whitespace separated IOC to lookup</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--ai-insights"><a href="#banshee-ioc-lookup--ai-insights"><code>--ai-insights</code></a>,  <code>-a</code></dt><dd>
    <p>Enable AI-generated insights from Recorded Future that summarize relevant risk rules and key references.</p>
    <p><strong>Note:</strong> Response times may be slightly longer due to AI processing.</p<dd></dd>
    <dt id="banshee-ioc-lookup--verbosity"><a href="#banshee-ioc-lookup--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>Controls the amount of data returned in the response (1-5). Higher verbosity levels include additional fields and details in the JSON output.</p>
    <p><strong>Note:</strong> Higher verbosity levels may result in slower response times due to increased data retrieval.</p>
    <p>Defaults to 1</p>
    <h4>Available Fields by Verbosity Level</h4>
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
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ioc-lookup--help"><a href="#banshee-ioc-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23,139.224.189.177 -p
</code></pre>

Pipe a comma or newline separated list of IOCs to lookup:

<pre><code>
cat test_ips.csv| banshee ioc lookup ip -p
</code></pre>


### banshee ioc bulk-lookup

Fast bulk enrichment for any number of IOCs of a single type. The command batches up to 1000 IOCs per API call and handles batching automatically, making it significantly faster than [`banshee ioc lookup`](#banshee-ioc-lookup) for large volumes.

Returns a fixed set of fields per indicator: risk score and triggered risk rules. Use this for high-volume triage.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ioc bulk-lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--entity-type"><a href="#banshee-ioc-bulk-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>Entity type to enrich</p>
    <p>Supported values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-bulk-lookup--ioc"><a href="#banshee-ioc-bulk-lookup--ioc"><code>IOC</code></a></dt><dd><p>One or more whitespace separated IOCs to enrich. Also accepts input from stdin (see examples below).</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--pretty"><a href="#banshee-ioc-bulk-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ioc-bulk-lookup--help"><a href="#banshee-ioc-bulk-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877
</code></pre>

<h4>File / Stdin Input</h4>

Pipe or redirect a newline-separated file of IOCs (one per line):

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

<h4>Extract Names and Scores</h4>
Use `jq` to extract specific fields from the JSON output, for example:

<pre><code>
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'
</code></pre>


### banshee ioc search

Search for Classic Alerts.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ioc search [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>Entity type to lookup</p>
    <p>Supported values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-search--limit"><a href="#banshee-ioc-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>Limit the number of results</p>
    <p>The maximum limit is 1000</p>
    <p>Defaults to 5</p><dd></dd>
    <dt id="banshee-ioc-search--risk-score"><a href="#banshee-ioc-search--risk-score"><code>--risk-score</code>, <code>-r</code></a> <i>risk-score</i></dt><dd>
    <p>Filter by risk score range, for example:</p>
    <p>
        <ul>
            <li><code>--risk-score '[20,90]'</code> &rarr; same as <code>20 &lt;= riskScore &lt;= 90</code></li>
            <li><code>--risk-score '(20,90)'</code> &rarr; same as <code>20 &lt; riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,90)'</code> &rarr; same as <code>20 &lt;= riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,)'</code> &rarr; same as <code>20 &lt;= riskScore</code></li>
            <li><code>--risk-score '[,90)'</code> &rarr; same as <code>riskScore &lt; 90</code></li>
        </ul>
    </p>
    <p>Surround the risk score range with quotes to ensure correct parsing</p>
    <dd></dd>
    <dt id="banshee-ioc-search--risk-rule"><a href="#banshee-ioc-search--risk-rule"><code>--risk-rule</code>, <code>-R</code></a> <i>rule-name</i></dt><dd>
    <p>Filter by risk rule name</p>
    <p>For available options refer to this <a href="https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future" target="_blank">support article</a>, specifically the <b>Machine Name</b> column in the risk rules tables, or use the <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> command</p><dd></dd>
    <dt id="banshee-ioc-search--verbosity"><a href="#banshee-ioc-search--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>Controls the amount of data returned in the response (1-5). Higher verbosity levels include additional fields and details in the JSON output.</p>
    <p><strong>Note:</strong> Higher verbosity levels may result in slower response times due to increased data retrieval.</p>
    <p>Defaults to 1</p>
    <h4>Available Fields by Verbosity Level</h4>
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
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ioc-search--help"><a href="#banshee-ioc-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee ioc rules

Search for IOC rules for a given entity type.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee ioc rules [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--entity-type"><a href="#banshee-ioc-rules--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>Entity type of the IOC rules</p>
    <p>Supported values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--freetext"><a href="#banshee-ioc-rules--freetext"><code>--freetext</code>, <code>-F</code></a> <i>freetext-rule-name</i></dt><dd>
    <p>Filter by risk rule name using freetext search</p><dd></dd>
    <dt id="banshee-ioc-rules--mitre"><a href="#banshee-ioc-rules--mitre"><code>--mitre-code</code>, <code>-M</code></a> <i>mitre-code</i></dt><dd>
    <p>Filter by MITRE ATT&CK code</p><dd></dd>
    <dt id="banshee-ioc-rules--criticality"><a href="#banshee-ioc-rules--criticality"><code>--criticality</code>, <code>-C</code></a> <i>criticality</i></dt><dd>
    <p>Filter by criticality. Higher the value, higher the criticality</p>
    <p>Accepted values are from 1 to 5</p>
    <p><strong>Criticality Levels (IP, Domain, URL, Hash)</strong></p>
    <ul>
        <li><code>4</code> – Very Malicious (Risk Score band: 90–99)</li>
        <li><code>3</code> – Malicious (Risk Score band: 65–89)</li>
        <li><code>2</code> – Suspicious (Risk Score band: 25–64)</li>
        <li><code>1</code> – Unusual (Risk Score band: 5–24)</li>
        <li><code>0</code> – No evidence of risk (Risk Score band: 0)</li>
    </ul>
    <p><strong>Criticality Levels (Vulnerability)</strong></p>
    <ul>
        <li><code>5</code> – Very Critical (Risk Score band: 90–99)</li>
        <li><code>4</code> – Critical (Risk Score band: 80–89)</li>
        <li><code>3</code> – High (Risk Score band: 65–79)</li>
        <li><code>2</code> – Medium (Risk Score band: 25–64)</li>
        <li><code>1</code> – Low (Risk Score band: 5–24)</li>
        <li><code>0</code> – No evidence of risk (Risk Score band: 0)</li>
    </ul>
    <dd></dd>
    <dt id="banshee-ioc-rules--pretty"><a href="#banshee-ioc-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-ioc-rules--help"><a href="#banshee-ioc-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

## banshee list

Manage Recorded Future lists and Watch lists

<h3 class="commands-reference">Usage</h3>

```
banshee list [OPTIONS] COMMAND [ARGS]...
```
<dl class="commands-reference">
    <dt><a href="#banshee-list-create"><code>banshee list create</code></a></dt><dd><p>Create a new list</p></dd>
    <dt><a href="#banshee-list-info"><code>banshee list info</code></a></dt><dd><p>Get basic information about a list</p></dd>
    <dt><a href="#banshee-list-search"><code>banshee list search</code></a></dt><dd><p>Search for lists</p></dd>
    <dt><a href="#banshee-list-status"><code>banshee list status</code></a></dt><dd><p>Get the status of a list</p></dd>
    <dt><a href="#banshee-list-entities"><code>banshee list entities</code></a></dt><dd><p>Get the entities in a list</p></dd>
    <dt><a href="#banshee-list-add"><code>banshee list add</code></a></dt><dd><p>Add an entity to a list</p></dd>
    <dt><a href="#banshee-list-bulk-add"><code>banshee list bulk-add</code></a></dt><dd><p>Bulk add entities to a list</p></dd>
    <dt><a href="#banshee-list-remove"><code>banshee list remove</code></a></dt><dd><p>Remove an entity from a list</p></dd>
    <dt><a href="#banshee-list-bulk-remove"><code>banshee list bulk-remove</code></a></dt><dd><p>Bulk remove entities from a list</p></dd>
    <dt><a href="#banshee-list-clear"><code>banshee list clear</code></a></dt><dd><p>Clear all entities from a list</p></dd>
    <dt><a href="#banshee-list-entries"><code>banshee list entries</code></a></dt><dd><p>Get text entries from a list</p></dd>
</dl>

### banshee list create

Create a new list.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list create [OPTIONS] NAME [LIST_TYPE]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>NAME</code></a></dt><dd><p>List name to create</p></dd>
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>LIST_TYPE</code></a></dt><dd><p>List type to create</p>
    <p>Supported types are:</p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
    </ul>
    <p>Defaults to <code>entity</code></p>
    </dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--pretty"><a href="#banshee-list-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-lookup--help"><a href="#banshee-list-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list info

Get information about a list, such as name, type, timestamps and owner details.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list info [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to get information about</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list search

Search for lists

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list search [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--name"><a href="#banshee-list-search--name"><code>NAME</code></a></dt><dd>
    <p>List name to search for</p>
    <p>Not specifying a name will return all lists</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--list-type"><a href="#banshee-list-search--list-type"><code>--list-type</code>, <code>-t</code></a> <i>list-type</i></dt><dd>
    <p>Filter by list type</p>
    <p>Supported types:</p>
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
    <p>Limit the number of results</p>
    <p>The maximum limit is 3 000</p>
    <p>Defaults to 1 000</p><dd></dd>
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list status

Get list status and number of entities.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list status [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to get the status of</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list entities

Get entities on the list

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list entities [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to fetch entities from</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>


### banshee list entries

Get text entries on the list

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee list entries [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to fetch text entries from</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>



### banshee list clear

Fully clear the list and remove all entities. Please note this command will not clear text entries and is not supported.

<h3 class="commands-reference">Usage</h3>

```
banshee list clear [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to clear</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list add

Add an entity to the list.

<h3 class="commands-reference">Usage</h3>

```
banshee list add [OPTIONS] LIST_ID ENTITY_ID [PROPERTIES]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--list-id"><a href="#banshee-list-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to add to</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
    <dt id="banshee-list-add--entity-id"><a href="#banshee-list-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>Entity ID or name with type to add to the list, for example:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul></dd>
    <dt id="banshee-list-add--properties"><a href="#banshee-list-add--properties"><code>PROPERTIES</code></a></dt><dd>
    <p>Optional properties to set on the entity</p>
    <p>Properties can be supplied as key=value pairs, for example: type=malware,cool=beans,another=value</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--help"><a href="#banshee-list-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list bulk-add

Add multiple entities to a list

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-add [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--list-id"><a href="#banshee-list-bulk-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to add to</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
    <dt id="banshee-list-bulk-add--entity-id"><a href="#banshee-list-bulk-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>One or more space/newline separated entities, for example:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>The command also accepts input from stdin. Assume 'entities.txt' is a newline separated file of entities, for example:</p>
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
    <p>Considering the above you could then run one of the following commands to bulk add the entities:</p>
    <pre><code>
    $ banshee list bulk-add LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-add LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--help"><a href="#banshee-list-bulk-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list remove

Remove an entity from the list.

<h3 class="commands-reference">Usage</h3>

```
banshee list remove [OPTIONS] LIST_ID ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--list-id"><a href="#banshee-list-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to remove from</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
    <dt id="banshee-list-remove--entity-id"><a href="#banshee-list-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>Entity ID to remove from the list</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--help"><a href="#banshee-list-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee list bulk-remove

Remove multiple entities from a list

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-remove [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--list-id"><a href="#banshee-list-bulk-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID to remove from</p>
    <p>List ID can be supplied with and without the '<strong>report:</strong>' prefix</p></dd>
    <dt id="banshee-list-bulk-remove--entity-id"><a href="#banshee-list-bulk-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>One or more space/newline separated entities, for example:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>The command also accepts input from stdin. Assume 'entities.txt' is a newline separated file of entities, for example:</p>
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
    <p>Considering the above you could then run one of the following commands to bulk remove the entities:</p>
    <pre><code>
    $ banshee list bulk-remove LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-remove LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--help"><a href="#banshee-list-bulk-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

## banshee pba

Search, lookup and update Recorded Future Playbook Alerts

<h3 class="commands-reference">Usage</h3>

```
banshee pba [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pba-lookup"><code>banshee pba lookup</code></a></dt><dd><p>Lookup a Playook Alert</p></dd>
    <dt><a href="#banshee-pba-search"><code>banshee pba search</code></a></dt><dd><p>Search for Playook Alerts</p></dd>
    <dt><a href="#banshee-pba-update"><code>banshee pba update</code></a></dt><dd><p>Update one or more Playook Alert</p></dd>
</dl>

### banshee pba lookup

Lookup a Playook Alert.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee pba lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--alert-id"><a href="#banshee-pba-lookup--alert-id"<code>ALERT_ID</code></a></dt><dd><p>Alert ID to lookup</p>
    <p>Alert ID can be supplied with and without the '<strong>task:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--pretty"><a href="#banshee-pba-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-pba-lookup--help"><a href="#banshee-pba-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee pba search

Search for Playook Alerts.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee pba search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-search--created"><a href="#banshee-pba-search--created"><code>--created</code>, <code>-C</code></a> <i>created-from</i></dt><dd>
    <p>Filter on the created from time, for example: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--updated"><a href="#banshee-pba-search--updated"><code>--updated</code>, <code>-u</code></a> <i>updated-from</i></dt><dd>
    <p>Filter on the updated from time, for example: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--category"><a href="#banshee-pba-search--category"><code>--category</code>, <code>-c</code></a> <i>category</i></dt><dd>
    <p>Filter by alert category</p>
    <p>Supported categories:</p>
    <p>
    <ul>
        <li><code>domain_abuse</code></li>
        <li><code>cyber_vulnerability</code></li>
        <li><code>third_party_risk</code></li>
        <li><code>code_repo_leakage</code></li>
        <li><code>identity_novel_exposures</code></li>
        <li><code>geopolitics_facility</code></li>
    </ul>
    </p><dd></dd>
    <dt id="banshee-pba-search--priority"><a href="#banshee-pba-search--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>Filter by alert priority</p>
    <p>Possible values are: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p>
    <p>Defaults to all categories</p><dd></dd>
    <dt id="banshee-pba-search--status"><a href="#banshee-pba-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>Filter by alert status</p>
    <p>Possible values are: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p>
    <p>Defaults to all categories</p><dd></dd>
    <dt id="banshee-pba-search--entity"><a href="#banshee-pba-search--entity"><code>--entity</code></a>,  <code>-e</code> <i>entity</i></dt><dd>
    <p>Filter alerts by associated entity, for example: idn:recordedfuture.com</p><dd></dd>
    <dt id="banshee-pba-search--limit"><a href="#banshee-pba-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>Limit the number of results</p>
    <p>The maximum limit is 10 000</p>
    <p>Defaults to 50</p><dd></dd>
    <dt id="banshee-pba-search--pretty"><a href="#banshee-pba-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-pba-search--help"><a href="#banshee-pba-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

### banshee pba update

Update one or more Playook Alert

<h3 class="commands-reference">Usage</h3>

```
banshee pba update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--alert-id"><a href="#banshee-pba-update--alert-id"<code>ALERT_IDS</code></a></dt><dd>
    <p>One or more whitespace separated Alert ID</p>
    <p>Alert ID can be supplied with and without the '<strong>task:</strong>' prefix</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--status"><a href="#banshee-pba-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>Update the alert(s) to this alert status</p>
    <p>Possible values are: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-pba-update--repopen"><a href="#banshee-pba-update--repopen"><code>--repopen</code></a>,  <code>-r</code> <i>reopen</i></dt><dd>
    <p>Reopen strategies can only be applied to alerts with a status of Dismissed or Resolved. The following combinations of status/reopen are allowed: <code>Dismissed -> Never</code>; <code>Resolved -> Never</code>; <code>Resolved -> SignificantUpdates</code></p>
    <p>Supported values are: <code>Never</code>, <code>SignificantUpdates</code></p><dd></dd>
    <dt id="banshee-pba-update--priority"><a href="#banshee-pba-update--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>Set a new alert priority</p>
    <p>Possible values are: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p><dd></dd>
    <dt id="banshee-pba-update--comment"><a href="#banshee-pba-update--comment"><code>--comment</code></a>,  <code>-t</code> <i>comment</i></dt><dd>
    <p>Comment to add to the alert(s), for example: "Bulk resolved via banshee"</p><dd></dd>
    <dt id="banshee-pba-update--assignee"><a href="#banshee-pba-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>New user to assign the alert(s) to. Accepts uhash of the user, for example: uhash:3aXZxdkM12</p><dd></dd>
    <dt id="banshee-pba-update--help"><a href="#banshee-pba-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>Provide one or more alert IDs (whitespace separated) and specify the desired update options:</p>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Dismissed
banshee pba update ALERT_ID -s InProgress -p High -t "Escalated due to new findings"
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved -a uhash:3aXZxdkM12
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. Directly as arguments (single or multiple):</h4>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved
</code></pre>

<h4>2. From a file or standard input:</h4>

<p>If you have a file (e.g., <code>alerts.txt</code>) with one alert ID per line:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>You can update all listed alerts using:</p>

<pre><code class="language-bash">
banshee pba update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee pba update -s Dismissed
</code></pre>

<h4>3. By piping from a search command:</h4>

<p>Use tools like <code>jq</code> to extract alert IDs from search results and pipe them into the update command:</p>

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


## banshee pcap

Enrich packet captures (pcap) with Recorded Future intelligence.

<h3 class="commands-reference">Usage</h3>

```
banshee pcap [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pcap-enrich"><code>banshee pcap enrich</code></a></dt><dd><p>Enrich a packet capture (pcap) file with Recorded Future intelligence</p></dd>
</dl>

### banshee pcap enrich

This command parses the pcap file to extract network indicators like IP addresses and domains, then enriches them with threat intelligence data. By default, results are filtered to show only indicators that meet your risk score threshold. Use `--threat-hunt` to also include indicators linked to threat actors, even if they fall below the risk score threshold.
<br>Please note that lowering the risk score threshold and/or enabling threat hunting may significantly increase both the number of results and processing time.

By default the command will print the results in JSON format.

<h3 class="commands-reference">JSON Output</h3>

Each result object in the JSON array contains the following fields:

| Field | Description |
|---|---|
| `ioc` | The network indicator extracted from the pcap — either an IP address or a domain name |
| `risk_score` | Recorded Future risk score |
| `most_malicious_rule` | The name of the highest-severity risk rule that contributed to the risk score |
| `rule_evidence` | Array of individual risk rule evidence details, sorted highest severity first |
| `ta_names` | List of threat actor names associated with this IOC. Empty if none known |
| `malwares` | List of malware family names linked to this IOC. Empty if none known |
| `wireshark_query` | Ready-to-paste Wireshark display filter to isolate this IOC's traffic |

Each object in the `rule_evidence` array contains:

| Field | Description |
|---|---|
| `count` | Number of sources that contributed references to this risk rule |
| `description` | Human-readable summary of the evidence|
| `level` | Severity level of this rule — higher integers mean more severe |
| `mitigation` | Describes white lists that the IOC may appear on which reduces (or mitigates) the associated risk |
| `rule` | Name of the specific Recorded Future risk rule that fired |
| `sightings` | Number of individual sightings recorded|
| `timestamp` | ISO 8601 timestamp of the most recent sighting for this rule |
| `type` | Type identifier |

<h3 class="commands-reference">Usage</h3>


```
banshee pcap enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--file-path"><a href="#banshee-pcap-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>Path to the pcap file to enrich</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--risk-score"><a href="#banshee-pcap-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>Filter results to show only indicators with risk score (1 - 99) above this threshold<p>Defaults to 65</p></p></dd>
    <dt id="banshee-pcap-enrich--threat-hunt"><a href="#banshee-pcap-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>Include indicators linked to threat actors regardless of risk score threshold (retrospective threat hunting)</p></dd>
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p><dd></dd>
    <dt id="banshee-pcap-enrich--help"><a href="#banshee-pcap-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

## banshee risklist

Manage Risk Lists.

<h3 class="commands-reference">Usage</h3>

```
banshee risklist [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-risklist-create"><code>banshee risklist create</code></a></dt><dd><p>Build a custom risk list by combining one or more risk rules</p></dd>
    <dt><a href="#banshee-risklist-fetch"><code>banshee risklist fetch</code></a></dt><dd><p>Download a risk list</p></dd>
    <dt><a href="#banshee-risklist-stat"><code>banshee risklist stat</code></a></dt><dd><p>Show risk list metadata (etag and timestamp)</p></dd>
</dl>

### banshee risklist create

Build a custom risk list by combining one or more Recorded Future risk rules into a single deduplicated file.

Entries are fetched for each `--risk-rule`, merged by IOC (first occurrence wins), and optionally filtered down to a minimum `--risk-score`. The output is sorted by risk score descending and written in your chosen format — ready to feed into a firewall, SIEM, or other integration.

Output is written to a local file by default. Use `--fusion` with `--output-path` to upload the result directly to Recorded Future Fusion without writing a local copy.

<h3 class="commands-reference">Usage</h3>

```
banshee risklist create [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-create--entity-type"><a href="#banshee-risklist-create--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>Entity type for the risk list. Valid values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><strong>Required</strong></p></dd>
    <dt id="banshee-risklist-create--risk-rule"><a href="#banshee-risklist-create--risk-rule"><code>--risk-rule</code></a>, <code>-R</code> <i>risk-rule</i></dt><dd>
    <p>Risk rule to include. Use <code>default</code>, <code>large</code>, or any rule name from <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a>. Repeatable — specify multiple times to merge rules into a single output.<br><strong>Required (at least one)</strong></p></dd>
    <dt id="banshee-risklist-create--risk-score"><a href="#banshee-risklist-create--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>Minimum risk score threshold (5–99). Entries with a risk score below this value are excluded from the output</p></dd>
    <dt id="banshee-risklist-create--format"><a href="#banshee-risklist-create--format"><code>--format</code></a>, <code>-f</code> <i>format</i></dt><dd>
    <p>Output format. Defaults to <code>csv</code></p>
    <ul>
        <li><code>csv</code> — Comma-separated with headers: <code>Name</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code>. Hash entity type includes an additional <code>Algorithm</code> column: <code>Name</code>, <code>Algorithm</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code></li>
        <li><code>edl</code> — Plain list of IOC values, one per line (suitable for firewall EDL feeds). Written with a <code>.txt</code> extension</li>
        <li><code>json</code> — JSON array of full risk list entries</li>
    </ul></dd>
    <dt id="banshee-risklist-create--output-path"><a href="#banshee-risklist-create--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>Output file path. Accepts a file path or a directory (filename is auto-generated as <code>custom_risklist_{entity_type}.{ext}</code>). Defaults to the current directory with an auto-generated filename.<br>Required when using <code>--fusion</code></p></dd>
    <dt id="banshee-risklist-create--fusion"><a href="#banshee-risklist-create--fusion"><code>--fusion</code></a>, <code>-F</code></dt><dd>
    <p>Upload the result directly to Recorded Future Fusion using <code>--output-path</code> as the destination path. No local file is written when this flag is set</p></dd>
    <dt id="banshee-risklist-create--help"><a href="#banshee-risklist-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

Build a CSV risk list for IPs from the default rule, filtered to risk score 70+

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
```

Merge two domain rules into a single deduplicated CSV, filtered to risk score 80+

```bash
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
```

Merge two IP rules and output as an EDL (plain IOC list)

```bash
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
```

Build a JSON risk list for hashes from two rules and output to a specific local file path

```bash
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
```

Build a risk list and upload directly to Recorded Future Fusion

```bash
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

### banshee risklist fetch

Download a risk list for a specific entity type and list name, or use a custom risk list file.

Risk lists can be downloaded from Recorded Future by specifying an entity type (`--entity-type`) and list name (`--list-name`). Available list names include `default`, `large`, or any rule name from `banshee ioc rules`. For more information about Recorded Future Risk Rules, see the [Risk Scoring in Recorded Future](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future) support article.

Alternatively, you can provide a path to a custom risk list file using `--custom-list-path`.

<h3 class="commands-reference">Usage</h3>

```
banshee risklist fetch [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-fetch--entity-type"><a href="#banshee-risklist-fetch--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>Entity type for the risk list. Valid values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br>Required when using <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-fetch--list-name"><a href="#banshee-risklist-fetch--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>Risk list name: <code>default</code>, <code>large</code>, or rule name from <code>banshee ioc rules</code><br>Required when using <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-fetch--custom-list-path"><a href="#banshee-risklist-fetch--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>Path to custom risk list file. Cannot be used with <code>--entity-type</code> or <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-fetch--output-path"><a href="#banshee-risklist-fetch--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>Output file path. Defaults to current directory with auto-generated filename</p></dd>
    <dt id="banshee-risklist-fetch--as-json"><a href="#banshee-risklist-fetch--as-json"><code>--as-json</code></a>, <code>-j</code></dt><dd>
    <p>Convert risk list to JSON format. Can only be used with <code>--list-name</code> and <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-fetch--help"><a href="#banshee-risklist-fetch--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
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

Show risk list metadata including etag and timestamp information.

This command retrieves metadata for a risk list without downloading the full list content. It can be used to check when a risk list was last updated.

<h3 class="commands-reference">Usage</h3>

```
banshee risklist stat [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-stat--entity-type"><a href="#banshee-risklist-stat--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>Entity type for the risk list. Valid values: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br>Required when using <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-stat--list-name"><a href="#banshee-risklist-stat--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>Risk list name: <code>default</code>, <code>large</code>, or rule name from <code>banshee ioc rules</code><br>Required when using <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-stat--custom-list-path"><a href="#banshee-risklist-stat--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>Path to custom risk list file. Cannot be used with <code>--entity-type</code> or <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-stat--pretty"><a href="#banshee-risklist-stat--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p></dd>
    <dt id="banshee-risklist-stat--help"><a href="#banshee-risklist-stat--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# Check metadata for the default IP risk list
banshee risklist stat -e ip -l default

# Check metadata with pretty formatting
banshee risklist stat -e domain -l large -p

# Check metadata for a custom risk list file
banshee risklist stat -c /path/to/custom_risklist.txt
</code></pre>

## banshee rules

Search for and download detection rules.

<h3 class="commands-reference">Usage</h3>

```
banshee rules [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-rules-search"><code>banshee rules search</code></a></dt><dd><p>Search for detection rules based on filter options</p></dd>
</dl>

### banshee rules search

Search for detection rules based on the provided filter options. Results can be displayed in the console or saved to disk as individual rule files.

Detection rules can be filtered by type (YARA, Snort, Sigma), associated entities (threat actors, malware, MITRE ATT&CK techniques), creation/update dates, and more. Use `--threat-actor-map` or `--threat-malware-map` to automatically filter rules based on entities in your Threat Map.

To avoid overwhelming output, results are limited to 10 by default. Use the `--limit` option to retrieve up to 1000 rules.

By default the command will print the results in JSON format.

<h3 class="commands-reference">Usage</h3>

```
banshee rules search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-rules-search--type"><a href="#banshee-rules-search--type"><code>--type</code></a>, <code>-t</code> <i>type</i></dt><dd>
    <p>Filter by rule type. Valid values: <code>yara</code>, <code>snort</code>, <code>sigma</code><br>Multiple types can be specified and work as a logical OR (e.g., <code>-t yara -t snort</code> returns rules matching either type)</p></dd>
    <dt id="banshee-rules-search--threat-actor-map"><a href="#banshee-rules-search--threat-actor-map"><code>--threat-actor-map</code></a>, <code>-T</code></dt><dd>
    <p>Filter rules by threat actors from your Threat Actor Map. When enabled, detection rules associated with actors in your Threat Actor Map will be returned</p></dd>
    <dt id="banshee-rules-search--threat-actor-category"><a href="#banshee-rules-search--threat-actor-category"><code>--threat-actor-category</code></a>, <code>-C</code> <i>category</i></dt><dd>
    <p>Filter by threat actor categories from your Threat Actor Map. Multiple categories can be specified and work as a logical OR (e.g., <code>-C nation_state_sponsored -C ransomware_and_extortion_groups</code>)</p></dd>
    <dt id="banshee-rules-search--threat-malware-map"><a href="#banshee-rules-search--threat-malware-map"><code>--threat-malware-map</code></a>, <code>-M</code></dt><dd>
    <p>Filter rules by malware from your Malware Threat Map. When enabled, detection rules associated with malware in your Malware Threat Map will be returned</p></dd>
    <dt id="banshee-rules-search--org-id"><a href="#banshee-rules-search--org-id"><code>--org-id</code></a>, <code>-O</code> <i>org-id</i></dt><dd>
    <p>Specify the organization ID when fetching threat actors from a Threat Maps (requires <code>--threat-actor-map</code> or <code>--threat-malware-map</code>). Accepts values with or without the <code>uhash:</code> prefix. Useful for MSSP and multi-organization accounts</p></dd>
    <dt id="banshee-rules-search--entity"><a href="#banshee-rules-search--entity"><code>--entity</code></a>, <code>-e</code> <i>entity</i></dt><dd>
    <p>Filter by Recorded Future entity IDs associated with detection rules. Multiple entities can be specified and work as a logical OR. Use <code>banshee entity search</code> to find entity IDs (e.g., <code>lzQ5GL</code> for IsaacWiper malware, <code>mitre:T1486</code> for Data Encrypted for Impact)</p></dd>
    <dt id="banshee-rules-search--created-after"><a href="#banshee-rules-search--created-after"><code>--created-after</code></a>, <code>-a</code> <i>time</i></dt><dd>
    <p>Filter detection rules created after the specified time. Accepts relative time (e.g., <code>1d</code>, <code>3d</code>, <code>7d</code>) or absolute date (e.g., <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--created-before"><a href="#banshee-rules-search--created-before"><code>--created-before</code></a>, <code>-b</code> <i>time</i></dt><dd>
    <p>Filter detection rules created before the specified time. Accepts relative time (e.g., <code>1d</code>, <code>3d</code>, <code>7d</code>) or absolute date (e.g., <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--updated-after"><a href="#banshee-rules-search--updated-after"><code>--updated-after</code></a>, <code>-u</code> <i>time</i></dt><dd>
    <p>Filter detection rules updated after the specified time. Accepts relative time (e.g., <code>1d</code>, <code>3d</code>, <code>7d</code>) or absolute date (e.g., <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--updated-before"><a href="#banshee-rules-search--updated-before"><code>--updated-before</code></a>, <code>-U</code> <i>time</i></dt><dd>
    <p>Filter detection rules updated before the specified time. Accepts relative time (e.g., <code>1d</code>, <code>3d</code>, <code>7d</code>) or absolute date (e.g., <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--id"><a href="#banshee-rules-search--id"><code>--id</code></a>, <code>-i</code> <i>document-id</i></dt><dd>
    <p>Filter by a specific Insikt Note document ID associated with detection rules (e.g., <code>doc:lmRPGB</code>)</p></dd>
    <dt id="banshee-rules-search--title"><a href="#banshee-rules-search--title"><code>--title</code></a>, <code>-n</code> <i>title</i></dt><dd>
    <p>Free text search for detection rules by their associated Insikt Note titles</p></dd>
    <dt id="banshee-rules-search--limit"><a href="#banshee-rules-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>Maximum number of detection rules to return<p>Defaults to 10</p></p></dd>
    <dt id="banshee-rules-search--output-path"><a href="#banshee-rules-search--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>Save the detection rules to the specified directory. Can be a relative or an absolute path. If not specified, results are printed to console</p></dd>
    <dt id="banshee-rules-search--pretty"><a href="#banshee-rules-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>Pretty print the results in a human readable format</p></dd>
    <dt id="banshee-rules-search--help"><a href="#banshee-rules-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>Show help for this command</p>
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

