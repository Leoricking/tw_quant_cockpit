"""
paper_trading/multi_session/deadlock_detector_v166.py — Deadlock Detector v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No auto-kill. Mark BLOCKED and recommend release only.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_KILL_SESSION = True


class DeadlockDetector:
    """
    Wait-for graph cycle detection.
    Actions: mark BLOCKED, recommend release, simulate rollback.
    No auto-kill.
    """

    def detect_cycles(self, wait_for_graph: Dict[str, List[str]]) -> List[List[str]]:
        cycles: List[List[str]] = []
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in wait_for_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path + [neighbor])
                elif neighbor in rec_stack:
                    # Found cycle — extract it
                    idx = path.index(neighbor) if neighbor in path else 0
                    cycle = path[idx:] + [neighbor]
                    if cycle not in cycles:
                        cycles.append(cycle)
            rec_stack.discard(node)

        for node in wait_for_graph:
            if node not in visited:
                dfs(node, [node])
        return cycles

    def detect_self_cycle(self, session_id: str, wait_for_graph: Dict[str, List[str]]) -> bool:
        return session_id in wait_for_graph.get(session_id, [])

    def is_deadlocked(self, wait_for_graph: Dict[str, List[str]]) -> bool:
        return len(self.detect_cycles(wait_for_graph)) > 0

    def select_victim(
        self,
        cycle: List[str],
        priority_map: Dict[str, int],
        seed: int = 0,
    ) -> str:
        # Deterministic: lowest priority, then alphabetical
        return min(cycle, key=lambda s: (priority_map.get(s, 0), s))

    def recommend_resolution(
        self,
        cycle: List[str],
        priority_map: Dict[str, int],
        seed: int = 0,
    ) -> Dict[str, Any]:
        victim = self.select_victim(cycle, priority_map, seed)
        return {
            "action": "mark_blocked_recommend_release",
            "victim": victim,
            "cycle": cycle,
            "rollback_suggestion": [victim],
            "auto_kill": False,
        }
