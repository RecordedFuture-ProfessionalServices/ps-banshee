# ca

> **Classic Alerts** - 레거시 규칙 기반 알림. ID는 6자 이상의 불투명한 짧은 문자열입니다(예: `tybakN`). 자동화/플레이북 기반 알림(선택적 `task:` 접두사가 있는 36자 UUID ID, `domain_abuse` / `third_party_risk` 등의 카테고리)은 대신 [`pba`](pba.md)를 사용하십시오.
>
> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee ca lookup ALERT_ID`

ID로 단일 Classic Alert를 조회합니다.

| 인수/옵션 | 설명 |
|-----------------|-------------|
| `ALERT_ID` (필수) | Alert ID, 예: `tybakN` |
| `--pretty` / `-p` | 보기 좋게 출력 |

```bash
banshee ca lookup tybakN
banshee ca lookup tybakN -p
```

**응답 형식:** 단일 JSON 객체를 반환합니다.

| 필드 | 설명 |
|-------|-------------|
| `.id` | Alert ID |
| `.title` | 알림 제목 |
| `.type` | 알림 유형 문자열(예: `"EVENT"`) |
| `.log.triggered` | 트리거 타임스탬프(ISO 8601) |
| `.review.status_in_portal` | 사람이 읽을 수 있는 상태: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.assignee` | 담당 분석가 이메일 |
| `.rule.id` | 알림 규칙 ID |
| `.rule.name` | 알림 규칙 이름 |
| `.url.portal` | RF 포털의 알림 직접 링크 |
| `.ai_insights.text` | RF AI가 생성한 요약 문자열 |
| `.hits[]` | 알림을 트리거한 문서 |
| `.hits[].id` | 히트 문서 ID |
| `.hits[].fragment` | 일치한 텍스트 스니펫 |
| `.hits[].language` | 언어 코드(예: `"eng"`) |
| `.hits[].entities[]` | 히트에서 발견된 엔티티: `{id, name, type}` |
| `.hits[].document.title` | 소스 문서 제목 |
| `.hits[].document.url` | 소스 문서 URL |
| `.hits[].document.source` | 소스 이름 문자열 |
| `.hits[].document.authors` | 작성자 문자열 배열(비어 있을 수 있음) |
| `.triggered_by[]` | 알림을 트리거한 엔티티/규칙(비어 있을 수 있음) |
| `.triggered_by[].reference_id` | 참조 문서 ID |
| `.triggered_by[].triggered_by_strings[]` | 사람이 읽을 수 있는 트리거 설명 |
| `.enriched_entities[]` | RF 컨텍스트가 포함된 사전 강화된 엔티티 객체(비어 있을 수 있음) |

```bash
# Extract all entities from alert hits for enrichment
banshee ca lookup tybakN | jq '[.hits[].entities[] | {id, name, type}] | unique_by(.id)'

# Get the AI summary
banshee ca lookup tybakN | jq -r '.ai_insights.text'

# Get portal link
banshee ca lookup tybakN | jq -r '.url.portal'
```

---

### `banshee ca search`

선택적 필터를 사용하여 Classic Alerts를 검색합니다.

| 옵션 | 단축키 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--triggered TEXT` | `-t` | `1d` | 시간 범위. 상대적(`1d`, `12h`) 또는 절대 구간(`[2024-08-01, 2024-08-14]`). |
| `--rule TEXT` | `-r` | | 알림 규칙 이름으로 필터링(자유 텍스트, 반복 가능). |
| `--status` | `-s` | | 다음 중 하나: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--pretty` | `-p` | | 보기 좋게 출력 |

```bash
banshee ca search -t 1d
banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending
banshee ca search -t 12h -p
banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d
banshee ca search -r leaked -t 12h -p
```

**응답 형식:** JSON 배열을 반환합니다. 각 알림 객체에는 다음과 같은 최상위 필드가 있습니다.

| 필드 | 설명 |
|-------|-------------|
| `.id` | Alert ID(예: `tybakN`) |
| `.title` | 알림 제목 |
| `.log.triggered` | 트리거 타임스탬프(ISO 8601) |
| `.review.status_in_portal` | 사람이 읽을 수 있는 상태: `New`, `Pending`, `Dismissed`, `Resolved` |
| `.review.status` | 내부 상태 문자열(`no-action` 등) — jq 필터링에는 유용하지 않음 |
| `.rule.name` | 실행된 알림 규칙 이름 |
| `.rule.id` | 알림 규칙 ID |

**참고:** `ca search` 알림 레코드에는 최상위 `priority` 필드가 없습니다. jq 파이프라인에서 상태로 필터링할 때는 `.review.status`가 아닌 `.review.status_in_portal`을 사용하십시오.

```bash
# Extract IDs of New alerts (use status_in_portal for jq filtering)
banshee ca search -t 1d | jq -r '.[] | select(.review.status_in_portal == "New") | .id'

# When using the -s flag, status filtering happens server-side — no jq select needed
banshee ca search -t 1d -s New | jq -r '.[].id'
```

---

### `banshee ca rules [FREETEXT]`

모든 Classic Alert 규칙을 나열하며, 선택적으로 자유 텍스트로 필터링합니다.

| 인수/옵션 | 설명 |
|-----------------|-------------|
| `FREETEXT` (선택사항) | 규칙 이름을 필터링할 검색어 |
| `--pretty` / `-p` | 보기 좋게 출력 |

```bash
banshee ca rules
banshee ca rules -p
```

**응답 형식:** 평면 JSON 배열을 반환합니다. 각 항목에는 다음 필드가 있습니다.

| 필드 | 설명 |
|-------|-------------|
| `.id` | 규칙 ID(예: `k_TnPe`) |
| `.title` | 규칙 이름 |
| `.enabled` | `true`/`false` — 규칙 활성화 여부 |
| `.priority` | `true` = 이 규칙의 알림 심각도는 **High**; `false` = 심각도 **Informational**. 우선순위별로 분류하려면 먼저 규칙을 가져온 후 `.rule.id`를 통해 알림과 조인하십시오(아래 우선순위 분류 워크플로 참조). |
| `.tags` | 태그 문자열 배열 |
| `.created` | 생성 타임스탬프(ISO 8601) |
| `.owner` | `id`와 `name`이 있는 객체 — 규칙 소유자 |
| `.intelligence_goals` | `{id, name}` 객체 배열 — 연관된 인텔리전스 목표 |
| `.notification_settings` | `email_subscribers` 배열이 있는 객체 |

파이프라인 구성 시 `.title`과 `.id`를 사용하십시오. `.priority`는 알림 심각도에 직접 매핑됩니다: `true`는 High, `false`는 Informational입니다.

---

### 우선순위 분류 워크플로

`ca search`와 `ca lookup`은 알림별 심각도 필드를 반환하지 않습니다. 심각도별로 알림을 분류하려면 먼저 규칙 목록을 가져오고, `.priority == true`인 규칙으로 필터링한 후, 알림 `.rule.id` 값과 교차하십시오.

```bash
# High-priority alert IDs in the last day
PRIORITY_RULES=$(banshee ca rules | jq -r '.[] | select(.priority == true) | .id' | paste -sd'|' -)
banshee ca search -t 1d | jq --arg rules "$PRIORITY_RULES" -r '.[] | select(.rule.id | test("^(" + $rules + ")$")) | .id'
```

결과 ID를 `banshee ca update`에 바로 파이프하여 높은 우선순위 알림만 상태를 변경하십시오.

---

### `banshee ca update [ALERT_IDS]...`

하나 이상의 Classic Alerts를 업데이트합니다. ID는 인수로 전달하거나, 공백으로 구분하거나, stdin을 통해 파이프할 수 있습니다.

| 옵션 | 단축키 | 설명 |
|--------|-------|-------------|
| `--status` | `-s` | 새 상태: `New`, `Pending`, `Dismissed`, `Resolved` |
| `--note TEXT` | `-n` | 텍스트 노트 추가 |
| `--append` | `-A` | 덮어쓰는 대신 기존 노트에 추가 |
| `--assignee TEXT` | `-a` | 알림 재할당. `uhash:3aXZxdkM12` 또는 `analyst@acme.com` 허용 |

**입력 방법:**

```bash
# Single ID
banshee ca update 8cORlQ -s Resolved

# Multiple IDs (space-separated)
banshee ca update 8cORlQ 8biCIG -s Pending

# Pipe IDs from file
cat alerts.txt | banshee ca update -s Dismissed

# Pipe from search via jq
banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"

# stdin redirect
banshee ca update -s Dismissed < alerts.txt
```

**응답:** JSON이 아닌 일반 텍스트를 반환합니다 — 업데이트된 알림마다 한 줄: `SUCCESS:\n<ALERT_ID>`. `jq`로 파이프하지 마십시오.

---

### `banshee ca export`

`ca search`로 생성된 알림의 전체 알림 세부 정보를 가져와 JSON 또는 CSV로 출력합니다. 입력은 **stdin 전용**입니다 — `banshee ca search`의 JSON 배열을 파이프하십시오. 위치 인수는 없습니다.

| 옵션 | 단축키 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--csv` | | JSON | JSON(전체 알림 세부 정보) 대신 CSV(고정 열 세트)로 출력합니다. |

```bash
banshee ca search -t 1d | banshee ca export
banshee ca search -t 1d -r "Leaked Credential Monitoring" | banshee ca export > credential_alerts.json
banshee ca search -t 12h -s Pending | banshee ca export --csv > alerts.csv
```

**입력:** stdin에서 `banshee ca search`가 출력하는 JSON 배열을 기대하며, 모든 요소에 `id`가 있어야 합니다. 파이프된 입력 없이(TTY에서) 실행하면 `BadParameter` 오류가 발생합니다.

**응답 형식(기본값):** 전체 알림 객체의 JSON 배열 — `banshee ca lookup`이 반환하는 것과 동일한 알림별 구조(`.id`, `.title`, `.log.triggered`, `.review`, `.rule`, `.hits[]` 등).

**응답 형식(`--csv`):** 헤더 행과 다음 고정 열이 있는 CSV: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Title`, `Assignee`, `URL`, `Entities`, `Recorded Future AI Insights`. `Priority`는 알림 규칙에서 파생됩니다(규칙이 우선순위 규칙이면 `High`, 그렇지 않으면 `Informational`). 필드 값 내의 쉼표는 공백으로 대체됩니다.