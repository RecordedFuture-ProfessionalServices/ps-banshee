#################################### TERMS OF USE ###########################################
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

from typing import Annotated

from psengine.common_models import DetectionRuleType
from typer import Option, Typer

from ..branding import banshee_cmd
from ..detection_rules import search_detection_rules
from ..threat import ThreatActorCategories
from .args import OPT_PRETTY_PRINT
from .epilogs import DETECTION_RULES_SEARCH

CMD_NAME = 'rules'
CMD_HELP = 'Search for and download detection rules'
CMD_RICH_HELP = 'Detection Rules'

app = Typer(no_args_is_help=True)


SEARCH_HELP = (
    'Search for detection rules based on the provided filter options. '
    'Results can be displayed in the console or saved to disk as individual rule files.'
    'To avoid overwhelming output, results are limited to 10 by default. '
    'Use the `--limit` option to retrieve up to 1000 rules.'
)


@banshee_cmd(app=app, help_=SEARCH_HELP, epilog=DETECTION_RULES_SEARCH)
def search(
    types: Annotated[
        list[DetectionRuleType],
        Option(
            '--type',
            '-t',
            help='Filter by rule type. Multiple types can be specified and work as a logical OR (e.g., -t yara -t snort returns rules matching either type)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    threat_actor_map: Annotated[
        bool,
        Option(
            '--threat-actor-map',
            '-T',
            help='Filter rules by threat actors from your Threat Actor Map. When enabled, detection rules associated with actors in your Threat Actor Map will be returned',  # noqa: E501
        ),
    ] = False,
    threat_actor_categories: Annotated[
        list[ThreatActorCategories],
        Option(
            '--threat-actor-category',
            '-C',
            help='Filter by threat actor categories from your Threat Actor Map. Multiple categories can be specified and work as a logical OR (e.g., -C nation_state_sponsored -C ransomware_and_extortion_groups)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    threat_malware_map: Annotated[
        bool,
        Option(
            '--threat-malware-map',
            '-M',
            help='Filter rules by malware from your Malware Threat Map. When enabled, detection rules associated with malware in your Malware Threat Map will be returned',  # noqa: E501
        ),
    ] = False,
    org_id: Annotated[
        str,
        Option(
            '--org-id',
            '-O',
            help='Specify the organization ID when fetching threat actors from a Threat Maps (requires --threat-actor-map or --threat-malware-map). Accepts values with or without the uhash: prefix. Useful for MSSP and multi-organization accounts',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    entities: Annotated[
        list[str],
        Option(
            '--entity',
            '-e',
            help='Filter by Recorded Future entity IDs associated with detection rules. Multiple entities can be specified and work as a logical OR. Use `banshee entity search` to find entity IDs (e.g., lzQ5GL for IsaacWiper malware, mitre:T1486 for Data Encrypted for Impact)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    created_after: Annotated[
        str,
        Option(
            '--created-after',
            '-a',
            help='Filter detection rules created after the specified time. Accepts relative time (e.g., 1d, 3d, 7d) or absolute date (e.g., 2024-01-01)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    created_before: Annotated[
        str,
        Option(
            '--created-before',
            '-b',
            help='Filter detection rules created before the specified time. Accepts relative time (e.g., 1d, 3d, 7d) or absolute date (e.g., 2024-01-01)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    updated_after: Annotated[
        str,
        Option(
            '--updated-after',
            '-u',
            help='Filter detection rules updated after the specified time. Accepts relative time (e.g., 1d, 3d, 7d) or absolute date (e.g., 2024-01-01)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    updated_before: Annotated[
        str,
        Option(
            '--updated-before',
            '-U',
            help='Filter detection rules updated before the specified time. Accepts relative time (e.g., 1d, 3d, 7d) or absolute date (e.g., 2024-01-01)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    rule_id: Annotated[
        str,
        Option(
            '--id',
            '-i',
            help='Filter by a specific Insikt Note document ID associated with detection rules (e.g., doc:lmRPGB)',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    title: Annotated[
        str,
        Option(
            '--title',
            '-n',
            help='Free text search for detection rules by their associated Insikt Note titles',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    limit: Annotated[
        int,
        Option(
            '--limit',
            '-l',
            help='Maximum number of detection rules to return',
            min=1,
            max=1000,
        ),
    ] = 10,
    output_path: Annotated[
        str,
        Option(
            '--output-path',
            '-o',
            help='Save the detection rules to the specified directory. Can be a relative or an absolute path. If not specified, results are printed to console.',  # noqa: E501
            show_default=False,
        ),
    ] = None,
    pretty: OPT_PRETTY_PRINT = False,
):
    search_detection_rules(
        types=types,
        threat_actor_map=threat_actor_map,
        threat_malware_map=threat_malware_map,
        threat_actor_categories=threat_actor_categories,
        org_id=org_id,
        entities=entities,
        created_after=created_after,
        created_before=created_before,
        updated_after=updated_after,
        updated_before=updated_before,
        rule_id=rule_id,
        title=title,
        limit=limit,
        output_path=output_path,
        pretty=pretty,
    )
