# AI 에이전트와 함께 사용하기

Banshee는 터미널에서 실행하도록 설계되어 있으며, Claude Code, Codex 등 셸 명령을 실행할 수 있는 모든 LLM 기반 AI 코딩 에이전트에서도 사용할 수 있습니다. 에이전트가 CLI를 학습할 수 있도록 두 가지 아티팩트(artifact)가 제공됩니다:

- **인덱스** — 선택적 참조를 위한 간결한 목차: [llms.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt)
- **전체 번들** — 모든 명령 그룹을 단일 문서에 인라인으로 포함: [llms-full.txt](https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt)

두 파일 모두 [llms.txt](https://llmstxt.org/) 규약을 따릅니다.

## 에이전트가 `banshee`를 인식하도록 설정하기

아래 스니펫을 복사하여 에이전트가 읽는 규칙/지침 파일 — `CLAUDE.md`, `AGENTS.md`, 또는 해당 도구에 상응하는 파일 — 에 붙여넣으십시오:

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

## 인증

banshee를 호출하기 전에 에이전트의 셸에서 `RF_TOKEN` 환경 변수를 설정하십시오. 에이전트 워크플로우에서는 환경 변수 방식을 강력히 권장합니다 — 매번 호출 시 `-k`를 전달하지 않아도 됩니다.

전체 설정 방법(macOS, Linux, Windows)은 [설치 → 인증](installation.md#authorization)을 참조하십시오.