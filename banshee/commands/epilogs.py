##################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from ..indicators.constants import get_entity_field_map_epilog

EPILOG_IOC_SEARCH = f"""

## Verbosity Levels

{get_entity_field_map_epilog()}

## Risk Score Ranges

* --risk-score '[20,90]'  ->  same as 20 <= riskScore <= 90

* --risk-score '(20,90)'  ->  same as 20 < riskScore < 90

* --risk-score '[20,90)'  ->  same as 20 <= riskScore < 90

* --risk-score '[20,)'    ->  same as 20 <= riskScore

* --risk-score '[,90)'    ->  same as riskScore < 90


## Example Usage

* banshee ioc search ip -l 10 -r '(,80]'

* banshee ioc search domain -r '[90,)'

* banshee ioc search hash -r '[80,81]' -p

* banshee ioc search url -p

* banshee ioc search vulnerability --limit 1 -v

"""


EPILOG_IOC_LOOKUP = f"""

## Verbosity Levels

{get_entity_field_map_epilog()}

## Example Usage

* banshee ioc lookup ip 139.224.189.177

* banshee ioc lookup domain overafazg.org

* banshee ioc lookup ip 8.140.135.23 -v 3

* banshee ioc lookup ip 8.140.135.23 139.224.189.177 -p


\nPipe a comma or newline separated list of IOCs to lookup:


* cat test_ips.csv| banshee ioc lookup ip -p


## Advanced Usage


Find the most critical rule for a given IOC:


* banshee ioc lookup ... | jq '[ .[].risk.evidenceDetails[] ] | group_by(.criticality) | max_by(.[0].criticality) | .[].rule'


\nFind all the triggered rules:

* banshee ioc lookup ... | jq '.[].risk.evidenceDetails.[].rule'


\nFind risk score and most critical rule:

* banshee ioc lookup ... | jq  '[ .[] | ( [ .risk.evidenceDetails[].criticality ] | max ) as $max_crit | {{ score: .risk.score, rules: [ .risk.evidenceDetails[] | select(.criticality == $max_crit) | .rule ] }} ]'


\nFind risk score and all rules:

* banshee ioc lookup ... |jq  ' [ .[] | {{ score: .risk.score, rules: [.risk.evidenceDetails.[].rule] }} ]'
"""

EPILOG_IOC_BULK_LOOKUP = """

## Example Usage

* banshee ioc bulk-lookup ip 92.38.178.133 203.0.113.17

* banshee ioc bulk-lookup domain overafazg.org coolbeans.org -p

* banshee ioc bulk-lookup hash e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877


## File / Stdin Input

Pipe or redirect a newline-separated file of IOCs (one per line):

```

> cat cves.txt

CVE-2012-4792

CVE-2011-0611

CVE-2013-0422

CVE-2021-22204

CVE-2016-4557


```

* banshee ioc bulk-lookup vulnerability < cves.txt

* cat cves.txt | banshee ioc bulk-lookup vulnerability


## Advanced Usage

### Extract names and scores

banshee ioc bulk-lookup vulnerability CVE-2021-22204 CVE-2016-4557 | jq '[.[] | {ioc: .entity.name, risk_score: .risk.score}]'

"""

EPILOG_IOC_RULES = """

## Criticality Levels (IP, Domain, URL, Hash)

* 4      Very Malicious       Risk Score band: 90-99

* 3        Malicious          Risk Score band: 65-89

* 2        Suspicious         Risk Score band: 25-64

* 1         Unusual           Risk Score band: 5-24

* 0    No evidence of risk    Risk Score band: 0


## Criticality Levels (Vulnerability)

* 5       Very Critical      Risk Score band: 90-99

* 4         Critical         Risk Score band: 80-89

* 3           High           Risk Score band: 65-79

* 2          Medium          Risk Score band: 25-64

* 1           Low            Risk Score band: 5-24

* 0   No evidence of risk    Risk Score band: 0

## Example Usage

* banshee ioc rules ip

* banshee ioc rules domain -p

* banshee ioc rules hash -C 3

* banshee ioc rules vulnerability -M T1587.004 -C 2 -F concept

"""

EPILOG_PCAP_ANALYZER = """
## Example Usage

* banshee pcap enrich sandbox.pcap

* banshee pcap enrich honeypot-traffic.pcap -r 25 -tp

"""

EPILOG_ALERT_SEARCH = """
## Example Usage

* banshee ca search -t 1d

* banshee ca search -t "[2025-05-01, 2025-05-05]" -s Pending

* banshee ca search -t 12h -p

* banshee ca search -r "Leaked Credential Monitoring" -r "Brand Mentions with Cyber entities" -t 1d

* banshee ca search -r leaked -t 12h -p

"""  # noqa: E501

EPILOG_ALERT_LOOKUP = """
## Example Usage

* banshee ca lookup tybakN

* banshee ca lookup tybakN -p

"""

EPILOG_ALERT_RULES_SEARCH = """
## Example Usage

* banshee ca rules

* banshee ca rules -p

"""

EPILOG_ALERT_UPDATE = """
You can provide alert IDs to the update command in several ways:

1. Pass a single alert ID directly:

    > banshee ca update 8cORlQ -s Resolved

2. Pass multiple alert IDs directly (whitespace separated):

    > banshee ca update 8cORlQ 8biCIG -s Pending

3. Pipe a whitespace separated list of alert IDs:

   > cat alerts.txt | banshee ca update -s Dismissed

4. Pipe the output of `banshee ca search` via tools like `jq` to grab the alert IDs:

   > banshee ca search | jq -r '.[].id' | banshee ca update -n "Investigation started"


### Standard Input / File Input

If you have a file (e.g., `alerts.txt`) with one alert ID per line:

```

8bDNGD

8bSGtK

8bSGtJ

```

You can use either of the following commands to update the alerts:

* banshee pba update -s Dismissed < alerts.txt

* cat alerts.txt | banshee pba update -s Dismissed


## Example Usage

* banshee ca search | jq -r '.[].id' | banshee ca update -s Resolved

* banshee ca update 8bcRcG -s Resolved -r Never

* banshee ca update 8bcRcG 8biCIF -s Pending --note "Looking into this.."

* banshee ca update 8bcRcG -a Pending -a analyst@acme.com

"""


EPILOG_PBA_UPDATE = """
## Accepted Inputs

You can provide alert IDs to the update command in several ways:

1. Pass a single alert ID directly (with or without 'task:' prefix):

   > banshee pba update task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved \n\n

   > banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s Resolved

2. Pass multiple alert IDs directly (whitespace separated):

    > banshee pba update c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 a0ce3533-7438-4a6a-9cfd-9eb150fc540c -s Resolved

3. Pipe a whitespace separated list of alert IDs:

   > cat alerts.txt | banshee pba update -s Dismissed

3. Pipe the output of `banshee pba search` via tools like `jq` to grab the alert IDs:

   > banshee pba search | jq -r '.data[].playbook_alert_id' | banshee pba update -p High -c "Investigation started"


### Standard Input / File Input

If you have a file (e.g., `alerts.txt`) with one alert ID per line:

```

task:10cdcde1-d934-424d-af5c-f57aa0c25d00

task:c5dd878b-e5e2-4a19-ad28-a5b770a0aa64

task:a0ce3533-7438-4a6a-9cfd-9eb150fc540c

```

You can use either of the following commands to update the alerts:

* banshee pba update -s Dismissed < alerts.txt

* cat alerts.txt | banshee pba update -s Dismissed

## Example Usage

* banshee pba search -c domain_abuse -P Informational | jq -r '.data[].playbook_alert_id' | banshee pba update -s Resolved

* banshee pba update task:26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 -s Resolved -r Never

* banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 c5dd878b-e5e2-4a19-ad28-a5b770a0aa64 -s InProgress -p Informational -t "Bumping priority down due to recent findings."

* banshee pba update 26ca663b-a1d8-4dbd-85ef-4bd3cecaa935 -a uhash:3aXZxdkM12
"""

EPILOG_PBA_LOOKUP = """
## Example Usage

* banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c

* banshee pba lookup task:d144a9ec-90e6-40fe-89b0-d85ed65d3e9c -p


"""

EPILOG_PBA_SEARCH = """
## Example Usage

* banshee pba search --created 1d

* banshee pba search -C 1d -u 1d -p

* banshee pba search --limit 1000 --category identity_novel_exposures --category domain_abuse

* banshee pba search --updated 7d --category domain_abuse --pretty

* banshee pba search -c identity_novel_exposures -c third_party_risk -P High -P Moderate -s New

* banshee pba search -e idn:recordedfuture.com -e idn:example.com -c domain_abuse -u 7d

"""

EPILOG_ENTITY_LOOKUP = """
## Example Usage

* banshee entity lookup qf0H03

* banshee entity lookup qf0H03 -p

"""

EPILOG_ENTITY_SEARCH = """
## Example Usage

* banshee entity search wannacry

* banshee entity search "Cobalt Strike" -p

* banshee entity search "Cobalt Strike" -t Malware -t Username -p -l 20

"""

EPILOG_LIST_CREATE = """
## Example Usage

* banshee list create coolbeans

* banshee list create coolsources source -p

"""

EPILOG_LIST_INFO = """
## Example Usage

* banshee list info 1b0tFN

* banshee list info 1b0tFN -p

"""

EPILOG_LIST_STATUS = """
## Example Usage

* banshee list status 1b0tFN

"""

EPILOG_LIST_SEARCH = """
## Example Usage

* banshee list search -l 1500 -p

* banshee list search -t vulnerability

* banshee list search Attacker

* banshee list search ernest -t entity -p -l 3

"""

EPILOG_LIST_ADD = """
## Example Usage

* banshee list add 1b0s1q lYNvCK

* banshee list add 1b0s1q lYNvCK key=value,another=value

"""

EPILOG_LIST_REMOVE = """
## Example Usage

* banshee list remove 1b0s1q lYNvCK

"""

EPILOG_LIST_BULK_ADD = """
## Example Usage

Accepts both entity ID and name,type pairs.

* banshee list bulk-add report:21YKUC SoA6SP lYNvCK

* banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

### Standard Input / File Input

The command also accepts input from stdin. Each entity must be on a separate line. Assume 'entities.txt' is a newline-separated file of entities, for example:


```


> cat entities.txt

verifyaccount.otzo.com,InternetDomainName

92.38.178.133,IpAddress

https://constructorachg.cl/eFSLb6eV/j.html,URL

CVE-2019-1215,CyberVulnerability

e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877,Hash

SoA6SP

lYNvCK

```

* banshee list bulk-add 21YKUC < entities.txt

* cat entities.txt | banshee list bulk-add 21YKUC


"""

EPILOG_LIST_BULK_REMOVE = """
## Example Usage

Accepts both Entity ID and name,type pairs.

* banshee list bulk-remove 21YKUC JLHNoH lYNvCK

* banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

### Standard Input / File Input

The command also accepts input from stdin. Each entity must be on a separate line. Assume 'entities.txt' is a newline-separated file of entities, for example:


```


> cat entities.txt

verifyaccount.otzo.com,InternetDomainName

92.38.178.133,IpAddress

https://constructorachg.cl/eFSLb6eV/j.html,URL

CVE-2019-1215,CyberVulnerability

e3f236e4aeb73f8f8f0caebe46f53abbb2f71fa4b266a34ab50e01933709e877,Hash

SoA6SP

lYNvCK

```

* banshee list bulk-remove 21YKUC < entities.txt

* cat entities.txt | banshee list bulk-remove 21YKUC

"""


EPILOG_LIST_CLEAR = """
## Example Usage

* banshee list clear 1b0s1q

* banshee list clear 1b0s1

"""

EPILOG_LIST_ENTITIES = """
## Example Usage

* banshee list entities 1b0s1q

"""

EPILOG_LIST_ENTRIES = """
## Example Usage

* banshee list entries 1b0s1q

"""

RISKLIST_FETCH = """
## Example Usage

* banshee risklist fetch -e domain -l default

* banshee risklist fetch -c /custom/path/to/list.csv

* banshee risklist fetch -e ip -l recentValidatedCnc -o ./custom_name.csv

"""

RISKLIST_STAT = """
## Example Usage

* banshee risklist stat --entity-type ip --list-name ip_risklist

* banshee risklist stat -e domain -l domain_risklist

* banshee risklist stat --custom-list-path /custom/path/to/risklist.csv

* banshee risklist stat -c /custom/path/to/list.csv

"""

RISKLIST_CREATE = """
## Output Formats

* csv     Comma-separated with headers (Name, Risk, RiskString, EvidenceDetails)

* edl     Plain list of IOC values, one per line (suitable for firewalls/EDL feeds)

* json    JSON array of full risk list entries

## Example Usage

* banshee risklist create -e ip -R default -r 70 -o ip_risklist_70.csv

* banshee risklist create -e domain -R analystNote -R recentPhishing -r 80

* banshee risklist create -e ip -R recentActiveCnc -R recentValidatedCnc -f edl

* banshee risklist create -e hash -R default -f json -o /tmp/hash_risklist.json

* banshee risklist create -e ip -R recentValidatedCnc -F -o /home/risklists/ip_cnc_risklist.csv

"""

DETECTION_RULES_SEARCH = """
## Example Usage

* banshee rules search -t yara -t snort -l 20 -a 3d

* banshee rules search -t sigma --entity mitre:T1486 --entity kK5UbE

* banshee rules search --id doc:0uTafk

* banshee rules search --title Ransomware -p

* banshee rules search -t yara --output-path .

* banshee rules search --threat-actor-map -o fetched_rules

"""

EPILOG_EMAIL_ENRICH = """
## Example usage

* banshee email enrich phishing_email.eml

* banshee email enrich phishing_submission.eml -r 1 -p
"""
