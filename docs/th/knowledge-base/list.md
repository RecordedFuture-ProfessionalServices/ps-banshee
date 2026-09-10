# list

> ดูที่ [index.md](index.md) สำหรับข้อมูลเกี่ยวกับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบเอาต์พุต และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee list create NAME [LIST_TYPE]`

สร้างรายการใหม่

| อาร์กิวเมนต์/ตัวเลือก | ค่าเริ่มต้น | คำอธิบาย |
|-----------------|---------|-------------|
| `NAME` (จำเป็น) | | ชื่อของรายการ |
| `LIST_TYPE` | `entity` | ค่าใดค่าหนึ่งจาก: `entity`, `source`, `text` |
| `--pretty` / `-p` | | แสดงผลในรูปแบบที่อ่านง่าย |

```bash
banshee list create coolbeans
banshee list create coolsources source -p
```

---

### `banshee list search [NAME]`

ค้นหารายการตามชื่อและ/หรือประเภท

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `NAME` (ไม่บังคับ) | | | กรองตามชื่อรายการ |
| `--list-type` | `-t` | | ค่าใดค่าหนึ่งจาก: `entity`, `source`, `text`, `custom`, `ip`, `domain`, `tech_stack`, `industry`, `brand`, `partner`, `industry_peer`, `location`, `supplier`, `vulnerability`, `company`, `hash`, `operation`, `attacker`, `target`, `method`, `executive` |
| `--limit INTEGER` | `-l` | `1000` | จำนวนผลลัพธ์สูงสุด (1–3000) |
| `--pretty` | `-p` | | แสดงผลในรูปแบบที่อ่านง่าย |

```bash
banshee list search -l 1500 -p
banshee list search -t vulnerability
banshee list search Attacker
banshee list search ernest -t entity -p -l 3
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array แบบแบน แต่ละรายการมีฟิลด์ดังนี้:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | รหัสรายการ (เช่น `report:-19oM7`) |
| `.name` | ชื่อรายการ |
| `.type` | ประเภทรายการ: `entity`, `source`, `text` เป็นต้น |
| `.created` | เวลาที่สร้าง (ISO 8601) |
| `.updated` | เวลาที่อัปเดตล่าสุด (ISO 8601) |
| `.owner_id` | รหัส uhash ของเจ้าของ |
| `.owner_name` | ชื่อที่แสดงของเจ้าของ |
| `.owner_organisation_details` | ข้อมูลความเป็นเจ้าของขององค์กร |

---

### `banshee list info LIST_ID`

ดูข้อมูล metadata ของรายการ

```bash
banshee list info 1b0tFN
banshee list info 1b0tFN -p
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดี่ยว — มีชุดฟิลด์เดียวกับรายการใน `list search` ได้แก่: `id`, `name`, `type`, `created`, `updated`, `owner_id`, `owner_name`, `organisation_id`, `organisation_name`, `owner_organisation_details`

---

### `banshee list status LIST_ID`

ดูสถานะการประมวลผล/การซิงค์ของรายการ

```bash
banshee list status 1b0tFN
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดี่ยวที่มีสองฟิลด์:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.status` | สตริงสถานะการประมวลผล (เช่น `"ready"`) |
| `.size` | จำนวน entity ที่อยู่ในรายการในขณะนั้น |

---

### `banshee list entities LIST_ID`

ดึงข้อมูล entity ทั้งหมดที่อยู่ในรายการในขณะนั้น

```bash
banshee list entities 1b0s1q
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array แบบแบน แต่ละรายการมีฟิลด์ดังนี้:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.entity.id` | รหัส entity ของ RF |
| `.entity.name` | ชื่อที่แสดงของ entity |
| `.entity.type` | สตริงประเภท entity |
| `.status` | สถานะของ entity ในรายการ (เช่น `"ready"`) |
| `.added` | เวลาที่เพิ่ม entity (ISO 8601) |

```bash
# Extract all entity IDs on a list
banshee list entities report:6P8708 | jq -r '.[].entity.id'

# Get entity names and types
banshee list entities report:6P8708 | jq '[.[] | {name: .entity.name, type: .entity.type}]'
```

---

### `banshee list entries LIST_ID`

ดึงข้อมูลรายการ text match entries ในรายการ (สำหรับรายการประเภท `text`)

```bash
banshee list entries 1b0s1q
```

---

### `banshee list add LIST_ID ENTITY_ID [PROPERTIES]`

เพิ่ม entity เดี่ยวเข้าสู่รายการ

| อาร์กิวเมนต์ | คำอธิบาย |
|----------|-------------|
| `LIST_ID` (จำเป็น) | รหัสรายการ |
| `ENTITY_ID` (จำเป็น) | รหัส entity ของ RF (เช่น `SoA6SP`) หรือคู่ `name,type` (เช่น `wannacry,Malware`) |
| `PROPERTIES` (ไม่บังคับ) | ใช้ `annotation=<text>` เพื่อแนบหมายเหตุที่จะแสดงบนแพลตฟอร์ม Recorded Future สำหรับ entity นี้ หากค่ามีช่องว่างให้ใส่เครื่องหมายคำพูดครอบ |

```bash
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
```

---

### `banshee list bulk-add LIST_ID [ENTITY_INPUT]...`

เพิ่ม entity หลายรายการเข้าสู่รายการ รับรหัส entity, คู่ `name,type` หรือคู่ `type:value` ได้

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | ปิด | โหมดเขียนทับ: คง entity ที่มีอยู่ในข้อมูลที่ส่งมา เพิ่ม entity ใหม่ และลบ entity ที่อยู่ในรายการในขณะนั้นซึ่ง**ไม่**ปรากฏในข้อมูลที่ส่งมา หากไม่ใช้ตัวเลือกนี้ คำสั่งจะเพิ่มเฉพาะ entity ใหม่และจะไม่ลบ entity ที่มีอยู่เดิม |

**รูปแบบข้อมูลอินพุต:**
- รหัส entity ของ RF: `SoA6SP`
- ชื่อ + ประเภท: `wannacry,Malware` หรือ `www.duckdns.org,InternetDomainName`
- ค่าที่นำหน้าด้วยประเภท: `ip:8.8.8.8`

```bash
banshee list bulk-add report:21YKUC SoA6SP lYNvCK
banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# Overwrite mode: make the list match exactly the entities supplied (adds missing, removes stale)
banshee list bulk-add 21YKUC SoA6SP lYNvCK --overwrite

# From file (one entity per line)
banshee list bulk-add 21YKUC < entities.txt
cat entities.txt | banshee list bulk-add 21YKUC
```

**การตอบกลับ:** ข้อความธรรมดาจัดกลุ่มตามผลลัพธ์ — บล็อก `ADDED:`, `REMOVED:` (เฉพาะโหมด overwrite) และ `UNCHANGED:` ที่แสดงรายการ entity ที่ได้รับผลกระทบ ไม่ใช่ JSON จึงไม่ควรส่งต่อไปยัง `jq`

---

### `banshee list remove LIST_ID ENTITY_ID`

ลบ entity เดี่ยวออกจากรายการ

```bash
banshee list remove 1b0s1q lYNvCK
```

---

### `banshee list bulk-remove LIST_ID [ENTITY_INPUT]...`

ลบ entity หลายรายการออกจากรายการ รับรูปแบบข้อมูลอินพุตเดียวกับ `bulk-add`

```bash
banshee list bulk-remove 21YKUC JLHNoH lYNvCK
banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# From file
banshee list bulk-remove 21YKUC < entities.txt
cat entities.txt | banshee list bulk-remove 21YKUC
```

---

### `banshee list copy SOURCE_LIST_ID DESTINATION_LIST_ID`

คัดลอก entity จากรายการหนึ่งไปยังอีกรายการหนึ่ง โดยจะอ่าน entity จากรายการต้นทางแล้วเพิ่มเข้าสู่รายการปลายทาง

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | ปิด | โหมดเขียนทับ: คง entity ที่มีอยู่ในทั้งสองรายการ เพิ่ม entity ใหม่ และลบ entity ในรายการปลายทางที่**ไม่**มีในรายการต้นทาง หากไม่ใช้ตัวเลือกนี้ entity จะถูกเพิ่มต่อท้ายรายการปลายทางเท่านั้นและจะไม่มีการลบข้อมูลใด |

หากรายการต้นทางว่างเปล่า คำสั่งจะออกโดยไม่แก้ไขรายการปลายทาง แม้จะใช้ `--overwrite` ก็ตาม

```bash
banshee list copy 1b0s1q 21YKUC

# Make the destination mirror the source exactly (adds missing, removes stale)
banshee list copy 1b0s1q 21YKUC --overwrite
```

**การตอบกลับ:** ข้อความธรรมดาจัดกลุ่มตามผลลัพธ์ — บล็อก `ADDED:`, `REMOVED:` (เฉพาะโหมด overwrite) และ `UNCHANGED:` ที่แสดงรายการ entity ที่ได้รับผลกระทบ ไม่ใช่ JSON จึงไม่ควรส่งต่อไปยัง `jq`

---

### `banshee list clear LIST_ID`

ลบ entity **ทั้งหมด** ออกจากรายการ (เป็นการดำเนินการที่ไม่สามารถกู้คืนได้ — ใช้ด้วยความระมัดระวัง) รายการ text match entries ไม่สามารถลบผ่าน API ได้ ตัวรายการเองจะไม่ถูกลบ มีเพียง entity เท่านั้นที่ถูกลบออก

```bash
banshee list clear 1b0s1q
```

**การตอบกลับ:** ข้อความธรรมดา แสดง `No entities to remove` เมื่อรายการว่างเปล่าอยู่แล้ว แสดง `Successfully removed <N> entities` เมื่อสำเร็จ หรือ — หากการลบบางรายการล้มเหลว — แสดง `<N> entities were not removed from the list:` ตามด้วยรายการ entity ที่ยังคงอยู่ ไม่ใช่ JSON