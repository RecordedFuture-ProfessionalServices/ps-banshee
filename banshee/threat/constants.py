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


from enum import Enum


class ThreatActorCategories(str, Enum):
    """Enum for threat actor categories."""

    azerbaijani_influence_operations_groups = 'azerbaijani_influence_operations_groups'
    china_nation_state_sponsored = 'china_nation_state_sponsored'
    chinese_influence_operations_groups = 'chinese_influence_operations_groups'
    dark_web_market_member = 'dark_web_market_member'
    defacement_crew = 'defacement_crew'
    farsi_hacking_community_members = 'farsi_hacking_community_members'
    financially_motivated = 'financially_motivated'
    financially_motivated_russia = 'financially_motivated_russia'
    financially_motivated_serbia = 'financially_motivated_serbia'
    france_nation_state_sponsored = 'france_nation_state_sponsored'
    fvey_related = 'fvey_related'
    germany_nation_state_sponsored = 'germany_nation_state_sponsored'
    hacktivist = 'hacktivist'
    india_nation_state_sponsored = 'india_nation_state_sponsored'
    influence_operations_groups = 'influence_operations_groups'
    iran_nation_state_sponsored = 'iran_nation_state_sponsored'
    iranian_influence_operations_groups = 'iranian_influence_operations_groups'
    islamist_forum_member = 'islamist_forum_member'
    israel_nation_state_sponsored = 'israel_nation_state_sponsored'
    lebanon_nation_state_sponsored = 'lebanon_nation_state_sponsored'
    magecart_threat_groups = 'magecart_threat_groups'
    mobile_apt = 'mobile_apt'
    msfv = 'msfv'
    nation_state_sponsored = 'nation_state_sponsored'
    nonspecific_regional = 'nonspecific_regional'
    north_korea_nation_state_sponsored = 'north_korea_nation_state_sponsored'
    pakistan_nation_state_sponsored = 'pakistan_nation_state_sponsored'
    ransomware_and_extortion_groups = 'ransomware_and_extortion_groups'
    russia_nation_state_sponsored = 'russia_nation_state_sponsored'
    russian_influence_operations_groups = 'russian_influence_operations_groups'
    south_korea_nation_state_sponsored = 'south_korea_nation_state_sponsored'
    underground_forum_drug_related = 'underground_forum_drug_related'
    underground_forum_member = 'underground_forum_member'


TA_CATEGORIES_MAP = {
    ThreatActorCategories.azerbaijani_influence_operations_groups: '1ceL6j',
    ThreatActorCategories.china_nation_state_sponsored: 'Ps4Y01',
    ThreatActorCategories.chinese_influence_operations_groups: '1ceL6i',
    ThreatActorCategories.dark_web_market_member: 'Vajy8p',
    ThreatActorCategories.defacement_crew: 'QCqLfF',
    ThreatActorCategories.farsi_hacking_community_members: 'TVQwoR',
    ThreatActorCategories.financially_motivated: 'Qn3P4k',
    ThreatActorCategories.financially_motivated_russia: 'TPtQ6J',
    ThreatActorCategories.financially_motivated_serbia: 'TPtQ6K',
    ThreatActorCategories.france_nation_state_sponsored: 'VAj58R',
    ThreatActorCategories.fvey_related: 'Qd_6Io',
    ThreatActorCategories.germany_nation_state_sponsored: 'MNQkoC',
    ThreatActorCategories.hacktivist: 'I_7J4G',
    ThreatActorCategories.india_nation_state_sponsored: 'VBD4zw',
    ThreatActorCategories.influence_operations_groups: '1cddTQ',
    ThreatActorCategories.iran_nation_state_sponsored: 'PzmSRJ',
    ThreatActorCategories.iranian_influence_operations_groups: '1ceL6h',
    ThreatActorCategories.islamist_forum_member: 'T8IJfR',
    ThreatActorCategories.israel_nation_state_sponsored: 'VQW4kV',
    ThreatActorCategories.lebanon_nation_state_sponsored: 'VEiTbf',
    ThreatActorCategories.magecart_threat_groups: 'yHAUZK',
    ThreatActorCategories.mobile_apt: 'VBBeeA',
    ThreatActorCategories.msfv: '-Aq3E3',
    ThreatActorCategories.nation_state_sponsored: 'PD_NyL',
    ThreatActorCategories.nonspecific_regional: 'PD_N2J',
    ThreatActorCategories.north_korea_nation_state_sponsored: 'Qd_6Ic',
    ThreatActorCategories.pakistan_nation_state_sponsored: 'sqRaWI',
    ThreatActorCategories.ransomware_and_extortion_groups: 'ppu8e4',
    ThreatActorCategories.russia_nation_state_sponsored: 'PzmSRI',
    ThreatActorCategories.russian_influence_operations_groups: '1cddTS',
    ThreatActorCategories.south_korea_nation_state_sponsored: 'VBD4zu',
    ThreatActorCategories.underground_forum_drug_related: 'T0CPRw',
    ThreatActorCategories.underground_forum_member: 'Turzv9',
}


def get_threat_actor_category_ids(actor_category: list[ThreatActorCategories]) -> list[str]:
    """Get threat actor category IDs from category names."""
    return (
        [TA_CATEGORIES_MAP[category.value] for category in actor_category]
        if actor_category is not None
        else []
    )
