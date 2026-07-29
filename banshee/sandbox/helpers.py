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

from datetime import datetime

from psengine.common_models import RFBaseModel
from psengine.config import get_config
from psengine.sandbox import SandboxMgr
from pydantic import Field
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .constants import SCORE_BUCKETS


def get_sandbox_mgr() -> SandboxMgr:
    return SandboxMgr(sandbox_choice=get_config().sandbox_choice)


def spinner(label: str) -> Progress:
    progress = Progress(
        SpinnerColumn(), TextColumn(label), transient=True, console=Console(stderr=True)
    )
    progress.add_task('')
    return progress


def score_bucket(score: int | None) -> str:
    if score is None:
        return 'unknown'
    for threshold, bucket in SCORE_BUCKETS:
        if score >= threshold:
            return bucket
    return 'clean'


class TopTags(RFBaseModel):
    """Classified tag counts from overview reports."""

    malware_families: dict = Field(default_factory=dict)
    botnets: dict = Field(default_factory=dict)
    arch_file: dict = Field(default_factory=dict)
    behavioral_ttp: dict = Field(default_factory=dict)


class VerifiedIoc(RFBaseModel):
    """A SOAR-validated network indicator."""

    indicator: str
    type: str
    rf_score: int
    most_critical_rule: str


class TopIocs(RFBaseModel):
    """Extracted and verified IOCs from malicious samples."""

    extracted_c2: list = Field(default_factory=list)
    verified_network: list = Field(default_factory=list)
    malicious_sha256: list = Field(default_factory=list)
    c2_soar: dict = Field(default_factory=dict)


class SandboxStats(RFBaseModel):
    """Aggregated sandbox submission statistics for a time window."""

    period_start: datetime
    period_end: datetime
    period_days: int
    subset: str
    total: int
    pending: int
    failed: int
    by_kind: dict
    by_platform: dict
    by_score: dict
    top_tags: TopTags
    top_iocs: TopIocs
    trend_vs_prior_period: dict
    soar_skipped: bool = False
    sandbox_choice: str = 'eu'
    by_kind_prev: dict = Field(default_factory=dict)
    by_file_type: dict = Field(default_factory=dict)
    daily_by_family: dict = Field(default_factory=dict)
