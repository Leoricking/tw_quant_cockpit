"""
data/providers/mops/normalizer_v142.py — MOPS data normalizer v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Handles: ROC year conversion, unit normalization, field mapping, currency normalization.
Missing values always -> None, never 0 or empty string.
"""
from __future__ import annotations

import re
from typing import Any, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_UNIT_MAP = {
    "千元": "TWD_THOUSAND",
    "千": "TWD_THOUSAND",
    "元": "TWD",
    "萬元": "TWD_TEN_THOUSAND",
    "萬": "TWD_TEN_THOUSAND",
    "億元": "TWD_HUNDRED_MILLION",
    "億": "TWD_HUNDRED_MILLION",
    "thousand": "TWD_THOUSAND",
    "TWD": "TWD",
    "NTD": "TWD",
}

_MARKET_MAP = {
    "上市": "TWSE",
    "TWSE": "TWSE",
    "TSE": "TWSE",
    "上櫃": "TPEx",
    "OTC": "TPEx",
    "TPEx": "TPEx",
    "興櫃": "EMERGING",
    "EMERGING": "EMERGING",
}

_PERIOD_MAP = {
    "Q1": "Q1", "第一季": "Q1", "1Q": "Q1",
    "Q2": "Q2", "第二季": "Q2", "2Q": "Q2",
    "Q3": "Q3", "第三季": "Q3", "3Q": "Q3",
    "Q4": "Q4", "第四季": "Q4", "4Q": "Q4",
    "ANNUAL": "ANNUAL", "年度": "ANNUAL", "全年": "ANNUAL",
    "MONTHLY": "MONTHLY", "月": "MONTHLY",
}


class MOPSNormalizer:
    """Normalize MOPS data: units, markets, periods, symbols."""

    def normalize_unit(self, raw_unit: Any) -> str:
        """Normalize currency unit string."""
        if raw_unit is None:
            return "TWD_THOUSAND"  # default for financial statements
        s = str(raw_unit).strip()
        return _UNIT_MAP.get(s, s if s else "TWD_THOUSAND")

    def normalize_market(self, raw_market: Any) -> Optional[str]:
        """Normalize market identifier."""
        if raw_market is None:
            return None
        s = str(raw_market).strip()
        return _MARKET_MAP.get(s, s if s else None)

    def normalize_period(self, raw_period: Any) -> str:
        """Normalize fiscal period."""
        if raw_period is None:
            return "UNKNOWN"
        s = str(raw_period).strip()
        return _PERIOD_MAP.get(s, "UNKNOWN")

    def canonical_symbol(self, raw_symbol: Any) -> str:
        """Normalize a stock symbol (strip market prefix/suffix)."""
        if raw_symbol is None:
            return ""
        s = str(raw_symbol).strip()
        # Remove suffixes like .TW, .TWO
        s = re.sub(r"\.(TW|TWO|TWR)$", "", s, flags=re.IGNORECASE)
        # Remove market prefixes like TWSE:, TPEx:
        s = re.sub(r"^(TWSE|TPEx|OTC|TSE):", "", s, flags=re.IGNORECASE)
        return s.strip()

    def normalize_revenue_unit(self, unit_str: Any) -> str:
        """Normalize revenue unit (MOPS monthly revenue uses TWD_THOUSAND by default)."""
        if unit_str is None:
            return "TWD_THOUSAND"
        return self.normalize_unit(unit_str)

    def roc_year_to_ce(self, roc_year: Any) -> Optional[int]:
        """Convert ROC year integer to CE year."""
        if roc_year is None:
            return None
        try:
            return int(roc_year) + 1911
        except (ValueError, TypeError):
            return None

    def ce_year_to_roc(self, ce_year: Any) -> Optional[int]:
        """Convert CE year to ROC year."""
        if ce_year is None:
            return None
        try:
            return int(ce_year) - 1911
        except (ValueError, TypeError):
            return None

    def normalize_amount(self, raw: Any, unit: str = "TWD_THOUSAND") -> Optional[float]:
        """
        Normalize a financial amount. Returns None for missing, never 0 for missing.
        Removes commas, handles parentheses as negative.
        """
        if raw is None:
            return None
        s = str(raw).strip()
        if s in {"", "--", "---", "-", "N/A", "NA", "＊"}:
            return None
        # Parentheses = negative
        if s.startswith("(") and s.endswith(")"):
            s = "-" + s[1:-1]
        s = s.replace(",", "").replace("，", "")
        try:
            return float(s)
        except (ValueError, TypeError):
            return None
