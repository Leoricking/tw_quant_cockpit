"""
evidence_graph/__init__.py — Research Intelligence Evidence Graph package v0.8.3

[!] Research Intelligence Evidence Graph Only.
[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice.
[!] Does NOT place orders, connect broker, modify weights, or auto-trade.
[!] Does NOT auto-accept memories, modify rule governance, or enable strategies.
"""

from evidence_graph.evidence_graph_schema import (
    EvidenceNode,
    EvidenceEdge,
    EvidenceGraphSummary,
)
from evidence_graph.evidence_collector import EvidenceCollector
from evidence_graph.evidence_graph_builder import EvidenceGraphBuilder
from evidence_graph.evidence_graph_engine import EvidenceGraphEngine
from evidence_graph.evidence_graph_store import EvidenceGraphStore
from evidence_graph.evidence_graph_query import EvidenceGraphQuery

__all__ = [
    "EvidenceNode",
    "EvidenceEdge",
    "EvidenceGraphSummary",
    "EvidenceCollector",
    "EvidenceGraphBuilder",
    "EvidenceGraphEngine",
    "EvidenceGraphStore",
    "EvidenceGraphQuery",
]

read_only          = True
no_real_orders     = True
production_blocked = True
real_order_ready   = False
