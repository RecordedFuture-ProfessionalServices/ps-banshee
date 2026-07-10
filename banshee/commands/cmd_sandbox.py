##################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly "as-is" and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from typing import Annotated, Optional

from typer import Option, Typer

from ..branding import banshee_cmd
from ..sandbox import fetch_sandbox_stats, print_sandbox_stats
from .args import OPT_PRETTY_PRINT

CMD_NAME = 'sandbox'
CMD_HELP = 'Sandbox submission analytics'
CMD_RICH_HELP = 'Sandbox'

_HELP_STATS = (
    'Aggregate sandbox submissions over a configurable window and print a '
    '"morning brief" suitable for SOC shift handover or daily triage. '
    'Shows submission volume, score distribution, top malware families, platform '
    'coverage, extracted C2s, and SOAR-validated network IOCs. '
    'Default output is JSON; use `--pretty` for a human-readable Rich layout.'
)

_EPILOG_STATS = """
## Score buckets (Triage 1–10 scale)

| Bucket | Range | Meaning |
|--------|-------|---------|
| malicious | 8–10 | Known malware, high confidence |
| suspicious | 5–7 | Strong behavioural indicators |
| potentially_suspicious | 3–4 | Some indicators |
| clean | 1–2 | Low risk / benign |

## Examples

```
banshee sandbox stats
banshee sandbox stats --days 14 --subset owned --pretty
banshee sandbox stats --days 30 --limit 500
banshee sandbox stats --pretty --hashes
```
"""

app = Typer(no_args_is_help=True)


@banshee_cmd(app=app, help_=_HELP_STATS, epilog=_EPILOG_STATS)
def stats(
    days: Annotated[
        int,
        Option('--days', '-d', help='Lookback window in days', min=1),
    ] = 7,
    subset: Annotated[
        str,
        Option(
            '--subset',
            '-s',
            help="Sample scope: 'org' (org-wide) or 'owned' (current user)",
        ),
    ] = 'org',
    limit: Annotated[
        Optional[int],
        Option(
            '--limit',
            '-l',
            help='Cap on total samples fetched (default: 2000). Prints a warning if hit.',
            min=1,
        ),
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
    hashes: Annotated[
        bool,
        Option('--hashes', '-H', help='Show top 20 malicious SHA256s (pretty mode only)'),
    ] = False,
):
    result = fetch_sandbox_stats(days=days, subset=subset, limit=limit or 0)
    print_sandbox_stats(result, pretty=pretty, show_hashes=hashes)
