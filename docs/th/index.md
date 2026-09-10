---
title: ""
---

<div style="width: 100%; text-align: center;">
    <img src="assets/rf-logo.png" alt="Recorded Future Logo" style="margin-top: -80px; margin-bottom: 16px;">
</div>
<p style="margin-top: -60px;">
PS Banshee เป็นเครื่องมือบรรทัดคำสั่ง (command-line tool) สำหรับการเข้าถึง Recorded Future Intelligence อย่างรวดเร็วและมีประสิทธิภาพ ออกแบบมาสำหรับผู้เชี่ยวชาญด้านความปลอดภัยและทีม SOC
</p>
<img src="img/welcome.gif" alt="Welcome to PS Banshee!" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

!!! tip "ขับเคลื่อนโดย PSEngine"
    PS Banshee ขับเคลื่อนด้วยไลบรารี [PSEngine](https://recordedfuture-professionalservices.github.io/psengine/latest/)

---

## คุณสมบัติหลัก

- การเสริมข้อมูล E-mail (EML)
- การค้นหาและตรวจสอบ IOC (ตัวบ่งชี้การบุกรุก)
- การเสริมข้อมูล Packet capture (pcap)
- การค้นหา ตรวจสอบ อัปเดต และส่งออก Recorded Future Alert
- การค้นหาและดาวน์โหลด Recorded Future Detection Rules (YARA, Snort, Sigma)
- การค้นหาและตรวจสอบ Recorded Future Entity
- การจัดการ Recorded Future List และ Watch List
- การค้นหา ตรวจสอบ อัปเดต และส่งออก Recorded Future Playbook Alert
- การดาวน์โหลดและสร้าง Recorded Future Risk List

## การติดตั้ง

PS Banshee พร้อมใช้งานบน [PyPI](https://pypi.org/project/ps-banshee/) และสามารถติดตั้งได้โดยใช้ `pip` หรือ `pipx`

!!! tip "PS Banshee ต้องการ Python 3.10 หรือเวอร์ชันที่ใหม่กว่า (สูงสุด 3.13)"

### แนะนำ: pipx (สภาพแวดล้อมแบบแยกอิสระ)
เพื่อติดตั้งแบบ global ให้รันคำสั่งต่อไปนี้:

```bash
pipx install ps-banshee
```


!!! info "การติดตั้ง pipx"
    หากยังไม่ได้ติดตั้ง pipx โปรดดู[คู่มือการติดตั้ง](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)


### ทางเลือก: pip (สภาพแวดล้อมปัจจุบัน)
เพื่อติดตั้งในสภาพแวดล้อมปัจจุบัน ให้รันคำสั่งต่อไปนี้:
```bash
pip install ps-banshee
```

### การอ้างอิง (Dependencies)

การอ้างอิง Python ที่จำเป็นทั้งหมดจะได้รับการแก้ไขโดยอัตโนมัติโดย `pipx`
เพื่อใช้คำสั่ง `pcap` โปรดตรวจสอบให้แน่ใจว่ามีสิ่งต่อไปนี้:

- tshark 3.0.0 หรือเวอร์ชันที่ใหม่กว่า

### การเติมคำสั่งอัตโนมัติ (Command Auto Completion)

หลังจากติดตั้ง PS Banshee แล้ว ให้เปิดใช้งานการเติมคำสั่งอัตโนมัติด้วยคำสั่ง:

```bash
banshee --install-completion
```

รีสตาร์ต shell เพื่อให้การติดตั้งเสร็จสมบูรณ์ จากนั้นสามารถใช้ TAB เพื่อเติมคำสั่งอัตโนมัติได้

## เอกสารประกอบ

เพื่อดูคำสั่งที่ใช้งานได้ ให้รันคำสั่งต่อไปนี้:

```bash
banshee
```

### การอนุญาตสิทธิ์ (Authorization)

--8<-- "_includes/authorization.md"

### Proxies

หากอยู่เบื้องหลัง proxy ให้กำหนดค่าตัวแปรสภาพแวดล้อม `HTTP_PROXY` และ `HTTPS_PROXY`

เพื่อปิดใช้งานการตรวจสอบ SSL ให้ใช้แฟล็ก `-s`:

```bash
banshee -s ca rules
```

## ขั้นตอนถัดไป

[เริ่มต้นใช้งาน](getting-started/index.md) PS Banshee ได้เลยตอนนี้!