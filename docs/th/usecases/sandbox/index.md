# การวิเคราะห์ Sandbox

## สรุปกรณีการใช้งาน
ส่งไฟล์และ URL สำหรับการวิเคราะห์มัลแวร์อัตโนมัติใน Recorded Future Sandbox เรียกดูรายงานที่ได้รับ และส่งต่อตัวอย่างที่ผ่านการตรวจสอบแล้วสำหรับการวิเคราะห์แบบออฟไลน์ เพื่อเร่งกระบวนการคัดกรองและการสืบสวนภัยคุกคามของ Security Operations Center (SOC)

## ปัญหา
นักวิเคราะห์จำเป็นต้องทดสอบไฟล์และ URL ที่น่าสงสัยในสภาพแวดล้อมที่ปลอดภัยและควบคุมได้ เพื่อระบุเจตนาและดึงข้อมูล threat indicator (ตัวบ่งชี้ภัยคุกคาม) ออกมา หากไม่มีขั้นตอนการทำงานที่บูรณาการไว้ การรวบรวมและเชื่อมโยงรายงานที่ได้รับ ซึ่งประกอบด้วย static signature, กิจกรรมเชิงพฤติกรรม, network IOC (ตัวบ่งชี้การประนีประนอมเครือข่าย) และ malware config จะต้องดำเนินการด้วยตนเองผ่านเครื่องมือหลายชนิด ซึ่งทำให้การตอบสนองของ SOC ล่าช้า

## วิธีแก้ไข
ส่งตัวอย่างและเรียกดูรายงานโดยตรงใน PS Banshee โดยใช้คำสั่ง [`banshee sandbox`](../../reference/commands.md#banshee-sandbox)

- ใช้ [`banshee sandbox submit`](../../reference/commands.md#banshee-sandbox-submit) เพื่อส่งไฟล์ในเครื่อง, URL, หรือตัวอย่างสาธารณะสำหรับการวิเคราะห์ เพิ่ม [`--wait`](../../reference/commands.md#banshee-sandbox-submit--wait) เพื่อรอจนกว่าการวิเคราะห์จะเสร็จสิ้นและแสดงรายงานสรุปทันที หรือ [`--interactive`](../../reference/commands.md#banshee-sandbox-submit--interactive) เพื่อหยุดชั่วคราวที่ขั้นตอน static analysis และเลือก detonation profile ก่อนดำเนินการต่อ

- เมื่อการวิเคราะห์เสร็จสิ้น ใช้ [`banshee sandbox report overview`](../../reference/commands.md#banshee-sandbox-report-overview) เพื่อดูสรุปของ verdict, malware family, network IOC และผลลัพธ์รายงานแต่ละ task; ใช้ [`banshee sandbox report static`](../../reference/commands.md#banshee-sandbox-report-static) สำหรับการวิเคราะห์ก่อนการ detonation และ malware config ที่ดึงออกมา; และใช้ [`banshee sandbox report behavioral`](../../reference/commands.md#banshee-sandbox-report-behavioral) สำหรับกิจกรรมหลังการ detonation ซึ่งรวมถึง signature ที่ถูกกระตุ้น, กระบวนการที่สังเกตได้ และ C2 ที่ดึงออกมา

- ใช้ [`banshee sandbox stats`](../../reference/commands.md#banshee-sandbox-stats) เพื่อสร้างรายงานสรุปยามเช้าสำหรับ SOC ซึ่งแสดงปริมาณการส่ง, การกระจายคะแนน, malware family ที่พบมากที่สุด และ network IOC ในช่วงเวลาย้อนหลังที่กำหนดได้ เหมาะสำหรับการส่งต่อกะหรือการคัดกรองประจำวัน

- ใช้ [`banshee sandbox list`](../../reference/commands.md#banshee-sandbox-list) เพื่อตรวจสอบการส่งล่าสุดจากบัญชีของคุณเอง, องค์กรของคุณ หรือ public feed และ [`banshee sandbox get`](../../reference/commands.md#banshee-sandbox-get) เพื่อตรวจสอบสถานะปัจจุบัน, คะแนนรวม และรายละเอียดแยกตาม task ของตัวอย่างใดตัวอย่างหนึ่งโดยไม่ต้องดึงรายงานฉบับเต็ม

- ใช้ [`banshee sandbox search`](../../reference/commands.md#banshee-sandbox-search) เพื่อค้นหาข้อมูลในประวัติการส่งโดยใช้ hash, malware family, tag, botnet, wallet, network indicator (IP, domain, URL) หรือช่วงวันที่ส่ง ส่ง Triage query string แบบ raw ด้วย `--query` สำหรับนิพจน์ `AND`/`OR`/`NOT`

- ใช้ [`banshee sandbox download`](../../reference/commands.md#banshee-sandbox-download) เพื่อดึงข้อมูล byte ต้นฉบับที่ส่งมาสำหรับการวิเคราะห์แบบออฟไลน์ (การปรับแต่ง YARA/Sigma, การทดสอบการตรวจจับ EDR, การระบุแหล่งที่มาของแคมเปญ) ตัวอย่างแต่ละรายการจะถูกห่อหุ้มในไฟล์ ZIP ที่เข้ารหัสด้วย AES และใช้รหัสผ่าน `infected` — แตกไฟล์ด้วย `7z x -pinfected <sample-id>.zip` ข้อมูล byte จะอยู่ใน process memory ชั่วคราวระหว่างการดาวน์โหลดและการบีบอัด ดังนั้นควรรันบนเครื่องของนักวิเคราะห์

- ใช้ [`banshee sandbox delete`](../../reference/commands.md#banshee-sandbox-delete) เพื่อลบตัวอย่างและ artifact ที่เกี่ยวข้องเมื่อไม่จำเป็นต้องใช้อีกต่อไป

- สำหรับทีมที่ใช้สภาพแวดล้อมการ detonation แบบกำหนดเอง คำสั่ง [`banshee sandbox profile`](../../reference/commands.md#banshee-sandbox-profile) ให้คุณสร้าง, อัปเดต และลบ analysis profile ที่ควบคุม OS, การกำหนดค่าเครือข่าย, เบราว์เซอร์ และ analysis timeout ที่ใช้กับการส่งแต่ละรายการ