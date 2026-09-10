# rules

> ดู [index.md](index.md) สำหรับข้อมูลเกี่ยวกับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบผลลัพธ์ และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee rules search`

ค้นหาและดาวน์โหลดกฎการตรวจจับ Sigma, YARA และ Snort จาก Recorded Future

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--type` | `-t` | | ประเภทกฎ (ระบุได้หลายครั้ง, ตรรกะ OR): `sigma`, `yara`, `snort` |
| `--threat-actor-map` | `-T` | | กรองตาม actor ใน Threat Actor Map ของคุณ |
| `--threat-actor-category` | `-C` | | กรองตามหมวดหมู่ threat actor (ระบุได้หลายครั้ง, ตรรกะ OR) หมวดหมู่ประกอบด้วย กลุ่มที่ได้รับการสนับสนุนจากรัฐ กลุ่ม ransomware กลุ่ม hacktivist ผู้กระทำที่มีแรงจูงใจทางการเงิน และอื่นๆ |
| `--threat-malware-map` | `-M` | | กรองตาม malware ใน Malware Threat Map ของคุณ |
| `--org-id TEXT` | `-O` | | Organization ID สำหรับบัญชี MSSP/multi-org (สำหรับใช้กับ threat map) |
| `--entity TEXT` | `-e` | | กรองตาม RF entity ID (ระบุได้หลายครั้ง, ตรรกะ OR) ใช้ `banshee entity search` เพื่อค้นหา ID รองรับรหัส MITRE (เช่น `mitre:T1486`) |
| `--created-after TEXT` | `-a` | | แบบสัมพัทธ์ (`1d`, `7d`) หรือแบบสัมบูรณ์ (`2024-01-01`) |
| `--created-before TEXT` | `-b` | | วันที่แบบสัมพัทธ์หรือสัมบูรณ์ |
| `--updated-after TEXT` | `-u` | | วันที่แบบสัมพัทธ์หรือสัมบูรณ์ |
| `--updated-before TEXT` | `-U` | | วันที่แบบสัมพัทธ์หรือสัมบูรณ์ |
| `--id TEXT` | `-i` | | กรองตาม document ID ของ Insikt Note (เช่น `doc:lmRPGB`) |
| `--title TEXT` | `-n` | | ค้นหาข้อความอิสระในชื่อ Insikt Note ที่เกี่ยวข้อง |
| `--limit INTEGER` | `-l` | `10` | จำนวนผลลัพธ์สูงสุด (1–1000) |
| `--output-path TEXT` | `-o` | | บันทึกกฎลงในไดเรกทอรี (หากไม่ระบุจะแสดงผลในคอนโซล) |
| `--pretty` | `-p` | | แสดงผลแบบจัดรูปแบบ (pretty print) |

```bash
banshee rules search -t yara -t snort -l 20 -a 3d
banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE
banshee rules search --id doc:0uTafk
banshee rules search --title Ransomware -p
banshee rules search -t yara --output-path .
banshee rules search --threat-actor-map -o fetched_rules
```

**รูปแบบการตอบสนอง:** คืนค่าเป็น JSON array แบบเรียบ (เมื่อไม่ได้ใช้ `--output-path`) แต่ละรายการแทนค่า Insikt Note พร้อมกฎการตรวจจับที่เกี่ยวข้อง:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | document ID ของ Insikt Note (เช่น `doc:o6_lui`) |
| `.type` | ประเภทกฎ: `sigma`, `yara` หรือ `snort` |
| `.title` | ชื่อ Insikt Note |
| `.description` | ข้อความคำอธิบายฉบับเต็มของ Insikt Note |
| `.created` | timestamp การสร้าง Note (ISO 8601) |
| `.updated` | timestamp การอัปเดตล่าสุดของ Note (ISO 8601) |
| `.rules[]` | อาร์เรย์ของออบเจกต์กฎ — หนึ่ง Note อาจมีหลายกฎ |

ฟิลด์ของรายการใน `.rules[]`:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.content` | ข้อความกฎดิบ (YAML สำหรับ Sigma, ข้อความธรรมดาสำหรับ YARA/Snort) |
| `.file_name` | ชื่อไฟล์ที่แนะนำสำหรับการบันทึกกฎ |
| `.entities[]` | entity ที่กฎอ้างอิง: `{id, name, type}` (อาจมี `display_name`) |

```bash
# List all sigma rule titles and filenames from the last 7 days
banshee rules search -t sigma -l 50 -a 7d | jq '[.[] | {title, file: .rules[0].file_name}]'

# Extract all MITRE ATT&CK IDs referenced by rules
banshee rules search -t sigma -l 20 | jq '[.[].rules[].entities[] | select(.type == "MitreAttackIdentifier") | .name] | unique'

# Print raw Sigma rule content
banshee rules search --id doc:0uTafk | jq -r '.[0].rules[0].content'
```