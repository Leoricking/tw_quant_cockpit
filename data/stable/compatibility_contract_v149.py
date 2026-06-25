"""
data/stable/compatibility_contract_v149.py — Compatibility Contract Registry v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Documents stable compatibility guarantees between providers and consumers.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

_CONTRACT_VERSION = "1.4.9"


_CONTRACTS: List[Dict[str, Any]] = [
    {
        "contract_id":  "c001",
        "provider":     "twse_official",
        "consumer":     "empirical_backtest",
        "guarantee":    "PIT price data always available for backtesting; fetched_at separate from available_from",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c002",
        "provider":     "twse_official",
        "consumer":     "coverage_repair",
        "guarantee":    "Gap detection based on calendar business days; repair uses TWSE only",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c003",
        "provider":     "tpex_official",
        "consumer":     "empirical_backtest",
        "guarantee":    "OTC price PIT semantics identical to TWSE contract",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c004",
        "provider":     "mops_official",
        "consumer":     "abc_validation",
        "guarantee":    "Fundamental data point-in-time; no future leakage; revision lineage tracked",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c005",
        "provider":     "finmind_aggregator",
        "consumer":     "empirical_backtest",
        "guarantee":    "FinMind values supplementary only; conflicts resolved in favor of primary; no override",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c006",
        "provider":     "ptt_stock",
        "consumer":     "market_sentiment",
        "guarantee":    "Forum data supplementary; no standalone formal conclusion; no buy/sell signal",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c007",
        "provider":     "data_gov_tw_official",
        "consumer":     "provider_quality_gates",
        "guarantee":    "Domain dataset admission gate enforced; allowlist checked before every fetch",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
    {
        "contract_id":  "c008",
        "provider":     "all_providers",
        "consumer":     "source_lineage",
        "guarantee":    "source_hash and normalized_hash required; lineage record mandatory for every fetch",
        "breaking_changes_allowed": False,
        "stable_since": "1.4.9",
    },
]


class CompatibilityContractRegistry:
    """
    Registry of all stable compatibility contracts at v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _CONTRACT_VERSION

    def get_all(self) -> List[Dict[str, Any]]:
        return list(_CONTRACTS)

    def get_by_id(self, contract_id: str) -> Dict[str, Any]:
        for c in _CONTRACTS:
            if c["contract_id"] == contract_id:
                return dict(c)
        raise KeyError(f"Unknown contract: {contract_id}")

    def get_by_provider(self, provider_id: str) -> List[Dict[str, Any]]:
        return [c for c in _CONTRACTS
                if c["provider"] == provider_id or c["provider"] == "all_providers"]

    def validate(self) -> Dict[str, Any]:
        total = len(_CONTRACTS)
        breaking_allowed = [c["contract_id"] for c in _CONTRACTS if c["breaking_changes_allowed"]]
        ok = total >= 8 and len(breaking_allowed) == 0
        return {
            "contract_version": self.VERSION,
            "total_contracts": total,
            "breaking_changes_allowed": breaking_allowed,
            "valid": ok,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = [(f"contract_{c['contract_id']}",
                  "PASS" if not c["breaking_changes_allowed"] else "FAIL",
                  f"{c['provider']}→{c['consumer']}")
                 for c in _CONTRACTS]
        result["items"] = items
        return result
