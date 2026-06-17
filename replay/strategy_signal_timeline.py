"""
replay/strategy_signal_timeline.py — Signal timeline tracker for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Timeline only shows data up to the current replay date.
[!] No future data. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class StrategySignalTimeline:
    """
    Tracks how strategy signals change over the replay session timeline.
    Stores snapshots and detects signal/warning/score/availability changes.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._session_snapshots: Dict[str, List[dict]] = {}

    def build_for_session(self, session_id: str) -> Dict[str, Any]:
        """Build full timeline summary for a session."""
        snapshots = self._session_snapshots.get(session_id, [])
        return {
            "session_id": session_id,
            "snapshot_count": len(snapshots),
            "snapshots": snapshots,
            "research_only": True,
            "no_real_orders": True,
        }

    def build_for_module(
        self, session_id: str, module_name: str
    ) -> List[Dict[str, Any]]:
        """Build timeline for a specific module in a session."""
        snapshots = self._session_snapshots.get(session_id, [])
        records = []
        for snap in snapshots:
            for mod in snap.get("modules", []):
                if mod.get("module_name") == module_name:
                    records.append({
                        "replay_date": snap.get("replay_date", ""),
                        "module_name": module_name,
                        "signal": mod.get("signal", ""),
                        "score": mod.get("score"),
                        "warning": mod.get("warning", ""),
                        "available": mod.get("available", False),
                    })
        return records

    def append_snapshot(self, snapshot) -> List[Dict[str, Any]]:
        """
        Add snapshot to timeline, detect changes from previous.
        Returns list of detected changes.
        """
        snap_dict = snapshot.to_dict() if hasattr(snapshot, "to_dict") else snapshot
        session_id = snap_dict.get("session_id", "")
        if session_id not in self._session_snapshots:
            self._session_snapshots[session_id] = []

        changes = []
        prev_snaps = self._session_snapshots[session_id]
        if prev_snaps:
            prev = prev_snaps[-1]
            changes.extend(self.detect_signal_changes(prev, snap_dict))
            changes.extend(self.detect_warning_changes(prev, snap_dict))
            changes.extend(self.detect_score_changes(prev, snap_dict))
            changes.extend(self.detect_availability_changes(prev, snap_dict))

        self._session_snapshots[session_id].append(snap_dict)
        return changes

    def get_date(
        self, session_id: str, replay_date: str
    ) -> Optional[Dict[str, Any]]:
        """Get snapshot for a specific date."""
        for snap in self._session_snapshots.get(session_id, []):
            if snap.get("replay_date") == replay_date:
                return snap
        return None

    def get_range(
        self, session_id: str, start: str, end: str
    ) -> List[Dict[str, Any]]:
        """Get snapshots in date range [start, end]."""
        return [
            snap for snap in self._session_snapshots.get(session_id, [])
            if start <= snap.get("replay_date", "") <= end
        ]

    def detect_signal_changes(
        self, prev_snapshot: Dict[str, Any], curr_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect signal changes between two snapshots."""
        changes = []
        prev_modules = {m.get("module_name"): m for m in prev_snapshot.get("modules", [])}
        curr_modules = {m.get("module_name"): m for m in curr_snapshot.get("modules", [])}
        for module_name, curr_mod in curr_modules.items():
            prev_mod = prev_modules.get(module_name, {})
            if prev_mod.get("signal") != curr_mod.get("signal"):
                changes.append({
                    "change_type": "SIGNAL_CHANGE",
                    "module_name": module_name,
                    "replay_date": curr_snapshot.get("replay_date", ""),
                    "from": prev_mod.get("signal", ""),
                    "to": curr_mod.get("signal", ""),
                })
        return changes

    def detect_warning_changes(
        self, prev_snapshot: Dict[str, Any], curr_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect warning changes between two snapshots."""
        changes = []
        prev_modules = {m.get("module_name"): m for m in prev_snapshot.get("modules", [])}
        curr_modules = {m.get("module_name"): m for m in curr_snapshot.get("modules", [])}
        for module_name, curr_mod in curr_modules.items():
            prev_mod = prev_modules.get(module_name, {})
            if prev_mod.get("warning") != curr_mod.get("warning"):
                changes.append({
                    "change_type": "WARNING_CHANGE",
                    "module_name": module_name,
                    "replay_date": curr_snapshot.get("replay_date", ""),
                    "from": prev_mod.get("warning", ""),
                    "to": curr_mod.get("warning", ""),
                })
        return changes

    def detect_score_changes(
        self, prev_snapshot: Dict[str, Any], curr_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect score changes between two snapshots."""
        changes = []
        prev_modules = {m.get("module_name"): m for m in prev_snapshot.get("modules", [])}
        curr_modules = {m.get("module_name"): m for m in curr_snapshot.get("modules", [])}
        for module_name, curr_mod in curr_modules.items():
            prev_mod = prev_modules.get(module_name, {})
            prev_score = prev_mod.get("score")
            curr_score = curr_mod.get("score")
            if prev_score != curr_score and (prev_score is not None or curr_score is not None):
                changes.append({
                    "change_type": "SCORE_CHANGE",
                    "module_name": module_name,
                    "replay_date": curr_snapshot.get("replay_date", ""),
                    "from": prev_score,
                    "to": curr_score,
                })
        return changes

    def detect_availability_changes(
        self, prev_snapshot: Dict[str, Any], curr_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect availability changes between two snapshots."""
        changes = []
        prev_modules = {m.get("module_name"): m for m in prev_snapshot.get("modules", [])}
        curr_modules = {m.get("module_name"): m for m in curr_snapshot.get("modules", [])}
        for module_name, curr_mod in curr_modules.items():
            prev_mod = prev_modules.get(module_name, {})
            if prev_mod.get("available") != curr_mod.get("available"):
                changes.append({
                    "change_type": "AVAILABILITY_CHANGE",
                    "module_name": module_name,
                    "replay_date": curr_snapshot.get("replay_date", ""),
                    "from": prev_mod.get("available"),
                    "to": curr_mod.get("available"),
                })
        return changes

    def summary(self, session_id: str) -> Dict[str, Any]:
        """Build summary statistics for a session timeline."""
        snapshots = self._session_snapshots.get(session_id, [])
        total_changes = 0
        module_change_counts: Dict[str, int] = {}

        for i in range(1, len(snapshots)):
            changes = (
                self.detect_signal_changes(snapshots[i - 1], snapshots[i])
                + self.detect_warning_changes(snapshots[i - 1], snapshots[i])
                + self.detect_availability_changes(snapshots[i - 1], snapshots[i])
            )
            total_changes += len(changes)
            for ch in changes:
                mod = ch.get("module_name", "")
                module_change_counts[mod] = module_change_counts.get(mod, 0) + 1

        return {
            "session_id": session_id,
            "snapshot_count": len(snapshots),
            "total_changes": total_changes,
            "module_change_counts": module_change_counts,
            "research_only": True,
        }
