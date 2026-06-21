"""
data/stable/provider_stable_profiles_v149.py — Provider Stable Profiles v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Formally certifies six provider stable profiles with fixed authority tiers.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, List

_PROFILES_VERSION = "1.4.9"


@dataclass(frozen=True)
class ProviderStableProfile:
    provider_id:         str
    display_name:        str
    authority_tier:      str
    stability_status:    str   # STABLE
    introduced_in:       str
    stable_since:        str
    data_domains:        tuple
    pit_enforced:        bool
    lineage_required:    bool
    quality_gate_active: bool
    # Safety constraints
    can_override_primary:       bool = False  # ALWAYS FALSE for non-primary
    standalone_formal_allowed:  bool = False
    buy_sell_allowed:           bool = False
    notes: str = ""


_PROFILES: List[ProviderStableProfile] = [
    ProviderStableProfile(
        provider_id         = "twse_official",
        display_name        = "Taiwan Stock Exchange (TWSE)",
        authority_tier      = "PRIMARY_OFFICIAL",
        stability_status    = "STABLE",
        introduced_in       = "1.4.0",
        stable_since        = "1.4.9",
        data_domains        = ("equity_price", "market_index", "corporate_actions",
                               "institutional_flow", "margin"),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,
        standalone_formal_allowed  = True,   # primary source — formal use allowed
        buy_sell_allowed           = False,  # still research only
        notes               = "Authoritative price source; PRIMARY authority; no broker execution",
    ),
    ProviderStableProfile(
        provider_id         = "tpex_official",
        display_name        = "Taipei Exchange (TPEx)",
        authority_tier      = "PRIMARY_OFFICIAL",
        stability_status    = "STABLE",
        introduced_in       = "1.4.1",
        stable_since        = "1.4.9",
        data_domains        = ("otc_price", "otc_index", "corporate_actions",
                               "institutional_flow", "valuation", "suspensions"),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,
        standalone_formal_allowed  = True,
        buy_sell_allowed           = False,
        notes               = "Authoritative OTC source; PRIMARY authority; no broker execution",
    ),
    ProviderStableProfile(
        provider_id         = "mops_official",
        display_name        = "Market Observation Post System (MOPS)",
        authority_tier      = "PRIMARY_OFFICIAL",
        stability_status    = "STABLE",
        introduced_in       = "1.4.2",
        stable_since        = "1.4.9",
        data_domains        = ("revenue", "income_statement", "balance_sheet",
                               "cash_flow", "material_info", "xbrl"),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,
        standalone_formal_allowed  = True,
        buy_sell_allowed           = False,
        notes               = "Authoritative fundamental source; revision lineage tracked",
    ),
    ProviderStableProfile(
        provider_id         = "data_gov_tw_official",
        display_name        = "Taiwan Government Open Data (data.gov.tw)",
        authority_tier      = "PRIMARY_OFFICIAL",
        stability_status    = "STABLE",
        introduced_in       = "1.4.3",
        stable_since        = "1.4.9",
        data_domains        = ("domain_specific_government_data",),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,
        standalone_formal_allowed  = True,
        buy_sell_allowed           = False,
        notes               = "Domain-specific official authority; allowlist admission enforced",
    ),
    ProviderStableProfile(
        provider_id         = "finmind_aggregator",
        display_name        = "FinMind Data Aggregator",
        authority_tier      = "SECONDARY_AGGREGATOR",
        stability_status    = "STABLE",
        introduced_in       = "1.4.4",
        stable_since        = "1.4.9",
        data_domains        = ("aggregated_price", "aggregated_fundamental",
                               "aggregated_institutional"),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,  # ALWAYS FALSE
        standalone_formal_allowed  = False,  # cannot be sole source for formal research
        buy_sell_allowed           = False,
        notes               = "Secondary aggregator; defers to primary on conflict; no override",
    ),
    ProviderStableProfile(
        provider_id         = "ptt_stock",
        display_name        = "PTT Stock Discussion Board",
        authority_tier      = "SUPPLEMENTARY",
        stability_status    = "STABLE",
        introduced_in       = "1.4.7",
        stable_since        = "1.4.9",
        data_domains        = ("forum_sentiment", "retail_opinion"),
        pit_enforced        = True,
        lineage_required    = True,
        quality_gate_active = True,
        can_override_primary       = False,  # ALWAYS FALSE
        standalone_formal_allowed  = False,  # ALWAYS FALSE
        buy_sell_allowed           = False,  # ALWAYS FALSE
        notes               = "Supplementary sentiment only; no standalone conclusions; no buy/sell",
    ),
]

_PROFILES_BY_ID: Dict[str, ProviderStableProfile] = {p.provider_id: p for p in _PROFILES}


class ProviderStableProfileRegistry:
    """
    Registry of six certified provider stable profiles at v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _PROFILES_VERSION

    # Safety constraints — mirrored at module level for easy assertion
    FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
    PTT_STANDALONE_FORMAL_CONCLUSION      = False
    PTT_CAN_GENERATE_BUY_SELL             = False

    def get_all(self) -> List[ProviderStableProfile]:
        return list(_PROFILES)

    def get_by_id(self, provider_id: str) -> ProviderStableProfile:
        if provider_id not in _PROFILES_BY_ID:
            raise KeyError(f"Unknown provider: {provider_id}")
        return _PROFILES_BY_ID[provider_id]

    def get_by_tier(self, tier: str) -> List[ProviderStableProfile]:
        return [p for p in _PROFILES if p.authority_tier == tier]

    def validate(self) -> Dict[str, Any]:
        total = len(_PROFILES)
        non_stable = [p.provider_id for p in _PROFILES if p.stability_status != "STABLE"]
        override_violations = [p.provider_id for p in _PROFILES
                               if p.authority_tier != "PRIMARY_OFFICIAL"
                               and p.can_override_primary]
        ptt = _PROFILES_BY_ID.get("ptt_stock")
        ptt_ok = (ptt is not None
                  and not ptt.standalone_formal_allowed
                  and not ptt.buy_sell_allowed)
        finmind = _PROFILES_BY_ID.get("finmind_aggregator")
        finmind_ok = finmind is not None and not finmind.can_override_primary
        ok = (total == 6 and not non_stable and not override_violations
              and ptt_ok and finmind_ok)
        return {
            "profiles_version": self.VERSION,
            "total_profiles": total,
            "non_stable": non_stable,
            "override_violations": override_violations,
            "ptt_constraints_enforced": ptt_ok,
            "finmind_constraints_enforced": finmind_ok,
            "valid": ok,
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = [(p.provider_id,
                  "PASS" if p.stability_status == "STABLE" else "FAIL",
                  f"tier={p.authority_tier} pit={p.pit_enforced}")
                 for p in _PROFILES]
        result["items"] = items
        return result
