"""
strategy_validation/evidence_context_builder.py
TW Quant Cockpit — Evidence Context Builder
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from typing import Any, Dict, List

VERSION = "v0.9.2"

logger = logging.getLogger(__name__)

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True

_CRASH_REVERSAL_RULE_NAMES = [
    "crash_cause_classifier",
    "post_crash_stabilization_checklist",
    "relative_strength_after_crash_score",
    "sakata_eps_backed_dip_buy_filter",
    "moving_average_profit_discipline",
    "high_risk_industry_exposure_guard",
]

_DEFAULT_CONTEXT: Dict[str, Any] = {
    "evidence_threads":   [],
    "graph_gaps":         [],
    "contradictions":     0,
    "requires_data":      0,
    "requires_backtest":  0,
    "requires_replay":    0,
    "training_metrics":   [],
    "backtest_results":   [],
    "replay_mistakes":    [],
    "journal_patterns":   [],
    "crash_reversal_rules": _CRASH_REVERSAL_RULE_NAMES,
    "data_coverage":      50.0,
}


def _empty_context() -> Dict[str, Any]:
    """Return a fresh copy of the default context."""
    ctx = dict(_DEFAULT_CONTEXT)
    ctx["evidence_threads"]    = []
    ctx["graph_gaps"]          = []
    ctx["training_metrics"]    = []
    ctx["backtest_results"]    = []
    ctx["replay_mistakes"]     = []
    ctx["journal_patterns"]    = []
    ctx["crash_reversal_rules"] = list(_CRASH_REVERSAL_RULE_NAMES)
    return ctx


class EvidenceContextBuilder:
    """
    Builds evidence context for a strategy candidate from all available sources.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only                         = True
    no_real_orders                    = True
    production_blocked                = True
    validated_does_not_enable_trading = True

    def __init__(self, project_root: str = "") -> None:
        if not project_root:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = project_root

    def _abs(self, rel: str) -> str:
        return os.path.join(self.project_root, rel)

    def build_context(self, candidate: dict) -> Dict[str, Any]:
        """
        Build full evidence context for a candidate.
        Returns a context dict; all sub-loaders fall back to defaults on failure.
        """
        ctx = _empty_context()

        # Evidence graph
        try:
            eg = self.load_evidence_graph_context()
            ctx["evidence_threads"] = eg.get("evidence_threads", [])
            ctx["graph_gaps"]       = eg.get("graph_gaps", [])
            ctx["contradictions"]   = eg.get("contradictions", 0)
            ctx["requires_data"]    = eg.get("requires_data", 0)
            ctx["requires_backtest"] = eg.get("requires_backtest", 0)
            ctx["requires_replay"]  = eg.get("requires_replay", 0)
        except Exception as exc:
            logger.warning("build_context: evidence_graph failed: %s", exc)

        # Backtest
        try:
            bt = self.load_backtest_context()
            ctx["backtest_results"] = bt.get("backtest_results", [])
        except Exception as exc:
            logger.warning("build_context: backtest failed: %s", exc)

        # Replay
        try:
            rp = self.load_replay_context()
            ctx["replay_mistakes"] = rp.get("replay_mistakes", [])
        except Exception as exc:
            logger.warning("build_context: replay failed: %s", exc)

        # Journal
        try:
            jn = self.load_journal_context()
            ctx["journal_patterns"] = jn.get("journal_patterns", [])
        except Exception as exc:
            logger.warning("build_context: journal failed: %s", exc)

        # Training metrics
        try:
            tm = self.load_training_metrics_context()
            ctx["training_metrics"] = tm.get("training_metrics", [])
        except Exception as exc:
            logger.warning("build_context: training_metrics failed: %s", exc)

        # Data coverage
        try:
            dc = self.load_data_coverage_context()
            ctx["data_coverage"] = dc.get("data_coverage", 50.0)
        except Exception as exc:
            logger.warning("build_context: data_coverage failed: %s", exc)

        # Crash reversal (always available)
        try:
            cr = self.load_crash_reversal_context()
            ctx["crash_reversal_rules"] = cr.get("crash_reversal_rules", _CRASH_REVERSAL_RULE_NAMES)
        except Exception as exc:
            logger.warning("build_context: crash_reversal failed: %s", exc)

        return ctx

    # ------------------------------------------------------------------
    # Evidence graph context
    # ------------------------------------------------------------------

    def load_evidence_graph_context(self) -> Dict[str, Any]:
        """Load evidence graph threads, gaps, contradiction/data counts."""
        result: Dict[str, Any] = {
            "evidence_threads":  [],
            "graph_gaps":        [],
            "contradictions":    0,
            "requires_data":     0,
            "requires_backtest": 0,
            "requires_replay":   0,
        }
        try:
            import sys
            sys.path.insert(0, self.project_root)
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            store = EvidenceGraphStore(
                output_dir=self._abs("data/backtest_results/evidence_graph")
            )
            try:
                threads = store.load_latest_threads()
                result["evidence_threads"] = threads if isinstance(threads, list) else []
            except Exception:
                pass
            try:
                gaps = store.load_latest_gaps()
                result["graph_gaps"] = gaps if isinstance(gaps, list) else []
                for g in result["graph_gaps"]:
                    gap_type = str(g.get("gap_type", "")).upper()
                    if "CONTRADICTION" in gap_type or "CONFLICT" in gap_type:
                        result["contradictions"] = result["contradictions"] + 1
                    if "DATA" in gap_type:
                        result["requires_data"] = result["requires_data"] + 1
                    if "BACKTEST" in gap_type:
                        result["requires_backtest"] = result["requires_backtest"] + 1
                    if "REPLAY" in gap_type:
                        result["requires_replay"] = result["requires_replay"] + 1
            except Exception:
                pass
        except Exception as exc:
            logger.debug("load_evidence_graph_context fallback: %s", exc)
            # Fallback: scan CSV directly
            try:
                pattern = self._abs("data/backtest_results/evidence_graph/evidence_graph_threads_*.csv")
                files = sorted(glob.glob(pattern))
                if files:
                    with open(files[-1], newline="", encoding="utf-8") as fh:
                        result["evidence_threads"] = list(csv.DictReader(fh))
            except Exception:
                pass
        return result

    # ------------------------------------------------------------------
    # Backtest context
    # ------------------------------------------------------------------

    def load_backtest_context(self) -> Dict[str, Any]:
        """Scan backtest_coach CSVs for results."""
        result: Dict[str, Any] = {"backtest_results": []}
        try:
            pattern = self._abs("data/backtest_results/backtest_coach/*.csv")
            files = sorted(glob.glob(pattern))
            rows: List[dict] = []
            for fpath in files[-5:]:
                try:
                    with open(fpath, newline="", encoding="utf-8") as fh:
                        rows.extend(list(csv.DictReader(fh)))
                except Exception:
                    pass
            result["backtest_results"] = rows
        except Exception as exc:
            logger.debug("load_backtest_context: %s", exc)
        return result

    # ------------------------------------------------------------------
    # Replay context
    # ------------------------------------------------------------------

    def load_replay_context(self) -> Dict[str, Any]:
        """Scan replay_sessions and backtest_results for replay mistake data."""
        result: Dict[str, Any] = {"replay_mistakes": []}
        try:
            mistakes: List[dict] = []
            for base in ["replay_sessions", "data/backtest_results"]:
                pattern = self._abs(f"{base}/*.csv")
                for fpath in sorted(glob.glob(pattern))[-3:]:
                    try:
                        with open(fpath, newline="", encoding="utf-8") as fh:
                            reader = csv.DictReader(fh)
                            for row in reader:
                                if any(k in row for k in ("mistake", "error", "replay_mistake")):
                                    mistakes.append(row)
                    except Exception:
                        pass
            result["replay_mistakes"] = mistakes
        except Exception as exc:
            logger.debug("load_replay_context: %s", exc)
        return result

    # ------------------------------------------------------------------
    # Journal context
    # ------------------------------------------------------------------

    def load_journal_context(self) -> Dict[str, Any]:
        """Scan journal_data CSVs for patterns."""
        result: Dict[str, Any] = {"journal_patterns": []}
        try:
            patterns: List[dict] = []
            for fpath in sorted(glob.glob(self._abs("journal_data/*.csv")))[-3:]:
                try:
                    with open(fpath, newline="", encoding="utf-8") as fh:
                        patterns.extend(list(csv.DictReader(fh)))
                except Exception:
                    pass
            result["journal_patterns"] = patterns
        except Exception as exc:
            logger.debug("load_journal_context: %s", exc)
        return result

    # ------------------------------------------------------------------
    # Training metrics context
    # ------------------------------------------------------------------

    def load_training_metrics_context(self) -> Dict[str, Any]:
        """Load training metrics via MetricsCollector or CSV fallback."""
        result: Dict[str, Any] = {"training_metrics": []}
        try:
            import sys
            sys.path.insert(0, self.project_root)
            from training_metrics.metrics_collector import MetricsCollector
            collector = MetricsCollector()
            metrics = collector.collect_all()
            result["training_metrics"] = [
                m.to_dict() if hasattr(m, "to_dict") else (m if isinstance(m, dict) else {})
                for m in (metrics or [])
            ]
        except Exception:
            try:
                pattern = self._abs("data/backtest_results/training_metrics/*.csv")
                files = sorted(glob.glob(pattern))
                rows: List[dict] = []
                for fpath in files[-3:]:
                    with open(fpath, newline="", encoding="utf-8") as fh:
                        rows.extend(list(csv.DictReader(fh)))
                result["training_metrics"] = rows
            except Exception as exc2:
                logger.debug("load_training_metrics_context CSV fallback failed: %s", exc2)
        return result

    # ------------------------------------------------------------------
    # Data coverage context
    # ------------------------------------------------------------------

    def load_data_coverage_context(self) -> Dict[str, Any]:
        """Scan data_coverage CSVs and compute average coverage percentage."""
        result: Dict[str, Any] = {"data_coverage": 50.0}
        try:
            pattern = self._abs("data/backtest_results/data_coverage/*.csv")
            files = sorted(glob.glob(pattern))
            coverages: List[float] = []
            for fpath in files[-5:]:
                try:
                    with open(fpath, newline="", encoding="utf-8") as fh:
                        for row in csv.DictReader(fh):
                            for key in ("coverage_pct", "coverage", "data_coverage", "coverage_percent"):
                                val = row.get(key)
                                if val is not None:
                                    try:
                                        coverages.append(float(val))
                                    except ValueError:
                                        pass
                                    break
                except Exception:
                    pass
            if coverages:
                result["data_coverage"] = sum(coverages) / len(coverages)
        except Exception as exc:
            logger.debug("load_data_coverage_context: %s", exc)
        return result

    # ------------------------------------------------------------------
    # Crash reversal context
    # ------------------------------------------------------------------

    def load_crash_reversal_context(self) -> Dict[str, Any]:
        """Return default crash reversal rule pack context."""
        return {
            "crash_reversal_rules": list(_CRASH_REVERSAL_RULE_NAMES),
        }
