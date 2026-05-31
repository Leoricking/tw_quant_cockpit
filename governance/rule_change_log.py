"""
governance/rule_change_log.py — Rule change log (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.
Note: Runtime change logs go to data/backtest_results or logs/governance — not committed.

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


class RuleChangeLog:
    """
    Append-only JSONL log of rule status and metadata changes.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, path: str = None):
        # Default: logs/governance/rule_change_log.jsonl (not committed)
        if path is None:
            path = os.path.join(
                _BASE_DIR, "logs", "governance", "rule_change_log.jsonl"
            )
        self._path = path

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append_change(
        self,
        rule_id: str,
        change_type: str,
        reason: str,
        before=None,
        after=None,
    ) -> None:
        """
        Append one JSON-line entry to the change log.
        Creates parent directories if necessary.
        On any error, logs a warning and continues — never crashes.
        """
        try:
            parent = os.path.dirname(self._path)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent, exist_ok=True)

            entry = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "rule_id": rule_id,
                "change_type": change_type,
                "reason": reason,
                "before": before,
                "after": after,
            }
            line = json.dumps(entry, ensure_ascii=False)
            with open(self._path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception as exc:
            _LOG.warning("RuleChangeLog.append_change failed: %s", exc)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def load_changes(self, rule_id: str = None, limit: int = 100) -> list:
        """
        Load change log entries.
        Optionally filter by rule_id.
        Returns last `limit` matching entries.
        On missing file, returns [].
        """
        if not os.path.isfile(self._path):
            return []

        entries = []
        try:
            with open(self._path, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except Exception:
                        pass
        except Exception as exc:
            _LOG.warning("RuleChangeLog.load_changes failed: %s", exc)
            return []

        if rule_id is not None:
            entries = [e for e in entries if e.get("rule_id") == rule_id]

        return entries[-limit:]

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summarize_changes(self) -> dict:
        """
        Summarize change log by change_type.
        Returns: {change_type: count, ..., "total": int, "rules_changed": list}
        """
        entries = self.load_changes(limit=0)  # load all
        counts: dict = {}
        rules_changed = set()

        for entry in entries:
            ct = entry.get("change_type", "unknown")
            counts[ct] = counts.get(ct, 0) + 1
            rid = entry.get("rule_id")
            if rid:
                rules_changed.add(rid)

        result = dict(counts)
        result["total"] = len(entries)
        result["rules_changed"] = sorted(rules_changed)
        return result
