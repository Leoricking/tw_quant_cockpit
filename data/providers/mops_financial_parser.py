"""
data/providers/mops_financial_parser.py - MOPS financial statement & announcement date parser (v0.4.1).

Handles estimated announcement dates, timing quality classification,
and financial statement normalization without crashing.

[!] Read Only. No Real Orders.
[!] announcement_date_is_estimated must be preserved.
[!] timing_quality must be explicitly output.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Timing quality constants
TIMING_ACTUAL         = "ACTUAL"
TIMING_ESTIMATED      = "ESTIMATED"
TIMING_DEADLINE       = "DEADLINE"
TIMING_UNKNOWN        = "UNKNOWN"

# Schema status
SCHEMA_OK             = "OK"
SCHEMA_PARTIAL        = "PARTIAL"
SCHEMA_CHANGED        = "SCHEMA_CHANGED"


# Taiwan statutory announcement deadlines (days after quarter end)
# Q1 ends 3/31: deadline ~5/15 (45 days)
# Q2 ends 6/30: deadline ~8/14 (45 days)
# Q3 ends 9/30: deadline ~11/14 (45 days)
# Q4 ends 12/31: deadline ~3/31 next year (90 days)
_QUARTER_DEADLINE_DAYS: Dict[str, int] = {
    "Q1": 45,
    "Q2": 45,
    "Q3": 45,
    "Q4": 90,
}

# Quarter end months
_QUARTER_END_MONTH: Dict[str, int] = {
    "Q1": 3,
    "Q2": 6,
    "Q3": 9,
    "Q4": 12,
}


class MOPSFinancialParser:
    """
    MOPS financial statement and announcement date parser.

    Features:
        - If actual announcement date is unavailable, uses estimated deadline
          but marks announcement_date_is_estimated=True
        - Classifies timing quality: ACTUAL / ESTIMATED / DEADLINE / UNKNOWN
        - Never crashes on bad input
        - Schema change returns PARTIAL / SCHEMA_CHANGED with clear message
    """

    read_only      = True
    no_real_orders = True

    # Standard financial statement columns
    _FIN_STMT_COLS = [
        "date", "symbol", "year", "quarter",
        "eps", "gross_margin", "operating_margin", "net_income",
        "announcement_date", "announcement_date_source",
        "announcement_date_is_estimated", "timing_quality",
        "source",
    ]

    _FIN_ALIASES: Dict[str, List[str]] = {
        "date":             ["date", "日期", "report_date"],
        "symbol":           ["symbol", "代號", "StockNo", "stock_id"],
        "year":             ["year", "年度", "fiscal_year"],
        "quarter":          ["quarter", "季別", "fiscal_quarter"],
        "eps":              ["eps", "EPS", "每股盈餘", "diluted_eps"],
        "gross_margin":     ["gross_margin", "毛利率", "GrossMarginRatio"],
        "operating_margin": ["operating_margin", "營業利益率", "OperatingMarginRatio"],
        "net_income":       ["net_income", "稅後淨利", "NetIncome"],
        "announcement_date": ["announcement_date", "公告日期", "AnnouncementDate"],
    }

    # ------------------------------------------------------------------
    # Parse methods
    # ------------------------------------------------------------------

    def parse_financial_statement(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[Any], str]:
        """
        Parse MOPS financial statement response.
        Returns (DataFrame_or_None, schema_status).
        Preserves announcement_date_is_estimated column.
        """
        try:
            import pandas as pd

            if data is None:
                return None, SCHEMA_CHANGED
            if isinstance(data, list):
                if not data:
                    return None, SCHEMA_CHANGED
                df = pd.DataFrame(data)
            elif hasattr(data, "columns"):
                df = data.copy()
            else:
                return None, SCHEMA_CHANGED

            if df.empty:
                return None, SCHEMA_CHANGED

            # Map columns
            col_map = {}
            for std, alias_list in self._FIN_ALIASES.items():
                for alias in alias_list:
                    if alias in df.columns:
                        col_map[alias] = std
                        break
            if col_map:
                df = df.rename(columns=col_map)

            # Add required columns if missing
            for col in self._FIN_STMT_COLS:
                if col not in df.columns:
                    df[col] = None

            # Add symbol if provided
            if symbol and "symbol" in df.columns:
                df["symbol"] = df["symbol"].fillna(symbol) if hasattr(df["symbol"], "fillna") else symbol

            # Normalize quarter
            if "quarter" in df.columns:
                df["quarter"] = df["quarter"].apply(
                    lambda x: self.normalize_quarter(str(x)) if x is not None else None
                )

            # Process announcement dates
            df = self._process_announcement_dates(df)

            # Validate
            ok, missing = self._validate(df, ["date", "symbol"])
            schema_status = SCHEMA_OK if ok else SCHEMA_CHANGED
            if ok and any(c not in df.columns for c in ["eps", "gross_margin"]):
                schema_status = SCHEMA_PARTIAL

            return df, schema_status

        except Exception as exc:
            logger.warning("MOPSFinancialParser.parse_financial_statement: %s", exc)
            return None, SCHEMA_CHANGED

    def parse_announcement_date(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[str], str]:
        """
        Parse MOPS announcement date for a symbol/period.
        Returns (date_string_or_None, timing_quality).
        """
        try:
            if data is None:
                return None, TIMING_UNKNOWN

            if isinstance(data, dict):
                date_val = data.get("announcement_date") or data.get("AnnouncementDate")
                if date_val:
                    return str(date_val)[:10], TIMING_ACTUAL

            if isinstance(data, str) and len(data) >= 8:
                return data[:10], TIMING_ACTUAL

            return None, TIMING_UNKNOWN

        except Exception as exc:
            logger.debug("MOPSFinancialParser.parse_announcement_date: %s", exc)
            return None, TIMING_UNKNOWN

    def estimate_announcement_date(
        self,
        year: int,
        quarter: str,
    ) -> Tuple[str, str]:
        """
        Estimate announcement deadline for a year/quarter.
        Returns (estimated_date_YYYY-MM-DD, timing_quality=ESTIMATED).

        Uses statutory deadline: Q1/Q2/Q3 = 45 days, Q4 = 90 days after quarter end.
        """
        quarter = self.normalize_quarter(str(quarter))
        if quarter not in _QUARTER_END_MONTH:
            return f"{year}-12-31", TIMING_UNKNOWN

        end_month = _QUARTER_END_MONTH[quarter]
        deadline_days = _QUARTER_DEADLINE_DAYS[quarter]

        # Quarter end date
        if end_month == 12:
            end_date = datetime(year, 12, 31)
        else:
            end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)

        deadline = end_date + timedelta(days=deadline_days)
        return deadline.strftime("%Y-%m-%d"), TIMING_ESTIMATED

    def classify_timing_quality(
        self,
        announcement_date: Optional[str],
        quarter_end_date:  Optional[str],
        is_estimated:      bool = True,
    ) -> str:
        """
        Classify timing quality for a given announcement date.

        Returns one of: ACTUAL, ESTIMATED, DEADLINE, UNKNOWN.
        """
        if not announcement_date:
            return TIMING_UNKNOWN
        if not is_estimated:
            return TIMING_ACTUAL
        if quarter_end_date:
            try:
                ann_dt  = datetime.strptime(announcement_date[:10], "%Y-%m-%d")
                qend_dt = datetime.strptime(quarter_end_date[:10], "%Y-%m-%d")
                days    = (ann_dt - qend_dt).days
                # Within 45 days = typical announcement; beyond = deadline fallback
                if days <= 50:
                    return TIMING_ESTIMATED
                return TIMING_DEADLINE
            except Exception:
                pass
        return TIMING_ESTIMATED

    def normalize_quarter(self, quarter_str: str) -> str:
        """
        Normalize quarter string to Q1/Q2/Q3/Q4.
        Handles "1Q", "Q1", "季1", "第一季", "1" etc.
        """
        if not quarter_str:
            return ""
        s = str(quarter_str).strip().upper()

        # Already correct
        if s in ("Q1", "Q2", "Q3", "Q4"):
            return s

        # Numeric: "1", "2", "3", "4"
        m = re.match(r'^[QS]?(\d)$', s)
        if m:
            return f"Q{m.group(1)}"

        # Chinese: 第一季, 第二季...
        cn_map = {"一": "1", "二": "2", "三": "3", "四": "4"}
        for cn, num in cn_map.items():
            if cn in s:
                return f"Q{num}"

        # Number followed by Q: "1Q"
        m = re.match(r'^(\d)Q', s)
        if m:
            return f"Q{m.group(1)}"

        return s  # return as-is

    def validate_financial_columns(self, df: Any) -> Tuple[bool, List[str]]:
        """Check for core financial columns. Returns (ok, missing)."""
        return self._validate(df, ["date", "symbol", "eps"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _process_announcement_dates(self, df: Any) -> Any:
        """
        Ensure announcement_date_is_estimated is set.
        If announcement_date is missing for a row, estimate from year/quarter.
        """
        try:
            import pandas as pd

            for idx, row in df.iterrows():
                ann_date = row.get("announcement_date")
                is_estimated = row.get("announcement_date_is_estimated")
                year    = row.get("year")
                quarter = row.get("quarter")

                if ann_date and str(ann_date).strip() not in ("", "None", "nan"):
                    # Actual date found
                    df.at[idx, "announcement_date_is_estimated"] = False if is_estimated is None else is_estimated
                    df.at[idx, "announcement_date_source"] = row.get("announcement_date_source", "actual")
                    df.at[idx, "timing_quality"] = TIMING_ACTUAL
                else:
                    # Estimate from year + quarter
                    if year and quarter:
                        try:
                            yr = int(str(year).strip())
                            qtr = self.normalize_quarter(str(quarter))
                            est_date, tq = self.estimate_announcement_date(yr, qtr)
                            df.at[idx, "announcement_date"]            = est_date
                            df.at[idx, "announcement_date_is_estimated"] = True
                            df.at[idx, "announcement_date_source"]     = "estimated_deadline"
                            df.at[idx, "timing_quality"]               = tq
                        except Exception:
                            df.at[idx, "announcement_date_is_estimated"] = True
                            df.at[idx, "timing_quality"] = TIMING_UNKNOWN
                    else:
                        df.at[idx, "announcement_date_is_estimated"] = True
                        df.at[idx, "timing_quality"] = TIMING_UNKNOWN

        except Exception as exc:
            logger.debug("MOPSFinancialParser._process_announcement_dates: %s", exc)

        return df

    @staticmethod
    def _validate(df: Any, required: List[str]) -> Tuple[bool, List[str]]:
        try:
            cols    = list(df.columns)
            missing = [c for c in required if c not in cols]
            return len(missing) == 0, missing
        except Exception:
            return False, list(required)
