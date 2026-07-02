"""
paper_trading/performance_attribution/attribution_store_v167.py
Deterministic in-memory/fixture-backed store for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No production DB. No external DB. No Redis/Kafka. No network. No hidden persistence.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionStatus

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

STORE_PAPER_ONLY          = True
STORE_NO_PRODUCTION_DB    = True
STORE_NO_EXTERNAL_DB      = True
STORE_NO_NETWORK          = True
STORE_NO_REAL_LEDGER_WRITE = True
STORE_NO_REDIS            = True
STORE_NO_KAFKA            = True


class AttributionStore:
    """
    In-memory attribution run store. Schema-versioned. Safe serialization.
    No production DB. No external storage. No network. No secrets.
    Runtime artifacts must NOT be committed to Git.
    """

    def __init__(self) -> None:
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._schema_version = "167"
        self._policy_version = "1.6.7-paper-attribution"

    # ── Write operations ──────────────────────────────────────────────────────

    def save_run(self, run_id: str, run_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save an attribution run. Validates safety markers."""
        if not run_id:
            return {"saved": False, "error": "missing_run_id"}
        if run_data.get("paper_only") is not True:
            return {"saved": False, "error": "BLOCKED: paper_only must be True"}
        if run_data.get("research_only") is not True:
            return {"saved": False, "error": "BLOCKED: research_only must be True"}
        # Forbidden fields check
        for field in ("broker_session", "real_account_token", "api_secret",
                      "password", "credential", "production_db_connection"):
            if field in run_data:
                return {"saved": False, "error": f"BLOCKED: forbidden field {field!r}"}

        self._runs[run_id] = {
            **run_data,
            "run_id": run_id,
            "schema_version": self._schema_version,
            "policy_version": self._policy_version,
        }
        return {"saved": True, "run_id": run_id}

    def delete_test_run(self, run_id: str) -> Dict[str, Any]:
        """Delete a test/research run (not production data)."""
        if run_id in self._runs:
            del self._runs[run_id]
            return {"deleted": True, "run_id": run_id}
        return {"deleted": False, "run_id": run_id, "error": "not_found"}

    # ── Read operations ───────────────────────────────────────────────────────

    def load_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Load an attribution run by ID."""
        return self._runs.get(run_id)

    def list_runs(self) -> List[str]:
        """List all run IDs. Deterministic sorted."""
        return sorted(self._runs.keys())

    def query_by_portfolio(self, portfolio_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if r.get("portfolio_id") == portfolio_id]

    def query_by_strategy(self, strategy_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if r.get("strategy_id") == strategy_id]

    def query_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if r.get("session_id") == session_id]

    def query_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if symbol in r.get("symbols", [])]

    def query_by_date_range(self, date_start: str, date_end: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._runs.values()
            if (r.get("period_start", "") >= date_start and
                r.get("period_end", "") <= date_end)
        ]

    def query_by_regime(self, regime: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if regime in r.get("regimes", [])]

    def query_by_status(self, status: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs.values() if r.get("status") == status]

    def summarize(self) -> Dict[str, Any]:
        """Return store summary statistics."""
        runs = list(self._runs.values())
        statuses = [r.get("status", "UNKNOWN") for r in runs]
        return {
            "total_runs": len(runs),
            "complete_runs": statuses.count(AttributionStatus.COMPLETE.value),
            "degraded_runs": statuses.count(AttributionStatus.DEGRADED.value),
            "failed_runs": statuses.count(AttributionStatus.FAILED.value),
            "run_ids": self.list_runs(),
            "schema_version": self._schema_version,
            "policy_version": self._policy_version,
            "paper_only": True,
            "research_only": True,
            "no_production_db": True,
        }

    def export_json(self, run_id: Optional[str] = None) -> str:
        """Export run(s) as JSON string."""
        if run_id:
            data = self._runs.get(run_id, {})
        else:
            data = self._runs
        return json.dumps(data, default=str, sort_keys=True, indent=2)

    def export_csv(self, run_id: Optional[str] = None) -> str:
        """Export run(s) as CSV string (flat)."""
        runs = [self._runs[run_id]] if (run_id and run_id in self._runs) else list(self._runs.values())
        if not runs:
            return "run_id,status,portfolio_id,strategy_id,period_start,period_end\n"
        header = "run_id,status,portfolio_id,strategy_id,period_start,period_end\n"
        rows = []
        for r in runs:
            row = ",".join([
                str(r.get("run_id", "")),
                str(r.get("status", "")),
                str(r.get("portfolio_id", "")),
                str(r.get("strategy_id", "")),
                str(r.get("period_start", "")),
                str(r.get("period_end", "")),
            ])
            rows.append(row)
        return header + "\n".join(rows)

    def export_markdown(self, run_id: Optional[str] = None) -> str:
        """Export run(s) as Markdown summary."""
        runs = [self._runs[run_id]] if (run_id and run_id in self._runs) else list(self._runs.values())
        if not runs:
            return "# Attribution Store\n\nNo runs found.\n"
        lines = ["# Attribution Store Summary\n"]
        lines.append(f"Total runs: {len(runs)}\n")
        lines.append("| run_id | status | portfolio | period_start | period_end |")
        lines.append("|--------|--------|-----------|--------------|------------|")
        for r in runs:
            lines.append(f"| {r.get('run_id','')} | {r.get('status','')} | "
                         f"{r.get('portfolio_id','')} | {r.get('period_start','')} | "
                         f"{r.get('period_end','')} |")
        return "\n".join(lines)
