# ขั้นตอนแรกกับ PS Banshee

หลังจาก[ติดตั้ง PS Banshee](./installation.md) แล้ว คุณสามารถตรวจสอบว่าคำสั่งพร้อมใช้งานโดยเรียกใช้คำสั่ง [banshee](../reference/commands.md#banshee):

<img src="../../img/first-steps.gif" alt="PS Banshee commands" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

คุณควรเห็นเมนูช่วยเหลือที่แสดงรายการคำสั่งที่พร้อมใช้งาน

### การอนุญาตสิทธิ์

--8<-- "_includes/authorization.md"

### Proxies

หากคุณอยู่หลัง proxy ให้ตั้งค่าตัวแปรสภาพแวดล้อม `HTTP_PROXY` และ `HTTPS_PROXY`

หากต้องการปิดใช้งานการตรวจสอบ SSL ให้ใช้แฟล็ก `-s`:

```bash
banshee -s ca rules
```

## ขั้นตอนถัดไป

เมื่อยืนยันแล้วว่า PS Banshee ได้รับการติดตั้งเรียบร้อยแล้ว ไปที่[ข้อมูลอ้างอิงคำสั่ง](../reference/commands.md) เพื่อเริ่มใช้งาน PS Banshee และเรียนรู้วิธี[ขอความช่วยเหลือ](./help.md) หากพบปัญหาใด ๆ