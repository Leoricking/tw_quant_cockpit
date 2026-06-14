"""
quality_gates.gate_store — GateStore v1.1.4

Runtime CSV persistence for quality gate outputs.
Saves to data/quality_gate_reports/ — NOT committed to git.
Uses csv module (not pandas).
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GateStore:
    """Saves and loads quality gate runtime outputs as CSV files."""

    def __init__(self, output_dir: Optional[str] = None):
        self._output_dir = output_dir or os.path.join(BASE_DIR, "data", "quality_gate_reports")

    @property
    def output_dir(self) -> str:
        return self._output_dir

    def _ensure_dir(self) -> None:
        os.makedirs(self._output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)

    def save_decisions(self, decisions: List[Any]) -> str:
        """Save list of QualityGateDecision objects or dicts to CSV."""
        self._ensure_dir()
        path = self._path("symbol_gate_decisions.csv")
        rows = []
        for d in decisions:
            row = d.to_dict() if hasattr(d, "to_dict") else (d if isinstance(d, dict) else {})
            # Flatten list fields to JSON strings for CSV
            flat = {}
            for k, v in row.items():
                flat[k] = json.dumps(v) if isinstance(v, (list, dict)) else v
            rows.append(flat)
        if rows:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        else:
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("symbol,gate_name,gate_level,decision,confidence\n")
        logger.info("GateStore: saved %d decisions to %s", len(rows), path)
        return path

    def load_decisions(self) -> List[Dict]:
        """Load saved decisions CSV."""
        path = self._path("symbol_gate_decisions.csv")
        if not os.path.exists(path):
            return []
        try:
            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
            return rows
        except Exception as exc:
            logger.warning("GateStore.load_decisions failed: %s", exc)
            return []

    def save_universe_summary(self, summary: Any) -> str:
        """Save a UniverseGateSummary to CSV."""
        self._ensure_dir()
        path = self._path("universe_gate_summary.csv")
        row = summary.to_dict() if hasattr(summary, "to_dict") else (summary if isinstance(summary, dict) else {})
        flat = {k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in row.items()}
        with open(path, "w", newline="", encoding="utf-8") as f:
            if flat:
                writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
                writer.writeheader()
                writer.writerow(flat)
            else:
                f.write("tier,formal_eligible,observational_eligible,blocked\n")
        return path

    def load_universe_summary(self) -> Optional[Dict]:
        """Load saved universe summary."""
        path = self._path("universe_gate_summary.csv")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    return dict(row)
        except Exception as exc:
            logger.warning("GateStore.load_universe_summary failed: %s", exc)
        return None

    def save_gate_matrix(self, matrix: Dict[str, Dict[str, str]]) -> str:
        """Save gate matrix {symbol: {gate: level}} to CSV."""
        self._ensure_dir()
        path = self._path("gate_matrix.csv")
        if not matrix:
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("symbol\n")
            return path
        # Collect all gate names
        all_gates: List[str] = []
        for row in matrix.values():
            for g in row:
                if g not in all_gates:
                    all_gates.append(g)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol"] + all_gates)
            writer.writeheader()
            for sym, gates in matrix.items():
                row = {"symbol": sym}
                row.update(gates)
                writer.writerow(row)
        return path

    def load_gate_matrix(self) -> Dict:
        """Load gate matrix CSV."""
        path = self._path("gate_matrix.csv")
        if not os.path.exists(path):
            return {}
        try:
            result = {}
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sym = row.pop("symbol", "")
                    if sym:
                        result[sym] = dict(row)
            return result
        except Exception as exc:
            logger.warning("GateStore.load_gate_matrix failed: %s", exc)
            return {}

    def save_reason_codes(self) -> str:
        """Save REASON_CODE_METADATA to CSV."""
        self._ensure_dir()
        path = self._path("gate_reason_codes.csv")
        try:
            from quality_gates.gate_schema import REASON_CODE_METADATA
            rows = []
            for code, meta in REASON_CODE_METADATA.items():
                rows.append({
                    "reason_code": code,
                    "severity": meta.get("severity", ""),
                    "blocking_by_default": meta.get("blocking_by_default", False),
                    "explanation": meta.get("explanation", ""),
                    "safe_action": meta.get("safe_action", ""),
                })
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["reason_code", "severity",
                                                         "blocking_by_default", "explanation", "safe_action"])
                writer.writeheader()
                writer.writerows(rows)
        except Exception as exc:
            logger.warning("GateStore.save_reason_codes failed: %s", exc)
        return path

    def save_execution_filter(self, filter_dict: Dict) -> str:
        """Save execution filter to CSV."""
        self._ensure_dir()
        path = self._path("gate_execution_filter.csv")
        rows = []
        for sym, data in filter_dict.items():
            rows.append({
                "symbol": sym,
                "eligible": data.get("eligible", False),
                "gate_level": data.get("gate_level", "BLOCKED"),
                "decision": data.get("decision", ""),
                "reason_codes": json.dumps(data.get("reason_codes", [])),
                "confidence": data.get("confidence", "UNKNOWN"),
            })
        with open(path, "w", newline="", encoding="utf-8") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            else:
                f.write("symbol,eligible,gate_level,decision,reason_codes,confidence\n")
        return path

    def save_overrides(self, overrides: List) -> str:
        """Save override records to CSV."""
        self._ensure_dir()
        path = self._path("gate_overrides.csv")
        rows = []
        for o in overrides:
            row = o.to_dict() if hasattr(o, "to_dict") else (o if isinstance(o, dict) else {})
            flat = {k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in row.items()}
            rows.append(flat)
        with open(path, "w", newline="", encoding="utf-8") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            else:
                f.write("override_id,decision_id,symbol,original_decision,requested_decision,reason\n")
        return path

    def save_run_history(self, run_summary: Dict) -> str:
        """Append a run summary entry to run history CSV."""
        self._ensure_dir()
        path = self._path("gate_run_history.csv")
        flat = {k: (json.dumps(v) if isinstance(v, (list, dict)) else v)
                for k, v in run_summary.items()}
        flat["saved_at"] = datetime.now(timezone.utc).isoformat()
        file_exists = os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(flat)
        return path
