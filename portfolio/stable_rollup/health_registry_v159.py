"""portfolio/stable_rollup/health_registry_v159.py — Health registry v1.5.9."""
from .models_v159 import StableHealthRecord

HEALTH_REGISTRY = [
    StableHealthRecord(health_id="portfolio_health", command="portfolio-health", module="portfolio.health_v150", expected_checks=32, minimum_pass_count=32),
    StableHealthRecord(health_id="position_sizing_health", command="position-sizing-health", module="portfolio.sizing.health_v151", expected_checks=56, minimum_pass_count=56),
    StableHealthRecord(health_id="correlation_exposure_health", command="correlation-exposure-health", module="portfolio.correlation.health_v152", expected_checks=122, minimum_pass_count=122),
    StableHealthRecord(health_id="drawdown_risk_health", command="drawdown-risk-health", module="portfolio.risk_controls.health_v153", expected_checks=108, minimum_pass_count=108),
    StableHealthRecord(health_id="portfolio_walk_forward_health", command="portfolio-walk-forward-health", module="portfolio.walk_forward.health_v154", expected_checks=46, minimum_pass_count=46),
    StableHealthRecord(health_id="provider_stable_health", command="provider-stable-health", module="release.provider_stable_health_v149", expected_checks=17, minimum_pass_count=17),
    StableHealthRecord(health_id="provider_integration_health", command="provider-integration-health", module="release.provider_integration_health", expected_checks=30, minimum_pass_count=30),
    StableHealthRecord(health_id="research_foundation_health", command="research-foundation-health", module="release.research_foundation_health_v139", expected_checks=39, minimum_pass_count=39),
    StableHealthRecord(health_id="source_governance_health", command="source-governance-health", module="release.source_governance_health", expected_checks=41, minimum_pass_count=41),
    StableHealthRecord(health_id="provider_quality_health", command="provider-quality-health", module="release.provider_quality_health", expected_checks=59, minimum_pass_count=59),
    StableHealthRecord(health_id="forum_health", command="forum-health", module="data.providers.forum", expected_checks=59, minimum_pass_count=59),
    StableHealthRecord(health_id="cli_registration_health", command="cli-registration-health", module="cli.command_registry", expected_checks=6, minimum_pass_count=6),
    StableHealthRecord(health_id="portfolio_stable_rollup_health", command="portfolio-stable-health", module="portfolio.stable_rollup.health_v159", expected_checks=40, minimum_pass_count=40),
]


class HealthRegistryV159:
    def get_all(self):
        return list(HEALTH_REGISTRY)

    def get_by_id(self, hid):
        return next((h for h in HEALTH_REGISTRY if h.health_id == hid), None)

    def validate(self):
        issues = []
        ids = [h.health_id for h in HEALTH_REGISTRY]
        if len(ids) != len(set(ids)):
            issues.append("DUPLICATE_HEALTH_ID")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(HEALTH_REGISTRY)}
