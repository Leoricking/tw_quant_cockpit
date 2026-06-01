"""
data/providers/data_lineage.py - Data source lineage tracking (v0.4.1).

Records fetch/write operations for each dataset to enable auditing and
reproducibility analysis.

[!] Read Only. No Real Orders.
[!] Never records token or account credentials.
[!] Output written to data/backtest_results/ — not committed.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DataLineageTracker:
    """
    Data source lineage tracker.

    Parameters
    ----------
    lineage_root : Directory to write lineage files (default: data/backtest_results)

    Lineage record fields:
        lineage_id, dataset, provider, source_url_or_endpoint_masked,
        params_hash, fetched_at, written_at, rows_fetched, rows_written,
        schema_status, cache_status, retry_attempts, warning, output_path,
        data_hash (optional)

    Safety:
        - Never records full token or credentials.
        - URL/endpoint is masked of any query params containing token.
    """

    read_only      = True
    no_real_orders = True

    def __init__(self, lineage_root: str = "data/backtest_results"):
        if os.path.isabs(lineage_root):
            self._root = lineage_root
        else:
            self._root = os.path.join(_BASE_DIR, lineage_root)
        os.makedirs(self._root, exist_ok=True)
        self._records: List[dict] = []

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_fetch(
        self,
        dataset:         str,
        provider:        str,
        params:          Any,
        result_summary:  dict,
    ) -> dict:
        """
        Record a data fetch operation.

        Parameters
        ----------
        dataset         : Dataset name (e.g. "daily_price", "monthly_revenue")
        provider        : Provider name (e.g. "finmind", "twse")
        params          : Fetch parameters (token fields are excluded from hash)
        result_summary  : Dict with rows_fetched, schema_status, cache_status,
                         retry_attempts, warning, source_url

        Returns the lineage record dict.
        """
        lineage_id    = f"LIN-{uuid.uuid4().hex[:12].upper()}"
        fetched_at    = datetime.utcnow().isoformat()
        params_hash   = self._hash_params(params)
        source_masked = self._mask_url(result_summary.get("source_url", ""))

        record = {
            "lineage_id":                lineage_id,
            "dataset":                   dataset,
            "provider":                  provider,
            "source_url_or_endpoint_masked": source_masked,
            "params_hash":               params_hash,
            "fetched_at":                fetched_at,
            "written_at":                None,
            "rows_fetched":              result_summary.get("rows_fetched", 0),
            "rows_written":              result_summary.get("rows_written", 0),
            "schema_status":             result_summary.get("schema_status", "OK"),
            "cache_status":              result_summary.get("cache_status", "MISS"),
            "retry_attempts":            result_summary.get("retry_attempts", 1),
            "warning":                   result_summary.get("warning", ""),
            "output_path":               result_summary.get("output_path", ""),
            "data_hash":                 result_summary.get("data_hash", None),
            "read_only":                 True,
            "no_real_orders":            True,
        }
        self._records.append(record)
        return record

    def record_write(
        self,
        dataset:         str,
        output_path:     str,
        source_summary:  dict,
    ) -> dict:
        """
        Record a data write operation. Updates the most recent fetch record
        for the same dataset if found, otherwise creates a standalone write record.
        """
        written_at = datetime.utcnow().isoformat()

        # Try to update the most recent fetch record for this dataset
        for rec in reversed(self._records):
            if rec.get("dataset") == dataset and rec.get("written_at") is None:
                rec["written_at"]   = written_at
                rec["output_path"]  = output_path
                rec["rows_written"] = source_summary.get("rows_written", rec.get("rows_written", 0))
                return rec

        # Standalone write record
        record = {
            "lineage_id":                f"LIN-W-{uuid.uuid4().hex[:12].upper()}",
            "dataset":                   dataset,
            "provider":                  source_summary.get("provider", "unknown"),
            "source_url_or_endpoint_masked": "",
            "params_hash":               "",
            "fetched_at":                "",
            "written_at":                written_at,
            "rows_fetched":              source_summary.get("rows_fetched", 0),
            "rows_written":              source_summary.get("rows_written", 0),
            "schema_status":             source_summary.get("schema_status", "OK"),
            "cache_status":              source_summary.get("cache_status", "MISS"),
            "retry_attempts":            source_summary.get("retry_attempts", 1),
            "warning":                   source_summary.get("warning", ""),
            "output_path":               output_path,
            "data_hash":                 source_summary.get("data_hash", None),
            "read_only":                 True,
            "no_real_orders":            True,
        }
        self._records.append(record)
        return record

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def build_lineage_for_dataset(self, dataset: str) -> List[dict]:
        """Return all lineage records for a specific dataset."""
        return [r for r in self._records if r.get("dataset") == dataset]

    def export_lineage_summary(self) -> dict:
        """Export all lineage records as a summary."""
        return {
            "generated_at":  datetime.utcnow().isoformat(),
            "total_records": len(self._records),
            "records":       list(self._records),
            "datasets":      list({r.get("dataset", "") for r in self._records}),
            "providers":     list({r.get("provider", "") for r in self._records}),
            "read_only":     True,
            "no_real_orders": True,
        }

    def save_lineage_csv(self) -> Optional[str]:
        """Save lineage records to a CSV file in lineage_root. Returns path or None."""
        if not self._records:
            return None
        try:
            import csv
            today = datetime.now().strftime("%Y-%m-%d")
            path  = os.path.join(self._root, f"api_lineage_{today}.csv")
            fieldnames = [
                "lineage_id", "dataset", "provider",
                "source_url_or_endpoint_masked", "params_hash",
                "fetched_at", "written_at", "rows_fetched", "rows_written",
                "schema_status", "cache_status", "retry_attempts",
                "warning", "output_path",
            ]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(self._records)
            return path
        except Exception as exc:
            logger.debug("DataLineageTracker.save_lineage_csv: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_params(params: Any) -> str:
        """Hash params, excluding token-like fields."""
        if isinstance(params, dict):
            safe = {
                k: v for k, v in params.items()
                if not any(kw in str(k).lower() for kw in ("token", "password", "secret", "key", "auth"))
            }
        else:
            safe = str(params)
        raw = json.dumps(safe, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _mask_url(url: str) -> str:
        """Remove token query params from URL."""
        if not url:
            return ""
        # Remove ?token=... and &token=... patterns
        import re
        masked = re.sub(r'([?&])(token|key|password|secret|auth)=[^&]*', r'\1\2=<redacted>', url, flags=re.IGNORECASE)
        return masked
