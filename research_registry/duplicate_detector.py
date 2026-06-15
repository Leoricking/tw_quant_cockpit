"""
research_registry.duplicate_detector — ResearchRunDuplicateDetector v1.1.8

Detects exact and near-duplicate research runs by fingerprint.
Exact duplicate: only mark, never delete.
mock vs real: NEVER exact duplicate.
Different gate policy or included symbols: NOT exact duplicate.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ResearchRunDuplicateDetector:
    """
    Detects exact and near-duplicate research runs.

    Fingerprint includes:
        command_name, sorted(normalized_arguments), mode, tier, stock,
        sorted(included_symbols), gate_name, gate_policy_version,
        code_version, sorted(data_snapshot_ids), reproducibility_hash.

    Does NOT include: timestamp, temp paths, output paths, secrets.

    [!] Exact duplicate: only mark, never delete.
    [!] mock vs real: NEVER exact duplicate.
    [!] Different gate policy: NOT exact duplicate.
    [!] Different included symbols: NOT exact duplicate.
    """

    no_real_orders = True
    research_only = True

    def __init__(self):
        self._duplicates: Dict[str, str] = {}  # run_id -> original_run_id

    def build_fingerprint(self, run: Any) -> str:
        """Build a deterministic fingerprint for a run record."""
        try:
            args = {}
            if hasattr(run, "arguments") and run.arguments:
                args = run.arguments
            elif isinstance(run, dict):
                args = run.get("arguments", {})

            # Normalize and sort arguments (exclude sensitive and path fields)
            norm_args = self._normalize_args(args)
            sorted_args = sorted(norm_args.items())

            included_syms = []
            if hasattr(run, "included_symbols"):
                included_syms = sorted(run.included_symbols or [])
            elif isinstance(run, dict):
                included_syms = sorted(run.get("included_symbols", []) or [])

            mode = getattr(run, "mode", None) or run.get("mode", "") if isinstance(run, dict) else ""
            tier = getattr(run, "tier", None) or run.get("tier", "") if isinstance(run, dict) else ""
            stock = getattr(run, "stock", None) or run.get("stock", "") if isinstance(run, dict) else ""
            command_name = getattr(run, "command_name", None) or run.get("command_name", "") if isinstance(run, dict) else ""
            gate_name = getattr(run, "gate_name", None) or run.get("gate_name", "") if isinstance(run, dict) else ""
            gate_policy_version = getattr(run, "gate_policy_version", None) or run.get("gate_policy_version", "") if isinstance(run, dict) else ""
            code_version = getattr(run, "code_version", None) or run.get("code_version", "") if isinstance(run, dict) else ""
            reproducibility_hash = getattr(run, "reproducibility_hash", None) or run.get("reproducibility_hash", "") if isinstance(run, dict) else ""

            # Build snapshot ids list
            snapshot_ids = []
            for key in ("gate_snapshot_id", "coverage_snapshot_id", "freshness_snapshot_id"):
                val = getattr(run, key, None) or (run.get(key, "") if isinstance(run, dict) else "")
                if val:
                    snapshot_ids.append(val)
            snapshot_ids = sorted(snapshot_ids)

            payload = {
                "command_name": str(command_name).strip().lower(),
                "mode": str(mode).strip().lower(),
                "tier": str(tier).strip().lower(),
                "stock": str(stock).strip().lower(),
                "included_symbols": included_syms,
                "gate_name": str(gate_name).strip().lower(),
                "gate_policy_version": str(gate_policy_version).strip().lower(),
                "code_version": str(code_version).strip().lower(),
                "reproducibility_hash": str(reproducibility_hash).strip().lower(),
                "snapshot_ids": snapshot_ids,
                "arguments": sorted_args,
            }

            canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
            return _sha256_hex(canonical)
        except Exception as exc:
            logger.warning("build_fingerprint failed (non-fatal): %s", exc)
            return ""

    def find_exact_duplicate(self, run: Any, existing_runs: List[Any]) -> Optional[str]:
        """Return the run_id of an exact duplicate if found, else None."""
        try:
            fp = self.build_fingerprint(run)
            if not fp:
                return None
            run_id = getattr(run, "run_id", None) or (run.get("run_id", "") if isinstance(run, dict) else "")

            # mock vs real: never exact duplicate
            run_mode = getattr(run, "mode", "") or (run.get("mode", "") if isinstance(run, dict) else "")

            for existing in existing_runs:
                existing_id = getattr(existing, "run_id", None) or (existing.get("run_id", "") if isinstance(existing, dict) else "")
                if existing_id == run_id:
                    continue

                existing_mode = getattr(existing, "mode", "") or (existing.get("mode", "") if isinstance(existing, dict) else "")
                # mock vs real: never exact duplicate
                if run_mode != existing_mode:
                    continue

                existing_fp = self.build_fingerprint(existing)
                if fp and existing_fp and fp == existing_fp:
                    return existing_id
        except Exception as exc:
            logger.warning("find_exact_duplicate failed (non-fatal): %s", exc)
        return None

    def find_near_duplicates(self, run: Any, existing_runs: List[Any]) -> List[dict]:
        """Find near-duplicate runs (same command+mode, slightly different arguments)."""
        result = []
        try:
            run_id = getattr(run, "run_id", None) or (run.get("run_id", "") if isinstance(run, dict) else "")
            command_name = getattr(run, "command_name", "") or (run.get("command_name", "") if isinstance(run, dict) else "")
            mode = getattr(run, "mode", "") or (run.get("mode", "") if isinstance(run, dict) else "")

            for existing in existing_runs:
                existing_id = getattr(existing, "run_id", None) or (existing.get("run_id", "") if isinstance(existing, dict) else "")
                if existing_id == run_id:
                    continue
                existing_cmd = getattr(existing, "command_name", "") or (existing.get("command_name", "") if isinstance(existing, dict) else "")
                existing_mode = getattr(existing, "mode", "") or (existing.get("mode", "") if isinstance(existing, dict) else "")

                if existing_cmd != command_name or existing_mode != mode:
                    continue

                diff = self.compare_fingerprints(run, existing)
                similarity = diff.get("similarity_score", 0.0)
                if similarity >= 0.7 and not diff.get("exact", False):
                    result.append({
                        "run_id": run_id,
                        "similar_to": existing_id,
                        "similarity_score": similarity,
                        "differences": diff.get("differences", []),
                    })
        except Exception as exc:
            logger.warning("find_near_duplicates failed (non-fatal): %s", exc)
        return result

    def compare_fingerprints(self, run_a: Any, run_b: Any) -> dict:
        """Compare two runs' fingerprint components and return differences."""
        differences = []
        try:
            fields_to_check = [
                "command_name", "mode", "tier", "stock",
                "gate_name", "gate_policy_version", "code_version",
            ]
            for field in fields_to_check:
                val_a = getattr(run_a, field, "") or (run_a.get(field, "") if isinstance(run_a, dict) else "")
                val_b = getattr(run_b, field, "") or (run_b.get(field, "") if isinstance(run_b, dict) else "")
                if str(val_a).lower() != str(val_b).lower():
                    differences.append({"field": field, "a": val_a, "b": val_b})

            syms_a = sorted(getattr(run_a, "included_symbols", []) or [])
            syms_b = sorted(getattr(run_b, "included_symbols", []) or [])
            if syms_a != syms_b:
                differences.append({"field": "included_symbols", "a": syms_a, "b": syms_b})

            fp_a = self.build_fingerprint(run_a)
            fp_b = self.build_fingerprint(run_b)
            exact = fp_a == fp_b and bool(fp_a)

            total_fields = len(fields_to_check) + 1  # +1 for symbols
            similarity_score = max(0.0, 1.0 - len(differences) / total_fields) if not exact else 1.0

            return {
                "exact": exact,
                "differences": differences,
                "similarity_score": round(similarity_score, 3),
            }
        except Exception as exc:
            logger.warning("compare_fingerprints failed (non-fatal): %s", exc)
            return {"exact": False, "differences": [], "similarity_score": 0.0}

    def explain_duplicate(self, run_id: str) -> str:
        """Return a human-readable explanation for why a run is marked as duplicate."""
        original_id = self._duplicates.get(run_id, "")
        if not original_id:
            return f"Run {run_id} is NOT marked as a duplicate."
        return (
            f"Run {run_id} is marked as a duplicate of {original_id}. "
            f"Both runs have the same fingerprint (command, mode, tier, stock, "
            f"included_symbols, gate_policy_version, code_version)."
        )

    def mark_duplicate(self, run_id: str, original_run_id: str) -> None:
        """Mark a run as duplicate of another (does NOT delete either)."""
        self._duplicates[run_id] = original_run_id

    def get_duplicate_map(self) -> Dict[str, str]:
        """Return mapping of duplicate_run_id -> original_run_id."""
        return dict(self._duplicates)

    def _normalize_args(self, args: dict) -> dict:
        """Normalize arguments: remove paths, timestamps, secrets, output fields."""
        if not isinstance(args, dict):
            return {}
        exclude_keys = [
            "output_dir", "output_file", "report_dir", "log_file",
            "started_at", "completed_at", "timestamp", "run_id", "registry_id",
            # sensitive fields
            "api_key", "token", "secret", "password", "cookie", "authorization",
        ]
        result = {}
        for k, v in args.items():
            k_lower = str(k).lower()
            if any(ex in k_lower for ex in exclude_keys):
                continue
            if isinstance(v, (str, int, float, bool)):
                result[k_lower] = str(v).lower()
            elif isinstance(v, list):
                result[k_lower] = sorted(str(x).lower() for x in v)
        return result
