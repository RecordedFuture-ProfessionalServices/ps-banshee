# Getting help

## Help menus

The `--help`, `-h` flag can be used to view the help menu for a command, e.g., for `banshee`:

```bash
$ banshee --help
```

To view the help menu for a specific command, e.g., for `banshee pcap`:

```bash
$ banshee pcap --help
```

## Viewing the version

When seeking help, it's important to determine the version of ps-banshee package that you're using — sometimes the
problem is already solved in a newer version.

To check the installed version:

```bash
$ banshee --version
```

## Troubleshooting issues

## Errors

To enhance the error if a command is failing in unexpected ways,  the `--debug` flag can be used:

```bash
banshee --debug ioc search ip -p
```

The output will display where exactly `banshee` is failing over. This information can then be passed to our support team to aid you in troubleshooting.

## Open a support case with Recorded Future Support

Submit a [support request](https://support.recordedfuture.com/hc/en-us/requests/new) for help alternatively reach out to [support@recordedfuture.com](mailto:support@recordedfuture.com).