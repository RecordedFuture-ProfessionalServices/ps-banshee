# Environment variables

PS Banshee uses environment variables described in the sections below.

### `RF_TOKEN`

In order for PS Banshee to get authorized against Recorded Future APIs an API token is needed. The user can either set the token as an environment variable:


```bash
export RF_TOKEN=API-TOKEN
```

 or provide it as an argument `-k` or `--api-key` to the `banshee` command directly:

```bash
banshee -k API-TOKEN ca search
```


### `HTTP_PROXY`

If your organisation requires you to use a proxy then ensure you set `HTTP_PROXY`, for example:

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
```

For more information please see [requests documentation](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)

### `HTTPS_PROXY`

If your organisation requires you to use a proxy then ensure you set `HTTPS_PROXY`, for example:

```bash
export HTTPS_PROXY="http://10.10.1.10:1080"
```
For more information please see [requests documentation](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)


!!! Tip

    If using either of the proxy environment variables, you might need to disable SSL verification. This can be achieved with the `-s`, `--no-ssl-verify` flags passed to the `banshee` command directly, for example:

    $ banshee -s ca search