"""
replay/strategy_replay_comparator.py — Comparator for strategy snapshots.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Before outcome reveal: NO forward returns, NO outcomes shown.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class StrategyReplayComparator:
    """
    Compares strategy snapshots across dates, sessions, or forks.
    Before outcome reveal: NO forward returns, NO outcomes shown.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def compare_snapshots(
        self, snapshot_a: Any, snapshot_b: Any
    ) -> Dict[str, Any]:
        """Compare two strategy snapshots."""
        a = snapshot_a.to_dict() if hasattr(snapshot_a, "to_dict") else snapshot_a
        b = snapshot_b.to_dict() if hasattr(snapshot_b, "to_dict") else snapshot_b
        return {
            "snapshot_a_id": a.get("strategy_snapshot_id", ""),
            "snapshot_b_id": b.get("strategy_snapshot_id", ""),
            "date_a": a.get("replay_date", ""),
            "date_b": b.get("replay_date", ""),
            "agreement_delta": b.get("agreement_score", 0) - a.get("agreement_score", 0),
            "conflict_delta": b.get("conflict_score", 0) - a.get("conflict_score", 0),
            "module_changes": self._compare_modules(a, b),
            "research_only": True,
            "no_forward_return": True,
            "no_outcome": True,
        }

    def _compare_modules(
        self, snap_a: Dict[str, Any], snap_b: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Compare module signals between two snapshots."""
        mods_a = {m.get("module_name"): m for m in snap_a.get("modules", [])}
        mods_b = {m.get("module_name"): m for m in snap_b.get("modules", [])}
        changes = []
        all_modules = set(mods_a.keys()) | set(mods_b.keys())
        for mod_name in sorted(all_modules):
            a_mod = mods_a.get(mod_name, {})
            b_mod = mods_b.get(mod_name, {})
            if a_mod.get("signal") != b_mod.get("signal"):
                changes.append({
                    "module_name": mod_name,
                    "signal_a": a_mod.get("signal", ""),
                    "signal_b": b_mod.get("signal", ""),
                    "score_a": a_mod.get("score"),
                    "score_b": b_mod.get("score"),
                })
        return changes

    def compare_dates(
        self,
        session_id: str,
        date_a: str,
        date_b: str,
    ) -> Dict[str, Any]:
        """Compare two dates within a session (requires store queries)."""
        return {
            "session_id": session_id,
            "date_a": date_a,
            "date_b": date_b,
            "note": "Requires store queries for full comparison.",
            "research_only": True,
        }

    def compare_sessions(
        self,
        session_id_a: str,
        session_id_b: str,
        replay_date: str,
    ) -> Dict[str, Any]:
        """Compare two sessions at same replay date."""
        return {
            "session_id_a": session_id_a,
            "session_id_b": session_id_b,
            "replay_date": replay_date,
            "note": "Requires store queries for full comparison.",
            "research_only": True,
        }

    def compare_forks(
        self,
        parent_session_id: str,
        fork_session_id: str,
    ) -> Dict[str, Any]:
        """Compare parent and fork sessions."""
        return {
            "parent_session_id": parent_session_id,
            "fork_session_id": fork_session_id,
            "note": "Requires store queries for full comparison.",
            "research_only": True,
        }

    def compare_modules(
        self,
        snapshot_a: Any,
        snapshot_b: Any,
        module_name: str,
    ) -> Dict[str, Any]:
        """Compare a specific module between two snapshots."""
        a = snapshot_a.to_dict() if hasattr(snapshot_a, "to_dict") else snapshot_a
        b = snapshot_b.to_dict() if hasattr(snapshot_b, "to_dict") else snapshot_b
        mods_a = {m.get("module_name"): m for m in a.get("modules", [])}
        mods_b = {m.get("module_name"): m for m in b.get("modules", [])}
        return {
            "module_name": module_name,
            "snapshot_a": mods_a.get(module_name, {}),
            "snapshot_b": mods_b.get(module_name, {}),
            "research_only": True,
        }

    def summarize(self, comparison_result: Dict[str, Any]) -> str:
        """Return summary string."""
        changes = comparison_result.get("module_changes", [])
        return (
            f"Comparison: {comparison_result.get('date_a')} vs "
            f"{comparison_result.get('date_b')}, "
            f"{len(changes)} module signal changes."
        )

    def render_markdown(self, comparison_result: Dict[str, Any]) -> str:
        """Render comparison as markdown."""
        lines = [
            "## Strategy Snapshot Comparison",
            f"**Date A:** {comparison_result.get('date_a', '')}",
            f"**Date B:** {comparison_result.get('date_b', '')}",
            f"**Agreement Delta:** {comparison_result.get('agreement_delta', 0):.3f}",
            f"**Conflict Delta:** {comparison_result.get('conflict_delta', 0):.3f}",
            "",
            "### Module Changes",
        ]
        changes = comparison_result.get("module_changes", [])
        if not changes:
            lines.append("No signal changes.")
        for ch in changes:
            lines.append(
                f"- **{ch['module_name']}**: "
                f"`{ch.get('signal_a', '')}` → `{ch.get('signal_b', '')}`"
            )
        lines.append("")
        lines.append("*Research Only. No Real Orders. Not Investment Advice.*")
        return "\n".join(lines)
