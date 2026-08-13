# rules

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee rules search`

Recorded Future에서 Sigma, YARA, Snort 탐지 규칙을 검색하고 다운로드합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--type` | `-t` | | 규칙 유형 (반복 가능, OR 논리): `sigma`, `yara`, `snort` |
| `--threat-actor-map` | `-T` | | Threat Actor Map에 등록된 위협 행위자로 필터링 |
| `--threat-actor-category` | `-C` | | 위협 행위자 카테고리로 필터링 (반복 가능, OR 논리). 카테고리에는 국가 지원 그룹, 랜섬웨어 그룹, 핵티비스트, 금전적 동기를 가진 행위자 등이 포함됩니다. |
| `--threat-malware-map` | `-M` | | Malware Threat Map에 등록된 악성코드로 필터링 |
| `--org-id TEXT` | `-O` | | MSSP/다중 조직 계정의 조직 ID (threat map과 함께 사용) |
| `--entity TEXT` | `-e` | | RF 엔티티 ID로 필터링 (반복 가능, OR 논리). ID 검색에는 `banshee entity search`를 사용하십시오. MITRE 코드도 허용됩니다 (예: `mitre:T1486`). |
| `--created-after TEXT` | `-a` | | 상대적 (`1d`, `7d`) 또는 절대적 (`2024-01-01`) 날짜 |
| `--created-before TEXT` | `-b` | | 상대적 또는 절대적 날짜 |
| `--updated-after TEXT` | `-u` | | 상대적 또는 절대적 날짜 |
| `--updated-before TEXT` | `-U` | | 상대적 또는 절대적 날짜 |
| `--id TEXT` | `-i` | | Insikt Note 문서 ID로 필터링 (예: `doc:lmRPGB`) |
| `--title TEXT` | `-n` | | 연관된 Insikt Note 제목에 대한 자유 텍스트 검색 |
| `--limit INTEGER` | `-l` | `10` | 최대 결과 수 (1–1000) |
| `--output-path TEXT` | `-o` | | 규칙을 디렉터리에 저장 (생략 시 콘솔에 출력) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

```bash
banshee rules search -t yara -t snort -l 20 -a 3d
banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE
banshee rules search --id doc:0uTafk
banshee rules search --title Ransomware -p
banshee rules search -t yara --output-path .
banshee rules search --threat-actor-map -o fetched_rules
```

**응답 형식:** `--output-path`를 사용하지 않을 경우 단순 JSON 배열을 반환합니다. 각 항목은 연관된 탐지 규칙이 포함된 Insikt Note를 나타냅니다.

| 필드 | 설명 |
|-------|-------------|
| `.id` | Insikt Note 문서 ID (예: `doc:o6_lui`) |
| `.type` | 규칙 유형: `sigma`, `yara`, 또는 `snort` |
| `.title` | Insikt Note 제목 |
| `.description` | Insikt Note 전체 설명 텍스트 |
| `.created` | Note 생성 타임스탬프 (ISO 8601) |
| `.updated` | Note 마지막 업데이트 타임스탬프 (ISO 8601) |
| `.rules[]` | 규칙 객체 배열 — 하나의 Note에 여러 규칙이 포함될 수 있습니다 |

`.rules[]` 항목 필드:

| 필드 | 설명 |
|-------|-------------|
| `.content` | 원시 규칙 텍스트 (Sigma의 경우 YAML, YARA/Snort의 경우 일반 텍스트) |
| `.file_name` | 규칙 저장 시 제안되는 파일명 |
| `.entities[]` | 규칙에서 참조하는 엔티티: `{id, name, type}` (`display_name` 포함 가능) |

```bash
# 최근 7일간의 모든 sigma 규칙 제목과 파일명 목록 출력
banshee rules search -t sigma -l 50 -a 7d | jq '[.[] | {title, file: .rules[0].file_name}]'

# 규칙에서 참조하는 모든 MITRE ATT&CK ID 추출
banshee rules search -t sigma -l 20 | jq '[.[].rules[].entities[] | select(.type == "MitreAttackIdentifier") | .name] | unique'

# 원시 Sigma 규칙 내용 출력
banshee rules search --id doc:0uTafk | jq -r '.[0].rules[0].content'
```