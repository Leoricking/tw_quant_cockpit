"""
paper_trading/operational_integration/integration_store_v168.py
Integration Store (in-memory) for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import csv
import io
import json
from typing import Any, Dict, List, Optional

from .models_v168 import IntegrationRun, IntegrationSnapshot

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class IntegrationStore:
    """In-memory store for integration runs and snapshots. Research only."""

    def __init__(self) -> None:
        self._runs: Dict[str, IntegrationRun] = {}
        self._snapshots: Dict[str, IntegrationSnapshot] = {}
        self._run_data: Dict[str, Dict[str, Any]] = {}  # raw dicts too

    def save_run(self, run: IntegrationRun) -> str:
        """Save an integration run, return run_id."""
        self._runs[run.run_id] = run
        return run.run_id

    def save_run_dict(self, run_dict: Dict[str, Any]) -> str:
        """Save a run as raw dict."""
        run_id = run_dict.get("run_id", "unknown")
        self._run_data[run_id] = run_dict
        return run_id

    def load_run(self, run_id: str) -> Optional[IntegrationRun]:
        """Load a run by run_id. Returns None if not found."""
        return self._runs.get(run_id)

    def list_runs(self) -> List[str]:
        """Return all run IDs."""
        all_ids = list(set(list(self._runs.keys()) + list(self._run_data.keys())))
        return sorted(all_ids)

    def save_snapshot(self, snapshot: IntegrationSnapshot) -> str:
        """Save a snapshot, return snapshot_id."""
        self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot.snapshot_id

    def load_snapshot(self, snapshot_id: str) -> Optional[IntegrationSnapshot]:
        """Load a snapshot by ID. Returns None if not found."""
        return self._snapshots.get(snapshot_id)

    def query_by_component(self, component_id: str) -> List[str]:
        """Return run IDs that include the given component."""
        result = []
        for rid, run in self._runs.items():
            if component_id in run.components:
                result.append(rid)
        for rid, run_dict in self._run_data.items():
            comps = run_dict.get("components", [])
            if component_id in comps or run_dict.get("component_id") == component_id:
                result.append(rid)
        return list(set(result))

    def query_by_status(self, status: str) -> List[str]:
        """Return run IDs with the given status."""
        result = []
        for rid, run in self._runs.items():
            if run.status.value == status or run.status == status:
                result.append(rid)
        for rid, run_dict in self._run_data.items():
            if run_dict.get("status") == status:
                result.append(rid)
        return list(set(result))

    def query_by_session(self, session_id: str) -> List[str]:
        """Return run IDs for the given session."""
        result = []
        for rid, run in self._runs.items():
            if run.session_id == session_id:
                result.append(rid)
        for rid, run_dict in self._run_data.items():
            if run_dict.get("session_id") == session_id:
                result.append(rid)
        return list(set(result))

    def query_by_period(self, period_start: str, period_end: str) -> List[str]:
        """Return run IDs with periods overlapping the given range."""
        result = []
        for rid, run_dict in self._run_data.items():
            ps = run_dict.get("period_start", "")
            pe = run_dict.get("period_end", "")
            if ps and pe:
                if ps <= period_end and pe >= period_start:
                    result.append(rid)
        return result

    def summarize(self) -> Dict[str, Any]:
        """Return store summary."""
        total_runs = len(set(list(self._runs.keys()) + list(self._run_data.keys())))
        return {
            "total_runs": total_runs,
            "total_snapshots": len(self._snapshots),
            "paper_only": True,
            "research_only": True,
        }

    def export_json(self, run_id: str) -> str:
        """Export a run as JSON string."""
        run = self._runs.get(run_id)
        run_dict = self._run_data.get(run_id)
        if run is not None:
            data = {
                "run_id": run.run_id,
                "session_id": run.session_id,
                "status": run.status.value,
                "mode": run.mode.value,
                "started_at": run.started_at,
                "paper_only": True,
            }
        elif run_dict is not None:
            data = run_dict
        else:
            data = {"error": f"run not found: {run_id}", "paper_only": True}
        return json.dumps(data, default=str)

    def export_csv(self, run_id: str) -> str:
        """Export a run summary as CSV string."""
        buf = io.StringIO()
        writer = csv.writer(buf)
        run = self._runs.get(run_id)
        if run is not None:
            writer.writerow(["run_id", "session_id", "status", "mode", "started_at"])
            writer.writerow([run.run_id, run.session_id, run.status.value, run.mode.value, run.started_at])
        else:
            writer.writerow(["run_id", "error"])
            writer.writerow([run_id, "not found"])
        return buf.getvalue()

    def export_markdown(self, run_id: str) -> str:
        """Export a run summary as Markdown."""
        run = self._runs.get(run_id)
        if run is None:
            run_dict = self._run_data.get(run_id, {})
            return f"# Integration Run: {run_id}\n\nNot found in structured store.\n\nPaper only: True\n"
        lines = [
            f"# Integration Run: {run.run_id}",
            f"- Session: {run.session_id}",
            f"- Status: {run.status.value}",
            f"- Mode: {run.mode.value}",
            f"- Started: {run.started_at}",
            f"- Paper Only: True",
        ]
        return "\n".join(lines)
