# email

> ดู [index.md](index.md) สำหรับข้อมูลเกี่ยวกับการยืนยันตัวตน การตรวจสอบความพร้อม รูปแบบเอาต์พุต และหมายเหตุเกี่ยวกับ LLM ที่ใช้ร่วมกัน

### `banshee email enrich FILE_PATH`

แยกวิเคราะห์ไฟล์ EML แล้วดึง IP จาก header, URL/โดเมนจาก body และแฮชของไฟล์แนบ จากนั้นเสริมข้อมูล indicator ด้วย RF threat intelligence (ข้อมูลภัยคุกคาม) โดยค่าเริ่มต้นจะแสดงเฉพาะ indicator ที่มีคะแนนความเสี่ยงสูงกว่าเกณฑ์ที่กำหนด (65)

| ตัวเลือก | รูปแบบย่อ | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | แสดงเฉพาะ indicator ที่มีคะแนนสูงกว่าค่านี้ (0–99) |
| `--threat-hunt` | `-t` | `false` | รวม indicator ที่เชื่อมโยงกับ threat actor แม้คะแนนจะต่ำกว่าเกณฑ์ก็ตาม |
| `--pretty` | `-p` | | จัดรูปแบบเอาต์พุตให้อ่านง่าย (Pretty print) |

เอาต์พุต JSON เริ่มต้นเป็น array แบบแบนของระเบียนที่มีฟิลด์ต่างๆ เช่น `ioc`, `type`, `location`, `risk_score`, `first_seen`, `last_seen`, `rule_evidence`, `analyst_notes`, `malwares`, `count_of_analyst_notes` และ `ta_names`

```bash
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p

# Extract the highest-risk indicators from an enriched EML
banshee email enrich phishing_email.eml -r 1 | jq '[.[] | {ioc, type, location, score: .risk_score, top_rule: (.rule_evidence[0].rule // "")}] | sort_by(-.score)'
```