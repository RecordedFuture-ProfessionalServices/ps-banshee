# Risk Lists

## 사용 사례 요약
Recorded Future Risk List(위험 목록)를 터미널에서 직접 가져오고 구축하여 강화(enrichment), 상관 분석, 자동화된 탐지를 지원합니다. 분석가는 위험 점수가 매겨진 IP, 도메인, URL, 해시, 또는 취약점을 필요에 따라 가져오거나, 여러 위험 규칙을 단일 사용자 정의 목록으로 결합하여 SOC 워크플로가 항상 최신 인텔리전스를 사용하도록 할 수 있습니다.

## 문제
SOC 팀은 조사, 탐지, 또는 선제적 차단을 위해 최신 위험 점수 지표가 필요한 경우가 많습니다. 여러 플랫폼을 탐색하거나 목록을 수동으로 내보내는 작업은 마찰을 유발하고 대응 속도를 저하시킵니다. 직접 검색 방법을 사용하면 속도와 일관성이 향상됩니다.

## 솔루션
[`banshee risklist`](../../reference/commands.md#banshee-risklist) 명령을 사용하여 PS Banshee에서 Risk List를 가져옵니다. 엔터티 유형과 목록 이름을 지정하여 Recorded Future의 기본, 대용량, 또는 규칙별 risk list를 검색합니다. 결과를 로컬에 저장하여 SIEM 또는 SOAR 강화 파이프라인에 자동으로 수집할 수 있습니다. 필요에 따라 `--as-json`을 추가하면 JSON 기반 수집을 지원하는 시스템을 위해 목록을 JSON 형식으로 출력하므로, 수동 변환 없이 원활한 통합이 가능합니다.

[`banshee risklist create`](../../reference/commands.md#banshee-risklist-create)를 사용하면 하나 이상의 위험 규칙을 단일 중복 제거 출력으로 병합하여 사용자 정의 risk list를 구축할 수 있습니다. 최소 위험 점수로 필터링하고, CSV, EDL, 또는 JSON 출력 형식 중에서 선택하며, 결과를 Recorded Future Fusion에 직접 업로드하는 옵션도 사용할 수 있습니다.