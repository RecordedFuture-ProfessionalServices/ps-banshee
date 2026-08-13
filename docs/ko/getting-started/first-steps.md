# PS Banshee 시작하기

[PS Banshee 설치](./installation.md) 후, [banshee](../reference/commands.md#banshee) 명령을 실행하여 명령어가 사용 가능한지 확인할 수 있습니다:

<img src="../../img/first-steps.gif" alt="PS Banshee commands" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

사용 가능한 명령어 목록이 포함된 도움말 메뉴가 표시됩니다.

### 인증

--8<-- "_includes/authorization.md"

### 프록시

프록시 환경에서 사용하는 경우, `HTTP_PROXY` 및 `HTTPS_PROXY` 환경 변수를 설정하십시오.

SSL 검증을 비활성화하려면 `-s` 플래그를 사용하십시오:

```bash
banshee -s ca rules
```

## 다음 단계

PS Banshee가 설치되었음을 확인하였다면 [명령어 참조](../reference/commands.md)로 이동하여 PS Banshee 사용을 시작하고, 문제가 발생할 경우 [도움말 받기](./help.md) 방법을 확인하십시오.