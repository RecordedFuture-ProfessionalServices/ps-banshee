# 도움말 가져오기

## 도움말 메뉴

`--help`, `-h` 플래그를 사용하여 명령의 도움말 메뉴를 볼 수 있습니다. 예를 들어 [banshee](../reference/commands.md#banshee)의 경우:

```bash
banshee --help
```

특정 명령의 도움말 메뉴를 보려면, 예를 들어 [banshee pcap](../reference/commands.md#banshee-pcap)의 경우:

```bash
banshee pcap --help
```

## 버전 확인

도움을 요청할 때는 현재 사용 중인 ps-banshee 패키지의 버전을 확인하는 것이 중요합니다. 경우에 따라 문제가 최신 버전에서 이미 해결되어 있을 수 있습니다.

설치된 버전을 확인하려면:

```bash
banshee --version
```

## 문제 해결

명령이 예기치 않은 방식으로 실패하는 경우 오류 정보를 보강하기 위해 `--debug` 플래그를 사용할 수 있습니다:

```bash
banshee --debug ioc search ip -p
```

출력 결과에는 명령이 실패하는 정확한 위치가 표시됩니다. 이 정보를 지원 팀에 전달하여 문제 해결에 활용할 수 있습니다.

## Recorded Future 지원팀에 지원 케이스 열기

[지원 요청](https://support.recordedfuture.com/hc/en-us/requests/new)을 제출하거나 [support@recordedfuture.com](mailto:support@recordedfuture.com)으로 문의하시기 바랍니다.