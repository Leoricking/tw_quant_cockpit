"""
reports/evidence_graph_report.py — Evidence Graph Report Builder v0.9.1

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
    """Build the Research Intelligence Evidence Graph UX Markdown report.

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
        nodes, edges, threads, summary, gaps = self._load_or_run(mode, graph_output_dir)

        lines = self._build_lines(mode, nodes, edges, threads, summary, gaps)
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

        # Load gaps — store method may not exist yet in v0.8.3 stores
        gaps = []
        try:
            gaps = store.load_latest_gaps()
        except AttributeError:
            pass
        except Exception as exc:
            logger.warning("[EvidenceGraphReportBuilder] gaps load failed: %s", exc)

        if summary is None or not nodes:
            try:
                from evidence_graph.evidence_graph_engine import EvidenceGraphEngine
                engine = EvidenceGraphEngine(output_dir=graph_dir)
                result = engine.run(mode=mode)
                nodes   = result["nodes"]
                edges   = result["edges"]
                threads = result["threads"]
                summary = result["summary"]
                # Re-try gaps after engine run
                try:
                    gaps = store.load_latest_gaps()
                except Exception:
                    pass
            except Exception as exc:
                logger.warning("[EvidenceGraphReportBuilder] engine failed: %s", exc)
                from evidence_graph.evidence_graph_schema import EvidenceGraphSummary
                summary = EvidenceGraphSummary()
        return nodes, edges, threads, summary, gaps

    def _build_lines(self, mode, nodes, edges, threads, summary, gaps=None) -> List[str]:
        if gaps is None:
            gaps = []
        today = date.today().isoformat()
        L: List[str] = []

        L += [
            f"# Research Intelligence Evidence Graph UX Report",
            f"",
            _SAFETY_HEADER,
            f"**Date**: {today}  |  **Mode**: {mode}  |  **Version**: v0.9.1",
            f"",
            f"---",
            f"",
        ]

        # ---------------------------------------------------------------
        # 一、總覽
        # ---------------------------------------------------------------
        # Crash reversal threads count
        cr_threads = []
        try:
            cr_keywords = ['crash', 'reversal', 'stabiliz', 'relative strength',
                           'sakata', 'eps', 'dip', 'industry guard', 'ma profit']
            for t in threads:
                td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                title = str(td.get('title', td.get('anchor_title', ''))).lower()
                mods  = str(td.get('source_modules', '')).lower()
                if 'crash_reversal' in mods or any(kw in title for kw in cr_keywords):
                    cr_threads.append(t)
        except Exception:
            pass

        L += [
            f"## 一、總覽",
            f"",
            f"| 項目 | 值 |",
            f"|------|-----|",
            f"| Version | v0.9.1 |",
            f"| Evidence Graph Only | YES |",
            f"| Research Only | YES |",
            f"| No Real Orders | YES |",
            f"| Production Trading BLOCKED | YES |",
            f"| Total Nodes | {summary.total_nodes} |",
            f"| Total Edges | {summary.total_edges} |",
            f"| Threads | {len(threads)} |",
            f"| Gaps | {len(gaps)} |",
            f"| Crash Reversal Threads | {len(cr_threads)} |",
            f"| Orphan Nodes | {summary.orphan_node_count} |",
            f"| Contradictions | {summary.contradiction_count} |",
            f"| Requires Data | {summary.requires_data_count} |",
            f"| Requires Backtest | {summary.requires_backtest_count} |",
            f"| Requires Replay | {summary.requires_replay_count} |",
            f"| Overall Status | {summary.overall_status} |",
            f"",
        ]

        # ---------------------------------------------------------------
        # 二、Evidence Thread Quality Board
        # ---------------------------------------------------------------
        L += [f"## 二、Evidence Thread Quality Board", f""]
        if threads:
            L += [
                f"| Thread | Quality Score | Quality Label | Nodes | Edges | Suggested Next Step |",
                f"|--------|--------------|---------------|-------|-------|---------------------|",
            ]
            for t in threads[:20]:
                td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                title       = str(td.get('title', td.get('anchor_title', '(unknown)')))[:60]
                q_score     = td.get('quality_score', 'N/A')
                q_label     = td.get('quality_label', 'INSUFFICIENT_DATA')
                node_count  = td.get('node_count', len(td.get('key_nodes', [])))
                edge_count  = td.get('edge_count', 'N/A')
                next_step   = td.get('suggested_next_step', 'REVIEW')
                # If quality fields missing, flag as insufficient
                if q_label in ('', 'INSUFFICIENT_DATA', None):
                    q_label = 'INSUFFICIENT_DATA — run evidence-graph-ux first'
                L += [f"| {title} | {q_score} | {q_label} | {node_count} | {edge_count} | {next_step} |"]
            L += [f""]
        else:
            L += [f"_No evidence threads found. Run more Research OS modules to build evidence._", f""]

        # ---------------------------------------------------------------
        # 三、Crash Reversal Evidence Chain
        # ---------------------------------------------------------------
        L += [f"## 三、Crash Reversal Evidence Chain", f""]
        L += [
            f"Chain: **Crash Cause** → **Stabilization** → **Relative Strength** → "
            f"**EPS-backed Dip Filter** → **MA Profit Discipline** → **High-Risk Industry Guard**",
            f"",
        ]

        # Map crash stages to node crash_stage field or keywords
        crash_stage_labels = [
            ("CRASH_CAUSE",            "Crash Cause"),
            ("STABILIZATION",          "Stabilization"),
            ("RELATIVE_STRENGTH",      "Relative Strength"),
            ("EPS_DIP_FILTER",         "EPS-backed Dip Filter"),
            ("MA_PROFIT_DISCIPLINE",   "MA Profit Discipline"),
            ("HIGH_RISK_GUARD",        "High-Risk Industry Guard"),
        ]

        # Collect crash reversal nodes
        cr_nodes = [n for n in nodes if getattr(n, 'is_crash_reversal_node', False)
                    or 'crash_reversal' in getattr(n, 'source_module', '').lower()]

        if cr_nodes:
            L += [
                f"| Stage | Node | Evidence Quality | Next Safe Action |",
                f"|-------|------|-----------------|-----------------|",
            ]
            for stage_key, stage_label in crash_stage_labels:
                stage_nodes = [n for n in cr_nodes
                               if getattr(n, 'crash_stage', '').upper() == stage_key]
                if stage_nodes:
                    for n in stage_nodes[:3]:
                        eq  = getattr(n, 'evidence_quality', n.status) or n.status
                        nxt = getattr(n, 'safe_next_step', '') or 'REVIEW'
                        L += [f"| {stage_label} | {n.title[:60]} | {eq} | {nxt} |"]
                else:
                    L += [f"| {stage_label} | _(no nodes)_ | — | — |"]
            L += [f""]
        elif cr_threads:
            L += [
                f"| Thread | Evidence Quality | Next Safe Action |",
                f"|--------|-----------------|-----------------|",
            ]
            for t in cr_threads[:6]:
                td  = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                ttl = str(td.get('title', td.get('anchor_title', '(unknown)')))[:60]
                eq  = td.get('quality_label', 'INSUFFICIENT_DATA — run evidence-graph-ux first')
                nxt = td.get('suggested_next_step', 'REVIEW')
                L += [f"| {ttl} | {eq} | {nxt} |"]
            L += [f""]
        else:
            L += [
                f"_INSUFFICIENT_DATA — run evidence-graph-ux first to build crash reversal chain._",
                f"",
            ]

        # ---------------------------------------------------------------
        # 四、Research Recommendation Evidence Paths
        # ---------------------------------------------------------------
        L += [f"## 四、Research Recommendation Evidence Paths", f""]
        rec_nodes = [n for n in nodes if n.node_type == "RESEARCH_RECOMMENDATION"]
        if rec_nodes:
            L += [
                f"| Recommendation | Memory | Coach Task | Metric | Report | Evidence Path |",
                f"|----------------|--------|-----------|--------|--------|---------------|",
            ]
            # Build quick lookup maps for related items
            mem_titles = {n.node_id: n.title for n in nodes
                          if n.node_type in ("STRATEGY_MEMORY", "STRATEGY_HYPOTHESIS")}
            coach_titles = {n.node_id: n.title for n in nodes
                            if n.node_type == "BACKTEST_COACH_TASK"}
            metric_titles = {n.node_id: n.title for n in nodes
                             if n.node_type == "TRAINING_METRIC"}
            report_titles = {n.node_id: n.title for n in nodes
                             if n.node_type == "REPORT_RESULT"}

            # Build adjacency for path lookup
            adj: Dict[str, List[str]] = {}
            for e in edges:
                adj.setdefault(e.source_node_id, []).append(e.target_node_id)
                adj.setdefault(e.target_node_id, []).append(e.source_node_id)

            for n in rec_nodes[:10]:
                neighbors = adj.get(n.node_id, [])
                mem_str   = "; ".join(mem_titles[nid][:30] for nid in neighbors if nid in mem_titles)[:50] or "—"
                coach_str = "; ".join(coach_titles[nid][:30] for nid in neighbors if nid in coach_titles)[:50] or "—"
                met_str   = "; ".join(metric_titles[nid][:30] for nid in neighbors if nid in metric_titles)[:50] or "—"
                rep_str   = "; ".join(report_titles[nid][:30] for nid in neighbors if nid in report_titles)[:50] or "—"
                # Evidence path from thread if available
                ev_path = "—"
                for t in threads:
                    td = t.to_dict() if hasattr(t, 'to_dict') else (t if isinstance(t, dict) else {})
                    key_nodes = td.get('key_nodes', [])
                    if isinstance(key_nodes, str):
                        key_nodes = [x for x in key_nodes.split('|') if x]
                    if n.node_id in key_nodes or td.get('anchor_node') == n.node_id:
                        ev_path = str(td.get('evidence_path', ''))[:60] or "—"
                        break
                L += [f"| {n.title[:50]} | {mem_str} | {coach_str} | {met_str} | {rep_str} | {ev_path} |"]
            L += [f""]
        else:
            L += [f"_No research recommendations found._", f""]

        # ---------------------------------------------------------------
        # 五、Graph Gaps
        # ---------------------------------------------------------------
        L += [f"## 五、Graph Gaps", f""]

        # Compute orphans inline
        try:
            connected = set()
            for e in edges:
                connected.add(e.source_node_id)
                connected.add(e.target_node_id)
            orphan_nodes_list = [n for n in nodes if n.node_id not in connected]
        except Exception:
            orphan_nodes_list = []

        # Duplicate clusters
        dup_clusters: List[List[str]] = []
        try:
            from evidence_graph.evidence_graph_schema import EDGE_DUPLICATES
            dup_edges = [e for e in edges if getattr(e, 'relation_type', '') == EDGE_DUPLICATES]
            clusters: Dict[int, set] = {}
            for e in dup_edges:
                src, tgt = e.source_node_id, e.target_node_id
                placed = False
                for k in clusters:
                    if src in clusters[k] or tgt in clusters[k]:
                        clusters[k].add(src)
                        clusters[k].add(tgt)
                        placed = True
                        break
                if not placed:
                    clusters[len(clusters)] = {src, tgt}
            dup_clusters = [list(v) for v in clusters.values()]
        except Exception:
            pass

        L += [
            f"| Gap Type | Count |",
            f"|----------|-------|",
            f"| Orphan Nodes | {len(orphan_nodes_list)} |",
            f"| Requires Data | {summary.requires_data_count} |",
            f"| Requires Backtest | {summary.requires_backtest_count} |",
            f"| Requires Replay | {summary.requires_replay_count} |",
            f"| Contradictions | {summary.contradiction_count} |",
            f"| Duplicate Clusters | {len(dup_clusters)} |",
            f"",
        ]

        # Loaded gaps from store (v0.9.1 EvidenceGraphGap objects)
        if gaps:
            L += [f"**Loaded Graph Gaps** ({len(gaps)}):"]
            L += [
                f"| # | Gap Type | Severity | Source Module | Title |",
                f"|---|----------|----------|---------------|-------|",
            ]
            for i, g in enumerate(gaps[:20], 1):
                gd = g.to_dict() if hasattr(g, 'to_dict') else (g if isinstance(g, dict) else {})
                L += [
                    f"| {i} | {gd.get('gap_type','—')} | {gd.get('severity','—')} "
                    f"| {str(gd.get('source_module','—'))[:30]} | {str(gd.get('title','—'))[:50]} |"
                ]
            L += [f""]
        else:
            L += [f"_No gap objects loaded. Run evidence-graph-ux to populate gaps._", f""]

        if orphan_nodes_list:
            L += [f"**Orphan node titles**:"]
            for n in orphan_nodes_list[:8]:
                L += [f"- {n.title[:80]} _(type: {n.node_type})_"]
            L += [f""]

        # ---------------------------------------------------------------
        # 六、Node Explanations
        # ---------------------------------------------------------------
        L += [f"## 六、Node Explanations", f""]
        # Show top nodes with explanations (prioritise high-priority or recent)
        explain_nodes = [n for n in nodes if n.priority in ("HIGH", "CRITICAL")][:10] or nodes[:10]
        if explain_nodes:
            L += [
                f"| Node | Why It Exists | Related Evidence | Next Safe Action |",
                f"|------|--------------|-----------------|-----------------|",
            ]
            adj2: Dict[str, List[str]] = {}
            for e in edges:
                adj2.setdefault(e.source_node_id, []).append(e.target_node_id)
                adj2.setdefault(e.target_node_id, []).append(e.source_node_id)
            node_map = {n.node_id: n for n in nodes}
            for n in explain_nodes:
                why = f"{n.node_type} from {n.source_module}"
                neighbor_titles = [node_map[nid].title[:30] for nid in adj2.get(n.node_id, [])[:3]
                                   if nid in node_map]
                related_str = "; ".join(neighbor_titles) or "—"
                next_act = getattr(n, 'safe_next_step', '') or 'REVIEW'
                L += [f"| {n.title[:50]} | {why} | {related_str} | {next_act} |"]
            L += [f""]
        else:
            L += [f"_No nodes available for explanation._", f""]

        # ---------------------------------------------------------------
        # 七、Contradictions / Weak Evidence
        # ---------------------------------------------------------------
        L += [f"## 七、Contradictions / Weak Evidence", f""]
        from evidence_graph.evidence_graph_schema import EDGE_CONTRADICTS
        contradiction_edges = [e for e in edges if e.relation_type == EDGE_CONTRADICTS]
        low_conf_edges      = [e for e in edges if getattr(e, 'confidence', 1.0) < 0.4]

        if contradiction_edges or low_conf_edges:
            L += [
                f"| Source | Target | Relation | Why Conflicted | Safe Next Step |",
                f"|--------|--------|----------|---------------|----------------|",
            ]
            node_map2 = {n.node_id: n for n in nodes}
            shown = set()
            for e in (contradiction_edges + low_conf_edges)[:15]:
                if e.edge_id in shown:
                    continue
                shown.add(e.edge_id)
                src_title = node_map2[e.source_node_id].title[:30] if e.source_node_id in node_map2 else e.source_node_id[:20]
                tgt_title = node_map2[e.target_node_id].title[:30] if e.target_node_id in node_map2 else e.target_node_id[:20]
                why = str(e.description or e.evidence or '—')[:50]
                nxt = getattr(e, 'suggested_next_step', '') or 'REVIEW'
                L += [f"| {src_title} | {tgt_title} | {e.relation_type} | {why} | {nxt} |"]
            L += [f""]
        else:
            L += [f"_No contradictions or weak evidence edges found._", f""]

        # ---------------------------------------------------------------
        # 八、Suggested Safe Next Steps
        # ---------------------------------------------------------------
        L += [f"## 八、Suggested Safe Next Steps", f""]
        # Aggregate next steps from nodes
        step_counts: Dict[str, int] = {}
        for n in nodes:
            step = getattr(n, 'safe_next_step', '') or 'REVIEW'
            step_counts[step] = step_counts.get(step, 0) + 1
        for e in edges:
            step = getattr(e, 'suggested_next_step', '') or ''
            if step:
                step_counts[step] = step_counts.get(step, 0) + 1

        canonical_steps = [
            "REVIEW", "BACKTEST_MORE", "PRACTICE_REPLAY",
            "FIX_DATA", "READ_REPORT", "DO_NOT_CHASE",
        ]
        L += [
            f"| Safe Next Step | Count | Meaning |",
            f"|----------------|-------|---------|",
            f"| REVIEW | {step_counts.get('REVIEW', 0)} | Review evidence before any action |",
            f"| BACKTEST_MORE | {step_counts.get('BACKTEST_MORE', 0)} | Run additional backtests |",
            f"| PRACTICE_REPLAY | {step_counts.get('PRACTICE_REPLAY', 0)} | Replay training drill |",
            f"| FIX_DATA | {step_counts.get('FIX_DATA', 0)} | Resolve data gap/quality issue |",
            f"| READ_REPORT | {step_counts.get('READ_REPORT', 0)} | Read relevant report output |",
            f"| DO_NOT_CHASE | {step_counts.get('DO_NOT_CHASE', 0)} | Do not chase — wait for setup |",
        ]
        # Any other steps present
        others = {k: v for k, v in step_counts.items() if k not in canonical_steps and k}
        for step, cnt in sorted(others.items(), key=lambda x: -x[1])[:5]:
            L += [f"| {step} | {cnt} | — |"]
        L += [f""]

        # ---------------------------------------------------------------
        # 九、安全聲明
        # ---------------------------------------------------------------
        L += [
            f"## 九、安全聲明",
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
            f"_Generated by TW Quant Cockpit v0.9.1 — Research Intelligence Evidence Graph UX_",
            f"_Research Only. No Real Orders. Production Trading BLOCKED._",
        ]

        return L
