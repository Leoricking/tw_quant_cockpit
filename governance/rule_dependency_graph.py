"""
governance/rule_dependency_graph.py — Rule dependency graph (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RuleDependencyGraph:
    """
    Builds and queries a directed dependency graph over registered rules.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, registry=None):
        self._registry = registry
        # rule_id -> list of dependency rule_ids (forward edges)
        self._edges: dict = {}
        # rule_id -> list of rule_ids that depend on this rule (reverse edges)
        self._reverse_edges: dict = {}

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build_graph(self) -> None:
        """
        Build adjacency maps from registry.
        If registry is None, builds empty graph.
        """
        self._edges = {}
        self._reverse_edges = {}

        if self._registry is None:
            return

        try:
            rules = self._registry.list_rules()
        except Exception:
            return

        # Initialise all nodes
        for rule in rules:
            rid = rule.rule_id
            if rid not in self._edges:
                self._edges[rid] = []
            if rid not in self._reverse_edges:
                self._reverse_edges[rid] = []

        # Add edges
        for rule in rules:
            rid = rule.rule_id
            for dep_id in (rule.dependencies or []):
                # Forward edge: rid depends on dep_id
                if dep_id not in self._edges[rid]:
                    self._edges[rid].append(dep_id)
                # Ensure dep_id node exists
                if dep_id not in self._reverse_edges:
                    self._reverse_edges[dep_id] = []
                if dep_id not in self._edges:
                    self._edges[dep_id] = []
                # Reverse edge: dep_id is depended upon by rid
                if rid not in self._reverse_edges[dep_id]:
                    self._reverse_edges[dep_id].append(rid)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_dependencies(self, rule_id: str) -> list:
        """Return list of rule_ids that rule_id directly depends on."""
        return list(self._edges.get(rule_id, []))

    def get_dependents(self, rule_id: str) -> list:
        """Return list of rule_ids that directly depend on rule_id."""
        return list(self._reverse_edges.get(rule_id, []))

    # ------------------------------------------------------------------
    # Cycle detection (DFS)
    # ------------------------------------------------------------------

    def detect_cycles(self) -> list:
        """
        DFS-based cycle detection.
        Returns list of human-readable cycle descriptions.
        Never crashes.
        """
        cycles = []
        try:
            visited = set()
            rec_stack = set()

            def _dfs(node: str) -> bool:
                visited.add(node)
                rec_stack.add(node)
                for neighbour in self._edges.get(node, []):
                    if neighbour not in visited:
                        if _dfs(neighbour):
                            return True
                    elif neighbour in rec_stack:
                        cycles.append(f"Cycle detected involving {node}")
                        return True
                rec_stack.discard(node)
                return False

            all_nodes = set(self._edges.keys()) | set(self._reverse_edges.keys())
            for node in sorted(all_nodes):
                if node not in visited:
                    _dfs(node)
        except Exception:
            pass
        return cycles

    # ------------------------------------------------------------------
    # Topological order (DFS)
    # ------------------------------------------------------------------

    def topological_order(self) -> list:
        """
        Return rule_ids in topological order (dependencies before dependents).
        If a cycle exists, returns nodes in arbitrary order without crashing.
        """
        try:
            all_nodes = sorted(
                set(self._edges.keys()) | set(self._reverse_edges.keys())
            )
            visited = set()
            order = []

            def _visit(node: str, in_progress: set):
                if node in in_progress:
                    # cycle — skip to avoid infinite recursion
                    return
                if node in visited:
                    return
                in_progress.add(node)
                for dep in self._edges.get(node, []):
                    _visit(dep, in_progress)
                in_progress.discard(node)
                visited.add(node)
                order.append(node)

            for n in all_nodes:
                _visit(n, set())

            return order
        except Exception:
            return list(self._edges.keys())

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_edges(self) -> list:
        """Return list of {"from": rule_id, "to": dep_id} dicts."""
        result = []
        for rule_id, deps in self._edges.items():
            for dep_id in deps:
                result.append({"from": rule_id, "to": dep_id})
        return result

    def get_high_impact_rules(self, min_dependents: int = 2) -> list:
        """
        Return rule_ids with at least min_dependents dependents.
        Sorted by descending dependent count.
        """
        result = []
        for rule_id, dependents in self._reverse_edges.items():
            if len(dependents) >= min_dependents:
                result.append((rule_id, len(dependents)))
        result.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in result]
