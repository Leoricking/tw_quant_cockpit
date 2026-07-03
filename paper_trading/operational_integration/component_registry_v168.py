"""
paper_trading/operational_integration/component_registry_v168.py
Component Registry for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .models_v168 import ComponentDescriptor, ComponentCapability

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_DEFAULT_COMPONENTS = [
    ComponentDescriptor(
        component_id="market_data_session",
        component_name="Market Data Session",
        component_version="1.6.1",
        capabilities=["market_data_feed", "session_management", "lineage_tracking"],
        dependencies=[],
        supported_contracts=["MarketDataToSession"],
    ),
    ComponentDescriptor(
        component_id="live_paper_trading",
        component_name="Live Paper Trading",
        component_version="1.6.0",
        capabilities=["paper_order", "paper_fill", "paper_ledger"],
        dependencies=["market_data_session"],
        supported_contracts=["SessionToStrategy"],
    ),
    ComponentDescriptor(
        component_id="paper_strategy",
        component_name="Paper Strategy",
        component_version="1.6.2",
        capabilities=["signal_generation", "decision_pipeline", "policy_approval"],
        dependencies=["live_paper_trading"],
        supported_contracts=["StrategyToPortfolio"],
    ),
    ComponentDescriptor(
        component_id="portfolio_research",
        component_name="Portfolio Research",
        component_version="1.5.0",
        capabilities=["portfolio_management", "risk_management"],
        dependencies=["paper_strategy"],
        supported_contracts=["PortfolioToExecution"],
    ),
    ComponentDescriptor(
        component_id="position_sizing",
        component_name="Position Sizing",
        component_version="1.5.1",
        capabilities=["sizing_compute", "risk_budget"],
        dependencies=["portfolio_research"],
        supported_contracts=[],
    ),
    ComponentDescriptor(
        component_id="correlation_exposure",
        component_name="Correlation Exposure",
        component_version="1.5.2",
        capabilities=["correlation_check", "exposure_limit"],
        dependencies=["portfolio_research"],
        supported_contracts=[],
    ),
    ComponentDescriptor(
        component_id="drawdown_risk",
        component_name="Drawdown Risk Controls",
        component_version="1.5.3",
        capabilities=["drawdown_monitor", "risk_control"],
        dependencies=["portfolio_research"],
        supported_contracts=["ExecutionToAnalytics"],
    ),
    ComponentDescriptor(
        component_id="operational_analytics",
        component_name="Operational Analytics",
        component_version="1.6.4",
        capabilities=["analytics_run", "metrics_compute", "scorecard"],
        dependencies=["drawdown_risk"],
        supported_contracts=["AnalyticsToAttribution"],
    ),
    ComponentDescriptor(
        component_id="paper_attribution",
        component_name="Paper Attribution",
        component_version="1.6.7",
        capabilities=["attribution_run", "reconciliation", "scorecard"],
        dependencies=["operational_analytics"],
        supported_contracts=["AttributionToCoordination"],
    ),
    ComponentDescriptor(
        component_id="multi_session_coordination",
        component_name="Multi-session Coordination",
        component_version="1.6.6",
        capabilities=["session_coordination", "conflict_resolution"],
        dependencies=["paper_attribution"],
        supported_contracts=["CoordinationToRecovery"],
    ),
    ComponentDescriptor(
        component_id="failure_injection_recovery",
        component_name="Failure Injection Recovery",
        component_version="1.6.5",
        capabilities=["failure_inject", "recovery_validate"],
        dependencies=["multi_session_coordination"],
        supported_contracts=["RecoveryToHealth"],
    ),
    ComponentDescriptor(
        component_id="fixture_governance",
        component_name="Fixture Governance",
        component_version="1.6.6.1",
        capabilities=["fixture_validate", "marker_check"],
        dependencies=[],
        supported_contracts=[],
    ),
    ComponentDescriptor(
        component_id="cli_registration",
        component_name="CLI Registration",
        component_version="1.6.8",
        capabilities=["cli_commands", "command_dispatch"],
        dependencies=[],
        supported_contracts=[],
    ),
    ComponentDescriptor(
        component_id="gui_integration",
        component_name="GUI Integration",
        component_version="1.6.8",
        capabilities=["headless_render", "tab_management"],
        dependencies=[],
        supported_contracts=["HealthToReport"],
    ),
]


class ComponentRegistry:
    """Registry for all integration components. Research only. No production."""

    def __init__(self) -> None:
        self._components: Dict[str, ComponentDescriptor] = {}
        for comp in _DEFAULT_COMPONENTS:
            self._components[comp.component_id] = comp

    def register_component(self, descriptor: ComponentDescriptor) -> None:
        """Register a component. Raises ValueError if already registered."""
        if descriptor.component_id in self._components:
            raise ValueError(f"Component already registered: {descriptor.component_id!r}")
        self._components[descriptor.component_id] = descriptor

    def get_component(self, component_id: str) -> Optional[ComponentDescriptor]:
        """Return component descriptor or None."""
        return self._components.get(component_id)

    def list_components(self) -> List[str]:
        """Return sorted list of component IDs."""
        return sorted(self._components.keys())

    def validate_component(self, component_id: str) -> Dict[str, Any]:
        """Validate a single component for structural integrity."""
        comp = self._components.get(component_id)
        if comp is None:
            return {"valid": False, "errors": [f"component_not_found: {component_id}"], "paper_only": True}
        errors = []
        if not comp.component_id:
            errors.append("missing component_id")
        if not comp.component_name:
            errors.append("missing component_name")
        if not comp.component_version:
            errors.append("missing component_version")
        if not comp.paper_only:
            errors.append("paper_only must be True")
        return {"valid": len(errors) == 0, "errors": errors, "paper_only": True}

    def validate_capabilities(self) -> Dict[str, Any]:
        """Validate all component capabilities are consistent."""
        results = {}
        for cid, comp in self._components.items():
            if not comp.paper_only or not comp.research_only:
                results[cid] = {"valid": False, "issue": "paper_only or research_only not set"}
            else:
                results[cid] = {"valid": True, "capabilities": comp.capabilities}
        all_valid = all(v["valid"] for v in results.values())
        return {"all_valid": all_valid, "details": results, "paper_only": True}

    def validate_version(self, component_id: str, expected_version: str) -> bool:
        """Return True if component version matches expected."""
        comp = self._components.get(component_id)
        if comp is None:
            return False
        return comp.component_version == expected_version

    def validate_contracts(self, component_id: str) -> Dict[str, Any]:
        """Return all contracts supported by this component."""
        comp = self._components.get(component_id)
        if comp is None:
            return {"valid": False, "contracts": [], "paper_only": True}
        return {"valid": True, "contracts": comp.supported_contracts, "paper_only": True}

    def list_dependencies(self, component_id: str) -> List[str]:
        """Return direct dependencies of a component."""
        comp = self._components.get(component_id)
        if comp is None:
            return []
        return list(comp.dependencies)

    def list_dependents(self, component_id: str) -> List[str]:
        """Return components that depend on this one."""
        dependents = []
        for cid, comp in self._components.items():
            if component_id in comp.dependencies:
                dependents.append(cid)
        return dependents

    def detect_cycles(self) -> List[List[str]]:
        """Detect circular dependency chains. Returns list of cycles."""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            comp = self._components.get(node)
            if comp is None:
                rec_stack.discard(node)
                return
            for dep in comp.dependencies:
                if dep not in visited:
                    dfs(dep, path + [dep])
                elif dep in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(dep) if dep in path else 0
                    cycles.append(path[cycle_start:] + [dep])
            rec_stack.discard(node)

        for cid in list(self._components.keys()):
            if cid not in visited:
                dfs(cid, [cid])
        return cycles

    def detect_missing_dependencies(self) -> Dict[str, List[str]]:
        """Return mapping of component_id -> missing dependency ids."""
        missing: Dict[str, List[str]] = {}
        for cid, comp in self._components.items():
            miss = [dep for dep in comp.dependencies if dep not in self._components]
            if miss:
                missing[cid] = miss
        return missing

    def component_health_summary(self) -> Dict[str, Any]:
        """Return a health summary for all registered components."""
        total = len(self._components)
        missing_deps = self.detect_missing_dependencies()
        cycles = self.detect_cycles()
        paper_only_count = sum(1 for c in self._components.values() if c.paper_only)
        return {
            "total_components": total,
            "paper_only_count": paper_only_count,
            "missing_dependency_count": len(missing_deps),
            "cycle_count": len(cycles),
            "healthy": len(missing_deps) == 0 and len(cycles) == 0,
            "paper_only": True,
            "research_only": True,
        }
