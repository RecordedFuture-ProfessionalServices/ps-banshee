# ca

> **Classic Alerts** - การแจ้งเตือนแบบ rule-based รูปแบบเดิม (legacy) โดย ID จะเป็นสตริงสั้น ๆ ที่ไม่โปร่งใส ความยาว 6 อักขระขึ้นไป (เช่น `tybakN`) สำหรับการแจ้งเตือนแบบอัตโนมัติ/ขับเคลื่อนด้วย playbook (ID เป็น UUID 36 อักขระ มี prefix `task:` ได้ตามต้องการ หมวดหมู่เช่น `domain_abuse` / `third_party_risk` / ฯลฯ) ให้ใช้ [`pba`](pba.md) แทน
>
> ดู [index.md](index.md) สำหรับการยืนยันตัวตน การตรวจสอบความพร้อม ข้อตกลงด้าน output และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee ca lookup ALERT_ID`

ดึงข้อมูล Classic Alert รายการเดียวตาม ID

| อาร์กิวเมนต์/ตัวเลือก | คำอธิบาย |
|-----------------|-------------|
| `ALERT_ID` (จำเป็น) | Alert ID เช่น `tybakN` |
| `--pretty` / `-p` | แสดงผลแบบ pretty print |

```bash
banshee ca lookup tybakN
banshee ca lookup tybakN -p
```

**รูปแบบ Response:** คืนค่าเป็น JSON object รายการเดียว

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | Alert ID |
| `.title` | ชื่อ alert |
| `.type` | สตริงประเภท alert (เช่น `"EVENT"`) |
| `.log.triggered` | timestamp ที่ trigger (ISO 8601) |
| `.review.status_in_portal` | สถานะที่อ่านได้โดยมนุษย์: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.assignee` | อีเมลของนักวิเคราะห์ที่ได้รับมอบหมาย |
| `.rule.id` | ID ของกฎ alert |
| `.rule.name` | ชื่อกฎ alert |
| `.url.portal` | ลิงก์ตรงไปยัง alert ใน RF portal |
| `.ai_insights.text` | สตริงสรุปที่สร้างโดย RF AI |
| `.hits[]` | เอกสารที่ trigger alert |
| `.hits[].id` | ID ของเอกสาร hit |
| `.hits[].fragment` | ข้อความที่ตรงกัน (text snippet) |
| `.hits[].language` | รหัสภาษา (เช่น `"eng"`) |
| `.hits[].entities[]` | entities ที่พบใน hit: `{id, name, type}` |
| `.hits[].document.title` | ชื่อเอกสารต้นทาง |
| `.hits[].document.url` | URL เอกสารต้นทาง |
| `.hits[].document.source` | สตริงชื่อแหล่งที่มา |
| `.hits[].document.authors` | อาร์เรย์ของสตริงชื่อผู้แต่ง (อาจว่างเปล่า) |
| `.triggered_by[]` | entities/กฎที่ trigger alert (อาจว่างเปล่า) |
| `.triggered_by[].reference_id` | ID เอกสารอ้างอิง |
| `.triggered_by[].triggered_by_strings[]` | คำอธิบาย trigger ที่อ่านได้โดยมนุษย์ |
| `.enriched_entities[]` | entity object ที่ผ่านการ enrich ล่วงหน้าพร้อม RF context (อาจว่างเปล่า) |

```bash
# Extract all entities from alert hits for enrichment
banshee ca lookup tybakN | jq '[.hits[].entities[] | {id, name, type}] | unique_by(.id)'

# Get the AI summary
banshee ca lookup tybakN | jq -r '.ai_insights.text'

# Get portal link
banshee ca lookup tybakN | jq -r '.url.portal'
```

---

### `banshee ca search`

ค้นหา Classic Alerts พร้อมตัวกรองเพิ่มเติมตามต้องการ

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--triggered TEXT` | `-t` | `1d` | ช่วงเวลา แบบ relative (`1d`, `12h`) หรือช่วงเวลาแบบ absolute (`[2024-08-01, 2024-08-14]`) |
| `--rule TEXT` | `-r` | | กรองตามชื่อกฎ alert (freetext ใช้ซ้ำได้) |
| `--status` | `-s` | | ค่าใดค่าหนึ่ง: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--pretty` | `-p` | | แสดงผลแบบ pretty print |

```bash
banshee ca search -t 1d
banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending
banshee ca search -t 12h -p
banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d
banshee ca search -r leaked -t 12h -p
```

**รูปแบบ Response:** คืนค่าเป็น JSON array แต่ละ alert object มีฟิลด์ระดับบนสุดดังนี้:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | Alert ID (เช่น `tybakN`) |
| `.title` | ชื่อ alert |
| `.log.triggered` | timestamp ที่ trigger (ISO 8601) |
| `.review.status_in_portal` | สถานะที่อ่านได้โดยมนุษย์: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.status` | สตริงสถานะภายใน (`no-action` ฯลฯ) — ไม่เหมาะสำหรับการกรองด้วย jq |
| `.rule.name` | ชื่อกฎ alert ที่ทำงาน |
| `.rule.id` | ID ของกฎ alert |

**หมายเหตุ:** ไม่มีฟิลด์ `priority` ระดับบนสุดใน alert record ของ `ca search` ให้ใช้ `.review.status_in_portal` (ไม่ใช่ `.review.status`) เมื่อกรองตามสถานะใน jq pipelines

```bash
# Extract IDs of New alerts (use status_in_portal for jq filtering)
banshee ca search -t 1d | jq -r '.[] | select(.review.status_in_portal == "New") | .id'

# When using the -s flag, status filtering happens server-side — no jq select needed
banshee ca search -t 1d -s New | jq -r '.[].id'
```

---

### `banshee ca rules [FREETEXT]`

แสดงรายการกฎ Classic Alert ทั้งหมด โดยกรองด้วย freetext ได้ตามต้องการ

| อาร์กิวเมนต์/ตัวเลือก | คำอธิบาย |
|-----------------|-------------|
| `FREETEXT` (ไม่บังคับ) | คำค้นหาสำหรับกรองชื่อกฎ |
| `--pretty` / `-p` | แสดงผลแบบ pretty print |

```bash
banshee ca rules
banshee ca rules -p
```

**รูปแบบ Response:** คืนค่าเป็น JSON array แบบ flat แต่ละรายการมีฟิลด์ดังนี้:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | Rule ID (เช่น `k_TnPe`) |
| `.title` | ชื่อกฎ |
| `.enabled` | `true`/`false` — กฎนี้ active หรือไม่ |
| `.priority` | `true` = alert จากกฎนี้มีความรุนแรงระดับ **High**; `false` = ระดับ **Informational** หากต้องการจัดลำดับความสำคัญ ให้ดึงรายการกฎก่อน แล้ว join กับ alert ผ่าน `.rule.id` (ดู Priority triage workflow ด้านล่าง) |
| `.tags` | อาร์เรย์ของสตริง tag |
| `.created` | timestamp ที่สร้าง (ISO 8601) |
| `.owner` | object ที่มี `id` และ `name` — เจ้าของกฎ |
| `.intelligence_goals` | อาร์เรย์ของ object `{id, name}` — intelligence goals ที่เกี่ยวข้อง |
| `.notification_settings` | object ที่มีอาร์เรย์ `email_subscribers` |

ใช้ `.title` และ `.id` เมื่อสร้าง pipeline `.priority` แมปตรงกับความรุนแรงของ alert: `true` คือ High และ `false` คือ Informational

---

### Priority triage workflow

`ca search` และ `ca lookup` ไม่คืนค่าฟิลด์ความรุนแรงต่อ alert หากต้องการจัดลำดับความสำคัญของ alert ตามความรุนแรง ให้ดึงรายการกฎก่อน กรองเฉพาะกฎที่ `.priority == true` แล้วนำไปตัดกับค่า `.rule.id` ของ alert:

```bash
# High-priority alert IDs in the last day
PRIORITY_RULES=$(banshee ca rules | jq -r '.[] | select(.priority == true) | .id' | paste -sd'|' -)
banshee ca search -t 1d | jq --arg rules "$PRIORITY_RULES" -r '.[] | select(.rule.id | test("^(" + $rules + ")$")) | .id'
```

นำ ID ที่ได้ไป pipe ต่อเข้า `banshee ca update` โดยตรง เพื่อเปลี่ยนสถานะเฉพาะ alert ที่มีความสำคัญสูง

---

### `banshee ca update [ALERT_IDS]...`

อัปเดต Classic Alert หนึ่งรายการขึ้นไป สามารถส่ง ID เป็นอาร์กิวเมนต์คั่นด้วยช่องว่าง หรือ pipe ผ่าน stdin ได้

| ตัวเลือก | ย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--status` | `-s` | สถานะใหม่: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--note TEXT` | `-n` | เพิ่มหมายเหตุข้อความ |
| `--append` | `-A` | ต่อท้ายหมายเหตุที่มีอยู่แทนการเขียนทับ |
| `--assignee TEXT` | `-a` | มอบหมาย alert ใหม่ รับค่าเป็น `uhash:3aXZxdkM12` หรือ `analyst@acme.com` |

**วิธีการรับข้อมูลเข้า:**

```bash
# Single ID
banshee ca update 8cORlQ -s Resolved

# Multiple IDs (space-separated)
banshee ca update 8cORlQ 8biCIG -s Pending

# Pipe IDs from file
cat alerts.txt | banshee ca update -s Dismissed

# Pipe from search via jq
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"

# stdin redirect
banshee ca update -s Dismissed < alerts.txt
```

**Response:** คืนค่าเป็น plain text ไม่ใช่ JSON — หนึ่งบรรทัดต่อ alert ที่อัปเดต: `SUCCESS:\n<ALERT_ID>` ไม่ควร pipe ไปยัง `jq`

---

### `banshee ca export`

ดึงรายละเอียด alert แบบเต็มสำหรับ alert ที่ได้จาก `ca search` และส่งออกเป็น JSON หรือ CSV โดยรับข้อมูลผ่าน **stdin เท่านั้น** — ให้ pipe JSON array จาก `banshee ca search` และไม่มีอาร์กิวเมนต์แบบ positional

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--csv` | | JSON | ส่งออกเป็น CSV (ชุดคอลัมน์คงที่) แทน JSON (รายละเอียด alert แบบเต็ม) |

```bash
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s Pending | banshee ca export --csv > alerts.csv
```

**Input:** รับ JSON array ที่ส่งออกโดย `banshee ca search` ทาง stdin โดยทุก element ต้องมี `id` หากรันโดยไม่มีข้อมูล pipe (TTY) จะเกิดข้อผิดพลาด `BadParameter`

**รูปแบบ Response (ค่าเริ่มต้น):** JSON array ของ alert object แบบเต็ม — มีโครงสร้างต่อ alert เดียวกับที่ `banshee ca lookup` คืนค่า (`.id`, `.title`, `.log.triggered`, `.review`, `.rule`, `.hits[]` ฯลฯ)

**รูปแบบ Response (`--csv`):** CSV ที่มีแถว header และคอลัมน์คงที่เหล่านี้: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Title`, `Assignee`, `URL`, `Entities`, `Recorded Future AI Insights` โดย `Priority` ได้มาจากกฎ alert (`High` เมื่อกฎเป็น priority rule มิฉะนั้นเป็น `Informational`) และเครื่องหมายจุลภาคภายในค่าฟิลด์จะถูกแทนที่ด้วยช่องว่าง