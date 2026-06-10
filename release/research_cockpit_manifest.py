"""
release/research_cockpit_manifest.py — ResearchCockpitManifestBuilder v1.0.0

Builds and saves the v1.0.0 Research Trading Cockpit Stable manifest (JSON).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchCockpitManifestBuilder:
    """Build v1.0.0 Research Trading Cockpit Stable manifest.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)

    # ------------------------------------------------------------------
    # Module availability checks
    # ------------------------------------------------------------------

    def _check_modules(self) -> List[Dict]:
        module_checks = [
            ("Strategy Lab Dashboard",      "strategy_lab.strategy_lab_dashboard_engine",  "StrategyLabDashboardEngine"),
            ("Strategy Validation Score",   "strategy_validation.strategy_validation_engine", "StrategyValidationEngine"),
            ("Evidence Graph UX",           "evidence_graph.evidence_graph_query",          "EvidenceGraphQuery"),
            ("Crash Reversal Strategy Pack","strategy_rules.crash_reversal_pack",           "CrashReversalStrategyPack"),
            ("Strategy Lab Stable",         "strategy_lab.strategy_lab_engine",             "StrategyLabEngine"),
            ("Training Metrics",            "training_metrics.training_metrics_engine",      "TrainingMetricsEngine"),
            ("Backtest Coach",              "backtest_coach.backtest_coach_engine",          "BacktestCoachEngine"),
            ("Strategy Memory",             "strategy_memory.strategy_memory_engine",        "StrategyMemoryEngine"),
            ("Research Intelligence",       "research_intelligence.research_intelligence_engine", "ResearchIntelligenceEngine"),
            ("Data Coverage",               "data_coverage.data_coverage_engine",            "DataCoverageEngine"),
            ("Report Pack",                 "report_pack.report_registry",                  "ReportRegistry"),
            ("Regression Gate",             "regression.suite_registry",                    "RegressionSuiteRegistry"),
            ("Paper Trading",               "sim.simulator",                                 "PaperTrader"),
            ("Mock Realtime",               "broker.mock_broker",                            "MockBroker"),
        ]

        results = []
        for name, module_path, class_name in module_checks:
            try:
                import importlib
                mod = importlib.import_module(module_path)
                if class_name:
                    available = hasattr(mod, class_name)
                    status = "AVAILABLE" if available else "PARTIAL"
                else:
                    available = True
                    status = "AVAILABLE"
            except Exception as exc:
                available = False
                status = f"UNAVAILABLE: {exc}"
            results.append({
                "name":      name,
                "module":    module_path,
                "class":     class_name or "",
                "available": available,
                "status":    status,
            })
        return results

    def build(self) -> dict:
        """Returns manifest dict with full v1.0.0 research cockpit metadata."""
        from release.version_info import (
            VERSION, RELEASE_NAME, RELEASE_STAGE,
            REAL_ORDERS_ENABLED, NO_REAL_ORDERS,
            PRODUCTION_TRADING_BLOCKED, BROKER_EXECUTION_ENABLED,
            VALIDATED_DOES_NOT_ENABLE_TRADING,
        )

        modules = self._check_modules()

        manifest = {
            "version":           VERSION,
            "release_name":      RELEASE_NAME,
            "release_stage":     RELEASE_STAGE,
            "generated_at":      datetime.now().isoformat(),
            "modules":           modules,
            "cli_commands": [
                "version-info",
                "research-cockpit-stable",
                "research-cockpit-stable-summary",
                "research-cockpit-stable-checks",
                "research-cockpit-stable-manifest",
                "research-cockpit-stable-report",
                "strategy-lab-dashboard",
                "strategy-validation",
                "evidence-graph-ux",
                "crash-reversal-summary",
                "strategy-lab-summary",
                "mock-realtime",
                "paper",
                "stable-v060-check",
                "regression-run",
            ],
            "gui_tabs": [
                "Strategy Lab Dashboard",
                "Strategy Lab Stable",
                "Strategy Validation Score",
                "Evidence Graph",
                "Research Intelligence Stable",
                "Backtest Coach",
                "Training Metrics",
                "Strategy Memory",
            ],
            "reports": [
                "research_trading_cockpit_stable_report",
                "strategy_lab_stable_report",
                "strategy_validation_report",
                "evidence_graph_report",
                "crash_reversal_strategy_report",
                "strategy_lab_dashboard_report",
            ],
            "safety_guards": [
                "No Real Orders",
                "Production Trading BLOCKED",
                "Broker Execution Disabled",
                "VALIDATED does not enable trading",
                "Paper trading is simulation only",
                "Mock realtime is simulation only",
            ],
            "regression_suites": [
                "quick",
                "full",
                "release_gate",
                "safety",
            ],
            "known_warnings": [
                "cp950 subprocess encoding warning (Windows only — non-critical)",
                "Paper smoke test may WARN if paper_state.json missing (non-critical)",
                "no_real_orders flag pre-existing check is advisory only",
                "Optional report_pack modules may show ENV_LIMITED (non-critical)",
            ],
            "no_real_orders":                      NO_REAL_ORDERS,
            "real_orders_enabled":                 REAL_ORDERS_ENABLED,
            "production_blocked":                  PRODUCTION_TRADING_BLOCKED,
            "broker_execution_enabled":            BROKER_EXECUTION_ENABLED,
            "validated_does_not_enable_trading":   VALIDATED_DOES_NOT_ENABLE_TRADING,
        }
        return manifest

    def save(self, output_dir: str = "data/backtest_results/release") -> str:
        """Save manifest as JSON. Returns path to saved file."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(self._root, output_dir)
        os.makedirs(output_dir, exist_ok=True)

        manifest = self.build()
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(output_dir, f"research_cockpit_manifest_{today}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
        logger.info("Research Cockpit Manifest saved: %s", path)
        return path
