"""
gui/rule_governance_adapter.py — Rule Governance GUI bridge (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
import logging
from typing import Optional

_LOG = logging.getLogger(__name__)

# Resolve project base directory
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RuleGovernanceAdapter:
    """
    Bridge between governance package and GUI layer.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
    ):
        if not os.path.isabs(results_dir):
            results_dir = os.path.join(_BASE_DIR, results_dir)
        if not os.path.isabs(report_dir):
            report_dir = os.path.join(_BASE_DIR, report_dir)

        self._results_dir = results_dir
        self._report_dir = report_dir

    # ------------------------------------------------------------------
    # Governance run
    # ------------------------------------------------------------------

    def run_governance(self, mode: str = "real") -> dict:
        """
        Run full governance pipeline and return summary dict.
        Never crashes — returns error dict on failure.
        """
        try:
            from governance.rule_registry import RuleRegistry
            from governance.rule_dependency_graph import RuleDependencyGraph
            from governance.rule_confidence import RuleConfidenceScorer

            registry = RuleRegistry()
            count = registry.load_builtin_rules()
            summary = registry.build_rule_summary()

            dg = RuleDependencyGraph(registry=registry)
            dg.build_graph()
            edges = dg.export_edges()
            cycles = dg.detect_cycles()
            high_impact = dg.get_high_impact_rules(min_dependents=2)

            scorer = RuleConfidenceScorer(
                registry=registry, results_dir=self._results_dir
            )
            confidence_result = scorer.run()

            # Build review queue
            review_queue = self._build_review_queue(registry, confidence_result)

            return {
                "mode": mode,
                "registry_summary": summary,
                "rules_loaded": count,
                "confidence_result": confidence_result,
                "dependency_edges": edges,
                "dependency_cycles": cycles,
                "high_impact_rules": high_impact,
                "review_queue": review_queue,
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
            }

        except Exception as exc:
            _LOG.warning("RuleGovernanceAdapter.run_governance error: %s", exc)
            return {
                "error": str(exc),
                "mode": mode,
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
            }

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> str:
        """
        Run governance and generate Markdown report.
        Returns report file path on success, empty string on failure.
        """
        try:
            from governance.rule_registry import RuleRegistry
            from governance.rule_dependency_graph import RuleDependencyGraph
            from governance.rule_confidence import RuleConfidenceScorer
            from governance.rule_snapshot import RuleSnapshotBuilder
            from reports.rule_governance_report import RuleGovernanceReportBuilder

            registry = RuleRegistry()
            registry.load_builtin_rules()

            dg = RuleDependencyGraph(registry=registry)
            dg.build_graph()

            scorer = RuleConfidenceScorer(
                registry=registry, results_dir=self._results_dir
            )
            confidence_result = scorer.run()

            builder = RuleSnapshotBuilder(registry=registry)
            snapshot = builder.build_snapshot()

            report_builder = RuleGovernanceReportBuilder(
                mode=mode,
                registry=registry,
                confidence_result=confidence_result,
                dependency_graph=dg,
                snapshot=snapshot,
            )
            path = report_builder.build(output_dir=self._report_dir)
            return path

        except Exception as exc:
            _LOG.warning("RuleGovernanceAdapter.generate_report error: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Snapshot export
    # ------------------------------------------------------------------

    def export_snapshot(self) -> dict:
        """
        Export governance snapshot JSON + CSV.
        Returns {snapshot_path, summary_path} or {error: str}.
        """
        try:
            from governance.rule_registry import RuleRegistry
            from governance.rule_snapshot import RuleSnapshotBuilder

            registry = RuleRegistry()
            registry.load_builtin_rules()

            builder = RuleSnapshotBuilder(
                registry=registry, output_dir=self._results_dir
            )
            return builder.write_snapshot()

        except Exception as exc:
            _LOG.warning("RuleGovernanceAdapter.export_snapshot error: %s", exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # Load latest summary from file system
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """
        Load the most recent governance snapshot JSON from results_dir.
        Returns empty dict if none found.
        """
        try:
            if not os.path.isdir(self._results_dir):
                return {}
            candidates = [
                f for f in os.listdir(self._results_dir)
                if f.startswith("rule_governance_snapshot_") and f.endswith(".json")
            ]
            if not candidates:
                return {}
            candidates.sort(reverse=True)
            latest = os.path.join(self._results_dir, candidates[0])
            import json
            with open(latest, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            _LOG.warning("RuleGovernanceAdapter.load_latest_summary error: %s", exc)
            return {}

    def load_latest_report_path(self) -> Optional[str]:
        """
        Return path to the most recent governance Markdown report, or None.
        """
        try:
            if not os.path.isdir(self._report_dir):
                return None
            candidates = [
                f for f in os.listdir(self._report_dir)
                if f.startswith("rule_governance_report_") and f.endswith(".md")
            ]
            if not candidates:
                return None
            candidates.sort(reverse=True)
            return os.path.join(self._report_dir, candidates[0])
        except Exception as exc:
            _LOG.warning("RuleGovernanceAdapter.load_latest_report_path error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_review_queue(registry, confidence_result: dict) -> list:
        """Build a list of dicts describing rules that need attention."""
        queue = []
        try:
            for rule in registry.list_rules(status="NEEDS_REVIEW"):
                queue.append({
                    "rule_id": rule.rule_id,
                    "reason": "Status: NEEDS_REVIEW",
                    "severity": "HIGH",
                    "recommended_action": "Review and update status",
                })
            for rule in registry.list_rules(status="INSUFFICIENT_SAMPLE"):
                queue.append({
                    "rule_id": rule.rule_id,
                    "reason": "Insufficient sample count",
                    "severity": "MEDIUM",
                    "recommended_action": "Collect more backtest data",
                })
            # Add unknown-confidence rules
            unknown = confidence_result.get("unknown_confidence", [])
            known_ids = {item["rule_id"] for item in queue}
            for rid in unknown:
                if rid not in known_ids:
                    queue.append({
                        "rule_id": rid,
                        "reason": "No validation data — confidence UNKNOWN",
                        "severity": "LOW",
                        "recommended_action": "Run backtest validation",
                    })
        except Exception as exc:
            _LOG.warning("_build_review_queue error: %s", exc)
        return queue
