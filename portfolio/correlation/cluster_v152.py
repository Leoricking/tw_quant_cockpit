"""
portfolio/correlation/cluster_v152.py — Correlation Cluster Builder v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional

from portfolio.correlation.enums_v152 import ClusterMethod
from portfolio.correlation.models_v152 import CorrelationCluster, CorrelationMatrixResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class CorrelationClusterBuilder:
    """
    Builds clusters of correlated symbols using threshold-graph connected components.
    Pure Python BFS — no networkx required.
    Deterministic: symbols sorted alphabetically, clusters sorted by weight descending.
    """

    RESEARCH_ONLY = True

    def build_threshold_graph(
        self,
        correlation_matrix: CorrelationMatrixResult,
        cluster_threshold: float = 0.75,
        weights: Optional[Dict[str, float]] = None,
        risk_contributions: Optional[List] = None,
    ) -> List[CorrelationCluster]:
        """
        Build clusters via BFS on the correlation graph.
        Edge between symbols i,j if abs(corr[i][j]) >= cluster_threshold.
        Isolated symbols form their own cluster of size 1.
        """
        symbols = correlation_matrix.symbols
        matrix  = correlation_matrix.matrix
        n = len(symbols)

        if n == 0:
            return []

        # Build adjacency list
        adj: Dict[str, List[str]] = {s: [] for s in symbols}
        for i in range(n):
            for j in range(i + 1, n):
                if abs(matrix[i][j]) >= cluster_threshold:
                    adj[symbols[i]].append(symbols[j])
                    adj[symbols[j]].append(symbols[i])

        # BFS to find connected components
        visited: set = set()
        components: List[List[str]] = []

        for sym in sorted(symbols):  # deterministic order
            if sym in visited:
                continue
            queue = deque([sym])
            visited.add(sym)
            component: List[str] = []
            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in sorted(adj[node]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(sorted(component))

        # Build CorrelationCluster objects
        w_map = weights or {}
        rc_map: Dict[str, float] = {}
        if risk_contributions:
            for rc in risk_contributions:
                rc_map[rc.symbol] = getattr(rc, "component_contribution", 0.0)

        sym_idx = {s: i for i, s in enumerate(symbols)}

        clusters: List[CorrelationCluster] = []
        for cid, comp in enumerate(components):
            # Portfolio weight
            portfolio_weight = sum(w_map.get(s, 0.0) for s in comp)
            risk_contrib = sum(rc_map.get(s, 0.0) for s in comp)

            # Internal correlations
            internal_corrs: List[float] = []
            for i, si in enumerate(comp):
                for j, sj in enumerate(comp):
                    if i < j:
                        ii = sym_idx[si]
                        jj = sym_idx[sj]
                        internal_corrs.append(matrix[ii][jj])

            avg_corr = sum(internal_corrs) / len(internal_corrs) if internal_corrs else 1.0
            max_corr = max(internal_corrs) if internal_corrs else 1.0

            clusters.append(CorrelationCluster(
                cluster_id=f"CLU_{cid + 1:03d}",
                symbols=comp,
                method=ClusterMethod.THRESHOLD_GRAPH,
                threshold=cluster_threshold,
                average_internal_correlation=avg_corr,
                maximum_internal_correlation=max_corr,
                portfolio_weight=portfolio_weight,
                risk_contribution=risk_contrib,
            ))

        # Sort by weight descending (deterministic by symbol list for ties)
        clusters.sort(key=lambda c: (-c.portfolio_weight, c.symbols[0]))

        return clusters
