"""
data/providers/twse_tpex_parser.py - TWSE / TPEx response parser hardening (v0.4.1).

Handles schema drift, numeric normalization, and date format variations
without crashing. Returns PARTIAL / SCHEMA_CHANGED status on anomalies.

[!] Read Only. No Real Orders.
[!] Does not pretend success on schema change.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Schema status constants
SCHEMA_OK            = "OK"
SCHEMA_PARTIAL       = "PARTIAL"
SCHEMA_CHANGED       = "SCHEMA_CHANGED"
SCHEMA_EMPTY         = "EMPTY"


class TWSETPEXParser:
    """
    TWSE / TPEx response parser with schema hardening.

    Features:
        - Handles renamed or missing columns without crashing
        - Converts comma-formatted numbers (e.g. "1,234,567")
        - Handles both ROC (民國) and Western (西元) year formats
        - Returns PARTIAL / SCHEMA_CHANGED status on anomalies
        - Never pretends success on bad data
    """

    # Standard output column sets
    _DAILY_PRICE_COLS = ["date", "symbol", "open", "high", "low", "close", "volume"]
    _MONTHLY_REV_COLS = ["date", "symbol", "revenue", "revenue_mom", "revenue_yoy"]
    _INSTITUTIONAL_COLS = ["date", "symbol", "foreign_net_buy", "trust_net_buy", "dealer_net_buy"]
    _MARGIN_COLS = ["date", "symbol", "margin_balance", "margin_change", "short_balance", "short_change"]

    # Alternative column name mappings (TWSE / TPEx use inconsistent naming)
    _DAILY_ALIASES: Dict[str, List[str]] = {
        "date":   ["日期", "Date", "date"],
        "symbol": ["代號", "StockNo", "Code", "symbol", "stock_code"],
        "open":   ["開盤價", "Open", "open", "開盤"],
        "high":   ["最高價", "High", "high", "最高"],
        "low":    ["最低價", "Low",  "low",  "最低"],
        "close":  ["收盤價", "Close", "close", "收盤"],
        "volume": ["成交量", "TradeVolume", "volume", "成交股數"],
    }
    _REVENUE_ALIASES: Dict[str, List[str]] = {
        "date":        ["日期", "Date", "date", "年月"],
        "symbol":      ["代號", "StockNo", "Code", "symbol"],
        "revenue":     ["當月營收", "Revenue", "revenue", "營業收入"],
        "revenue_mom": ["上月比較增減(%)", "MoM", "revenue_mom"],
        "revenue_yoy": ["去年同月增減(%)", "YoY", "revenue_yoy"],
    }
    _INSTITUTIONAL_ALIASES: Dict[str, List[str]] = {
        "date":            ["日期", "Date", "date"],
        "symbol":          ["代號", "StockNo", "Code", "symbol"],
        "foreign_net_buy": ["外資買賣超", "Foreign_Net", "foreign_net_buy"],
        "trust_net_buy":   ["投信買賣超", "Investment_Trust_Net", "trust_net_buy"],
        "dealer_net_buy":  ["自營商買賣超", "Dealer_Net", "dealer_net_buy"],
    }
    _MARGIN_ALIASES: Dict[str, List[str]] = {
        "date":           ["日期", "Date", "date"],
        "symbol":         ["代號", "StockNo", "Code", "symbol"],
        "margin_balance": ["融資餘額", "MarginPurchase_Balance", "margin_balance"],
        "margin_change":  ["融資增減", "MarginPurchase_Change", "margin_change"],
        "short_balance":  ["融券餘額", "ShortSale_Balance", "short_balance"],
        "short_change":   ["融券增減", "ShortSale_Change", "short_change"],
    }

    # ------------------------------------------------------------------
    # Parse methods
    # ------------------------------------------------------------------

    def parse_daily_price_response(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[Any], str]:
        """
        Parse TWSE/TPEx daily price response.
        Returns (DataFrame_or_None, schema_status).
        """
        return self._parse_generic(
            data, self._DAILY_PRICE_COLS, self._DAILY_ALIASES, symbol=symbol, label="daily_price"
        )

    def parse_monthly_revenue_response(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[Any], str]:
        """Parse monthly revenue response."""
        return self._parse_generic(
            data, self._MONTHLY_REV_COLS, self._REVENUE_ALIASES, symbol=symbol, label="monthly_revenue"
        )

    def parse_institutional_response(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[Any], str]:
        """Parse institutional buy/sell response."""
        return self._parse_generic(
            data, self._INSTITUTIONAL_COLS, self._INSTITUTIONAL_ALIASES, symbol=symbol, label="institutional"
        )

    def parse_margin_response(
        self,
        data: Any,
        symbol: Optional[str] = None,
    ) -> Tuple[Optional[Any], str]:
        """Parse margin/short-sell response."""
        return self._parse_generic(
            data, self._MARGIN_COLS, self._MARGIN_ALIASES, symbol=symbol, label="margin"
        )

    # ------------------------------------------------------------------
    # Normalizers
    # ------------------------------------------------------------------

    def normalize_numeric_columns(self, df: Any, columns: List[str]) -> Any:
        """
        Convert comma-formatted strings to float in specified columns.
        e.g. "1,234,567" -> 1234567.0
        Non-convertible values become None (not NaN to avoid dependencies).
        """
        try:
            import pandas as pd
            df = df.copy()
            for col in columns:
                if col not in df.columns:
                    continue
                df[col] = df[col].apply(self._parse_numeric)
        except ImportError:
            pass
        return df

    @staticmethod
    def _parse_numeric(val: Any) -> Optional[float]:
        if val is None:
            return None
        s = str(val).strip().replace(",", "").replace(" ", "")
        if not s or s in ("-", "--", "N/A", "na", "NA"):
            return None
        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def normalize_date(self, date_str: str) -> str:
        """
        Normalize date string to YYYY-MM-DD.
        Handles ROC year (民國) format like "112/05/01" → "2023-05-01".
        Handles Western format "2023/05/01", "20230501", etc.
        """
        if not date_str:
            return ""
        s = str(date_str).strip()

        # ROC year: digits/digits/digits where first part <= 120
        m = re.match(r'^(\d{2,3})/(\d{1,2})/(\d{1,2})$', s)
        if m:
            year_roc = int(m.group(1))
            if year_roc <= 120:
                year = year_roc + 1911
            else:
                year = year_roc  # already Western
            month = int(m.group(2))
            day   = int(m.group(3))
            return f"{year:04d}-{month:02d}-{day:02d}"

        # Western date: YYYY/MM/DD
        m = re.match(r'^(\d{4})[/-](\d{1,2})[/-](\d{1,2})$', s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        # Compact: YYYYMMDD
        m = re.match(r'^(\d{4})(\d{2})(\d{2})$', s)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

        # ROC compact: YYYMMDD (7 digits)
        m = re.match(r'^(\d{3})(\d{2})(\d{2})$', s)
        if m:
            year = int(m.group(1)) + 1911
            return f"{year}-{m.group(2)}-{m.group(3)}"

        return s  # return as-is — don't crash

    def validate_required_columns(
        self,
        df: Any,
        required: List[str],
    ) -> Tuple[bool, List[str]]:
        """
        Check that required columns are present.
        Returns (ok, missing_cols).
        """
        try:
            df_cols = list(df.columns)
        except Exception:
            return False, list(required)
        missing = [c for c in required if c not in df_cols]
        return len(missing) == 0, missing

    def handle_schema_change(self, missing_cols: List[str], dataset: str) -> dict:
        """
        Return a schema-change diagnostic dict.
        Does NOT crash or pretend success.
        """
        return {
            "schema_status":     SCHEMA_CHANGED,
            "missing_columns":   missing_cols,
            "dataset":           dataset,
            "warning":           f"Schema change detected in {dataset}: missing {missing_cols}",
            "recommended_action": "Check TWSE/TPEx API for column changes; update parser mappings.",
        }

    # ------------------------------------------------------------------
    # Internal generic parser
    # ------------------------------------------------------------------

    def _parse_generic(
        self,
        data:     Any,
        std_cols: List[str],
        aliases:  Dict[str, List[str]],
        symbol:   Optional[str],
        label:    str,
    ) -> Tuple[Optional[Any], str]:
        """
        Generic parse: normalize column names, validate, return (df, schema_status).
        """
        try:
            import pandas as pd

            # Accept list of dicts, DataFrame, or None
            if data is None:
                return None, SCHEMA_EMPTY
            if isinstance(data, list):
                if not data:
                    return None, SCHEMA_EMPTY
                df = pd.DataFrame(data)
            elif hasattr(data, "columns"):
                df = data.copy()
            else:
                return None, SCHEMA_EMPTY

            if df.empty:
                return None, SCHEMA_EMPTY

            # Map columns using aliases
            col_map = {}
            for std, alias_list in aliases.items():
                for alias in alias_list:
                    if alias in df.columns:
                        col_map[alias] = std
                        break
            if col_map:
                df = df.rename(columns=col_map)

            # Validate required columns
            required_core = [c for c in std_cols if c in ("date", "symbol")]
            ok, missing = self.validate_required_columns(df, required_core)
            if not ok:
                return df, SCHEMA_CHANGED

            # Normalize numeric columns (all except date, symbol)
            numeric_cols = [c for c in std_cols if c not in ("date", "symbol") and c in df.columns]
            df = self.normalize_numeric_columns(df, numeric_cols)

            # Normalize date column
            if "date" in df.columns:
                df["date"] = df["date"].apply(lambda x: self.normalize_date(str(x)) if x is not None else "")

            # Add symbol if provided and missing
            if symbol and "symbol" not in df.columns:
                df["symbol"] = symbol

            # Add missing std columns as None
            for col in std_cols:
                if col not in df.columns:
                    df[col] = None

            # Determine schema status
            expected = set(std_cols)
            present  = set(df.columns)
            if not expected.issubset(present):
                schema_status = SCHEMA_PARTIAL
            else:
                schema_status = SCHEMA_OK

            return df, schema_status

        except Exception as exc:
            logger.warning("TWSETPEXParser._parse_generic(%s): %s", label, exc)
            return None, SCHEMA_CHANGED
