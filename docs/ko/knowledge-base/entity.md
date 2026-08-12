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

**주요 엔터티 유형 (일부 목록):** `Malware`, `IpAddress`, `InternetDomainName`, `URL`, `Hash`, `CyberVulnerability`, `CyberThreatActorCategory`, `Organization`, `Person`, `Country`, `MitreAttackIdentifier`, `YaraDetectionRule`, `SnortDetectionRule`, `SigmaDetectionRule` (100개 이상 추가 유형 포함).

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