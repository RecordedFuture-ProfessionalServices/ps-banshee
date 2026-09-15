# การติดตั้ง PS Banshee

## วิธีการติดตั้ง

ติดตั้ง [ps-banshee](https://pypi.org/project/ps-banshee/) ด้วย `pipx` หรือ `pip`

## การติดตั้ง

!!! tip "PS Banshee ต้องใช้ Python 3.10 หรือเวอร์ชันที่ใหม่กว่า (สูงสุดถึง 3.13)"

### แนะนำ: pipx (สภาพแวดล้อมแบบแยกส่วน)
เพื่อติดตั้งในระดับ global ให้รัน:

```bash
pipx install ps-banshee
```


!!! info "การติดตั้ง pipx"
    หากยังไม่ได้ติดตั้ง pipx ให้ดูที่ [คู่มือการติดตั้ง](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)


### ทางเลือก: pip (สภาพแวดล้อมปัจจุบัน)
เพื่อติดตั้งในสภาพแวดล้อมปัจจุบัน ให้รัน:
```bash
pip install ps-banshee
```


### การอ้างอิง (Dependencies)

Python dependencies ที่จำเป็นทั้งหมดจะถูกจัดการโดยอัตโนมัติโดย `pip`
เพื่อใช้คำสั่ง `pcap` ให้แน่ใจว่ามีสิ่งต่อไปนี้:

- tshark 3.0.0 หรือเวอร์ชันที่ใหม่กว่า



## การอนุญาตสิทธิ์

PS Banshee อ่าน API key ของ Recorded Future จากตัวแปรสภาพแวดล้อม `RF_TOKEN` (แนะนำ) หรือจาก flag `-k` / `--api-key` ที่ระบุในแต่ละคำสั่ง

### ตัวเลือกที่ 1: ตั้งค่า `RF_TOKEN` (แนะนำ)

=== "macOS / Linux"

    เฉพาะ shell ปัจจุบันเท่านั้น:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    บันทึกอย่างถาวรสำหรับ shell ในอนาคต (zsh — ปรับเป็น `~/.bashrc` สำหรับ bash) เปิด shell ใหม่หลังจากรันคำสั่งนี้ (หรือรัน `source ~/.zshrc` เพื่อใช้งานใน shell ปัจจุบัน):

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    เฉพาะ session ปัจจุบันเท่านั้น:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    บันทึกอย่างถาวรสำหรับ session ในอนาคต (เปิด PowerShell ใหม่หลังจากรันคำสั่งนี้):

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    เฉพาะ session ปัจจุบันเท่านั้น:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    บันทึกอย่างถาวรสำหรับ session ในอนาคต (เปิด Command Prompt ใหม่หลังจากรันคำสั่งนี้):

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

### ตัวเลือกที่ 2: ระบุด้วย `-k` ในแต่ละคำสั่ง

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

วิธีนี้ใช้งานได้บนทุกแพลตฟอร์ม แต่มีความยุ่งยากมากกว่า และ key อาจถูกบันทึกไว้ใน shell history

## การอัปเกรด PS Banshee

เพื่ออัปเกรด PS Banshee เป็นเวอร์ชันที่ใหม่กว่า ให้ติดตั้งใหม่โดยใช้ไฟล์ wheel ที่อัปเดตแล้ว

!!! warning "การอัปเกรดจาก v1.0.0 หรือเวอร์ชันก่อนหน้า"
    หากกำลังอัปเกรดจาก v1.0.0 หรือเวอร์ชันที่เก่ากว่า จะต้องถอนการติดตั้งแพ็กเกจที่มีอยู่ก่อนจึงจะติดตั้งเวอร์ชันใหม่ได้

    **หากติดตั้งด้วย pipx:**
    ```bash
    pipx uninstall banshee 
    pipx install ps-banshee
    ```

    **หากติดตั้งด้วย pip:**
    ```bash
    pip uninstall banshee
    pip install ps-banshee
    ```

**หากติดตั้งด้วย pipx:**

```bash
pipx install --force ps-banshee
```

**หากติดตั้งด้วย pip:**

```bash
pip install --upgrade ps-banshee
```

## การเติมคำสั่งอัตโนมัติใน Shell

หลังจากติดตั้ง PS Banshee แล้ว ให้เปิดใช้งานการเติมคำสั่งอัตโนมัติด้วย:

```bash
banshee --install-completion
```

รีสตาร์ท shell เพื่อให้การติดตั้งเสร็จสมบูรณ์ หลังจากนั้นสามารถใช้ TAB เพื่อเติมคำสั่งอัตโนมัติได้

## การถอนการติดตั้ง

เพื่อลบ PS Banshee ออกจากระบบ ให้ใช้คำสั่งที่เหมาะสมตามวิธีการติดตั้งที่ใช้

**หากติดตั้งด้วย pipx:**

```bash
pipx uninstall ps-banshee
```

**หากติดตั้งด้วย pip:**

```bash
pip uninstall ps-banshee
```


## ขั้นตอนถัดไป

ดูที่ [ขั้นตอนเริ่มต้น](./first-steps.md) เพื่อเริ่มใช้งาน PS Banshee