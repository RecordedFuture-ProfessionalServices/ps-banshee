# sandbox

> ดู [index.md](index.md) สำหรับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบผลลัพธ์ และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

คำสั่ง sandbox จำเป็นต้องมี `RF_SANDBOX_TOKEN` เพิ่มเติมจาก `RF_TOKEN` ตั้งค่า `RF_SANDBOX_CHOICE` (หรือ `--sandbox-choice` แบบ global) เพื่อกำหนดเป้าหมายไปยังภูมิภาคที่ต้องการ: `eu` (ค่าเริ่มต้น), `usa`, `apj`, `public` หรือ `private`

---

### `banshee sandbox stats`

รวบรวมข้อมูลการส่งตัวอย่างใน sandbox ในช่วงเวลาย้อนหลังที่กำหนดได้ และแสดงรายงานสรุปสำหรับ SOC ในตอนเช้า ได้แก่ ปริมาณการส่ง การกระจายคะแนน ตระกูลมัลแวร์ที่พบมากที่สุด การครอบคลุมของแพลตฟอร์ม C2 ที่ดึงออกมา และ network IOC (ตัวบ่งชี้ที่เป็นอันตรายในเครือข่าย) ที่ผ่านการตรวจสอบจาก SOAR

| ตัวเลือก | แบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--days INTEGER` | `-d` | `7` | ช่วงเวลาย้อนหลังเป็นวัน (ขั้นต่ำ 1) |
| `--subset` | `-s` | `org` | ขอบเขตตัวอย่าง: `owned`, `public`, `org` |
| `--pretty` | `-p` | | แสดงผลแบบอ่านง่ายด้วย Rich layout |

กลุ่มคะแนน (สเกล triage 1–10):

| กลุ่ม | ช่วงคะแนน | ความหมาย |
|--------|-------------|---------|
| `malicious` | 8–10 | มัลแวร์ที่รู้จัก ความเชื่อมั่นสูง |
| `suspicious` | 5–7 | มีพฤติกรรมบ่งชี้ที่ชัดเจน |
| `potentially_suspicious` | 3–4 | มีตัวบ่งชี้บางประการ |
| `clean` | 1–2 | ความเสี่ยงต่ำหรือไม่เป็นอันตราย |

```bash
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats -d 30 | jq '.by_score'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดียว:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.period_start` | จุดเริ่มต้นของช่วงการรวบรวมข้อมูล (ISO 8601) |
| `.period_end` | จุดสิ้นสุดของช่วงการรวบรวมข้อมูล (ISO 8601) |
| `.period_days` | ช่วงเวลาย้อนหลังเป็นวัน |
| `.subset` | ขอบเขตที่ใช้ (`owned`, `public`, `org`) |
| `.total` | จำนวนการส่งทั้งหมดในช่วงเวลา |
| `.pending` | การส่งที่อยู่ระหว่างการวิเคราะห์ |
| `.failed` | การส่งที่เกิดข้อผิดพลาด |
| `.by_kind` | Object ที่แมปประเภทการส่ง (`file`, `url` ฯลฯ) กับจำนวน |
| `.by_platform` | Object ที่แมปแท็กแพลตฟอร์มกับจำนวน |
| `.by_score` | Object ที่แมปชื่อกลุ่มคะแนนกับจำนวน |
| `.by_file_type` | Object ที่แมปนามสกุลไฟล์กับจำนวน |
| `.top_tags` | Object ที่มีคีย์ `malware_families`, `botnets`, `arch_file`, `behavioral_ttp` — แต่ละคีย์แมปชื่อแท็กกับจำนวน |
| `.top_iocs` | Object ที่มีคีย์ `extracted_c2`, `verified_network`, `malicious_sha256` — แต่ละคีย์เป็น array ของสตริง IOC |
| `.daily_by_family` | Object ที่แมปตระกูลมัลแวร์กับจำนวนรายวัน |
| `.trend_vs_prior_period` | Object ที่มี sub-object `total` และ `reported` ซึ่งแต่ละอันมี `current`, `prev` และ `pct_change` |
| `.soar_skipped` | `true` เมื่อการตรวจสอบ SOAR ถูกข้ามไป (`.top_iocs.verified_network` จะว่างเปล่า) |

---

### `banshee sandbox list`

แสดงรายการตัวอย่างใน sandbox — ของตนเอง ขององค์กร (ค่าเริ่มต้น) หรือฟีดสาธารณะ

| ตัวเลือก | แบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--subset` | `-s` | `org` | ขอบเขตตัวอย่าง: `owned`, `public`, `org` |
| `--limit INTEGER` | `-l` | `20` | จำนวนผลลัพธ์สูงสุด (1–4095) |
| `--pretty` | `-p` | | แสดงผลแบบตารางอ่านง่าย |

```bash
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array แบบ flat แต่ละรายการประกอบด้วย:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | ID ของตัวอย่าง (เช่น `260722-x8lgjahyvx`) |
| `.status` | สถานะการวิเคราะห์: `pending`, `running`, `reported`, `failed` |
| `.kind` | ประเภทการส่ง: `file`, `url`, `fetch`, `import` |
| `.filename` | ชื่อไฟล์ต้นฉบับ (อาจว่างเปล่าสำหรับการส่ง URL) |
| `.submitted` | เวลาที่ส่ง (ISO 8601) |
| `.completed` | เวลาที่เสร็จสิ้น (ISO 8601; ไม่มีค่าหากยังดำเนินการอยู่) |
| `.sha256` | SHA-256 ของไฟล์ที่ส่ง |
| `.user_id` | UUID ของผู้ใช้ที่ส่ง |

---

### `banshee sandbox search`

ค้นหาตัวอย่างที่ตรงกับตัวกรองแบบมีโครงสร้าง (hash, family, tag, botnet, wallet, IP, domain, URL, ช่วงวันที่ส่ง) หรือ Triage query แบบดิบ ต้องระบุตัวกรองอย่างน้อยหนึ่งรายการหรือ `--query`

| ตัวเลือก | แบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--hash TEXT` | | | กรองตาม file hash (MD5/SHA1/SHA256) |
| `--family TEXT` | | | กรองตามชื่อตระกูลมัลแวร์ |
| `--tag TEXT` | `-T` | | กรองตามแท็ก (ระบุซ้ำได้) |
| `--botnet TEXT` | | | กรองตามชื่อ botnet |
| `--wallet TEXT` | | | กรองตามที่อยู่ wallet |
| `--ip TEXT` | | | กรองตาม IP address |
| `--domain TEXT` | | | กรองตาม domain |
| `--url TEXT` | | | กรองตาม URL |
| `--from-date YYYY-MM-DD` | | | ส่งในหรือหลังวันที่นี้ |
| `--to-date YYYY-MM-DD` | | | ส่งในหรือก่อนวันที่นี้ |
| `--query TEXT` | `-q` | | Triage query string แบบดิบ (รวมกับตัวกรองแบบมีโครงสร้างด้วย AND) |
| `--limit INTEGER` | `-l` | `50` | จำนวนผลลัพธ์สูงสุด (1–200) |
| `--pretty` | `-p` | | แสดงผลแบบตารางอ่านง่าย |

```bash
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array — มีโครงสร้างเดียวกับรายการใน `sandbox list`

---

### `banshee sandbox get`

ดึงข้อมูลสรุปของตัวอย่าง sandbox รายการเดียวตาม ID ได้แก่ สถานะปัจจุบัน คะแนนรวม เป้าหมาย เวลาสร้างและเสร็จสิ้น SHA256 และรายละเอียดแต่ละ task รองรับทั้งตัวอย่างที่อยู่ระหว่างดำเนินการและที่เสร็จสิ้นแล้ว

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `SAMPLE_ID` (จำเป็น) | | ID ของตัวอย่าง sandbox |
| `--pretty` | `-p` | แสดงผลแบบอ่านง่ายด้วย Rich layout |

```bash
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดียว:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.sample` | ID ของตัวอย่าง |
| `.status` | สถานะการวิเคราะห์: `pending`, `running`, `static_analysis`, `reported`, `failed` |
| `.target` | เป้าหมายหลักของการจุดชนวน (ชื่อไฟล์หรือ URL) |
| `.score` | คะแนน triage รวม (1–10; `0` ขณะที่การวิเคราะห์กำลังดำเนินการ) |
| `.created` | เวลาที่ส่ง (ISO 8601) |
| `.completed` | เวลาที่เสร็จสิ้น (ISO 8601; ไม่มีค่าขณะยังดำเนินการอยู่) |
| `.sha256` | SHA-256 ของไฟล์ที่ส่ง (ไม่มีค่าสำหรับการส่ง URL) |
| `.owner` | ID ของผู้ใช้ที่ส่ง |
| `.tasks` | Object ที่แมป task ID → `{kind, status, score, tags, platform}` |

---

### `banshee sandbox download` *(เปลี่ยนแปลงข้อมูลบนดิสก์)*

ดาวน์โหลดไบต์ต้นฉบับของตัวอย่างที่ส่งสำหรับ ID ตัวอย่างหนึ่งรายการหรือมากกว่า ตัวอย่างแต่ละรายการจะถูกบรรจุในไฟล์ ZIP ที่เข้ารหัส AES ด้วยรหัสผ่าน `infected` เพื่อป้องกันการจุดชนวนโดยไม่ตั้งใจจากโปรแกรมป้องกันไวรัส secure email gateway หรือโปรแกรมจัดการไฟล์ แตกไฟล์ด้วย `7z x -pinfected <sample-id>.zip` — `unzip` มาตรฐานไม่รองรับ zip ที่เข้ารหัส AES อย่างเชื่อถือได้

ID ตัวอย่างสามารถส่งผ่านเป็นอาร์กิวเมนต์ positional หรือผ่าน stdin (คั่นด้วยช่องว่าง) จะแสดงการยืนยันก่อนดำเนินการ เว้นแต่จะระบุ `--yes` ไบต์จะอยู่ในหน่วยความจำของกระบวนการนี้ชั่วคราวระหว่างการดาวน์โหลดและการบีบอัด — การสแกนหน่วยความจำแบบรุนแรงของ EDR อาจยังตรวจพบได้ ควรรันบนเครื่องของนักวิเคราะห์ ไม่ใช่บนแล็ปท็อปส่วนตัวขององค์กรที่ใช้งานประจำ

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|-----------------|-------|---------|-------------|
| `SAMPLE_IDS` | | | ID ตัวอย่างหนึ่งรายการหรือมากกว่า (หรืออ่านจาก stdin) |
| `--output-dir PATH` | `-d` | (จำเป็น) | ไดเรกทอรีสำหรับบันทึกไฟล์ zip ที่เข้ารหัส (สร้างขึ้นหากยังไม่มี) |
| `--yes` | `-y` | | ข้ามการยืนยัน |
| `--workers INTEGER` | `-w` | `1` | จำนวน worker สำหรับดาวน์โหลดพร้อมกัน (1–16) |

```bash
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
```

**การตอบกลับ:** แสดงข้อความเตือนหนึ่งครั้งทาง stderr; แสดงบรรทัด `[<id>] Saved: <path> (<bytes> bytes, sha256=<hex>)` ทาง stderr สำหรับการดาวน์โหลดที่สำเร็จแต่ละรายการ; `[<id>] ERROR: <msg>` สำหรับกรณีที่ล้มเหลว การดำเนินการที่ล้มเหลวบางส่วนจะดำเนินต่อจนเสร็จสิ้นและออกด้วย exit code 1; การดำเนินการที่สำเร็จทั้งหมดออกด้วย exit code 0

เนื้อหาในไฟล์เก็บถาวร: รายการเดียวที่ชื่อ `<sample-id>` (ไม่มีการเดานามสกุลไฟล์) ซึ่งมีไบต์ดิบของตัวอย่าง

---

### `banshee sandbox delete` *(เปลี่ยนแปลงข้อมูล)*

ลบตัวอย่าง sandbox ตาม ID และลบ artifact ของ task ที่เกี่ยวข้องทั้งหมด จะแสดงการยืนยันก่อนดำเนินการ เว้นแต่จะระบุ `--yes`

| อาร์กิวเมนต์/ตัวเลือก | คำอธิบาย |
|-----------------|-------------|
| `SAMPLE_ID` (จำเป็น) | ID ของตัวอย่างที่ต้องการลบ |
| `--yes` / `-y` | ข้ามการยืนยัน |

```bash
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
```

**การตอบกลับ:** ไม่มีผลลัพธ์เมื่อสำเร็จ; ออกด้วย exit code 0

---

### `banshee sandbox submit` *(เปลี่ยนแปลงข้อมูล)*

ส่งตัวอย่างเพื่อวิเคราะห์ ไฟล์ในเครื่องจะถูกอัปโหลด URL จะถูกจุดชนวนในเบราว์เซอร์ (หรือดาวน์โหลดก่อนด้วย `--fetch`) และสามารถนำเข้าตัวอย่างสาธารณะตาม ID ด้วย `--import`

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `TARGET` (จำเป็น) | | เส้นทางไฟล์ URL หรือ ID ตัวอย่างสาธารณะ (ใช้ร่วมกับ `--import`) |
| `--fetch` | | ดาวน์โหลด URL ก่อน จากนั้นวิเคราะห์ไฟล์ ใช้ร่วมกับ `--import` ไม่ได้ |
| `--import` | | ถือว่าเป้าหมายเป็น ID ของตัวอย่างสาธารณะ ใช้ร่วมกับ `--fetch` ไม่ได้ |
| `--profile TEXT` | | ชื่อหรือ ID ของโปรไฟล์การวิเคราะห์ (ระบุซ้ำได้; ใช้ร่วมกับ `--interactive` ไม่ได้) |
| `--timeout INTEGER` | `-t` | ระยะเวลาหมดเวลาการวิเคราะห์เป็นวินาที (1–3600) |
| `--network` | `-N` | โหมดเครือข่าย: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | รหัสประเทศสำหรับ VPN exit; ต้องใช้ร่วมกับ `--network vpn` |
| `--tags TEXT` | `-T` | แท็กกำหนดเอง (ระบุซ้ำได้) |
| `--password TEXT` | | รหัสผ่านสำหรับไฟล์เก็บถาวรที่มีการป้องกัน |
| `--wait` | `-w` | รอจนการวิเคราะห์เสร็จสิ้น จากนั้นแสดงรายงานสรุป |
| `--interactive` | `-i` | หยุดชั่วคราวที่ static analysis เพื่อเลือกโปรไฟล์ผ่าน `set-profile`; ใช้ร่วมกับ `--profile` ไม่ได้ |
| `--pretty` | `-p` | แสดงผลแบบอ่านง่าย |

```bash
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
```

**รูปแบบการตอบกลับ (ค่าเริ่มต้น):** คืนค่าตัวอย่างที่ส่งเป็น JSON object โดยมีฟิลด์เดียวกับรายการใน `sandbox list` (`id`, `status`, `kind`, `filename`, `submitted`, `sha256`, `user_id`) ใช้ `.id` เพื่อติดตามหรือรายงานการส่ง

**รูปแบบการตอบกลับ (เมื่อใช้ `--wait`):** คืนค่ารายงานสรุป — มีโครงสร้างเดียวกับ `sandbox report overview`

---

### `banshee sandbox set-profile` *(เปลี่ยนแปลงข้อมูล)*

กำหนดโปรไฟล์การวิเคราะห์ให้กับตัวอย่างที่หยุดชั่วคราวที่ static analysis (ส่งด้วย `--interactive`) ใช้ `--auto` เพื่อให้ sandbox เลือกโดยอัตโนมัติ หรือ `--pick FILE:PROFILE` สำหรับการกำหนดด้วยตนเองแบบรายไฟล์

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `SAMPLE_ID` (จำเป็น) | | ID ของตัวอย่างที่หยุดชั่วคราวที่ static analysis |
| `--auto` | `-a` | เลือกโปรไฟล์โดยอัตโนมัติสำหรับทุกไฟล์ ใช้ร่วมกับ `--pick` ไม่ได้ |
| `--pick FILE:PROFILE` | | แมปไฟล์หนึ่งรายการกับโปรไฟล์หนึ่งรายการ (ระบุซ้ำได้) ใช้ร่วมกับ `--auto` ไม่ได้ |
| `--pretty` | `-p` | แสดงผลแบบอ่านง่าย |

```bash
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
```

---

### `banshee sandbox profile list`

แสดงรายการโปรไฟล์การวิเคราะห์ทั้งหมดที่มีอยู่ใน Recorded Future Sandbox

| ตัวเลือก | แบบย่อ | คำอธิบาย |
|--------|-------|-------------|
| `--pretty` | `-p` | แสดงผลแบบตารางอ่านง่าย |

```bash
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array แบบ flat แต่ละรายการประกอบด้วย:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.id` | UUID ของโปรไฟล์ |
| `.name` | ชื่อโปรไฟล์ |
| `.tags` | Array ของแท็ก OS/locale (เช่น `["os:windows10-2004-x64", "locale:en-us"]`) |
| `.network` | โหมดเครือข่าย (เช่น `"internet"`, `"tor"`, `"vpn"`) |
| `.geolocation` | Array ของรหัสประเทศสำหรับ VPN exit (ว่างเปล่าเมื่อไม่เกี่ยวข้อง) |
| `.timeout` | ระยะเวลาหมดเวลาการวิเคราะห์เป็นวินาที |
| `.options` | Object ที่มีฟิลด์เสริม เช่น `browser` |

---

### `banshee sandbox profile get`

ดึงข้อมูลโปรไฟล์การวิเคราะห์รายการเดียวตาม ID หรือชื่อ

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME` (จำเป็น) | | UUID หรือชื่อของโปรไฟล์ |
| `--pretty` | `-p` | แสดงผลแบบตารางอ่านง่าย |

```bash
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
```

**รูปแบบการตอบกลับ:** object ของโปรไฟล์รายการเดียว — มีฟิลด์เดียวกับรายการใน `sandbox profile list`

---

### `banshee sandbox profile create` *(เปลี่ยนแปลงข้อมูล)*

สร้างโปรไฟล์การวิเคราะห์ใหม่ ชื่อโปรไฟล์ต้องไม่ซ้ำกันภายในองค์กรของคุณ

| ตัวเลือก | แบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--name TEXT` | `-n` | (จำเป็น) | ชื่อโปรไฟล์ (ต้องไม่ซ้ำกัน) |
| `--tag TEXT` | `-T` | (จำเป็น) | แท็ก OS/locale (ระบุซ้ำได้) แท็ก locale ต้องจับคู่กับแท็ก OS อย่างน้อยหนึ่งรายการ |
| `--timeout INTEGER` | `-t` | `120` | ระยะเวลาหมดเวลาการวิเคราะห์เป็นวินาที (1–3600) |
| `--network` | `-N` | | โหมดเครือข่าย: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | | รหัสประเทศสำหรับ VPN exit; ต้องใช้ร่วมกับ `--network vpn` (ระบุซ้ำได้) |
| `--browser` | `-b` | | เบราว์เซอร์: `chrome`, `firefox`, `ie11`, `microsoft-edge` |
| `--pretty` | `-p` | | แสดงผลแบบตารางอ่านง่าย |

```bash
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
```

**รูปแบบการตอบกลับ:** คืนค่าโปรไฟล์ที่สร้างขึ้นเป็น JSON object — มีฟิลด์เดียวกับรายการใน `sandbox profile list`

---

### `banshee sandbox profile update` *(เปลี่ยนแปลงข้อมูล)*

อัปเดตโปรไฟล์การวิเคราะห์ที่มีอยู่ เฉพาะตัวเลือกที่ระบุเท่านั้นที่จะเปลี่ยนแปลง — ตัวเลือกที่ไม่ได้ระบุจะคงค่าเดิมไว้ ใช้ `--unset` เพื่อล้างค่า `network`, `browser` หรือ `geolocation`

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME` (จำเป็น) | | UUID หรือชื่อของโปรไฟล์ |
| `--name TEXT` | `-n` | ชื่อโปรไฟล์ใหม่ |
| `--tag TEXT` | `-T` | แท็ก OS/locale; แทนที่แท็กที่มีอยู่ทั้งหมด (ระบุซ้ำได้) |
| `--timeout INTEGER` | `-t` | ระยะเวลาหมดเวลาการวิเคราะห์เป็นวินาที (1–3600) |
| `--network` | `-N` | โหมดเครือข่าย: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | รหัสประเทศสำหรับ VPN exit; ต้องใช้ร่วมกับ `--network vpn` (ระบุซ้ำได้) |
| `--browser` | `-b` | เบราว์เซอร์: `chrome`, `firefox`, `ie11`, `microsoft-edge` |
| `--unset` | | ล้างค่าฟิลด์: `network`, `browser` หรือ `geolocation` (ระบุซ้ำได้) |
| `--pretty` | `-p` | แสดงข้อความสถานะแบบอ่านง่าย |

```bash
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
```

**รูปแบบการตอบกลับ:** คืนค่า `{"updated": true}` เมื่อโปรไฟล์มีอยู่และได้รับการอัปเดต หรือ `{"updated": false}` เมื่อไม่พบโปรไฟล์ ออกด้วย exit code 0 ในทั้งสองกรณี

---

### `banshee sandbox profile delete` *(เปลี่ยนแปลงข้อมูล)*

ลบโปรไฟล์การวิเคราะห์ตาม ID หรือชื่อ ปลอดภัยสำหรับการทำซ้ำ: การลบโปรไฟล์ที่ไม่มีอยู่แล้วจะแสดงคำเตือนและออกด้วย exit code 0

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `PROFILE_ID_OR_NAME` (จำเป็น) | | UUID หรือชื่อของโปรไฟล์ |
| `--yes` / `-y` | | ข้ามการยืนยัน |

```bash
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
```

**การตอบกลับ:** ไม่มีผลลัพธ์เมื่อสำเร็จ; ออกด้วย exit code 0

---

### `banshee sandbox report overview`

ดึงรายงานสรุปแบบครบถ้วนสำหรับตัวอย่าง sandbox ที่วิเคราะห์เสร็จแล้ว ได้แก่ คะแนนผลตัดสิน ตระกูลมัลแวร์ แท็ก hash ลายเซ็นการตรวจจับ การดึงค่าคอนฟิกมัลแวร์ network IOC และผลลัพธ์แต่ละ task ตัวอย่างต้องอยู่ในสถานะ `reported`

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `SAMPLE_ID` (จำเป็น) | | ID ของตัวอย่าง sandbox |
| `--wait` | `-w` | รอสูงสุด 30 นาทีจนรายงานพร้อม |
| `--pretty` | `-p` | แสดงผลสรุปแบบอ่านง่าย |

```bash
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดียว:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.version` | เวอร์ชันรูปแบบรายงาน |
| `.build` | ข้อมูล build ของ sandbox |
| `.analysis` | object ผลตัดสิน: คะแนน ตระกูลมัลแวร์ แท็ก |
| `.sample` | ข้อมูลเมตาของตัวอย่าง: id, kind, filename, sha256, submitted, completed |
| `.signatures` | ลายเซ็นการตรวจจับจากทุก task |
| `.targets` | Array ของ object เป้าหมายที่จุดชนวน แต่ละรายการมี `.iocs` (network IOC) และการดึงค่าคอนฟิกมัลแวร์ |
| `.tasks` | Array ของสรุปแต่ละ task: task ID, platform, status, คะแนนผลตัดสิน |

---

### `banshee sandbox report static`

ดึงรายงานการวิเคราะห์แบบ static (ก่อนการจุดชนวน) สำหรับตัวอย่าง sandbox ได้แก่ คะแนนผลตัดสิน แท็ก ไฟล์ที่แตกออกมา ลายเซ็นการตรวจจับแบบ static และการดึงค่าคอนฟิกมัลแวร์ พร้อมใช้งานทันทีที่ static analysis เสร็จสิ้น — ก่อนที่ task เชิงพฤติกรรมจะเสร็จสมบูรณ์

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `SAMPLE_ID` (จำเป็น) | | ID ของตัวอย่าง sandbox |
| `--wait` | `-w` | รอสูงสุด 10 นาทีจนรายงานพร้อม |
| `--pretty` | `-p` | แสดงผลสรุปแบบอ่านง่าย |

```bash
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON object เดียว:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.version` | เวอร์ชันรูปแบบรายงาน |
| `.build` | ข้อมูล build ของ sandbox |
| `.sample` | ข้อมูลเมตาของตัวอย่าง: id, kind, filename, sha256, submitted |
| `.task` | ข้อมูลเมตาของ static task |
| `.analysis` | object ผลตัดสิน: คะแนน แท็ก ลายเซ็น static |
| `.files` | Array ของไฟล์ที่แตกออกมา — แต่ละรายการมี `sha256`, `filename`, `size` และรายละเอียด static analysis |
| `.unpack_count` | จำนวนไฟล์ทั้งหมดที่แตกออกมาจากการส่ง |
| `.error_count` | จำนวนไฟล์ที่ไม่สามารถแตกออกได้ |

---

### `banshee sandbox report behavioral`

ดึงรายงานเชิงพฤติกรรม (หลังการจุดชนวน) สำหรับตัวอย่าง sandbox ที่วิเคราะห์เสร็จแล้ว โดยแสดงหนึ่ง object ต่อ behavioral task ที่เสร็จสมบูรณ์ Task ที่ยังไม่เสร็จจะถูกละเว้นจากผลลัพธ์และแจ้งทาง stderr; คำสั่งจะออกด้วย exit code ที่ไม่ใช่ศูนย์จนกว่าทุก task จะเสร็จสมบูรณ์ คืนค่า array ว่างพร้อม exit code 0 เมื่อตัวอย่างไม่มี behavioral task

บรรทัดคำสั่งของกระบวนการในมุมมอง `--pretty` จะถูกตัดทอนตามค่าเริ่มต้น — ส่งผ่าน `--full-cmd` หากต้องการข้อมูลแบบเต็ม (ค่าเหล่านี้นำมาจากตัวอย่างมัลแวร์โดยตรง ดังนั้นควรถือว่าเป็นข้อมูลที่ไม่น่าเชื่อถือ)

| อาร์กิวเมนต์/ตัวเลือก | แบบย่อ | คำอธิบาย |
|-----------------|-------|-------------|
| `SAMPLE_ID` (จำเป็น) | | ID ของตัวอย่าง sandbox |
| `--wait` | `-w` | รอสูงสุด 30 นาทีจนทุก task เสร็จสมบูรณ์ |
| `--full-cmd` | | แสดงบรรทัดคำสั่งของกระบวนการแบบเต็มโดยไม่ตัดทอน (ถือว่าเป็นข้อมูลที่ไม่น่าเชื่อถือ) |
| `--pretty` | `-p` | แสดงผลสรุปแบบอ่านง่ายต่อ task |

```bash
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
```

**รูปแบบการตอบกลับ:** คืนค่าเป็น JSON array แต่ละรายการสอดคล้องกับ behavioral task หนึ่งรายการ:

| ฟิลด์ | คำอธิบาย |
|-------|-------------|
| `.task_id` | ID ของ behavioral task |
| `.version` | เวอร์ชันรูปแบบรายงาน |
| `.build` | ข้อมูล build ของ sandbox |
| `.sample` | ข้อมูลเมตาของตัวอย่าง: id, kind, filename, sha256 |
| `.task` | ข้อมูลเมตาของ task: platform, status, started, completed |
| `.analysis` | object ผลตัดสิน: คะแนน ตระกูลมัลแวร์ แท็ก |
| `.tags` | Array ของแท็กเชิงพฤติกรรม (เช่น `discovery`, `execution`) |
| `.signatures` | Array ของลายเซ็นการตรวจจับที่ถูกเรียกใช้ |
| `.processes` | Array ของกระบวนการที่สังเกตพบ — แต่ละรายการมี `pid`, `name`, `cmd` (ตัดทอนเว้นแต่จะใช้ `--full-cmd`) และกระบวนการย่อย |
| `.network` | กิจกรรมเครือข่าย: `.flows` (บันทึกการเชื่อมต่อ), `.dns` (คำถาม DNS), `.http` (คำขอ HTTP) |
| `.dumped` | Array ของไฟล์ที่ dump/ดึงออกมาพร้อม SHA-256 hash |