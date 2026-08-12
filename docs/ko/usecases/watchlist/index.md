# Watch List 관리

## 사용 사례 요약
Recorded Future Watch List를 활용하여 보안 운영 센터(SOC)에서 가장 중요한 항목(기업, 도메인, IP, 취약점, 임원, 공급업체)을 선별된 고우선순위 엔터티로 유지 관리함으로써, 알림과 인텔리전스가 핵심 사안에 집중될 수 있도록 합니다.

Watch List에 대한 자세한 정보는 [여기](https://support.recordedfuture.com/hc/en-us/articles/115005092427-Watch-Lists)를 클릭하십시오.

## 문제
위협 환경과 비즈니스 우선순위는 끊임없이 변화합니다. Watch List를 능동적으로 유지 관리하지 않으면, 알림과 인텔리전스의 범위가 지나치게 넓어져 분석가가 가장 중요한 사안에 신속하게 집중하기 어렵습니다.

## 해결 방법
[`banshee list`](../../reference/commands.md#banshee-list) 명령을 사용하여 PS Banshee에서 직접 Watch List를 생성하고 유지 관리합니다. 대량 변경 시에는 CSV를 업로드하고, 엔터티를 개별적으로 추가하거나, 새로운 항목의 큐레이션을 요청할 수 있습니다. Watch List를 Intelligence Goal에 매핑하여 관련 알림만 트리거되도록 설정합니다. 목록을 통합하거나 재편성할 때는 [`banshee list copy`](../../reference/commands.md#banshee-list-copy)를 사용하여 한 목록의 엔터티를 다른 목록으로 병합합니다(필요에 따라 `--overwrite` 옵션 사용 가능). 브랜드, 도메인, 임원, 공급업체, 취약점, 위치 등의 목록을 정기적으로 검토하고 갱신하여, 변화하는 위험 환경에 맞게 적용 범위가 유지되도록 합니다.