# ioc

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee ioc lookup ENTITY_TYPE [IOC]...`

IOC별 상세 enrichment(보강). 지표 하나당 API 호출 한 번. 심층 컨텍스트 조회에 사용하십시오.

**Entity type:** `ip`, `domain`, `url`, `hash`, `vulnerability`

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--verbosity INTEGER` | `-v` | `1` | 상세 수준 1–5 (아래 verbosity 표 참조) |
| `--ai-insights` | `-a` | | AI가 생성한 risk rule 요약 포함 |
| `--pretty` | `-p` | | 보기 좋게 출력 |

**Entity type별 verbosity 수준:**

| 수준 | ip | domain | hash | url | vulnerability |
|-------|----|--------|------|-----|---------------|
| 1 | entity, risk, timestamps | entity, risk, timestamps | entity, hashAlgorithm, risk, timestamps | entity, risk, timestamps | entity, lifecycleStage, risk, timestamps |
| 2 | + intelCard, location | + intelCard | + fileHashes, intelCard | + intelCard | + intelCard |
| 3 | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links | + analystNotes, links |
| 4 | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings, threatLists | + enterpriseLists, riskMapping, sightings | + cvss, cvssv3, cvssv4, enterpriseLists, riskMapping, sightings, threatLists |
| 5 | + dnsPortCert, scanner | 4와 동일 | 4와 동일 | 4와 동일 | + cpe, cpe22uri, nvdDescription, nvdReferences |

```bash
banshee ioc lookup ip 139.224.189.177
banshee ioc lookup domain overafazg.org
banshee ioc lookup ip 8.140.135.23 -v 3
banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p

# CSV 파일에서 파이프로 입력
cat test_ips.csv | banshee ioc lookup ip -p
```

**응답 구조 (verbosity 1):** JSON 배열을 반환합니다. 각 항목에는 `entity`, `risk`, `timestamps`가 포함됩니다. 상위 verbosity 수준에서는 다음이 추가됩니다: v2 `+intelCard, location`; v3 `+analystNotes, links`; v4 `+enterpriseLists, riskMapping, sightings, threatLists`; v5 `+dnsPortCert, scanner` (ip 전용).

`.risk.evidenceDetails[]` 항목 필드:

| 필드 | 설명 |
|-------|-------------|
| `.rule` | rule 이름 문자열 |
| `.criticality` | 정수 0–4 (vulnerability의 경우 0–5) |
| `.criticalityLabel` | 사람이 읽을 수 있는 레이블 (예: `"Unusual"`, `"Malicious"`) |
| `.evidenceString` | 사람이 읽을 수 있는 증거 설명 |
| `.mitigationString` | 완화 지침 (빈 문자열일 수 있음) |
| `.timestamp` | 가장 최근 증거 타임스탬프 (ISO 8601) |

**고급 jq 활용 예시:**

```bash
# 가장 심각도가 높은 rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'

# 트리거된 모든 rule
banshee ioc lookup ip 1.2.3.4 | jq '.[].risk.evidenceDetails[].rule'

# 위험 점수 + 가장 심각도가 높은 rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | { score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] } ]'

# 위험 점수 + criticality 레이블이 포함된 모든 rule
banshee ioc lookup ip 1.2.3.4 | jq '[ .[] | { score: .risk.score, rules: [.risk.evidenceDetails[] | {rule, label: .criticalityLabel}] } ]'
```

---

### `banshee ioc bulk-lookup ENTITY_TYPE [IOC]...`

고속 대량 enrichment — API 호출 한 번당 최대 1,000개의 IOC를 배치 처리합니다. 위험 점수와 트리거된 risk rule만 반환합니다. 대용량 트리아지(triage)에 사용하십시오.

| 옵션 | 설명 |
|--------|-------------|
| `--pretty` / `-p` | 보기 좋게 출력 |

**응답 구조:** JSON 배열을 반환합니다. 각 항목에는 `entity` (`id`, `name`, `type`)와 `risk`가 포함됩니다. 참고: `ioc lookup`과 달리 `timestamps` 키가 없습니다.

`.risk` 필드:

| 필드 | 설명 |
|-------|-------------|
| `.risk.score` | 정수 위험 점수 0–99 |
| `.risk.level` | 정수 criticality 수준 |
| `.risk.context` | risk 도메인별로 그룹화된 컨텍스트 객체 (`phishing`, `public`, `c2`, `malware`) |
| `.risk.rule.count` | 트리거된 rule 수 |
| `.risk.rule.maxCount` | 최대 가능한 rule 수 |
| `.risk.rule.mostCritical` | 가장 심각도가 높은 rule 이름 |
| `.risk.rule.summary` | 요약 문자열 배열 |
| `.risk.rule.evidence[]` | 트리거된 rule 객체 배열 |

`.risk.rule.evidence[]` 항목 필드:

| 필드 | 설명 |
|-------|-------------|
| `.rule` | rule 이름 문자열 |
| `.level` | 정수 criticality 0–4 |
| `.description` | HTML 태그가 포함된 증거 문자열 (entity 참조는 `<e id=...>` 마크업 사용) |
| `.count` | 히트 횟수 |
| `.sightings` | 탐지 횟수 |
| `.timestamp` | 가장 최근 증거 타임스탬프 (ISO 8601) |
| `.mitigation` | 완화 지침 (빈 문자열일 수 있음) |
| `.type` | rule 유형 문자열 (예: `linkedIntrusion`) |

대량 조회의 risk rule 증거는 `.risk.rule.evidence[]` 아래에 있습니다. 이는 `.risk.evidenceDetails[]`를 사용하는 `ioc lookup`과 다릅니다.

```bash
banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17
banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p
banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877

# 파일에서 입력 (한 줄에 IOC 하나)
banshee ioc bulk-lookup vulnerability < cves.txt
cat cves.txt | banshee ioc bulk-lookup vulnerability

# 이름과 점수 추출
banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

# 이름, 점수 및 트리거된 rule 이름 추출
banshee ioc bulk-lookup ip 92.38.178.133 | jq '[.[] | {ioc: .entity.name, score: .risk.score, rules: [(.risk.rule.evidence // [])[].rule]}]'
```

---

### `banshee ioc search ENTITY_TYPE`

필터를 사용하여 RF IOC 코퍼스를 검색합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--limit INTEGER` | `-l` | `5` | 최대 결과 수 (1–1000) |
| `--risk-score TEXT` | `-r` | | 위험 점수 범위 (구간 표기법) |
| `--risk-rule TEXT` | `-R` | | risk rule 이름으로 필터링 |
| `--verbosity INTEGER` | `-v` | `1` | 상세 수준 1–5 (`ioc lookup`과 동일한 표) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

**위험 점수 구간 표기법:**

| 구문 | 의미 |
|--------|---------|
| `'[20,90]'` | 20 ≤ 점수 ≤ 90 |
| `'(20,90)'` | 20 < 점수 < 90 |
| `'[20,90)'` | 20 ≤ 점수 < 90 |
| `'[20,)'` | 점수 ≥ 20 |
| `'[,90)'` | 점수 < 90 |

기본 JSON 출력은 객체입니다. 검색 결과는 `.data.results[]` 아래에 있으며, 전체/반환 건수는 `.counts` 아래에 있습니다.

```bash
banshee ioc search ip -l 10 -r '(,80]'
banshee ioc search domain -r '[90,)'
banshee ioc search hash -r '[80,81]' -p
banshee ioc search vulnerability --limit 1 -v 3

# 검색 결과에서 IOC 이름 추출
banshee ioc search ip -r '[90,)' -l 100 | jq -r '.data.results[].entity.name'
```

---

### `banshee ioc rules ENTITY_TYPE`

entity type에 대한 risk rule을 나열합니다. 선택적 필터를 사용할 수 있습니다.

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--freetext TEXT` | `-F` | 이름/설명으로 rule 필터링 |
| `--mitre-code TEXT` | `-M` | MITRE ATT&CK 코드로 필터링 (예: `T1587.004`) |
| `--criticality INTEGER` | `-C` | criticality 0–5로 필터링 |
| `--pretty` | `-p` | 보기 좋게 출력 |

**Criticality 기준 (IP, Domain, URL, Hash):**

| 수준 | 레이블 | 위험 점수 범위 |
|-------|-------|----------------|
| 4 | Very Malicious | 90–99 |
| 3 | Malicious | 65–89 |
| 2 | Suspicious | 25–64 |
| 1 | Unusual | 5–24 |
| 0 | No evidence of risk | 0 |

**Criticality 기준 (Vulnerability):**

| 수준 | 레이블 | 위험 점수 범위 |
|-------|-------|----------------|
| 5 | Very Critical | 90–99 |
| 4 | Critical | 80–89 |
| 3 | High | 65–79 |
| 2 | Medium | 25–64 |
| 1 | Low | 5–24 |
| 0 | No evidence of risk | 0 |

```bash
banshee ioc rules ip
banshee ioc rules domain -p
banshee ioc rules hash -C 3
banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept
```

**응답 구조:** 단순 JSON 배열을 반환합니다. 각 항목은 하나의 risk rule을 나타냅니다:

| 필드 | 설명 |
|-------|-------------|
| `.name` | rule 이름 문자열 — `ioc search` 및 `risklist` 명령에서 `--risk-rule`과 함께 사용하는 값 (예: `"recentActiveCnc"`) |
| `.criticalityLabel` | 사람이 읽을 수 있는 레이블 (예: `"Very Malicious"`) |
| `.criticality` | 정수 criticality 수준 |
| `.description` | rule 설명 문자열 |
| `.categories[]` | `{name, framework}` 객체 배열 — MITRE ATT&CK 카테고리 (예: `{name: "TA0011", framework: "MITRE"}`) |
| `.relatedEntities[]` | 이 rule이 참조하는 RF entity ID 문자열 배열 |
| `.count` | 현재 이 rule에 해당하는 IOC 수 |

```bash
# entity type의 모든 rule 이름 나열
banshee ioc rules ip | jq -r '.[].name'

# criticality 3 이상인 rule과 해당 설명 조회
banshee ioc rules ip | jq '[.[] | select(.criticality >= 3) | {name, criticalityLabel, description}]'
```