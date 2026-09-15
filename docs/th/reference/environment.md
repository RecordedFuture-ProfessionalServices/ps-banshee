# ตัวแปรสภาพแวดล้อม

PS Banshee ใช้ตัวแปรสภาพแวดล้อมตามที่อธิบายไว้ในส่วนต่าง ๆ ด้านล่าง

### `RF_TOKEN`

เพื่อให้ PS Banshee ได้รับการอนุญาตในการเข้าถึง Recorded Future APIs จำเป็นต้องมี API token ผู้ใช้สามารถกำหนด token เป็นตัวแปรสภาพแวดล้อมได้ดังนี้:

```bash
export RF_TOKEN=API-TOKEN
```

หรือระบุเป็นอาร์กิวเมนต์ `-k` หรือ `--api-key` ให้กับคำสั่ง `banshee` โดยตรง:

```bash
banshee -k API-TOKEN ca search
```


### `HTTP_PROXY`

หากองค์กรของคุณกำหนดให้ใช้ proxy ให้ตรวจสอบว่าได้กำหนดค่า `HTTP_PROXY` แล้ว ตัวอย่างเช่น:

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
```

สำหรับข้อมูลเพิ่มเติม โปรดดูที่ [เอกสาร requests](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)

### `HTTPS_PROXY`

หากองค์กรของคุณกำหนดให้ใช้ proxy ให้ตรวจสอบว่าได้กำหนดค่า `HTTPS_PROXY` แล้ว ตัวอย่างเช่น:

```bash
export HTTPS_PROXY="http://10.10.1.10:1080"
```
สำหรับข้อมูลเพิ่มเติม โปรดดูที่ [เอกสาร requests](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)


!!! Tip

    หากใช้ตัวแปรสภาพแวดล้อม proxy ใดตัวหนึ่ง คุณอาจจำเป็นต้องปิดใช้งานการตรวจสอบ SSL ซึ่งสามารถทำได้โดยใช้ flag `-s` หรือ `--no-ssl-verify` ที่ส่งให้กับคำสั่ง `banshee` โดยตรง ตัวอย่างเช่น:

    $ banshee -s ca search