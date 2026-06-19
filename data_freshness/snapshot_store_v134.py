"""data_freshness/snapshot_store_v134.py — v1.3.4 Freshness Snapshot Store.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime path: data/freshness/ (gitignored).
[!] Tests use tmp_path.
[!] Not Investment Advice.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import (
    FreshnessRecord, ProviderSLARecord, FreshnessAlert, DailyFreshnessSummary,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

SCHEMA_VERSION = "1.3.4"

# Default runtime path (gitignored)
_DEFAULT_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "freshness",
)


class FreshnessSnapshotStore:
    """Persist freshness snapshots, SLA history, alerts, and daily summaries.

    [!] Research Only. Runtime files are gitignored.
    [!] Tests should pass tmp_path to base_dir.
    """

    def __init__(self, base_dir: Optional[str] = None) -> None:
        self._base_dir = base_dir or _DEFAULT_BASE
        os.makedirs(self._base_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._base_dir, filename)

    def _write_json(self, path: str, data: Any) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _read_json(self, path: str) -> Any:
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_snapshot(self, records: List[FreshnessRecord]) -> None:
        """Save current freshness snapshot."""
        data = {
            "schema_version": SCHEMA_VERSION,
            "records": [r.to_dict() for r in records],
        }
        self._write_json(self._path("snapshot_latest.json"), data)
        logger.debug("Saved freshness snapshot with %d records", len(records))

    def load_latest_snapshot(self) -> List[FreshnessRecord]:
        """Load the latest freshness snapshot."""
        data = self._read_json(self._path("snapshot_latest.json"))
        if data is None:
            return []
        try:
            return [FreshnessRecord.from_dict(r) for r in data.get("records", [])]
        except Exception as exc:
            logger.warning("load_latest_snapshot: error: %s", exc)
            return []

    def save_sla_history(self, records: List[ProviderSLARecord]) -> None:
        """Save SLA history records."""
        data = {
            "schema_version": SCHEMA_VERSION,
            "records": [r.to_dict() for r in records],
        }
        self._write_json(self._path("sla_history.json"), data)

    def load_sla_history(self) -> List[ProviderSLARecord]:
        """Load SLA history records."""
        data = self._read_json(self._path("sla_history.json"))
        if data is None:
            return []
        try:
            return [ProviderSLARecord.from_dict(r) for r in data.get("records", [])]
        except Exception as exc:
            logger.warning("load_sla_history: error: %s", exc)
            return []

    def save_alerts(self, alerts: List[FreshnessAlert]) -> None:
        """Save alert list."""
        data = {
            "schema_version": SCHEMA_VERSION,
            "alerts": [a.to_dict() for a in alerts],
        }
        self._write_json(self._path("alerts.json"), data)

    def load_alerts(self) -> List[FreshnessAlert]:
        """Load alert list."""
        data = self._read_json(self._path("alerts.json"))
        if data is None:
            return []
        try:
            return [FreshnessAlert.from_dict(a) for a in data.get("alerts", [])]
        except Exception as exc:
            logger.warning("load_alerts: error: %s", exc)
            return []

    def save_daily_summary(self, summary: DailyFreshnessSummary) -> None:
        """Save daily freshness summary."""
        data = {
            "schema_version": SCHEMA_VERSION,
            "summary": summary.to_dict(),
        }
        self._write_json(self._path("daily_summary.json"), data)

    def load_daily_summary(self) -> Optional[DailyFreshnessSummary]:
        """Load daily freshness summary."""
        data = self._read_json(self._path("daily_summary.json"))
        if data is None:
            return None
        try:
            sd = data.get("summary", {})
            known = {f.name for f in __import__("dataclasses").fields(DailyFreshnessSummary)}
            return DailyFreshnessSummary(**{k: v for k, v in sd.items() if k in known})
        except Exception as exc:
            logger.warning("load_daily_summary: error: %s", exc)
            return None
