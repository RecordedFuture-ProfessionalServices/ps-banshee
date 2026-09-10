# pba

> **Playbook Alerts** - การแจ้งเตือนที่ขับเคลื่อนด้วยระบบอัตโนมัติ โดย ID เป็น UUID ขนาด 36 อักขระ และ prefix `task:` เป็นทางเลือก (เช่น `d144a9ec-90e6-40fe-89b0-d85ed65d3e9c` หรือ `task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c`) หมวดหมู่เฉพาะของ PBA ได้แก่: `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report` สำหรับการแจ้งเตือนแบบ rule-based แบบเดิม (ID สั้นและไม่โปร่งใส) ให้ใช้ [`ca`](ca.md) แทน
>
> โปรดดู [index.md](index.md) สำหรับข้อมูลเกี่ยวกับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบผลลัพธ์ และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee pba search`

ค้นหา Playbook Alerts ด้วยตัวกรองที่หลากหลาย

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--created TEXT` | `-C` | | กรองตามวันที่สร้าง (เช่น `1d`, `7d`) |
| `--updated TEXT` | `-u` | | กรองตามวันที่อัปเดต |
| `--category` | `-c` | all | หนึ่งหมวดหมู่หรือมากกว่า (ระบุซ้ำได้): `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report` |
| `--entity TEXT` | `-e` | | กรองตาม entity ที่เกี่ยวข้อง (ระบุซ้ำได้) |
| `--priority` | `-P` | all | `Informational`, `Moderate`, `High` (ระบุซ้ำได้) |
| `--status` | `-s` | all | `New`, `InProgress`, `Dismissed`, `Resolved` (ระบุซ้ำได้) |
| `--org-id TEXT` | `-o` | all | กรองตาม ID ขององค์กรเจ้าของ (ระบุซ้ำได้) รองรับ ID ขนาด 10 อักขระ หรือรูปแบบ `uhash:` ขนาด 16 อักขระ |
| `--limit INTEGER` | `-l` | `100` | จำนวนผลลัพธ์สูงสุด (1–10000) |
| `--pretty` | `-p` | | แสดงผลในรูปแบบที่อ่านง่าย (Pretty print) |

**รูปแบบการตอบสนอง:** คืนค่าเป็น JSON object ที่มีสามคีย์ระดับบนสุด ได้แก่ `.data` (อาร์เรย์ของระเบียนการแจ้งเตือน), `.counts` (`{returned, total}`), และ `.status` (object สถานะของคำขอ: `{status_code, status_message}`) ระเบียนการแจ้งเตือนอยู่ภายใต้ `.data[]` พร้อมฟิลด์: `playbook_alert_id`, `alert_rule` (`{id, label, name}`), `category`, `priority`, `status`, `title`, `created`, `updated`, `actions_taken`, `owner_organisation_details`

```bash
banshee pba search --created 1d
banshee pba search -C 1d -u 1d -p
banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse
banshee pba search --updated 7d --category domain_abuse --pretty
banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New
banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d
banshee pba search -o 69sKLfTGsS -o uhash:5zQaSyRpA1 -C 7d -P High
```

---

### `banshee pba lookup ALERT_ID`

ดึงข้อมูล Playbook Alert รายการเดียวตาม ID โดยรองรับ UUID ขนาด 36 อักขระทั้งแบบที่มีหรือไม่มี prefix `task:` — CLI จะเติม `task:` ให้โดยอัตโนมัติหากเป็น UUID ที่ไม่มี prefix

```bash
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p
```

**รูปแบบการตอบสนอง:** คืนค่าเป็น JSON object รายการเดียวที่มีสี่คีย์ระดับบนสุด: `playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`

**`.panel_status`** — ข้อมูลเมตาของการแจ้งเตือนและสถานะปัจจุบัน:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.panel_status.status` | สถานะปัจจุบัน: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `.panel_status.priority` | ระดับความสำคัญ: `Informational`, `Moderate`, `High` |
| `.panel_status.case_rule_label` | ชื่อกฎที่มนุษย์อ่านได้ (เช่น `"Data Leakage on Code Repository"`) |
| `.panel_status.entity_id` | RF entity ID ของหัวข้อหลัก (เช่น `"url:https://..."`) |
| `.panel_status.entity_name` | ชื่อ entity หลัก |
| `.panel_status.risk_score` | ค่าคะแนนความเสี่ยง RF (integer) |
| `.panel_status.targets[]` | อาร์เรย์ของ object `{name}` — entities ที่ถูกกำหนดเป้าหมายหรือได้รับผลกระทบ |
| `.panel_status.actions_taken[]` | การดำเนินการที่บันทึกไว้แล้วในการแจ้งเตือน |
| `.panel_status.created` | เวลาที่สร้าง (ISO 8601) |
| `.panel_status.updated` | เวลาที่อัปเดตล่าสุด (ISO 8601) |

**`.panel_evidence_summary`** — รายละเอียดหลักฐาน โดยโครงสร้างจะแตกต่างกันตามหมวดหมู่ของการแจ้งเตือน สำหรับ `code_repo_leakage`:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.panel_evidence_summary.repository.name` | URL ของ repository |
| `.panel_evidence_summary.repository.owner.name` | ชื่อ login ของเจ้าของ repository |
| `.panel_evidence_summary.evidence[]` | อาร์เรย์ของรายการหลักฐาน |
| `.panel_evidence_summary.evidence[].url` | URL ต้นทางของเนื้อหาที่ถูกเปิดเผย |
| `.panel_evidence_summary.evidence[].content` | ข้อความตัดย่อของเนื้อหาที่ถูกเปิดเผย |
| `.panel_evidence_summary.evidence[].assessments[]` | object การประเมิน: `{id, title, value}` |
| `.panel_evidence_summary.evidence[].targets[]` | entities เป้าหมาย: `{name}` |
| `.panel_evidence_summary.evidence[].published` | เวลาที่เผยแพร่ |

```bash
# Summary: entity, rule, status
banshee pba lookup task:<ID> | jq '{entity: .panel_status.entity_name, rule: .panel_status.case_rule_label, status: .panel_status.status, priority: .panel_status.priority}'

# Extract evidence URLs (code_repo_leakage)
banshee pba lookup task:<ID> | jq '[.panel_evidence_summary.evidence[].url]'
```

---

### `banshee pba update [ALERT_IDS]...`

อัปเดต Playbook Alerts หนึ่งรายการหรือมากกว่า โดย ID รองรับ prefix `task:` หรือ UUID ที่ไม่มี prefix และสามารถรับข้อมูลจาก pipe ได้

| ตัวเลือก | ย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--status` | `-s` | สถานะใหม่: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `--reopen` | `-r` | กลยุทธ์การเปิดใหม่ (สำหรับ Dismissed/Resolved เท่านั้น): `Never`, `SignificantUpdates` |
| `--priority` | `-p` | ระดับความสำคัญใหม่: `Informational`, `Moderate`, `High` |
| `--comment TEXT` | `-t` | เพิ่มความคิดเห็น |
| `--assignee TEXT` | `-a` | มอบหมายใหม่ (รองรับ `uhash:3aXZxdkM12`) |

**การผสมผสานสถานะ/การเปิดใหม่ที่ถูกต้อง:** `Dismissed → Never`, `Resolved → Never`, `Resolved → SignificantUpdates`

```bash
# Single update
banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

# Multiple IDs
banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

# Pipe from search
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

# From file
banshee pba update -s Dismissed < alerts.txt
cat alerts.txt | banshee pba update -s Dismissed

# Full example
banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
```

**การตอบสนอง:** คืนค่าเป็นข้อความธรรมดา ไม่ใช่ JSON — หนึ่งบรรทัดต่อการแจ้งเตือนที่อัปเดต: `SUCCESS:\n<ALERT_ID>` ห้ามส่งต่อไปยัง `jq`

---

### `banshee pba export`

ดึงรายละเอียดการแจ้งเตือนฉบับสมบูรณ์สำหรับการแจ้งเตือนที่ได้จาก `pba search` และส่งออกเป็น JSON หรือ CSV โดยรับข้อมูลจาก **stdin เท่านั้น** — ให้ pipe JSON object จาก `banshee pba search` มาเป็นอินพุต และไม่มี positional argument

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--csv` | | JSON | ส่งออกเป็น CSV (ชุดคอลัมน์คงที่) แทน JSON (รายละเอียดการแจ้งเตือนฉบับสมบูรณ์) |

```bash
banshee pba search --created 1d -l 10 | banshee pba export > alerts.json
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export --csv > identity_alerts.csv
```

**อินพุต:** คาดหวัง JSON object ที่ส่งออกโดย `banshee pba search` ทาง stdin — การส่งออกจะอ่าน `.data[]` และต้องการ `playbook_alert_id` และ `category` ในแต่ละระเบียน (ซึ่งใช้ขับเคลื่อนการดึงข้อมูลเฉพาะหมวดหมู่) การเรียกใช้โดยไม่มีอินพุตจาก pipe (TTY) จะทำให้เกิดข้อผิดพลาด `BadParameter`

**รูปแบบการตอบสนอง (ค่าเริ่มต้น):** อาร์เรย์ JSON ของ Playbook Alert object ฉบับสมบูรณ์ — มีโครงสร้างต่อการแจ้งเตือนเดียวกันกับที่ `banshee pba lookup` คืนค่า (`playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`)

**รูปแบบการตอบสนอง (`--csv`):** CSV ที่มีแถวส่วนหัวและคอลัมน์คงที่เหล่านี้: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Subject`, `Assignee`, `Assessments`, `Entities`, `Reopen Strategy`, `Onwards Actions` โดย `Assessments` และ `Entities` เชื่อมด้วย `; ` และเครื่องหมายจุลภาคภายในค่าของฟิลด์จะถูกแทนที่ด้วยช่องว่าง