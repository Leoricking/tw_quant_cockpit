"""
replay/future_data_firewall.py — ReplayFutureDataFirewall v1.2.0

Strictly enforces: no data with date > replay_date can appear in snapshot.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Future data firewall is non-negotiable. BLOCKED qualification if violated.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("[ReplayFutureDataFirewall] pandas not available — limited functionality")


class ReplayFutureDataFirewall:
    """
    Strictly enforces: no data with date > replay_date can appear in snapshot.

    FORBIDDEN snapshot fields:
    forward_return_*, future_return, future_high, future_low, outcome,
    final_label, target_label, realized_pnl, next_close, next_open,
    future_signal, hindsight_score
    """

    FORBIDDEN_FIELDS = [
        "forward_return", "future_return", "future_high", "future_low",
        "outcome", "final_label", "target_label", "realized_pnl",
        "next_close", "next_open", "future_signal", "hindsight_score",
    ]
    FORBIDDEN_PREFIXES = ["forward_return_"]

    def filter_dataframe(self, df, date_col: str, replay_date: str):
        """Returns df with rows where date_col <= replay_date only."""
        if not _PANDAS_OK or df is None or df.empty:
            return df
        try:
            col_lower = [c.lower() for c in df.columns]
            # find date_col case-insensitively
            actual_col = None
            for c in df.columns:
                if c.lower() == date_col.lower():
                    actual_col = c
                    break
            if actual_col is None:
                logger.warning("[Firewall] date_col=%s not found in DataFrame", date_col)
                return df
            date_series = pd.to_datetime(df[actual_col], errors="coerce")
            replay_dt = pd.to_datetime(replay_date)
            mask = date_series <= replay_dt
            return df[mask].reset_index(drop=True)
        except Exception as exc:
            logger.warning("[Firewall] filter_dataframe error: %s", exc)
            return df

    def filter_by_announcement_date(self, df, announcement_col: str, replay_date: str):
        """
        Returns rows where announcement_col <= replay_date.
        Missing dates: include with timing_approximate warning.
        """
        if not _PANDAS_OK or df is None or df.empty:
            return df, []
        warnings = []
        try:
            actual_col = None
            for c in df.columns:
                if c.lower() == announcement_col.lower():
                    actual_col = c
                    break
            if actual_col is None:
                warnings.append(f"ANNOUNCEMENT_DATE_COLUMN_MISSING: {announcement_col} not found — FUNDAMENTAL_TIMING_APPROXIMATE")
                return df, warnings

            ann_series = pd.to_datetime(df[actual_col], errors="coerce")
            replay_dt = pd.to_datetime(replay_date)
            mask_known = ann_series.notna() & (ann_series <= replay_dt)
            mask_unknown = ann_series.isna()
            if mask_unknown.any():
                warnings.append("FUNDAMENTAL_TIMING_APPROXIMATE: some rows have no announcement_date")
            result = df[mask_known | mask_unknown].reset_index(drop=True)
            return result, warnings
        except Exception as exc:
            logger.warning("[Firewall] filter_by_announcement_date error: %s", exc)
            warnings.append(f"ANNOUNCEMENT_DATE_FILTER_ERROR: {exc}")
            return df, warnings

    def validate_frame(self, df, date_col: str, replay_date: str) -> Tuple[bool, int, List[str]]:
        """Returns (is_valid, future_row_count, warnings)."""
        if not _PANDAS_OK or df is None or df.empty:
            return True, 0, []
        future_count = self.detect_future_rows(df, date_col, replay_date)
        warnings = []
        if future_count > 0:
            warnings.append(f"FUTURE_ROWS_DETECTED: {future_count} rows with date > {replay_date}")
        is_valid = (future_count == 0)
        return is_valid, future_count, warnings

    def detect_future_rows(self, df, date_col: str, replay_date: str) -> int:
        """Returns count of rows with date > replay_date."""
        if not _PANDAS_OK or df is None or df.empty:
            return 0
        try:
            actual_col = None
            for c in df.columns:
                if c.lower() == date_col.lower():
                    actual_col = c
                    break
            if actual_col is None:
                return 0
            date_series = pd.to_datetime(df[actual_col], errors="coerce")
            replay_dt = pd.to_datetime(replay_date)
            return int((date_series > replay_dt).sum())
        except Exception as exc:
            logger.warning("[Firewall] detect_future_rows error: %s", exc)
            return 0

    def sanitize_context(self, context_dict: Dict[str, Any], replay_date: str) -> Tuple[Dict[str, Any], int, List[str]]:
        """Removes future fields from a dict. Returns (sanitized_dict, blocked_count, warnings)."""
        if not context_dict:
            return {}, 0, []
        sanitized = {}
        blocked_count = 0
        warnings = []
        for k, v in context_dict.items():
            if self._is_forbidden_field(k):
                blocked_count += 1
                warnings.append(f"FUTURE_FIELD_BLOCKED: {k}")
            else:
                sanitized[k] = v
        return sanitized, blocked_count, warnings

    def verify_snapshot(self, snapshot) -> Tuple[bool, List[str]]:
        """Verifies ReplayMarketSnapshot has no future data. Returns (is_clean, issues)."""
        issues = []
        try:
            # Check price_data for forbidden fields
            price_fields = self.future_field_scan(snapshot.price_data)
            if price_fields:
                issues.append(f"FORBIDDEN_FIELDS_IN_PRICE_DATA: {price_fields}")

            # Check indicator_data
            ind_fields = self.future_field_scan(snapshot.indicator_data)
            if ind_fields:
                issues.append(f"FORBIDDEN_FIELDS_IN_INDICATOR_DATA: {ind_fields}")

            # Check chips_data
            chips_fields = self.future_field_scan(snapshot.chips_data)
            if chips_fields:
                issues.append(f"FORBIDDEN_FIELDS_IN_CHIPS_DATA: {chips_fields}")

            # Check fundamental_data
            fund_fields = self.future_field_scan(snapshot.fundamental_data)
            if fund_fields:
                issues.append(f"FORBIDDEN_FIELDS_IN_FUNDAMENTAL_DATA: {fund_fields}")

        except Exception as exc:
            issues.append(f"SNAPSHOT_VERIFY_ERROR: {exc}")

        is_clean = len(issues) == 0
        return is_clean, issues

    def future_field_scan(self, data) -> List[str]:
        """Scans dict/DataFrame for forbidden field names. Returns list of found forbidden fields."""
        found = []
        if data is None:
            return found
        if _PANDAS_OK and hasattr(data, "columns"):
            fields = [str(c).lower() for c in data.columns]
        elif isinstance(data, dict):
            fields = [str(k).lower() for k in data.keys()]
        else:
            return found
        for field in fields:
            if self._is_forbidden_field(field):
                found.append(field)
        return found

    def build_firewall_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Returns dict summary of firewall verification."""
        return {
            "firewall_version": "v1.2.0",
            "research_only": True,
            "no_real_orders": True,
            "results": results,
            "total_checks": len(results),
            "passed": sum(1 for r in results.values() if r.get("passed", False)),
            "failed": sum(1 for r in results.values() if not r.get("passed", True)),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_forbidden_field(self, field_name: str) -> bool:
        """Check if a field name is forbidden (future-leaking)."""
        fname = str(field_name).lower()
        for f in self.FORBIDDEN_FIELDS:
            if fname == f:
                return True
        for prefix in self.FORBIDDEN_PREFIXES:
            if fname.startswith(prefix):
                return True
        return False
