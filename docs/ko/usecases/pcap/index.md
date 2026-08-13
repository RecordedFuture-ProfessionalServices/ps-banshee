# 패킷 캡처 강화

## 사용 사례 요약
패킷 캡처 파일 및 관찰된 IP/도메인을 Recorded Future Intelligence로 강화(enrich)하여 네트워크 보안 조사 및 위협 헌팅 활동을 가속화합니다.

## 문제
원시 PCAP은 네트워크 트래픽을 보여주지만 위협 컨텍스트가 부족합니다. 분석가는 위험 또는 위협 활동을 식별하기 위해 IP/도메인을 수동으로 조회해야 하며, 이는 시간이 많이 소요되고 대량 조사 중 간과하기 쉽습니다.

## 해결책
[`banshee pcap`](../../reference/commands.md#banshee-pcap) 명령을 사용하여 PS Banshee에서 직접 네트워크 트래픽을 강화합니다. [`banshee pcap enrich`](../../reference/commands.md#banshee-pcap-enrich)를 사용하여 패킷 캡처를 자동으로 파싱하고, 관찰된 인디케이터(indicator)를 위협 인텔리전스로 강화한 후, 결과를 터미널에 직접 표시합니다. 강화된 IOC(침해 지표)를 [`banshee ioc lookup`](../../reference/commands.md#banshee-ioc-lookup)으로 파이프하여 심층 분석을 수행하거나, 고위험 인디케이터를 Watch List에 추가하여 장기적인 추적 및 모니터링을 진행합니다.