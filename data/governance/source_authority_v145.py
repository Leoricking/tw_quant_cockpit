"""
data/governance/source_authority_v145.py — Source Authority Registry v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Lower authority cannot override higher authority.
[!] MOCK/TEST_FIXTURE/UNKNOWN → formal use NOT allowed.
"""
from __future__ import annotations

from typing import Dict, Any

from data.governance.models_v145 import SourceAuthorityLevel

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Authority level ordering (higher = more authoritative)
_AUTHORITY_ORDER = {
    SourceAuthorityLevel.PRIMARY_OFFICIAL: 100,
    SourceAuthorityLevel.PRIMARY_DOMAIN_OFFICIAL: 90,
    SourceAuthorityLevel.SECONDARY_OFFICIAL: 70,
    SourceAuthorityLevel.SECONDARY_AGGREGATOR: 50,
    SourceAuthorityLevel.SUPPLEMENTARY: 30,
    SourceAuthorityLevel.TEST_FIXTURE: 10,
    SourceAuthorityLevel.MOCK: 5,
    SourceAuthorityLevel.UNKNOWN: 0,
}

# Built-in provider → authority mappings
_BUILT_IN_MAPPINGS: Dict[str, SourceAuthorityLevel] = {
    "twse": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "twse_official": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "tpex": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "tpex_official": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "mops": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "mops_official": SourceAuthorityLevel.PRIMARY_OFFICIAL,
    "data_gov_tw": SourceAuthorityLevel.PRIMARY_DOMAIN_OFFICIAL,
    "data_gov_tw_official": SourceAuthorityLevel.PRIMARY_DOMAIN_OFFICIAL,
    "finmind": SourceAuthorityLevel.SECONDARY_AGGREGATOR,
    "fixture": SourceAuthorityLevel.TEST_FIXTURE,
    "mock": SourceAuthorityLevel.MOCK,
}


class SourceAuthorityRegistry:
    """
    Registry of provider authority levels.
    [!] Lower authority cannot override higher.
    [!] MOCK/TEST_FIXTURE/UNKNOWN → formal_use_allowed = False.
    """

    def __init__(self) -> None:
        self._mappings: Dict[str, SourceAuthorityLevel] = dict(_BUILT_IN_MAPPINGS)

    def register(self, provider_id: str, level: SourceAuthorityLevel) -> None:
        self._mappings[provider_id] = level

    def get_authority(self, provider_id: str) -> SourceAuthorityLevel:
        return self._mappings.get(provider_id, SourceAuthorityLevel.UNKNOWN)

    def can_override(
        self,
        challenger_authority: SourceAuthorityLevel,
        incumbent_authority: SourceAuthorityLevel,
    ) -> bool:
        """Lower authority cannot override higher authority."""
        return _AUTHORITY_ORDER.get(challenger_authority, 0) > _AUTHORITY_ORDER.get(incumbent_authority, 0)

    def compare_authority(self, a: SourceAuthorityLevel, b: SourceAuthorityLevel) -> int:
        """Return -1 if a < b, 0 if equal, 1 if a > b."""
        oa = _AUTHORITY_ORDER.get(a, 0)
        ob = _AUTHORITY_ORDER.get(b, 0)
        if oa < ob:
            return -1
        if oa > ob:
            return 1
        return 0

    def is_formal_allowed(self, authority_level: SourceAuthorityLevel) -> bool:
        """MOCK/TEST_FIXTURE/UNKNOWN → formal_use NOT allowed."""
        blocked = {
            SourceAuthorityLevel.MOCK,
            SourceAuthorityLevel.TEST_FIXTURE,
            SourceAuthorityLevel.UNKNOWN,
        }
        return authority_level not in blocked

    def validate_authority_decision(
        self,
        primary: SourceAuthorityLevel,
        secondary: SourceAuthorityLevel,
    ) -> Dict[str, Any]:
        """Validate that primary wins over secondary."""
        primary_order = _AUTHORITY_ORDER.get(primary, 0)
        secondary_order = _AUTHORITY_ORDER.get(secondary, 0)
        valid = primary_order >= secondary_order
        return {
            "primary": primary.value,
            "secondary": secondary.value,
            "primary_order": primary_order,
            "secondary_order": secondary_order,
            "decision": "PRIMARY_WINS",
            "valid": valid,
            "note": "Primary always wins. No auto-repair. No secondary override." if valid else "WARNING: secondary has higher authority.",
        }
