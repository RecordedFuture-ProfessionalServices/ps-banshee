# 릴리스 히스토리

## 1.5.0 - 2026-08-21

### Added
- Recorded Future Sandbox를 위한 새로운 [`sandbox`](reference/commands.md#banshee-sandbox) 명령어 그룹을 추가하였습니다. `RF_SANDBOX_TOKEN`이 필요하며, 지역은 [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) 또는 `RF_SANDBOX_CHOICE`로 선택할 수 있습니다(`eu` 기본값, `usa`, `apj`, `public`, `private`).
- 로컬 파일, URL, 공개 샘플 ID(`--import`), 또는 다운로드할 URL(`--fetch`)을 분석을 위해 제출하는 새로운 [`sandbox submit`](reference/commands.md#banshee-sandbox-submit) 서브 명령어를 추가하였습니다. 프로파일 할당, 커스텀 태그, 타임아웃, 네트워크 모드(지리적 위치를 사용하는 VPN 포함), 아카이브 비밀번호, 분석 완료까지 폴링하고 개요 보고서를 출력하는 [`--wait`](reference/commands.md#banshee-sandbox-submit--wait), 정적 분석 단계에서 일시 중지하고 기폭 전에 파일별 프로파일을 선택하는 [`--interactive`](reference/commands.md#banshee-sandbox-submit--interactive)를 지원합니다.
- 샘플의 통합 판정 보고서, 기폭 전 정적 분석, 또는 작업별 기폭 후 보고서를 가져오는 새로운 [`sandbox report overview`](reference/commands.md#banshee-sandbox-report-overview), [`sandbox report static`](reference/commands.md#banshee-sandbox-report-static), [`sandbox report behavioral`](reference/commands.md#banshee-sandbox-report-behavioral) 서브 명령어를 추가하였습니다. 각각 보고서가 준비될 때까지 폴링하는 [`--wait`](reference/commands.md#banshee-sandbox-report-overview--wait)를 지원합니다.
- 자신의 피드, 조직의 피드, 또는 공개 피드의 샘플을 나열하는 새로운 [`sandbox list`](reference/commands.md#banshee-sandbox-list) 서브 명령어를 추가하였습니다.
- 해시, 악성코드 패밀리, 태그, 봇넷, 지갑, 네트워크 지표(IP, 도메인, URL), 또는 제출 날짜 범위로 과거 제출 이력을 피벗 검색하는 새로운 [`sandbox search`](reference/commands.md#banshee-sandbox-search) 서브 명령어를 추가하였습니다. [`--query`](reference/commands.md#banshee-sandbox-search--query)를 통해 `AND`/`OR`/`NOT` 표현식에 대한 원시 Triage 쿼리 문자열도 허용합니다.
- 전체 보고서를 가져오지 않고 샘플의 현재 상태, 전체 점수, 작업별 분류를 가져오는 새로운 [`sandbox get`](reference/commands.md#banshee-sandbox-get) 서브 명령어를 추가하였습니다. 진행 중인 샘플과 완료된 샘플 모두에 작동합니다.
- 하나 이상의 샘플 ID에 대해 원본 제출 바이트를 가져오는 새로운 [`sandbox download`](reference/commands.md#banshee-sandbox-download) 서브 명령어를 추가하였습니다. 각 샘플은 비밀번호 `infected`가 설정된 AES 암호화 ZIP 아카이브로 래핑됩니다(MalwareBazaar/VirusTotal/Triage 관례와 동일). 이는 안티바이러스, 보안 이메일 게이트웨이, 또는 파일 관리자에 의한 우발적 기폭을 방지하기 위함입니다. 샘플 ID는 위치 인수로 전달하거나 stdin으로 파이프할 수 있습니다. `7z x -pinfected <sample-id>.zip`으로 압축을 해제하십시오.
- 샘플 및 해당 작업 아티팩트를 제거하는 새로운 [`sandbox delete`](reference/commands.md#banshee-sandbox-delete) 서브 명령어를 추가하였습니다(`--yes`가 지정되지 않으면 확인 메시지가 표시됩니다).
- 정적 분석 단계에서 일시 중지된 샘플에 분석 프로파일을 할당하는 새로운 [`sandbox set-profile`](reference/commands.md#banshee-sandbox-set-profile) 서브 명령어를 추가하였습니다(`--auto` 또는 파일별 `--pick FILE:PROFILE`).
- 커스텀 기폭 프로파일을 관리하는 새로운 [`sandbox profile`](reference/commands.md#banshee-sandbox-profile) 서브 명령어 그룹을 추가하였습니다: [`list`](reference/commands.md#banshee-sandbox-profile-list), [`get`](reference/commands.md#banshee-sandbox-profile-get), [`create`](reference/commands.md#banshee-sandbox-profile-create), [`update`](reference/commands.md#banshee-sandbox-profile-update)(필드를 초기화하는 `--unset` 포함), [`delete`](reference/commands.md#banshee-sandbox-profile-delete).
- SOC 모닝 브리핑을 생성하는 새로운 [`sandbox stats`](reference/commands.md#banshee-sandbox-stats) 서브 명령어를 추가하였습니다: 설정 가능한 조회 기간에 걸쳐 제출 볼륨, 점수 분포(악성/의심/잠재적 의심/정상으로 구분된 1~10 Triage 척도), 플랫폼 커버리지, 상위 악성코드 패밀리 및 봇넷, 행동 TTP, 추출된 C2, SOAR 검증 네트워크 IOC를 제공합니다.
- Docs: 한국어(`ko`) 언어 인프라를 추가하였습니다. 콘텐츠는 후속 PR에서 제공되며, 그 전까지는 번역 미제공 배너가 표시됩니다.
- Docs: `scripts/docs.py` — `build-all`, `dev`, `check-translations`, `translate` 명령어를 추가하였습니다.
- Docs: 영어 이외의 모든 번역에 대한 CI 드리프트 검사를 추가하였습니다. 기여자는 LLM 번역기를 로컬에서 실행합니다(`uv sync --group translations && scripts/docs.py translate --lang <code> --all`). CI는 LLM을 호출하지 않습니다.

### Changed
- Configuration: banshee 전용 전역 필드(`sandbox_choice`)를 포함하는 `BansheeConfig(psengine.ConfigModel)` 서브클래스를 추가하였습니다. 새로운 루트 레벨 [`--sandbox-key`](reference/commands.md#banshee--sandbox-key) / `RF_SANDBOX_TOKEN` 및 [`--sandbox-choice`](reference/commands.md#banshee--sandbox-choice) / `RF_SANDBOX_CHOICE` 옵션을 통해 필요한 모든 명령어에서 sandbox 인증을 사용할 수 있습니다.
- Docs: `mike` 버전 관리 배포를 제거하였습니다. 사이트는 이제 루트 URL에서 배포됩니다. 이전의 버전 관리 URL(`/1.x/…`)은 더 이상 유효하지 않으니, 루트 URL을 사용하십시오.
- Docs: `mkdocs-static-i18n`을 fastapi 방식의 언어별 빌드로 대체하였으며, `scripts/docs.py`가 이를 조율합니다. 단일 권위 파일인 `docs/mkdocs.yml`을 사용하며, 번역된 언어는 해당 번역 마크다운 파일만 보유합니다.
- Docs: `noklam/mkdocs-llmstxt-md`를 `pawamoy/mkdocs-llmstxt`로 교체하였습니다. `llms.txt` / `llms-full.txt`는 영어 전용이며 사이트 루트에 위치합니다.


## v.1.4.1 - 2026-07-13

### Changed
- `psengine` 의존성을 업그레이드하였습니다.


## v.1.4.0 - 2026-07-13

### Added
- [`risklist stat`](reference/commands.md#banshee-risklist-stat)에 새로운 [`-C`/`--count`](reference/commands.md#banshee-risklist-stat--count) 옵션을 추가하였습니다. 이 옵션은 risk list(위험 목록)를 다운로드하고 위험 점수별 지표 수를 테이블로 출력합니다.

## v1.3.1 - 2026-06-30

### Changed
- 의존성을 업그레이드하였습니다.

## 1.3.0 - 2026-06-15

### Added
- 새로운 [`email enrich`](reference/commands.md#banshee-email-enrich) 서브 명령어를 추가하였습니다. EML 파일을 보강하며, 헤더 IP 및 본문 URL을 추출한 후 위험 점수, 위협 행위자 연관 정보, 악성코드 링크, 위험 규칙 증거를 포함한 Recorded Future 인텔리전스를 반환합니다.
- 새로운 [`ca export`](reference/commands.md#banshee-ca-export) 서브 명령어를 추가하였습니다. Classic Alert를 전체 JSON 또는 요약 CSV로 내보냅니다. [`ca search`](reference/commands.md#banshee-ca-search)에서 파이프로 전달된 알림 ID를 읽습니다.
- 새로운 [`pba export`](reference/commands.md#banshee-pba-export) 서브 명령어를 추가하였습니다. Playbook Alert를 전체 JSON 또는 요약 CSV로 내보냅니다. [`pba search`](reference/commands.md#banshee-pba-search)에서 파이프로 전달된 검색 결과를 읽습니다.
- [`pba search`](reference/commands.md#banshee-pba-search)에 새로운 [`-o`/`--org-id`](reference/commands.md#banshee-pba-search--org-id) 옵션을 추가하였습니다. 소유 조직 ID로 Playbook Alert를 필터링합니다(반복 사용 가능).
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add)에 새로운 [`-o`/`--overwrite`](reference/commands.md#banshee-list-bulk-add--overwrite) 옵션을 추가하였습니다. 제공된 엔터티와 정확히 일치하도록 목록을 갱신하며, 새 엔터티를 추가하고 제공되지 않은 기존 엔터티를 제거합니다.
- 새로운 [`list copy`](reference/commands.md#banshee-list-copy) 서브 명령어를 추가하였습니다. 한 목록에서 다른 목록으로 엔터티를 복사합니다. 기본적으로 추가(append) 방식이며, [`-o`/`--overwrite`](reference/commands.md#banshee-list-copy--overwrite)를 사용하면 대상 목록이 소스를 정확히 미러링합니다.
- [AI 에이전트와 함께 banshee 사용](getting-started/llms.md)을 지원합니다. 코딩 어시스턴트가 CLI를 탐색하고 실행할 수 있습니다.

### Changed
- [`list clear`](reference/commands.md#banshee-list-clear)는 이제 엔터티를 동시에 제거합니다(대용량 목록에서 훨씬 빠름). [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)와 동일하게, 제거된 항목을 결과(`REMOVED` 및 제거되지 않은 항목)별로 그룹화하고 가독성을 위해 정렬하여 보고합니다.
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add)는 이제 이미 목록에 있는 엔터티를 재추가 시도하지 않고 건너뛰며, `UNCHANGED`로 보고합니다. 동일한 입력 파일을 반복 실행하여 엔터티를 추가 및 제거할 때 속도가 크게 향상됩니다.
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 및 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)는 이제 결과(`ADDED`, `REMOVED`, `UNCHANGED`)별로 출력을 그룹화하고 가독성을 위해 정렬합니다.
- [`ca search`](reference/commands.md#banshee-ca-search) 및 [`pba search`](reference/commands.md#banshee-pba-search)는 이제 진행 상태 표시를 stderr에 출력하여, 새로운 `export` 명령어로 파이프 연결 시 stdout을 깔끔하게 유지합니다.
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 및 [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup)의 pretty 출력(`-p`, `--pretty`)이 이제 악성도에 따라 위험 점수를 색상으로 구분하여 표시합니다.
- PSEngine을 ~v2.8.1로 업그레이드하였습니다.

### Fixed
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 및 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)는 이제 빈 입력 줄을 무시하며, 엔터티가 제공되지 않은 경우 명확한 오류를 보고합니다.

## 1.1.3 - 2026-03-18

### Fixed
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)에서 SOAR 보강 시 멀티스레딩이 사용되지 않던 문제를 수정하였습니다. 대용량 캡처의 경우 위험 점수 보강 속도가 향상되었습니다.


## 1.1.0 - 2026-03-13

### Added
- 새로운 [`risklist create`](reference/commands.md#banshee-risklist-create) 서브 명령어를 추가하였습니다. 하나 이상의 Recorded Future 위험 규칙을 병합하여 중복 제거된 단일 파일로 커스텀 risk list를 생성합니다. CSV, JSON, EDL 출력 형식을 지원하며, 최소 위험 점수 필터링 및 Recorded Future Fusion으로의 직접 업로드를 지원합니다.
- 새로운 [`ioc bulk-lookup`](reference/commands.md#banshee-ioc-bulk-lookup) 서브 명령어를 추가하였습니다. IOC(침해 지표)의 대량 보강을 빠르게 처리합니다. API 호출당 최대 1,000개의 지표를 배치 처리하고 각 지표의 위험 점수 및 트리거된 위험 규칙을 반환합니다. IP, 도메인, URL, 해시, 취약점 등 모든 IOC 유형을 지원합니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON 출력에 위험 규칙 증거 세부 정보가 포함됩니다. 위험 규칙이 트리거된 특정 증거를 상세히 설명합니다.

### Changed
- [`entity search`](reference/commands.md#banshee-entity-search) 기본 결과 수를 100으로 늘렸습니다.
- [`list search`](reference/commands.md#banshee-list-search) 기본 결과 수를 1,000으로 늘렸습니다.
- [`pba search`](reference/commands.md#banshee-pba-search) 기본 결과 수를 50으로 늘렸습니다.
- [`pba search`](reference/commands.md#banshee-pba-search) 최대 결과 수를 10,000으로 늘렸습니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)는 이제 1 이상의 위험 점수를 허용합니다.

### Fixed
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)에서 멀티스레딩이 사용되지 않아 대량 조회가 순차적으로 실행되던 문제를 수정하였습니다. 여러 지표를 보강할 경우 조회 속도가 최대 20배 향상됩니다.
- [`risklist fetch`](reference/commands.md#banshee-risklist-fetch)에서 CSV 파일의 비정상적으로 큰 열 값을 파싱할 때 명령어가 실패하던 문제를 수정하였습니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)에서 빈 IOC 링크를 파싱할 때 실패하던 문제를 수정하였습니다.
- [`list`](reference/commands.md#banshee-list) 명령어에서 API 오류 발생 시 오류 원인이 항상 올바르게 출력되지 않던 문제를 수정하였습니다.

## 1.0.0 - 2025-12-05

### Added

- Recorded Future Risk List의 메타데이터를 다운로드하고 확인하는 새로운 [`risklist`](reference/commands.md#banshee-risklist) 명령어를 추가하였습니다.
- 탐지 규칙(YARA, Snort, Sigma)을 검색하고 다운로드하는 새로운 [`rules`](reference/commands.md#banshee-rules) 명령어를 추가하였습니다.
- [`ioc search`](reference/commands.md#banshee-ioc-search) 및 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 명령어에 CVSS v4 필드 지원을 추가하였습니다.

### Fixed

- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 및 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)는 이제 사용자가 제공한 엔터티를 중복 제거합니다.
- [`list bulk-add`](reference/commands.md#banshee-list-bulk-add) 및 [`list bulk-remove`](reference/commands.md#banshee-list-bulk-remove)에서 공백이 포함된 엔터티 이름이 올바르게 파싱되지 않던 문제를 수정하였습니다.
- [`pba lookup`](reference/commands.md#banshee-pba-lookup)이 이제 이미지 검색 실패 시 알림을 올바르게 처리합니다.

### Changed

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich) JSON 출력에 이제 위험 규칙 증거 세부 정보와 IOC가 트리거한 모든 위험 규칙이 포함됩니다.
- PSEngine을 v2.4.0으로 업그레이드하였습니다.


## 0.0.5 - 2025-11-12

## Fixed

- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)에서 pcap 파일에 IP 또는 도메인이 없을 경우 프로그램이 예기치 않게 종료되던 문제를 수정하였습니다.

## 0.0.4 - 2025-11-07

### Added

- [`ca search`](reference/commands.md#banshee-ca-search) 명령어에 알림 상태로 필터링하는 기능을 추가하였습니다.
- [`pba search`](reference/commands.md#banshee-pba-search) 명령어에 엔터티로 필터링하는 기능을 추가하였습니다.
- 모든 `pba` 명령어에 `malware_report` 카테고리 지원을 추가하였습니다.
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 및 [`ioc search`](reference/commands.md#banshee-ioc-search)의 pretty 출력(`-p`, `--pretty`)에 해시 알고리즘 정보가 포함됩니다.
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup) 및 [`ioc search`](reference/commands.md#banshee-ioc-search)의 pretty 출력(`-p`, `--pretty`)에 취약점의 수명 주기 단계가 포함됩니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)에 결과를 위험 점수로 필터링하는 `-r`/`--risk-score` 옵션을 추가하였습니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)에 위협 헌팅을 활성화하는 `-t`/`--threat-hunt` 옵션을 추가하였습니다.

### Changed

- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)의 각 상세 수준에 대한 필드 선택을 최적화하였습니다.
- [`ioc search`](reference/commands.md#banshee-ioc-search)를 상세 수준 1~5까지 지원하도록 확장하였습니다(기본값은 1).
- `pcap analyze` 서브 명령어의 이름을 [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)로 변경하였습니다.
- [`pcap enrich`](reference/commands.md#banshee-pcap-enrich)는 이제 Wireshark 호환 필터 쿼리를 포함한 정제된 JSON 출력을 생성합니다.
- PSEngine을 v2.3.0으로 업그레이드하였습니다.

### Fixed

- [`ca rules`](reference/commands.md#banshee-ca-rules)에서 결과가 10개의 알림 규칙으로 잘리던 문제를 수정하였습니다.
- [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)에서 IOC에 증거 세부 정보가 없을 때 발생하던 오류를 수정하였습니다.

### Removed

- `pba enrich`에서 대화형 TUI 출력을 제거하고, pretty 출력(`--pretty`, `-p`)으로 대체하였습니다.


## 0.0.3 - 2025-09-02

### Added

- 하나 이상의 Classic Alert를 업데이트하는 새로운 [`ca update`](reference/commands.md#banshee-ca-update) 서브 명령어를 추가하였습니다.
- 하나 이상의 Playbook Alert를 업데이트하는 새로운 [`pba update`](reference/commands.md#banshee-pba-update) 서브 명령어를 추가하였습니다.
- [`pba`](reference/commands.md#banshee-pba) 명령어에 `geopolitics_facility` 카테고리 지원을 추가하였습니다.
- Python 3.13 호환성을 추가하였습니다.
- `tshark` 버전 확인 시 최소 버전 4.4.5를 강제합니다.

### Fixed

- `pcap analyze`가 버전 불일치로 인해 충돌하는 문제를 수정하였습니다.
- CLI 전반에 걸쳐 예외 처리를 개선하였습니다.

### Changed

- `ioc search ENTITY_TYPE IOC`는 이제 쉼표로 구분된 문자열 대신 공백으로 구분된 IOC를 허용합니다.
- `pba lookup ALERT_ID -p` 출력 형식을 개선하였습니다.
- `ca search --triggered`는 이제 시간 범위를 지원합니다.
- `ca search -r`은 이제 쉼표로 구분된 문자열 대신 `-r`을 반복하여 여러 규칙을 허용합니다(예: `-r rule1 -r rule2`).
- PSEngine을 v2.0.6으로 업그레이드하였습니다.


## 0.0.2 - 2025-02-20

### Added

- 엔터티를 검색하고 조회하는 새로운 [`entity`](reference/commands.md#banshee-entity) 명령어를 추가하였습니다.
- Recorded Future 목록 및 감시 목록을 관리하는 새로운 [`list`](reference/commands.md#banshee-list) 명령어를 추가하였습니다.
- IOC 규칙을 검색하고 필터링하는 새로운 [`ioc rules`](reference/commands.md#banshee-ioc-rules) 서브 명령어를 추가하였습니다.
- 향상된 문제 해결을 위한 새로운 `--debug` 옵션을 추가하였습니다.


### Changed

- 서브 명령어 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)의 ``-v`` 옵션이 이제 상세 수준(1~5)을 선택할 수 있습니다.
- 서브 명령어 [`ioc lookup`](reference/commands.md#banshee-ioc-lookup)은 이제 엔터티 유형을 인수로 필요로 합니다. 예: ``banshee ioc lookup ip 8.8.8.8``
- 서브 명령어 [`ca lookup`](reference/commands.md#banshee-ca-lookup)은 이제 정제된 pretty 알림을 반환합니다.
- PSEngine을 v2.0.2로 업그레이드하였습니다.


## 0.0.1 - 2024-09-01

### Added

- 베타 릴리스

---

🚀 Recorded Future 사이버 보안 엔지니어 팀이 제공합니다.