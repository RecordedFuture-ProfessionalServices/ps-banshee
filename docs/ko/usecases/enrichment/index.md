# IOC 강화

## 사용 사례 요약
Recorded Future 위험 점수, 관련 엔티티(entity), 분석가 컨텍스트를 활용하여 침해 지표(IOC)를 강화하고, 보안 운영 센터(SOC) 트리아지 및 위협 조사를 가속화합니다.

IOC 강화에 대한 자세한 내용은 [여기](https://support.recordedfuture.com/hc/en-us/articles/115000897208-Risk-Scoring-in-Recorded-Future)를 클릭하십시오.

## 문제
분석가는 IP/도메인/URL/해시/취약점에 대해 여러 도구를 전환하며 시간을 소비하게 되어 조사가 지연되고 대응 시간이 늘어납니다. 여러 소스에 걸친 위협 인텔리전스의 수동 상관 분석은 분석의 공백을 초래하고 인시던트 대응을 지연시킵니다.

## 솔루션
[`banshee ioc`](../../reference/commands.md#banshee-ioc) 명령을 사용하여 PS Banshee에서 직접 IOC를 강화합니다. 개별 지표를 조회하여 위험 점수, AI 인사이트, 위협 행위자(threat actor)/악성코드(malware) 연관 정보를 확인합니다. 다양한 필터링 옵션을 사용하여 IOC를 검색하고 고위험 지표를 식별합니다. 강화된 컨텍스트를 활용하여 조직이 직면한 위협을 파악하고 인시던트 대응 의사 결정을 가속화합니다.