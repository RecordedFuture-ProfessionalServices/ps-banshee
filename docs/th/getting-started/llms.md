# การใช้งานร่วมกับ AI agents

Banshee ได้รับการออกแบบให้สามารถสั่งงานจาก terminal — รวมถึงโดย AI coding agents เช่น Claude Code, Codex และ LLM อื่น ๆ ที่สามารถรันคำสั่ง shell ได้ มีเอกสารสองรายการที่เผยแพร่เพื่อช่วยให้ agent เรียนรู้ CLI:

- **Index** — สารบัญแบบกระชับสำหรับการดึงข้อมูลเฉพาะส่วน: [llms.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt)
- **Full bundle** — ทุก command group รวมอยู่ในเอกสารเดียว: [llms-full.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt)

ทั้งสองรายการเป็นไปตามแนวทาง [llms.txt](https://llmstxt.org/)

## ทำให้ `banshee` เป็นที่รู้จักแก่ agent ของคุณ

คัดลอก snippet ด้านล่างและวางลงในไฟล์ rules/instructions ที่ agent ของคุณอ่าน — `CLAUDE.md`, `AGENTS.md` หรือไฟล์ที่เทียบเท่าสำหรับเครื่องมือที่คุณใช้:

```markdown
## Recorded Future (banshee CLI)

When a request involves Recorded Future or threat intelligence, use the
`banshee` CLI. This covers, for example:

- checking or enriching the risk of an IOC (IP, domain, URL, file hash, or CVE)
- looking up or searching for entities
- triaging Classic or Playbook alerts
- managing RF lists and watchlists
- fetching or building risk lists
- finding or downloading detection rules (Sigma, YARA, Snort)
- enriching an email (`.eml`) or packet capture (`.pcap`)

First fetch the full command reference, then run `banshee`:
<https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>

If that URL is unreachable, or a command from the reference isn't present in your
installed version, run `banshee --help` (and `banshee <group> --help`) to confirm
the commands your binary actually supports.
```

## การอนุญาตสิทธิ์

ตั้งค่าตัวแปรสภาพแวดล้อม `RF_TOKEN` ใน shell ของ agent ก่อนเรียกใช้งาน banshee วิธีการผ่าน env-var เป็นที่แนะนำอย่างยิ่งสำหรับ agent workflows — agent ไม่จำเป็นต้องจดจำการส่ง `-k` ในทุกครั้งที่เรียกใช้

ดู [Installation → Authorization](installation.md#authorization) สำหรับคำแนะนำการตั้งค่าแบบสมบูรณ์ (macOS, Linux, Windows)