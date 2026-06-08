"""
reports/evidence_graph_report.py — Evidence Graph Report Builder v0.8.3

Generates reports/evidence_graph_report_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice.
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_HEADER = """\
> **[!] Research Intelligence Evidence Graph Only.**
> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not Investment Advice. Does NOT place orders or auto-trade.**
"""


class EvidenceGraphReportBuilder:
    """Build the Research Intelligence Evidence Graph Markdown report.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        pass

    def build(
        self,
        mode:       str = "real",
        output_dir: str = "reports",
        graph_output_dir: str = "data/backtest_results/evidence_graph",
    ) -> str:
        """Build report and save to output_dir. Returns file path."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isabs(graph_output_dir):
            graph_output_dir = os.path.join(BASE_DIR, graph_output_dir)
        os.makedirs(output_dir, exist_ok=True)

        # Load or run engine
        nodes, edges, threads, summary = self._load_or_run(mode, graph_output_dir)

        lines = self._build_lines(mode, nodes, edges, threads, summary)
        content = "\n".join(lines)

        today = date.today().isoformat()
        fname = f"evidence_graph_report_{today}.md"
        path  = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("[EvidenceGraphReportBuilder] saved → %s", path)
        return path

    # ------------------------------------------------------------------

    def _load_or_run(self, mode: str, graph_dir: str):
        """Try to load latest data; fall back to running the engine."""
        from evidence_graph.evidence_graph_store import EvidenceGraphStore
        store   = EvidenceGraphStore(output_dir=graph_dir)
        nodes   = store.load_latest_nodes()
        edges   = store.load_latest_edges()
        threads = store.load_latest_threads()
        summary = store.load_latest_summary()

        if summary is None or not nodes:
            try:
                from evidence_graph.evidence_graph_engine import EvidenceGraphEngine
                engine = EvidenceGraphEngine(output_dir=graph_dir)
                result = engine.run(mode=mode)
                nodes   = result["nodes"]
                edges   = result["edges"]
                threads = result["threads"]
                summary = result["summary"]
            except Exception as exc:
                logger.warning("[EvidenceGraphReportBuilder] engine failed: %s", exc)
                from evidence_graph.evidence_graph_schema import EvidenceGraphSummary
                summary = EvidenceGraphSummary()
        return nodes, edges, threads, summary

    def _build_lines(self, mode, nodes, edges, threads, summary) -> List[str]:
        today = date.today().isoformat()
        L: List[str] = []

        L += [
            f"# Research Intelligence Evidence Graph Report",
            f"",
            _SAFETY_HEADER,
            f"**Date**: {today}  |  **Mode**: {mode}  |  **Version**: v0.8.3",
            f"",
            f"---",
            f"",
        ]

        # 一、總覽
        L += [
            f"## 一、總覽",
            f"",
            f"| 項目 | 值 |",
            f"|------|-----|",
            f"| Version | v0.8.3 |",
            f"| Evidence Graph Only | YES |",
            f"| Research Only | YES |",
            f"| No Real Orders | YES |",
            f"| Production Trading BLOCKED | YES |",
            f"| Total Nodes | {summary.total_nodes} |",
            f"| Total Edges | {summary.total_edges} |",
            f"| Orphan Nodes | {summary.orphan_node_count} |",
            f"| Contradictions | {summary.contradiction_count} |",
            f"| Requires Data | {summary.requires_data_count} |",
            f"| Requires Backtest | {summary.requires_backtest_count} |",
            f"| Requires Replay | {summary.requires_replay_count} |",
            f"| Overall Status | {summary.overall_status} |",
            f"",
        ]

        # 二、Top Evidence Threads
        L += [f"## 二、Top Evidence Threads", f""]
        if threads:
            for t in threads[:5]:
                L += [
                    f"### Thread: {t.get('anchor_title', '(unknown)')[:80]}",
                    f"- **Key Nodes**: {len(t.get('key_nodes', []))}",
                    f"- **Evidence Path**: {t.get('evidence_path', '')}",
                    f"- **Suggested Next Step**: {t.get('suggested_next_step', 'REVIEW')}",
                    f"",
                ]
        else:
            L += [f"_No evidence threads found. Run more Research OS modules to build evidence._", f""]

        # 三、Research Recommendation Evidence
        L += [f"## 三、Research Recommendation Evidence", f""]
        rec_nodes = [n for n in nodes if n.node_type == "RESEARCH_RECOMMENDATION"]
        if rec_nodes:
            for n in rec_nodes[:10]:
                L += [
                    f"- **{n.title[:80]}** _(confidence: {n.confidence:.2f}, priority: {n.priority})_",
                    f"  - Source: `{n.source_module}` | Status: {n.status}",
                ]
                if n.related_symbols:
                    L += [f"  - Symbols: {', '.join(n.related_symbols[:5])}"]
            L += [f""]
        else:
            L += [f"_No research recommendations found._", f""]

        # 四、Strategy Memory Evidence
        L += [f"## 四、Strategy Memory Evidence", f""]
        mem_nodes = [n for n in nodes if n.node_type in ("STRATEGY_MEMORY", "STRATEGY_HYPOTHESIS")]
        if mem_nodes:
            for n in mem_nodes[:10]:
                L += [f"- **{n.title[:80]}** _(type: {n.node_type}, confidence: {n.confidence:.2f})_"]
            L += [f""]
        else:
            L += [f"_No strategy memory nodes found._", f""]

        # 五、Backtest Coach Evidence
        L += [f"## 五、Backtest Coach Evidence", f""]
        coach_nodes = [n for n in nodes if n.node_type == "BACKTEST_COACH_TASK"]
        if coach_nodes:
            for n in coach_nodes[:10]:
                L += [f"- **{n.title[:80]}** _(priority: {n.priority}, status: {n.status})_"]
            L += [f""]
        else:
            L += [f"_No backtest coach tasks found._", f""]

        # 六、Training Metrics Evidence
        L += [f"## 六、Training Metrics Evidence", f""]
        metric_nodes = [n for n in nodes if n.node_type == "TRAINING_METRIC"]
        if metric_nodes:
            for n in metric_nodes[:10]:
                L += [f"- **{n.title[:80]}** | {n.summary[:100]}"]
            L += [f""]
        else:
            L += [f"_No training metrics found._", f""]

        # 七、Data / Report / Regression Evidence
        L += [f"## 七、Data / Report / Regression Evidence", f""]
        data_gap_nodes  = [n for n in nodes if n.node_type == "DATA_GAP"]
        report_nodes    = [n for n in nodes if n.node_type == "REPORT_RESULT"]
        reg_nodes       = [n for n in nodes if n.node_type == "REGRESSION_RESULT"]
        if data_gap_nodes:
            L += [f"**Data Gaps** ({len(data_gap_nodes)}):"]
            for n in data_gap_nodes[:5]:
                L += [f"- {n.title[:80]} _(source: {n.source_module})_"]
            L += [f""]
        if report_nodes:
            L += [f"**Report Results** ({len(report_nodes)}):"]
            for n in report_nodes[:5]:
                L += [f"- {n.title[:80]} | Status: {n.status}"]
            L += [f""]
        if reg_nodes:
            L += [f"**Regression Issues** ({len(reg_nodes)}):"]
            for n in reg_nodes[:5]:
                L += [f"- {n.title[:80]} | Status: {n.status}"]
            L += [f""]
        if not (data_gap_nodes or report_nodes or reg_nodes):
            L += [f"_No data/report/regression evidence nodes found._", f""]

        # 八、Graph Gaps
        L += [f"## 八、Graph Gaps", f""]
        orphan_nodes = [n for n in nodes]  # will compute properly
        try:
            connected = set()
            for e in edges:
                connected.add(e.source_node_id)
                connected.add(e.target_node_id)
            orphan_nodes = [n for n in nodes if n.node_id not in connected]
        except Exception:
            orphan_nodes = []

        L += [f"- **Orphan Nodes**: {len(orphan_nodes)}"]
        L += [f"- **Requires Data**: {summary.requires_data_count}"]
        L += [f"- **Requires Backtest**: {summary.requires_backtest_count}"]
        L += [f"- **Requires Replay**: {summary.requires_replay_count}"]
        if orphan_nodes:
            L += [f""]
            L += [f"**Orphan node titles**:"]
            for n in orphan_nodes[:8]:
                L += [f"- {n.title[:80]} _(type: {n.node_type})_"]
        L += [f""]

        # 九、Safety
        L += [
            f"## 九、Safety",
            f"",
            f"| Safety Item | Status |",
            f"|-------------|--------|",
            f"| Research Only | YES |",
            f"| No Real Orders | YES |",
            f"| No broker execution | YES |",
            f"| No auto trading | YES |",
            f"| Not investment advice | YES |",
            f"| Production Trading BLOCKED | YES |",
            f"",
            f"---",
            f"",
            f"_Generated by TW Quant Cockpit v0.8.3 — Research Intelligence Evidence Graph_",
            f"_Research Only. No Real Orders. Production Trading BLOCKED._",
        ]

        return L
