# Command Line Reference

## banshee

PS Banshee เป็นเครื่องมือบรรทัดคำสั่ง (command-line tool) สำหรับเข้าถึง Recorded Future Intelligence ได้อย่างรวดเร็วและมีประสิทธิภาพ ออกแบบมาสำหรับผู้เชี่ยวชาญด้านความปลอดภัยและทีม SOC

<h3 class="commands-reference">Usage</h3>

```
banshee [OPTIONS] <COMMAND>
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca"><code>banshee ca</code></a></dt><dd><p>ค้นหา ดูข้อมูล และอัปเดต Recorded Future Classic Alerts</p></dd>
    <dt><a href="#banshee-email"><code>banshee email</code></a></dt><dd><p>เสริมข้อมูลไฟล์อีเมล (EML) ด้วย Recorded Future intelligence</p></dd>
    <dt><a href="#banshee-entity"><code>banshee entity</code></a></dt><dd><p>ค้นหาและดูข้อมูล entity ของ Recorded Future</p></dd>
    <dt><a href="#banshee-ioc"><code>banshee ioc</code></a></dt><dd><p>ค้นหาและดูข้อมูล Indicators of Compromise (IOC)</p></dd>
    <dt><a href="#banshee-list"><code>banshee list</code></a></dt><dd><p>จัดการ Recorded Future lists และ Watch lists</p></dd>
    <dt><a href="#banshee-pba"><code>banshee pba</code></a></dt><dd><p>ค้นหา ดูข้อมูล และอัปเดต Recorded Future Playbook Alerts</p></dd>
    <dt><a href="#banshee-pcap"><code>banshee pcap</code></a></dt><dd><p>วิเคราะห์ไฟล์ packet capture (pcap) โดยเสริมข้อมูลด้วย Recorded Future Intelligence</p></dd>
    <dt><a href="#banshee-risklist"><code>banshee risklist</code></a></dt><dd><p>จัดการ Risk Lists</p></dd>
    <dt><a href="#banshee-rules"><code>banshee rules</code></a></dt><dd><p>ค้นหาและดาวน์โหลด detection rules</p></dd>
</dl>

## banshee ca

ค้นหา ดูข้อมูล และอัปเดต Recorded Future Classic Alerts

<h3 class="commands-reference">Usage</h3>

```
banshee ca [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ca-lookup"><code>banshee ca lookup</code></a></dt><dd><p>ดูข้อมูล Classic Alert</p></dd>
    <dt><a href="#banshee-ca-search"><code>banshee ca search</code></a></dt><dd><p>ค้นหา Classic Alerts</p></dd>
    <dt><a href="#banshee-ca-rules"><code>banshee ca rules</code></a></dt><dd><p>ค้นหา Classic Alert rules</p></dd>
    <dt><a href="#banshee-ca-update"><code>banshee ca update</code></a></dt><dd><p>อัปเดต Classic Alert หนึ่งรายการหรือมากกว่า</p></dd>
    <dt><a href="#banshee-ca-export"><code>banshee ca export</code></a></dt><dd><p>ส่งออก Classic Alerts เป็น JSON หรือ CSV</p></dd>
</dl>

### banshee ca lookup

ดูข้อมูล Classic Alert

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ca lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--alert-id"><a href="#banshee-ca-lookup--alert-id"><code>ALERT_ID</code></a></dt><dd><p>Alert ID ที่ต้องการดูข้อมูล</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ca-lookup--help"><a href="#banshee-ca-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee ca search

ค้นหา Classic Alerts

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ca search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-search--triggered"><a href="#banshee-ca-search--triggered"><code>--triggered</code>, <code>-t</code></a> <i>triggered</i></dt><dd>
    <p>กรองตามเวลาที่ triggered เช่น: 1d; 12h; [2024-08-01, 2024-08-14]; [2024-09-23 12:03:58.000, 2024-09-23 12:03:58.567)</p>
    <p>ค่าเริ่มต้นคือ 1d</p><dd></dd>
    <dt id="banshee-ca-search--rule"><a href="#banshee-ca-search--rule"><code>--rule</code></a> <i>rule-name</i></dt><dd>
    <p>กรองตามชื่อ alert rule (freetext)</p><dd></dd>
    <dt id="banshee-ca-search--status"><a href="#banshee-ca-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>กรองตามสถานะของ alert</p>
    <p>ค่าที่เป็นไปได้: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-search--pretty"><a href="#banshee-ca-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ca-search--help"><a href="#banshee-ca-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee ca rules

ค้นหา Classic Alert rules

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ca rules [OPTIONS] [FREETEXT]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--freetext"><a href="#banshee-ca-rules--freetext"><code>FREETEXT</code></a></dt><dd><p>ไม่บังคับ ข้อความอิสระที่ใช้กรอง alert rules ตามชื่อ</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-rules--pretty"><a href="#banshee-ca-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ca-rules--help"><a href="#banshee-ca-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee ca update

อัปเดต Classic Alert หนึ่งรายการหรือมากกว่า

<h3 class="commands-reference">Usage</h3>

```
banshee ca update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--alert-id"><a href="#banshee-ca-update--alert-id"<code>ALERT_IDS</code></a></dt><dd><p>Alert ID หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่าง</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-update--status"><a href="#banshee-ca-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>อัปเดต alert ไปยังสถานะที่ระบุ</p>
    <p>ค่าที่เป็นไปได้: <code>New</code>, <code>Pending</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-ca-update--note"><a href="#banshee-ca-update--note"><code>--note</code></a>,  <code>-n</code> <i>note</i></dt><dd>
    <p>ข้อความบันทึกสำหรับ alert</p><p>ความยาวสูงสุดของบันทึกคือ 1,000 อักขระ</p><dd></dd>
    <dt id="banshee-ca-update--append"><a href="#banshee-ca-update--append"><code>--append</code></a>,  <code>-a</code></dt><dd>
    <p>Flag นี้จะต่อท้ายข้อความบันทึก หาก alert มีบันทึกอยู่แล้ว</p><dd></dd>
    <dt id="banshee-ca-update--assignee"><a href="#banshee-ca-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>ผู้ใช้ใหม่ที่ต้องการมอบหมาย alert ให้ รับค่า uhash หรืออีเมลของผู้ใช้ เช่น: uhash:3aXZxdkM12, analyst@acme.com</p><dd></dd>
    <dt id="banshee-ca-update--help"><a href="#banshee-ca-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>ระบุ Alert ID หนึ่งรายการหรือมากกว่า (คั่นด้วยช่องว่าง) และกำหนดตัวเลือกการอัปเดตที่ต้องการ:</p>

<pre><code class="language-bash">
banshee ca update <alert id> -s Dismissed
banshee ca update <alert id> -s Dismissed -n "note text"
banshee ca update <alert id1> <alert id2>-s Dismissed -n "note text" -a analyst@acme.com
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. ระบุโดยตรงเป็น arguments (รายการเดียวหรือหลายรายการ):</h4>

<pre><code class="language-bash">
banshee ca update ALERT_ID -s Resolved
banshee ca update ALERT_ID_1 ALERT_ID_2 -s Pending
</code></pre>

<h4>2. จากไฟล์หรือ standard input:</h4>

<p>หากมีไฟล์ (เช่น <code>alerts.txt</code>) ที่มี Alert ID หนึ่งรายการต่อบรรทัด:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>สามารถอัปเดต alert ทั้งหมดที่ระบุในไฟล์ได้โดยใช้:</p>

<pre><code class="language-bash">
banshee ca update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee ca update -s Dismissed
</code></pre>

<h4>3. โดย pipe จากคำสั่ง search:</h4>

<p>ใช้เครื่องมืออย่าง <code>jq</code> เพื่อดึง Alert ID จากผลการค้นหาและ pipe เข้าสู่คำสั่ง update:</p>

<pre><code class="language-bash">
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"
</code></pre>

<h3 class="commands-reference">Note Append</h3>

<p>Classic Alerts รองรับบันทึกเพียงรายการเดียว โดยค่าเริ่มต้น คำสั่ง <code>update</code> จะเขียนทับบันทึกที่มีอยู่ด้วยบันทึกใหม่
หากต้องการต่อท้ายบันทึกใหม่แทน ให้ใช้ตัวเลือก <code>--append</code> (<code>-A</code>)</p>

### banshee ca export

ส่งออก Classic Alerts เป็น JSON หรือ CSV โดยอ่าน alert ID จาก stdin — โดยทั่วไปจะ pipe มาจาก [`banshee ca search`](#banshee-ca-search)

<h3 class="commands-reference">Output Formats</h3>

<p><b>JSON (ค่าเริ่มต้น)</b> — ส่งออก object alert แบบ <i>เต็มรูปแบบ</i> สำหรับแต่ละ ID ตามที่ Recorded Future API ส่งกลับมา ประกอบด้วยฟิลด์ระดับบนสุดทั้งหมด รวมถึง hits, entities, evidence, AI insights, review history, portal URLs และอื่น ๆ เหมาะสำหรับการนำไปใช้กับเครื่องมือ downstream, <code>jq</code> pipelines หรือการนำเข้าใหม่</p>

<p><b>CSV (<a href="#banshee-ca-export--csv"><code>--csv</code></a>)</b> — ส่งออกสรุประดับสูงสำหรับใช้กับ spreadsheet และการรายงาน โดยเขียนเฉพาะ 11 คอลัมน์ที่ระบุด้านล่าง (โดยมีแถวหัวตารางก่อน) และละเว้นฟิลด์อื่นที่มีอยู่ใน JSON response ทั้งหมด</p>

| Field | Description |
|---|---|
| `ID` | Classic Alert ID |
| `Priority` | ลำดับความสำคัญของ alert — `High` หาก alert rule เป็น priority rule มิฉะนั้นจะเป็น `Informational` |
| `Alert Rule` | ชื่อของ alert rule ที่ถูก trigger |
| `Status` | สถานะบน portal เช่น `New`, `Pending`, `Dismissed`, `Resolved` |
| `Created` | timestamp ที่ถูก trigger (UTC) |
| `Updated` | timestamp ที่อัปเดตล่าสุด — *ปัจจุบันว่างเสมอ สงวนไว้สำหรับ API ในอนาคต* |
| `Title` | ชื่อของ alert |
| `Assignee` | ผู้ใช้ที่ได้รับมอบหมาย (uhash หรืออีเมล) |
| `URL` | Recorded Future portal URL สำหรับ alert |
| `Entities` | ชื่อ entity หลัก คั่นด้วย `;` |
| `Recorded Future AI Insights` | ข้อความ insight ที่สร้างโดย AI หรือความคิดเห็น |

<h3 class="commands-reference">Usage</h3>

```
banshee ca search [SEARCH_OPTIONS] | banshee ca export [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ca-export--csv"><a href="#banshee-ca-export--csv"><code>--csv</code></a></dt><dd>
    <p>ส่งออกเป็น CSV ด้วยชุดคอลัมน์ที่กำหนดตามที่อธิบายข้างต้น หากไม่ระบุ flag นี้ คำสั่งจะส่งออกเป็น JSON</p><dd></dd>
    <dt id="banshee-ca-export--help"><a href="#banshee-ca-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Piped Input</h3>

<p><code>banshee ca export</code> รับเฉพาะ input ที่ pipe มาเท่านั้น โดยจะนำ JSON array ที่ <a href="#banshee-ca-search"><code>banshee ca search</code></a> สร้างขึ้นมาดึง alert ID และดึงข้อมูล alert แต่ละรายการแบบเต็ม การรันคำสั่งโดยไม่มี pipe จะถูกปฏิเสธพร้อมข้อผิดพลาด</p>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s New | banshee ca export --csv > alerts.csv
</code></pre>

## banshee entity

ค้นหาและดูข้อมูล entity ของ Recorded Future

<h3 class="commands-reference">Usage</h3>

```
banshee entity [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-entity-lookup"><code>banshee entity lookup</code></a></dt><dd><p>ดูข้อมูล entity ตาม ID</p></dd>
    <dt><a href="#banshee-entity-search"><code>banshee entity search</code></a></dt><dd><p>ค้นหา entity ตามชื่อและ/หรือประเภท</p></dd>
</dl>

### banshee entity lookup

ดูข้อมูล entity ตาม ID

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee entity lookup [OPTIONS] ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--entity-id"><a href="#banshee-entity-lookup--entity-id"<code>ENTITY_ID</code></a></dt><dd><p>Entity ID ที่ต้องการดูข้อมูล</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-lookup--pretty"><a href="#banshee-entity-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-entity-lookup--help"><a href="#banshee-entity-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee entity search

ค้นหา entity ตามชื่อและ/หรือประเภท

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee entity search [OPTIONS] NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--name"><a href="#banshee-entity-search--name"><code>NAME</code></a></dt><dd><p>ชื่อของ entity ที่ต้องการค้นหา</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-entity-search--type"><a href="#banshee-entity-search--type"><code>--type</code>, <code>-t</code></a> <i>entity-type</i></dt><dd>
    <p>ประเภท entity ที่ต้องการค้นหา</p>
    <p>สามารถระบุได้หลายครั้งสำหรับประเภท entity ที่แตกต่างกัน</p>
    <p>ค่าที่รองรับ:</p>
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
    <p>จำกัดจำนวนผลลัพธ์</p>
    <p>ค่าสูงสุดคือ 100</p>
    <p>ค่าเริ่มต้นคือ 100</p><dd></dd>
    <dt id="banshee-entity-search--pretty"><a href="#banshee-entity-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-entity-search--help"><a href="#banshee-entity-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>


## banshee email

เสริมข้อมูลไฟล์อีเมล (EML) ด้วย Recorded Future intelligence

<h3 class="commands-reference">Usage</h3>

```
banshee email [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-email-enrich"><code>banshee email enrich</code></a></dt><dd><p>เสริมข้อมูลไฟล์อีเมล (EML) ด้วย Recorded Future intelligence</p></dd>
</dl>

### banshee email enrich

เสริมข้อมูลไฟล์อีเมล (EML) ด้วย Recorded Future Intelligence คำสั่งนี้จะแยกวิเคราะห์ไฟล์ EML เพื่อดึง IP address จาก header และ URL (ที่ขึ้นต้นด้วย `http`/`https`) ที่พบใน body จากนั้นเสริมข้อมูลด้วย threat intelligence โดยค่าเริ่มต้น ผลลัพธ์จะถูกกรองเพื่อแสดงเฉพาะ indicator ที่ผ่านเกณฑ์ risk score ของคุณ ใช้ `--threat-hunt` เพื่อรวม indicator ที่เชื่อมโยงกับ threat actor แม้ว่าจะต่ำกว่าเกณฑ์ risk score

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">JSON Output</h3>

แต่ละ object ในผลลัพธ์ JSON array ประกอบด้วยฟิลด์ดังต่อไปนี้:

| Field | Description |
|---|---|
| `ioc` | indicator ที่ดึงจากอีเมล — เป็น IP address หรือ URL |
| `type` | ประเภทของ indicator เช่น `ip` หรือ `url` |
| `location` | ส่วนของอีเมลที่พบ indicator เช่น `header` หรือ `body` |
| `risk_score` | Recorded Future risk score |
| `ta_names` | รายชื่อ threat actor ที่เกี่ยวข้องกับ indicator นี้ ว่างหากไม่มีข้อมูล |
| `malwares` | รายชื่อ malware family ที่เชื่อมโยงกับ indicator นี้ ว่างหากไม่มีข้อมูล |
| `first_seen` | timestamp รูปแบบ ISO 8601 ของการพบเห็นครั้งแรกที่บันทึกไว้ |
| `last_seen` | timestamp รูปแบบ ISO 8601 ของการพบเห็นล่าสุดที่บันทึกไว้ |
| `count_of_analyst_notes` | จำนวน analyst note ของ Recorded Future ที่อ้างอิงถึง indicator นี้ |
| `rule_evidence` | อาร์เรย์ของรายละเอียด evidence ของ risk rule แต่ละรายการ เรียงลำดับจาก severity สูงสุดก่อน |

แต่ละ object ใน `rule_evidence` array ประกอบด้วย:

| Field | Description |
|---|---|
| `rule` | ชื่อของ Recorded Future risk rule เฉพาะที่ถูก trigger |
| `level` | ระดับ severity ของ rule นี้ — ตัวเลขที่สูงกว่าหมายถึง severity ที่มากกว่า |
| `timestamp` | timestamp รูปแบบ ISO 8601 ของการพบเห็นล่าสุดสำหรับ rule นี้ |
| `evidence_string` | สรุป evidence ที่อ่านได้โดยมนุษย์ |

<h3 class="commands-reference">Usage</h3>

```
banshee email enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--file-path"><a href="#banshee-email-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>Path ของไฟล์ EML ที่ต้องการเสริมข้อมูล</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-email-enrich--risk-score"><a href="#banshee-email-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>กรองผลลัพธ์เพื่อแสดงเฉพาะ indicator ที่มี risk score (0 - 99) สูงกว่าเกณฑ์นี้</p><p>ค่าเริ่มต้นคือ 65</p></dd>
    <dt id="banshee-email-enrich--threat-hunt"><a href="#banshee-email-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>รวม indicator ที่เชื่อมโยงกับ threat actor โดยไม่คำนึงถึงเกณฑ์ risk score</p></dd>
    <dt id="banshee-email-enrich--pretty"><a href="#banshee-email-enrich--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-email-enrich--help"><a href="#banshee-email-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code class="language-bash">
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p
banshee email enrich suspicious.eml --threat-hunt
</code></pre>

### banshee email extract-attachments

แยก attachment จากไฟล์อีเมล (EML) บีบอัดเข้า ZIP ที่มีรหัสผ่าน (รหัสผ่าน `infected`) และส่ง archive ดังกล่าวไปยัง Recorded Future Sandbox เพื่อวิเคราะห์ รอจนกว่าการวิเคราะห์ใน sandbox จะเสร็จสมบูรณ์ก่อนแสดงสรุป ได้แก่ สถานะปัจจุบัน คะแนนรวม เป้าหมาย timestamps การสร้างและเสร็จสิ้น SHA256 และรายละเอียดแต่ละ task

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee email extract-attachments [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-email-extract-attachments--file-path"><a href="#banshee-email-extract-attachments--file-path"><code>FILE_PATH</code></a></dt><dd><p>Path ของไฟล์ EML ที่ต้องการแยก attachment</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-email-extract-attachments--zip-path"><a href="#banshee-email-extract-attachments--zip-path"><code>--zip-path</code></a>, <code>-z</code> <i>zip-path</i></dt><dd>
    <p>ระบุ path แบบกำหนดเองสำหรับบันทึก archive ที่มีไฟล์ที่แยกออกมา</p>
    <p>ค่าเริ่มต้นคือ directory ปัจจุบัน</p></dd>
    <dt id="banshee-email-extract-attachments--pretty"><a href="#banshee-email-extract-attachments--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-email-extract-attachments--help"><a href="#banshee-email-extract-attachments--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee email extract-attachments phishing_email.eml
banshee email extract-attachments phishing_email.eml -p -z ../sandbox/files.zip
</code></pre>

## banshee ioc

ค้นหาและดูข้อมูล Indicators of Compromise (IOC)

<h3 class="commands-reference">Usage</h3>

```
banshee ioc [OPTIONS] COMMAND [ARGS]...
```
<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-ioc-lookup"><code>banshee ioc lookup</code></a></dt><dd><p>เสริมข้อมูลแบบละเอียดสำหรับ IOC หนึ่งรายการหรือมากกว่า พร้อมกำหนดระดับข้อมูลได้</p></dd>
    <dt><a href="#banshee-ioc-bulk-lookup"><code>banshee ioc bulk-lookup</code></a></dt><dd><p>เสริมข้อมูลแบบ bulk อย่างรวดเร็ว ส่งคืน risk score และ rule ที่ถูก trigger — ประมวลผลครั้งละสูงสุด 1,000 IOC ต่อการเรียก API</p></dd>
    <dt><a href="#banshee-ioc-search"><code>banshee ioc search</code></a></dt><dd><p>ค้นหา IOC</p></dd>
    <dt><a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></dt><dd><p>ค้นหา IOC rules</p></dd>
</dl>

### banshee ioc lookup

เสริมข้อมูลแบบละเอียดสำหรับ IOC หนึ่งรายการหรือมากกว่า — หนึ่งการเรียก API ต่อ indicator ใช้ [`--verbosity`](#banshee-ioc-lookup--verbosity) เพื่อควบคุมจำนวนฟิลด์ที่ส่งคืน ตั้งแต่ risk score พื้นฐานจนถึง intel ครบถ้วน รวมถึง links, analyst notes และอื่น ๆ ใช้เมื่อต้องการบริบทที่ละเอียด

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ioc lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>ประเภท entity ที่ต้องการดูข้อมูล</p>
    <p>ค่าที่รองรับ: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-lookup--ioc"><a href="#banshee-ioc-lookup--ioc"><code>IOC</code></a></dt><dd><p>IOC หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่าง</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--ai-insights"><a href="#banshee-ioc-lookup--ai-insights"><code>--ai-insights</code></a>,  <code>-a</code></dt><dd>
    <p>เปิดใช้งาน AI insights จาก Recorded Future ที่สรุป risk rules ที่เกี่ยวข้องและเอกสารอ้างอิงสำคัญ</p>
    <p><strong>หมายเหตุ:</strong> เวลาตอบสนองอาจช้าลงเล็กน้อยเนื่องจากการประมวลผล AI</p<dd></dd>
    <dt id="banshee-ioc-lookup--verbosity"><a href="#banshee-ioc-lookup--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>ควบคุมปริมาณข้อมูลที่ส่งคืนในการตอบสนอง (1-5) ระดับ verbosity ที่สูงขึ้นจะรวมฟิลด์และรายละเอียดเพิ่มเติมใน JSON output</p>
    <p><strong>หมายเหตุ:</strong> ระดับ verbosity ที่สูงขึ้นอาจส่งผลให้เวลาตอบสนองช้าลงเนื่องจากการดึงข้อมูลที่มากขึ้น</p>
    <p>ค่าเริ่มต้นคือ 1</p>
    <h4>ฟิลด์ที่มีตามระดับ Verbosity</h4>
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
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ioc-lookup--help"><a href="#banshee-ioc-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23,139.224.189.177 -p
</code></pre>

Pipe รายการ IOC ที่คั่นด้วยเครื่องหมายจุลภาคหรือขึ้นบรรทัดใหม่เพื่อดูข้อมูล:

<pre><code>
cat test_ips.csv| banshee ioc lookup ip -p
</code></pre>


### banshee ioc bulk-lookup

เสริมข้อมูลแบบ bulk อย่างรวดเร็วสำหรับ IOC จำนวนเท่าใดก็ได้ในประเภทเดียว คำสั่งจะแบ่งกลุ่มสูงสุด 1,000 IOC ต่อการเรียก API และจัดการการแบ่งกลุ่มโดยอัตโนมัติ ทำให้เร็วกว่า [`banshee ioc lookup`](#banshee-ioc-lookup) อย่างมากสำหรับปริมาณข้อมูลจำนวนมาก

ส่งคืนชุดฟิลด์ที่กำหนดไว้สำหรับแต่ละ indicator ได้แก่ risk score และ risk rules ที่ถูก trigger เหมาะสำหรับการ triage ปริมาณสูง

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ioc bulk-lookup [OPTIONS] ENTITY_TYPE IOC...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--entity-type"><a href="#banshee-ioc-bulk-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>ประเภท entity ที่ต้องการเสริมข้อมูล</p>
    <p>ค่าที่รองรับ: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p>
    </dd>
    <dt id="banshee-ioc-bulk-lookup--ioc"><a href="#banshee-ioc-bulk-lookup--ioc"><code>IOC</code></a></dt><dd><p>IOC หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่าง รับ input จาก stdin ด้วย (ดูตัวอย่างด้านล่าง)</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-bulk-lookup--pretty"><a href="#banshee-ioc-bulk-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ioc-bulk-lookup--help"><a href="#banshee-ioc-bulk-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>
<pre><code>
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877
</code></pre>

<h4>File / Stdin Input</h4>

Pipe หรือ redirect ไฟล์ IOC ที่มีรายการแยกตามบรรทัด (หนึ่งรายการต่อบรรทัด):

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
ใช้ `jq` เพื่อดึงฟิลด์เฉพาะจาก JSON output เช่น:

<pre><code>
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'
</code></pre>


### banshee ioc search

ค้นหา Classic Alerts

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ioc search [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-lookup--entity-type"><a href="#banshee-ioc-lookup--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>ประเภท entity ที่ต้องการดูข้อมูล</p>
    <p>ค่าที่รองรับ: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-search--limit"><a href="#banshee-ioc-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>จำกัดจำนวนผลลัพธ์</p>
    <p>ค่าสูงสุดคือ 1,000</p>
    <p>ค่าเริ่มต้นคือ 5</p><dd></dd>
    <dt id="banshee-ioc-search--risk-score"><a href="#banshee-ioc-search--risk-score"><code>--risk-score</code>, <code>-r</code></a> <i>risk-score</i></dt><dd>
    <p>กรองตามช่วง risk score เช่น:</p>
    <p>
        <ul>
            <li><code>--risk-score '[20,90]'</code> &rarr; เทียบเท่า <code>20 &lt;= riskScore &lt;= 90</code></li>
            <li><code>--risk-score '(20,90)'</code> &rarr; เทียบเท่า <code>20 &lt; riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,90)'</code> &rarr; เทียบเท่า <code>20 &lt;= riskScore &lt; 90</code></li>
            <li><code>--risk-score '[20,)'</code> &rarr; เทียบเท่า <code>20 &lt;= riskScore</code></li>
            <li><code>--risk-score '[,90)'</code> &rarr; เทียบเท่า <code>riskScore &lt; 90</code></li>
        </ul>
    </p>
    <p>ล้อมรอบช่วง risk score ด้วยเครื่องหมายคำพูดเพื่อให้แยกวิเคราะห์ได้ถูกต้อง</p>
    <dd></dd>
    <dt id="banshee-ioc-search--risk-rule"><a href="#banshee-ioc-search--risk-rule"><code>--risk-rule</code>, <code>-R</code></a> <i>rule-name</i></dt><dd>
    <p>กรองตามชื่อ risk rule</p>
    <p>สำหรับตัวเลือกที่มี โปรดดูที่<a href="https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future" target="_blank">บทความสนับสนุน</a>นี้ โดยเฉพาะคอลัมน์ <b>Machine Name</b> ในตาราง risk rules หรือใช้คำสั่ง <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a></p><dd></dd>
    <dt id="banshee-ioc-search--verbosity"><a href="#banshee-ioc-search--verbosity"><code>--verbosity</code></a>,  <code>-v</code> <i>verbosity-level</i></dt><dd>
    <p>ควบคุมปริมาณข้อมูลที่ส่งคืนในการตอบสนอง (1-5) ระดับ verbosity ที่สูงขึ้นจะรวมฟิลด์และรายละเอียดเพิ่มเติมใน JSON output</p>
    <p><strong>หมายเหตุ:</strong> ระดับ verbosity ที่สูงขึ้นอาจส่งผลให้เวลาตอบสนองช้าลงเนื่องจากการดึงข้อมูลที่มากขึ้น</p>
    <p>ค่าเริ่มต้นคือ 1</p>
    <h4>ฟิลด์ที่มีตามระดับ Verbosity</h4>
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
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ioc-search--help"><a href="#banshee-ioc-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee ioc rules

ค้นหา IOC rules สำหรับประเภท entity ที่กำหนด

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee ioc rules [OPTIONS] ENTITY_TYPE
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--entity-type"><a href="#banshee-ioc-rules--entity-type"><code>ENTITY_TYPE</code></a></dt><dd>
    <p>ประเภท entity ของ IOC rules</p>
    <p>ค่าที่รองรับ: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code></p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-ioc-rules--freetext"><a href="#banshee-ioc-rules--freetext"><code>--freetext</code>, <code>-F</code></a> <i>freetext-rule-name</i></dt><dd>
    <p>กรองตามชื่อ risk rule โดยใช้การค้นหาแบบ freetext</p><dd></dd>
    <dt id="banshee-ioc-rules--mitre"><a href="#banshee-ioc-rules--mitre"><code>--mitre-code</code>, <code>-M</code></a> <i>mitre-code</i></dt><dd>
    <p>กรองตามรหัส MITRE ATT&CK</p><dd></dd>
    <dt id="banshee-ioc-rules--criticality"><a href="#banshee-ioc-rules--criticality"><code>--criticality</code>, <code>-C</code></a> <i>criticality</i></dt><dd>
    <p>กรองตามระดับความรุนแรง ค่าที่สูงกว่าหมายถึงความรุนแรงที่มากกว่า</p>
    <p>ค่าที่รับได้คือ 1 ถึง 5</p>
    <p><strong>ระดับความรุนแรง (IP, Domain, URL, Hash)</strong></p>
    <ul>
        <li><code>4</code> – Very Malicious (ช่วง Risk Score: 90–99)</li>
        <li><code>3</code> – Malicious (ช่วง Risk Score: 65–89)</li>
        <li><code>2</code> – Suspicious (ช่วง Risk Score: 25–64)</li>
        <li><code>1</code> – Unusual (ช่วง Risk Score: 5–24)</li>
        <li><code>0</code> – ไม่มีหลักฐานความเสี่ยง (ช่วง Risk Score: 0)</li>
    </ul>
    <p><strong>ระดับความรุนแรง (Vulnerability)</strong></p>
    <ul>
        <li><code>5</code> – Very Critical (ช่วง Risk Score: 90–99)</li>
        <li><code>4</code> – Critical (ช่วง Risk Score: 80–89)</li>
        <li><code>3</code> – High (ช่วง Risk Score: 65–79)</li>
        <li><code>2</code> – Medium (ช่วง Risk Score: 25–64)</li>
        <li><code>1</code> – Low (ช่วง Risk Score: 5–24)</li>
        <li><code>0</code> – ไม่มีหลักฐานความเสี่ยง (ช่วง Risk Score: 0)</li>
    </ul>
    <dd></dd>
    <dt id="banshee-ioc-rules--pretty"><a href="#banshee-ioc-rules--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-ioc-rules--help"><a href="#banshee-ioc-rules--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

## banshee list

จัดการ Recorded Future lists และ Watch lists

<h3 class="commands-reference">Usage</h3>

```
banshee list [OPTIONS] COMMAND [ARGS]...
```
<dl class="commands-reference">
    <dt><a href="#banshee-list-create"><code>banshee list create</code></a></dt><dd><p>สร้าง list ใหม่</p></dd>
    <dt><a href="#banshee-list-info"><code>banshee list info</code></a></dt><dd><p>ดูข้อมูลพื้นฐานของ list</p></dd>
    <dt><a href="#banshee-list-search"><code>banshee list search</code></a></dt><dd><p>ค้นหา list</p></dd>
    <dt><a href="#banshee-list-status"><code>banshee list status</code></a></dt><dd><p>ดูสถานะของ list</p></dd>
    <dt><a href="#banshee-list-entities"><code>banshee list entities</code></a></dt><dd><p>ดู entity ใน list</p></dd>
    <dt><a href="#banshee-list-add"><code>banshee list add</code></a></dt><dd><p>เพิ่ม entity เข้า list</p></dd>
    <dt><a href="#banshee-list-bulk-add"><code>banshee list bulk-add</code></a></dt><dd><p>เพิ่ม entity หลายรายการเข้า list พร้อมกัน</p></dd>
    <dt><a href="#banshee-list-remove"><code>banshee list remove</code></a></dt><dd><p>ลบ entity ออกจาก list</p></dd>
    <dt><a href="#banshee-list-bulk-remove"><code>banshee list bulk-remove</code></a></dt><dd><p>ลบ entity หลายรายการออกจาก list พร้อมกัน</p></dd>
    <dt><a href="#banshee-list-copy"><code>banshee list copy</code></a></dt><dd><p>คัดลอก entity จาก list หนึ่งไปยังอีก list หนึ่ง</p></dd>
    <dt><a href="#banshee-list-clear"><code>banshee list clear</code></a></dt><dd><p>ล้าง entity ทั้งหมดออกจาก list</p></dd>
    <dt><a href="#banshee-list-entries"><code>banshee list entries</code></a></dt><dd><p>ดูรายการข้อความใน list</p></dd>
</dl>

### banshee list create

สร้าง list ใหม่

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list create [OPTIONS] NAME [LIST_TYPE]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>NAME</code></a></dt><dd><p>ชื่อ list ที่ต้องการสร้าง</p></dd>
    <dt id="banshee-list-lookup--alert-id"><a href="#banshee-list-lookup--alert-id"<code>LIST_TYPE</code></a></dt><dd><p>ประเภท list ที่ต้องการสร้าง</p>
    <p>ประเภทที่รองรับ:</p>
    <ul>
        <li><code>entity</code></li>
        <li><code>source</code></li>
        <li><code>text</code></li>
    </ul>
    <p>ค่าเริ่มต้นคือ <code>entity</code></p>
    </dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-lookup--pretty"><a href="#banshee-list-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-lookup--help"><a href="#banshee-list-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list info

ดูข้อมูลของ list เช่น ชื่อ ประเภท timestamps และรายละเอียดเจ้าของ

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list info [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการดูข้อมูล</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list search

ค้นหา list

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list search [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--name"><a href="#banshee-list-search--name"><code>NAME</code></a></dt><dd>
    <p>ชื่อ list ที่ต้องการค้นหา</p>
    <p>หากไม่ระบุชื่อ จะส่งคืน list ทั้งหมด</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-search--list-type"><a href="#banshee-list-search--list-type"><code>--list-type</code>, <code>-t</code></a> <i>list-type</i></dt><dd>
    <p>กรองตามประเภท list</p>
    <p>ประเภทที่รองรับ:</p>
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
    <p>จำกัดจำนวนผลลัพธ์</p>
    <p>ค่าสูงสุดคือ 3,000</p>
    <p>ค่าเริ่มต้นคือ 1,000</p><dd></dd>
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list status

ดูสถานะ list และจำนวน entity

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list status [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการดูสถานะ</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list entities

ดู entity ใน list

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list entities [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการดึง entity</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>


### banshee list entries

ดูรายการข้อความใน list

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee list entries [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการดึงรายการข้อความ</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--pretty"><a href="#banshee-list-info--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>



### banshee list clear

ล้าง list และลบ entity ทั้งหมดออกอย่างสมบูรณ์ โปรดทราบว่าคำสั่งนี้จะไม่ล้างรายการข้อความและไม่รองรับการดำเนินการดังกล่าว

<h3 class="commands-reference">Usage</h3>

```
banshee list clear [OPTIONS] LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--list-id"><a href="#banshee-list-info--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการล้าง</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-info--help"><a href="#banshee-list-info--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list add

เพิ่ม entity เข้า list

<h3 class="commands-reference">Usage</h3>

```
banshee list add [OPTIONS] LIST_ID ENTITY_ID [PROPERTIES]
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--list-id"><a href="#banshee-list-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการเพิ่มเข้า</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
    <dt id="banshee-list-add--entity-id"><a href="#banshee-list-add--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>Entity ID หรือชื่อพร้อมประเภทที่ต้องการเพิ่มเข้า list เช่น:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul></dd>
    <dt id="banshee-list-add--properties"><a href="#banshee-list-add--properties"><code>PROPERTIES</code></a></dt><dd>
    <p>ไม่บังคับ ใช้ <code>annotation=&lt;text&gt;</code> เพื่อแนบบันทึกที่จะแสดงบน Recorded Future platform สำหรับ entity นี้</p>
    <p>ล้อมรอบค่าด้วยเครื่องหมายคำพูดหากมีช่องว่าง</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-add--help"><a href="#banshee-list-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
</code></pre>

### banshee list bulk-add

เพิ่ม entity หลายรายการเข้า list

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-add [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--list-id"><a href="#banshee-list-bulk-add--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการเพิ่มเข้า</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
    <dt id="banshee-list-bulk-add--entity-input"><a href="#banshee-list-bulk-add--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>Entity หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่างหรือขึ้นบรรทัดใหม่ เช่น:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>คำสั่งยังรับ input จาก stdin ด้วย สมมติว่า 'entities.txt' เป็นไฟล์ที่มี entity แยกตามบรรทัด เช่น:</p>
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
    <p>จากข้างต้น สามารถรันคำสั่งใดคำสั่งหนึ่งต่อไปนี้เพื่อเพิ่ม entity แบบ bulk:</p>
    <pre><code>
    $ banshee list bulk-add LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-add LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-add--overwrite"><a href="#banshee-list-bulk-add--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>เปิดใช้งานโหมด overwrite เมื่อตั้งค่านี้ คำสั่งจะ:</p>
    <ul>
        <li>คงไว้ซึ่ง entity ที่มีอยู่ใน list ที่ปรากฏในไฟล์ที่ระบุ</li>
        <li>เพิ่ม entity ใหม่จากไฟล์ที่ระบุที่ยังไม่มีใน list</li>
        <li>ลบ entity ที่มีอยู่ใน list ที่ <strong>ไม่</strong> ปรากฏในไฟล์ที่ระบุ</li>
    </ul>
    <p>โดยค่าเริ่มต้น (ไม่มี flag นี้) คำสั่งจะเพิ่ม entity ใหม่เข้า list ที่มีอยู่โดยไม่ลบสิ่งใด</p>
    </dd>
    <dt id="banshee-list-bulk-add--help"><a href="#banshee-list-bulk-add--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Result Status Output</h3>

<p><code>banshee list bulk-add</code> จัดกลุ่ม output ตามสถานะและแสดง entity ที่ตรงกันใต้สถานะนั้น เช่น:</p>

<pre><code class="language-text">
ADDED:
SoA6SP

ERROR_MULTIPLE_MATCHES:
wanna:malware
</code></pre>

<p>สถานะทั่วไป:</p>
<ul>
    <li><code>ADDED</code> - เพิ่ม entity เข้า list สำเร็จ</li>
    <li><code>UNCHANGED</code> - Entity มีอยู่ใน list แล้ว (ไม่มีการเปลี่ยนแปลง)</li>
    <li><code>UPDATED</code> - Entity มีอยู่แล้วและถูกอัปเดตโดย API</li>
    <li><code>ERROR_BAD_ID</code> - รูปแบบ input ไม่ถูกต้องหรือ entity reference ไม่ถูกต้อง</li>
    <li><code>ERROR_NOT_FOUND</code> - ไม่พบ entity ที่ตรงกัน</li>
    <li><code>ERROR_NOT_ALLOWED</code> - ประเภท entity ไม่ได้รับอนุญาตใน list ที่ระบุ</li>
    <li><code>ERROR_MULTIPLE_MATCHES</code> - Input ตรงกับ entity ที่เป็นไปได้มากกว่าหนึ่งรายการ <strong>Entity ไม่ได้ถูกเพิ่ม</strong></li>
    <li><code>LIST_MAX_SIZE_REACHED</code> - List ที่ระบุเต็มและไม่สามารถเพิ่ม entity ได้อีก</li>
</ul>

<h3 class="commands-reference">How to Resolve <code>ERROR_MULTIPLE_MATCHES</code></h3>

<p>เมื่อพบ <code>ERROR_MULTIPLE_MATCHES</code> หมายความว่าชื่อ entity ที่ระบุไม่ชัดเจน API ไม่สามารถระบุ entity เดียวได้อย่างแน่ชัด ดังนั้น row นั้นจะถูกข้ามและไม่ถูกเพิ่ม</p>

<p>ขั้นตอนที่แนะนำ:</p>
<ol>
    <li>นำค่าที่ไม่ชัดเจนจาก output ของคำสั่ง</li>
    <li>รัน <code>banshee entity search</code> เพื่อค้นหา entity ที่ต้องการ หากจำเป็น ปรับวิธีการเขียนชื่อในคำค้นหา (เช่น การสะกดที่ต่างกัน ช่องว่าง หรือรูปแบบที่เฉพาะเจาะจงกว่า) เพื่อจำกัดผลลัพธ์</li>
    <li>แทนที่ค่าที่ไม่ชัดเจนในไฟล์ input ด้วย entity ID ที่แน่ชัด</li>
    <li>รัน <code>banshee list bulk-add</code> อีกครั้งด้วยไฟล์ที่แก้ไขแล้ว</li>
</ol>

<p>ตัวอย่าง:</p>
<pre><code class="language-bash">
banshee entity search wannacry --type Malware
banshee list bulk-add LIST_ID &lt; entities.txt
</code></pre>

<p>เคล็ดลับ: หากทราบ entity ID แล้ว (เช่น <code>SoA6SP</code>) ควรใช้ ID แทนคู่ชื่อ/ประเภทในไฟล์ bulk เพื่อหลีกเลี่ยงความไม่ชัดเจน</p>

### banshee list remove

ลบ entity ออกจาก list

<h3 class="commands-reference">Usage</h3>

```
banshee list remove [OPTIONS] LIST_ID ENTITY_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--list-id"><a href="#banshee-list-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการลบออกจาก</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
    <dt id="banshee-list-remove--entity-id"><a href="#banshee-list-remove--entity-id"><code>ENTITY_ID</code></a></dt><dd>
    <p>Entity ID ที่ต้องการลบออกจาก list</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-remove--help"><a href="#banshee-list-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list bulk-remove

ลบ entity หลายรายการออกจาก list

<h3 class="commands-reference">Usage</h3>

```
banshee list bulk-remove [OPTIONS] LIST_ID ENTITY_INPUT...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--list-id"><a href="#banshee-list-bulk-remove--list-id"><code>LIST_ID</code></a></dt><dd>
    <p>List ID ที่ต้องการลบออกจาก</p>
    <p>List ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>report:</strong>'</p></dd>
    <dt id="banshee-list-bulk-remove--entity-input"><a href="#banshee-list-bulk-remove--entity-input"><code>ENTITY_INPUT</code></a></dt><dd>
    <p>Entity หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่างหรือขึ้นบรรทัดใหม่ เช่น:</p> 
    <ul>
        <li>SoA6SP</li>
        <li>wannacry,Malware</li>
        <li>www.duckdns.org,InternetDomainName</li>
    </ul>
    <p>คำสั่งยังรับ input จาก stdin ด้วย สมมติว่า 'entities.txt' เป็นไฟล์ที่มี entity แยกตามบรรทัด เช่น:</p>
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
    <p>จากข้างต้น สามารถรันคำสั่งใดคำสั่งหนึ่งต่อไปนี้เพื่อลบ entity แบบ bulk:</p>
    <pre><code>
    $ banshee list bulk-remove LIST_ID < entities.txt
    $ cat entities.txt | banshee list bulk-remove LIST_ID
    </code></pre></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-bulk-remove--help"><a href="#banshee-list-bulk-remove--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee list copy

คำสั่งยูทิลิตีสำหรับคัดลอก entity จาก list หนึ่งไปยังอีก list หนึ่ง

entity จาก list ต้นทางจะถูกอ่านและเพิ่มเข้า list ปลายทาง โดยค่าเริ่มต้น entity ใหม่จะถูก append เข้า list ปลายทางโดยไม่แตะต้องสิ่งที่มีอยู่แล้ว เมื่อใช้ `--overwrite` list ปลายทางจะถูกทำให้สอดคล้องกับ list ต้นทาง: entity ที่มีอยู่ในทั้งสอง list จะถูกคงไว้ entity ใหม่จะถูกเพิ่ม และ entity ใดก็ตามที่อยู่ใน list ปลายทางแต่ **ไม่** อยู่ใน list ต้นทางจะถูกลบออก

หาก list ต้นทางว่างเปล่า คำสั่งจะออกโดยไม่แก้ไข list ปลายทาง — แม้เมื่อใช้ `--overwrite`

<h3 class="commands-reference">Usage</h3>

```
banshee list copy [OPTIONS] SOURCE_LIST_ID DESTINATION_LIST_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--source-list-id"><a href="#banshee-list-copy--source-list-id"><code>SOURCE_LIST_ID</code></a></dt><dd>
    <p>ID ของ list ที่ต้องการคัดลอก entity จาก</p></dd>
    <dt id="banshee-list-copy--destination-list-id"><a href="#banshee-list-copy--destination-list-id"><code>DESTINATION_LIST_ID</code></a></dt><dd>
    <p>ID ของ list ที่ต้องการคัดลอก entity ไปยัง</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-list-copy--overwrite"><a href="#banshee-list-copy--overwrite"><code>--overwrite</code></a>, <code>-o</code></dt><dd>
    <p>โหมด Overwrite: คงไว้ซึ่ง entity ที่มีอยู่ใน list ปลายทางแล้ว เพิ่ม entity ใหม่ และลบ entity ใดก็ตามที่อยู่ใน list ปลายทางแต่ไม่อยู่ใน list ต้นทาง โดยค่าเริ่มต้น คำสั่งจะ append entity ใหม่โดยไม่ลบที่มีอยู่</p></dd>
    <dt id="banshee-list-copy--help"><a href="#banshee-list-copy--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Examples</h3>

```
$ banshee list copy 1b0s1q 21YKUC
$ banshee list copy 1b0s1q 21YKUC --overwrite
```

## banshee pba

ค้นหา ดูข้อมูล และอัปเดต Recorded Future Playbook Alerts

<h3 class="commands-reference">Usage</h3>

```
banshee pba [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pba-lookup"><code>banshee pba lookup</code></a></dt><dd><p>ดูข้อมูล Playbook Alert</p></dd>
    <dt><a href="#banshee-pba-search"><code>banshee pba search</code></a></dt><dd><p>ค้นหา Playbook Alerts</p></dd>
    <dt><a href="#banshee-pba-update"><code>banshee pba update</code></a></dt><dd><p>อัปเดต Playbook Alert หนึ่งรายการหรือมากกว่า</p></dd>
    <dt><a href="#banshee-pba-export"><code>banshee pba export</code></a></dt><dd><p>ส่งออก Playbook Alerts เป็น JSON หรือ CSV</p></dd>
</dl>

### banshee pba lookup

ดูข้อมูล Playbook Alert

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee pba lookup [OPTIONS] ALERT_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--alert-id"><a href="#banshee-pba-lookup--alert-id"<code>ALERT_ID</code></a></dt><dd><p>Alert ID ที่ต้องการดูข้อมูล</p>
    <p>Alert ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>task:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-lookup--pretty"><a href="#banshee-pba-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-pba-lookup--help"><a href="#banshee-pba-lookup--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee pba search

ค้นหา Playbook Alerts

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee pba search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-search--created"><a href="#banshee-pba-search--created"><code>--created</code>, <code>-C</code></a> <i>created-from</i></dt><dd>
    <p>กรองตามเวลาที่สร้างจาก เช่น: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--updated"><a href="#banshee-pba-search--updated"><code>--updated</code>, <code>-u</code></a> <i>updated-from</i></dt><dd>
    <p>กรองตามเวลาที่อัปเดตจาก เช่น: 1d; 12h</p><dd></dd>
    <dt id="banshee-pba-search--category"><a href="#banshee-pba-search--category"><code>--category</code>, <code>-c</code></a> <i>category</i></dt><dd>
    <p>กรองตามหมวดหมู่ alert (ระบุได้หลายครั้ง)</p>
    <p>หมวดหมู่ที่รองรับ:</p>
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
    <p>กรองตามลำดับความสำคัญของ alert (ระบุได้หลายครั้ง)</p>
    <p>ค่าที่เป็นไปได้: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p>
    <p>ค่าเริ่มต้นคือทุกลำดับความสำคัญ</p><dd></dd>
    <dt id="banshee-pba-search--status"><a href="#banshee-pba-search--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>กรองตามสถานะของ alert (ระบุได้หลายครั้ง)</p>
    <p>ค่าที่เป็นไปได้: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p>
    <p>ค่าเริ่มต้นคือทุกสถานะ</p><dd></dd>
    <dt id="banshee-pba-search--entity"><a href="#banshee-pba-search--entity"><code>--entity</code></a>,  <code>-e</code> <i>entity</i></dt><dd>
    <p>กรอง alert ตาม entity ที่เกี่ยวข้อง (ระบุได้หลายครั้ง) เช่น: <code>-e idn:recordedfuture.com -e idn:example.com</code></p><dd></dd>
    <dt id="banshee-pba-search--org-id"><a href="#banshee-pba-search--org-id"><code>--org-id</code></a>,  <code>-o</code> <i>organisation-id</i></dt><dd>
    <p>กรอง alert ตาม ID ขององค์กรเจ้าของ (ระบุได้หลายครั้ง)</p>
    <p>รับค่า ID 10 อักขระ หรือรูปแบบ <code>uhash:</code> 16 อักขระ เช่น: <code>-o 69sKLfTGsS -o uhash:5zQaSyRpA1</code></p><dd></dd>
    <dt id="banshee-pba-search--limit"><a href="#banshee-pba-search--limit"><code>--limit</code>, <code>-l</code></a> <i>limit</i></dt><dd>
    <p>จำกัดจำนวนผลลัพธ์</p>
    <p>ค่าสูงสุดคือ 10,000</p>
    <p>ค่าเริ่มต้นคือ 100</p><dd></dd>
    <dt id="banshee-pba-search--pretty"><a href="#banshee-pba-search--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-pba-search--help"><a href="#banshee-pba-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

### banshee pba update

อัปเดต Playbook Alert หนึ่งรายการหรือมากกว่า

<h3 class="commands-reference">Usage</h3>

```
banshee pba update [OPTIONS] ALERT_IDS...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--alert-id"><a href="#banshee-pba-update--alert-id"<code>ALERT_IDS</code></a></dt><dd>
    <p>Alert ID หนึ่งรายการหรือมากกว่า คั่นด้วยช่องว่าง</p>
    <p>Alert ID สามารถระบุได้ทั้งแบบมีและไม่มี prefix '<strong>task:</strong>'</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-update--status"><a href="#banshee-pba-update--status"><code>--status</code></a>,  <code>-s</code> <i>alert-status</i></dt><dd>
    <p>อัปเดต alert ไปยังสถานะที่ระบุ</p>
    <p>ค่าที่เป็นไปได้: <code>New</code>, <code>InProgress</code>, <code>Dismissed</code>, <code>Resolved</code></p><dd></dd>
    <dt id="banshee-pba-update--reopen"><a href="#banshee-pba-update--reopen"><code>--reopen</code></a>,  <code>-r</code> <i>reopen</i></dt><dd>
    <p>กลยุทธ์การเปิดใหม่สามารถใช้ได้เฉพาะกับ alert ที่มีสถานะ Dismissed หรือ Resolved เท่านั้น การผสมสถานะ/การเปิดใหม่ที่อนุญาต: <code>Dismissed -> Never</code>; <code>Resolved -> Never</code>; <code>Resolved -> SignificantUpdates</code></p>
    <p>ค่าที่รองรับ: <code>Never</code>, <code>SignificantUpdates</code></p><dd></dd>
    <dt id="banshee-pba-update--priority"><a href="#banshee-pba-update--priority"><code>--priority</code></a>,  <code>-P</code> <i>priority</i></dt><dd>
    <p>กำหนดลำดับความสำคัญของ alert ใหม่</p>
    <p>ค่าที่เป็นไปได้: <code>Informational</code>, <code>Moderate</code>, <code>High</code></p><dd></dd>
    <dt id="banshee-pba-update--comment"><a href="#banshee-pba-update--comment"><code>--comment</code></a>,  <code>-t</code> <i>comment</i></dt><dd>
    <p>ความคิดเห็นที่จะเพิ่มใน alert เช่น: "Bulk resolved via banshee"</p><dd></dd>
    <dt id="banshee-pba-update--assignee"><a href="#banshee-pba-update--assignee"><code>--assignee</code></a>,  <code>-a</code> <i>assignee</i></dt><dd>
    <p>ผู้ใช้ใหม่ที่ต้องการมอบหมาย alert ให้ รับค่า uhash ของผู้ใช้ เช่น: uhash:3aXZxdkM12</p><dd></dd>
    <dt id="banshee-pba-update--help"><a href="#banshee-pba-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<p>ระบุ alert ID หนึ่งรายการหรือมากกว่า (คั่นด้วยช่องว่าง) และกำหนดตัวเลือกการอัปเดตที่ต้องการ:</p>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Dismissed
banshee pba update ALERT_ID -s InProgress -p High -t "Escalated due to new findings"
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved -a uhash:3aXZxdkM12
</code></pre>

<h3 class="commands-reference">Supplying Alert IDs</h3>

<h4>1. ระบุโดยตรงเป็น arguments (รายการเดียวหรือหลายรายการ):</h4>

<pre><code class="language-bash">
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID -s Resolved
banshee pba update ALERT_ID_1 ALERT_ID_2 -s Resolved
</code></pre>

<h4>2. จากไฟล์หรือ standard input:</h4>

<p>หากมีไฟล์ (เช่น <code>alerts.txt</code>) ที่มี alert ID หนึ่งรายการต่อบรรทัด:</p>

<pre><code class="language-text">
ALERT_ID_1
ALERT_ID_2
ALERT_ID_3
</code></pre>

<p>สามารถอัปเดต alert ทั้งหมดที่ระบุในไฟล์ได้โดยใช้:</p>

<pre><code class="language-bash">
banshee pba update -s Dismissed &lt; alerts.txt
cat alerts.txt | banshee pba update -s Dismissed
</code></pre>

<h4>3. โดย pipe จากคำสั่ง search:</h4>

<p>ใช้เครื่องมืออย่าง <code>jq</code> เพื่อดึง alert ID จากผลการค้นหาและ pipe เข้าสู่คำสั่ง update:</p>

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

ส่งออก Playbook Alerts เป็น JSON หรือ CSV โดยอ่าน alert ID และหมวดหมู่จาก stdin — โดยทั่วไปจะ pipe มาจาก [`banshee pba search`](#banshee-pba-search)

<h3 class="commands-reference">Output Formats</h3>

<p><b>JSON (ค่าเริ่มต้น)</b> — ส่งออก object alert แบบ <i>เต็มรูปแบบ</i> สำหรับแต่ละ ID ตามที่ Recorded Future API ส่งกลับมา ประกอบด้วยฟิลด์ระดับบนสุดทั้งหมด รวมถึงสถานะ panel ที่ซ้อนกัน เป้าหมาย หลักฐาน ผู้รับมอบหมาย timestamps และอื่น ๆ เหมาะสำหรับการนำไปใช้กับเครื่องมือ downstream, <code>jq</code> pipelines หรือการนำเข้าใหม่</p>

<p><b>CSV (<a href="#banshee-pba-export--csv"><code>--csv</code></a>)</b> — ส่งออกสรุประดับสูงสำหรับใช้กับ spreadsheet และการรายงาน โดยเขียนเฉพาะ 12 คอลัมน์ที่ระบุด้านล่าง (โดยมีแถวหัวตารางก่อน) และละเว้นฟิลด์อื่นที่มีอยู่ใน JSON response ทั้งหมด</p>

| Field | Description |
|---|---|
| `ID` | Playbook Alert ID (รวม prefix `task:`) |
| `Priority` | ลำดับความสำคัญของ alert เช่น `Informational`, `Moderate`, `High` |
| `Alert Rule` | ชื่อของ alert rule ที่ถูก trigger (ใช้ rule label หากไม่มีชื่อ) |
| `Status` | สถานะของ alert เช่น `New`, `InProgress`, `Dismissed`, `Resolved` |
| `Created` | timestamp ที่สร้าง (UTC, `%Y-%m-%d %H:%M:%S`) |
| `Updated` | timestamp ที่อัปเดตล่าสุด (UTC, `%Y-%m-%d %H:%M:%S`) |
| `Subject` | หัวเรื่องของ alert |
| `Assignee` | ชื่อที่แสดงของผู้ใช้ที่ได้รับมอบหมาย |
| `Assessments` | การประเมินความเสี่ยง / rules สำหรับ alert (ขึ้นอยู่กับหมวดหมู่) คั่นด้วย `;` |
| `Entities` | ชื่อ entity เป้าหมายที่ไม่ซ้ำกัน คั่นด้วย `;` |
| `Reopen Strategy` | กลยุทธ์การเปิดใหม่สำหรับ alert ที่ปิดแล้ว เช่น `Never`, `SignificantUpdates` |
| `Onwards Actions` | การดำเนินการที่ดำเนินการกับ alert คั่นด้วย `;` |

<h3 class="commands-reference">Usage</h3>

```
banshee pba search [SEARCH_OPTIONS] | banshee pba export [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pba-export--csv"><a href="#banshee-pba-export--csv"><code>--csv</code></a></dt><dd>
    <p>ส่งออกเป็น CSV ด้วยชุดคอลัมน์ที่กำหนดตามที่อธิบายข้างต้น หากไม่ระบุ flag นี้ คำสั่งจะส่งออกเป็น JSON</p><dd></dd>
    <dt id="banshee-pba-export--help"><a href="#banshee-pba-export--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Piped Input</h3>

<p><code>banshee pba export</code> รับเฉพาะ input ที่ pipe มาเท่านั้น โดยจะนำ JSON object ที่ <a href="#banshee-pba-search"><code>banshee pba search</code></a> สร้างขึ้นมาดึง <code>playbook_alert_id</code> และ <code>category</code> ของแต่ละ alert และดึงข้อมูล alert ทุกรายการแบบเต็ม การรันคำสั่งโดยไม่มี pipe จะถูกปฏิเสธพร้อมข้อผิดพลาด</p>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee pba search --created 1d | banshee pba export
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export > identity_alerts.json
banshee pba search --created 1d --category domain_abuse | banshee pba export --csv > domain_alerts.csv
</code></pre>


## banshee pcap

เสริมข้อมูล packet captures (pcap) ด้วย Recorded Future intelligence

<h3 class="commands-reference">Usage</h3>

```
banshee pcap [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-pcap-enrich"><code>banshee pcap enrich</code></a></dt><dd><p>เสริมข้อมูลไฟล์ packet capture (pcap) ด้วย Recorded Future intelligence</p></dd>
</dl>

### banshee pcap enrich

คำสั่งนี้จะแยกวิเคราะห์ไฟล์ pcap เพื่อดึง network indicator เช่น IP address และ domain จากนั้นเสริมข้อมูลด้วย threat intelligence โดยค่าเริ่มต้น ผลลัพธ์จะถูกกรองเพื่อแสดงเฉพาะ indicator ที่ผ่านเกณฑ์ risk score ของคุณ ใช้ `--threat-hunt` เพื่อรวม indicator ที่เชื่อมโยงกับ threat actor แม้ว่าจะต่ำกว่าเกณฑ์ risk score
<br>โปรดทราบว่าการลดเกณฑ์ risk score และ/หรือเปิดใช้งาน threat hunting อาจเพิ่มจำนวนผลลัพธ์และเวลาในการประมวลผลอย่างมีนัยสำคัญ

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">JSON Output</h3>

แต่ละ object ในผลลัพธ์ JSON array ประกอบด้วยฟิลด์ดังต่อไปนี้:

| Field | Description |
|---|---|
| `ioc` | network indicator ที่ดึงจาก pcap — เป็น IP address หรือ domain name |
| `risk_score` | Recorded Future risk score |
| `most_malicious_rule` | ชื่อของ risk rule ที่มี severity สูงสุดที่ส่งผลต่อ risk score |
| `rule_evidence` | อาร์เรย์ของรายละเอียด evidence ของ risk rule แต่ละรายการ เรียงลำดับจาก severity สูงสุดก่อน |
| `ta_names` | รายชื่อ threat actor ที่เกี่ยวข้องกับ IOC นี้ ว่างหากไม่มีข้อมูล |
| `malwares` | รายชื่อ malware family ที่เชื่อมโยงกับ IOC นี้ ว่างหากไม่มีข้อมูล |
| `wireshark_query` | Wireshark display filter ที่พร้อมใช้งานเพื่อแยก traffic ของ IOC นี้ |

แต่ละ object ใน `rule_evidence` array ประกอบด้วย:

| Field | Description |
|---|---|
| `count` | จำนวนแหล่งที่มาที่มีส่วนร่วมในการอ้างอิง risk rule นี้ |
| `description` | สรุป evidence ที่อ่านได้โดยมนุษย์ |
| `level` | ระดับ severity ของ rule นี้ — ตัวเลขที่สูงกว่าหมายถึง severity ที่มากกว่า |
| `mitigation` | อธิบาย white list ที่ IOC อาจปรากฏอยู่ซึ่งลด (หรือบรรเทา) ความเสี่ยงที่เกี่ยวข้อง |
| `rule` | ชื่อของ Recorded Future risk rule เฉพาะที่ถูก trigger |
| `sightings` | จำนวนการพบเห็นแต่ละครั้งที่บันทึกไว้ |
| `timestamp` | timestamp รูปแบบ ISO 8601 ของการพบเห็นล่าสุดสำหรับ rule นี้ |
| `type` | ตัวระบุประเภท |

<h3 class="commands-reference">Usage</h3>


```
banshee pcap enrich [OPTIONS] FILE_PATH
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--file-path"><a href="#banshee-pcap-enrich--file-path"><code>FILE_PATH</code></a></dt><dd><p>Path ของไฟล์ pcap ที่ต้องการเสริมข้อมูล</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-pcap-enrich--risk-score"><a href="#banshee-pcap-enrich--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>กรองผลลัพธ์เพื่อแสดงเฉพาะ indicator ที่มี risk score (1 - 99) สูงกว่าเกณฑ์นี้<p>ค่าเริ่มต้นคือ 65</p></p></dd>
    <dt id="banshee-pcap-enrich--threat-hunt"><a href="#banshee-pcap-enrich--threat-hunt"><code>--threat-hunt</code></a>, <code>-t</code></dt><dd>
    <p>รวม indicator ที่เชื่อมโยงกับ threat actor โดยไม่คำนึงถึงเกณฑ์ risk score (retrospective threat hunting)</p></dd>
    <dt id="banshee-ca-lookup--pretty"><a href="#banshee-ca-lookup--pretty"><code>--pretty</code></a>,  <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p><dd></dd>
    <dt id="banshee-pcap-enrich--help"><a href="#banshee-pcap-enrich--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

## banshee risklist

จัดการ Risk Lists

<h3 class="commands-reference">Usage</h3>

```
banshee risklist [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-risklist-create"><code>banshee risklist create</code></a></dt><dd><p>สร้าง risk list แบบกำหนดเองโดยรวม risk rules หนึ่งรายการหรือมากกว่า</p></dd>
    <dt><a href="#banshee-risklist-fetch"><code>banshee risklist fetch</code></a></dt><dd><p>ดาวน์โหลด risk list</p></dd>
    <dt><a href="#banshee-risklist-stat"><code>banshee risklist stat</code></a></dt><dd><p>แสดง metadata ของ risk list (etag และ timestamp)</p></dd>
</dl>

### banshee risklist create

สร้าง risk list แบบกำหนดเองโดยรวม Recorded Future risk rules หนึ่งรายการหรือมากกว่าเป็นไฟล์เดียวที่ไม่มีรายการซ้ำ

รายการจะถูกดึงสำหรับแต่ละ `--risk-rule` ผสานตาม IOC (รายการแรกที่พบจะชนะ) และกรองตาม `--risk-score` ขั้นต่ำตามต้องการ output จะเรียงลำดับตาม risk score จากมากไปน้อยและเขียนในรูปแบบที่เลือก — พร้อมสำหรับการนำไปใช้กับ firewall, SIEM หรือ integration อื่น ๆ

โดยค่าเริ่มต้น output จะถูกเขียนลงในไฟล์ local ใช้ `--fusion` กับ `--output-path` เพื่ออัปโหลดผลลัพธ์โดยตรงไปยัง Recorded Future Fusion โดยไม่เขียนไฟล์ local

<h3 class="commands-reference">Usage</h3>

```
banshee risklist create [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-create--entity-type"><a href="#banshee-risklist-create--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>ประเภท entity สำหรับ risk list ค่าที่ถูกต้อง: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br><strong>จำเป็น</strong></p></dd>
    <dt id="banshee-risklist-create--risk-rule"><a href="#banshee-risklist-create--risk-rule"><code>--risk-rule</code></a>, <code>-R</code> <i>risk-rule</i></dt><dd>
    <p>Risk rule ที่จะรวม ใช้ <code>default</code>, <code>large</code> หรือชื่อ rule ใดก็ได้จาก <a href="#banshee-ioc-rules"><code>banshee ioc rules</code></a> ระบุได้หลายครั้ง — ระบุหลายครั้งเพื่อผสาน rule เป็น output เดียว<br><strong>จำเป็น (อย่างน้อยหนึ่งรายการ)</strong></p></dd>
    <dt id="banshee-risklist-create--risk-score"><a href="#banshee-risklist-create--risk-score"><code>--risk-score</code></a>, <code>-r</code> <i>risk-score</i></dt><dd>
    <p>เกณฑ์ risk score ขั้นต่ำ (5–99) รายการที่มี risk score ต่ำกว่าค่านี้จะถูกยกเว้นจาก output</p></dd>
    <dt id="banshee-risklist-create--format"><a href="#banshee-risklist-create--format"><code>--format</code></a>, <code>-f</code> <i>format</i></dt><dd>
    <p>รูปแบบ output ค่าเริ่มต้นคือ <code>csv</code></p>
    <ul>
        <li><code>csv</code> — คั่นด้วยเครื่องหมายจุลภาคพร้อม headers: <code>Name</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code> สำหรับประเภท entity แบบ Hash จะมีคอลัมน์ <code>Algorithm</code> เพิ่มเติม: <code>Name</code>, <code>Algorithm</code>, <code>Risk</code>, <code>RiskString</code>, <code>EvidenceDetails</code></li>
        <li><code>edl</code> — รายการ IOC แบบ plain หนึ่งรายการต่อบรรทัด (เหมาะสำหรับ firewall EDL feeds) เขียนด้วยนามสกุล <code>.txt</code></li>
        <li><code>json</code> — JSON array ของรายการ risk list แบบเต็ม</li>
    </ul></dd>
    <dt id="banshee-risklist-create--output-path"><a href="#banshee-risklist-create--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>Path ของไฟล์ output รับ file path หรือ directory (ชื่อไฟล์จะสร้างอัตโนมัติเป็น <code>custom_risklist_{entity_type}.{ext}</code>) ค่าเริ่มต้นคือ directory ปัจจุบันพร้อมชื่อไฟล์ที่สร้างอัตโนมัติ<br>จำเป็นเมื่อใช้ <code>--fusion</code></p></dd>
    <dt id="banshee-risklist-create--fusion"><a href="#banshee-risklist-create--fusion"><code>--fusion</code></a>, <code>-F</code></dt><dd>
    <p>อัปโหลดผลลัพธ์โดยตรงไปยัง Recorded Future Fusion โดยใช้ <code>--output-path</code> เป็น path ปลายทาง ไม่มีการเขียนไฟล์ local เมื่อตั้งค่า flag นี้</p></dd>
    <dt id="banshee-risklist-create--help"><a href="#banshee-risklist-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

สร้าง CSV risk list สำหรับ IP จาก default rule กรองที่ risk score 70 ขึ้นไป

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
```

ผสาน domain rules สองรายการเป็น CSV เดียวที่ไม่มีรายการซ้ำ กรองที่ risk score 80 ขึ้นไป

```bash
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
```

ผสาน IP rules สองรายการและส่งออกเป็น EDL (รายการ IOC แบบ plain)

```bash
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
```

สร้าง JSON risk list สำหรับ hash จาก rules สองรายการและส่งออกไปยัง file path local ที่ระบุ

```bash
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
```

สร้าง risk list และอัปโหลดโดยตรงไปยัง Recorded Future Fusion

```bash
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

### banshee risklist fetch

ดาวน์โหลด risk list สำหรับประเภท entity และชื่อ list ที่ระบุ หรือใช้ไฟล์ risk list แบบกำหนดเอง

Risk lists สามารถดาวน์โหลดจาก Recorded Future ได้โดยระบุประเภท entity (`--entity-type`) และชื่อ list (`--list-name`) ชื่อ list ที่มีได้แก่ `default`, `large` หรือชื่อ rule ใดก็ได้จาก `banshee ioc rules` สำหรับข้อมูลเพิ่มเติมเกี่ยวกับ Recorded Future Risk Rules โปรดดูที่บทความสนับสนุน [Risk Scoring in Recorded Future](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future)

หรือสามารถระบุ path ไปยังไฟล์ risk list แบบกำหนดเองโดยใช้ `--custom-list-path`

<h3 class="commands-reference">Usage</h3>

```
banshee risklist fetch [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-fetch--entity-type"><a href="#banshee-risklist-fetch--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>ประเภท entity สำหรับ risk list ค่าที่ถูกต้อง: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br>จำเป็นเมื่อใช้ <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-fetch--list-name"><a href="#banshee-risklist-fetch--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>ชื่อ risk list: <code>default</code>, <code>large</code> หรือชื่อ rule จาก <code>banshee ioc rules</code><br>จำเป็นเมื่อใช้ <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-fetch--custom-list-path"><a href="#banshee-risklist-fetch--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>Path ไปยังไฟล์ risk list แบบกำหนดเอง ไม่สามารถใช้ร่วมกับ <code>--entity-type</code> หรือ <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-fetch--output-path"><a href="#banshee-risklist-fetch--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>Path ของไฟล์ output ค่าเริ่มต้นคือ directory ปัจจุบันพร้อมชื่อไฟล์ที่สร้างอัตโนมัติ</p></dd>
    <dt id="banshee-risklist-fetch--as-json"><a href="#banshee-risklist-fetch--as-json"><code>--as-json</code></a>, <code>-j</code></dt><dd>
    <p>แปลง risk list เป็นรูปแบบ JSON สามารถใช้ได้เฉพาะกับ <code>--list-name</code> และ <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-fetch--help"><a href="#banshee-risklist-fetch--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# ดาวน์โหลด default risk list สำหรับ IP address
banshee risklist fetch -e ip -l default

# ดาวน์โหลด large risk list สำหรับ domain เป็น JSON
banshee risklist fetch -e domain -l large -j

# ดาวน์โหลด risk list สำหรับ hash ที่เกี่ยวข้องกับ Insikt Group Note
banshee risklist fetch -e hash -l analystNote

# ดาวน์โหลดไฟล์ risk list แบบกำหนดเอง
banshee risklist fetch -c /path/to/custom_risklist.csv

# ดาวน์โหลด default risklist สำหรับ URL และบันทึกไปยัง output path ที่ระบุ
banshee risklist fetch -e url -l default -o /tmp/rf_default_url_risklist.csv
</code></pre>

### banshee risklist stat

แสดง metadata ของ risk list รวมถึงข้อมูล etag และ timestamp

คำสั่งนี้ดึง metadata สำหรับ risk list โดยไม่ต้องดาวน์โหลดเนื้อหา list ทั้งหมด สามารถใช้เพื่อตรวจสอบว่า risk list ถูกอัปเดตล่าสุดเมื่อใด

<h3 class="commands-reference">Usage</h3>

```
banshee risklist stat [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-risklist-stat--entity-type"><a href="#banshee-risklist-stat--entity-type"><code>--entity-type</code></a>, <code>-e</code> <i>entity-type</i></dt><dd>
    <p>ประเภท entity สำหรับ risk list ค่าที่ถูกต้อง: <code>ip</code>, <code>domain</code>, <code>url</code>, <code>hash</code>, <code>vulnerability</code><br>จำเป็นเมื่อใช้ <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-stat--list-name"><a href="#banshee-risklist-stat--list-name"><code>--list-name</code></a>, <code>-l</code> <i>list-name</i></dt><dd>
    <p>ชื่อ risk list: <code>default</code>, <code>large</code> หรือชื่อ rule จาก <code>banshee ioc rules</code><br>จำเป็นเมื่อใช้ <code>--entity-type</code></p></dd>
    <dt id="banshee-risklist-stat--custom-list-path"><a href="#banshee-risklist-stat--custom-list-path"><code>--custom-list-path</code></a>, <code>-c</code> <i>custom-list-path</i></dt><dd>
    <p>Path ไปยังไฟล์ risk list แบบกำหนดเอง ไม่สามารถใช้ร่วมกับ <code>--entity-type</code> หรือ <code>--list-name</code></p></dd>
    <dt id="banshee-risklist-stat--pretty"><a href="#banshee-risklist-stat--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-risklist-stat--count"><a href="#banshee-risklist-stat--count"><code>--count</code></a>, <code>-C</code></dt><dd>
    <p>แสดงจำนวน IOC และการกระจาย risk score ใน risk list</p></dd>
    <dt id="banshee-risklist-stat--help"><a href="#banshee-risklist-stat--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# ตรวจสอบ metadata สำหรับ IP risk list เริ่มต้น
banshee risklist stat -e ip -l default

# ตรวจสอบ metadata พร้อมการจัดรูปแบบแบบ pretty
banshee risklist stat -e domain -l large -p

# ตรวจสอบ metadata สำหรับไฟล์ risk list แบบกำหนดเอง
banshee risklist stat -c /path/to/custom_risklist.txt

# นับ indicator ตาม risk score ใน IP risk list เริ่มต้นและแสดงแบบ pretty
banshee risklist stat -e ip -l default -Cp
</code></pre>

## banshee rules

ค้นหาและดาวน์โหลด detection rules

<h3 class="commands-reference">Usage</h3>

```
banshee rules [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-rules-search"><code>banshee rules search</code></a></dt><dd><p>ค้นหา detection rules ตามตัวเลือกการกรอง</p></dd>
</dl>

### banshee rules search

ค้นหา detection rules ตามตัวเลือกการกรองที่ระบุ ผลลัพธ์สามารถแสดงใน console หรือบันทึกลงดิสก์เป็นไฟล์ rule แต่ละรายการ

Detection rules สามารถกรองตามประเภท (YARA, Snort, Sigma) entity ที่เกี่ยวข้อง (threat actor, malware, MITRE ATT&CK technique) วันที่สร้าง/อัปเดต และอื่น ๆ ใช้ `--threat-actor-map` หรือ `--threat-malware-map` เพื่อกรอง rule โดยอัตโนมัติตาม entity ใน Threat Map ของคุณ

เพื่อหลีกเลี่ยง output ที่มากเกินไป ผลลัพธ์จะถูกจำกัดที่ 10 รายการโดยค่าเริ่มต้น ใช้ตัวเลือก `--limit` เพื่อดึง rule ได้สูงสุด 1,000 รายการ

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee rules search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-rules-search--type"><a href="#banshee-rules-search--type"><code>--type</code></a>, <code>-t</code> <i>type</i></dt><dd>
    <p>กรองตามประเภท rule ค่าที่ถูกต้อง: <code>yara</code>, <code>snort</code>, <code>sigma</code><br>สามารถระบุหลายประเภทได้ โดยทำงานเป็น OR เชิงตรรกะ (เช่น <code>-t yara -t snort</code> จะส่งคืน rule ที่ตรงกับประเภทใดประเภทหนึ่ง)</p></dd>
    <dt id="banshee-rules-search--threat-actor-map"><a href="#banshee-rules-search--threat-actor-map"><code>--threat-actor-map</code></a>, <code>-T</code></dt><dd>
    <p>กรอง rule ตาม threat actor จาก Threat Actor Map ของคุณ เมื่อเปิดใช้งาน จะส่งคืน detection rules ที่เกี่ยวข้องกับ actor ใน Threat Actor Map ของคุณ</p></dd>
    <dt id="banshee-rules-search--threat-actor-category"><a href="#banshee-rules-search--threat-actor-category"><code>--threat-actor-category</code></a>, <code>-C</code> <i>category</i></dt><dd>
    <p>กรองตามหมวดหมู่ threat actor จาก Threat Actor Map ของคุณ สามารถระบุหลายหมวดหมู่ได้ โดยทำงานเป็น OR เชิงตรรกะ (เช่น <code>-C nation_state_sponsored -C ransomware_and_extortion_groups</code>)</p></dd>
    <dt id="banshee-rules-search--threat-malware-map"><a href="#banshee-rules-search--threat-malware-map"><code>--threat-malware-map</code></a>, <code>-M</code></dt><dd>
    <p>กรอง rule ตาม malware จาก Malware Threat Map ของคุณ เมื่อเปิดใช้งาน จะส่งคืน detection rules ที่เกี่ยวข้องกับ malware ใน Malware Threat Map ของคุณ</p></dd>
    <dt id="banshee-rules-search--org-id"><a href="#banshee-rules-search--org-id"><code>--org-id</code></a>, <code>-O</code> <i>org-id</i></dt><dd>
    <p>ระบุ organization ID เมื่อดึง threat actor จาก Threat Maps (ต้องใช้ร่วมกับ <code>--threat-actor-map</code> หรือ <code>--threat-malware-map</code>) รับค่าที่มีหรือไม่มี prefix <code>uhash:</code> เหมาะสำหรับบัญชี MSSP และหลายองค์กร</p></dd>
    <dt id="banshee-rules-search--entity"><a href="#banshee-rules-search--entity"><code>--entity</code></a>, <code>-e</code> <i>entity</i></dt><dd>
    <p>กรองตาม Recorded Future entity ID ที่เกี่ยวข้องกับ detection rules สามารถระบุหลาย entity ได้ โดยทำงานเป็น OR เชิงตรรกะ ใช้ <code>banshee entity search</code> เพื่อค้นหา entity ID (เช่น <code>lzQ5GL</code> สำหรับ malware IsaacWiper, <code>mitre:T1486</code> สำหรับ Data Encrypted for Impact)</p></dd>
    <dt id="banshee-rules-search--created-after"><a href="#banshee-rules-search--created-after"><code>--created-after</code></a>, <code>-a</code> <i>time</i></dt><dd>
    <p>กรอง detection rules ที่สร้างหลังจากเวลาที่ระบุ รับเวลาแบบ relative (เช่น <code>1d</code>, <code>3d</code>, <code>7d</code>) หรือวันที่แบบ absolute (เช่น <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--created-before"><a href="#banshee-rules-search--created-before"><code>--created-before</code></a>, <code>-b</code> <i>time</i></dt><dd>
    <p>กรอง detection rules ที่สร้างก่อนเวลาที่ระบุ รับเวลาแบบ relative (เช่น <code>1d</code>, <code>3d</code>, <code>7d</code>) หรือวันที่แบบ absolute (เช่น <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--updated-after"><a href="#banshee-rules-search--updated-after"><code>--updated-after</code></a>, <code>-u</code> <i>time</i></dt><dd>
    <p>กรอง detection rules ที่อัปเดตหลังจากเวลาที่ระบุ รับเวลาแบบ relative (เช่น <code>1d</code>, <code>3d</code>, <code>7d</code>) หรือวันที่แบบ absolute (เช่น <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--updated-before"><a href="#banshee-rules-search--updated-before"><code>--updated-before</code></a>, <code>-U</code> <i>time</i></dt><dd>
    <p>กรอง detection rules ที่อัปเดตก่อนเวลาที่ระบุ รับเวลาแบบ relative (เช่น <code>1d</code>, <code>3d</code>, <code>7d</code>) หรือวันที่แบบ absolute (เช่น <code>2024-01-01</code>)</p></dd>
    <dt id="banshee-rules-search--id"><a href="#banshee-rules-search--id"><code>--id</code></a>, <code>-i</code> <i>document-id</i></dt><dd>
    <p>กรองตาม Insikt Note document ID เฉพาะที่เกี่ยวข้องกับ detection rules (เช่น <code>doc:lmRPGB</code>)</p></dd>
    <dt id="banshee-rules-search--title"><a href="#banshee-rules-search--title"><code>--title</code></a>, <code>-n</code> <i>title</i></dt><dd>
    <p>ค้นหา detection rules ด้วยข้อความอิสระตามชื่อ Insikt Note ที่เกี่ยวข้อง</p></dd>
    <dt id="banshee-rules-search--limit"><a href="#banshee-rules-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>จำนวนสูงสุดของ detection rules ที่จะส่งคืน<p>ค่าเริ่มต้นคือ 10</p></p></dd>
    <dt id="banshee-rules-search--output-path"><a href="#banshee-rules-search--output-path"><code>--output-path</code></a>, <code>-o</code> <i>output-path</i></dt><dd>
    <p>บันทึก detection rules ไปยัง directory ที่ระบุ สามารถเป็น relative หรือ absolute path ได้ หากไม่ระบุ ผลลัพธ์จะแสดงใน console</p></dd>
    <dt id="banshee-rules-search--pretty"><a href="#banshee-rules-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-rules-search--help"><a href="#banshee-rules-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Usage Examples</h3>

<pre><code class="language-bash">
# ค้นหา YARA rules ที่สร้างใน 7 วันที่ผ่านมา
banshee rules search -t yara -a 7d

# ค้นหา rule ที่เกี่ยวข้องกับ threat actor ใน Threat Map และแสดงแบบ pretty
# เนื่องจาก --limit ค่าเริ่มต้นคือ 10 จะส่งคืน rule ที่ตรงกัน 10 รายการแรก
banshee rules search -Tp

# รวม threat actor และ malware maps
banshee rules search -TMp

# ค้นหา rule ตาม entity ID เฉพาะ (เช่น malware IsaacWiper)
banshee rules search -e lzQ5GL -p

# ค้นหา Snort และ Sigma rules ที่อัปเดตใน 3 วันที่ผ่านมา บันทึกไปยัง directory
banshee rules search -t snort -t sigma -u 3d -o ./detection_rules

# ค้นหาตามชื่อ Insikt Note
banshee rules search --title "APT28" -p
</code></pre>

## banshee sandbox

การวิเคราะห์การส่ง sandbox และการจัดการ profile

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-stats"><code>banshee sandbox stats</code></a></dt><dd><p>รวบรวมสถิติการส่ง sandbox ในช่วงเวลาที่กำหนดและแสดงสรุปสำหรับ SOC ยามเช้า</p></dd>
    <dt><a href="#banshee-sandbox-list"><code>banshee sandbox list</code></a></dt><dd><p>แสดงรายการ sandbox sample</p></dd>
    <dt><a href="#banshee-sandbox-search"><code>banshee sandbox search</code></a></dt><dd><p>ค้นหา sample ตาม hash, family, tag, botnet, wallet, network indicator หรือ Triage query แบบ raw</p></dd>
    <dt><a href="#banshee-sandbox-get"><code>banshee sandbox get</code></a></dt><dd><p>ดึงสรุปสำหรับ sandbox sample รายการเดียวตาม ID</p></dd>
    <dt><a href="#banshee-sandbox-download"><code>banshee sandbox download</code></a></dt><dd><p>ดาวน์โหลด bytes ที่ส่งเดิมสำหรับ sample ID หนึ่งรายการหรือมากกว่า (บรรจุใน ZIP archive ที่เข้ารหัส AES)</p></dd>
    <dt><a href="#banshee-sandbox-delete"><code>banshee sandbox delete</code></a></dt><dd><p>ลบ sandbox sample ตาม ID</p></dd>
    <dt><a href="#banshee-sandbox-submit"><code>banshee sandbox submit</code></a></dt><dd><p>ส่งไฟล์ URL หรือ public sample เพื่อวิเคราะห์ใน sandbox</p></dd>
    <dt><a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a></dt><dd><p>กำหนด analysis profile ให้กับ sample ที่หยุดอยู่ที่ static analysis</p></dd>
    <dt><a href="#banshee-sandbox-profile"><code>banshee sandbox profile</code></a></dt><dd><p>จัดการ analysis profile</p></dd>
    <dt><a href="#banshee-sandbox-report"><code>banshee sandbox report</code></a></dt><dd><p>รายงานการวิเคราะห์ sample</p></dd>
</dl>

### banshee sandbox stats

รวบรวมสถิติการส่ง sandbox ในช่วงเวลาที่กำหนดและแสดง "สรุปยามเช้า" ที่เหมาะสำหรับการส่งต่อกะ SOC หรือการ triage ประจำวัน

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Score Buckets</h3>

<p>Sandbox ให้คะแนน sample ในระดับ triage 1–10 ผลลัพธ์จะถูกจัดกลุ่มเป็น bucket ดังต่อไปนี้:</p>

| Bucket | ช่วงคะแนน | ความหมาย |
|---|---|---|
| `malicious` | 8–10 | Malware ที่ทราบแล้ว ความมั่นใจสูง |
| `suspicious` | 5–7 | มี behavioural indicator ที่ชัดเจน |
| `potentially_suspicious` | 3–4 | มี indicator บางอย่าง |
| `clean` | 1–2 | ความเสี่ยงต่ำหรือไม่เป็นอันตราย |

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox stats [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-stats--days"><a href="#banshee-sandbox-stats--days"><code>--days</code></a>, <code>-d</code> <i>days</i></dt><dd>
    <p>ช่วงเวลาย้อนหลังในหน่วยวัน</p>
    <p>ค่าเริ่มต้นคือ 7</p></dd>
    <dt id="banshee-sandbox-stats--subset"><a href="#banshee-sandbox-stats--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>ขอบเขต sample ที่จะรวบรวม</p>
    <p>ค่าที่เป็นไปได้: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>ค่าเริ่มต้นคือ <code>org</code></p></dd>
    <dt id="banshee-sandbox-stats--pretty"><a href="#banshee-sandbox-stats--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-stats--help"><a href="#banshee-sandbox-stats--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats --days 30 --pretty
</code></pre>

### banshee sandbox list

แสดงรายการ sandbox sample — ของตัวเอง ขององค์กร (ค่าเริ่มต้น) หรือ feed สาธารณะ

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox list [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-list--subset"><a href="#banshee-sandbox-list--subset"><code>--subset</code></a>, <code>-s</code> <i>subset</i></dt><dd>
    <p>ขอบเขต sample ที่จะแสดง</p>
    <p>ค่าที่เป็นไปได้: <code>owned</code>, <code>public</code>, <code>org</code></p>
    <p>ค่าเริ่มต้นคือ <code>org</code></p></dd>
    <dt id="banshee-sandbox-list--limit"><a href="#banshee-sandbox-list--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>จำนวนสูงสุดของ sample ที่จะส่งคืน</p>
    <p>ช่วงที่รับได้: 1–4095</p>
    <p>ค่าเริ่มต้นคือ 20</p></dd>
    <dt id="banshee-sandbox-list--pretty"><a href="#banshee-sandbox-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-list--help"><a href="#banshee-sandbox-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

ค้นหา sample ที่ตรงกับตัวกรองแบบมีโครงสร้าง (hash, family, tag, botnet, wallet, IP, domain, URL, ช่วงวันที่ส่ง) หรือ Triage query แบบ raw ต้องระบุตัวกรองอย่างน้อยหนึ่งตัวหรือ `--query`

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox search [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-search--hash"><a href="#banshee-sandbox-search--hash"><code>--hash</code></a> <i>hash</i></dt><dd>
    <p>กรองตาม file hash (MD5/SHA1/SHA256)</p></dd>
    <dt id="banshee-sandbox-search--family"><a href="#banshee-sandbox-search--family"><code>--family</code></a> <i>family</i></dt><dd>
    <p>กรองตามชื่อ malware family</p></dd>
    <dt id="banshee-sandbox-search--tag"><a href="#banshee-sandbox-search--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>กรองตาม tag (ระบุได้หลายครั้ง)</p></dd>
    <dt id="banshee-sandbox-search--botnet"><a href="#banshee-sandbox-search--botnet"><code>--botnet</code></a> <i>botnet</i></dt><dd>
    <p>กรองตามชื่อ botnet</p></dd>
    <dt id="banshee-sandbox-search--wallet"><a href="#banshee-sandbox-search--wallet"><code>--wallet</code></a> <i>wallet</i></dt><dd>
    <p>กรองตาม wallet address</p></dd>
    <dt id="banshee-sandbox-search--ip"><a href="#banshee-sandbox-search--ip"><code>--ip</code></a> <i>ip</i></dt><dd>
    <p>กรองตาม IP address</p></dd>
    <dt id="banshee-sandbox-search--domain"><a href="#banshee-sandbox-search--domain"><code>--domain</code></a> <i>domain</i></dt><dd>
    <p>กรองตาม domain</p></dd>
    <dt id="banshee-sandbox-search--url"><a href="#banshee-sandbox-search--url"><code>--url</code></a> <i>url</i></dt><dd>
    <p>กรองตาม URL</p></dd>
    <dt id="banshee-sandbox-search--from-date"><a href="#banshee-sandbox-search--from-date"><code>--from-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>ส่งเมื่อวันนี้หรือหลังจากวันที่นี้</p></dd>
    <dt id="banshee-sandbox-search--to-date"><a href="#banshee-sandbox-search--to-date"><code>--to-date</code></a> <i>YYYY-MM-DD</i></dt><dd>
    <p>ส่งเมื่อวันนี้หรือก่อนวันที่นี้</p></dd>
    <dt id="banshee-sandbox-search--query"><a href="#banshee-sandbox-search--query"><code>--query</code></a>, <code>-q</code> <i>query</i></dt><dd>
    <p>Triage query string แบบ raw (รวมกับตัวกรองแบบมีโครงสร้างโดยใช้ AND)</p></dd>
    <dt id="banshee-sandbox-search--limit"><a href="#banshee-sandbox-search--limit"><code>--limit</code></a>, <code>-l</code> <i>limit</i></dt><dd>
    <p>จำนวนสูงสุดของ sample ที่จะส่งคืน (1–200)</p>
    <p>ค่าเริ่มต้นคือ 50</p></dd>
    <dt id="banshee-sandbox-search--pretty"><a href="#banshee-sandbox-search--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-search--help"><a href="#banshee-sandbox-search--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

ดึงสรุปสำหรับ sandbox sample รายการเดียวตาม ID ได้แก่ สถานะปัจจุบัน คะแนนรวม เป้าหมาย timestamps การสร้างและเสร็จสิ้น SHA256 และรายละเอียดแต่ละ task ใช้ได้กับทั้ง sample ที่กำลังดำเนินการและที่เสร็จสมบูรณ์แล้ว

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox get [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--sample-id"><a href="#banshee-sandbox-get--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>Sandbox sample ID</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-get--pretty"><a href="#banshee-sandbox-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-get--help"><a href="#banshee-sandbox-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
</code></pre>

### banshee sandbox download

ดาวน์โหลด bytes ของ sample ที่ส่งเดิมสำหรับ sample ID หนึ่งรายการหรือมากกว่า sample แต่ละรายการจะถูกบรรจุใน ZIP archive ที่เข้ารหัส AES พร้อมรหัสผ่าน `infected` เพื่อป้องกันการ detonate โดยไม่ตั้งใจโดย antivirus, secure email gateway หรือ file manager

แตกไฟล์ด้วย `7z x -pinfected <sample-id>.zip` — `unzip` มาตรฐานไม่รองรับ ZIP ที่เข้ารหัส AES อย่างน่าเชื่อถือ

Sample ID สามารถส่งเป็น positional argument หรือ pipe ทาง stdin (คั่นด้วยช่องว่าง) จะแสดงคำยืนยันหากไม่ได้ระบุ `--yes`

> **หมายเหตุด้านความปลอดภัย:** bytes ของ sample จะอยู่ใน memory ของ process นี้ชั่วคราวระหว่างการดาวน์โหลดและการบีบอัด การสแกน memory ของ EDR ที่ aggressive อาจยังตรวจพบได้ ควรรันบนเครื่องของ analyst ไม่ใช่ laptop ขององค์กรที่ใช้งานประจำ

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox download [OPTIONS] [SAMPLE_IDS]...
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--sample-ids"><a href="#banshee-sandbox-download--sample-ids"><code>SAMPLE_IDS</code></a></dt><dd><p>Sample ID หนึ่งรายการหรือมากกว่า (หรืออ่านจาก stdin คั่นด้วยช่องว่าง)</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-download--output-dir"><a href="#banshee-sandbox-download--output-dir"><code>--output-dir</code></a>, <code>-d</code> <i>DIR</i></dt><dd>
    <p>Directory สำหรับบันทึก encrypted zip archive (สร้างหากไม่มี) จำเป็น</p></dd>
    <dt id="banshee-sandbox-download--yes"><a href="#banshee-sandbox-download--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>ข้ามคำยืนยัน</p></dd>
    <dt id="banshee-sandbox-download--workers"><a href="#banshee-sandbox-download--workers"><code>--workers</code></a>, <code>-w</code> <i>N</i></dt><dd>
    <p>จำนวน parallel download worker (1–16)</p>
    <p>ค่าเริ่มต้นคือ 1</p></dd>
    <dt id="banshee-sandbox-download--help"><a href="#banshee-sandbox-download--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# แตกไฟล์
7z x -pinfected ./samples/260501-h4p7laawme.zip
</code></pre>

### banshee sandbox delete

ลบ sandbox sample ตาม ID และลบ task artifact ที่เกี่ยวข้องทั้งหมด

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox delete [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--sample-id"><a href="#banshee-sandbox-delete--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>Sample ID ที่ต้องการลบ</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-delete--yes"><a href="#banshee-sandbox-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>ข้ามคำยืนยัน</p></dd>
    <dt id="banshee-sandbox-delete--help"><a href="#banshee-sandbox-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
</code></pre>

### banshee sandbox submit

ส่ง sample เพื่อวิเคราะห์ ไฟล์ local จะถูกอัปโหลด URL จะถูก detonate ใน browser (หรือดาวน์โหลดก่อนด้วย `--fetch`) และ public sample สามารถนำเข้าตาม ID ด้วย `--import`

โดยค่าเริ่มต้น คำสั่งจะแสดง JSON submission receipt ใช้ `--wait` เพื่อ poll จนกว่าการวิเคราะห์จะเสร็จสมบูรณ์และแสดงรายงานสรุป

<h3 class="commands-reference">Target Kinds</h3>

| Target | พฤติกรรม |
|---|---|
| Local file path | อัปโหลดและวิเคราะห์ |
| URL | Detonate ใน browser |
| URL + `--fetch` | ดาวน์โหลดก่อน จากนั้นวิเคราะห์เป็นไฟล์ |
| Public sample ID + `--import` | นำเข้าใน sandbox ขององค์กรของคุณ |

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox submit [OPTIONS] TARGET
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--target"><a href="#banshee-sandbox-submit--target"><code>TARGET</code></a></dt><dd><p>File path, URL หรือ public sample ID (พร้อม <code>--import</code>)</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-submit--fetch"><a href="#banshee-sandbox-submit--fetch"><code>--fetch</code></a></dt><dd>
    <p>ดาวน์โหลด URL target ก่อน จากนั้นวิเคราะห์ไฟล์ที่ได้ ใช้ร่วมกับ <code>--import</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-submit--import"><a href="#banshee-sandbox-submit--import"><code>--import</code></a></dt><dd>
    <p>ถือว่า target เป็น public sample ID เพื่อนำเข้าใน sandbox ขององค์กรของคุณ ใช้ร่วมกับ <code>--fetch</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-submit--profile"><a href="#banshee-sandbox-submit--profile"><code>--profile</code></a> <i>profile</i></dt><dd>
    <p>ชื่อหรือ ID ของ analysis profile สามารถระบุได้หลายครั้งเพื่อกำหนดมากกว่าหนึ่ง profile ใช้ร่วมกับ <code>--interactive</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-submit--timeout"><a href="#banshee-sandbox-submit--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>เวลา timeout ในการวิเคราะห์ (วินาที)</p>
    <p>ช่วงที่รับได้: 1–3600</p></dd>
    <dt id="banshee-sandbox-submit--network"><a href="#banshee-sandbox-submit--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>โหมด network สำหรับ analysis environment</p>
    <p>ค่าที่เป็นไปได้: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-submit--geolocation"><a href="#banshee-sandbox-submit--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>รหัสประเทศของ VPN exit ต้องใช้ร่วมกับ <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-submit--tags"><a href="#banshee-sandbox-submit--tags"><code>--tags</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>Tag แบบกำหนดเองที่จะแนบกับ submission สามารถระบุได้หลายครั้ง</p></dd>
    <dt id="banshee-sandbox-submit--password"><a href="#banshee-sandbox-submit--password"><code>--password</code></a> <i>password</i></dt><dd>
    <p>รหัสผ่านสำหรับ archive ที่มีการป้องกัน</p></dd>
    <dt id="banshee-sandbox-submit--wait"><a href="#banshee-sandbox-submit--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>Poll จนกว่าการวิเคราะห์จะเสร็จสิ้น จากนั้นแสดงรายงานสรุป</p></dd>
    <dt id="banshee-sandbox-submit--interactive"><a href="#banshee-sandbox-submit--interactive"><code>--interactive</code></a>, <code>-i</code></dt><dd>
    <p>หยุดที่ static analysis เพื่อให้เลือกไฟล์และ profile ผ่าน <a href="#banshee-sandbox-set-profile"><code>banshee sandbox set-profile</code></a> ใช้ร่วมกับ <code>--profile</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-submit--pretty"><a href="#banshee-sandbox-submit--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-submit--help"><a href="#banshee-sandbox-submit--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

กำหนด analysis profile ให้กับ sample ที่หยุดอยู่ที่ static analysis (ส่งพร้อม `--interactive`) ใช้ `--auto` เพื่อให้ sandbox เลือก profile โดยอัตโนมัติ หรือ `--pick` เพื่อกำหนดไฟล์เฉพาะให้กับ profile เฉพาะด้วยตนเอง

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox set-profile [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--sample-id"><a href="#banshee-sandbox-set-profile--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>ID ของ sample ที่หยุดอยู่ที่ static analysis</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-set-profile--auto"><a href="#banshee-sandbox-set-profile--auto"><code>--auto</code></a>, <code>-a</code></dt><dd>
    <p>ให้ sandbox เลือก profile สำหรับไฟล์ทั้งหมดโดยอัตโนมัติ ใช้ร่วมกับ <code>--pick</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-set-profile--pick"><a href="#banshee-sandbox-set-profile--pick"><code>--pick</code></a> <i>FILE:PROFILE</i></dt><dd>
    <p>กำหนดไฟล์เฉพาะให้กับ profile เฉพาะ ในรูปแบบ <code>FILE:PROFILE</code> สามารถระบุได้หลายครั้ง ใช้ร่วมกับ <code>--auto</code> ไม่ได้</p></dd>
    <dt id="banshee-sandbox-set-profile--pretty"><a href="#banshee-sandbox-set-profile--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-set-profile--help"><a href="#banshee-sandbox-set-profile--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

จัดการ analysis profile

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-profile-list"><code>banshee sandbox profile list</code></a></dt><dd><p>แสดงรายการ analysis profile ทั้งหมดที่มี</p></dd>
    <dt><a href="#banshee-sandbox-profile-get"><code>banshee sandbox profile get</code></a></dt><dd><p>ดูรายละเอียดของ profile เฉพาะ</p></dd>
    <dt><a href="#banshee-sandbox-profile-create"><code>banshee sandbox profile create</code></a></dt><dd><p>สร้าง analysis profile ใหม่</p></dd>
    <dt><a href="#banshee-sandbox-profile-update"><code>banshee sandbox profile update</code></a></dt><dd><p>อัปเดต analysis profile ที่มีอยู่</p></dd>
    <dt><a href="#banshee-sandbox-profile-delete"><code>banshee sandbox profile delete</code></a></dt><dd><p>ลบ analysis profile</p></dd>
</dl>

#### banshee sandbox profile list

แสดงรายการ analysis profile ทั้งหมดที่มี

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile list [OPTIONS]
```

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-list--pretty"><a href="#banshee-sandbox-profile-list--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-profile-list--help"><a href="#banshee-sandbox-profile-list--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
</code></pre>

#### banshee sandbox profile get

ดูรายละเอียดของ analysis profile เฉพาะตามชื่อหรือ ID

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile get [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--profile-id-or-name"><a href="#banshee-sandbox-profile-get--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>Profile UUID หรือชื่อที่แสดง</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-get--pretty"><a href="#banshee-sandbox-profile-get--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-profile-get--help"><a href="#banshee-sandbox-profile-get--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
</code></pre>

#### banshee sandbox profile create

สร้าง analysis profile ใหม่

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Profile Tags</h3>

<p>Tags กำหนดระบบปฏิบัติการและ environment สำหรับ profile ต้องระบุ locale tag พร้อมกับ <code>os</code> tag อย่างน้อยหนึ่งรายการเสมอ</p>

<pre><code class="language-bash">
# OS เท่านั้น
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
    <p>ชื่อที่แสดงของ profile จำเป็น</p></dd>
    <dt id="banshee-sandbox-profile-create--tag"><a href="#banshee-sandbox-profile-create--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>Profile tag (เช่น <code>os:windows10-2004-x64</code>, <code>locale:en-us</code>) สามารถระบุได้หลายครั้ง จำเป็น</p></dd>
    <dt id="banshee-sandbox-profile-create--timeout"><a href="#banshee-sandbox-profile-create--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>เวลา timeout ในการวิเคราะห์ (วินาที)</p>
    <p>ช่วงที่รับได้: 1–3600</p>
    <p>ค่าเริ่มต้นคือ 120</p></dd>
    <dt id="banshee-sandbox-profile-create--network"><a href="#banshee-sandbox-profile-create--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>โหมด network</p>
    <p>ค่าที่เป็นไปได้: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-create--geolocation"><a href="#banshee-sandbox-profile-create--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>รหัสประเทศของ VPN exit สามารถระบุได้หลายครั้ง ต้องใช้ร่วมกับ <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-profile-create--browser"><a href="#banshee-sandbox-profile-create--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>Browser สำหรับการ detonate URL</p>
    <p>ค่าที่เป็นไปได้: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-create--pretty"><a href="#banshee-sandbox-profile-create--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-profile-create--help"><a href="#banshee-sandbox-profile-create--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
</code></pre>

#### banshee sandbox profile update

อัปเดต analysis profile ที่มีอยู่ตามชื่อหรือ ID ต้องระบุ option อย่างน้อยหนึ่งตัว

Output จะเป็น `{"updated": true}` หรือ `{"updated": false}` (ออกด้วย exit code 0 ในทุกกรณี)

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile update [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--profile-id-or-name"><a href="#banshee-sandbox-profile-update--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>Profile UUID หรือชื่อที่แสดงที่ต้องการอัปเดต</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-update--name"><a href="#banshee-sandbox-profile-update--name"><code>--name</code></a>, <code>-n</code> <i>name</i></dt><dd>
    <p>ชื่อที่แสดงของ profile ใหม่</p></dd>
    <dt id="banshee-sandbox-profile-update--tag"><a href="#banshee-sandbox-profile-update--tag"><code>--tag</code></a>, <code>-T</code> <i>tag</i></dt><dd>
    <p>แทนที่ tag ที่มีอยู่ทั้งหมด สามารถระบุได้หลายครั้ง</p></dd>
    <dt id="banshee-sandbox-profile-update--timeout"><a href="#banshee-sandbox-profile-update--timeout"><code>--timeout</code></a>, <code>-t</code> <i>seconds</i></dt><dd>
    <p>เวลา timeout ในการวิเคราะห์ (วินาที)</p>
    <p>ช่วงที่รับได้: 1–3600</p></dd>
    <dt id="banshee-sandbox-profile-update--network"><a href="#banshee-sandbox-profile-update--network"><code>--network</code></a>, <code>-N</code> <i>mode</i></dt><dd>
    <p>โหมด network</p>
    <p>ค่าที่เป็นไปได้: <code>internet</code>, <code>drop</code>, <code>tor</code>, <code>vpn</code>, <code>sim200</code>, <code>sim404</code>, <code>simnx</code></p></dd>
    <dt id="banshee-sandbox-profile-update--geolocation"><a href="#banshee-sandbox-profile-update--geolocation"><code>--geolocation</code></a> <i>country-code</i></dt><dd>
    <p>รหัสประเทศของ VPN exit สามารถระบุได้หลายครั้ง ต้องใช้ร่วมกับ <code>--network vpn</code></p></dd>
    <dt id="banshee-sandbox-profile-update--browser"><a href="#banshee-sandbox-profile-update--browser"><code>--browser</code></a>, <code>-b</code> <i>browser</i></dt><dd>
    <p>Browser สำหรับการ detonate URL</p>
    <p>ค่าที่เป็นไปได้: <code>chrome</code>, <code>firefox</code>, <code>ie11</code>, <code>microsoft-edge</code></p></dd>
    <dt id="banshee-sandbox-profile-update--unset"><a href="#banshee-sandbox-profile-update--unset"><code>--unset</code></a> <i>field</i></dt><dd>
    <p>ล้างค่าของฟิลด์ สามารถระบุได้หลายครั้ง</p>
    <p>ค่าที่เป็นไปได้: <code>network</code>, <code>browser</code>, <code>geolocation</code></p>
    <p>ไม่สามารถใช้ร่วมกับ option ที่ตั้งค่าฟิลด์เดียวกัน <code>--unset network</code> ขัดแย้งกับ <code>--geolocation</code></p></dd>
    <dt id="banshee-sandbox-profile-update--pretty"><a href="#banshee-sandbox-profile-update--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-profile-update--help"><a href="#banshee-sandbox-profile-update--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

ลบ analysis profile ตามชื่อหรือ ID การลบ profile ที่ไม่มีอยู่จะแสดงคำเตือนและออกด้วย exit code 0

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox profile delete [OPTIONS] PROFILE_ID_OR_NAME
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--profile-id-or-name"><a href="#banshee-sandbox-profile-delete--profile-id-or-name"><code>PROFILE_ID_OR_NAME</code></a></dt><dd><p>Profile UUID หรือชื่อที่แสดงที่ต้องการลบ</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-profile-delete--yes"><a href="#banshee-sandbox-profile-delete--yes"><code>--yes</code></a>, <code>-y</code></dt><dd>
    <p>ข้ามคำยืนยัน</p></dd>
    <dt id="banshee-sandbox-profile-delete--help"><a href="#banshee-sandbox-profile-delete--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
</dl>

<h3 class="commands-reference">Example Usage</h3>

<pre><code class="language-bash">
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
</code></pre>

### banshee sandbox report

รายงานการวิเคราะห์ sample

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report [OPTIONS] COMMAND [ARGS]...
```

<h3 class="commands-reference">Commands</h3>

<dl class="commands-reference">
    <dt><a href="#banshee-sandbox-report-overview"><code>banshee sandbox report overview</code></a></dt><dd><p>รายงานสรุปฉบับเต็มสำหรับ sample ที่วิเคราะห์เสร็จแล้ว</p></dd>
    <dt><a href="#banshee-sandbox-report-static"><code>banshee sandbox report static</code></a></dt><dd><p>รายงาน static analysis — มีให้ก่อน behavioural task เสร็จสิ้น</p></dd>
    <dt><a href="#banshee-sandbox-report-behavioral"><code>banshee sandbox report behavioral</code></a></dt><dd><p>รายงาน behavioural analysis — หนึ่ง object ต่อ task ที่เสร็จสมบูรณ์</p></dd>
</dl>

#### banshee sandbox report overview

รายงานสรุปฉบับเต็มสำหรับ sample ที่วิเคราะห์เสร็จแล้ว ประกอบด้วย verdict score, malware family, tags, hashes, detection signature, malware config ที่ดึงมา, network IOC และผลลัพธ์แต่ละ task Sample ต้องอยู่ในสถานะ `reported`

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report overview [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--sample-id"><a href="#banshee-sandbox-report-overview--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>Sample ID ที่ต้องการดึงรายงาน</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-overview--wait"><a href="#banshee-sandbox-report-overview--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>Poll จนกว่ารายงานจะพร้อม (สูงสุด 30 นาที) ออกด้วย exit code ที่ไม่ใช่ศูนย์หากยังไม่พร้อมหลังจาก timeout</p></dd>
    <dt id="banshee-sandbox-report-overview--pretty"><a href="#banshee-sandbox-report-overview--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-report-overview--help"><a href="#banshee-sandbox-report-overview--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

รายงาน static analysis สำหรับ sample ประกอบด้วย verdict score, tags, ไฟล์ที่ unpack, static detection signature และ malware config ที่ดึงมา มีให้ก่อน behavioural task เสร็จสิ้น

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report static [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--sample-id"><a href="#banshee-sandbox-report-static--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>Sample ID ที่ต้องการดึงรายงาน static</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-static--wait"><a href="#banshee-sandbox-report-static--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>Poll จนกว่ารายงานจะพร้อม (สูงสุด 10 นาที)</p></dd>
    <dt id="banshee-sandbox-report-static--pretty"><a href="#banshee-sandbox-report-static--pretty"><code>--pretty</code></a>, <code>-p</code></dt><dd>
    <p>แสดงผลลัพธ์ในรูปแบบที่อ่านง่ายสำหรับมนุษย์</p></dd>
    <dt id="banshee-sandbox-report-static--help"><a href="#banshee-sandbox-report-static--help"><code>--help</code></a>, <code>-h</code></dt><dd>
    <p>แสดงความช่วยเหลือสำหรับคำสั่งนี้</p>
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

รายงาน behavioural analysis สำหรับ sample ส่งคืน JSON object หนึ่งรายการต่อ behavioural task ที่เสร็จสมบูรณ์ ประกอบด้วย verdict score, platform, signature ที่ถูก trigger, process ที่สังเกตพบ, network activity และ malware config ที่ดึงมา

Task ที่ยังไม่เสร็จสมบูรณ์จะถูกละเว้นจาก output และแสดงใน stderr คำสั่งจะออกด้วย exit code ที่ไม่ใช่ศูนย์จนกว่า task ทั้งหมดจะเสร็จสมบูรณ์ จะส่งคืน array ว่างพร้อม exit 0 เมื่อไม่มี behavioural task สำหรับ sample

โดยค่าเริ่มต้น คำสั่งจะแสดงผลลัพธ์ในรูปแบบ JSON

<h3 class="commands-reference">Usage</h3>

```
banshee sandbox report behavioral [OPTIONS] SAMPLE_ID
```

<h3 class="commands-reference">Arguments</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--sample-id"><a href="#banshee-sandbox-report-behavioral--sample-id"><code>SAMPLE_ID</code></a></dt><dd><p>Sample ID ที่ต้องการดึงรายงาน behavioural</p></dd>
</dl>

<h3 class="commands-reference">Options</h3>

<dl class="commands-reference">
    <dt id="banshee-sandbox-report-behavioral--wait"><a href="#banshee-sandbox-report-behavioral--wait"><code>--wait</code></a>, <code>-w</code></dt><dd>
    <p>Poll จนกว่า task ทั้งหมดจะเสร็จสมบูรณ์ (สูงสุด 30 นาที)</p></dd>
    <dt id="banshee-sandbox-report-behavioral--full-cmd"><a href="#banshee-sandbox-report-behavioral--full-cmd"><code>--full-cmd</code></a></dt><dd>
    <p>แสดง command line ของ process แบบเต็มโดยไม่ตัดทอน เนื้อหา command line นำมาโด