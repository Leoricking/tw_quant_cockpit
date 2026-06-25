"""portfolio/stable_rollup/readiness_matrix_v159.py — Readiness matrix v1.5.9."""
from .models_v159 import StableReadinessItem


def build_readiness_matrix():
    stable_items = [
        StableReadinessItem(domain="Portfolio Research", capability="Portfolio Research Foundation", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, reproducibility=False, safety=True, stage="STABLE", blockers=[], ready=True),
        StableReadinessItem(domain="Portfolio Research", capability="Position Sizing", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, safety=True, stage="STABLE", blockers=[], ready=True),
        StableReadinessItem(domain="Portfolio Research", capability="Correlation & Exposure", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, safety=True, stage="STABLE", blockers=[], ready=True),
        StableReadinessItem(domain="Portfolio Research", capability="Drawdown & Risk Controls", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, safety=True, stage="STABLE", blockers=[], ready=True),
        StableReadinessItem(domain="Portfolio Research", capability="Portfolio Walk-forward Backtest", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, reproducibility=True, safety=True, stage="STABLE", blockers=[], ready=True),
        StableReadinessItem(domain="Portfolio Research", capability="Portfolio Stable Rollup", implementation=True, tests=True, health=True, release_gate=True, docs=True, cli=True, gui=True, PIT=True, lineage=True, safety=True, stage="STABLE", blockers=[], ready=True),
    ]
    planned_items = [
        StableReadinessItem(domain="Live Trading", capability="Live Paper Trading", stage="PLANNED", blockers=["not-implemented"], ready=False),
        StableReadinessItem(domain="Live Trading", capability="Broker Integration", stage="PLANNED", blockers=["not-implemented", "blocked-by-policy"], ready=False),
        StableReadinessItem(domain="Live Trading", capability="Production Trading", stage="DISABLED", blockers=["permanently-blocked"], ready=False),
        StableReadinessItem(domain="Optimization", capability="Portfolio Optimization", stage="PLANNED", blockers=["not-implemented"], ready=False),
        StableReadinessItem(domain="Optimization", capability="Auto Rebalance", stage="PLANNED", blockers=["not-implemented"], ready=False),
    ]
    return stable_items + planned_items


class ReadinessMatrixV159:
    def __init__(self):
        self._items = build_readiness_matrix()

    def get_all(self):
        return list(self._items)

    def get_stable(self):
        return [i for i in self._items if i.stage == "STABLE"]

    def get_planned(self):
        return [i for i in self._items if i.stage == "PLANNED"]

    def get_blockers(self):
        return [(i.capability, i.blockers) for i in self._items if i.blockers]

    def validate(self):
        issues = []
        for item in self._items:
            if item.stage == "STABLE" and not item.ready:
                issues.append(f"STABLE_NOT_READY:{item.capability}")
            if item.stage == "STABLE" and item.blockers:
                issues.append(f"STABLE_HAS_BLOCKERS:{item.capability}")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "stable_ready": sum(1 for i in self._items if i.ready),
        }
