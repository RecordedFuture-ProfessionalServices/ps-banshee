# list

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee list create NAME [LIST_TYPE]`

새 목록을 생성합니다.

| 인수/옵션 | 기본값 | 설명 |
|-----------------|---------|-------------|
| `NAME` (필수) | | 목록 이름 |
| `LIST_TYPE` | `entity` | 다음 중 하나: `entity`, `source`, `text` |
| `--pretty` / `-p` | | 보기 좋게 출력 |

```bash
banshee list create coolbeans
banshee list create coolsources source -p
```

---

### `banshee list search [NAME]`

이름 및/또는 유형으로 목록을 검색합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `NAME` (선택) | | | 목록 이름으로 필터링 |
| `--list-type` | `-t` | | 다음 중 하나: `entity`, `source`, `text`, `custom`, `ip`, `domain`, `tech_stack`, `industry`, `brand`, `partner`, `industry_peer`, `location`, `supplier`, `vulnerability`, `company`, `hash`, `operation`, `attacker`, `target`, `method`, `executive` |
| `--limit INTEGER` | `-l` | `1000` | 최대 결과 수 (1–3000) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

```bash
banshee list search -l 1500 -p
banshee list search -t vulnerability
banshee list search Attacker
banshee list search ernest -t entity -p -l 3
```

**응답 형식:** 단순 JSON 배열을 반환합니다. 각 항목은 다음 필드를 포함합니다:

| 필드 | 설명 |
|-------|-------------|
| `.id` | 목록 ID (예: `report:-19oM7`) |
| `.name` | 목록 이름 |
| `.type` | 목록 유형: `entity`, `source`, `text` 등 |
| `.created` | 생성 타임스탬프 (ISO 8601) |
| `.updated` | 마지막 업데이트 타임스탬프 (ISO 8601) |
| `.owner_id` | 소유자 uhash ID |
| `.owner_name` | 소유자 표시 이름 |
| `.owner_organisation_details` | 조직 소유 정보 |

---

### `banshee list info LIST_ID`

목록에 대한 메타데이터를 가져옵니다.

```bash
banshee list info 1b0tFN
banshee list info 1b0tFN -p
```

**응답 형식:** 단일 JSON 객체를 반환합니다. `list search` 항목과 동일한 필드 집합으로 구성됩니다: `id`, `name`, `type`, `created`, `updated`, `owner_id`, `owner_name`, `organisation_id`, `organisation_name`, `owner_organisation_details`.

---

### `banshee list status LIST_ID`

목록의 처리/동기화 상태를 가져옵니다.

```bash
banshee list status 1b0tFN
```

**응답 형식:** 두 개의 필드를 포함하는 단일 JSON 객체를 반환합니다:

| 필드 | 설명 |
|-------|-------------|
| `.status` | 처리 상태 문자열 (예: `"ready"`) |
| `.size` | 현재 목록에 있는 엔티티 수 |

---

### `banshee list entities LIST_ID`

현재 목록에 있는 모든 엔티티를 가져옵니다.

```bash
banshee list entities 1b0s1q
```

**응답 형식:** 단순 JSON 배열을 반환합니다. 각 항목은 다음 필드를 포함합니다:

| 필드 | 설명 |
|-------|-------------|
| `.entity.id` | RF 엔티티 ID |
| `.entity.name` | 엔티티 표시 이름 |
| `.entity.type` | 엔티티 유형 문자열 |
| `.status` | 목록에서의 엔티티 상태 (예: `"ready"`) |
| `.added` | 엔티티가 추가된 타임스탬프 (ISO 8601) |

```bash
# Extract all entity IDs on a list
banshee list entities report:6P8708 | jq -r '.[].entity.id'

# Get entity names and types
banshee list entities report:6P8708 | jq '[.[] | {name: .entity.name, type: .entity.type}]'
```

---

### `banshee list entries LIST_ID`

목록에서 텍스트 매칭 항목을 가져옵니다 (`text` 유형 목록에 해당).

```bash
banshee list entries 1b0s1q
```

---

### `banshee list add LIST_ID ENTITY_ID [PROPERTIES]`

목록에 단일 엔티티를 추가합니다.

| 인수 | 설명 |
|----------|-------------|
| `LIST_ID` (필수) | 목록 ID |
| `ENTITY_ID` (필수) | RF 엔티티 ID (예: `SoA6SP`) 또는 `name,type` 쌍 (예: `wannacry,Malware`) |
| `PROPERTIES` (선택) | `annotation=<text>`를 사용하여 Recorded Future 플랫폼에서 해당 엔티티에 표시되는 메모를 첨부합니다. 값에 공백이 포함된 경우 따옴표로 묶으십시오. |

```bash
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
```

---

### `banshee list bulk-add LIST_ID [ENTITY_INPUT]...`

목록에 여러 엔티티를 추가합니다. 엔티티 ID, `name,type` 쌍, 또는 `type:value` 쌍을 허용합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | 꺼짐 | 덮어쓰기 모드: 입력에 있는 엔티티는 유지하고 새 엔티티를 추가하며, 입력에 **없는** 엔티티는 목록에서 제거합니다. 이 옵션 없이는 새 엔티티만 추가되며 기존 엔티티는 제거되지 않습니다. |

**입력 형식:**
- RF 엔티티 ID: `SoA6SP`
- 이름 + 유형: `wannacry,Malware` 또는 `www.duckdns.org,InternetDomainName`
- 유형 접두사 값: `ip:8.8.8.8`

```bash
banshee list bulk-add report:21YKUC SoA6SP lYNvCK
banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# Overwrite mode: make the list match exactly the entities supplied (adds missing, removes stale)
banshee list bulk-add 21YKUC SoA6SP lYNvCK --overwrite

# From file (one entity per line)
banshee list bulk-add 21YKUC < entities.txt
cat entities.txt | banshee list bulk-add 21YKUC
```

**응답:** 결과별로 그룹화된 일반 텍스트 — 영향을 받은 엔티티를 나열하는 `ADDED:`, `REMOVED:` (덮어쓰기 모드 한정), `UNCHANGED:` 블록. JSON 형식이 아니므로 `jq`로 파이프하지 마십시오.

---

### `banshee list remove LIST_ID ENTITY_ID`

목록에서 단일 엔티티를 제거합니다.

```bash
banshee list remove 1b0s1q lYNvCK
```

---

### `banshee list bulk-remove LIST_ID [ENTITY_INPUT]...`

목록에서 여러 엔티티를 제거합니다. `bulk-add`와 동일한 입력 형식을 사용합니다.

```bash
banshee list bulk-remove 21YKUC JLHNoH lYNvCK
banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# From file
banshee list bulk-remove 21YKUC < entities.txt
cat entities.txt | banshee list bulk-remove 21YKUC
```

---

### `banshee list copy SOURCE_LIST_ID DESTINATION_LIST_ID`

한 목록의 엔티티를 다른 목록으로 복사합니다. 원본 목록의 엔티티를 읽어 대상 목록에 추가합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | 꺼짐 | 덮어쓰기 모드: 두 목록 모두에 있는 엔티티는 유지하고 새 엔티티를 추가하며, 대상 목록에는 있지만 원본 목록에 **없는** 엔티티는 제거합니다. 이 옵션 없이는 엔티티가 대상 목록에만 추가되며 아무것도 제거되지 않습니다. |

원본 목록이 비어 있으면 `--overwrite` 옵션을 사용하더라도 대상 목록을 수정하지 않고 명령이 종료됩니다.

```bash
banshee list copy 1b0s1q 21YKUC

# Make the destination mirror the source exactly (adds missing, removes stale)
banshee list copy 1b0s1q 21YKUC --overwrite
```

**응답:** 결과별로 그룹화된 일반 텍스트 — 영향을 받은 엔티티를 나열하는 `ADDED:`, `REMOVED:` (덮어쓰기 모드 한정), `UNCHANGED:` 블록. JSON 형식이 아니므로 `jq`로 파이프하지 마십시오.

---

### `banshee list clear LIST_ID`

목록에서 **모든** 엔티티를 제거합니다 (파괴적 작업 — 주의하여 사용하십시오). 텍스트 매칭 항목은 API를 통해 제거할 수 없습니다. 목록 자체는 삭제되지 않으며 엔티티만 제거됩니다.

```bash
banshee list clear 1b0s1q
```

**응답:** 일반 텍스트. 목록이 이미 비어 있으면 `No entities to remove`를 출력하고, 성공 시 `Successfully removed <N> entities`를 출력합니다. 일부 제거에 실패한 경우에는 `<N> entities were not removed from the list:`에 이어 아직 남아 있는 엔티티를 출력합니다. JSON 형식이 아닙니다.