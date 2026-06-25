"""portfolio/stable_rollup/release_gate_registry_v159.py — Release gate registry v1.5.9."""
from .models_v159 import StableReleaseGateRecord

RELEASE_GATE_REGISTRY = [
    StableReleaseGateRecord(gate_id="portfolio_research_gate", module="release.portfolio_research_release_gate", public_entry_point="PortfolioResearchReleaseGate", public_cli_available=False, expected_checks=10, stable_version="1.5.0"),
    StableReleaseGateRecord(gate_id="position_sizing_gate", module="release.position_sizing_release_gate_v151", public_entry_point="PositionSizingReleaseGate", public_cli_available=False, expected_checks=20, stable_version="1.5.1"),
    StableReleaseGateRecord(gate_id="correlation_exposure_gate", module="release.correlation_exposure_release_gate_v152", public_entry_point="CorrelationExposureReleaseGate", public_cli_available=False, expected_checks=30, stable_version="1.5.2"),
    StableReleaseGateRecord(gate_id="drawdown_risk_gate", module="release.drawdown_risk_controls_release_gate_v153", public_entry_point="DrawdownRiskControlsReleaseGate", public_cli_available=False, expected_checks=38, stable_version="1.5.3"),
    StableReleaseGateRecord(gate_id="portfolio_walk_forward_gate", module="release.portfolio_walk_forward_release_gate_v154", public_entry_point="PortfolioWalkForwardReleaseGate", public_cli_available=False, expected_checks=36, stable_version="1.5.4"),
    StableReleaseGateRecord(gate_id="portfolio_stable_gate", module="release.portfolio_stable_release_gate_v159", public_entry_point="PortfolioStableReleaseGate", public_cli_available=True, expected_checks=36, stable_version="1.5.9"),
]


class ReleaseGateRegistryV159:
    def get_all(self):
        return list(RELEASE_GATE_REGISTRY)

    def get_by_id(self, gid):
        return next((g for g in RELEASE_GATE_REGISTRY if g.gate_id == gid), None)

    def validate(self):
        issues = []
        ids = [g.gate_id for g in RELEASE_GATE_REGISTRY]
        if len(ids) != len(set(ids)):
            issues.append("DUPLICATE_GATE_ID")
        for g in RELEASE_GATE_REGISTRY:
            if not g.public_entry_point:
                issues.append(f"MISSING_ENTRY_POINT:{g.gate_id}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(RELEASE_GATE_REGISTRY)}
