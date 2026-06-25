"""
data/stable/provider_registry_v149.py — Stable Provider Registry v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Formally certifies six providers as STABLE with fixed authority tiers.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List

_REGISTRY_VERSION = "1.4.9"


@dataclass(frozen=True)
class ProviderRegistryEntry:
    provider_id:     str
    display_name:    str
    authority_tier:  str   # PRIMARY_OFFICIAL | SECONDARY_AGGREGATOR | SUPPLEMENTARY
    stable_since:    str
    introduced_in:   str
    data_type:       str
    pit_supported:   bool
    lineage_tracked: bool
    conflict_policy: str
    notes:           str = ""


_REGISTRY: List[ProviderRegistryEntry] = [
    ProviderRegistryEntry(
        provider_id     = "twse_official",
        display_name    = "TWSE Official",
        authority_tier  = "PRIMARY_OFFICIAL",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.0",
        data_type       = "equity_price_official",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "PRIMARY_WINS",
        notes           = "Taiwan Stock Exchange — authoritative price source",
    ),
    ProviderRegistryEntry(
        provider_id     = "tpex_official",
        display_name    = "TPEx Official",
        authority_tier  = "PRIMARY_OFFICIAL",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.1",
        data_type       = "otc_price_official",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "PRIMARY_WINS",
        notes           = "Taipei Exchange — authoritative OTC price source",
    ),
    ProviderRegistryEntry(
        provider_id     = "mops_official",
        display_name    = "MOPS Official",
        authority_tier  = "PRIMARY_OFFICIAL",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.2",
        data_type       = "fundamental_official",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "PRIMARY_WINS",
        notes           = "Market Observation Post System — authoritative fundamental source",
    ),
    ProviderRegistryEntry(
        provider_id     = "data_gov_tw_official",
        display_name    = "data.gov.tw Official",
        authority_tier  = "PRIMARY_OFFICIAL",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.3",
        data_type       = "domain_specific_official",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "PRIMARY_WINS",
        notes           = "Taiwan government open data — domain-specific authority",
    ),
    ProviderRegistryEntry(
        provider_id     = "finmind_aggregator",
        display_name    = "FinMind Aggregator",
        authority_tier  = "SECONDARY_AGGREGATOR",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.4",
        data_type       = "aggregated_market_data",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "SECONDARY_DEFER",
        notes           = "FinMind — secondary aggregator; cannot override primary providers",
    ),
    ProviderRegistryEntry(
        provider_id     = "ptt_stock",
        display_name    = "PTT Stock Board",
        authority_tier  = "SUPPLEMENTARY",
        stable_since    = "1.4.9",
        introduced_in   = "1.4.7",
        data_type       = "forum_sentiment",
        pit_supported   = True,
        lineage_tracked = True,
        conflict_policy = "WARN_ONLY",
        notes           = "PTT forum — supplementary sentiment only; no formal conclusions standalone",
    ),
]


class StableProviderRegistry:
    """
    Stable registry for all six certified providers at v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _REGISTRY_VERSION

    # Safety constraints — ALWAYS FALSE
    FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
    PTT_STANDALONE_FORMAL_CONCLUSION      = False
    PTT_CAN_GENERATE_BUY_SELL             = False

    def get_all(self) -> List[ProviderRegistryEntry]:
        return list(_REGISTRY)

    def get_by_id(self, provider_id: str) -> ProviderRegistryEntry:
        for p in _REGISTRY:
            if p.provider_id == provider_id:
                return p
        raise KeyError(f"Unknown provider: {provider_id}")

    def get_by_tier(self, tier: str) -> List[ProviderRegistryEntry]:
        return [p for p in _REGISTRY if p.authority_tier == tier]

    def validate(self) -> Dict[str, Any]:
        total = len(_REGISTRY)
        primary = len(self.get_by_tier("PRIMARY_OFFICIAL"))
        secondary = len(self.get_by_tier("SECONDARY_AGGREGATOR"))
        supplementary = len(self.get_by_tier("SUPPLEMENTARY"))
        ok = (
            total == 6
            and primary == 4
            and secondary == 1
            and supplementary == 1
            and not self.FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER
            and not self.PTT_STANDALONE_FORMAL_CONCLUSION
            and not self.PTT_CAN_GENERATE_BUY_SELL
        )
        return {
            "registry_version": self.VERSION,
            "total_providers": total,
            "primary_official": primary,
            "secondary_aggregator": secondary,
            "supplementary": supplementary,
            "finmind_override_blocked": not self.FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER,
            "ptt_standalone_blocked": not self.PTT_STANDALONE_FORMAL_CONCLUSION,
            "ptt_buy_sell_blocked": not self.PTT_CAN_GENERATE_BUY_SELL,
            "valid": ok,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = []
        for p in _REGISTRY:
            items.append((f"provider_{p.provider_id}",
                          "PASS" if p.stable_since == "1.4.9" else "WARN",
                          f"tier={p.authority_tier} pit={p.pit_supported}"))
        result["items"] = items
        return result
