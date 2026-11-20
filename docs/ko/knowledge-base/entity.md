# entity

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee entity lookup ENTITY_ID`

ID로 Recorded Future 엔터티를 조회합니다.

| 인수/옵션 | 설명 |
|-----------------|-------------|
| `ENTITY_ID` (필수) | RF 엔터티 ID, 예: `qf0H03` |
| `--pretty` / `-p` | 보기 좋게 출력 |

```bash
banshee entity lookup qf0H03
banshee entity lookup qf0H03 -p
```

**응답 형태:** 최상위 키 `id`, `type`, `attributes`를 포함하는 단일 JSON 객체를 반환합니다. 엔터티 이름은 최상위 레벨이 아닌 `.attributes.name` 아래에 중첩되어 있습니다.

```bash
# Correct jq to extract id, type, and name:
banshee entity lookup qf0H03 | jq '{id, type, name: .attributes.name}'
```

---

### `banshee entity search NAME`

이름으로 엔터티를 검색하며, 선택적으로 유형별로 필터링할 수 있습니다.

| 인수/옵션 | 단축 | 기본값 | 설명 |
|-----------------|-------|---------|-------------|
| `NAME` (필수) | | | 검색할 엔터티 이름 |
| `--type` | `-t` | | 하나 이상의 엔터티 유형 (반복 가능). 아래의 전체 유형 목록을 참조하십시오. |
| `--limit INTEGER` | `-l` | `100` | 최대 결과 수 (1–100) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

**주요 엔터티 유형 (일부 목록):** `Malware`, `IpAddress`, `InternetDomainName`, `URL`, `Hash`, `CyberVulnerability`, `CyberThreatActorCategory`, `Organization`, `Person`, `Country`, `MitreAttackIdentifier`, `YaraDetectionRule`, `SnortDetectionRule`, `SigmaDetectionRule` (100개 이상의 추가 유형 포함).

```bash
banshee entity search wannacry
banshee entity search "Cobalt Strike" -p
banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20
```

**응답 형태:** 평면 JSON 배열을 반환합니다. 각 항목은 정확히 세 개의 필드를 포함합니다:

| 필드 | 설명 |
|-------|-------------|
| `.id` | RF 엔터티 ID (예: `SoA6SP`) |
| `.name` | 엔터티 표시 이름 |
| `.type` | 엔터티 유형 문자열 (예: `Malware`, `InternetDomainName`) |

```bash
# Extract all IDs matching a name
banshee entity search "Cobalt Strike" -t Malware | jq -r '.[].id'

# Build a lookup table of id → name
banshee entity search wannacry | jq '[.[] | {(.id): .name}] | add'
```


---

### `banshee entity links ENTITY_ID...`

하나 이상의 엔터티에 연결된 엔터티(IOC(침해 지표), 탐지 룰, 멀웨어, TTP(전술·기술·절차), 위협 행위자)를 가져옵니다. 엔터티 ID는 엔터티 이름이 아닌 Recorded Future 엔터티 ID(예: `banshee entity search`에서 얻은 값)여야 합니다. 연결된 IOC는 `--skip-enrichment`가 설정되지 않은 경우 SOAR를 통해 보강됩니다.

엔터티 ID는 공백으로 구분된 인수로 전달하거나, stdin을 통해 파이프 또는 리디렉션으로 입력할 수 있습니다(한 줄에 하나씩). 서브커맨드 단어(예: `links search`)는 추가하지 마십시오. 해당 서브커맨드는 존재하지 않으며, 추가로 입력된 단어는 엔터티 ID로 처리됩니다.

| 인수/옵션 | 단축 | 기본값 | 설명 |
|-----------------|-------|---------|-------------|
| `ENTITY_ID...` | | stdin | 하나 이상의 엔터티 ID |
| `--type TEXT` | `-t` | | 반환할 엔터티 유형. 반복 가능 |
| `--source [Technical\|Insikt]` | `-s` | | 반환할 링크의 출처 |
| `--sections TEXT` | `-S` | | 링크 유형별 필터, 예: `'Indicators and Detection Rules'`. 반복 가능 |
| `--timeframe TEXT` | `-T` | | 링크가 생성된 기간, 예: `-1d` (최대 `-90d`) |
| `--events TEXT` | `-e` | | 이벤트 유형별 필터, 예: `type:MalwareAnalysis`. 반복 가능 |
| `--connected-entities TEXT` | `-c` | | 해당 엔터티에도 연결된 엔터티만 반환. 반복 가능 |
| `--limit INTEGER` | `-l` | | 유형별 최대 반환 엔터티 수 (1–1,000,000) |
| `--small` | | | 이벤트 유형별로 참조 10건 및 Insikt Note 10건 검색 |
| `--large` | | | 이벤트 유형별로 참조 100건 및 Insikt Note 500건 검색 |
| `--skip-enrichment` | | | 연결된 IOC의 추가 보강 건너뜀 |
| `--pretty` | `-p` | | 보기 좋게 출력 |

`--small`과 `--large`는 상호 배타적이며, 둘 다 지정하지 않으면 중간 범위가 사용됩니다.

**응답 형태:** 입력 엔터티당 하나의 객체를 포함하는 JSON 배열을 반환합니다. 각 객체에는 검색된 `entity`와 해당 `links`가 포함됩니다. 각 링크에는 연결된 IOC에 대한 SOAR 보강 결과를 담는 `enrichment` 필드가 포함되며, IOC가 아닌 링크, 보강되지 않은 IOC, 또는 `--skip-enrichment` 사용 시에는 `null`이 설정됩니다. SOAR 보강에 실패한 경우 stderr에 메시지가 출력되고 보강은 건너뜁니다.

보기 좋게 출력(pretty output)할 경우(stderr에 출력), 엔터티별로 연결된 IOC(위험 점수, 주요 위험 규칙 및 인텔리전스 카드 링크 포함), TTP, 멀웨어, 위협 행위자의 테이블이 표시되며, 각 테이블은 최대 20행으로 제한됩니다. pretty 모드에서의 IOC 보강 역시 유형별 최대 20개의 IOC로 제한됩니다.

```bash
banshee entity links BUl6R5r
banshee entity links BUl6R5r -T -10d --small -p
banshee entity links BUl6R5r sIG7Rn -T -10d --large > links.json

# Skip enrichment for faster results
banshee entity links BUl6R5r --skip-enrichment

# Entity IDs from a file or pipe
banshee entity links -T -1d < link_entities.txt
cat link_entities.txt | banshee entity links -T -1d --large > links_out.json

# Find an entity ID first, then search its links
banshee entity search wannacry -t Malware -l 1 | jq -r '.[].id' | banshee entity links --small
```