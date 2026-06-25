"""
data/stable/policy_version_registry_v149.py — Policy Version Registry v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Tracks governance/quality/safety policy versions through stable baseline.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

_POLICY_REGISTRY_VERSION = "1.4.9"

_POLICY_ENTRIES: List[Dict[str, Any]] = [
    {
        "policy_id":        "source_authority",
        "description":      "Provider authority tier assignment policy",
        "version":          "1",
        "introduced_in":    "1.4.5",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "PRIMARY_OFFICIAL sources cannot be overridden by SECONDARY or SUPPLEMENTARY",
            "SECONDARY_AGGREGATOR defers on conflict",
            "SUPPLEMENTARY sources generate WARN_ONLY on conflict",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "pit_enforcement",
        "description":      "Point-in-time isolation policy",
        "version":          "1",
        "introduced_in":    "1.4.5",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "fetched_at must be set at fetch time; cannot backfill",
            "available_from must be separate from fetched_at",
            "No future leakage; no lookahead bias",
            "Forum data PIT enforced: FORUM_FUTURE_LEAKAGE_ENABLED=False",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "quality_gate",
        "description":      "Dataset admission and provider quality gate policy",
        "version":          "1",
        "introduced_in":    "1.4.6",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "Every dataset must pass admission gate before formal research use",
            "Auto-release from quarantine is not allowed",
            "Quality score < threshold triggers quarantine",
            "Blocked providers cannot feed formal backtest",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "lineage_completeness",
        "description":      "Source lineage completeness policy",
        "version":          "1",
        "introduced_in":    "1.4.5",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "source_hash required for every record",
            "normalized_hash required for derived records",
            "Incomplete lineage records blocked from formal use",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "forum_safety",
        "description":      "Forum intelligence safety policy",
        "version":          "1",
        "introduced_in":    "1.4.7",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "Forum data cannot produce standalone formal conclusions",
            "Forum data cannot generate buy/sell signals",
            "Forum cannot override official price/fundamental data",
            "Author identity inference is prohibited",
            "IP redaction is mandatory",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "rate_limit_budget",
        "description":      "Request rate limit and quota budget policy",
        "version":          "1",
        "introduced_in":    "1.4.5",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "Interactive quota reserve isolated from batch quota",
            "Batch quota reserve isolated from interactive quota",
            "Rate limit recovery is audit-logged",
            "Quota exhaustion does not trigger auto-fallback",
        ],
        "breaking_changes": [],
    },
    {
        "policy_id":        "safety_invariants",
        "description":      "Core safety invariant policy (cross-cutting)",
        "version":          "1",
        "introduced_in":    "1.3.9",
        "stable_since":     "1.4.9",
        "key_rules":        [
            "NO_REAL_ORDERS=True always",
            "BROKER_EXECUTION_ENABLED=False always",
            "PRODUCTION_TRADING_BLOCKED=True always",
            "AUTO_FALLBACK_ENABLED=False always",
            "MOCK_FALLBACK_ENABLED=False always",
        ],
        "breaking_changes": [],
    },
]


class PolicyVersionRegistry:
    """
    Registry of all governance and safety policy versions at v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _POLICY_REGISTRY_VERSION

    def get_all(self) -> List[Dict[str, Any]]:
        return list(_POLICY_ENTRIES)

    def get_by_id(self, policy_id: str) -> Dict[str, Any]:
        for p in _POLICY_ENTRIES:
            if p["policy_id"] == policy_id:
                return dict(p)
        raise KeyError(f"Unknown policy: {policy_id}")

    def validate(self) -> Dict[str, Any]:
        total = len(_POLICY_ENTRIES)
        drift = [p["policy_id"] for p in _POLICY_ENTRIES if p["breaking_changes"]]
        ok = total >= 7 and not drift
        return {
            "registry_version": self.VERSION,
            "total_policies": total,
            "breaking_changes": drift,
            "valid": ok,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = [(f"policy_{p['policy_id']}",
                  "PASS" if not p["breaking_changes"] else "FAIL",
                  f"introduced={p['introduced_in']} stable_since={p['stable_since']}")
                 for p in _POLICY_ENTRIES]
        result["items"] = items
        return result
