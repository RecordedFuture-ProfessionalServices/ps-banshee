---
title: ""
---

<div style="width: 100%; text-align: center;">
    <img src="assets/rf-logo.png" alt="Recorded Future Logo" style="margin-top: -80px; margin-bottom: 16px;">
</div>
<p style="margin-top: -60px;">
PS Banshee는 보안 전문가 및 SOC 팀을 위해 구축된 Recorded Future Intelligence에 빠르고 효율적으로 액세스하기 위한 명령줄 도구입니다.
</p>
<img src="img/welcome.gif" alt="Welcome to PS Banshee!" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

!!! tip "PSEngine 기반"
    PS Banshee는 [PSEngine](https://recordedfuture-professionalservices.github.io/psengine/latest/) 라이브러리를 기반으로 합니다.

---

## 주요 기능

- 이메일(EML) 강화(enrichment)
- IOC 조회 및 검색
- 패킷 캡처(pcap) 강화
- Recorded Future Alert 검색, 조회, 업데이트 및 내보내기
- Recorded Future 탐지 규칙(YARA, Snort, Sigma) 검색 및 다운로드
- Recorded Future 엔티티 검색 및 조회
- Recorded Future 리스트 및 Watch List 관리
- Recorded Future Playbook Alert 검색, 조회, 업데이트 및 내보내기
- Recorded Future Risk List 다운로드 및 생성

## 설치

PS Banshee는 [PyPI](https://pypi.org/project/ps-banshee/)에서 제공되며 `pip` 또는 `pipx`를 사용하여 설치할 수 있습니다.

!!! tip "PS Banshee는 Python 3.10 이상(최대 3.13)이 필요합니다."

### 권장 방법: pipx (격리된 환경)
전역으로 설치하려면 다음을 실행하십시오:

```bash
pipx install ps-banshee
```


!!! info "pipx 설치"
    pipx가 설치되어 있지 않은 경우 [설치 가이드](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)를 참조하십시오.


### 대체 방법: pip (현재 환경)
현재 환경에 설치하려면 다음을 실행하십시오:
```bash
pip install ps-banshee
```

### 의존성

필요한 모든 Python 의존성은 `pipx`에 의해 자동으로 해결됩니다.  
`pcap` 명령을 사용하려면 다음이 필요합니다:

- tshark 3.0.0 이상

### 명령 자동 완성

PS Banshee를 설치한 후 다음 명령으로 명령 자동 완성을 활성화하십시오:

```bash
banshee --install-completion
```

설치를 완료하려면 셸을 재시작하십시오. 이후 TAB 키를 사용하여 명령을 자동 완성할 수 있습니다.

## 문서

사용 가능한 명령을 보려면 다음을 실행하십시오:

```bash
banshee
```

### 인증

--8<-- "_includes/authorization.md"

### 프록시

프록시 환경에 있는 경우 `HTTP_PROXY` 및 `HTTPS_PROXY` 환경 변수를 설정하십시오.

SSL 검증을 비활성화하려면 `-s` 플래그를 사용하십시오:

```bash
banshee -s ca rules
```

## 다음 단계

지금 바로 PS Banshee [시작하기](getting-started/index.md)를 이용해 보십시오!