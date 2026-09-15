# Banshee CLI Knowledge Base

> CLI ของ Recorded Future สำหรับการสืบสวนภัยคุกคามทางไซเบอร์ผ่านเทอร์มินัล
> พัฒนาโดย Cyber Security Engineers ของ Recorded Future
> ผ่านการตรวจสอบกับ `ps-banshee` / `banshee` เวอร์ชัน 1.5.0

Knowledge Base นี้ออกแบบมาเพื่อใช้งานร่วมกับ LLM (Claude Code, Opus และ agentic CLI อื่น ๆ) โดยมีเอกสาร 3 รูปแบบสำหรับ agent:

- **Index** — สารบัญแบบย่อ: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt>
- **Full bundle** — ทุก command group รวมไว้ในเอกสารเดียว: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>
- **Per-group pages** — สำหรับการดึงข้อมูลเฉพาะกลุ่ม ให้บริการในรูป raw markdown ที่ `https://.../latest/knowledge-base/<group>/index.md` (เช่น `ca`, `ioc`, `list`) ซึ่งลิงก์ไว้ใน index ด้านบน

เพื่อให้ agent ในโปรเจกต์ค้นพบ `banshee` ได้ ให้เพิ่มบรรทัดที่อธิบายการดำเนินการลงใน `CLAUDE.md`, `AGENTS.md` หรือไฟล์กฎที่เทียบเท่า:

> เมื่อทำงานกับ Recorded Future ให้ดึงข้อมูลจาก <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt> เพื่อรับเอกสารอ้างอิง `banshee` CLI แบบสมบูรณ์ แล้วใช้งาน `banshee` CLI หากไม่สามารถเข้าถึง URL ดังกล่าวได้ ให้รัน `banshee --help` แทน

กำหนดค่า `RF_TOKEN` ในสภาพแวดล้อม shell ก่อนเรียกใช้งาน — ดูรายละเอียดที่ [Authentication](#authentication-global-options) ด้านล่าง

---

## Authentication & Global Options

```
banshee [OPTIONS] COMMAND [ARGS]...
```

| Flag | Short | คำอธิบาย |
|------|-------|-------------|
| `--api-key TEXT` | `-k` | API key ของ Recorded Future แนะนำให้ตั้งค่า env var `RF_TOKEN` แทน |
| `--no-ssl-verify` | `-s` | ปิดการตรวจสอบ SSL (ใช้กับ proxy ผ่าน `HTTP_PROXY` / `HTTPS_PROXY`) |
| `--debug` | | เปิดใช้งานโหมด debug |
| `--version` | | แสดงเวอร์ชัน |
| `--install-completion` | | ติดตั้ง shell tab completion |
| `--show-completion` | | แสดงการตั้งค่า completion สำหรับการติดตั้งแบบ manual |

**แนวทางปฏิบัติที่ดี:** Export `RF_TOKEN=<your_api_key>` เพื่อไม่ต้องระบุ `-k` ในทุกการเรียกใช้งาน

---

## การตรวจสอบความพร้อม

ก่อนรันขั้นตอนการทำงาน ให้ตรวจสอบ toolchain ในเครื่องและเส้นทางการยืนยันตัวตน

```bash
# CLI ติดตั้งแล้วและสามารถเข้าถึงได้
banshee --version
banshee --help

# ตรวจสอบว่ามี API token ของ Recorded Future
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# jq จำเป็นสำหรับตัวอย่าง pipeline ส่วนใหญ่
jq --version

# ทดสอบ API แบบอ่านอย่างเดียว
banshee entity search wannacry -l 1
banshee ioc bulk-lookup ip 8.8.8.8 | jq '.[0] | {ioc: .entity.name, score: .risk.score}'

# จำเป็นเฉพาะสำหรับขั้นตอน pcap เท่านั้น หากไม่มี tshark แม้แต่ `banshee pcap enrich --help` อาจล้มเหลว
command -v tshark
```

หาก `banshee` ไม่มีอยู่ ให้ติดตั้ง Python package `ps-banshee` ผ่านขั้นตอนการติดตั้ง Python package ที่ได้รับอนุมัติ แล้วรันการตรวจสอบข้างต้นอีกครั้ง

---

## สถานะการตรวจสอบล่าสุด

การตรวจสอบล่าสุด: **2026-07-23** (รีเฟรชเวอร์ชัน 1.5.0) กับ `ps-banshee` / `banshee` **1.5.0** โดยใช้การยืนยันตัวตนด้วย `RF_TOKEN` และ `RF_SANDBOX_TOKEN`

ผ่านการตรวจสอบสำเร็จ:

```bash
# ตรวจสอบ toolchain ในเครื่องและการมีอยู่ของ auth
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"
test -n "$RF_SANDBOX_TOKEN" && echo "RF_SANDBOX_TOKEN set"

# การเข้าถึง API แบบอ่านอย่างเดียว
banshee ca rules
banshee ca rules leaked
banshee ca search -t 7d
banshee ca search -t 12h | banshee ca export
banshee ca search -t 12h | banshee ca export --csv
banshee pba search -C 60d -l 3
banshee pba search -o uhash:69sKLfTGsS -C 60d -l 3
banshee pba search -C 60d -l 3 | banshee pba export
banshee pba search -C 60d -l 3 | banshee pba export --csv
banshee ioc bulk-lookup ip 8.8.8.8

# การเข้าถึง API ของ sandbox แบบอ่านอย่างเดียว
banshee sandbox stats --days 7
banshee sandbox list --limit 3
banshee sandbox profile list
banshee sandbox report overview 260722-x8lgjahyvx
banshee sandbox report static 260722-x8lgjahyvx
banshee sandbox report behavioral 260722-x8lgjahyvx
```

ข้อสังเกตที่พบ:

- `ca export` และ `pba export` อ่านข้อมูลจาก stdin **เท่านั้น** และไม่รับ positional argument ใด ๆ ให้ pipe `banshee ca search` / `banshee pba search` เข้าหา command เหล่านี้
- `pba export` รับ JSON object แบบสมบูรณ์จาก `pba search` (อ่านจาก `.data[]`) ในขณะที่ `ca export` รับ JSON array จาก `ca search`
- ใน `ca export --csv` คอลัมน์ `Updated` จะว่างเปล่าเสมอในขณะนี้ (สงวนไว้สำหรับการรองรับ API ในอนาคต) — ยืนยันในการรันครั้งนี้
- filter ใหม่ `pba search --org-id` (`-o`) รับ ID 10 ตัวอักษร หรือรูปแบบ `uhash:` 16 ตัวอักษร และสามารถระบุซ้ำได้
- `pcap enrich` ไม่ได้รับการทดสอบกับระบบจริง เนื่องจากไม่ได้ติดตั้ง `tshark` ซึ่งเป็นเรื่องปกติ: `banshee pcap enrich --help` จะเกิดข้อผิดพลาด `RuntimeError: tshark is not installed or not in PATH`
- `sandbox stats` มีฟิลด์ `soar_skipped` หากเป็น `true` แสดงว่า `.top_iocs.verified_network` จะว่างเปล่า (SOAR validation ไม่ได้ทำงานในช่วงเวลาดังกล่าว)
- คำสั่งที่แก้ไขข้อมูลของ sandbox (`submit`, `delete`, `set-profile`, `download`, `profile create/update/delete`) ไม่ได้รับการทดสอบกับระบบจริงในการรีเฟรชครั้งนี้
- `sandbox download` สร้างไฟล์ ZIP ที่เข้ารหัสด้วย AES (รหัสผ่าน `infected`) ให้แตกไฟล์ด้วย `7z x -pinfected <file>.zip` — `unzip` มาตรฐานไม่รองรับ AES zip อย่างน่าเชื่อถือ

---

## รูปแบบ Output

- ทุกคำสั่งจะ output เป็น **JSON** ไปยัง stdout โดยค่าเริ่มต้น — ออกแบบมาให้ใช้งานร่วมกับ pipe ได้
- เพิ่ม `--pretty` / `-p` ในคำสั่งใดก็ได้เพื่อแสดงผลในรูปแบบที่อ่านง่าย
- คำสั่งส่วนใหญ่รองรับการรับข้อมูลจาก stdin (ID/IOC ที่คั่นด้วยบรรทัดใหม่หรือช่องว่าง)
- ใช้ร่วมกับ `jq` เพื่อการกรองขั้นสูง (มีตัวอย่างตลอดทั้งเอกสาร)
- รูปแบบ response แตกต่างกันตาม endpoint โดยมีรูปแบบที่น่าสังเกตดังนี้:
  - `ioc lookup` คืนค่าเป็น JSON array และใช้ `.risk.evidenceDetails[]` สำหรับหลักฐานความเสี่ยงโดยละเอียด
  - `ioc bulk-lookup` คืนค่าเป็น JSON array และใช้ `.risk.rule.evidence[]` สำหรับหลักฐานความเสี่ยงแบบ bulk
  - `ioc search` คืนค่าเป็น object โดยมีผลลัพธ์อยู่ภายใต้ `.data.results[]`
  - `pba search` คืนค่าเป็น object โดยมี alert record อยู่ภายใต้ `.data[]`
  - `pcap enrich` และ `email enrich` คืนค่าเป็น record แบบ flat เช่น `.ioc`, `.risk_score` และ `.rule_evidence[]`

---

## Command Groups

| Group | หน้า | คำอธิบาย |
|-------|------|-------------|
| `ca` | [ca.md](ca.md) | Classic Alerts — ค้นหา, ดูรายละเอียด, อัปเดต, ส่งออก |
| `email` | [email.md](email.md) | เพิ่มความสมบูรณ์ให้ไฟล์ EML ด้วย RF intelligence |
| `entity` | [entity.md](entity.md) | ค้นหาและดูรายละเอียด entity |
| `ioc` | [ioc.md](ioc.md) | การเพิ่มความสมบูรณ์ IOC, bulk enrichment, ค้นหา, กฎ |
| `list` | [list.md](list.md) | จัดการ RF Lists & Watch Lists (สร้าง, เพิ่ม/ลบ entity, รายการ) |
| `pcap` | [pcap.md](pcap.md) | เพิ่มความสมบูรณ์ให้ packet capture ด้วย RF intelligence |
| `pba` | [pba.md](pba.md) | Playbook Alerts — ค้นหา, ดูรายละเอียด, อัปเดต, ส่งออก |
| `risklist` | [risklist.md](risklist.md) | ดึงข้อมูล สร้าง และตรวจสอบ risk list |
| `rules` | [rules.md](rules.md) | ค้นหาและดาวน์โหลด detection rule (Sigma, YARA, Snort) |
| `sandbox` | [sandbox.md](sandbox.md) | ส่งไฟล์และ URL เพื่อวิเคราะห์ใน sandbox ดึงรายงาน จัดการ profile และดาวน์โหลด sample |

---

## หมายเหตุสำหรับ LLM

- **ID ทั้งหมดเป็น string สั้นที่ไม่โปร่งใส** (เช่น `tybakN`, `1b0s1q`) — ห้ามเดา ให้ดึงข้อมูลผ่านการค้นหาเสมอ
- **PBA alert ID** ใช้รูปแบบ UUID และถูกส่งคืนพร้อม prefix `task:` แล้วโดย `pba search` (`.data[].playbook_alert_id`) ให้ส่งผ่านตามที่ได้รับไปยัง `pba lookup` และ `pba update` — ห้ามเพิ่ม `task:` เข้าไปอีก
- **`ca update` และ `pba update` คืนค่าเป็น plain text** ไม่ใช่ JSON — `SUCCESS:\n<ALERT_ID>` ต่อ alert ที่อัปเดต ห้าม pipe ไปยัง `jq`
- **การ pipe ผ่าน stdin** สม่ำเสมอในทุกคำสั่ง bulk/update: pipe ID หรือ IOC ที่คั่นด้วยบรรทัดใหม่โดยตรง
- **`--pretty` ไม่ใช่ JSON** — เป็นรูปแบบที่อ่านง่ายและไม่เหมาะสำหรับการประมวลผลต่อด้วย `jq` ห้ามใช้ใน pipeline
- **Risk rule** (ใช้ใน `ioc rules`, `risklist fetch`, `risklist create`) เป็น string ที่มีชื่อ เช่น `recentValidatedCnc`, `analystNote`, `recentPhishing` ค้นพบชื่อ rule ที่ใช้ได้ด้วย `banshee ioc rules <entity_type>`
- **Entity ID กับคู่ name,type**: `list bulk-add` / `list bulk-remove` รับทั้งสองรูปแบบ — ใช้ `SoA6SP` (RF ID) หรือ `wannacry,Malware` (ชื่อ + ประเภท) หรือ `ip:8.8.8.8` (ค่าที่มี type นำหน้า)
- **`risklist create --fusion`** อัปโหลดผลลัพธ์ไปยัง RF Fusion โดยตรง และ `--output-path` จะถูกตีความเป็น Fusion destination path ไม่ใช่ local path
- **หลักฐานของ `ioc lookup` กับ `ioc bulk-lookup` ต่างกัน**: `ioc lookup` ใช้ `.risk.evidenceDetails[]` และ `ioc bulk-lookup` ใช้ `.risk.rule.evidence[]` ซึ่งไม่สามารถใช้แทนกันได้