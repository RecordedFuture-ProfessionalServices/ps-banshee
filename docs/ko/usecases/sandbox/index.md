# Sandbox Analysis

## Use Case Summary
Recorded Future Sandbox에서 파일 및 URL을 자동화된 악성코드 분석에 제출하고, 결과 보고서를 검색하며, 검증된 샘플을 오프라인 분석을 위해 전달하여 보안 운영 센터(SOC) 트리아지(triage) 및 위협 조사를 가속화합니다.

## Issue
분석가는 의심스러운 파일 및 URL을 안전하고 통제된 환경에서 실행(detonate)하여 의도를 파악하고 위협 지표(IOC)를 추출해야 합니다. 통합된 워크플로가 없을 경우, 결과 보고서(정적 서명, 행위 활동, 네트워크 IOC, 악성코드 설정 등)를 수집하고 연계하려면 여러 도구에 걸쳐 수동 작업이 필요하므로 SOC 대응이 지연됩니다.

## Solution
PS Banshee에서 [`banshee sandbox`](../../reference/commands.md#banshee-sandbox) 명령을 사용하여 샘플을 제출하고 보고서를 직접 검색합니다.

- [`banshee sandbox submit`](../../reference/commands.md#banshee-sandbox-submit)을 사용하여 로컬 파일, URL, 또는 공개 샘플을 분석에 제출합니다. [`--wait`](../../reference/commands.md#banshee-sandbox-submit--wait)를 추가하면 분석이 완료될 때까지 폴링(polling)하고 개요 보고서를 즉시 출력하며, [`--interactive`](../../reference/commands.md#banshee-sandbox-submit--interactive)를 추가하면 정적 분석 단계에서 일시 중지하고 실행(detonation) 프로필을 선택한 후 진행할 수 있습니다.

- 분석이 완료되면, [`banshee sandbox report overview`](../../reference/commands.md#banshee-sandbox-report-overview)를 사용하여 판정(verdict), 악성코드 패밀리, 네트워크 IOC, 작업별 결과의 요약을 확인하고, [`banshee sandbox report static`](../../reference/commands.md#banshee-sandbox-report-static)을 사용하여 실행 전 분석 및 추출된 악성코드 설정을 확인하며, [`banshee sandbox report behavioral`](../../reference/commands.md#banshee-sandbox-report-behavioral)을 사용하여 트리거된 서명, 관찰된 프로세스, 추출된 C2(Command and Control) 서버를 포함한 실행 후 활동을 확인합니다.

- [`banshee sandbox stats`](../../reference/commands.md#banshee-sandbox-stats)를 사용하여 제출 볼륨, 점수 분포, 상위 악성코드 패밀리, 설정 가능한 조회 기간(lookback window) 내 네트워크 IOC를 표시하는 SOC 일일 브리핑(morning brief)을 생성합니다. 교대 인수인계 또는 일일 트리아지에 활용할 수 있습니다.

- [`banshee sandbox list`](../../reference/commands.md#banshee-sandbox-list)를 사용하여 자신의 계정, 소속 조직, 또는 공개 피드의 최근 제출 내역을 검토하고, [`banshee sandbox get`](../../reference/commands.md#banshee-sandbox-get)을 사용하여 전체 보고서를 가져오지 않고도 단일 샘플의 현재 상태, 전체 점수, 작업별 분석 결과를 확인합니다.

- [`banshee sandbox search`](../../reference/commands.md#banshee-sandbox-search)를 사용하여 해시(hash), 악성코드 패밀리, 태그, 봇넷(botnet), 지갑 주소(wallet), 네트워크 지표(IP, 도메인, URL), 또는 제출 날짜 범위를 기준으로 과거 제출 내역을 피벗(pivot) 검색합니다. `AND`/`OR`/`NOT` 표현식을 위해 `--query`를 사용하여 원시 Triage 쿼리 문자열을 전달합니다.

- [`banshee sandbox download`](../../reference/commands.md#banshee-sandbox-download)를 사용하여 오프라인 분석(YARA/Sigma 튜닝, EDR 탐지 테스트, 캠페인 귀속)을 위해 원본 제출 바이트를 검색합니다. 각 샘플은 비밀번호 `infected`로 AES 암호화된 ZIP 아카이브로 래핑됩니다. `7z x -pinfected <sample-id>.zip`으로 압축을 해제하십시오. 다운로드 및 압축 과정에서 바이트가 프로세스 메모리에 잠시 존재하므로, 분석가가 소유한 장비에서 실행하십시오.

- [`banshee sandbox delete`](../../reference/commands.md#banshee-sandbox-delete)를 사용하여 더 이상 필요하지 않은 샘플 및 관련 아티팩트를 삭제합니다.

- 맞춤형 실행 환경을 사용하는 팀의 경우, [`banshee sandbox profile`](../../reference/commands.md#banshee-sandbox-profile) 명령을 통해 각 제출에 적용되는 OS, 네트워크 구성, 브라우저, 분석 타임아웃을 제어하는 분석 프로필을 생성, 수정, 삭제할 수 있습니다.