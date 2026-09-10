# ioc

> ดูที่ [index.md](index.md) สำหรับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบเอาต์พุต และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee ioc lookup ENTITY_TYPE [IOC]...`

การเสริมข้อมูลเชิงลึกแบบรายตัว (per-IOC enrichment) สำหรับ IOC แต่ละรายการ โดยใช้หนึ่ง API call ต่อหนึ่ง indicator เหมาะสำหรับการวิเคราะห์บริบทเชิงลึก

**ประเภท entity:** `ip`, `domain`, `url`, `hash`, `vulnerability`

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--verbosity INTEGER` | `-v` | `1` | ระดับรายละเอียด 1–5 (ดูตาราง verbosity ด้านล่าง) |
| `--ai-insights` | `-a` | | รวมสรุปที่สร้างโดย AI สำหรับ risk rule |
| `--pretty` | `-p` | | จัดรูปแบบเอาต์พุต (Pretty print) |

**ระดับ verbosity แยกตามประเภท entity:**

| ระดับ | ip | domain | hash | url | vulnerability |
|-------|----|--------|------|-----|---------------|
| 1 | entity, risk, timestamps | entity, risk, timestamps | entity, hashAlgorithm, risk, timestamps | entity, risk, timestamps | entity, lifecycleStage, risk, timestamps |
| 2 | + intelCard, location | + intelCard | + fileHashes, intelCard | + intelCard | + intelCard |
| 3 | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links |
| 4 | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings | + cvss, cvssv3, cvssv4, enterpriseLists, riskMapping, sightings, threatLists |
| 5 | + dnsPortCert, scanner | เหมือนระดับ 4 | เหมือนระดับ 4 | เหมือนระดับ 4 | + cpe, cpe22uri, nvdDescription, nvdReferences |

```bash
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p

# Pipe from CSV file
cat test_ips.csv | banshee ioc lookup ip -p
```

**รูปแบบ response (verbosity 1):** คืนค่าเป็น JSON array โดยแต่ละรายการมี `entity`, `risk`, `timestamps` ระดับ verbosity ที่สูงขึ้นจะเพิ่มข้อมูล: v2 `+intelCard, location`; v3 `+analystNotes, links`; v4 `+enterpriseLists, riskMapping, sightings, threatLists`; v5 `+dnsPortCert, scanner` (เฉพาะ ip เท่านั้น)

ฟิลด์ของแต่ละรายการใน `.risk.evidenceDetails[]`:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.rule` | ชื่อ rule ในรูปแบบ string |
| `.criticality` | จำนวนเต็ม 0–4 (0–5 สำหรับ vulnerability) |
| `.criticalityLabel` | ป้ายกำกับที่อ่านได้ (เช่น `"Unusual"`, `"Malicious"`) |
| `.evidenceString` | คำอธิบาย evidence ที่อ่านได้ |
| `.mitigationString` | คำแนะนำสำหรับ mitigation (อาจเป็น string ว่าง) |
| `.timestamp` | timestamp ของ evidence ล่าสุด (ISO 8601) |

**สูตร jq ขั้นสูง:**

```bash
# Most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'

# All triggered rules
banshee ioc lookup ip 1.2.3.4 | jq '.[].risk.evidenceDetails[].rule'

# Risk score + most critical rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | { score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] } ]'

# Risk score + all rules with criticality labels
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | { score: .risk.score, rules: [.risk.evidenceDetails[] | {rule, label: .criticalityLabel}] } ]'
```

---

### `banshee ioc bulk-lookup ENTITY_TYPE [IOC]...`

การเสริมข้อมูลแบบกลุ่ม (bulk enrichment) ความเร็วสูง — ประมวลผลสูงสุด 1,000 IOC ต่อหนึ่ง API call โดยคืนค่าเฉพาะ risk score และ risk rule ที่ถูกเรียกใช้งาน เหมาะสำหรับการคัดกรองปริมาณสูง (high-volume triage)

| ตัวเลือก | คำอธิบาย |
|--------|-------------|
| `--pretty` / `-p` | จัดรูปแบบเอาต์พุต (Pretty print) |

**รูปแบบ response:** คืนค่าเป็น JSON array โดยแต่ละรายการมี `entity` (`id`, `name`, `type`) และ `risk` หมายเหตุ: ไม่มี key `timestamps` (ต่างจาก `ioc lookup`)

ฟิลด์ใน `.risk`:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.risk.score` | จำนวนเต็ม risk score 0–99 |
| `.risk.level` | จำนวนเต็มระดับ criticality |
| `.risk.context` | Object บริบทที่จัดกลุ่มตาม risk domain (`phishing`, `public`, `c2`, `malware`) |
| `.risk.rule.count` | จำนวน rule ที่ถูกเรียกใช้งาน |
| `.risk.rule.maxCount` | จำนวน rule สูงสุดที่เป็นไปได้ |
| `.risk.rule.mostCritical` | ชื่อ rule ที่มี criticality สูงสุด |
| `.risk.rule.summary` | Array ของ string สรุป |
| `.risk.rule.evidence[]` | Array ของ object สำหรับ rule ที่ถูกเรียกใช้งาน |

ฟิลด์ของแต่ละรายการใน `.risk.rule.evidence[]`:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.rule` | ชื่อ rule ในรูปแบบ string |
| `.level` | จำนวนเต็ม criticality 0–4 |
| `.description` | string evidence ที่มี HTML tag (การอ้างอิง entity ใช้ markup `<e id=...>`) |
| `.count` | จำนวนครั้งที่พบ (Hit count) |
| `.sightings` | จำนวน sighting |
| `.timestamp` | timestamp ของ evidence ล่าสุด (ISO 8601) |
| `.mitigation` | คำแนะนำสำหรับ mitigation (อาจเป็น string ว่าง) |
| `.type` | ประเภท rule ในรูปแบบ string (เช่น `linkedIntrusion`) |

Evidence ของ bulk risk rule อยู่ภายใต้ `.risk.rule.evidence[]` ซึ่งแตกต่างจาก `ioc lookup` ที่ใช้ `.risk.evidenceDetails[]`

```bash
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877

# From file (one IOC per line)
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability

# Extract names and scores
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

# Extract names, scores, and triggered rule names
banshee ioc bulk-lookup ip 92.38.178.133 | jq '[.[] | {ioc: .entity.name, score: .risk.score, rules: [(.risk.rule.evidence // [])[].rule]}]'
```

---

### `banshee ioc search ENTITY_TYPE`

ค้นหาใน RF IOC corpus พร้อมตัวกรอง

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--limit INTEGER` | `-l` | `5` | จำนวนผลลัพธ์สูงสุด (1–1000) |
| `--risk-score TEXT` | `-r` | | ช่วง risk score (รูปแบบ interval notation) |
| `--risk-rule TEXT` | `-R` | | กรองตามชื่อ risk rule |
| `--verbosity INTEGER` | `-v` | `1` | ระดับรายละเอียด 1–5 (ตารางเดียวกับ `ioc lookup`) |
| `--pretty` | `-p` | | จัดรูปแบบเอาต์พุต (Pretty print) |

**รูปแบบ interval notation สำหรับ risk score:**

| รูปแบบ | ความหมาย |
|--------|---------|
| `'[20,90]'` | 20 ≤ score ≤ 90 |
| `'(20,90)'` | 20 < score < 90 |
| `'[20,90)'` | 20 ≤ score < 90 |
| `'[20,)'` | score ≥ 20 |
| `'[,90)'` | score < 90 |

เอาต์พุต JSON เริ่มต้นเป็น object ผลลัพธ์การค้นหาอยู่ภายใต้ `.data.results[]` และจำนวนทั้งหมด/จำนวนที่คืนกลับมาอยู่ภายใต้ `.counts`

```bash
banshee ioc search ip -l 10 -r '(,80]'
banshee ioc search domain -r '[90,)'
banshee ioc search hash -r '[80,81]' -p
banshee ioc search vulnerability --limit 1 -v 3

# Extract IOC names from search results
banshee ioc search ip -r '[90,)' -l 100 | jq -r '.data.results[].entity.name'
```

---

### `banshee ioc rules ENTITY_TYPE`

แสดงรายการ risk rule สำหรับประเภท entity พร้อมตัวกรองที่เลือกได้

| ตัวเลือก | ย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--freetext TEXT` | `-F` | กรอง rule ตามชื่อหรือคำอธิบาย |
| `--mitre-code TEXT` | `-M` | กรองตามรหัส MITRE ATT&CK (เช่น `T1587.004`) |
| `--criticality INTEGER` | `-C` | กรองตาม criticality 0–5 |
| `--pretty` | `-p` | จัดรูปแบบเอาต์พุต (Pretty print) |

**อ้างอิงระดับ criticality (IP, Domain, URL, Hash):**

| ระดับ | ป้ายกำกับ | ช่วง Risk Score |
|-------|-------|----------------|
| 4 | Very Malicious | 90–99 |
| 3 | Malicious | 65–89 |
| 2 | Suspicious | 25–64 |
| 1 | Unusual | 5–24 |
| 0 | No evidence of risk | 0 |

**อ้างอิงระดับ criticality (Vulnerability):**

| ระดับ | ป้ายกำกับ | ช่วง Risk Score |
|-------|-------|----------------|
| 5 | Very Critical | 90–99 |
| 4 | Critical | 80–89 |
| 3 | High | 65–79 |
| 2 | Medium | 25–64 |
| 1 | Low | 5–24 |
| 0 | No evidence of risk | 0 |

```bash
banshee ioc rules ip
banshee ioc rules domain -p
banshee ioc rules hash -C 3
banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept
```

**รูปแบบ response:** คืนค่าเป็น JSON array แบบ flat โดยแต่ละรายการแทน risk rule หนึ่งรายการ:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.name` | ชื่อ rule ในรูปแบบ string — ใช้ค่านี้กับ `--risk-rule` ในคำสั่ง `ioc search` และ `risklist` (เช่น `"recentActiveCnc"`) |
| `.criticalityLabel` | ป้ายกำกับที่อ่านได้ (เช่น `"Very Malicious"`) |
| `.criticality` | จำนวนเต็มระดับ criticality |
| `.description` | string คำอธิบาย rule |
| `.categories[]` | Array ของ object `{name, framework}` — หมวดหมู่ MITRE ATT&CK (เช่น `{name: "TA0011", framework: "MITRE"}`) |
| `.relatedEntities[]` | Array ของ RF entity ID string ที่ rule นี้อ้างอิงถึง |
| `.count` | จำนวน IOC ที่ตรงกับ rule นี้ในปัจจุบัน |

```bash
# List all rule names for an entity type
banshee ioc rules ip | jq -r '.[].name'

# Find rules above criticality 3 with their descriptions
banshee ioc rules ip | jq '[.[] | select(.criticality >= 3) | {name, criticalityLabel, description}]'
```