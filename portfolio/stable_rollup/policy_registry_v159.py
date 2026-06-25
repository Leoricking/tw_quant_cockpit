"""portfolio/stable_rollup/policy_registry_v159.py — Policy registry v1.5.9."""
from .models_v159 import StablePolicyRecord

STABLE_POLICIES = [
    StablePolicyRecord(policy_id="sizing_policy_default", policy_type="PositionSizingPolicy", version="1.5.1", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="correlation_threshold_default", policy_type="CorrelationThresholdPolicy", version="1.5.2", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="exposure_limit_default", policy_type="ExposureLimitPolicy", version="1.5.2", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="risk_control_default", policy_type="RiskControlPolicy", version="1.5.3", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="cost_policy_default", policy_type="CostPolicy", version="1.5.4", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="tax_policy_default", policy_type="TaxPolicy", version="1.5.4", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="slippage_policy_default", policy_type="SlippagePolicy", version="1.5.4", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="liquidity_policy_default", policy_type="LiquidityPolicy", version="1.5.4", effective_from="2024-01-01"),
    StablePolicyRecord(policy_id="walk_forward_config_default", policy_type="WalkForwardConfigurationPolicy", version="1.5.4", effective_from="2024-01-01"),
]


class PolicyRegistryV159:
    def get_all(self):
        return list(STABLE_POLICIES)

    def get_by_id(self, pid):
        return next((p for p in STABLE_POLICIES if p.policy_id == pid), None)

    def validate(self):
        issues = []
        for p in STABLE_POLICIES:
            if not p.version:
                issues.append(f"MISSING_VERSION:{p.policy_id}")
            if not p.effective_from:
                issues.append(f"MISSING_EFFECTIVE_FROM:{p.policy_id}")
            if not p.PIT_safe:
                issues.append(f"PIT_UNSAFE:{p.policy_id}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(STABLE_POLICIES)}
