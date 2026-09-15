PS Banshee อ่าน Recorded Future API key ของคุณจากตัวแปรสภาพแวดล้อม `RF_TOKEN` (แนะนำ) หรือจาก flag `-k` / `--api-key` ในแต่ละคำสั่ง

#### Option 1: ตั้งค่า `RF_TOKEN` (แนะนำ)

=== "macOS / Linux"

    เฉพาะ shell ปัจจุบันเท่านั้น:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    บันทึกสำหรับ shell ในอนาคต (zsh — ปรับเป็น `~/.bashrc` สำหรับ bash) เปิด shell ใหม่หลังจากรันคำสั่งนี้ (หรือรัน `source ~/.zshrc` เพื่อใช้งานใน shell ปัจจุบัน):

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    เฉพาะ session ปัจจุบันเท่านั้น:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    บันทึกสำหรับ session ในอนาคต (เปิด PowerShell ใหม่หลังจากรันคำสั่งนี้):

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    เฉพาะ session ปัจจุบันเท่านั้น:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    บันทึกสำหรับ session ในอนาคต (เปิด Command Prompt ใหม่หลังจากรันคำสั่งนี้):

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

#### Option 2: ส่งค่าด้วย `-k` ในแต่ละคำสั่ง

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

วิธีนี้ใช้งานได้บนทุกแพลตฟอร์ม อย่างไรก็ตาม มีความยาวมากกว่า และ key อาจถูกบันทึกไว้ใน shell history