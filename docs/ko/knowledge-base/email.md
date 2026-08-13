# email

> 인증, 준비 상태 확인, 출력 규칙 및 공유 LLM 참고 사항은 [index.md](index.md)를 참조하십시오.

### `banshee email enrich FILE_PATH`

EML 파일을 파싱하여 헤더에서 IP를 추출하고, 본문에서 URL/도메인을, 첨부 파일에서 해시를 추출한 후, RF 위협 인텔리전스로 해당 지표를 보강합니다. 기본적으로 risk score (위험 점수) 임계값(65) 이상의 지표만 표시합니다.

| 옵션 | 단축 | 기본값 | 설명 |
|--------|-------|---------|-------------|
| `--risk-score INTEGER` | `-r` | `65` | 이 점수(0–99) 이상의 지표만 표시 |
| `--threat-hunt` | `-t` | `false` | 점수 임계값 미만이더라도 threat actor(위협 행위자)와 연관된 지표를 포함 |
| `--pretty` | `-p` | | 보기 좋게 출력 |

기본 JSON 출력은 `ioc`, `type`, `location`, `risk_score`, `first_seen`, `last_seen`, `rule_evidence`, `analyst_notes`, `malwares`, `count_of_analyst_notes`, `ta_names` 등의 필드를 포함하는 플랫 배열(flat array) 형식의 레코드입니다.

```bash
banshee email enrich phishing_email.eml
banshee email enrich phishing_submission.eml -r 1 -p

# Extract the highest-risk indicators from an enriched EML
banshee email enrich phishing_email.eml -r 1 | jq '[.[] | {ioc, type, location, score: .risk_score, top_rule: (.rule_evidence[0].rule // "")}] | sort_by(-.score)'
```