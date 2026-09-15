# pcap

> ดู [index.md](index.md) สำหรับข้อมูลเกี่ยวกับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบผลลัพธ์ และข้อสังเกตทั่วไปเกี่ยวกับ LLM

> **เงื่อนไขเบื้องต้น:** ต้องติดตั้ง `tshark` และกำหนดค่าไว้ใน `PATH` ใน Banshee 1.2.0 คำสั่ง `banshee pcap enrich --help` จะล้มเหลวหาก `tshark` ไม่ได้ติดตั้งไว้ ดังนั้นควรตรวจสอบด้วย `command -v tshark` ก่อนใช้งาน

### `banshee pcap enrich FILE_PATH`

แยกวิเคราะห์ไฟล์ pcap สกัด IP และโดเมน จากนั้นเสริมข้อมูลด้วย threat intelligence (ข่าวกรองภัยคุกคาม) จาก RF โดยค่าเริ่มต้น จะแสดงเฉพาะตัวบ่งชี้ที่มีคะแนนความเสี่ยงเกินกว่าเกณฑ์ที่กำหนด (65)

| ตัวเลือก | ย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | แสดงเฉพาะตัวบ่งชี้ที่มีคะแนนสูงกว่าค่านี้ (1–99) |
| `--threat-hunt` | `-t` | `false` | รวมตัวบ่งชี้ที่เชื่อมโยงกับ threat actor (ผู้ก่อภัยคุกคาม) แม้ว่าคะแนนจะต่ำกว่าเกณฑ์ (สำหรับการทำ retrospective threat hunting) |
| `--pretty` | `-p` | | จัดรูปแบบผลลัพธ์ให้อ่านง่าย |

ผลลัพธ์ JSON ค่าเริ่มต้นเป็น array แบบแบนของระเบียนข้อมูล โดยมีฟิลด์ต่าง ๆ เช่น `ioc`, `risk_score`, `most_malicious_rule`, `rule_evidence`, `ta_names`, `malwares` และ `wireshark_query`

```bash
banshee pcap enrich sandbox.pcap
banshee pcap enrich honeypot-traffic.pcap -r 25 -t -p

# Summarize hits from JSON output
banshee pcap enrich sandbox.pcap -r 25 -t | jq '[.[] | {indicator: .ioc, score: .risk_score, top_rule: .most_malicious_rule, evidence_rules: [(.rule_evidence // [])[].rule]}] | sort_by(-.score)'
```