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