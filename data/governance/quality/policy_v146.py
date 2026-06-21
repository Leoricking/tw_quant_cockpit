"""
data/governance/quality/policy_v146.py — Quality Policy Manager v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Policy versioning. Provider-specific profiles (stricter allowed, not looser).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Default policy (baseline)
_DEFAULT_POLICY: Dict[str, Any] = {
    "policy_version": "1.4.6",
    "data_quality_pass_threshold": 80,
    "data_quality_critical_pass_threshold": 90,
    "freshness_pass_required": True,
    "coverage_pass_threshold": 0.80,
    "backtest_coverage_threshold": 0.90,
    "pit_required_for_backtest": True,
    "authority_required": "PRIMARY_OFFICIAL",
    "mock_formal_conclusion_allowed": False,
    "auto_release_allowed": False,
    "score_can_override_blocking": False,
}

# Provider-specific overrides (stricter only — never looser than default)
_PROVIDER_POLICIES: Dict[str, Dict[str, Any]] = {
    "twse": {
        "data_quality_pass_threshold": 85,
        "coverage_pass_threshold": 0.95,
        "freshness_pass_required": True,
    },
    "twse_official": {
        "data_quality_pass_threshold": 85,
        "coverage_pass_threshold": 0.95,
    },
    "tpex": {
        "data_quality_pass_threshold": 85,
        "coverage_pass_threshold": 0.95,
    },
    "mops": {
        "data_quality_pass_threshold": 90,
        "pit_required_for_backtest": True,
    },
    "data_gov_tw": {
        "data_quality_pass_threshold": 80,
        "authority_required": "PRIMARY_DOMAIN_OFFICIAL",
    },
    "finmind": {
        "data_quality_pass_threshold": 75,
        "authority_required": "SECONDARY_AGGREGATOR",
        "coverage_pass_threshold": 0.80,
    },
}


class QualityPolicyManager:
    """
    Policy versioning and provider-specific profiles.
    Provider overrides can only be STRICTER than default, never looser.
    """

    POLICY_VERSION = "1.4.6"

    def __init__(self) -> None:
        self._default = dict(_DEFAULT_POLICY)
        self._provider_overrides: Dict[str, Dict[str, Any]] = {}
        # Load built-in provider policies
        for pid, overrides in _PROVIDER_POLICIES.items():
            self._provider_overrides[pid] = overrides

    def get_policy(self, provider_id: str) -> Dict[str, Any]:
        """Return merged policy for provider. Overrides only stricter."""
        policy = dict(self._default)
        overrides = self._provider_overrides.get(provider_id, {})
        for k, v in overrides.items():
            # Only apply override if it makes the policy stricter
            if k in policy:
                default_val = policy[k]
                # For numeric thresholds, stricter = higher for quality, lower for coverage pct
                if isinstance(default_val, (int, float)) and isinstance(v, (int, float)):
                    if "threshold" in k or "required" in k:
                        policy[k] = max(default_val, v)  # stricter = higher threshold
                    else:
                        policy[k] = v
                else:
                    policy[k] = v
            else:
                policy[k] = v
        return policy

    def register_provider_policy(self, provider_id: str,
                                  overrides: Dict[str, Any]) -> None:
        """Register provider-specific policy overrides (stricter only)."""
        self._provider_overrides[provider_id] = overrides

    def get_policy_version(self) -> str:
        return self.POLICY_VERSION

    def list_provider_policies(self) -> List[str]:
        return list(self._provider_overrides.keys())

    def validate_policy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that a policy does not enable forbidden features."""
        errors = []
        if policy.get("mock_formal_conclusion_allowed"):
            errors.append("mock_formal_conclusion_allowed must be False")
        if policy.get("auto_release_allowed"):
            errors.append("auto_release_allowed must be False")
        if policy.get("score_can_override_blocking"):
            errors.append("score_can_override_blocking must be False")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "policy_version": self.POLICY_VERSION,
        }
