# pba

> **Playbook Alerts** - 자동화 기반 알림입니다. ID는 36자 UUID이며 `task:` 접두사는 선택 사항입니다(예: `d144a9ec-90e6-40fe-89b0-d85ed65d3e9c` 또는 `task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c`). PBA 전용 카테고리: `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report`. 레거시 규칙 기반 알림(짧은 불투명 ID)의 경우 [`ca`](ca.md)를 사용하십시오.
>
> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee pba search`

다양한 필터 옵션으로 Playbook Alerts를 검색합니다.

| 옵션 | 단축 옵션 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--created TEXT` | `-C` | | 생성 날짜로 필터링 (예: `1d`, `7d`) |
| `--updated TEXT` | `-u` | | 업데이트 날짜로 필터링 |
| `--category` | `-c` | 전체 | 하나 이상의 카테고리 (반복 가능): `domain_abuse`, `cyber_vulnerability`, `third_party_risk`, `code_repo_leakage`, `identity_novel_exposures`, `geopolitics_facility`, `malware_report` |
| `--entity TEXT` | `-e` | | 연관된 엔터티로 필터링 (반복 가능) |
| `--priority` | `-P` | 전체 | `Informational`, `Moderate`, `High` (반복 가능) |
| `--status` | `-s` | 전체 | `New`, `InProgress`, `Dismissed`, `Resolved` (반복 가능) |
| `--org-id TEXT` | `-o` | 전체 | 소유 조직 ID로 필터링 (반복 가능). 10자 ID 또는 16자 `uhash:` 형식 허용 |
| `--limit INTEGER` | `-l` | `100` | 최대 결과 수 (1–10000) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

**응답 구조:** 세 개의 최상위 키를 가진 JSON 객체를 반환합니다. `.data` (알림 레코드 배열), `.counts` (`{returned, total}`), `.status` (요청 상태 객체: `{status_code, status_message}`). 알림 레코드는 `.data[]` 하위에 위치하며 다음 필드를 포함합니다: `playbook_alert_id`, `alert_rule` (`{id, label, name}`), `category`, `priority`, `status`, `title`, `created`, `updated`, `actions_taken`, `owner_organisation_details`.

```bash
banshee pba search --created 1d
banshee pba search -C 1d -u 1d -p
banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse
banshee pba search --updated 7d --category domain_abuse --pretty
banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New
banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d
banshee pba search -o 69sKLfTGsS -o uhash:5zQaSyRpA1 -C 7d -P High
```

---

### `banshee pba lookup ALERT_ID`

ID로 단일 Playbook Alert를 조회합니다. `task:` 접두사가 있거나 없는 36자 UUID를 허용하며, CLI는 접두사 없는 UUID에 자동으로 `task:`를 추가합니다.

```bash
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup d144a9ec-90e6-40fe-89b0-d85ed65d3e9c
banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p
```

**응답 구조:** 네 개의 최상위 키를 가진 단일 JSON 객체를 반환합니다: `playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`.

**`.panel_status`** — 알림 메타데이터 및 현재 처리 상태:

| 필드 | 설명 |
|-------|-------------|
| `.panel_status.status` | 현재 상태: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `.panel_status.priority` | 우선순위: `Informational`, `Moderate`, `High` |
| `.panel_status.case_rule_label` | 사람이 읽을 수 있는 규칙 이름 (예: `"Data Leakage on Code Repository"`) |
| `.panel_status.entity_id` | 주요 대상의 RF 엔터티 ID (예: `"url:https://..."`) |
| `.panel_status.entity_name` | 주요 엔터티 이름 |
| `.panel_status.risk_score` | RF 위험 점수 정수값 |
| `.panel_status.targets[]` | `{name}` 객체의 배열 — 대상이 되거나 영향을 받은 엔터티 |
| `.panel_status.actions_taken[]` | 알림에 이미 기록된 조치 |
| `.panel_status.created` | 생성 타임스탬프 (ISO 8601) |
| `.panel_status.updated` | 마지막 업데이트 타임스탬프 (ISO 8601) |

**`.panel_evidence_summary`** — 증거 세부 정보. 구조는 알림 카테고리에 따라 다릅니다. `code_repo_leakage`의 경우:

| 필드 | 설명 |
|-------|-------------|
| `.panel_evidence_summary.repository.name` | 저장소 URL |
| `.panel_evidence_summary.repository.owner.name` | 저장소 소유자 로그인 |
| `.panel_evidence_summary.evidence[]` | 증거 항목 배열 |
| `.panel_evidence_summary.evidence[].url` | 노출된 콘텐츠의 소스 URL |
| `.panel_evidence_summary.evidence[].content` | 노출된 콘텐츠의 발췌문 |
| `.panel_evidence_summary.evidence[].assessments[]` | 평가 객체: `{id, title, value}` |
| `.panel_evidence_summary.evidence[].targets[]` | 대상 엔터티: `{name}` |
| `.panel_evidence_summary.evidence[].published` | 게시 타임스탬프 |

```bash
# 요약: 엔터티, 규칙, 상태
banshee pba lookup task:<ID> | jq '{entity: .panel_status.entity_name, rule: .panel_status.case_rule_label, status: .panel_status.status, priority: .panel_status.priority}'

# 증거 URL 추출 (code_repo_leakage)
banshee pba lookup task:<ID> | jq '[.panel_evidence_summary.evidence[].url]'
```

---

### `banshee pba update [ALERT_IDS]...`

하나 이상의 Playbook Alerts를 업데이트합니다. ID는 `task:` 접두사 또는 접두사 없는 UUID를 허용합니다. 파이프 입력이 가능합니다.

| 옵션 | 단축 옵션 | 설명 |
|--------|-------|-------------|
| `--status` | `-s` | 새 상태: `New`, `InProgress`, `Dismissed`, `Resolved` |
| `--reopen` | `-r` | 재열기 전략 (Dismissed/Resolved 전용): `Never`, `SignificantUpdates` |
| `--priority` | `-p` | 새 우선순위: `Informational`, `Moderate`, `High` |
| `--comment TEXT` | `-t` | 댓글 추가 |
| `--assignee TEXT` | `-a` | 담당자 재지정 (`uhash:3aXZxdkM12` 형식 허용) |

**유효한 status/reopen 조합:** `Dismissed → Never`, `Resolved → Never`, `Resolved → SignificantUpdates`

```bash
# 단일 업데이트
banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

# 여러 ID
banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

# 검색 결과를 파이프로 전달
banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

# 파일에서 입력
banshee pba update -s Dismissed < alerts.txt
cat alerts.txt | banshee pba update -s Dismissed

# 전체 예시
banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."
```

**응답:** JSON이 아닌 일반 텍스트를 반환합니다. 업데이트된 알림마다 한 줄씩 출력됩니다: `SUCCESS:\n<ALERT_ID>`. `jq`로 파이프하지 마십시오.

---

### `banshee pba export`

`pba search`가 반환한 알림의 전체 세부 정보를 가져와 JSON 또는 CSV 형식으로 출력합니다. 입력은 **표준 입력(stdin)만** 허용합니다. `banshee pba search`의 JSON 객체를 파이프로 전달하십시오. 위치 인수는 없습니다.

| 옵션 | 단축 옵션 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--csv` | | JSON | JSON(전체 알림 세부 정보) 대신 CSV(고정 컬럼 세트)로 출력합니다. |

```bash
banshee pba search --created 1d -l 10 | banshee pba export > alerts.json
banshee pba search --updated 7d --category identity_novel_exposures | banshee pba export --csv > identity_alerts.csv
```

**입력:** 표준 입력으로 `banshee pba search`가 출력한 JSON 객체를 기대합니다. export는 `.data[]`를 읽으며 각 레코드에서 `playbook_alert_id`와 `category`를 필요로 합니다(이 값이 카테고리별 조회를 결정합니다). 파이프 입력 없이 실행하면(TTY) `BadParameter` 오류가 발생합니다.

**응답 구조 (기본값):** 전체 Playbook Alert 객체의 JSON 배열 — `banshee pba lookup`이 반환하는 것과 동일한 알림별 구조입니다(`playbook_alert_id`, `panel_status`, `panel_evidence_summary`, `panel_log_v2`).

**응답 구조 (`--csv`):** 헤더 행과 다음 고정 컬럼으로 구성된 CSV입니다: `ID`, `Priority`, `Alert Rule`, `Status`, `Created`, `Updated`, `Subject`, `Assignee`, `Assessments`, `Entities`, `Reopen Strategy`, `Onwards Actions`. `Assessments`와 `Entities`는 `; `로 구분되며, 필드 값 내의 쉼표는 공백으로 대체됩니다.