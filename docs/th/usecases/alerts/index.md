# การจัดการการแจ้งเตือน

## สรุปกรณีการใช้งาน
จัดการ คัดแยก และอัปเดตการแจ้งเตือนของ Recorded Future (Classic & Playbook) เป็นชุดโดยตรงจาก terminal เพื่อเร่งการตอบสนองของ Security Operations Center (SOC) และขั้นตอนการตรวจสอบ

## ปัญหา
การสลับไปยัง UI สำหรับการแจ้งเตือนทุกรายการทำให้การตรวจสอบล่าช้า ส่งผลให้นักวิเคราะห์เกิดความเหนื่อยล้าและการจัดการการแจ้งเตือนไม่สอดคล้องกัน กระบวนการคัดแยกด้วยตนเองทำให้การตอบสนองต่อเหตุการณ์ช้าลงและสร้างคอขวดในขั้นตอนการดำเนินงานด้านความปลอดภัย

## วิธีแก้ปัญหา
ดึงข้อมูลและจัดการการแจ้งเตือนของ Recorded Future โดยตรงจาก terminal โดยใช้คำสั่ง [`banshee ca`](../../reference/commands.md#banshee-ca) และ [`banshee pba`](../../reference/commands.md#banshee-pba)

- สำหรับ Classic Alerts ให้ใช้ [`banshee ca search`](../../reference/commands.md#banshee-ca-search) ร่วมกับตัวกรองเวลา และ [`banshee ca update`](../../reference/commands.md#banshee-ca-update) สำหรับการเปลี่ยนสถานะเป็นชุด การเพิ่มหมายเหตุ และการอัปเดตผู้รับมอบหมาย

- สำหรับ Playbook Alerts ให้ใช้ [`banshee pba search`](../../reference/commands.md#banshee-pba-search) ร่วมกับตัวกรองหมวดหมู่และลำดับความสำคัญ จากนั้นใช้ [`banshee pba update`](../../reference/commands.md#banshee-pba-update) เพื่อแก้ไขสถานะ เพิ่มความคิดเห็น มอบหมายผู้ใช้ และกำหนดกลยุทธ์การเปิดใหม่

- ส่งต่อผลการค้นหาใดก็ได้ไปยัง [`banshee ca export`](../../reference/commands.md#banshee-ca-export) หรือ [`banshee pba export`](../../reference/commands.md#banshee-pba-export) เพื่อบันทึกรายละเอียดการแจ้งเตือนแบบครบถ้วนในรูปแบบ JSON หรือเพิ่ม `--csv` เพื่อสรุปในรูปแบบที่พร้อมใช้กับ spreadsheet สำหรับการรายงานแบบออฟไลน์และการแบ่งปัน

แนวทางนี้ช่วยเร่งการคัดแยก รักษาความสอดคล้องของการแจ้งเตือน และช่วยให้นักวิเคราะห์สามารถอัปเดตการแจ้งเตือนหลายรายการพร้อมกันผ่านการดำเนินการแบบชุด