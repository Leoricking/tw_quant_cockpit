"""
portfolio/enums_v150.py — Portfolio Enums v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import enum


class PortfolioStatus(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE_RESEARCH = "ACTIVE_RESEARCH"
    FROZEN = "FROZEN"
    ARCHIVED = "ARCHIVED"
    INVALID = "INVALID"


class AssetType(enum.Enum):
    COMMON_STOCK = "COMMON_STOCK"
    ETF = "ETF"
    CASH = "CASH"
    UNKNOWN = "UNKNOWN"
    # Forward-compatible stubs — UNSUPPORTED in v1.5.0
    OPTIONS = "OPTIONS"
    FUTURES = "FUTURES"
    MARGIN_SHORT = "MARGIN_SHORT"
    CRYPTO = "CRYPTO"
    BOND = "BOND"
    FX = "FX"

    _UNSUPPORTED = {
        "OPTIONS", "FUTURES", "MARGIN_SHORT", "CRYPTO", "BOND", "FX"
    }

    @classmethod
    def is_supported(cls, v: "AssetType") -> bool:
        return v.value not in cls._UNSUPPORTED.value  # type: ignore[attr-defined]


class TransactionType(enum.Enum):
    RESEARCH_BUY = "RESEARCH_BUY"
    RESEARCH_SELL = "RESEARCH_SELL"
    CASH_DEPOSIT = "CASH_DEPOSIT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"
    DIVIDEND = "DIVIDEND"
    FEE = "FEE"
    TAX = "TAX"
    SPLIT = "SPLIT"
    STOCK_DIVIDEND = "STOCK_DIVIDEND"
    ADJUSTMENT = "ADJUSTMENT"

    RESEARCH_ONLY = True
    NOT_BROKER_EXECUTION = True


class CostBasisMethod(enum.Enum):
    WEIGHTED_AVERAGE = "WEIGHTED_AVERAGE"
    FIFO = "FIFO"

    DEFAULT = "WEIGHTED_AVERAGE"


class ValuationStatus(enum.Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    STALE = "STALE"
    MISSING = "MISSING"
    BLOCKED = "BLOCKED"


class EligibilityStatus(enum.Enum):
    ELIGIBLE = "ELIGIBLE"
    ELIGIBLE_WITH_WARNING = "ELIGIBLE_WITH_WARNING"
    RESTRICTED = "RESTRICTED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class ReturnCalculationStatus(enum.Enum):
    VALID = "VALID"
    EXPERIMENTAL = "EXPERIMENTAL"
    MISSING_DATA = "MISSING_DATA"
    ZERO_BEGINNING = "ZERO_BEGINNING"
    INCOMPLETE = "INCOMPLETE"


class ConcentrationLevel(enum.Enum):
    NORMAL = "NORMAL"
    HIGH_CONCENTRATION = "HIGH_CONCENTRATION"
    HIGH_TOP3_CONCENTRATION = "HIGH_TOP3_CONCENTRATION"
    HIGH_HHI = "HIGH_HHI"
