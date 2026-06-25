"""
data/stable/capability_manifest_v149.py — Stable Capability Manifest v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Certifies all capabilities stable through v1.4.8 Provider Integration Hardening.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

_MANIFEST_VERSION = "1.4.9"

_STABLE_CAPABILITIES: List[Dict[str, Any]] = [
    # v1.3.x Research Foundation capabilities
    {"id": "real_data_quality",               "since": "1.3.0", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "universe_expansion",              "since": "1.3.1", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "provider_adapter_foundation",     "since": "1.3.2", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "coverage_repair",                 "since": "1.3.3", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "data_freshness",                  "since": "1.3.4", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "empirical_backtest",              "since": "1.3.5", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "abc_validation",                  "since": "1.3.6", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "strategy_robustness",             "since": "1.3.7", "stable_since": "1.3.9", "status": "STABLE"},
    {"id": "canonical_version_alignment",     "since": "1.3.7", "stable_since": "1.3.9", "status": "STABLE"},
    # v1.4.x Public Data Provider capabilities
    {"id": "twse_provider",                   "since": "1.4.0", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "tpex_provider",                   "since": "1.4.1", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "mops_provider",                   "since": "1.4.2", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "data_gov_tw_provider",            "since": "1.4.3", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "finmind_adapter",                 "since": "1.4.4", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "source_lineage_rate_limit",       "since": "1.4.5", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "provider_quality_gates",          "since": "1.4.6", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "forum_intelligence",              "since": "1.4.7", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "market_sentiment",                "since": "1.4.7", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "provider_integration_hardening",  "since": "1.4.8", "stable_since": "1.4.9", "status": "STABLE"},
    {"id": "provider_stable_rollup",          "since": "1.4.9", "stable_since": "1.4.9", "status": "STABLE"},
]


class StableCapabilityManifest:
    """
    Certifies all provider capabilities as STABLE through v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _MANIFEST_VERSION

    def get_all(self) -> List[Dict[str, Any]]:
        return list(_STABLE_CAPABILITIES)

    def get_stable(self) -> List[Dict[str, Any]]:
        return [c for c in _STABLE_CAPABILITIES if c["status"] == "STABLE"]

    def get_by_id(self, capability_id: str) -> Dict[str, Any]:
        for c in _STABLE_CAPABILITIES:
            if c["id"] == capability_id:
                return dict(c)
        raise KeyError(f"Unknown capability: {capability_id}")

    def is_stable(self, capability_id: str) -> bool:
        try:
            return self.get_by_id(capability_id)["status"] == "STABLE"
        except KeyError:
            return False

    def validate(self) -> Dict[str, Any]:
        total = len(_STABLE_CAPABILITIES)
        stable = len(self.get_stable())
        non_stable = [c["id"] for c in _STABLE_CAPABILITIES if c["status"] != "STABLE"]
        ok = stable == total and total >= 20
        return {
            "manifest_version": self.VERSION,
            "total_capabilities": total,
            "stable_count": stable,
            "non_stable": non_stable,
            "valid": ok,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        }

    def get_summary(self) -> Dict[str, Any]:
        result = self.validate()
        items = []
        for c in _STABLE_CAPABILITIES:
            status = "PASS" if c["status"] == "STABLE" else "FAIL"
            items.append((f"capability_{c['id']}", status,
                          f"since={c['since']} stable_since={c['stable_since']}"))
        result["items"] = items
        return result
