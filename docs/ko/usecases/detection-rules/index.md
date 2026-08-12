# Detection Rules

## Use Case Summary
분석가와 탐지 엔지니어가 위협 행위자, 악성코드, MITRE ATT&CK 기법, 생성 날짜, 또는 Threat Map에 정의된 엔터티를 기준으로 Recorded Future 탐지 규칙(YARA, Snort, Sigma)을 신속하게 검색하고 필터링할 수 있습니다. 결과는 터미널에서 확인하거나 배포를 위한 개별 규칙 파일로 저장할 수 있습니다.

## Issue
위협 헌팅 또는 인시던트 대응 중에 분석가는 관련 탐지 규칙에 빠르고 목적에 맞게 접근해야 합니다. 플랫폼이나 대규모 규칙 저장소를 수동으로 검색하는 것은 시간이 많이 소요되며, 규칙을 활성 위협, 우선순위 행위자 또는 기법과 연계하기 어렵습니다.

## Solution
[`banshee rules`](../../reference/commands.md#banshee-rules) 명령을 사용하여 PS Banshee에서 직접 탐지 규칙을 검색, 필터링 및 검색할 수 있습니다. 규칙 유형, 위협 행위자, 악성코드 패밀리, ATT&CK 기법 등을 기준으로 필터링할 수 있습니다. Threat Map 필터링(`--threat-actor-map`, `--threat-malware-map`)을 활용하여 조직과 관련된 위협에 검색을 집중할 수 있습니다. `--limit`을 사용하면 최대 1,000개의 규칙을 검색할 수 있으며, 선택적으로 규칙 파일을 저장하여 SIEM, IDS/IPS 또는 탐지 엔지니어링 워크플로에 신속하게 배포할 수 있습니다.