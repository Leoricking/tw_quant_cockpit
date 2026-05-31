"""
governance/rule_snapshot.py — Rule snapshot builder (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.
Output: data/backtest_results/rule_governance_snapshot_YYYY-MM-DD.json (not committed)
        data/backtest_results/rule_governance_summary_YYYY-MM-DD.csv (not committed)

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
import json
import logging
import datetime

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG = logging.getLogger(__name__)


class RuleSnapshotBuilder:
    """
    Builds and writes a point-in-time snapshot of all registered rules.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, registry=None, output_dir: str = None):
        self._registry = registry
        if output_dir is None:
            output_dir = os.path.join(_BASE_DIR, "data", "backtest_results")
        self._output_dir = output_dir

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build_snapshot(self) -> dict:
        """
        Collect all rule metadata and build a snapshot dict.

        Returns dict with:
          snapshot_date, total_rules, rules (list of dicts),
          summary, read_only, no_real_orders, production_blocked
        """
        today = datetime.date.today().isoformat()
        snapshot = {
            "snapshot_date": today,
            "total_rules": 0,
            "rules": [],
            "summary": {},
            "read_only": True,
            "no_real_orders": True,
            "production_blocked": True,
        }

        if self._registry is None:
            return snapshot

        try:
            rules = self._registry.list_rules()
            snapshot["total_rules"] = len(rules)
            snapshot["rules"] = [r.to_dict() for r in rules]
            snapshot["summary"] = self._registry.build_rule_summary()
        except Exception as exc:
            _LOG.warning("RuleSnapshotBuilder.build_snapshot error: %s", exc)

        return snapshot

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write_snapshot(self) -> dict:
        """
        Build and write snapshot JSON + summary CSV.
        Returns: {snapshot_path, summary_path} or {"error": str}
        """
        try:
            snapshot = self.build_snapshot()
            today = snapshot["snapshot_date"]

            os.makedirs(self._output_dir, exist_ok=True)

            # --- JSON snapshot ---
            json_filename = f"rule_governance_snapshot_{today}.json"
            json_path = os.path.join(self._output_dir, json_filename)
            with open(json_path, "w", encoding="utf-8") as fh:
                json.dump(snapshot, fh, indent=2, ensure_ascii=False)

            # --- CSV summary ---
            csv_filename = f"rule_governance_summary_{today}.csv"
            csv_path = os.path.join(self._output_dir, csv_filename)
            self._write_csv(snapshot["rules"], csv_path)

            return {"snapshot_path": json_path, "summary_path": csv_path}

        except Exception as exc:
            _LOG.warning("RuleSnapshotBuilder.write_snapshot error: %s", exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _write_csv(rules: list, path: str) -> None:
        """Write rules list as a CSV file."""
        if not rules:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("rule_id,rule_name,category,status,enabled,"
                         "experimental,confidence_level,sample_count,"
                         "timeframe,version\n")
            return

        columns = [
            "rule_id", "rule_name", "category", "status", "enabled",
            "experimental", "confidence_level", "sample_count",
            "timeframe", "version",
        ]

        def _escape(val) -> str:
            s = str(val) if val is not None else ""
            if "," in s or '"' in s or "\n" in s:
                s = '"' + s.replace('"', '""') + '"'
            return s

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(",".join(columns) + "\n")
            for rule in rules:
                row = [_escape(rule.get(col, "")) for col in columns]
                fh.write(",".join(row) + "\n")
