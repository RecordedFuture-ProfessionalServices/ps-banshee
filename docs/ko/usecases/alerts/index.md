# Alert Management

## Use Case Summary
Recorded Future 알림(Classic & Playbook)을 터미널에서 직접 관리, 분류, 일괄 업데이트하여 보안 운영 센터(SOC) 대응 및 조사 워크플로우를 가속화합니다.

## Issue
알림이 발생할 때마다 UI로 전환하면 조사가 지연되어 분석가 피로와 일관성 없는 알림 처리로 이어집니다. 수동 분류 프로세스는 인시던트 대응을 느리게 하고 보안 운영 워크플로우에 병목 현상을 초래합니다.

## Solution
[`banshee ca`](../../reference/commands.md#banshee-ca) 및 [`banshee pba`](../../reference/commands.md#banshee-pba) 명령을 사용하여 터미널에서 직접 Recorded Future 알림을 검색하고 관리합니다.

- Classic Alert의 경우, [`banshee ca search`](../../reference/commands.md#banshee-ca-search)를 시간 필터와 함께 사용하고, [`banshee ca update`](../../reference/commands.md#banshee-ca-update)를 통해 상태 일괄 변경, 메모 추가, 담당자 업데이트를 수행합니다.

- Playbook Alert의 경우, [`banshee pba search`](../../reference/commands.md#banshee-pba-search)를 카테고리 및 우선순위 필터와 함께 활용한 후, [`banshee pba update`](../../reference/commands.md#banshee-pba-update)를 사용하여 상태 수정, 댓글 추가, 사용자 지정, 재오픈 전략 설정을 수행합니다.

- 두 검색 결과 모두 [`banshee ca export`](../../reference/commands.md#banshee-ca-export) 또는 [`banshee pba export`](../../reference/commands.md#banshee-pba-export)로 파이프하여 전체 알림 상세 정보를 JSON으로 캡처하거나, `--csv` 옵션을 추가하여 오프라인 보고 및 공유를 위한 스프레드시트 형식의 요약본을 생성할 수 있습니다.

이 접근 방식은 분류 속도를 높이고 알림 일관성을 유지하며, 분석가가 일괄 작업을 통해 여러 알림을 동시에 업데이트할 수 있도록 합니다.