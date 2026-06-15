"""
research_registry.run_comparator — ResearchRunComparator v1.1.8

Compares two research run records across arguments, symbols, artifacts, metrics.
"unavailable" shown when metric is missing. No crash on missing data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_METRICS_TO_COMPARE = [
    "sample_count", "signal_count", "win_rate", "avg_return",
    "median_return", "profit_factor", "drawdown",
    "formal_eligible_count", "blocked_count", "alert_count",
    "p0_count", "p1_count",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ResearchRunComparator:
    """
    Compares two research run records.

    [!] Research Only. No Real Orders.
    Shows "unavailable" for missing metrics. Never crashes on missing data.
    """

    no_real_orders = True
    research_only = True

    def compare(self, run_a: Any, run_b: Any) -> Any:
        """Compare two ResearchRunRecord objects and return RunComparison."""
        from research_registry.registry_schema import RunComparison

        try:
            id_a = getattr(run_a, "run_id", "") or (run_a.get("run_id", "") if isinstance(run_a, dict) else "")
            id_b = getattr(run_b, "run_id", "") or (run_b.get("run_id", "") if isinstance(run_b, dict) else "")

            arg_changes = self.compare_arguments(run_a, run_b)
            sym_changes = self.compare_symbols(run_a, run_b)
            art_changes = self.compare_artifacts(run_a, run_b)
            metric_changes = self.compare_metrics(run_a, run_b)
            qual_change = self.compare_qualification(run_a, run_b)
            status_change = self.compare_status(run_a, run_b)

            hash_a = getattr(run_a, "reproducibility_hash", "") or (run_a.get("reproducibility_hash", "") if isinstance(run_a, dict) else "")
            hash_b = getattr(run_b, "reproducibility_hash", "") or (run_b.get("reproducibility_hash", "") if isinstance(run_b, dict) else "")
            hash_match = bool(hash_a and hash_b and hash_a == hash_b)

            ver_a = getattr(run_a, "code_version", "") or (run_a.get("code_version", "") if isinstance(run_a, dict) else "")
            ver_b = getattr(run_b, "code_version", "") or (run_b.get("code_version", "") if isinstance(run_b, dict) else "")
            code_version_change = f"{ver_a} → {ver_b}" if ver_a != ver_b else "same"

            gp_a = getattr(run_a, "gate_policy_version", "") or (run_a.get("gate_policy_version", "") if isinstance(run_a, dict) else "")
            gp_b = getattr(run_b, "gate_policy_version", "") or (run_b.get("gate_policy_version", "") if isinstance(run_b, dict) else "")
            gate_policy_change = f"{gp_a} → {gp_b}" if gp_a != gp_b else "same"

            comparable = (
                _get_field(run_a, "command_name") == _get_field(run_b, "command_name")
            )

            comp = RunComparison(
                comparison_id=str(uuid.uuid4()),
                run_a=id_a,
                run_b=id_b,
                comparable=comparable,
                difference_summary=self._build_summary(arg_changes, sym_changes, qual_change, status_change),
                argument_changes=arg_changes,
                symbol_changes=sym_changes,
                qualification_change=qual_change,
                status_change=status_change,
                artifact_changes=art_changes,
                metric_changes=metric_changes,
                hash_match=hash_match,
                code_version_change=code_version_change,
                gate_policy_change=gate_policy_change,
                created_at=_now_utc(),
            )
            return comp
        except Exception as exc:
            logger.warning("compare failed (non-fatal): %s", exc)
            from research_registry.registry_schema import RunComparison
            return RunComparison(
                comparison_id=str(uuid.uuid4()),
                run_a="", run_b="", comparable=False,
                difference_summary=f"Comparison error: {exc}",
                created_at=_now_utc(),
            )

    def compare_arguments(self, run_a: Any, run_b: Any) -> dict:
        """Compare arguments of two runs."""
        args_a = _get_field(run_a, "arguments") or {}
        args_b = _get_field(run_b, "arguments") or {}
        if not isinstance(args_a, dict):
            args_a = {}
        if not isinstance(args_b, dict):
            args_b = {}

        all_keys = set(list(args_a.keys()) + list(args_b.keys()))
        added = {k: args_b[k] for k in all_keys if k in args_b and k not in args_a}
        removed = {k: args_a[k] for k in all_keys if k in args_a and k not in args_b}
        changed = {k: {"a": args_a[k], "b": args_b[k]} for k in all_keys if k in args_a and k in args_b and str(args_a[k]) != str(args_b[k])}

        return {"added": added, "removed": removed, "changed": changed}

    def compare_symbols(self, run_a: Any, run_b: Any) -> dict:
        """Compare symbol sets of two runs."""
        syms_a = set(_get_field(run_a, "included_symbols") or [])
        syms_b = set(_get_field(run_b, "included_symbols") or [])
        return {
            "only_in_a": sorted(syms_a - syms_b),
            "only_in_b": sorted(syms_b - syms_a),
            "shared": sorted(syms_a & syms_b),
        }

    def compare_artifacts(self, run_a: Any, run_b: Any) -> dict:
        """Compare artifact IDs of two runs."""
        arts_a = set(_get_field(run_a, "output_artifact_ids") or [])
        arts_b = set(_get_field(run_b, "output_artifact_ids") or [])
        return {
            "only_in_a": sorted(arts_a - arts_b),
            "only_in_b": sorted(arts_b - arts_a),
            "shared": sorted(arts_a & arts_b),
        }

    def compare_metrics(self, run_a: Any, run_b: Any) -> dict:
        """Compare metrics from two runs' arguments or metadata."""
        result = {}
        args_a = _get_field(run_a, "arguments") or {}
        args_b = _get_field(run_b, "arguments") or {}
        if not isinstance(args_a, dict):
            args_a = {}
        if not isinstance(args_b, dict):
            args_b = {}

        for metric in _METRICS_TO_COMPARE:
            val_a = args_a.get(metric, None)
            val_b = args_b.get(metric, None)
            a_str = str(val_a) if val_a is not None else "unavailable"
            b_str = str(val_b) if val_b is not None else "unavailable"
            result[metric] = {"a": a_str, "b": b_str}

        return result

    def compare_qualification(self, run_a: Any, run_b: Any) -> str:
        """Return qualification change description."""
        qual_a = _get_field(run_a, "qualification") or "UNKNOWN"
        qual_b = _get_field(run_b, "qualification") or "UNKNOWN"
        if qual_a == qual_b:
            return f"same ({qual_a})"
        return f"{qual_a} → {qual_b}"

    def compare_status(self, run_a: Any, run_b: Any) -> str:
        """Return status change description."""
        st_a = _get_field(run_a, "status") or "UNKNOWN"
        st_b = _get_field(run_b, "status") or "UNKNOWN"
        if st_a == st_b:
            return f"same ({st_a})"
        return f"{st_a} → {st_b}"

    def summarize(self, comparison: Any) -> str:
        """Return a short text summary of a RunComparison."""
        try:
            lines = [
                f"Comparison: {comparison.run_a} vs {comparison.run_b}",
                f"Comparable: {comparison.comparable}",
                f"Qualification: {comparison.qualification_change}",
                f"Status: {comparison.status_change}",
                f"Code Version: {comparison.code_version_change}",
                f"Gate Policy: {comparison.gate_policy_change}",
                f"Hash Match: {comparison.hash_match}",
            ]
            arg_ch = comparison.argument_changes or {}
            if any(arg_ch.get(k) for k in ("added", "removed", "changed")):
                lines.append(f"Argument changes: {comparison.difference_summary}")
            return "\n".join(lines)
        except Exception:
            return "Comparison summary unavailable"

    def render_markdown(self, comparison: Any) -> str:
        """Render a RunComparison as a Markdown string."""
        try:
            lines = [
                f"## Run Comparison",
                f"",
                f"| Field | Run A | Run B |",
                f"|-------|-------|-------|",
                f"| Run ID | {comparison.run_a} | {comparison.run_b} |",
                f"| Comparable | {comparison.comparable} | — |",
                f"| Qualification | {comparison.qualification_change} | — |",
                f"| Status | {comparison.status_change} | — |",
                f"| Code Version | {comparison.code_version_change} | — |",
                f"| Gate Policy | {comparison.gate_policy_change} | — |",
                f"| Hash Match | {comparison.hash_match} | — |",
                f"",
                f"### Metrics",
                f"",
                f"| Metric | Run A | Run B |",
                f"|--------|-------|-------|",
            ]
            for metric, vals in (comparison.metric_changes or {}).items():
                lines.append(f"| {metric} | {vals.get('a', 'unavailable')} | {vals.get('b', 'unavailable')} |")
            lines += ["", f"*[!] Research Only. No Real Orders.*"]
            return "\n".join(lines)
        except Exception:
            return "Comparison markdown unavailable"

    def _build_summary(self, arg_changes: dict, sym_changes: dict, qual_change: str, status_change: str) -> str:
        parts = []
        if arg_changes.get("added") or arg_changes.get("removed") or arg_changes.get("changed"):
            n = len(arg_changes.get("added", {})) + len(arg_changes.get("removed", {})) + len(arg_changes.get("changed", {}))
            parts.append(f"{n} argument change(s)")
        sym_diff = len(sym_changes.get("only_in_a", [])) + len(sym_changes.get("only_in_b", []))
        if sym_diff:
            parts.append(f"{sym_diff} symbol difference(s)")
        if "→" in qual_change:
            parts.append(f"qualification: {qual_change}")
        if "→" in status_change:
            parts.append(f"status: {status_change}")
        return "; ".join(parts) if parts else "no significant differences"


def _get_field(obj: Any, field: str) -> Any:
    """Get field from dataclass or dict."""
    if hasattr(obj, field):
        return getattr(obj, field)
    if isinstance(obj, dict):
        return obj.get(field)
    return None
