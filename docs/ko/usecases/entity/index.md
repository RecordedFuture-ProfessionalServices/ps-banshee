# 엔터티 매칭 (Entity Matching)

## 사용 사례 요약
Recorded Future 엔터티(기업, 악성코드, 위협 행위자 등)를 검색하고 확인하여 Security Operations Center (SOC) 도구 및 워크플로우 전반에 걸쳐 일관된 참조를 보장합니다.

Recorded Future 엔터티에 대한 자세한 정보는 [여기](https://support.recordedfuture.com/hc/en-us/articles/115001359567-What-is-an-Entity)를 클릭하십시오.

## 문제
자유 형식의 이름은 도구와 Recorded Future 간에 불일치를 유발할 수 있습니다. 위협 행위자(Threat Actor) 엔터티는 사용자 이름(Username) 엔터티와 동일한 이름을 가질 수 있지만, 해당 엔터티 ID는 서로 달라 혼란과 잘못된 위협 인텔리전스 연관이 발생할 수 있습니다.

## 솔루션
[`banshee entity`](../../reference/commands.md#banshee-entity) 명령을 사용하여 PS Banshee에서 직접 엔터티를 검색하고 확인합니다.

- 엔터티 이름 및/또는 유형을 알고 있고 해당 엔터티 ID를 찾아야 할 경우 [`banshee entity search`](../../reference/commands.md#banshee-entity-search)를 사용하십시오.

- 엔터티 ID를 알고 있고 이름과 유형을 검색해야 할 경우 [`banshee entity lookup`](../../reference/commands.md#banshee-entity-lookup)을 사용하십시오.

올바른 엔터티 ID를 확보한 후에는 [`banshee list add`](../../reference/commands.md#banshee-list-add)와 같은 후속 PS Banshee 명령에 해당 ID를 활용하여 조직의 감시 목록(watchlist)에서 정확한 엔터티 참조를 보장하십시오.