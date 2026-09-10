# risklist

> ดู [index.md](index.md) สำหรับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบผลลัพธ์ และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee risklist fetch`

ดาวน์โหลด risk list จาก RF หรือโหลดไฟล์กำหนดเองในเครื่อง

| ตัวเลือก | ย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--entity-type` | `-e` | ประเภทของ entity: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--list-name TEXT` | `-l` | `default`, `large`, หรือชื่อ rule ใดก็ได้จาก `banshee ioc rules` |
| `--custom-list-path TEXT` | `-c` | พาธไปยังไฟล์ risk list ในเครื่อง |
| `--output-path TEXT` | `-o` | พาธสำหรับผลลัพธ์ (ค่าเริ่มต้นคือ CWD พร้อมชื่อที่สร้างโดยอัตโนมัติ) |
| `--as-json` | `-j` | แปลงรายการที่ดาวน์โหลดเป็น JSON (ใช้ได้เฉพาะกับ `--list-name` + `--entity-type`) |

```bash
banshee risklist fetch -e domain -l default
banshee risklist fetch -c /custom/path/to/list.csv
banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv
```

---

### `banshee risklist create`

สร้าง risk list แบบผสมจาก risk rule ตั้งแต่หนึ่งรายการขึ้นไป พร้อมตัวกรองคะแนนแบบเลือกได้ สามารถบันทึกในเครื่องหรืออัปโหลดไปยัง RF Fusion ได้

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--entity-type` | `-e` | | ประเภทของ entity: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--risk-rule TEXT` | `-R` | | risk rule ที่จะรวมไว้ (ระบุซ้ำได้): `default`, `large`, หรือชื่อ rule ใดก็ได้จาก `banshee ioc rules` |
| `--risk-score INTEGER` | `-r` | | เกณฑ์คะแนน risk ขั้นต่ำ (5–99) |
| `--format` | `-f` | `csv` | รูปแบบผลลัพธ์: `csv`, `edl`, `json` |
| `--output-path TEXT` | `-o` | CWD | พาธของไฟล์ผลลัพธ์ |
| `--fusion` | `-F` | | อัปโหลดไปยัง RF Fusion (ใช้ร่วมกับ `--output-path` เป็นพาธปลายทางใน Fusion) |

**รูปแบบผลลัพธ์:**
- `csv` — คั่นด้วยเครื่องหมายจุลภาคพร้อมส่วนหัว: `Name, Risk, RiskString, EvidenceDetails`
- `edl` — รายการ IOC (Indicators of Compromise) แบบธรรมดา หนึ่งรายการต่อบรรทัด (สำหรับ feed ของ firewall/EDL)
- `json` — อาร์เรย์ JSON แบบเต็มของรายการใน risk list

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

---

### `banshee risklist stat`

แสดงเมทาดาทาของ risk list — ไม่ว่าจะมีอยู่ใน Fusion หรือไม่ และค่า etag ปัจจุบัน

| ตัวเลือก | ย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--entity-type` | `-e` | ประเภทของ entity |
| `--list-name TEXT` | `-l` | ชื่อของรายการ |
| `--custom-list-path TEXT` | `-c` | พาธไปยังไฟล์ risk list ในเครื่อง |
| `--pretty` | `-p` | จัดรูปแบบผลลัพธ์ให้อ่านง่าย |
| `--count` | `-C` | แสดงจำนวน IOC และการกระจายคะแนน risk ใน risk list |

```bash
banshee risklist stat -e ip -l recentValidatedCnc
banshee risklist stat -e domain -l domain_risklist
banshee risklist stat -e ip -l default --count
```

**รูปแบบของ Response:** คืนค่าเป็น JSON object เดียว:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.name` | ชื่อ risk list ตามที่จัดเก็บใน Fusion (เช่น `"recentValidatedCnc_ip_risklist"`) |
| `.exists` | `true`/`false` — ระบุว่ารายการมีอยู่ใน RF Fusion หรือไม่ |
| `.etag` | สตริง etag hash สำหรับการตรวจสอบ cache |
| `.counts` | *(เฉพาะเมื่อใช้ `--count`)* Object ที่แมปคะแนน risk แต่ละค่ากับจำนวน IOC เช่น `{"28": 261110, "65": 6531}` |

**หมายเหตุการทดสอบจริง:** ระหว่างการทดสอบเมื่อวันที่ 2026-05-01 การใช้ `--custom-list-path /tmp/banshee_smoke_risklist.json` ได้พยายามเรียก Fusion API และได้รับการตอบกลับ `400 Bad Request` ดังนั้นควรใช้ `-e`/`-l` แทน เว้นแต่จะต้องการตรวจสอบ custom path ที่รองรับโดย Fusion โดยตรง