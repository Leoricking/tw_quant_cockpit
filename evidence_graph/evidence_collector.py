"""
evidence_graph/evidence_collector.py — Evidence Collector v0.8.3

Collects EvidenceNode objects from all Research OS source modules.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Graceful fallback if any source module is missing or has no data.
[!] Does NOT read tokens. Does NOT place orders. Does NOT output trading commands.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

from evidence_graph.evidence_graph_schema import (
    EvidenceNode,
    NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_MEMORY, NODE_BACKTEST_COACH_TASK,
    NODE_TRAINING_METRIC, NODE_REPLAY_MISTAKE, NODE_JOURNAL_PATTERN,
    NODE_DATA_GAP, NODE_REPORT_RESULT, NODE_REGRESSION_RESULT,
    NODE_RULE_CANDIDATE, NODE_STRATEGY_HYPOTHESIS, NODE_PROVIDER_LIMITATION,
    NODE_STABLE_CHECK,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _node_id(prefix: str, idx: int) -> str:
    return f"{prefix}_{idx:04d}"


class EvidenceCollector:
    """Collects EvidenceNodes from all Research OS modules.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        if not os.path.isabs(project_root):
            project_root = os.path.join(BASE_DIR, project_root)
        self.project_root = project_root

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def collect_all(self, mode: str = "real") -> List[EvidenceNode]:
        """Collect nodes from all sources. Graceful fallback per source."""
        nodes: List[EvidenceNode] = []
        collectors = [
            self.collect_research_intelligence_nodes,
            self.collect_strategy_memory_nodes,
            self.collect_backtest_coach_nodes,
            self.collect_training_metrics_nodes,
            self.collect_replay_training_nodes,
            self.collect_portfolio_journal_nodes,
            self.collect_data_coverage_nodes,
            self.collect_report_pack_nodes,
            self.collect_regression_nodes,
            self.collect_rule_governance_nodes,
        ]
        for fn in collectors:
            try:
                partial = fn()
                nodes.extend(partial)
            except Exception as exc:
                logger.warning("[EvidenceCollector] %s failed: %s", fn.__name__, exc)
        logger.info("[EvidenceCollector] collected %d nodes total", len(nodes))
        return nodes

    # ------------------------------------------------------------------
    # Source-specific collectors
    # ------------------------------------------------------------------

    def collect_research_intelligence_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "research_intelligence")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            # recommendations
            rec_csv = self._latest_csv(out_dir, "recommendations")
            if rec_csv:
                with open(rec_csv, newline="", encoding="utf-8") as f:
                    for i, row in enumerate(csv.DictReader(f)):
                        title   = row.get("title", row.get("recommendation", "")) or ""
                        summary = row.get("summary", row.get("evidence", "")) or ""
                        symbols = [s.strip() for s in str(row.get("symbols", "")).split(",") if s.strip()]
                        nodes.append(EvidenceNode(
                            node_id=_node_id("RI_REC", len(nodes)),
                            node_type=NODE_RESEARCH_RECOMMENDATION,
                            title=title[:120] or f"RI Recommendation #{i+1}",
                            summary=summary[:500],
                            source_module="research_intelligence",
                            source_ref=os.path.basename(rec_csv),
                            confidence=float(row.get("confidence", 0.6) or 0.6),
                            priority=row.get("priority", "MEDIUM") or "MEDIUM",
                            related_symbols=symbols,
                        ))
            # priority board
            prio_csv = self._latest_csv(out_dir, "priority_board")
            if prio_csv:
                with open(prio_csv, newline="", encoding="utf-8") as f:
                    for i, row in enumerate(csv.DictReader(f)):
                        title = row.get("title", row.get("item", "")) or ""
                        if not title:
                            continue
                        nodes.append(EvidenceNode(
                            node_id=_node_id("RI_PRIO", len(nodes)),
                            node_type=NODE_RESEARCH_RECOMMENDATION,
                            title=title[:120],
                            summary=row.get("description", row.get("summary", ""))[:500],
                            source_module="research_intelligence",
                            source_ref=os.path.basename(prio_csv),
                            confidence=float(row.get("confidence", 0.5) or 0.5),
                            priority=row.get("priority", "HIGH") or "HIGH",
                        ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] research_intelligence: %s", exc)
        return nodes

    def collect_strategy_memory_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "strategy_memory")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            mem_csv = self._latest_csv(out_dir, "strategy_memories")
            if not mem_csv:
                mem_csv = self._latest_csv(out_dir, "memories")
            if mem_csv:
                with open(mem_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        mem_type = row.get("memory_type", "") or ""
                        title    = row.get("title", row.get("name", "")) or ""
                        summary  = row.get("summary", row.get("evidence", "")) or ""
                        symbols  = [s.strip() for s in str(row.get("related_symbols", "")).split(",") if s.strip()]
                        node_type_map = {
                            "STRATEGY_HYPOTHESIS":    NODE_STRATEGY_HYPOTHESIS,
                            "RULE_CANDIDATE":         NODE_RULE_CANDIDATE,
                            "REPLAY_MISTAKE_PATTERN": NODE_REPLAY_MISTAKE,
                            "DATA_GAP":               NODE_DATA_GAP,
                            "REPORT_GAP":             NODE_REPORT_RESULT,
                        }
                        ntype = node_type_map.get(mem_type.upper(), NODE_STRATEGY_MEMORY)
                        if not title:
                            continue
                        nodes.append(EvidenceNode(
                            node_id=_node_id("SM", len(nodes)),
                            node_type=ntype,
                            title=title[:120],
                            summary=summary[:500],
                            source_module="strategy_memory",
                            source_ref=os.path.basename(mem_csv),
                            status=row.get("status", "ACTIVE") or "ACTIVE",
                            confidence=float(row.get("confidence", 0.5) or 0.5),
                            related_symbols=symbols,
                            related_strategies=[s.strip() for s in str(row.get("related_strategies", "")).split(",") if s.strip()],
                        ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] strategy_memory: %s", exc)
        return nodes

    def collect_backtest_coach_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "backtest_coach")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            tasks_csv = self._latest_csv(out_dir, "coach_tasks")
            if not tasks_csv:
                tasks_csv = self._latest_csv(out_dir, "tasks")
            if tasks_csv:
                with open(tasks_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        title = row.get("title", row.get("task", "")) or ""
                        if not title:
                            continue
                        nodes.append(EvidenceNode(
                            node_id=_node_id("BC", len(nodes)),
                            node_type=NODE_BACKTEST_COACH_TASK,
                            title=title[:120],
                            summary=row.get("description", row.get("summary", ""))[:500],
                            source_module="backtest_coach",
                            source_ref=os.path.basename(tasks_csv),
                            status=row.get("status", "PENDING") or "PENDING",
                            confidence=float(row.get("confidence", 0.5) or 0.5),
                            priority=row.get("priority", "MEDIUM") or "MEDIUM",
                            related_symbols=[s.strip() for s in str(row.get("related_symbols", "")).split(",") if s.strip()],
                        ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] backtest_coach: %s", exc)
        return nodes

    def collect_training_metrics_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "training_metrics")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            metrics_csv = self._latest_csv(out_dir, "training_metrics")
            if not metrics_csv:
                metrics_csv = self._latest_csv(out_dir, "metrics")
            if metrics_csv:
                with open(metrics_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        label = row.get("label", row.get("metric_type", "")) or ""
                        if not label:
                            continue
                        status = row.get("status", "") or ""
                        trend  = row.get("trend", "") or ""
                        summary = f"Value: {row.get('value', '?')} {row.get('unit', '')} | Trend: {trend} | Status: {status}"
                        nodes.append(EvidenceNode(
                            node_id=_node_id("TM", len(nodes)),
                            node_type=NODE_TRAINING_METRIC,
                            title=label[:120],
                            summary=summary[:500],
                            source_module="training_metrics",
                            source_ref=os.path.basename(metrics_csv),
                            status=status or "ACTIVE",
                            confidence=float(row.get("confidence", 0.5) or 0.5),
                        ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] training_metrics: %s", exc)
        return nodes

    def collect_replay_training_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            replay_dir = os.path.join(self.project_root, "replay_sessions")
            if not os.path.isdir(replay_dir):
                return nodes
            import csv
            for fname in sorted(os.listdir(replay_dir)):
                if not fname.endswith(".csv"):
                    continue
                fpath = os.path.join(replay_dir, fname)
                try:
                    with open(fpath, newline="", encoding="utf-8") as f:
                        for row in csv.DictReader(f):
                            mistake = row.get("mistake", row.get("error", row.get("note", ""))) or ""
                            if not mistake:
                                continue
                            nodes.append(EvidenceNode(
                                node_id=_node_id("RT", len(nodes)),
                                node_type=NODE_REPLAY_MISTAKE,
                                title=mistake[:120],
                                summary=row.get("description", mistake)[:500],
                                source_module="replay_training",
                                source_ref=fname,
                                status="ACTIVE",
                                confidence=float(row.get("confidence", 0.4) or 0.4),
                                related_symbols=[s.strip() for s in str(row.get("symbol", "")).split(",") if s.strip()],
                            ))
                except Exception:
                    pass
        except Exception as exc:
            logger.warning("[EvidenceCollector] replay_training: %s", exc)
        return nodes

    def collect_portfolio_journal_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            journal_dir = os.path.join(self.project_root, "journal_data")
            if not os.path.isdir(journal_dir):
                return nodes
            import csv
            for fname in sorted(os.listdir(journal_dir)):
                if not fname.endswith(".csv"):
                    continue
                fpath = os.path.join(journal_dir, fname)
                try:
                    with open(fpath, newline="", encoding="utf-8") as f:
                        for row in csv.DictReader(f):
                            tags    = row.get("tags", row.get("mistake_tags", "")) or ""
                            quality = row.get("process_quality", row.get("quality_note", "")) or ""
                            item    = tags or quality
                            if not item:
                                continue
                            nodes.append(EvidenceNode(
                                node_id=_node_id("PJ", len(nodes)),
                                node_type=NODE_JOURNAL_PATTERN,
                                title=item[:120],
                                summary=row.get("note", item)[:500],
                                source_module="portfolio_journal",
                                source_ref=fname,
                                status="ACTIVE",
                                confidence=0.45,
                                related_symbols=[s.strip() for s in str(row.get("symbol", "")).split(",") if s.strip()],
                            ))
                except Exception:
                    pass
        except Exception as exc:
            logger.warning("[EvidenceCollector] portfolio_journal: %s", exc)
        return nodes

    def collect_data_coverage_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "data_coverage")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            cov_csv = self._latest_csv(out_dir, "data_coverage")
            if not cov_csv:
                cov_csv = self._latest_csv(out_dir, "coverage")
            if cov_csv:
                with open(cov_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        item_id = row.get("item_id", row.get("dataset_name", "")) or ""
                        if not item_id:
                            continue
                        missing   = str(row.get("missing_required", row.get("required", ""))).lower()
                        env_limit = str(row.get("environment_limited", "")).lower()
                        not_gen   = str(row.get("not_generated", "")). lower()
                        if env_limit in ("true", "1", "yes"):
                            ntype = NODE_PROVIDER_LIMITATION
                        else:
                            ntype = NODE_DATA_GAP
                        if missing in ("true", "1", "yes") or not_gen in ("true", "1", "yes") or env_limit in ("true", "1", "yes"):
                            nodes.append(EvidenceNode(
                                node_id=_node_id("DC", len(nodes)),
                                node_type=ntype,
                                title=item_id[:120],
                                summary=row.get("description", f"Data gap: {item_id}")[:500],
                                source_module="data_coverage",
                                source_ref=os.path.basename(cov_csv),
                                status="NEEDS_FIX",
                                confidence=0.9,
                            ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] data_coverage: %s", exc)
        return nodes

    def collect_report_pack_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            from report_pack.report_collector import ReportCollector
            from report_pack.report_pack_schema import ALL_REPORT_TYPES
            collector = ReportCollector(base_dir=self.project_root)
            items     = collector.collect(report_types=list(ALL_REPORT_TYPES))
            for item in items:
                status = getattr(item, "status", "")
                if status in ("MISSING", "FAILED", "ENV_LIMITED", "NOT_GENERATED"):
                    rtype = getattr(item, "report_type", "")
                    nodes.append(EvidenceNode(
                        node_id=_node_id("RP", len(nodes)),
                        node_type=NODE_REPORT_RESULT,
                        title=f"Report {rtype}: {status}",
                        summary=f"Report {rtype} status: {status}",
                        source_module="report_pack",
                        source_ref=rtype,
                        status=status,
                        confidence=0.85,
                    ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] report_pack: %s", exc)
        return nodes

    def collect_regression_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "regression")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            reg_csv = self._latest_csv(out_dir, "regression")
            if not reg_csv:
                reg_csv = self._latest_csv(out_dir, "results")
            if reg_csv:
                with open(reg_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        name   = row.get("name", row.get("test", "")) or ""
                        status = row.get("status", "") or ""
                        if status in ("FAIL", "WARN", "BLOCKED") and name:
                            nodes.append(EvidenceNode(
                                node_id=_node_id("RG", len(nodes)),
                                node_type=NODE_REGRESSION_RESULT,
                                title=f"Regression {name}: {status}",
                                summary=row.get("detail", row.get("message", ""))[:500],
                                source_module="regression",
                                source_ref=os.path.basename(reg_csv),
                                status=status,
                                confidence=0.8,
                            ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] regression: %s", exc)
        return nodes

    def collect_rule_governance_nodes(self) -> List[EvidenceNode]:
        nodes: List[EvidenceNode] = []
        try:
            out_dir = os.path.join(self.project_root,
                                   "data", "backtest_results", "rule_governance")
            if not os.path.isdir(out_dir):
                return nodes
            import csv
            rules_csv = self._latest_csv(out_dir, "rules")
            if not rules_csv:
                rules_csv = self._latest_csv(out_dir, "rule_governance")
            if rules_csv:
                with open(rules_csv, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        name       = row.get("rule_name", row.get("name", "")) or ""
                        confidence = float(row.get("confidence", 0.5) or 0.5)
                        status     = row.get("status", "") or ""
                        needs_review = str(row.get("needs_review", "")).lower() in ("true", "1", "yes")
                        is_candidate = str(row.get("is_candidate", "")).lower() in ("true", "1", "yes")
                        if not name:
                            continue
                        if confidence < 0.5 or needs_review or is_candidate:
                            nodes.append(EvidenceNode(
                                node_id=_node_id("RGV", len(nodes)),
                                node_type=NODE_RULE_CANDIDATE,
                                title=name[:120],
                                summary=row.get("description", f"Rule candidate: {name}")[:500],
                                source_module="rule_governance",
                                source_ref=os.path.basename(rules_csv),
                                status=status or "REVIEW",
                                confidence=confidence,
                            ))
        except Exception as exc:
            logger.warning("[EvidenceCollector] rule_governance: %s", exc)
        return nodes

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _latest_csv(self, directory: str, prefix: str) -> Optional[str]:
        """Return the most recently modified CSV file whose name starts with prefix."""
        try:
            files = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if f.startswith(prefix) and f.endswith(".csv")
            ]
            if not files:
                return None
            return max(files, key=os.path.getmtime)
        except Exception:
            return None


# Fix Optional import
from typing import Optional
