"""
evidence_graph/evidence_graph_builder.py — Evidence Graph Builder v0.9.1

Builds EvidenceEdge objects from collected EvidenceNodes.
Adds EvidenceThread and EvidenceGraphGap construction.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Conservative duplicate/contradiction detection — readability over completeness.
[!] Max 20 edges per node to avoid explosion.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Dict, List, Set, Tuple

from evidence_graph.evidence_graph_schema import (
    EvidenceEdge, EvidenceNode,
    EDGE_SUPPORTS, EDGE_CONTRADICTS, EDGE_DUPLICATES, EDGE_REFINES,
    EDGE_REQUIRES_DATA, EDGE_REQUIRES_BACKTEST, EDGE_REQUIRES_REPLAY,
    EDGE_REQUIRES_JOURNAL_REVIEW, EDGE_GENERATED_FROM, EDGE_VALIDATED_BY,
    EDGE_WEAKENED_BY, EDGE_RELATED_TO,
    NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_MEMORY, NODE_BACKTEST_COACH_TASK,
    NODE_TRAINING_METRIC, NODE_REPLAY_MISTAKE, NODE_JOURNAL_PATTERN,
    NODE_DATA_GAP, NODE_REPORT_RESULT, NODE_REGRESSION_RESULT,
    NODE_RULE_CANDIDATE, NODE_STRATEGY_HYPOTHESIS, NODE_PROVIDER_LIMITATION,
    THREAD_STRONG_EVIDENCE, THREAD_PARTIAL_EVIDENCE, THREAD_NEEDS_DATA,
    THREAD_NEEDS_BACKTEST, THREAD_CONFLICTED, THREAD_ORPHANED,
    GAP_ORPHAN_NODE, GAP_REQUIRES_DATA, GAP_REQUIRES_BACKTEST, GAP_REQUIRES_REPLAY,
    GAP_CONTRADICTION, GAP_LOW_CONFIDENCE_EDGE, GAP_DUPLICATE_CLUSTER,
    CRASH_STAGE_CRASH_CAUSE, CRASH_STAGE_STABILIZATION, CRASH_STAGE_RELATIVE_STRENGTH,
    CRASH_STAGE_EPS_DIP_FILTER, CRASH_STAGE_MA_PROFIT_DISCIPLINE, CRASH_STAGE_HIGH_RISK_GUARD,
)

# v0.9.1: try to import new schema classes — backward compat if not yet added
try:
    from evidence_graph.evidence_graph_schema import EvidenceThread, EvidenceGraphGap
    _THREAD_SCHEMA_AVAILABLE = True
except ImportError:
    _THREAD_SCHEMA_AVAILABLE = False

logger = logging.getLogger(__name__)

MAX_EDGES_PER_NODE = 20
MAX_TOTAL_EDGES    = 2000


def _edge_id(src: str, tgt: str, rel: str) -> str:
    raw = f"{src}|{tgt}|{rel}"
    return "E_" + hashlib.md5(raw.encode()).hexdigest()[:12]


class EvidenceGraphBuilder:
    """Builds edges between EvidenceNodes.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._edge_set: Set[str] = set()

    def build_edges(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """Main entry point: build all edges from node list."""
        self._edge_set = set()
        edges: List[EvidenceEdge] = []

        edges.extend(self.link_by_symbol(nodes))
        edges.extend(self.link_by_strategy(nodes))
        edges.extend(self.link_by_rule(nodes))
        edges.extend(self.link_by_memory(nodes))
        edges.extend(self.link_by_task(nodes))
        edges.extend(self.detect_duplicates(nodes))
        edges.extend(self.detect_contradictions(nodes))
        # v0.9.0.1 crash reversal
        try:
            edges.extend(self._link_crash_reversal_nodes(nodes))
        except Exception as exc:
            logger.warning("[EvidenceGraphBuilder] _link_crash_reversal_nodes failed: %s", exc)

        # Cap total edges to keep graph readable
        if len(edges) > MAX_TOTAL_EDGES:
            edges = edges[:MAX_TOTAL_EDGES]
        logger.info("[EvidenceGraphBuilder] built %d edges from %d nodes", len(edges), len(nodes))
        return edges

    def build_evidence_threads(
        self, nodes: List[EvidenceNode], edges: List[EvidenceEdge]
    ) -> list:
        """Build evidence threads: connected chains starting from RESEARCH_RECOMMENDATION nodes.

        v0.9.1: Returns List[EvidenceThread] if schema available, else List[Dict].
        Merges crash reversal threads and caps at 20 threads total.
        """
        threads: list = []
        node_map = {n.node_id: n for n in nodes}

        # Build adjacency (outgoing)
        adj: Dict[str, List[str]] = {}
        for e in edges:
            adj.setdefault(e.source_node_id, []).append(e.target_node_id)

        # Build edge lookup by node
        edges_by_node: Dict[str, List[EvidenceEdge]] = {}
        for e in edges:
            edges_by_node.setdefault(e.source_node_id, []).append(e)

        anchor_types = {NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_HYPOTHESIS}
        anchors = [n for n in nodes if n.node_type in anchor_types]

        seen_threads: Set[str] = set()
        for anchor in anchors[:20]:  # cap at 20 threads
            thread_nodes = self._bfs(anchor.node_id, adj, max_depth=3, node_map=node_map)
            key = "|".join(sorted(n.node_id for n in thread_nodes))
            if key in seen_threads:
                continue
            seen_threads.add(key)

            thread_node_ids = [n.node_id for n in thread_nodes]
            thread_node_id_set = set(thread_node_ids)

            # Determine thread edges
            thread_edge_ids = [
                e.edge_id for e in edges
                if e.source_node_id in thread_node_id_set
                or e.target_node_id in thread_node_id_set
            ]

            # Determine suggested next step from edges
            next_steps = []
            for e in edges:
                if e.source_node_id == anchor.node_id and e.suggested_next_step:
                    next_steps.append(e.suggested_next_step)

            # Collect metadata fields
            thread_id = f"T_{len(threads):04d}"
            title = anchor.title
            summary_text = anchor.summary if hasattr(anchor, "summary") else ""
            source_modules = list({n.source_module for n in thread_nodes if n.source_module})
            related_symbols = list({
                sym for n in thread_nodes for sym in (n.related_symbols or [])
            })
            related_strategies = list({
                s for n in thread_nodes for s in (n.related_strategies or [])
            })
            related_rules = list({
                r for n in thread_nodes for r in (n.related_rules or [])
            })
            evidence_path = [n.node_type for n in thread_nodes]
            suggested_next_step = next_steps[0] if next_steps else "REVIEW"

            # Count edge types in thread
            thread_edge_set = set(thread_edge_ids)
            thread_edges = [e for e in edges if e.edge_id in thread_edge_set]
            support_count = sum(1 for e in thread_edges if e.relation_type == EDGE_SUPPORTS)
            contradiction_count = sum(1 for e in thread_edges if e.relation_type == EDGE_CONTRADICTS)
            requires_data_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_DATA)
            requires_backtest_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_BACKTEST)
            requires_replay_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_REPLAY)

            if _THREAD_SCHEMA_AVAILABLE:
                try:
                    quality_score, quality_label, step = self.calculate_thread_quality(
                        thread_node_ids, thread_edge_ids, nodes, edges
                    )
                    if step:
                        suggested_next_step = step

                    thread_obj = EvidenceThread(
                        thread_id=thread_id,
                        title=title,
                        summary=summary_text,
                        node_ids=thread_node_ids,
                        edge_ids=thread_edge_ids,
                        node_count=len(thread_node_ids),
                        edge_count=len(thread_edge_ids),
                        support_count=support_count,
                        contradiction_count=contradiction_count,
                        requires_data_count=requires_data_count,
                        requires_backtest_count=requires_backtest_count,
                        requires_replay_count=requires_replay_count,
                        quality_score=quality_score,
                        quality_label=quality_label,
                        suggested_next_step=suggested_next_step,
                        evidence_path=evidence_path,
                        related_symbols=related_symbols,
                        related_strategies=related_strategies,
                        related_rules=related_rules,
                        source_modules=source_modules,
                        no_real_orders=True,
                        production_blocked=True,
                    )
                    threads.append(thread_obj)
                    continue
                except Exception as exc:
                    logger.warning("[EvidenceGraphBuilder] EvidenceThread creation failed: %s", exc)

            # Fallback: return dict (backward compat)
            threads.append({
                "thread_id":   thread_id,
                "anchor_node": anchor.node_id,
                "anchor_title": anchor.title,
                "title": title,
                "key_nodes":   thread_node_ids,
                "node_titles": [n.title for n in thread_nodes],
                "evidence_path": " -> ".join(evidence_path),
                "suggested_next_step": suggested_next_step,
                "node_count":  len(thread_nodes),
                "source_modules": "|".join(source_modules),
                "no_real_orders": True,
                "production_blocked": True,
            })

        # v0.9.1: merge crash reversal threads
        try:
            cr_threads = self.build_crash_reversal_threads(nodes, edges)
            for t in cr_threads:
                if len(threads) >= 20:
                    break
                threads.append(t)
        except Exception as exc:
            logger.warning("[EvidenceGraphBuilder] build_crash_reversal_threads failed: %s", exc)

        return threads

    # ------------------------------------------------------------------
    # v0.9.1 New methods
    # ------------------------------------------------------------------

    def calculate_thread_quality(
        self,
        thread_node_ids: list,
        thread_edge_ids: list,
        nodes: list,
        edges: list,
    ) -> tuple:
        """Returns (quality_score: float, quality_label: str, suggested_next_step: str).

        Score calculation:
          +20 per SUPPORTS edge in thread
          +20 per VALIDATED_BY edge in thread
          +15 if thread has strategy memory node
          +15 if thread has training metric node (improving)
          +10 if thread has report result node
          -20 per REQUIRES_DATA edge
          -15 per REQUIRES_BACKTEST edge
          -10 per REQUIRES_REPLAY edge
          -30 per CONTRADICTS edge
          -20 if any node is orphan (no edges)
          -10 per LOW_CONFIDENCE edge (confidence < 0.4)
        Score clamped to 0-100.
        """
        node_id_set = set(thread_node_ids)
        edge_id_set = set(thread_edge_ids)

        thread_nodes = [n for n in nodes if n.node_id in node_id_set]
        thread_edges = [e for e in edges if e.edge_id in edge_id_set]

        # Connected node IDs for orphan check
        connected_ids: Set[str] = set()
        for e in edges:
            connected_ids.add(e.source_node_id)
            connected_ids.add(e.target_node_id)

        score = 0.0

        # Positive signals
        for e in thread_edges:
            if e.relation_type == EDGE_SUPPORTS:
                score += 20
            elif e.relation_type == EDGE_VALIDATED_BY:
                score += 20

        has_memory = any(n.node_type == NODE_STRATEGY_MEMORY for n in thread_nodes)
        if has_memory:
            score += 15

        has_improving_metric = any(
            n.node_type == NODE_TRAINING_METRIC
            and ("IMPROVING" in n.status.upper() or "IMPROVING" in n.summary.upper())
            for n in thread_nodes
        )
        if has_improving_metric:
            score += 15

        has_report = any(n.node_type == NODE_REPORT_RESULT for n in thread_nodes)
        if has_report:
            score += 10

        # Negative signals
        for e in thread_edges:
            if e.relation_type == EDGE_REQUIRES_DATA:
                score -= 20
            elif e.relation_type == EDGE_REQUIRES_BACKTEST:
                score -= 15
            elif e.relation_type == EDGE_REQUIRES_REPLAY:
                score -= 10
            elif e.relation_type == EDGE_CONTRADICTS:
                score -= 30
            elif e.confidence < 0.4:
                score -= 10

        orphan_count = sum(1 for n in thread_nodes if n.node_id not in connected_ids)
        score -= orphan_count * 20

        # Clamp
        score = max(0.0, min(100.0, score))

        # Determine label
        requires_data_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_DATA)
        requires_backtest_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_BACKTEST)

        if score >= 80:
            quality_label = THREAD_STRONG_EVIDENCE
            suggested_next_step = "REVIEW"
        elif score >= 60:
            quality_label = THREAD_PARTIAL_EVIDENCE
            suggested_next_step = "VALIDATE"
        elif score >= 40:
            if requires_data_count > requires_backtest_count:
                quality_label = THREAD_NEEDS_DATA
                suggested_next_step = "FIX_DATA"
            else:
                quality_label = THREAD_NEEDS_BACKTEST
                suggested_next_step = "BACKTEST_MORE"
        else:
            contradiction_count = sum(1 for e in thread_edges if e.relation_type == EDGE_CONTRADICTS)
            if contradiction_count > 0 or orphan_count == 0:
                quality_label = THREAD_CONFLICTED
                suggested_next_step = "TRACE_EVIDENCE"
            else:
                quality_label = THREAD_ORPHANED
                suggested_next_step = "REVIEW"

        return (score, quality_label, suggested_next_step)

    def build_graph_gaps(self, nodes: list, edges: list) -> list:
        """Identify graph gaps: orphans, missing data, contradictions, etc.

        Returns List[EvidenceGraphGap] if schema available, else List[Dict].
        Max 50 gaps total.
        """
        gaps: list = []

        node_map = {n.node_id: n for n in nodes}

        # Build connected sets
        connected: Set[str] = set()
        for e in edges:
            connected.add(e.source_node_id)
            connected.add(e.target_node_id)

        def _make_gap(gap_id, gap_type, title, description, affected_node_ids,
                      affected_edge_ids, severity, suggested_next_step, source_module=""):
            if _THREAD_SCHEMA_AVAILABLE:
                try:
                    return EvidenceGraphGap(
                        gap_id=gap_id,
                        gap_type=gap_type,
                        title=title,
                        description=description,
                        affected_node_ids=list(affected_node_ids),
                        affected_edge_ids=list(affected_edge_ids),
                        severity=severity,
                        suggested_next_step=suggested_next_step,
                        source_module=source_module,
                        no_real_orders=True,
                        production_blocked=True,
                    )
                except Exception as exc:
                    logger.warning("[EvidenceGraphBuilder] EvidenceGraphGap creation failed: %s", exc)
            # Fallback dict
            return {
                "gap_id": gap_id,
                "gap_type": gap_type,
                "title": title,
                "description": description,
                "affected_node_ids": affected_node_ids,
                "affected_edge_ids": affected_edge_ids,
                "severity": severity,
                "suggested_next_step": suggested_next_step,
                "source_module": source_module,
                "no_real_orders": True,
                "production_blocked": True,
            }

        gap_idx = 0

        # Gap 1: ORPHAN_NODE — nodes with no edges
        orphan_nodes = [n for n in nodes if n.node_id not in connected]
        if orphan_nodes:
            severity = "HIGH" if len(orphan_nodes) >= 5 else "MEDIUM"
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_ORPHAN_NODE,
                title=f"Orphan nodes detected ({len(orphan_nodes)})",
                description=f"{len(orphan_nodes)} node(s) have no connecting edges",
                affected_node_ids=[n.node_id for n in orphan_nodes[:20]],
                affected_edge_ids=[],
                severity=severity,
                suggested_next_step="REVIEW",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 2: REQUIRES_DATA
        req_data_edges = [e for e in edges if e.relation_type == EDGE_REQUIRES_DATA]
        if req_data_edges:
            affected_nodes = list({e.target_node_id for e in req_data_edges})
            severity = "HIGH" if len(req_data_edges) >= 3 else "MEDIUM"
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_REQUIRES_DATA,
                title=f"Data gaps required ({len(req_data_edges)} edges)",
                description=f"{len(req_data_edges)} edge(s) require data to be sourced",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in req_data_edges[:20]],
                severity=severity,
                suggested_next_step="FIX_DATA",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 3: REQUIRES_BACKTEST
        req_bt_edges = [e for e in edges if e.relation_type == EDGE_REQUIRES_BACKTEST]
        if req_bt_edges:
            affected_nodes = list({e.target_node_id for e in req_bt_edges})
            severity = "HIGH" if len(req_bt_edges) >= 3 else "MEDIUM"
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_REQUIRES_BACKTEST,
                title=f"Backtest required ({len(req_bt_edges)} edges)",
                description=f"{len(req_bt_edges)} edge(s) require backtest validation",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in req_bt_edges[:20]],
                severity=severity,
                suggested_next_step="BACKTEST_MORE",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 4: REQUIRES_REPLAY
        req_replay_edges = [e for e in edges if e.relation_type == EDGE_REQUIRES_REPLAY]
        if req_replay_edges:
            affected_nodes = list({e.target_node_id for e in req_replay_edges})
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_REQUIRES_REPLAY,
                title=f"Replay required ({len(req_replay_edges)} edges)",
                description=f"{len(req_replay_edges)} edge(s) require replay practice",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in req_replay_edges[:20]],
                severity="MEDIUM",
                suggested_next_step="PRACTICE_REPLAY",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 5: CONTRADICTION
        contradicts_edges = [e for e in edges if e.relation_type == EDGE_CONTRADICTS]
        if contradicts_edges:
            affected_nodes = list({
                nid for e in contradicts_edges
                for nid in (e.source_node_id, e.target_node_id)
            })
            severity = "HIGH" if len(contradicts_edges) >= 2 else "MEDIUM"
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_CONTRADICTION,
                title=f"Contradictions detected ({len(contradicts_edges)} pairs)",
                description=f"{len(contradicts_edges)} contradicting edge(s) found in graph",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in contradicts_edges[:20]],
                severity=severity,
                suggested_next_step="TRACE_EVIDENCE",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 6: LOW_CONFIDENCE_EDGE
        low_conf_edges = [e for e in edges if e.confidence < 0.35]
        if low_conf_edges:
            affected_nodes = list({
                nid for e in low_conf_edges
                for nid in (e.source_node_id, e.target_node_id)
            })
            severity = "HIGH" if len(low_conf_edges) >= 5 else "LOW"
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_LOW_CONFIDENCE_EDGE,
                title=f"Low confidence edges ({len(low_conf_edges)})",
                description=f"{len(low_conf_edges)} edge(s) with confidence < 0.35",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in low_conf_edges[:20]],
                severity=severity,
                suggested_next_step="VALIDATE",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        if len(gaps) >= 50:
            return gaps[:50]

        # Gap 7: DUPLICATE_CLUSTER
        dup_edges = [e for e in edges if e.relation_type == EDGE_DUPLICATES]
        if dup_edges:
            affected_nodes = list({
                nid for e in dup_edges
                for nid in (e.source_node_id, e.target_node_id)
            })
            gaps.append(_make_gap(
                gap_id=f"GAP_{gap_idx:04d}",
                gap_type=GAP_DUPLICATE_CLUSTER,
                title=f"Duplicate node cluster ({len(dup_edges)} duplicate edges)",
                description=f"{len(dup_edges)} duplicate edge(s) suggest node consolidation",
                affected_node_ids=affected_nodes[:20],
                affected_edge_ids=[e.edge_id for e in dup_edges[:20]],
                severity="LOW",
                suggested_next_step="REVIEW",
                source_module="evidence_graph_builder",
            ))
            gap_idx += 1

        return gaps[:50]

    def build_crash_reversal_threads(self, nodes: list, edges: list) -> list:
        """Build crash reversal specific evidence threads.

        Looks for nodes with:
        - source_module containing 'crash_reversal'
        - title containing crash-related keywords
        - is_crash_reversal_node=True

        Groups them by crash_stage order:
        CRASH_CAUSE → STABILIZATION → RELATIVE_STRENGTH → EPS_DIP_FILTER
            → MA_PROFIT_DISCIPLINE → HIGH_RISK_GUARD
        """
        crash_keywords = (
            "crash", "stabilization", "relative strength", "sakata",
            "eps", "ma profit", "industry guard", "crash_reversal",
        )

        cr_nodes = [
            n for n in nodes
            if getattr(n, "is_crash_reversal_node", False)
            or "crash_reversal" in getattr(n, "source_module", "").lower()
            or any(kw in (n.title + " " + getattr(n, "summary", "")).lower() for kw in crash_keywords)
        ]

        if not cr_nodes:
            return []

        # Stage ordering
        stage_order = [
            CRASH_STAGE_CRASH_CAUSE,
            CRASH_STAGE_STABILIZATION,
            CRASH_STAGE_RELATIVE_STRENGTH,
            CRASH_STAGE_EPS_DIP_FILTER,
            CRASH_STAGE_MA_PROFIT_DISCIPLINE,
            CRASH_STAGE_HIGH_RISK_GUARD,
        ]

        # Group by crash_stage
        stage_groups: Dict[str, List] = {s: [] for s in stage_order}
        ungrouped = []
        for n in cr_nodes:
            stage = getattr(n, "crash_stage", "") or ""
            if stage in stage_groups:
                stage_groups[stage].append(n)
            else:
                ungrouped.append(n)

        # Build one thread for the full crash reversal chain
        ordered_nodes = []
        for stage in stage_order:
            ordered_nodes.extend(stage_groups[stage])
        ordered_nodes.extend(ungrouped)

        if not ordered_nodes:
            return []

        thread_node_ids = [n.node_id for n in ordered_nodes]
        thread_node_id_set = set(thread_node_ids)
        thread_edge_ids = [
            e.edge_id for e in edges
            if e.source_node_id in thread_node_id_set
            or e.target_node_id in thread_node_id_set
        ]
        source_modules = list({n.source_module for n in ordered_nodes if n.source_module})
        related_symbols = list({
            sym for n in ordered_nodes for sym in (n.related_symbols or [])
        })
        related_strategies = list({
            s for n in ordered_nodes for s in (n.related_strategies or [])
        })
        related_rules = list({
            r for n in ordered_nodes for r in (n.related_rules or [])
        })

        thread_edges = [e for e in edges if e.edge_id in set(thread_edge_ids)]
        support_count = sum(1 for e in thread_edges if e.relation_type == EDGE_SUPPORTS)
        contradiction_count = sum(1 for e in thread_edges if e.relation_type == EDGE_CONTRADICTS)
        requires_data_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_DATA)
        requires_backtest_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_BACKTEST)
        requires_replay_count = sum(1 for e in thread_edges if e.relation_type == EDGE_REQUIRES_REPLAY)

        evidence_path = [n.node_type for n in ordered_nodes]

        if _THREAD_SCHEMA_AVAILABLE:
            try:
                quality_score, quality_label, suggested_next_step = self.calculate_thread_quality(
                    thread_node_ids, thread_edge_ids, nodes, edges
                )
                thread_obj = EvidenceThread(
                    thread_id="T_CRASH_REVERSAL",
                    title="Crash Reversal Evidence Chain",
                    summary="Full crash reversal framework evidence chain across all stages",
                    node_ids=thread_node_ids,
                    edge_ids=thread_edge_ids,
                    node_count=len(thread_node_ids),
                    edge_count=len(thread_edge_ids),
                    support_count=support_count,
                    contradiction_count=contradiction_count,
                    requires_data_count=requires_data_count,
                    requires_backtest_count=requires_backtest_count,
                    requires_replay_count=requires_replay_count,
                    quality_score=quality_score,
                    quality_label=quality_label,
                    suggested_next_step=suggested_next_step,
                    evidence_path=evidence_path,
                    related_symbols=related_symbols,
                    related_strategies=related_strategies,
                    related_rules=related_rules,
                    source_modules=source_modules,
                    no_real_orders=True,
                    production_blocked=True,
                )
                return [thread_obj]
            except Exception as exc:
                logger.warning("[EvidenceGraphBuilder] crash reversal EvidenceThread failed: %s", exc)

        # Fallback dict
        return [{
            "thread_id": "T_CRASH_REVERSAL",
            "anchor_node": thread_node_ids[0] if thread_node_ids else "",
            "anchor_title": "Crash Reversal Evidence Chain",
            "title": "Crash Reversal Evidence Chain",
            "key_nodes": thread_node_ids,
            "node_titles": [n.title for n in ordered_nodes],
            "evidence_path": " -> ".join(evidence_path),
            "suggested_next_step": "REVIEW",
            "node_count": len(ordered_nodes),
            "source_modules": "|".join(source_modules),
            "no_real_orders": True,
            "production_blocked": True,
        }]

    # ------------------------------------------------------------------
    # Linkers
    # ------------------------------------------------------------------

    def link_by_symbol(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO: same symbol across different modules."""
        edges: List[EvidenceEdge] = []
        sym_map: Dict[str, List[EvidenceNode]] = {}
        for n in nodes:
            for sym in n.related_symbols:
                sym_map.setdefault(sym, []).append(n)

        node_edge_count: Dict[str, int] = {}
        for sym, sym_nodes in sym_map.items():
            if len(sym_nodes) < 2:
                continue
            for i, a in enumerate(sym_nodes):
                for b in sym_nodes[i + 1:]:
                    if a.source_module == b.source_module:
                        continue
                    if node_edge_count.get(a.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    if node_edge_count.get(b.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    e = self._make_edge(a.node_id, b.node_id, EDGE_RELATED_TO,
                                        confidence=0.4,
                                        description=f"Both reference symbol {sym}",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
                        node_edge_count[a.node_id] = node_edge_count.get(a.node_id, 0) + 1
                        node_edge_count[b.node_id] = node_edge_count.get(b.node_id, 0) + 1
        return edges

    def link_by_strategy(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO: same strategy name across modules."""
        edges: List[EvidenceEdge] = []
        strat_map: Dict[str, List[EvidenceNode]] = {}
        for n in nodes:
            for s in n.related_strategies:
                strat_map.setdefault(s, []).append(n)

        node_edge_count: Dict[str, int] = {}
        for strat, snodes in strat_map.items():
            if len(snodes) < 2:
                continue
            for i, a in enumerate(snodes):
                for b in snodes[i + 1:]:
                    if a.source_module == b.source_module:
                        continue
                    if node_edge_count.get(a.node_id, 0) >= MAX_EDGES_PER_NODE:
                        continue
                    e = self._make_edge(a.node_id, b.node_id, EDGE_RELATED_TO,
                                        confidence=0.4,
                                        description=f"Both reference strategy {strat}",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
                        node_edge_count[a.node_id] = node_edge_count.get(a.node_id, 0) + 1
        return edges

    def link_by_rule(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """RELATED_TO / REFINES: rule candidates linked to recommendations."""
        edges: List[EvidenceEdge] = []
        rec_nodes  = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        rule_nodes = [n for n in nodes if n.node_type == NODE_RULE_CANDIDATE]

        node_edge_count: Dict[str, int] = {}
        for rule in rule_nodes:
            for rec in rec_nodes[:5]:
                if node_edge_count.get(rule.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                # Simple heuristic: title word overlap
                if self._title_overlap(rule.title, rec.title) >= 2:
                    e = self._make_edge(rec.node_id, rule.node_id, EDGE_REFINES,
                                        confidence=0.5,
                                        description="Research recommendation may refine rule candidate",
                                        suggested_next_step="VALIDATE")
                    if e:
                        edges.append(e)
                        node_edge_count[rule.node_id] = node_edge_count.get(rule.node_id, 0) + 1
        return edges

    def link_by_memory(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """GENERATED_FROM / SUPPORTS: recommendation → strategy memory."""
        edges: List[EvidenceEdge] = []
        rec_nodes = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        mem_nodes = [n for n in nodes if n.node_type in (
            NODE_STRATEGY_MEMORY, NODE_STRATEGY_HYPOTHESIS)]

        node_edge_count: Dict[str, int] = {}
        for rec in rec_nodes:
            for mem in mem_nodes:
                if node_edge_count.get(rec.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                sym_overlap = set(rec.related_symbols) & set(mem.related_symbols)
                strat_overlap = set(rec.related_strategies) & set(mem.related_strategies)
                if sym_overlap or strat_overlap or self._title_overlap(rec.title, mem.title) >= 2:
                    e = self._make_edge(rec.node_id, mem.node_id, EDGE_SUPPORTS,
                                        confidence=0.55,
                                        description="Recommendation supports strategy memory",
                                        suggested_next_step="TRACE_EVIDENCE")
                    if e:
                        edges.append(e)
                        node_edge_count[rec.node_id] = node_edge_count.get(rec.node_id, 0) + 1
        return edges

    def link_by_task(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """Various links: coach tasks → replay/metric/data_gap."""
        edges: List[EvidenceEdge] = []
        task_nodes   = [n for n in nodes if n.node_type == NODE_BACKTEST_COACH_TASK]
        replay_nodes = [n for n in nodes if n.node_type == NODE_REPLAY_MISTAKE]
        metric_nodes = [n for n in nodes if n.node_type == NODE_TRAINING_METRIC]
        data_gaps    = [n for n in nodes if n.node_type == NODE_DATA_GAP]
        hypotheses   = [n for n in nodes if n.node_type == NODE_STRATEGY_HYPOTHESIS]

        node_edge_count: Dict[str, int] = {}

        # coach task → replay mistake: REQUIRES_REPLAY
        for task in task_nodes:
            for replay in replay_nodes[:3]:
                if node_edge_count.get(task.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                e = self._make_edge(task.node_id, replay.node_id, EDGE_REQUIRES_REPLAY,
                                    confidence=0.5,
                                    description="Coach task requires replay practice",
                                    suggested_next_step="PRACTICE_REPLAY")
                if e:
                    edges.append(e)
                    node_edge_count[task.node_id] = node_edge_count.get(task.node_id, 0) + 1

        # metric improving → coach task: VALIDATED_BY
        for metric in metric_nodes:
            if "IMPROVING" in metric.status.upper() or "IMPROVING" in metric.summary.upper():
                for task in task_nodes[:3]:
                    if node_edge_count.get(metric.node_id, 0) >= MAX_EDGES_PER_NODE:
                        break
                    e = self._make_edge(metric.node_id, task.node_id, EDGE_VALIDATED_BY,
                                        confidence=0.55,
                                        description="Improving metric validates coach task progress",
                                        suggested_next_step="VALIDATE")
                    if e:
                        edges.append(e)
                        node_edge_count[metric.node_id] = node_edge_count.get(metric.node_id, 0) + 1

        # data gap → REQUIRES_DATA for hypotheses
        for gap in data_gaps:
            for hyp in hypotheses[:3]:
                if node_edge_count.get(hyp.node_id, 0) >= MAX_EDGES_PER_NODE:
                    break
                e = self._make_edge(hyp.node_id, gap.node_id, EDGE_REQUIRES_DATA,
                                    confidence=0.65,
                                    description="Strategy hypothesis requires data gap to be fixed",
                                    suggested_next_step="FIX_DATA")
                if e:
                    edges.append(e)
                    node_edge_count[hyp.node_id] = node_edge_count.get(hyp.node_id, 0) + 1

        # hypothesis without backtest → REQUIRES_BACKTEST
        for hyp in hypotheses:
            if node_edge_count.get(hyp.node_id, 0) < MAX_EDGES_PER_NODE:
                e = self._make_edge(hyp.node_id, hyp.node_id + "_BT_NEEDED",
                                    EDGE_REQUIRES_BACKTEST,
                                    confidence=0.7,
                                    description="Strategy hypothesis requires backtest validation",
                                    suggested_next_step="BACKTEST_MORE")
                # self-loops not needed; instead mark in summary — skip
                pass

        return edges

    def detect_duplicates(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """DUPLICATES: nodes with highly similar titles from different sources."""
        edges: List[EvidenceEdge] = []
        seen_titles: Dict[str, EvidenceNode] = {}

        for node in nodes:
            key = self._normalize_title(node.title)
            if key in seen_titles:
                other = seen_titles[key]
                if other.source_module != node.source_module:
                    e = self._make_edge(node.node_id, other.node_id, EDGE_DUPLICATES,
                                        confidence=0.75,
                                        description="Near-identical title across different modules",
                                        suggested_next_step="REVIEW")
                    if e:
                        edges.append(e)
            else:
                seen_titles[key] = node
        return edges

    def detect_contradictions(self, nodes: List[EvidenceNode]) -> List[EvidenceEdge]:
        """CONTRADICTS: conservative detection only on high-confidence opposing evidence.

        Only fires when title word overlap is high AND sentiment indicators differ.
        Very conservative — prefer false negatives over false positives.
        """
        edges: List[EvidenceEdge] = []
        # Only compare recommendations vs memories for contradictions
        rec_nodes = [n for n in nodes if n.node_type == NODE_RESEARCH_RECOMMENDATION]
        mem_nodes = [n for n in nodes if n.node_type in (
            NODE_STRATEGY_MEMORY, NODE_STRATEGY_HYPOTHESIS)]

        pos_words = frozenset(["bullish", "uptrend", "strong", "positive", "increase", "growth"])
        neg_words = frozenset(["bearish", "downtrend", "weak", "negative", "decrease", "decline"])

        for rec in rec_nodes[:10]:
            rec_lower = (rec.title + " " + rec.summary).lower()
            rec_pos = any(w in rec_lower for w in pos_words)
            rec_neg = any(w in rec_lower for w in neg_words)
            if not rec_pos and not rec_neg:
                continue
            for mem in mem_nodes[:10]:
                if self._title_overlap(rec.title, mem.title) < 3:
                    continue
                mem_lower = (mem.title + " " + mem.summary).lower()
                mem_pos = any(w in mem_lower for w in pos_words)
                mem_neg = any(w in mem_lower for w in neg_words)
                is_contradicting = (rec_pos and mem_neg) or (rec_neg and mem_pos)
                if is_contradicting and min(rec.confidence, mem.confidence) >= 0.6:
                    e = self._make_edge(rec.node_id, mem.node_id, EDGE_CONTRADICTS,
                                        confidence=0.6,
                                        description="Opposing sentiment on overlapping topic",
                                        suggested_next_step="REVIEW_JOURNAL")
                    if e:
                        edges.append(e)
        return edges

    # v0.9.0.1 crash reversal
    def _link_crash_reversal_nodes(self, nodes: list) -> list:
        """Create edges between crash reversal framework nodes."""
        edges = []
        cr_nodes = [
            n for n in nodes
            if any(kw in (n.node_id + " " + n.title).lower()
                   for kw in ("crash_reversal", "crash_cause", "stabilization",
                               "relative strength after crash", "eps-backed dip",
                               "industry guard", "ma profit"))
        ]
        if len(cr_nodes) < 2:
            return edges
        # Map node_id to node for lookup
        node_map = {n.node_id: n for n in cr_nodes}
        crash_cause  = node_map.get("CR_CRASH_CAUSE")
        stab_signal  = node_map.get("CR_STAB_SIGNAL")
        rel_strength = node_map.get("CR_REL_STRENGTH")
        eps_filter   = node_map.get("CR_EPS_DIP_FILTER")
        ind_guard    = node_map.get("CR_INDUSTRY_GUARD")
        ma_disc      = node_map.get("CR_MA_DISCIPLINE")
        # crash cause SUPPORTS stabilization decision
        if crash_cause and stab_signal:
            e = self._make_edge(crash_cause.node_id, stab_signal.node_id, EDGE_SUPPORTS,
                                confidence=0.7,
                                description="Crash cause classification supports stabilization decision",
                                suggested_next_step="REVIEW")
            if e:
                edges.append(e)
        # relative strength SUPPORTS watchlist candidate
        if rel_strength and eps_filter:
            e = self._make_edge(rel_strength.node_id, eps_filter.node_id, EDGE_SUPPORTS,
                                confidence=0.65,
                                description="Relative strength after crash supports EPS-backed filter eligibility",
                                suggested_next_step="VALIDATE")
            if e:
                edges.append(e)
        # EPS support SUPPORTS dip eligibility
        if eps_filter and stab_signal:
            e = self._make_edge(eps_filter.node_id, stab_signal.node_id, EDGE_SUPPORTS,
                                confidence=0.65,
                                description="EPS-backed filter supports post-crash stabilization signal",
                                suggested_next_step="VALIDATE")
            if e:
                edges.append(e)
        # industry risk guard WEAKENED_BY aggressive position
        if ind_guard and rel_strength:
            e = self._make_edge(ind_guard.node_id, rel_strength.node_id, EDGE_WEAKENED_BY,
                                confidence=0.6,
                                description="Industry risk guard weakened by aggressive positioning in high-risk sector",
                                suggested_next_step="REVIEW")
            if e:
                edges.append(e)
        # MA profit discipline REFINES exit logic
        if ma_disc and eps_filter:
            e = self._make_edge(ma_disc.node_id, eps_filter.node_id, EDGE_REFINES,
                                confidence=0.65,
                                description="MA profit discipline refines exit logic for EPS-backed entry filter",
                                suggested_next_step="VALIDATE")
            if e:
                edges.append(e)
        return edges

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_edge(
        self,
        src: str, tgt: str, rel: str,
        confidence: float = 0.5,
        description: str = "",
        evidence: str = "",
        suggested_next_step: str = "",
    ) -> EvidenceEdge | None:
        """Create edge only if not already seen."""
        if src == tgt:
            return None
        eid = _edge_id(src, tgt, rel)
        if eid in self._edge_set:
            return None
        self._edge_set.add(eid)
        return EvidenceEdge(
            edge_id=eid,
            source_node_id=src,
            target_node_id=tgt,
            relation_type=rel,
            confidence=confidence,
            description=description,
            evidence=evidence,
            suggested_next_step=suggested_next_step,
        )

    def _bfs(
        self,
        start: str,
        adj: Dict[str, List[str]],
        max_depth: int,
        node_map: Dict[str, EvidenceNode],
    ) -> List[EvidenceNode]:
        visited: List[EvidenceNode] = []
        queue = [(start, 0)]
        seen: Set[str] = set()
        while queue:
            nid, depth = queue.pop(0)
            if nid in seen or depth > max_depth:
                continue
            seen.add(nid)
            if nid in node_map:
                visited.append(node_map[nid])
            for child in adj.get(nid, []):
                if child not in seen:
                    queue.append((child, depth + 1))
        return visited

    @staticmethod
    def _normalize_title(title: str) -> str:
        import re
        return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', title.lower())).strip()

    @staticmethod
    def _title_overlap(a: str, b: str) -> int:
        """Count common significant words between two titles."""
        stop = {"the", "a", "an", "is", "in", "of", "and", "or", "to", "for",
                "with", "on", "at", "by", "from", "that", "this"}
        wa = set(a.lower().split()) - stop
        wb = set(b.lower().split()) - stop
        return len(wa & wb)
