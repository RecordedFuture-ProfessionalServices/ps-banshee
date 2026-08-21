# sandbox

> 인증, 준비 상태 확인, 출력 규칙, 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

Sandbox 명령은 `RF_TOKEN` 외에 `RF_SANDBOX_TOKEN`이 필요합니다. 특정 지역을 대상으로 하려면 `RF_SANDBOX_CHOICE`(또는 전역 옵션 `--sandbox-choice`)를 설정하십시오: `eu`(기본값), `usa`, `apj`, `public`, `private`.

---

### `banshee sandbox stats`

설정 가능한 lookback 기간 동안의 sandbox 제출을 집계하고, SOC 아침 브리핑(제출 건수, 점수 분포, 상위 멀웨어 패밀리, 플랫폼 커버리지, 추출된 C2, SOAR 검증 네트워크 IOC)을 출력합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--days INTEGER` | `-d` | `7` | Lookback 기간(일 단위, 최솟값 1) |
| `--subset` | `-s` | `org` | 샘플 범위: `owned`, `public`, `org` |
| `--pretty` | `-p` | | 사람이 읽기 쉬운 Rich 레이아웃 |

점수 버킷(트리아지 1–10 척도):

| 버킷 | 점수 범위 | 의미 |
|------|-----------|------|
| `malicious` | 8–10 | 알려진 멀웨어, 높은 신뢰도 |
| `suspicious` | 5–7 | 강한 행위 지표 |
| `potentially_suspicious` | 3–4 | 일부 지표 존재 |
| `clean` | 1–2 | 위험 낮음 또는 정상 |

```bash
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats -d 30 | jq '.by_score'
```

**응답 형식:** 단일 JSON 객체를 반환합니다:

| 필드 | 설명 |
|------|------|
| `.period_start` | 집계 기간 시작(ISO 8601) |
| `.period_end` | 집계 기간 종료(ISO 8601) |
| `.period_days` | Lookback 기간(일 단위) |
| `.subset` | 사용된 범위(`owned`, `public`, `org`) |
| `.total` | 기간 내 총 제출 건수 |
| `.pending` | 아직 분석 중인 제출 건수 |
| `.failed` | 오류가 발생한 제출 건수 |
| `.by_kind` | 제출 종류(`file`, `url` 등)를 건수에 매핑하는 객체 |
| `.by_platform` | 플랫폼 태그를 건수에 매핑하는 객체 |
| `.by_score` | 점수 버킷 이름을 건수에 매핑하는 객체 |
| `.by_file_type` | 파일 확장자를 건수에 매핑하는 객체 |
| `.top_tags` | `malware_families`, `botnets`, `arch_file`, `behavioral_ttp` 키를 가지는 객체 — 각각 태그 이름을 건수에 매핑 |
| `.top_iocs` | `extracted_c2`, `verified_network`, `malicious_sha256` 키를 가지는 객체 — 각각 IOC 문자열 배열 |
| `.daily_by_family` | 멀웨어 패밀리를 일별 건수에 매핑하는 객체 |
| `.trend_vs_prior_period` | `total` 및 `reported` 하위 객체를 가지는 객체. 각 하위 객체에는 `current`, `prev`, `pct_change` 포함 |
| `.soar_skipped` | SOAR 검증이 생략된 경우 `true`(`.top_iocs.verified_network`는 비어 있음) |

---

### `banshee sandbox list`

Sandbox 샘플을 나열합니다 — 본인 소유, 조직 소유(기본값), 또는 공개 피드.

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--subset` | `-s` | `org` | 샘플 범위: `owned`, `public`, `org` |
| `--limit INTEGER` | `-l` | `20` | 최대 결과 수(1–4095) |
| `--pretty` | `-p` | | 사람이 읽기 쉬운 테이블 |

```bash
banshee sandbox list
banshee sandbox list --subset owned
banshee sandbox list -s public -l 50
banshee sandbox list -p
banshee sandbox list | jq '.[].sha256'
```

**응답 형식:** 플랫 JSON 배열을 반환합니다. 각 항목:

| 필드 | 설명 |
|------|------|
| `.id` | 샘플 ID(예: `260722-x8lgjahyvx`) |
| `.status` | 분석 상태: `pending`, `running`, `reported`, `failed` |
| `.kind` | 제출 종류: `file`, `url`, `fetch`, `import` |
| `.filename` | 원본 파일명(URL 제출의 경우 비어 있을 수 있음) |
| `.submitted` | 제출 타임스탬프(ISO 8601) |
| `.completed` | 완료 타임스탬프(ISO 8601; 아직 실행 중인 경우 없음) |
| `.sha256` | 제출된 파일의 SHA-256 |
| `.user_id` | 제출 사용자의 UUID |

---

### `banshee sandbox search`

해시, 패밀리, 태그, 봇넷, 지갑, IP, 도메인, URL, 제출 날짜 범위 등의 구조화된 필터 또는 원시 Triage 쿼리를 사용하여 샘플을 검색합니다. 최소한 하나의 필터 또는 `--query`를 제공해야 합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--hash TEXT` | | | 파일 해시(MD5/SHA1/SHA256)로 필터링 |
| `--family TEXT` | | | 멀웨어 패밀리 이름으로 필터링 |
| `--tag TEXT` | `-T` | | 태그로 필터링(반복 사용 가능) |
| `--botnet TEXT` | | | 봇넷 이름으로 필터링 |
| `--wallet TEXT` | | | 지갑 주소로 필터링 |
| `--ip TEXT` | | | IP 주소로 필터링 |
| `--domain TEXT` | | | 도메인으로 필터링 |
| `--url TEXT` | | | URL로 필터링 |
| `--from-date YYYY-MM-DD` | | | 이 날짜 이후에 제출된 항목 |
| `--to-date YYYY-MM-DD` | | | 이 날짜 이전에 제출된 항목 |
| `--query TEXT` | `-q` | | 원시 Triage 쿼리 문자열(구조화된 필터와 AND로 결합) |
| `--limit INTEGER` | `-l` | `50` | 최대 결과 수(1–200) |
| `--pretty` | `-p` | | 사람이 읽기 쉬운 테이블 |

```bash
banshee sandbox search --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
banshee sandbox search --family emotet
banshee sandbox search --ip 1.2.3.4 --domain evil.example
banshee sandbox search -T ransomware -T persistence
banshee sandbox search --from-date 2026-07-01 --to-date 2026-07-31 --family vidar
banshee sandbox search -q "NOT family:emotet" -l 100
banshee sandbox search --family emotet -p
banshee sandbox search --family emotet | jq '.[].sha256'
```

**응답 형식:** JSON 배열을 반환합니다 — `sandbox list` 항목과 동일한 구조.

---

### `banshee sandbox get`

ID로 단일 sandbox 샘플의 요약 정보(현재 상태, 전체 점수, 대상, 생성 및 완료 타임스탬프, SHA256, 태스크별 분석 결과)를 가져옵니다. 진행 중인 샘플과 완료된 샘플 모두에 사용할 수 있습니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `SAMPLE_ID` (필수) | | Sandbox 샘플 ID |
| `--pretty` | `-p` | 사람이 읽기 쉬운 Rich 레이아웃 |

```bash
banshee sandbox get 260501-h4p7laawme
banshee sandbox get 260501-h4p7laawme -p
banshee sandbox get 260501-h4p7laawme | jq '.score'
banshee sandbox get 260501-h4p7laawme | jq '.tasks | keys'
```

**응답 형식:** 단일 JSON 객체를 반환합니다:

| 필드 | 설명 |
|------|------|
| `.sample` | 샘플 ID |
| `.status` | 분석 상태: `pending`, `running`, `static_analysis`, `reported`, `failed` |
| `.target` | 기본 디토네이션 대상(파일명 또는 URL) |
| `.score` | 전체 트리아지 점수(1–10; 분석 진행 중에는 `0`) |
| `.created` | 제출 타임스탬프(ISO 8601) |
| `.completed` | 완료 타임스탬프(ISO 8601; 아직 실행 중인 경우 없음) |
| `.sha256` | 제출된 파일의 SHA-256(URL 제출의 경우 없음) |
| `.owner` | 제출 사용자 ID |
| `.tasks` | 태스크 ID → `{kind, status, score, tags, platform}` 매핑 객체 |

---

### `banshee sandbox download` *(디스크에 영향을 미치는 변경 작업)*

하나 이상의 샘플 ID에 대해 원본 제출 샘플 바이트를 다운로드합니다. 각 샘플은 바이러스 백신, 보안 이메일 게이트웨이, 파일 매니저에 의한 우발적 실행을 방지하기 위해 비밀번호 `infected`로 AES 암호화된 ZIP 아카이브로 래핑됩니다. `7z x -pinfected <sample-id>.zip`으로 압축을 해제하십시오 — 표준 `unzip`은 AES 암호화 ZIP을 안정적으로 처리하지 못합니다.

샘플 ID는 위치 인수로 전달하거나 stdin을 통해 파이프(공백으로 구분)할 수 있습니다. `--yes`를 지정하지 않으면 확인 메시지가 표시됩니다. 다운로드 및 압축 과정에서 바이트가 잠시 이 프로세스의 메모리에 존재하므로 공격적인 EDR 메모리 스캔이 여전히 감지할 수 있습니다. 일상적인 업무용 회사 노트북이 아닌, 분석가 전용 장비에서 실행하십시오.

| 인수/옵션 | 단축 | 기본값 | 설명 |
|-----------|------|--------|------|
| `SAMPLE_IDS` | | | 하나 이상의 샘플 ID(또는 stdin에서 읽기) |
| `--output-dir PATH` | `-d` | (필수) | 암호화된 ZIP 아카이브를 저장할 디렉터리(없으면 생성) |
| `--yes` | `-y` | | 확인 메시지 생략 |
| `--workers INTEGER` | `-w` | `1` | 병렬 다운로드 워커 수(1–16) |

```bash
banshee sandbox download 260501-h4p7laawme -d ./samples
banshee sandbox download id1 id2 id3 -d ./samples --yes -w 4
echo 'id1 id2 id3' | banshee sandbox download -d ./samples --yes

# Extract
7z x -pinfected ./samples/260501-h4p7laawme.zip
```

**응답:** 경고 메시지가 stderr에 한 번 출력됩니다. 성공한 다운로드마다 stderr에 `[<id>] Saved: <path> (<bytes> bytes, sha256=<hex>)` 줄이, 실패 시 `[<id>] ERROR: <msg>` 줄이 출력됩니다. 일부 실패가 있는 배치는 완료까지 계속 진행되며 종료 코드 1로 종료됩니다. 완전히 성공한 배치는 종료 코드 0으로 종료됩니다.

아카이브 내용: 원본 샘플 바이트를 담은 `<sample-id>`(확장자 추측 없음)라는 단일 항목.

---

### `banshee sandbox delete` *(변경 작업)*

ID로 sandbox 샘플을 삭제하고 연관된 모든 태스크 아티팩트를 제거합니다. `--yes`를 지정하지 않으면 확인 메시지가 표시됩니다.

| 인수/옵션 | 설명 |
|-----------|------|
| `SAMPLE_ID` (필수) | 삭제할 샘플 ID |
| `--yes` / `-y` | 확인 메시지 생략 |

```bash
banshee sandbox delete 260501-h4p7laawme
banshee sandbox delete 260501-h4p7laawme -y
```

**응답:** 성공 시 출력 없음; 종료 코드 0으로 종료.

---

### `banshee sandbox submit` *(변경 작업)*

분석을 위해 샘플을 제출합니다. 로컬 파일은 업로드되고, URL은 브라우저에서 디토네이션되거나(`--fetch` 사용 시 먼저 다운로드 후 파일 분석), 공개 샘플은 `--import`를 사용하여 ID로 임포트할 수 있습니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `TARGET` (필수) | | 파일 경로, URL, 또는 공개 샘플 ID(`--import` 사용 시) |
| `--fetch` | | URL을 먼저 다운로드한 후 파일을 분석. `--import`와 상호 배타적 |
| `--import` | | 대상을 공개 샘플 ID로 처리. `--fetch`와 상호 배타적 |
| `--profile TEXT` | | 분석 프로파일 이름 또는 ID(반복 사용 가능; `--interactive`와 상호 배타적) |
| `--timeout INTEGER` | `-t` | 분석 타임아웃(초 단위, 1–3600) |
| `--network` | `-N` | 네트워크 모드: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | VPN 출구 국가 코드; `--network vpn` 필요 |
| `--tags TEXT` | `-T` | 커스텀 태그(반복 사용 가능) |
| `--password TEXT` | | 보호된 아카이브의 비밀번호 |
| `--wait` | `-w` | 분석이 완료될 때까지 폴링 후 개요 보고서 출력 |
| `--interactive` | `-i` | 정적 분석 단계에서 일시 중지하여 `set-profile`로 프로파일 선택; `--profile`과 상호 배타적 |
| `--pretty` | `-p` | 사람이 읽기 쉬운 출력 |

```bash
banshee sandbox submit malware.exe
banshee sandbox submit https://evil.com
banshee sandbox submit https://cdn.evil.com/payload.exe --fetch
banshee sandbox submit 250601-abc123 --import
banshee sandbox submit malware.zip --password infected --profile win10-x64 -T case-42
banshee sandbox submit malware.exe --network vpn --geolocation us -t 300
banshee sandbox submit malware.exe --wait | jq '.analysis.score'
banshee sandbox submit archive.zip --interactive --wait --pretty
```

**응답 형식(기본값):** 제출된 샘플을 JSON 객체로 반환합니다 — `sandbox list` 항목과 동일한 필드(`id`, `status`, `kind`, `filename`, `submitted`, `sha256`, `user_id`). `.id`를 사용하여 제출을 추적하거나 보고할 수 있습니다.

**응답 형식(`--wait` 사용 시):** 개요 보고서를 반환합니다 — `sandbox report overview`와 동일한 구조.

---

### `banshee sandbox set-profile` *(변경 작업)*

정적 분석 단계에서 일시 중지된 샘플(`--interactive`로 제출된 샘플)에 분석 프로파일을 할당합니다. `--auto`를 사용하면 sandbox가 자동으로 선택하고, `--pick FILE:PROFILE`을 사용하면 파일별로 수동 매핑할 수 있습니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `SAMPLE_ID` (필수) | | 정적 분석 단계에서 일시 중지된 샘플의 ID |
| `--auto` | `-a` | 모든 파일에 대해 프로파일 자동 선택. `--pick`과 상호 배타적 |
| `--pick FILE:PROFILE` | | 파일 하나를 프로파일 하나에 매핑(반복 사용 가능). `--auto`와 상호 배타적 |
| `--pretty` | `-p` | 사람이 읽기 쉬운 출력 |

```bash
banshee sandbox set-profile 260501-h4p7laawme --auto
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 --pick doc.docx:office365
banshee sandbox set-profile 260501-h4p7laawme --pick file.exe:win10-x64 | jq '.success'
```

---

### `banshee sandbox profile list`

Recorded Future Sandbox에서 사용 가능한 모든 분석 프로파일을 나열합니다.

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--pretty` | `-p` | 사람이 읽기 쉬운 테이블 |

```bash
banshee sandbox profile list
banshee sandbox profile list -p
banshee sandbox profile list | jq '.[].name'
```

**응답 형식:** 플랫 JSON 배열을 반환합니다. 각 항목:

| 필드 | 설명 |
|------|------|
| `.id` | 프로파일 UUID |
| `.name` | 프로파일 이름 |
| `.tags` | OS/로케일 태그 배열(예: `["os:windows10-2004-x64", "locale:en-us"]`) |
| `.network` | 네트워크 모드(예: `"internet"`, `"tor"`, `"vpn"`) |
| `.geolocation` | VPN 출구 국가 코드 배열(해당 없을 경우 비어 있음) |
| `.timeout` | 분석 타임아웃(초 단위) |
| `.options` | `browser` 등 선택적 필드를 포함하는 객체 |

---

### `banshee sandbox profile get`

ID 또는 이름으로 단일 분석 프로파일을 가져옵니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `PROFILE_ID_OR_NAME` (필수) | | 프로파일 UUID 또는 이름 |
| `--pretty` | `-p` | 사람이 읽기 쉬운 테이블 |

```bash
banshee sandbox profile get 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile get 'Windows 7 Long'
banshee sandbox profile get w7-long -p
banshee sandbox profile get w7-long | jq '.tags'
```

**응답 형식:** 단일 프로파일 객체 — `sandbox profile list` 항목과 동일한 필드.

---

### `banshee sandbox profile create` *(변경 작업)*

새로운 분석 프로파일을 생성합니다. 프로파일 이름은 조직 내에서 고유해야 합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--name TEXT` | `-n` | (필수) | 프로파일 이름(고유해야 함) |
| `--tag TEXT` | `-T` | (필수) | OS/로케일 태그(반복 사용 가능). 로케일 태그는 최소 하나의 OS 태그와 함께 사용해야 함 |
| `--timeout INTEGER` | `-t` | `120` | 분석 타임아웃(초 단위, 1–3600) |
| `--network` | `-N` | | 네트워크 모드: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | | VPN 출구 국가 코드; `--network vpn` 필요(반복 사용 가능) |
| `--browser` | `-b` | | 브라우저: `chrome`, `firefox`, `ie11`, `microsoft-edge` |
| `--pretty` | `-p` | | 사람이 읽기 쉬운 테이블 |

```bash
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120
banshee sandbox profile create -n w10-vpn -T os:windows10-2004-x64 -t 300 -N vpn --geolocation se
banshee sandbox profile create -n w10-ff -T os:windows10-2004-x64 -T locale:en-us -t 120 -b firefox -p
banshee sandbox profile create -n w10-quick -T os:windows10-2004-x64 -t 120 | jq '.id'
```

**응답 형식:** 생성된 프로파일을 JSON 객체로 반환합니다 — `sandbox profile list` 항목과 동일한 필드.

---

### `banshee sandbox profile update` *(변경 작업)*

기존 분석 프로파일을 업데이트합니다. 지정한 옵션만 변경되며, 생략된 옵션은 현재 값을 유지합니다. `network`, `browser`, `geolocation`을 초기화하려면 `--unset`을 사용하십시오.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `PROFILE_ID_OR_NAME` (필수) | | 프로파일 UUID 또는 이름 |
| `--name TEXT` | `-n` | 새 프로파일 이름 |
| `--tag TEXT` | `-T` | OS/로케일 태그; 기존 태그를 모두 교체(반복 사용 가능) |
| `--timeout INTEGER` | `-t` | 분석 타임아웃(초 단위, 1–3600) |
| `--network` | `-N` | 네트워크 모드: `internet`, `drop`, `tor`, `vpn`, `sim200`, `sim404`, `simnx` |
| `--geolocation TEXT` | | VPN 출구 국가 코드; `--network vpn` 필요(반복 사용 가능) |
| `--browser` | `-b` | 브라우저: `chrome`, `firefox`, `ie11`, `microsoft-edge` |
| `--unset` | | 필드 초기화: `network`, `browser`, `geolocation`(반복 사용 가능) |
| `--pretty` | `-p` | 사람이 읽기 쉬운 상태 메시지 |

```bash
banshee sandbox profile update ernie -n ernie-v2
banshee sandbox profile update ernie -T os:windows10-2004-x64 -T locale:en-us
banshee sandbox profile update ernie -t 300 -N vpn --geolocation us --geolocation gb
banshee sandbox profile update ernie --unset browser --unset network
banshee sandbox profile update ernie -n ernie-v2 | jq '.updated'
```

**응답 형식:** 프로파일이 존재하고 업데이트된 경우 `{"updated": true}`를, 존재하지 않는 경우 `{"updated": false}`를 반환합니다. 어느 경우든 종료 코드 0으로 종료됩니다.

---

### `banshee sandbox profile delete` *(변경 작업)*

ID 또는 이름으로 분석 프로파일을 삭제합니다. 반복 실행에 안전합니다: 더 이상 존재하지 않는 프로파일을 삭제하면 경고를 출력하고 종료 코드 0으로 종료됩니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `PROFILE_ID_OR_NAME` (필수) | | 프로파일 UUID 또는 이름 |
| `--yes` / `-y` | | 확인 메시지 생략 |

```bash
banshee sandbox profile delete 022b8c4e-22ab-46a4-ac49-a2732b2412b7
banshee sandbox profile delete 'Windows 7 Long'
banshee sandbox profile delete w7-long -y
```

**응답:** 성공 시 출력 없음; 종료 코드 0으로 종료.

---

### `banshee sandbox report overview`

완료된 sandbox 샘플에 대한 전체 개요 보고서(판정 점수, 멀웨어 패밀리, 태그, 해시, 탐지 시그니처, 추출된 멀웨어 설정, 네트워크 IOC, 태스크별 결과)를 가져옵니다. 샘플은 `reported` 상태여야 합니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `SAMPLE_ID` (필수) | | Sandbox 샘플 ID |
| `--wait` | `-w` | 보고서가 준비될 때까지 최대 30분간 폴링 |
| `--pretty` | `-p` | 사람이 읽기 쉬운 요약 뷰 |

```bash
banshee sandbox report overview 260501-h4p7laawme
banshee sandbox report overview 260501-h4p7laawme -p
banshee sandbox report overview 260501-h4p7laawme --wait
banshee sandbox report overview 260501-h4p7laawme | jq '.analysis'
banshee sandbox report overview 260501-h4p7laawme | jq '.targets[].iocs'
```

**응답 형식:** 단일 JSON 객체를 반환합니다:

| 필드 | 설명 |
|------|------|
| `.version` | 보고서 형식 버전 |
| `.build` | Sandbox 빌드 정보 |
| `.analysis` | 판정 객체: 점수, 멀웨어 패밀리, 태그 |
| `.sample` | 샘플 메타데이터: id, kind, filename, sha256, submitted, completed |
| `.signatures` | 모든 태스크에 걸친 탐지 시그니처 |
| `.targets` | 디토네이션된 대상 객체 배열, 각각 `.iocs`(네트워크 IOC) 및 멀웨어 설정 추출 포함 |
| `.tasks` | 태스크별 요약 배열: 태스크 ID, 플랫폼, 상태, 판정 점수 |

---

### `banshee sandbox report static`

Sandbox 샘플의 정적(디토네이션 전) 분석 보고서(판정 점수, 태그, 언팩된 파일, 정적 탐지 시그니처, 추출된 멀웨어 설정)를 가져옵니다. 행위 기반 태스크가 완료되기 전에 정적 분석이 끝나는 즉시 사용 가능합니다.

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `SAMPLE_ID` (필수) | | Sandbox 샘플 ID |
| `--wait` | `-w` | 보고서가 준비될 때까지 최대 10분간 폴링 |
| `--pretty` | `-p` | 사람이 읽기 쉬운 요약 뷰 |

```bash
banshee sandbox report static 260501-h4p7laawme
banshee sandbox report static 260501-h4p7laawme -p
banshee sandbox report static 260501-h4p7laawme --wait
banshee sandbox report static 260501-h4p7laawme | jq '.analysis'
banshee sandbox report static 260501-h4p7laawme | jq '.files[].sha256'
```

**응답 형식:** 단일 JSON 객체를 반환합니다:

| 필드 | 설명 |
|------|------|
| `.version` | 보고서 형식 버전 |
| `.build` | Sandbox 빌드 정보 |
| `.sample` | 샘플 메타데이터: id, kind, filename, sha256, submitted |
| `.task` | 정적 태스크 메타데이터 |
| `.analysis` | 판정 객체: 점수, 태그, 정적 시그니처 |
| `.files` | 언팩된 파일 배열 — 각각 `sha256`, `filename`, `size` 및 정적 분석 세부 정보 포함 |
| `.unpack_count` | 제출에서 언팩된 총 파일 수 |
| `.error_count` | 언팩할 수 없었던 파일 수 |

---

### `banshee sandbox report behavioral`

완료된 sandbox 샘플의 행위 기반(디토네이션 후) 보고서를 가져옵니다. 완료된 행위 기반 태스크당 하나의 객체가 반환됩니다. 완료되지 않은 태스크는 출력에서 제외되며 stderr에 기록됩니다. 모든 태스크가 완료될 때까지 명령은 비정상 종료 코드로 종료됩니다. 샘플에 행위 기반 태스크가 없으면 빈 배열이 반환되고 종료 코드 0으로 종료됩니다.

`--pretty` 뷰에서 프로세스 커맨드 라인은 기본적으로 잘립니다 — 전체 내용이 필요하면 `--full-cmd`를 전달하십시오(멀웨어 샘플에서 그대로 가져온 것이므로 신뢰할 수 없는 입력으로 취급하십시오).

| 인수/옵션 | 단축 | 설명 |
|-----------|------|------|
| `SAMPLE_ID` (필수) | | Sandbox 샘플 ID |
| `--wait` | `-w` | 모든 태스크가 완료될 때까지 최대 30분간 폴링 |
| `--full-cmd` | | 잘리지 않은 전체 프로세스 커맨드 라인 표시(신뢰할 수 없는 입력으로 취급) |
| `--pretty` | `-p` | 태스크별 사람이 읽기 쉬운 요약 뷰 |

```bash
banshee sandbox report behavioral 260501-h4p7laawme
banshee sandbox report behavioral 260501-h4p7laawme -p
banshee sandbox report behavioral 260501-h4p7laawme --wait
banshee sandbox report behavioral 260501-h4p7laawme -p --full-cmd
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].analysis.score'
banshee sandbox report behavioral 260501-h4p7laawme | jq '.[].network.flows'
```

**응답 형식:** JSON 배열을 반환합니다. 각 항목은 하나의 행위 기반 태스크에 해당합니다:

| 필드 | 설명 |
|------|------|
| `.task_id` | 행위 기반 태스크 ID |
| `.version` | 보고서 형식 버전 |
| `.build` | Sandbox 빌드 정보 |
| `.sample` | 샘플 메타데이터: id, kind, filename, sha256 |
| `.task` | 태스크 메타데이터: platform, status, started, completed |
| `.analysis` | 판정 객체: 점수, 멀웨어 패밀리, 태그 |
| `.tags` | 행위 기반 태그 배열(예: `discovery`, `execution`) |
| `.signatures` | 트리거된 탐지 시그니처 배열 |
| `.processes` | 관찰된 프로세스 배열 — 각각 `pid`, `name`, `cmd`(`--full-cmd` 없이는 잘림), 자식 프로세스 포함 |
| `.network` | 네트워크 활동: `.flows`(연결 레코드), `.dns`(DNS 쿼리), `.http`(HTTP 요청) |
| `.dumped` | SHA-256 해시와 함께 덤프/추출된 파일 배열 |