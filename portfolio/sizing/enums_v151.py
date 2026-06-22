"""
portfolio/sizing/enums_v151.py — Position Sizing Enums v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from enum import Enum


class SizingMethod(str, Enum):
    FIXED_FRACTIONAL     = "FIXED_FRACTIONAL"
    STOP_DISTANCE        = "STOP_DISTANCE"
    ATR_BASED            = "ATR_BASED"
    VOLATILITY_TARGET    = "VOLATILITY_TARGET"
    FIXED_PORTFOLIO_WEIGHT = "FIXED_PORTFOLIO_WEIGHT"
    CASH_LIMITED         = "CASH_LIMITED"
    MANUAL_RESEARCH      = "MANUAL_RESEARCH"


class SizingStatus(str, Enum):
    VALID             = "VALID"
    CAPPED            = "CAPPED"
    REDUCED           = "REDUCED"
    RESTRICTED        = "RESTRICTED"
    BLOCKED           = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ConstraintType(str, Enum):
    AVAILABLE_CASH       = "AVAILABLE_CASH"
    PORTFOLIO_VALUE      = "PORTFOLIO_VALUE"
    SINGLE_NAME_LIMIT    = "SINGLE_NAME_LIMIT"
    INDUSTRY_LIMIT       = "INDUSTRY_LIMIT"
    THEME_LIMIT          = "THEME_LIMIT"
    MARKET_LIMIT         = "MARKET_LIMIT"
    ETF_LIMIT            = "ETF_LIMIT"
    LIQUIDITY_LIMIT      = "LIQUIDITY_LIMIT"
    LOT_SIZE             = "LOT_SIZE"
    MINIMUM_ORDER_VALUE  = "MINIMUM_ORDER_VALUE"
    MAXIMUM_ORDER_VALUE  = "MAXIMUM_ORDER_VALUE"
    STOP_DISTANCE        = "STOP_DISTANCE"
    ATR                  = "ATR"
    VOLATILITY           = "VOLATILITY"
    DATA_QUALITY         = "DATA_QUALITY"
    FRESHNESS            = "FRESHNESS"
    PIT                  = "PIT"
    LINEAGE              = "LINEAGE"
    CONFLICT             = "CONFLICT"
    UNSUPPORTED_ASSET    = "UNSUPPORTED_ASSET"
    UNSUPPORTED_SHORT    = "UNSUPPORTED_SHORT"


class ConstraintSeverity(str, Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    HARD_CAP = "HARD_CAP"
    BLOCKING = "BLOCKING"


class RoundingMode(str, Enum):
    ROUND_DOWN           = "ROUND_DOWN"
    NEAREST_LOT          = "NEAREST_LOT"
    ZERO_IF_BELOW_MINIMUM = "ZERO_IF_BELOW_MINIMUM"
