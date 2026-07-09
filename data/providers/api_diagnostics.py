"""
data/providers/api_diagnostics.py - Unified API fetch diagnostics (v0.4.1).

Aggregates per-provider, per-dataset fetch results for display in CLI and GUI.

[!] Read Only. No Real Orders.
[!] Never records token or full credentials.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class APIFetchDiagnostics:
    """
    Unified API fetch diagnostics aggregator.

    Records per-provider/dataset results and exposes summary and DataFrame views.

    Output fields per record:
        provider, dataset, status, rows, latency_ms, retry_attempts,
        cache_hit, fallback_used, error_type, warning, recommended_action
    """

    read_only      = True
    no_real_orders = True

    def __init__(self):
        self._records: List[dict] = []

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_provider_result(
        self,
        provider: str,
        dataset:  str,
        result:   dict,
    ) -> dict:
        """
        Record the result of one provider/dataset fetch.

        Parameters
        ----------
        provider : Provider name (e.g. "finmind", "twse")
        dataset  : Dataset name (e.g. "daily_price", "monthly_revenue")
        result   : Dict from fetch operation containing at least:
                   status, rows (or rows_fetched), latency_ms,
                   retry_attempts, cache_hit, fallback_used,
                   error_type, warning
        """
        rows = result.get("rows", result.get("rows_fetched", 0)) or 0
        status = result.get("status", "UNKNOWN")
        latency_ms = result.get("latency_ms", result.get("elapsed_ms", 0)) or 0
        retry_attempts = result.get("retry_attempts", result.get("attempts", 1)) or 1
        cache_hit = result.get("cache_hit", result.get("cache_status", "") == "HIT")
        fallback_used = result.get("fallback_used", False)
        error_type = result.get("error_type", result.get("error", ""))
        warning = result.get("warning", "")

        # Suppress any token in error messages
        if error_type:
            error_type = self._sanitize_message(str(error_type))
        if warning:
            warning = self._sanitize_message(str(warning))

        recommended_action = self._recommend(status, error_type, rows, provider, dataset)

        record = {
            "provider":          provider,
            "dataset":           dataset,
            "status":            status,
            "rows":              int(rows),
            "latency_ms":        round(float(latency_ms), 1),
            "retry_attempts":    int(retry_attempts),
            "cache_hit":         bool(cache_hit),
            "fallback_used":     bool(fallback_used),
            "error_type":        error_type or "",
            "warning":           warning or "",
            "recommended_action": recommended_action,
            "recorded_at":       datetime.now(timezone.utc).isoformat(),
        }
        self._records.append(record)
        return record

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summarize(self) -> dict:
        """Return a summary dict of all recorded results."""
        if not self._records:
            return {
                "total_providers_checked": 0,
                "total_datasets_checked":  0,
                "ok_count":                0,
                "partial_count":           0,
                "failed_count":            0,
                "cache_hits":              0,
                "retry_total":             0,
                "warnings":                [],
                "records":                 [],
                "read_only":               True,
                "no_real_orders":          True,
            }

        providers  = {r["provider"]  for r in self._records}
        datasets   = {r["dataset"]   for r in self._records}
        ok_n       = sum(1 for r in self._records if r["status"] == "OK")
        partial_n  = sum(1 for r in self._records if r["status"] == "PARTIAL")
        failed_n   = sum(1 for r in self._records if r["status"] in ("FAILED", "ERROR"))
        cache_hits = sum(1 for r in self._records if r["cache_hit"])
        retry_tot  = sum(r["retry_attempts"] - 1 for r in self._records)
        warnings   = [r["warning"] for r in self._records if r["warning"]]

        return {
            "total_providers_checked": len(providers),
            "total_datasets_checked":  len(datasets),
            "ok_count":                ok_n,
            "partial_count":           partial_n,
            "failed_count":            failed_n,
            "cache_hits":              cache_hits,
            "retry_total":             retry_tot,
            "warnings":                warnings[:20],
            "records":                 list(self._records),
            "read_only":               True,
            "no_real_orders":          True,
        }

    def to_dataframe(self):
        """Convert records to a pandas DataFrame. Returns empty DataFrame if pandas not available."""
        try:
            import pandas as pd
            if not self._records:
                return pd.DataFrame(columns=[
                    "provider", "dataset", "status", "rows", "latency_ms",
                    "retry_attempts", "cache_hit", "fallback_used",
                    "error_type", "warning", "recommended_action",
                ])
            return pd.DataFrame(self._records)
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_message(msg: str) -> str:
        """Remove token-like patterns from messages."""
        import re
        # Remove anything that looks like a token (long alphanumeric string after =)
        msg = re.sub(r'(token|key|password|secret)=[^\s&"\']*', r'\1=<redacted>', msg, flags=re.IGNORECASE)
        return msg[:300]

    @staticmethod
    def _recommend(
        status:    str,
        error_type: str,
        rows:      int,
        provider:  str,
        dataset:   str,
    ) -> str:
        if status == "OK" and rows > 0:
            return ""
        if error_type in ("AUTH_ERROR", "RATE_LIMIT"):
            if provider == "finmind":
                return "Check FINMIND_TOKEN in .env — run: python main.py api-token-check"
            return "Check API token configuration"
        if error_type == "SCHEMA_CHANGED":
            return f"Schema changed for {provider}/{dataset} — check provider parser"
        if error_type in ("TIMEOUT", "NETWORK"):
            return "Check internet connection; retry later"
        if status in ("FAILED", "ERROR") and rows == 0:
            return f"Run: python main.py provider-auto-fetch --dataset {dataset}"
        if status == "PARTIAL":
            return "Partial data — check provider logs for details"
        return ""
