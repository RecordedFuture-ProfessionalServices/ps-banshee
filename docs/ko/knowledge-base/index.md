# Banshee CLI Knowledge Base

> Recorded Future의 터미널 기반 위협 인텔리전스 조사를 위한 CLI입니다.
> Recorded Future의 사이버 보안 엔지니어가 개발하였습니다.
> `ps-banshee` / `banshee` 버전 1.3.0을 기준으로 검증되었습니다.

이 knowledge base는 LLM(Claude Code, Opus 및 기타 에이전트형 CLI)의 활용을 위해 설계되었습니다. 에이전트를 위해 세 가지 아티팩트가 게시됩니다.

- **Index** — 간결한 목차: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms.txt>
- **Full bundle** — 모든 커맨드 그룹이 하나의 문서에 인라인 포함: <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>
- **Per-group pages** — 선택적 조회를 위한 페이지로, `https://.../latest/knowledge-base/<group>/index.md` 경로에서 원시 Markdown으로 제공됩니다(예: `ca`, `ioc`, `list`). 위의 Index에서 링크됩니다.

프로젝트에서 에이전트가 `banshee`를 인식할 수 있도록, `CLAUDE.md`, `AGENTS.md` 또는 동등한 규칙 파일에 다음과 같이 액션 형태의 문장을 추가하십시오.

> Recorded Future와 관련된 작업 시, 전체 `banshee` CLI 레퍼런스를 위해 <https://recordedfuture-professionalservices.github.io/ps-banshee/llms-full.txt>를 가져온 다음 `banshee` CLI를 사용하십시오. 해당 URL에 접근할 수 없는 경우 대신 `banshee --help`를 실행하십시오.

호출 전에 셸 환경에 `RF_TOKEN`을 설정하십시오 — 아래 [인증](#authentication-global-options)을 참조하십시오.

---

## Authentication & Global Options

```
banshee [OPTIONS] COMMAND [ARGS]...
```

| 플래그 | 단축 | 설명 |
|------|-------|-------------|
| `--api-key TEXT` | `-k` | Recorded Future API 키. 권장 사항: 대신 `RF_TOKEN` 환경 변수를 설정하십시오. |
| `--no-ssl-verify` | `-s` | SSL 검증 비활성화(`HTTP_PROXY` / `HTTPS_PROXY`를 통한 프록시 사용 시). |
| `--debug` | | 디버그 모드 활성화. |
| `--version` | | 버전 표시. |
| `--install-completion` | | 셸 탭 완성 설치. |
| `--show-completion` | | 수동 설치를 위한 완성 설정 출력. |

**권장 사항:** `RF_TOKEN=<your_api_key>`를 export하여 매 호출 시 `-k`를 전달하지 않아도 되도록 설정하십시오.

---

## Readiness Checks

워크플로를 실행하기 전에 로컬 툴체인과 인증 경로를 확인하십시오.

```bash
# CLI가 설치되어 있고 접근 가능한지 확인
banshee --version
banshee --help

# Recorded Future API 토큰이 존재하는지 확인
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# jq는 대부분의 파이프라인 예제에 필요합니다
jq --version

# 읽기 전용 API 스모크 테스트
banshee entity search wannacry -l 1
banshee ioc bulk-lookup ip 8.8.8.8 | jq '.[0] | {ioc: .entity.name, score: .risk.score}'

# pcap 워크플로에만 필요합니다. tshark 없이는 `banshee pcap enrich --help`도 실패할 수 있습니다
command -v tshark
```

`banshee`가 없는 경우, 승인된 Python 패키지 워크플로를 통해 `ps-banshee` Python 패키지를 설치한 후 위의 확인 절차를 다시 실행하십시오.

---

## Live Validation Snapshot

마지막 라이브 검증: **2026-06-12** (릴리스 1.3.0 갱신) — `ps-banshee` / `banshee` **1.3.0**, `RF_TOKEN` 인증 사용.

검증 성공:

```bash
# 로컬 툴체인 및 인증 존재 여부
banshee --version
banshee --help
test -n "$RF_TOKEN" && echo "RF_TOKEN set"

# 읽기 전용 API 접근
banshee ca rules
banshee ca rules leaked
banshee ca search -t 7d
banshee ca search -t 12h | banshee ca export
banshee ca search -t 12h | banshee ca export --csv
banshee pba search -C 60d -l 3
banshee pba search -o uhash:69sKLfTGsS -C 60d -l 3
banshee pba search -C 60d -l 3 | banshee pba export
banshee pba search -C 60d -l 3 | banshee pba export --csv
banshee ioc bulk-lookup ip 8.8.8.8
```

확인된 주의 사항:

- `ca export` 및 `pba export`는 **오직** stdin에서만 읽으며 위치 인수를 받지 않습니다. `banshee ca search` / `banshee pba search`를 파이프로 연결하여 사용하십시오.
- `pba export`는 전체 `pba search` JSON 객체(`.data[]`를 읽음)를 소비하는 반면, `ca export`는 `ca search` JSON 배열을 소비합니다.
- `ca export --csv`에서 `Updated` 컬럼은 현재 항상 비어 있습니다(향후 API 지원을 위해 예약됨) — 이번 실행에서 확인되었습니다.
- 신규 `pba search --org-id` (`-o`) 필터는 10자리 ID 또는 16자리 `uhash:` 형식을 허용하며 반복 사용이 가능합니다.
- `pcap enrich`는 `tshark`가 설치되지 않아 라이브 테스트되지 않았습니다. 이는 예상된 동작입니다: `banshee pcap enrich --help`는 `RuntimeError: tshark is not installed or not in PATH`를 발생시킵니다.

---

## Output Conventions

- 모든 커맨드는 기본적으로 **JSON 출력**을 stdout에 출력합니다 — 파이프 친화적으로 설계되었습니다.
- 사람이 읽기 쉬운 형식의 출력을 위해 임의의 커맨드에 `--pretty` / `-p`를 추가하십시오.
- 대부분의 커맨드는 stdin을 통한 파이프(개행 또는 공백으로 구분된 ID/IOC)를 지원합니다.
- 고급 필터링을 위해 `jq`와 함께 사용하십시오(예시는 전체 문서에 걸쳐 제공됩니다).
- 응답 형식은 엔드포인트마다 다릅니다. 주요 패턴은 다음과 같습니다:
  - `ioc lookup`은 JSON 배열을 반환하며, 상세 위험 증거에 `.risk.evidenceDetails[]`를 사용합니다.
  - `ioc bulk-lookup`은 JSON 배열을 반환하며, 대량 위험 증거에 `.risk.rule.evidence[]`를 사용합니다.
  - `ioc search`는 `.data.results[]` 하위에 결과를 포함하는 객체를 반환합니다.
  - `pba search`는 `.data[]` 하위에 알림 레코드를 포함하는 객체를 반환합니다.
  - `pcap enrich` 및 `email enrich`는 `.ioc`, `.risk_score`, `.rule_evidence[]` 등의 평면 레코드를 반환합니다.

---

## Command Groups

| 그룹 | 페이지 | 설명 |
|-------|------|-------------|
| `ca` | [ca.md](ca.md) | Classic Alerts — 검색, 조회, 업데이트, 내보내기 |
| `email` | [email.md](email.md) | RF 인텔리전스로 EML 파일 강화 |
| `entity` | [entity.md](entity.md) | 엔티티 검색 및 조회 |
| `ioc` | [ioc.md](ioc.md) | IOC 강화, 대량 강화, 검색, 규칙 |
| `list` | [list.md](list.md) | RF Lists 및 Watch Lists 관리(생성, 엔티티 추가/제거, 항목) |
| `pcap` | [pcap.md](pcap.md) | RF 인텔리전스로 패킷 캡처 강화 |
| `pba` | [pba.md](pba.md) | Playbook Alerts — 검색, 조회, 업데이트, 내보내기 |
| `risklist` | [risklist.md](risklist.md) | risk list(위험 목록) 조회, 생성 및 검사 |
| `rules` | [rules.md](rules.md) | 탐지 규칙 검색 및 다운로드(Sigma, YARA, Snort) |

---

## LLM을 위한 참고 사항

- **모든 ID는 불투명한 단문 문자열입니다**(예: `tybakN`, `1b0s1q`) — 절대 추측하지 말고, 항상 먼저 검색을 통해 조회하십시오.
- **PBA alert ID**는 UUID 형식을 사용하며, `pba search`(`.data[].playbook_alert_id`)에 의해 이미 `task:` 접두사가 포함된 형태로 반환됩니다. `pba lookup` 및 `pba update`에 그대로 전달하십시오 — 추가로 `task:`를 붙이지 마십시오.
- **`ca update` 및 `pba update`는 JSON이 아닌 일반 텍스트를 반환합니다** — 업데이트된 알림마다 `SUCCESS:\n<ALERT_ID>` 형식입니다. `jq`로 파이프하지 마십시오.
- **stdin 파이핑**은 모든 대량/업데이트 커맨드에서 일관되게 지원됩니다: 개행으로 구분된 ID 또는 IOC를 직접 파이프하십시오.
- **`--pretty`는 JSON이 아닙니다** — 사람이 읽기 위한 형식으로, `jq`를 통한 추가 파싱에는 적합하지 않습니다. 파이프라인에서는 사용하지 마십시오.
- **Risk rules**(위험 규칙, `ioc rules`, `risklist fetch`, `risklist create`에서 사용됨)는 `recentValidatedCnc`, `analystNote`, `recentPhishing`과 같은 명명된 문자열입니다. 사용 가능한 규칙 이름은 `banshee ioc rules <entity_type>`으로 확인하십시오.
- **엔티티 ID 대 name,type 쌍**: `list bulk-add` / `list bulk-remove`는 둘 다 허용합니다 — `SoA6SP`(RF ID), `wannacry,Malware`(이름 + 타입), 또는 `ip:8.8.8.8`(타입 접두사 값)을 사용하십시오.
- **`risklist create --fusion`**은 결과를 RF Fusion에 직접 업로드합니다. 이때 `--output-path`는 로컬 경로가 아닌 Fusion 대상 경로로 해석됩니다.
- **`ioc lookup`과 `ioc bulk-lookup`의 증거 경로는 다릅니다**: `ioc lookup`은 `.risk.evidenceDetails[]`를 사용하고, `ioc bulk-lookup`은 `.risk.rule.evidence[]`를 사용합니다. 이 둘은 서로 호환되지 않습니다.