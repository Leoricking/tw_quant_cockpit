"""
replay/strategy_point_in_time.py — Point-in-time verifier for strategy modules.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Verifies each module only uses data available at replay_date.
[!] Any field matching future patterns is BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class StrategyPointInTimeVerifier:
    """
    Verifies each strategy module only uses data available at replay_date.
    Future-looking fields are blocked. Source dates must be <= replay_date.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    FUTURE_FIELD_PATTERNS = [
        "forward_return", "future_", "hindsight_", "final_",
        "outcome_", "post_", "forward_", "ex_post_",
    ]

    def verify_module_input(
        self,
        module_name: str,
        context: Dict[str, Any],
        replay_date: str,
    ) -> Dict[str, Any]:
        """Verify context inputs do not contain future data."""
        blocked = []
        for key in context:
            if any(p in key.lower() for p in self.FUTURE_FIELD_PATTERNS):
                blocked.append(key)
        return {
            "module_name": module_name,
            "verified": len(blocked) == 0,
            "blocked_fields": blocked,
            "replay_date": replay_date,
        }

    def verify_module_output(
        self,
        module_name: str,
        result: Dict[str, Any],
        replay_date: str,
    ) -> Dict[str, Any]:
        """Check if module result contains any future-looking fields."""
        blocked = []
        for key, val in result.items():
            if any(p in key.lower() for p in self.FUTURE_FIELD_PATTERNS):
                blocked.append(key)
        return {
            "module_name": module_name,
            "verified": len(blocked) == 0,
            "blocked_fields": blocked,
            "replay_date": replay_date,
        }

    def verify_source_dates(
        self,
        source_dates: List[str],
        replay_date: str,
    ) -> Dict[str, Any]:
        """All source dates must be <= replay_date."""
        future_dates = []
        for sd in source_dates:
            if sd and sd > replay_date:
                future_dates.append(sd)
        return {
            "verified": len(future_dates) == 0,
            "future_dates": future_dates,
            "replay_date": replay_date,
        }

    def scan_future_fields(
        self, data: Dict[str, Any], replay_date: str
    ) -> Dict[str, Any]:
        """Scan any dict for future-looking field names."""
        blocked = []
        for key in data:
            if any(p in key.lower() for p in self.FUTURE_FIELD_PATTERNS):
                blocked.append(key)
        return {"verified": len(blocked) == 0, "blocked_fields": blocked}

    def verify_rolling_windows(
        self,
        module_name: str,
        context: Dict[str, Any],
        replay_date: str,
        window_days: int = 60,
    ) -> Dict[str, Any]:
        """Verify rolling window data only uses past data."""
        import pandas as pd
        df = context.get("df")
        if df is None or not isinstance(df, pd.DataFrame):
            return {"verified": True, "note": "no_df_to_check", "module_name": module_name}
        date_col = None
        for col in ["date", "Date", "trade_date"]:
            if col in df.columns:
                date_col = col
                break
        if date_col is None:
            return {"verified": True, "note": "no_date_column", "module_name": module_name}
        future_rows = df[df[date_col].astype(str) > replay_date]
        return {
            "module_name": module_name,
            "verified": len(future_rows) == 0,
            "future_rows": len(future_rows),
            "replay_date": replay_date,
        }

    def verify_announcement_timing(
        self,
        announcement_date: Optional[str],
        replay_date: str,
    ) -> Dict[str, Any]:
        """Announcement must have been published on or before replay_date."""
        if announcement_date is None:
            return {
                "verified": False,
                "timing_approximate": True,
                "note": "No announcement_date — timing is approximate",
            }
        verified = announcement_date <= replay_date
        return {
            "verified": verified,
            "timing_approximate": False,
            "announcement_date": announcement_date,
            "replay_date": replay_date,
        }

    def verify_sector_window(
        self,
        context: Dict[str, Any],
        replay_date: str,
    ) -> Dict[str, Any]:
        """Verify sector leader data is within valid past window."""
        leader_df = context.get("leader_df")
        if leader_df is None:
            return {"verified": True, "note": "no_leader_df"}
        import pandas as pd
        if not isinstance(leader_df, pd.DataFrame):
            return {"verified": True, "note": "leader_df_not_dataframe"}
        date_col = None
        for col in ["date", "Date", "trade_date"]:
            if col in leader_df.columns:
                date_col = col
                break
        if date_col is None:
            return {"verified": True, "note": "no_date_column_in_leader_df"}
        future_rows = leader_df[leader_df[date_col].astype(str) > replay_date]
        return {
            "verified": len(future_rows) == 0,
            "future_rows": len(future_rows),
            "replay_date": replay_date,
        }

    def verify_confirmation_date(
        self,
        signal_date: Optional[str],
        confirmation_date: Optional[str],
        replay_date: str,
    ) -> Dict[str, Any]:
        """
        For bottom reversal: signal_date must be confirmation_date
        if confirmation needed. Both must be <= replay_date.
        """
        issues = []
        if signal_date and signal_date > replay_date:
            issues.append(f"signal_date {signal_date} > replay_date {replay_date}")
        if confirmation_date and confirmation_date > replay_date:
            issues.append(f"confirmation_date {confirmation_date} > replay_date {replay_date}")
        return {
            "verified": len(issues) == 0,
            "issues": issues,
            "signal_date": signal_date,
            "confirmation_date": confirmation_date,
            "replay_date": replay_date,
        }

    def build_report(
        self,
        module_name: str,
        verified: bool,
        blocked_fields: List[str],
        timing_warnings: List[str],
    ) -> Dict[str, Any]:
        """Build a point-in-time verification report."""
        return {
            "module_name": module_name,
            "verified": verified,
            "blocked_fields": blocked_fields,
            "timing_warnings": timing_warnings,
            "status": "PASS" if verified else "FAIL",
        }
