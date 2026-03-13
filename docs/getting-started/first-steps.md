# First steps with PS Banshee

After [installing PS Banshee](./installation.md), you can check that the commands are available by running the `banshee`
command:

<img src="../../img/first-steps.gif" alt="PS Banshee commands" onclick="this.src=this.src" style="cursor: pointer;" title="Click to replay">

You should see a help menu listing the available commands.

### Authorization

Provide your Recorded Future API key using the `-k` or `--api-key` argument, or set it as the `RF_TOKEN` environment variable:

```bash
banshee -k <RF_TOKEN> <command> <sub-command> <arguments>
```

### Proxies

If you are behind a proxy, set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables.

To disable SSL verification, use the `-s` flag:

```bash
banshee -s ca rules
```

## Next steps

Now that you've confirmed PS Banshee is installed jump to the [commands reference](../reference/commands.md) to start using PS Banshee, and learn how to [get help](./help.md) if you run into any issues.