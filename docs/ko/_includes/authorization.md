PS Banshee는 `RF_TOKEN` 환경 변수(권장) 또는 각 명령의 `-k` / `--api-key` 플래그에서 Recorded Future API 키를 읽습니다.

#### Option 1: `RF_TOKEN` 설정 (권장)

=== "macOS / Linux"

    현재 셸에서만 적용:

    ```bash
    export RF_TOKEN=<your_api_key>
    ```

    이후 셸에서도 유지 (zsh 기준 — bash의 경우 `~/.bashrc`로 변경). 실행 후 새 셸을 열거나 (`source ~/.zshrc`를 실행하면 현재 셸에 즉시 적용):

    ```bash
    echo 'export RF_TOKEN=<your_api_key>' >> ~/.zshrc
    ```

=== "Windows (PowerShell)"

    현재 세션에서만 적용:

    ```powershell
    $env:RF_TOKEN = '<your_api_key>'
    ```

    이후 세션에서도 유지 (실행 후 새 PowerShell을 여십시오):

    ```powershell
    setx RF_TOKEN <your_api_key>
    ```

=== "Windows (Command Prompt)"

    현재 세션에서만 적용:

    ```cmd
    set RF_TOKEN=<your_api_key>
    ```

    이후 세션에서도 유지 (실행 후 새 Command Prompt를 여십시오):

    ```cmd
    setx RF_TOKEN <your_api_key>
    ```

#### Option 2: 명령마다 `-k`로 전달

```bash
banshee -k <your_api_key> <command> <sub-command> <arguments>
```

모든 플랫폼에서 사용할 수 있지만, 입력이 더 번거로우며 키가 셸 히스토리에 기록될 수 있습니다.