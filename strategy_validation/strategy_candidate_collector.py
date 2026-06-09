"""
strategy_validation/strategy_candidate_collector.py
TW Quant Cockpit — Strategy Candidate Collector
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import hashlib
import logging
import os
from typing import List

from strategy_validation.strategy_validation_schema import (
    VERSION,
    STYPE_CRASH_REVERSAL_RULE, STYPE_STRATEGY_HYPOTHESIS,
    STYPE_RULE_CANDIDATE, STYPE_UNKNOWN,
    FORBIDDEN_ACTIONS,
)

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True

# Hardcoded crash reversal rule names (6 rules)
_CRASH_REVERSAL_RULES = [
    "crash_cause_classifier",
    "post_crash_stabilization_checklist",
    "relative_strength_after_crash_score",
    "sakata_eps_backed_dip_buy_filter",
    "moving_average_profit_discipline",
    "high_risk_industry_exposure_guard",
]


def _make_id(source_module: str, index: int, name: str) -> str:
    """Generate unique strategy_id as SV_{source_module}_{index}_{hash}."""
    raw = f"{source_module}_{index}_{name}"
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:8]
    return f"SV_{source_module}_{index}_{h}"


def _guard_name(name: str) -> str:
    """Ensure name doesn't contain forbidden action keywords."""
    for fa in FORBIDDEN_ACTIONS:
        if fa in name.upper():
            return name.replace(fa, "RESEARCH_" + fa)
    return name


class StrategyCandidateCollector:
    """
    Collects strategy candidates from all available Research OS modules.
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

    def collect_all(self, mode: str = "real") -> List[dict]:
        """Collect candidates from all sources. Returns deduplicated list."""
        candidates: List[dict] = []
        seen_ids: set = set()

        for method in [
            self.collect_from_crash_reversal,
            self.collect_from_strategy_memory,
            self.collect_from_rule_governance,
            self.collect_from_evidence_graph,
            self.collect_from_backtest_coach,
            self.collect_from_research_intelligence,
        ]:
            try:
                items = method()
                for item in items:
                    sid = item.get("strategy_id", "")
                    if sid and sid not in seen_ids:
                        seen_ids.add(sid)
                        candidates.append(item)
            except Exception as exc:
                logger.warning("collect_all: method %s failed: %s", method.__name__, exc)

        logger.info("StrategyCandidateCollector: collected %d candidates (mode=%s)", len(candidates), mode)
        return candidates

    # ------------------------------------------------------------------
    # Crash reversal rules (hardcoded — always available)
    # ------------------------------------------------------------------

    def collect_from_crash_reversal(self) -> List[dict]:
        """Return the 6 hardcoded crash reversal rules."""
        results = []
        try:
            for i, rule_name in enumerate(_CRASH_REVERSAL_RULES):
                sid = _make_id("crash_reversal", i, rule_name)
                results.append({
                    "strategy_id":   sid,
                    "strategy_name": _guard_name(rule_name),
                    "strategy_type": STYPE_CRASH_REVERSAL_RULE,
                    "source_module": "crash_reversal",
                    "source_ref":    f"crash_reversal/{rule_name}",
                    "description":   f"Crash reversal research rule: {rule_name}",
                })
        except Exception as exc:
            logger.warning("collect_from_crash_reversal: %s", exc)
        return results

    # ------------------------------------------------------------------
    # Strategy memory
    # ------------------------------------------------------------------

    def collect_from_strategy_memory(self) -> List[dict]:
        """Load candidates from strategy_memory CSV files."""
        results = []
        try:
            pattern = self._abs("data/backtest_results/strategy_memory/strategy_memory_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                pattern2 = self._abs("strategy_memory/data/strategy_memory_*.csv")
                files = sorted(glob.glob(pattern2))
            if not files:
                return results

            latest = files[-1]
            accepted_types = {
                STYPE_STRATEGY_HYPOTHESIS, STYPE_RULE_CANDIDATE,
                "RESEARCH_CONCLUSION", "STRATEGY_HYPOTHESIS", "RULE_CANDIDATE",
            }
            with open(latest, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for i, row in enumerate(reader):
                    stype = str(row.get("strategy_type", row.get("memory_type", "UNKNOWN"))).upper()
                    if stype not in accepted_types:
                        continue
                    name = str(row.get("strategy_name", row.get("name", row.get("memory_id", f"memory_{i}"))))
                    sid = _make_id("strategy_memory", i, name)
                    results.append({
                        "strategy_id":   sid,
                        "strategy_name": _guard_name(name),
                        "strategy_type": stype if stype in {STYPE_STRATEGY_HYPOTHESIS, STYPE_RULE_CANDIDATE} else STYPE_STRATEGY_HYPOTHESIS,
                        "source_module": "strategy_memory",
                        "source_ref":    os.path.basename(latest),
                        "description":   str(row.get("description", row.get("summary", ""))),
                    })
        except Exception as exc:
            logger.warning("collect_from_strategy_memory: %s", exc)
        return results

    # ------------------------------------------------------------------
    # Rule governance
    # ------------------------------------------------------------------

    def collect_from_rule_governance(self) -> List[dict]:
        """Load NEEDS_REVIEW rules from rule governance CSVs."""
        results = []
        try:
            pattern = self._abs("data/backtest_results/rule_governance/*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                pattern2 = self._abs("governance/*.csv")
                files = sorted(glob.glob(pattern2))

            for fpath in files[-3:]:  # scan last 3 files max
                with open(fpath, newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh)
                    for i, row in enumerate(reader):
                        status = str(row.get("status", row.get("review_status", ""))).upper()
                        if "REVIEW" not in status and "NEEDS" not in status:
                            continue
                        name = str(row.get("rule_name", row.get("strategy_name", row.get("name", f"rule_{i}"))))
                        sid = _make_id("rule_governance", i, name)
                        results.append({
                            "strategy_id":   sid,
                            "strategy_name": _guard_name(name),
                            "strategy_type": STYPE_RULE_CANDIDATE,
                            "source_module": "rule_governance",
                            "source_ref":    os.path.basename(fpath),
                            "description":   str(row.get("description", row.get("issue", ""))),
                        })
        except Exception as exc:
            logger.warning("collect_from_rule_governance: %s", exc)
        return results

    # ------------------------------------------------------------------
    # Evidence graph
    # ------------------------------------------------------------------

    def collect_from_evidence_graph(self) -> List[dict]:
        """Load STRONG_EVIDENCE / PARTIAL_EVIDENCE threads from evidence graph."""
        results = []
        try:
            try:
                import sys
                sys.path.insert(0, self.project_root)
                from evidence_graph.evidence_graph_store import EvidenceGraphStore
                store = EvidenceGraphStore(
                    output_dir=self._abs("data/backtest_results/evidence_graph")
                )
                threads = store.load_latest_threads()
            except Exception:
                threads = []

            if not threads:
                # Fallback: scan CSV directly
                pattern = self._abs("data/backtest_results/evidence_graph/evidence_graph_threads_*.csv")
                files = sorted(glob.glob(pattern))
                if files:
                    with open(files[-1], newline="", encoding="utf-8") as fh:
                        reader = csv.DictReader(fh)
                        threads = list(reader)

            accepted_strength = {"STRONG_EVIDENCE", "PARTIAL_EVIDENCE", "STRONG", "PARTIAL"}
            for i, t in enumerate(threads):
                strength = str(t.get("strength", t.get("evidence_strength", ""))).upper()
                if strength not in accepted_strength:
                    continue
                name = str(t.get("thread_id", t.get("name", t.get("strategy_id", f"thread_{i}"))))
                sid = _make_id("evidence_graph", i, name)
                results.append({
                    "strategy_id":   sid,
                    "strategy_name": _guard_name(name),
                    "strategy_type": STYPE_STRATEGY_HYPOTHESIS,
                    "source_module": "evidence_graph",
                    "source_ref":    f"evidence_graph_thread_{name}",
                    "description":   str(t.get("summary", t.get("description", ""))),
                })
        except Exception as exc:
            logger.warning("collect_from_evidence_graph: %s", exc)
        return results

    # ------------------------------------------------------------------
    # Backtest coach
    # ------------------------------------------------------------------

    def collect_from_backtest_coach(self) -> List[dict]:
        """Load recurring issues from backtest coach CSVs."""
        results = []
        try:
            pattern = self._abs("data/backtest_results/backtest_coach/*.csv")
            files = sorted(glob.glob(pattern))
            for fpath in files[-3:]:
                with open(fpath, newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh)
                    for i, row in enumerate(reader):
                        freq = str(row.get("frequency", row.get("recurrence", "0")))
                        try:
                            freq_val = float(freq)
                        except ValueError:
                            freq_val = 0.0
                        if freq_val < 2:
                            continue
                        name = str(row.get("issue_name", row.get("pattern_name", row.get("name", f"coach_issue_{i}"))))
                        sid = _make_id("backtest_coach", i, name)
                        results.append({
                            "strategy_id":   sid,
                            "strategy_name": _guard_name(name),
                            "strategy_type": STYPE_RULE_CANDIDATE,
                            "source_module": "backtest_coach",
                            "source_ref":    os.path.basename(fpath),
                            "description":   str(row.get("description", row.get("recommendation", ""))),
                        })
        except Exception as exc:
            logger.warning("collect_from_backtest_coach: %s", exc)
        return results

    # ------------------------------------------------------------------
    # Research intelligence
    # ------------------------------------------------------------------

    def collect_from_research_intelligence(self) -> List[dict]:
        """Load P1/P2 signals from research intelligence CSVs."""
        results = []
        try:
            pattern = self._abs("data/backtest_results/research_intelligence/*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                pattern2 = self._abs("intelligence_stable/*.csv")
                files = sorted(glob.glob(pattern2))

            for fpath in files[-3:]:
                with open(fpath, newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh)
                    for i, row in enumerate(reader):
                        priority = str(row.get("priority", row.get("signal_priority", "P3"))).upper()
                        if priority not in {"P1", "P2"}:
                            continue
                        name = str(row.get("signal_name", row.get("strategy_name", row.get("name", f"signal_{i}"))))
                        sid = _make_id("research_intelligence", i, name)
                        results.append({
                            "strategy_id":   sid,
                            "strategy_name": _guard_name(name),
                            "strategy_type": STYPE_STRATEGY_HYPOTHESIS,
                            "source_module": "research_intelligence",
                            "source_ref":    os.path.basename(fpath),
                            "description":   str(row.get("description", row.get("summary", ""))),
                        })
        except Exception as exc:
            logger.warning("collect_from_research_intelligence: %s", exc)
        return results
