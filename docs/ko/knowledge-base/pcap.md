# pcap

> 인증, 준비 상태 확인, 출력 규칙, 공유 LLM 관련 참고 사항은 [index.md](index.md)를 참조하십시오.

> **사전 요구 사항:** `tshark`가 설치되어 있고 `PATH`에 등록되어 있어야 합니다. Banshee 1.2.0에서는 `tshark`가 누락된 경우 `banshee pcap enrich --help`도 실패하므로, 먼저 `command -v tshark`로 확인하십시오.

### `banshee pcap enrich FILE_PATH`

pcap 파일을 파싱하여 IP 및 도메인을 추출하고, RF 위협 인텔리전스로 보강합니다. 기본적으로 위험 점수 임계값(65) 이상의 지표만 표시합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | 이 점수(1–99) 이상의 지표만 표시 |
| `--threat-hunt` | `-t` | `false` | 점수 임계값 미만이더라도 위협 행위자와 연결된 지표를 포함 (소급 위협 헌팅) |
| `--pretty` | `-p` | | 보기 좋게 출력 |

기본 JSON 출력은 `ioc`, `risk_score`, `most_malicious_rule`, `rule_evidence`, `ta_names`, `malwares`, `wireshark_query` 등의 필드를 포함하는 레코드의 단순 배열입니다.

```bash
banshee pcap enrich sandbox.pcap
banshee pcap enrich honeypot-traffic.pcap -r 25 -t -p

# Summarize hits from JSON output
banshee pcap enrich sandbox.pcap -r 25 -t | jq '[.[] | {indicator: .ioc, score: .risk_score, top_rule: .most_malicious_rule, evidence_rules: [(.rule_evidence // [])[].rule]}] | sort_by(-.score)'
```