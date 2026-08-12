# 환경 변수

PS Banshee는 아래 섹션에서 설명하는 환경 변수를 사용합니다.

### `RF_TOKEN`

PS Banshee가 Recorded Future API에 대해 인증을 받으려면 API 토큰이 필요합니다. 사용자는 토큰을 환경 변수로 설정할 수 있습니다:


```bash
export RF_TOKEN=API-TOKEN
```

 또는 `banshee` 명령에 직접 `-k` 또는 `--api-key` 인수로 제공할 수 있습니다:

```bash
banshee -k API-TOKEN ca search
```


### `HTTP_PROXY`

조직에서 프록시 사용을 요구하는 경우, 다음과 같이 `HTTP_PROXY`를 설정하십시오:

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
```

자세한 내용은 [requests 문서](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)를 참조하십시오.

### `HTTPS_PROXY`

조직에서 프록시 사용을 요구하는 경우, 다음과 같이 `HTTPS_PROXY`를 설정하십시오:

```bash
export HTTPS_PROXY="http://10.10.1.10:1080"
```
자세한 내용은 [requests 문서](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)를 참조하십시오.


!!! Tip

    프록시 환경 변수 중 하나를 사용하는 경우, SSL 검증을 비활성화해야 할 수 있습니다. 이는 `banshee` 명령에 직접 `-s`, `--no-ssl-verify` 플래그를 전달하여 수행할 수 있습니다. 예를 들면 다음과 같습니다:

    $ banshee -s ca search