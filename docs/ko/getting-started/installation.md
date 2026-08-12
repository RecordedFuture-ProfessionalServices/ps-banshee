# PS Banshee 설치

## 설치 방법

[ps-banshee](https://pypi.org/project/ps-banshee/)를 `pipx` 또는 `pip`으로 설치합니다.

## 설치

!!! tip "PS Banshee는 Python 3.10 이상(3.13까지)이 필요합니다."

### 권장 방법: pipx (격리된 환경)
전역으로 설치하려면 다음 명령을 실행합니다:

```bash
pipx install ps-banshee
```


!!! info "pipx 설치"
    pipx가 설치되어 있지 않은 경우, [설치 가이드](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)를 참조하십시오.


### 대체 방법: pip (현재 환경)
현재 환경에 설치하려면 다음 명령을 실행합니다:
```bash
pip install ps-banshee
```


### 의존성

필요한 모든 Python 의존성은 `pip`에 의해 자동으로 해결됩니다.  
`pcap` 명령을 사용하려면 다음이 필요합니다:

- tshark 3.0.0 이상



## 인증

PS Banshee는 `RF_TOKEN` 환경 변수(권장) 또는 각 명령의 `-k` / `--api-key` 플래그를 통해 Recorded Future API 키를 읽습니다.

### 옵션 1: `RF_TOKEN` 설정 (권장)

=== "macOS / Linux"

    현재 셸에서만 적용:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    이후 셸에서도 유지 (zsh 기준 — bash의 경우 `~/.bashrc`로 변경). 이 명령을 실행한 후 새 셸을 열거나 현재 셸에 적용하려면 `source ~/.zshrc`를 실행합니다:

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    현재 세션에서만 적용:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    이후 세션에서도 유지 (이 명령을 실행한 후 새 PowerShell을 엽니다):

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    현재 세션에서만 적용:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    이후 세션에서도 유지 (이 명령을 실행한 후 새 Command Prompt를 엽니다):

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

### 옵션 2: 명령마다 `-k`로 전달

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

모든 플랫폼에서 사용 가능하지만, 더 장황하며 키가 셸 히스토리에 남을 수 있습니다.

## PS Banshee 업그레이드

PS Banshee를 최신 버전으로 업그레이드하려면 업데이트된 wheel 파일을 사용하여 재설치합니다.

!!! warning "v1.0.0 이하 버전에서 업그레이드하는 경우"
    v1.0.0 또는 이전 버전에서 업그레이드하는 경우, 새 버전을 설치하기 전에 기존 패키지를 먼저 제거해야 합니다.

    **pipx로 설치한 경우:**
    ```bash
    pipx uninstall banshee 
    pipx install ps-banshee
    ```

    **pip으로 설치한 경우:**
    ```bash
    pip uninstall banshee
    pip install ps-banshee
    ```

**pipx로 설치한 경우:**

```bash
pipx install --force ps-banshee
```

**pip으로 설치한 경우:**

```bash
pip install --upgrade ps-banshee
```

## 셸 자동 완성

PS Banshee를 설치한 후, 다음 명령으로 명령 자동 완성을 활성화합니다:

```bash
banshee --install-completion
```

설치를 완료하려면 셸을 재시작합니다. 이후 TAB 키를 사용하여 명령을 자동 완성할 수 있습니다.

## 제거

PS Banshee를 시스템에서 제거하려면 설치 방법에 맞는 명령을 사용합니다.

**pipx로 설치한 경우:**

```bash
pipx uninstall ps-banshee
```

**pip으로 설치한 경우:**

```bash
pip uninstall ps-banshee
```


## 다음 단계

PS Banshee 사용을 시작하려면 [첫 번째 단계](./first-steps.md)를 참조하십시오.