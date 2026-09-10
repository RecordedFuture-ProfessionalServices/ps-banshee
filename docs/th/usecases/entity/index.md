# การจับคู่เอนทิตี (Entity Matching)

## สรุปกรณีการใช้งาน
ค้นหาและระบุ Recorded Future Entities (บริษัท, มัลแวร์, ผู้คุกคาม ฯลฯ) เพื่อให้การอ้างอิงมีความสอดคล้องกันทั่วทั้งเครื่องมือและขั้นตอนการทำงานของ Security Operations Center (SOC)

สำหรับข้อมูลเพิ่มเติมเกี่ยวกับ Recorded Future entities คลิก[ที่นี่](https://support.recordedfuture.com/hc/en-us/articles/115001359567-What-is-an-Entity)

## ปัญหา
ชื่อในรูปแบบข้อความอิสระ (free-text) อาจทำให้เกิดความไม่ตรงกันระหว่างเครื่องมือต่างๆ กับ Recorded Future เอนทิตีประเภท Threat Actor อาจมีชื่อเดียวกับเอนทิตีประเภท Username แต่ ID ของเอนทิตีทั้งสองจะแตกต่างกัน ส่งผลให้เกิดความสับสนและการเชื่อมโยงข้อมูลภัยคุกคามที่ไม่ถูกต้อง

## วิธีแก้ไข
ค้นหาและระบุเอนทิตีโดยตรงใน PS Banshee โดยใช้คำสั่ง [`banshee entity`](../../reference/commands.md#banshee-entity)

- ใช้ [`banshee entity search`](../../reference/commands.md#banshee-entity-search) เมื่อมีชื่อเอนทิตีและ/หรือประเภทเอนทิตี และต้องการค้นหา ID ของเอนทิตีที่ตรงกัน

- ใช้ [`banshee entity lookup`](../../reference/commands.md#banshee-entity-lookup) เมื่อมี ID ของเอนทิตีและต้องการดึงข้อมูลชื่อและประเภทของเอนทิตีนั้น

เมื่อได้รับ ID เอนทิตีที่ถูกต้องแล้ว ให้นำไปใช้ในคำสั่ง PS Banshee ลำดับถัดไป เช่น [`banshee list add`](../../reference/commands.md#banshee-list-add) เพื่อให้มั่นใจว่าการอ้างอิงเอนทิตีใน watchlist ขององค์กรมีความถูกต้องแม่นยำ