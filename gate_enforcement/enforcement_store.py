"""
gate_enforcement.enforcement_store — EnforcementStore v1.1.5

Runtime storage for enforcement requests, results, and snapshots.
These files are NOT committed to git.

Runtime files:
  data/quality_gate_enforcement/run_requests.csv
  data/quality_gate_enforcement/run_results.csv
  data/quality_gate_enforcement/symbol_exclusions.csv
  data/quality_gate_enforcement/run_snapshots.jsonl
  data/quality_gate_enforcement/run_hashes.csv
  data/quality_gate_enforcement/run_outputs.csv
  data/quality_gate_enforcement/audit_summary.csv

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

from gate_enforcement.enforcement_schema import (
    GateEnforcementRequest,
    GateEnforcementResult,
    RunGateSnapshot,
    SymbolExclusionRecord,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class EnforcementStore:
    """Stores and retrieves enforcement runtime data."""

    def __init__(self, output_dir: str = "data/quality_gate_enforcement"):
        self._dir = output_dir if os.path.isabs(output_dir) else os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._dir, filename)

    # ---- Run requests ----

    def save_request(self, request: GateEnforcementRequest) -> None:
        path = self._path("run_requests.csv")
        d = request.to_dict()
        write_header = not os.path.isfile(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(d.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(d)

    def list_requests(self) -> List[dict]:
        path = self._path("run_requests.csv")
        if not os.path.isfile(path):
            return []
        try:
            with open(path, encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.warning("list_requests failed: %s", exc)
            return []

    # ---- Run results ----

    def save_result(self, result: GateEnforcementResult) -> None:
        path = self._path("run_results.csv")
        d = result.to_dict()
        write_header = not os.path.isfile(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(d.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(d)

    def list_results(self) -> List[dict]:
        path = self._path("run_results.csv")
        if not os.path.isfile(path):
            return []
        try:
            with open(path, encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception as exc:
            logger.warning("list_results failed: %s", exc)
            return []

    def get_result(self, run_id: str) -> Optional[dict]:
        for row in reversed(self.list_results()):
            if row.get("run_id") == run_id:
                return row
        return None

    # ---- Snapshots ----

    def save_snapshot(self, snapshot: RunGateSnapshot) -> None:
        path = self._path("run_snapshots.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot.to_dict(), ensure_ascii=False) + "\n")

    def get_snapshot(self, run_id: str) -> Optional[dict]:
        path = self._path("run_snapshots.jsonl")
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        if d.get("run_id") == run_id:
                            return d
                    except json.JSONDecodeError:
                        continue
        except Exception as exc:
            logger.warning("get_snapshot failed: %s", exc)
        return None

    # ---- Symbol exclusions ----

    def save_exclusion_records(self, records: List[SymbolExclusionRecord]) -> None:
        if not records:
            return
        path = self._path("symbol_exclusions.csv")
        write_header = not os.path.isfile(path)
        if records:
            sample = records[0].to_dict()
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(sample.keys()))
                if write_header:
                    writer.writeheader()
                for rec in records:
                    writer.writerow(rec.to_dict())

    def list_exclusions(self, run_id: Optional[str] = None) -> List[dict]:
        path = self._path("symbol_exclusions.csv")
        if not os.path.isfile(path):
            return []
        try:
            with open(path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            if run_id:
                return [r for r in rows if r.get("run_id") == run_id]
            return rows
        except Exception as exc:
            logger.warning("list_exclusions failed: %s", exc)
            return []

    # ---- Hashes ----

    def save_hash(self, run_id: str, reproducibility_hash: str) -> None:
        path = self._path("run_hashes.csv")
        write_header = not os.path.isfile(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["run_id", "reproducibility_hash", "saved_at"])
            if write_header:
                writer.writeheader()
            writer.writerow({
                "run_id": run_id,
                "reproducibility_hash": reproducibility_hash,
                "saved_at": _now_utc(),
            })

    def get_hash(self, run_id: str) -> Optional[str]:
        path = self._path("run_hashes.csv")
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row.get("run_id") == run_id:
                        return row.get("reproducibility_hash")
        except Exception:
            pass
        return None

    # ---- Audit summary ----

    def save_audit_summary(self, run_id: str, summary: dict) -> None:
        path = self._path("audit_summary.csv")
        row = {"run_id": run_id, "saved_at": _now_utc()}
        row.update({k: str(v) for k, v in summary.items()})
        write_header = not os.path.isfile(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)
