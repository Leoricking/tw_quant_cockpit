"""
research_registry.run_capture — ResearchRunCapture v1.1.8

Captures run lifecycle events (start, complete, fail, block, cancel).
Never stores secrets. Registry failure does NOT break the underlying command.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NEVER store: api_key, token, secret, password, cookie, authorization, broker credentials.
"""
from __future__ import annotations

import logging
import os
import subprocess
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_SENSITIVE_FIELD_FRAGMENTS = [
    "api_key", "token", "secret", "password", "cookie", "authorization",
    "api_secret", "access_token", "refresh_token", "auth_token", "bearer",
    "credential", "broker_key", "shioaji_key", "shioaji_token",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


class ResearchRunCapture:
    """
    Captures research run lifecycle events into ResearchRunRecord objects.

    [!] Research Only. No Real Orders.
    [!] NEVER stores api_key, token, secret, password, cookie, authorization.
    [!] Registry failure MUST NOT break the underlying research command.
    """

    no_real_orders = True
    research_only = True

    def __init__(self):
        self._runs: Dict[str, Any] = {}

    def start_run(self, command_name: str, args: dict, context: Optional[dict] = None) -> Any:
        """Create a CREATED/RUNNING record for a new run."""
        try:
            from research_registry.registry_schema import ResearchRunRecord
            from research_registry.run_classifier import ResearchRunClassifier

            classifier = ResearchRunClassifier()
            run_id = _new_uuid()
            registry_id = f"RR-{run_id[:8].upper()}"
            mode = (args or {}).get("mode", "real")
            tier = (args or {}).get("tier", "")
            stock = (args or {}).get("stock", "")

            ctx = context or {}
            git_ctx = self.capture_git_context()
            ver_ctx = self.capture_version_context()
            sym_ctx = self.capture_symbols(args or {})
            clean_args = self.sanitize_arguments(args or {})

            record = ResearchRunRecord(
                registry_id=registry_id,
                run_id=run_id,
                run_type=classifier.classify(command_name),
                command_name=command_name,
                command_category=classifier.category(command_name),
                status="RUNNING",
                qualification=classifier.default_qualification(command_name, mode),
                mode=mode,
                tier=tier,
                stock=stock,
                requested_symbols=sym_ctx.get("requested_symbols", []),
                included_symbols=sym_ctx.get("included_symbols", []),
                excluded_symbols=sym_ctx.get("excluded_symbols", []),
                arguments=clean_args,
                started_at=_now_utc(),
                code_version=ver_ctx.get("version", ""),
                release_name=ver_ctx.get("release_name", ""),
                git_commit=git_ctx.get("commit", ""),
                git_tag=git_ctx.get("tag", ""),
                git_branch=git_ctx.get("branch", ""),
                parent_run_id=ctx.get("parent_run_id", ""),
                root_run_id=ctx.get("root_run_id", ""),
                rerun_of=ctx.get("rerun_of", ""),
                notes=ctx.get("notes", ""),
            )
            self._runs[run_id] = record
            return record
        except Exception as exc:
            logger.warning("ResearchRunCapture.start_run failed (non-fatal): %s", exc)
            return None

    def capture_running_state(self, run_id: str, **kwargs) -> None:
        """Update running state for a run (no-op if run not found)."""
        try:
            if run_id in self._runs:
                record = self._runs[run_id]
                for k, v in kwargs.items():
                    if hasattr(record, k):
                        setattr(record, k, v)
        except Exception as exc:
            logger.warning("capture_running_state failed (non-fatal): %s", exc)

    def complete_run(self, run_id: str, result: Any, artifacts: Optional[List[str]] = None) -> Optional[Any]:
        """Mark a run as COMPLETED."""
        try:
            from research_registry.registry_schema import ResearchRunRecord
            record = self._runs.get(run_id)
            if record is None:
                return None

            record.status = "COMPLETED"
            record.completed_at = _now_utc()
            record.duration_seconds = self._calc_duration(record.started_at, record.completed_at)

            if result and hasattr(result, "get"):
                metrics = self.capture_metrics(result)
                if metrics.get("warning_count", 0) > 0:
                    record.status = "COMPLETED_WITH_WARNINGS"
                    record.warning_count = metrics["warning_count"]
                record.error_count = metrics.get("error_count", 0)

            output_ids = self.capture_outputs(result or {})
            if artifacts:
                output_ids.extend(artifacts)
            record.output_artifact_ids = list(set(output_ids))

            return record
        except Exception as exc:
            logger.warning("complete_run failed (non-fatal): %s", exc)
            return None

    def warn_run(self, run_id: str, warnings: List[str]) -> Optional[Any]:
        """Mark a run as COMPLETED_WITH_WARNINGS."""
        try:
            record = self._runs.get(run_id)
            if record is None:
                return None
            record.status = "COMPLETED_WITH_WARNINGS"
            record.warning_count = len(warnings)
            record.completed_at = _now_utc()
            record.duration_seconds = self._calc_duration(record.started_at, record.completed_at)
            return record
        except Exception as exc:
            logger.warning("warn_run failed (non-fatal): %s", exc)
            return None

    def block_run(self, run_id: str, reasons: List[str]) -> Optional[Any]:
        """Mark a run as BLOCKED."""
        try:
            record = self._runs.get(run_id)
            if record is None:
                return None
            record.status = "BLOCKED"
            record.qualification = "BLOCKED"
            record.blocked_reason_codes = reasons or []
            record.completed_at = _now_utc()
            record.duration_seconds = self._calc_duration(record.started_at, record.completed_at)
            return record
        except Exception as exc:
            logger.warning("block_run failed (non-fatal): %s", exc)
            return None

    def fail_run(self, run_id: str, error: Any) -> Optional[Any]:
        """Mark a run as FAILED."""
        try:
            record = self._runs.get(run_id)
            if record is None:
                return None
            record.status = "FAILED"
            record.error_count = 1
            record.notes = f"Error: {error}" if error else "Unknown error"
            record.completed_at = _now_utc()
            record.duration_seconds = self._calc_duration(record.started_at, record.completed_at)
            return record
        except Exception as exc:
            logger.warning("fail_run failed (non-fatal): %s", exc)
            return None

    def cancel_run(self, run_id: str, reason: str) -> Optional[Any]:
        """Mark a run as CANCELLED."""
        try:
            record = self._runs.get(run_id)
            if record is None:
                return None
            record.status = "CANCELLED"
            record.notes = f"Cancelled: {reason}" if reason else "Cancelled"
            record.completed_at = _now_utc()
            record.duration_seconds = self._calc_duration(record.started_at, record.completed_at)
            return record
        except Exception as exc:
            logger.warning("cancel_run failed (non-fatal): %s", exc)
            return None

    def capture_gate_context(self, run_id: str, enforcement_result: Any) -> None:
        """Capture gate enforcement context for a run."""
        try:
            record = self._runs.get(run_id)
            if record is None:
                return
            if enforcement_result and hasattr(enforcement_result, "get"):
                record.gate_name = enforcement_result.get("gate_name", "")
                record.gate_policy_version = enforcement_result.get("policy_version", "")
                record.gate_requested_level = enforcement_result.get("requested_level", "")
                record.gate_applied_level = enforcement_result.get("applied_level", "")
                record.gate_snapshot_id = enforcement_result.get("snapshot_id", "")
                record.reproducibility_hash = enforcement_result.get("reproducibility_hash", "")
                qual = enforcement_result.get("qualification", "")
                if qual:
                    record.qualification = qual
        except Exception as exc:
            logger.warning("capture_gate_context failed (non-fatal): %s", exc)

    def capture_git_context(self) -> dict:
        """Capture current git context (commit, tag, branch)."""
        result = {"commit": "", "tag": "", "branch": ""}
        try:
            import subprocess
            def _git(args):
                try:
                    out = subprocess.check_output(
                        ["git", "-C", BASE_DIR] + args,
                        stderr=subprocess.DEVNULL,
                        timeout=5,
                    )
                    return out.decode("utf-8", errors="replace").strip()
                except Exception:
                    return ""

            result["commit"] = _git(["rev-parse", "--short", "HEAD"])
            result["branch"] = _git(["rev-parse", "--abbrev-ref", "HEAD"])
            result["tag"] = _git(["describe", "--tags", "--exact-match", "HEAD"])
        except Exception as exc:
            logger.debug("capture_git_context failed (non-fatal): %s", exc)
        return result

    def capture_version_context(self) -> dict:
        """Capture current version context from release.version_info."""
        result = {"version": "", "release_name": ""}
        try:
            from release.version_info import VERSION, RELEASE_NAME
            result["version"] = str(VERSION)
            result["release_name"] = str(RELEASE_NAME)
        except Exception as exc:
            logger.debug("capture_version_context failed (non-fatal): %s", exc)
        return result

    def capture_symbols(self, args: dict) -> dict:
        """Extract symbol lists from arguments."""
        result = {
            "requested_symbols": [],
            "included_symbols": [],
            "excluded_symbols": [],
        }
        try:
            if not args:
                return result
            for key in ("symbols", "requested_symbols", "symbol_list"):
                val = args.get(key, [])
                if val:
                    if isinstance(val, str):
                        val = [s.strip() for s in val.split(",") if s.strip()]
                    result["requested_symbols"] = list(val)
                    break
            for key in ("included_symbols", "included"):
                val = args.get(key, [])
                if val:
                    if isinstance(val, str):
                        val = [s.strip() for s in val.split(",") if s.strip()]
                    result["included_symbols"] = list(val)
                    break
            for key in ("excluded_symbols", "excluded"):
                val = args.get(key, [])
                if val:
                    if isinstance(val, str):
                        val = [s.strip() for s in val.split(",") if s.strip()]
                    result["excluded_symbols"] = list(val)
                    break
        except Exception as exc:
            logger.debug("capture_symbols failed (non-fatal): %s", exc)
        return result

    def capture_outputs(self, result: Any) -> list:
        """Extract artifact IDs from a command result."""
        ids = []
        try:
            if not result:
                return ids
            if isinstance(result, dict):
                for key in ("output_files", "artifacts", "output_artifact_ids", "outputs"):
                    val = result.get(key, [])
                    if val and isinstance(val, list):
                        ids.extend(str(v) for v in val if v)
                        break
        except Exception:
            pass
        return ids

    def capture_metrics(self, result: Any) -> dict:
        """Extract metrics from a command result."""
        metrics = {"warning_count": 0, "error_count": 0}
        try:
            if isinstance(result, dict):
                metrics["warning_count"] = int(result.get("warning_count", 0))
                metrics["error_count"] = int(result.get("error_count", 0))
        except Exception:
            pass
        return metrics

    def sanitize_arguments(self, args: dict) -> dict:
        """Remove sensitive fields from arguments before storing."""
        return self.redact_sensitive_fields(args)

    def redact_sensitive_fields(self, data: dict) -> dict:
        """Strip any field name containing sensitive fragments."""
        if not isinstance(data, dict):
            return {}
        clean = {}
        for k, v in data.items():
            key_lower = str(k).lower()
            is_sensitive = any(frag in key_lower for frag in _SENSITIVE_FIELD_FRAGMENTS)
            if is_sensitive:
                clean[k] = "[REDACTED]"
            elif isinstance(v, dict):
                clean[k] = self.redact_sensitive_fields(v)
            else:
                clean[k] = v
        return clean

    def get_record(self, run_id: str) -> Optional[Any]:
        """Return captured record by run_id."""
        return self._runs.get(run_id)

    def _calc_duration(self, started_at: str, completed_at: str) -> float:
        """Calculate duration in seconds between two ISO timestamps."""
        try:
            from datetime import datetime
            fmt = "%Y-%m-%dT%H:%M:%S.%f%z"
            t0 = datetime.fromisoformat(started_at)
            t1 = datetime.fromisoformat(completed_at)
            return max(0.0, (t1 - t0).total_seconds())
        except Exception:
            return 0.0
