# ประวัติการเผยแพร่

## 1.6.0 - 2026-09-15
### เพิ่มใหม่
- คำสั่งย่อย ['email extract-attachments`](reference/commands.md#banshee-email-extract-attachments) ใหม่สำหรับแยกไฟล์แนบจากไฟล์ EML, บันทึกลงในไฟล์เก็บถาวรที่ป้องกันด้วยรหัสผ่าน จากนั้นส่งไปยัง Recorded Future Sandbox เพื่อวิเคราะห์

## 1.5.0 - 2026-08-21

### เพิ่มใหม่
- คำสั่ง [`sandbox`](reference/commands.md#banshee-sandbox) ใหม่สำหรับโต้ตอบกับ Recorded Future sandbox


## v.1.4.1 - 2026-07-13

### เปลี่ยนแปลง
- อัปเดต dependencies ของ `psengine`


## v.1.4.0 - 2026-07-13

### เพิ่มใหม่
- ตัวเลือก [`-C`/`--count`](reference/commands.md#banshee-risklist-stat--count) ใหม่สำหรับ [`risklist stat`](reference/commands.md#banshee-risklist-stat) เพื่อดาวน์โหลด risk list และแสดงตารางจำนวน indicator ตาม risk score

## v1.3.1 - 2026-06-30

### เปลี่ยนแปลง
- อัปเดต dependencies

## 1.3.0 - 2026-06-15

### เพิ่มใหม่
- คำสั่งย่อย [`email enrich`](reference/commands.md#banshee-email-enrich) ใหม่สำหรับ enrich ไฟล์ EML โดยการดึง IP จาก header และ URL จาก body จากนั้นส่งคืนข่าวกรองจาก Recorded Future ซึ่งรวมถึง risk score, ความเชื่อมโยงกับ threat actor, ลิงก์มัลแวร์ และหลักฐาน risk rule
- คำสั่งย่อย [`ca export`](reference/commands.md#banshee-ca-export) ใหม่สำหรับส่งออก Classic Alerts เป็น JSON แบบเต็มหรือ CSV สรุป โดยอ่าน alert ID ที่ pipe มาจาก [`ca search`](reference/commands.md#banshee-ca-search)
- คำสั่งย่อย [`pba export`](reference/commands.md#banshee-pba-export) ใหม่สำหรับส่งออก Playbook Alerts เป็น JSON แบบเต็มหรือ CSV สรุป โดยอ่านผลการค้นหาที่ pipe มาจาก [`pba search`](reference/commands.md#banshee-pba-search)
- ตัวเลือก [`-o`/`--org-id`](reference/commands.md#banshee-pba-search--org-id) ใหม่สำหรับ [`pba search`](reference/commands.md#banshee-pba-search) เพื่อกรอง Playbook Alerts ตาม ID ขององค์กรที่เป็นเจ้าของ (สามารถระบุซ้ำได้)
- ตัวเลือก [`-o`/`--overwrite`](reference/commands.md#banshee-list-bulk-add--overwrite) ใหม่สำหรับ [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) เพื่อให้รายการตรงกับ entity ที่ระบุอย่างแน่นอน — โดยเพิ่ม entity ใหม่และลบ entity ที่มีอยู่ในรายการแต่ไม่ได้ระบุออก
- คำสั่งย่อย [`list copy`](reference/commands.md#banshee-list-copy) ใหม่สำหรับคัดลอก entity จากรายการหนึ่งไปยังอีกรายการหนึ่ง โดยค่าเริ่มต้นจะต่อท้าย หรือใช้ [`-o`/`--overwrite`](reference/commands.md#banshee-list-copy--overwrite) เพื่อให้ปลายทางสะท้อนต้นทางอย่างแน่นอน
- รองรับ[การใช้งาน banshee กับ AI agent](getting-started/llms.md) เพื่อให้ coding assistant สามารถค้นพบและรัน CLI ได้

### เปลี่ยนแปลง
- [`list clear`](reference/commands.md#banshee-list-clear) ขณะนี้ลบ entity พร้อมกันหลายรายการ (เร็วขึ้นมากสำหรับรายการขนาดใหญ่) ซึ่งสอดคล้องกับ [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove): รายงานสิ่งที่ถูกลบโดยจัดกลุ่มผลลัพธ์ตามสถานะ (`REMOVED` และรายการที่ไม่สามารถลบได้) และเรียงลำดับเพื่อความสะดวกในการอ่าน
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) ขณะนี้ข้าม entity ที่มีอยู่ในรายการแล้วแทนที่จะพยายามเพิ่มซ้ำ โดยรายงานว่าเป็น `UNCHANGED` ซึ่งเพิ่มความเร็วอย่างมีนัยสำคัญเมื่อรันไฟล์ input เดิมซ้ำเพื่อเพิ่มและลบ entity
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) และ [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) ขณะนี้จัดกลุ่มผลลัพธ์ตามสถานะ (`ADDED`, `REMOVED`, `UNCHANGED`) และเรียงลำดับเพื่อความสะดวกในการอ่าน
- [`ca search`](reference/commands.md#banshee-ca-search) และ [`pba search`](reference/commands.md#banshee-pba-search) ขณะนี้แสดง progress indicator ไปยัง stderr เพื่อให้ stdout สะอาดสำหรับการ pipe ไปยังคำสั่ง `export` ใหม่
- ผลลัพธ์แบบ pretty (`-p`, `--pretty`) ของ [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) และ [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) ขณะนี้แสดง risk score ด้วยรหัสสีตามระดับความเป็นอันตราย
- อัปเกรด PSEngine เป็น ~v2.8.1

### แก้ไข
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) และ [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) ขณะนี้ข้ามบรรทัด input ที่ว่างเปล่าและรายงานข้อผิดพลาดที่ชัดเจนเมื่อไม่มี entity ถูกระบุ

## 1.1.3 - 2026-03-18

### แก้ไข
- แก้ไขปัญหาใน [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ที่ไม่มีการใช้ multithreading ในการ enrich แบบ SOAR ขณะนี้การ enrich risk score เร็วขึ้นสำหรับการจับแพ็กเก็ตขนาดใหญ่


## 1.1.0 - 2026-03-13

### เพิ่มใหม่
- คำสั่งย่อย [`risklist create`](reference/commands.md#banshee-risklist-create) ใหม่สำหรับสร้าง custom risk list โดยรวม Recorded Future risk rule หนึ่งรายการหรือมากกว่าเข้าเป็นไฟล์เดียวที่ไม่มีข้อมูลซ้ำ รองรับรูปแบบผลลัพธ์ CSV, JSON และ EDL, การกรอง risk score ขั้นต่ำแบบเลือกได้ และการอัปโหลดโดยตรงไปยัง Recorded Future Fusion
- คำสั่งย่อย [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) ใหม่สำหรับการ enrich IOC (ตัวชี้วัดการประนีประนอม) จำนวนมากอย่างรวดเร็ว โดยรวม indicator สูงสุด 1,000 รายการต่อการเรียก API และส่งคืน risk score พร้อม risk rule ที่ถูกกระตุ้นสำหรับแต่ละ indicator รองรับ IOC ทุกประเภท: IP, domain, URL, hash และช่องโหว่
- ผลลัพธ์ JSON ของ [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ขณะนี้รวมรายละเอียดหลักฐาน risk rule ซึ่งอธิบายหลักฐานเฉพาะที่ทำให้ risk rule ถูกกระตุ้น

### เปลี่ยนแปลง
- ค่าเริ่มต้นของจำนวนผลลัพธ์ [`entity search`](reference/commands.md#banshee-entity-search) เพิ่มขึ้นเป็น 100 รายการ
- ค่าเริ่มต้นของจำนวนผลลัพธ์ [`list search`](reference/commands.md#banshee-list-search) เพิ่มขึ้นเป็น 1,000 รายการ
- ค่าเริ่มต้นของจำนวนผลลัพธ์ [`pba search`](reference/commands.md#banshee-pba-search) เพิ่มขึ้นเป็น 50 รายการ
- จำนวนผลลัพธ์สูงสุดของ [`pba search`](reference/commands.md#banshee-pba-search) เพิ่มขึ้นเป็น 10,000 รายการ
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ขณะนี้รับ risk score ที่ต่ำถึง 1

### แก้ไข
- แก้ไขปัญหาใน [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) ที่ไม่มีการใช้ multithreading ทำให้การ lookup จำนวนมากทำงานตามลำดับ ขณะนี้การ lookup เร็วขึ้นสูงสุด 20 เท่าเมื่อ enrich indicator หลายรายการ
- แก้ไขปัญหาใน [`risklist fetch`](reference/commands.md#banshee-risklist-fetch) ที่คำสั่งจะล้มเหลวเมื่อแยกวิเคราะห์ค่าคอลัมน์ที่ใหญ่ผิดปกติในไฟล์ CSV
- แก้ไขปัญหาที่ [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) จะล้มเหลวเมื่อแยกวิเคราะห์ลิงก์ IOC ที่ว่างเปล่า
- แก้ไขปัญหาในคำสั่ง [`list`](reference/commands.md#banshee-list) ที่สาเหตุของข้อผิดพลาดไม่ถูกแสดงอย่างถูกต้องเสมอไปเมื่อเกิด API error

## 1.0.0 - 2025-12-05

### เพิ่มใหม่

- คำสั่ง [`risklist`](reference/commands.md#banshee-risklist) ใหม่สำหรับดาวน์โหลดและตรวจสอบ metadata ของ Recorded Future Risk Lists
- คำสั่ง [`rules`](reference/commands.md#banshee-rules) ใหม่สำหรับค้นหาและดาวน์โหลด detection rule (YARA, Snort, Sigma)
- รองรับฟิลด์ CVSS v4 ในคำสั่ง [`ioc search`](reference/commands.md#banshee-ioc-search) และ [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)

### แก้ไข

- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) และ [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove) ขณะนี้ตัดข้อมูลซ้ำของ entity ที่ผู้ใช้ระบุ
- แก้ไขปัญหาที่ชื่อ entity ที่มีช่องว่างไม่ถูกแยกวิเคราะห์อย่างถูกต้องใน [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) และ [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)
- [`pba lookup`](reference/commands.md#banshee-pba-lookup) ขณะนี้จัดการ alert ได้อย่างถูกต้องเมื่อการดึงรูปภาพล้มเหลว

### เปลี่ยนแปลง

- ผลลัพธ์ JSON ของ [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ขณะนี้รวมรายละเอียดหลักฐาน risk rule และ risk rule ทั้งหมดที่ IOC กระตุ้น
- อัปเกรด PSEngine เป็น v2.4.0


## 0.0.5 - 2025-11-12

## แก้ไข

- แก้ไขปัญหาใน [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ที่โปรแกรมจะออกโดยไม่คาดคิดหากไม่พบ IP หรือ domain ในไฟล์ pcap

## 0.0.4 - 2025-11-07

### เพิ่มใหม่

- เพิ่มการรองรับการกรองตามสถานะ alert ในคำสั่ง [`ca search`](reference/commands.md#banshee-ca-search)
- เพิ่มการรองรับการกรองตาม entity ในคำสั่ง [`pba search`](reference/commands.md#banshee-pba-search)
- เพิ่มการรองรับหมวดหมู่ `malware_report` สำหรับคำสั่ง `pba` ทั้งหมด
- ผลลัพธ์แบบ pretty (`-p`, `--pretty`) สำหรับ [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) และ [`ioc search`](reference/commands.md#banshee-ioc-search) ขณะนี้รวม hash algorithm สำหรับ hash
- ผลลัพธ์แบบ pretty (`-p`, `--pretty`) สำหรับ [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) และ [`ioc search`](reference/commands.md#banshee-ioc-search) ขณะนี้รวมขั้นตอน lifecycle สำหรับช่องโหว่
- เพิ่มตัวเลือก `-r`/`--risk-score` สำหรับ [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) เพื่อกรองผลลัพธ์ตาม risk score
- เพิ่มตัวเลือก `-t`/`--threat-hunt` สำหรับ [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) เพื่อเปิดใช้งาน threat hunting

### เปลี่ยนแปลง

- ปรับปรุงการเลือกฟิลด์สำหรับแต่ละระดับ verbosity ใน [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)
- ขยาย [`ioc search`](reference/commands.md#banshee-ioc-search) เพื่อรองรับระดับ verbosity 1 ถึง 5 (ค่าเริ่มต้นคือ 1)
- เปลี่ยนชื่อคำสั่งย่อย `pcap analyze` เป็น [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) ขณะนี้สร้างผลลัพธ์ JSON ที่ปรับปรุงแล้ว รวมถึง filter query ที่เข้ากันได้กับ Wireshark
- อัปเกรด PSEngine เป็น v2.3.0

### แก้ไข

- แก้ไขปัญหาที่ [`ca rules`](reference/commands.md#banshee-ca-rules) จะตัดผลลัพธ์ที่ 10 alerting rule
- แก้ไขข้อผิดพลาดใน [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) เมื่อ IOC ไม่มีรายละเอียดหลักฐาน

### ลบออก

- ลบผลลัพธ์ interactive TUI จาก `pba enrich` แทนที่ด้วยผลลัพธ์แบบ pretty (`--pretty`, `-p`)


## 0.0.3 - 2025-09-02

### เพิ่มใหม่

- คำสั่งย่อย [`ca update`](reference/commands.md#banshee-ca-update) ใหม่สำหรับอัปเดต Classic Alert หนึ่งรายการหรือมากกว่า
- คำสั่งย่อย [`pba update`](reference/commands.md#banshee-pba-update) ใหม่สำหรับอัปเดต Playbook Alert หนึ่งรายการหรือมากกว่า
- คำสั่ง [`pba`](reference/commands.md#banshee-pba) ขณะนี้รองรับหมวดหมู่ `geopolitics_facility`
- รองรับ Python 3.13
- การตรวจสอบเวอร์ชัน `tshark` ขณะนี้บังคับใช้เวอร์ชันขั้นต่ำ 4.4.5

### แก้ไข

- `pcap analyze` ไม่ crash อีกต่อไปเนื่องจากเวอร์ชันไม่ตรงกัน
- ปรับปรุงการจัดการ exception ทั่วทั้ง CLI

### เปลี่ยนแปลง

- `ioc search ENTITY_TYPE IOC` ขณะนี้รับ IOC ที่คั่นด้วยช่องว่างแทนที่จะเป็น string ที่คั่นด้วยเครื่องหมายจุลภาค
- ปรับปรุงการจัดรูปแบบผลลัพธ์ของ `pba lookup ALERT_ID -p`
- `ca search --triggered` ขณะนี้รองรับช่วงเวลา
- `ca search -r` ขณะนี้รับหลาย rule โดยการระบุ `-r` ซ้ำ (เช่น `-r rule1 -r rule2`) แทนที่จะเป็น string ที่คั่นด้วยเครื่องหมายจุลภาค
- อัปเกรด PSEngine เป็น v2.0.6


## 0.0.2 - 2025-02-20

### เพิ่มใหม่

- คำสั่ง [`entity`](reference/commands.md#banshee-entity) ใหม่สำหรับค้นหาและ lookup entity
- คำสั่ง [`list`](reference/commands.md#banshee-list) ใหม่สำหรับจัดการ Recorded Future Lists & Watch Lists
- คำสั่งย่อย [`ioc rules`](reference/commands.md#banshee-ioc-rules) ใหม่สำหรับค้นหาและกรอง IOC rule
- ตัวเลือก `--debug` ใหม่สำหรับการแก้ไขปัญหาขั้นสูง


### เปลี่ยนแปลง

- ตัวเลือก ``-v`` ของคำสั่งย่อย [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) ขณะนี้อนุญาตให้ผู้ใช้เลือกระดับ verbosity (จาก 1 ถึง 5)
- คำสั่งย่อย [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) ขณะนี้ต้องการประเภท entity เป็น argument เช่น ``banshee ioc lookup ip 8.8.8.8``
- คำสั่งย่อย [`ca lookup`](reference/commands.md#banshee-ca-lookup) ขณะนี้ส่งคืน alert แบบ pretty ที่ปรับปรุงแล้ว
- อัปเกรด PSEngine เป็น v2.0.2


## 0.0.1 - 2024-09-01

### เพิ่มใหม่

- รุ่น Beta

---

🚀 จัดทำโดยทีม Cyber Security Engineers แห่ง Recorded Future