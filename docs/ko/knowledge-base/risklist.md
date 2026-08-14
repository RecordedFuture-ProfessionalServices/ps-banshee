# risklist

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 관련 사항은 [index.md](index.md)를 참조하십시오.

### `banshee risklist fetch`

RF에서 risk list를 다운로드하거나 로컬 사용자 정의 파일을 불러옵니다.

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--entity-type` | `-e` | 엔티티 유형: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--list-name TEXT` | `-l` | `default`, `large`, 또는 `banshee ioc rules`에서 확인 가능한 임의의 규칙 이름 |
| `--custom-list-path TEXT` | `-c` | 로컬 risk list 파일 경로 |
| `--output-path TEXT` | `-o` | 출력 경로 (기본값: 자동 생성된 이름으로 현재 작업 디렉터리에 저장) |
| `--as-json` | `-j` | 다운로드한 목록을 JSON으로 변환 (`--list-name` + `--entity-type` 조합 시에만 사용 가능) |

```bash
banshee risklist fetch -e domain -l default
banshee risklist fetch -c /custom/path/to/list.csv
banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv
```

---

### `banshee risklist create`

하나 이상의 risk rule로부터 사용자 정의 병합 risk list를 생성하며, 선택적으로 점수 필터링을 적용할 수 있습니다. 로컬에 저장하거나 RF Fusion에 업로드할 수 있습니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--entity-type` | `-e` | | 엔티티 유형: `ip`, `domain`, `url`, `hash`, `vulnerability` |
| `--risk-rule TEXT` | `-R` | | 포함할 risk rule (반복 지정 가능): `default`, `large`, 또는 `banshee ioc rules`에서 확인 가능한 임의의 규칙 이름 |
| `--risk-score INTEGER` | `-r` | | 최소 risk score 임계값 (5–99) |
| `--format` | `-f` | `csv` | 출력 형식: `csv`, `edl`, `json` |
| `--output-path TEXT` | `-o` | CWD | 출력 파일 경로 |
| `--fusion` | `-F` | | RF Fusion에 업로드 (`--output-path`를 Fusion 대상 경로로 함께 사용) |

**출력 형식:**
- `csv` — 헤더 포함 쉼표 구분 형식: `Name, Risk, RiskString, EvidenceDetails`
- `edl` — IOC 값을 한 줄에 하나씩 나열하는 일반 목록 (방화벽/EDL 피드용)
- `json` — risk list 항목의 전체 JSON 배열

```bash
banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv
banshee risklist create -e domain -R analystNote -R recentPhishing -r 80
banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl
banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json
banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv
```

---

### `banshee risklist stat`

risk list의 메타데이터(Fusion 내 존재 여부 및 현재 etag)를 표시합니다.

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--entity-type` | `-e` | 엔티티 유형 |
| `--list-name TEXT` | `-l` | 목록 이름 |
| `--custom-list-path TEXT` | `-c` | 로컬 risk list 파일 경로 |
| `--pretty` | `-p` | 보기 좋게 출력 |
| `--count` | `-C` | risk list 전체의 IOC 수 및 risk score 분포 표시 |

```bash
banshee risklist stat -e ip -l recentValidatedCnc
banshee risklist stat -e domain -l domain_risklist
banshee risklist stat -e ip -l default --count
```

**응답 구조:** 단일 JSON 객체를 반환합니다.

| 필드 | 설명 |
|-------|-------------|
| `.name` | Fusion에 저장된 risk list 이름 (예: `"recentValidatedCnc_ip_risklist"`) |
| `.exists` | `true`/`false` — RF Fusion에 해당 목록이 존재하는지 여부 |
| `.etag` | 캐시 유효성 검증용 etag 해시 문자열 |
| `.counts` | *(`--count` 사용 시에만)* 각 risk score를 해당 IOC 수에 매핑하는 객체, 예: `{"28": 261110, "65": 6531}` |

**실사용 테스트 참고:** 2026-05-01 테스트 중 `--custom-list-path /tmp/banshee_smoke_risklist.json`을 사용하면 Fusion API 조회가 시도되어 `400 Bad Request`가 반환되었습니다. Fusion 기반의 사용자 정의 경로를 검증하는 경우가 아니라면 `-e`/`-l` 옵션을 사용하는 것을 권장합니다.