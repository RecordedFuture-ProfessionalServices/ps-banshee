# entity

> ดู [index.md](index.md) สำหรับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบเอาต์พุต และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee entity lookup ENTITY_ID`

ค้นหา entity ของ Recorded Future โดยใช้ ID

| อาร์กิวเมนต์/ตัวเลือก | คำอธิบาย |
|-----------------|-------------|
| `ENTITY_ID` (จำเป็น) | RF entity ID เช่น `qf0H03` |
| `--pretty` / `-p` | แสดงผลแบบจัดรูปแบบ |

```bash
banshee entity lookup qf0H03
banshee entity lookup qf0H03 -p
```

**รูปแบบการตอบกลับ:** คืนค่าออบเจกต์ JSON รายการเดียว โดยมี key ระดับบนสุดได้แก่ `id`, `type` และ `attributes` ชื่อ entity จะอยู่ภายใต้ `.attributes.name` ไม่ใช่ที่ระดับบนสุด

```bash
# Correct jq to extract id, type, and name:
banshee entity lookup qf0H03 | jq '{id, type, name: .attributes.name}'
```

---

### `banshee entity search NAME`

ค้นหา entity ตามชื่อ โดยสามารถกรองตามประเภทได้

| อาร์กิวเมนต์/ตัวเลือก | ตัวย่อ | ค่าเริ่มต้น | คำอธิบาย |
|-----------------|-------|---------|-------------|
| `NAME` (จำเป็น) | | | ชื่อ entity ที่ต้องการค้นหา |
| `--type` | `-t` | | ประเภท entity อย่างน้อยหนึ่งประเภท (ระบุซ้ำได้) ดูรายการประเภททั้งหมดด้านล่าง |
| `--limit INTEGER` | `-l` | `100` | จำนวนผลลัพธ์สูงสุด (1–100) |
| `--pretty` | `-p` | | แสดงผลแบบจัดรูปแบบ |

**ประเภท entity ที่พบบ่อย (รายการบางส่วน):** `Malware`, `IpAddress`, `InternetDomainName`, `URL`, `Hash`, `CyberVulnerability`, `CyberThreatActorCategory`, `Organization`, `Person`, `Country`, `MitreAttackIdentifier`, `YaraDetectionRule`, `SnortDetectionRule`, `SigmaDetectionRule` (และอื่น ๆ อีกกว่า 100 ประเภท)

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**รูปแบบการตอบกลับ:** คืนค่าอาร์เรย์ JSON แบบแบน แต่ละรายการมีฟิลด์สามฟิลด์ดังนี้:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | RF entity ID (เช่น `SoA6SP`) |
| `.name` | ชื่อที่แสดงของ entity |
| `.type` | สตริงประเภท entity (เช่น `Malware`, `InternetDomainName`) |

```bash
# Extract all IDs matching a name
banshee entity search "Cobalt Strike" -t Malware | jq -r '.[].id'

# Build a lookup table of id → name
banshee entity search wannacry | jq '[.[] | {(.id): .name}] | add'
```


---

### `banshee entity links ENTITY_ID...`

ดึงข้อมูล entity ที่เชื่อมโยงกับ entity อย่างน้อยหนึ่งรายการ (IOC (Indicator of Compromise), detection rule, malware, TTP (Tactics, Techniques, and Procedures) และ threat actor) Entity ID คือ Recorded Future entity ID (เช่น ที่ได้จาก `banshee entity search`) ไม่ใช่ชื่อ entity IOC ที่เชื่อมโยงจะได้รับการเสริมข้อมูลผ่าน SOAR เว้นแต่จะระบุ `--skip-enrichment`

Entity ID สามารถส่งเป็นอาร์กิวเมนต์คั่นด้วยช่องว่าง หรือส่งผ่าน pipe / redirect ทาง stdin (หนึ่ง ID ต่อบรรทัด) อย่าเพิ่มคำสั่งย่อย (เช่น `links search`) เนื่องจากไม่มีคำสั่งดังกล่าว และคำเพิ่มเติมใด ๆ จะถูกตีความว่าเป็น entity ID

| อาร์กิวเมนต์/ตัวเลือก | ตัวย่อ | ค่าเริ่มต้น | คำอธิบาย |
|-----------------|-------|---------|-------------|
| `ENTITY_ID...` | | stdin | Entity ID อย่างน้อยหนึ่งรายการ |
| `--type TEXT` | `-t` | | ประเภท entity ที่ต้องการคืนค่า ระบุซ้ำได้ |
| `--source [Technical\|Insikt]` | `-s` | | แหล่งที่มาของลิงก์ที่ต้องการคืนค่า |
| `--sections TEXT` | `-S` | | กรองตามประเภทลิงก์ เช่น `'Indicators and Detection Rules'` ระบุซ้ำได้ |
| `--timeframe TEXT` | `-T` | | ช่วงเวลาที่ลิงก์ถูกสร้างขึ้น เช่น `-1d` (สูงสุด `-90d`) |
| `--events TEXT` | `-e` | | กรองตามประเภทเหตุการณ์ เช่น `type:MalwareAnalysis` ระบุซ้ำได้ |
| `--connected-entities TEXT` | `-c` | | คืนเฉพาะ entity ที่เชื่อมโยงกับ entity เหล่านี้ด้วย ระบุซ้ำได้ |
| `--limit INTEGER` | `-l` | | จำนวน entity สูงสุดที่คืนค่าต่อประเภท (1–1,000,000) |
| `--small` | | | ค้นหา 10 references และ 10 Insikt Notes ต่อประเภทเหตุการณ์ |
| `--large` | | | ค้นหา 100 references และ 500 Insikt Notes ต่อประเภทเหตุการณ์ |
| `--skip-enrichment` | | | ข้ามการเสริมข้อมูลเพิ่มเติมของ IOC ที่เชื่อมโยง |
| `--pretty` | `-p` | | แสดงผลแบบจัดรูปแบบ |

`--small` และ `--large` ใช้ร่วมกันไม่ได้ หากไม่ระบุตัวเลือกใดเลย จะใช้ขอบเขตขนาดกลาง

**รูปแบบการตอบกลับ:** คืนค่าอาร์เรย์ JSON โดยมีหนึ่งออบเจกต์ต่อ entity ที่ส่งเข้ามา แต่ละออบเจกต์ประกอบด้วย `entity` ที่ค้นหาและ `links` ของ entity นั้น แต่ละลิงก์มีฟิลด์ `enrichment` ซึ่งเก็บข้อมูลการเสริมจาก SOAR สำหรับ IOC ที่เชื่อมโยง หรือ `null` สำหรับลิงก์ที่ไม่ใช่ IOC, IOC ที่ไม่ได้รับการเสริมข้อมูล หรือเมื่อใช้ `--skip-enrichment` หากการเสริมข้อมูลจาก SOAR ล้มเหลว จะมีข้อความแจ้งเตือนแสดงที่ stderr และการเสริมข้อมูลจะถูกข้ามไป

เอาต์พุตแบบจัดรูปแบบ (แสดงที่ stderr) จะแสดงตารางต่อ entity ของ IOC ที่เชื่อมโยง (พร้อม risk score, risk rule อันดับต้น และลิงก์ไปยัง intelligence card), TTP, malware และ threat actor โดยแต่ละตารางมีจำนวนแถวสูงสุด 20 แถว การเสริมข้อมูล IOC ในโหมดแสดงผลแบบจัดรูปแบบจะจำกัดที่ 20 IOC ต่อประเภทเช่นกัน

```bash
banshee entity links BUl6R5r
banshee entity links BUl6R5r -T -10d --small -p
banshee entity links BUl6R5r sIG7Rn -T -10d --large > links.json

# Skip enrichment for faster results
banshee entity links BUl6R5r --skip-enrichment

# Entity IDs from a file or pipe
banshee entity links -T -1d < link_entities.txt
cat link_entities.txt | banshee entity links -T -1d --large > links_out.json

# Find an entity ID first, then search its links
banshee entity search wannacry -t Malware -l 1 | jq -r '.[].id' | banshee entity links --small
```


---