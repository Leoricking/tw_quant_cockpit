"""
portfolio/risk_controls/enums_v153.py — Drawdown & Risk Controls Enums v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import enum

RESEARCH_ONLY = True
ENUMS_VERSION = "1.5.3"


class DrawdownStatus(str, enum.Enum):
    """Status of a drawdown measurement."""
    AT_HIGH_WATER_MARK   = "AT_HIGH_WATER_MARK"
    IN_DRAWDOWN          = "IN_DRAWDOWN"
    RECOVERING           = "RECOVERING"
    RECOVERED            = "RECOVERED"
    UNKNOWN              = "UNKNOWN"


class RiskControlStatus(str, enum.Enum):
    """Evaluation status of a risk control check."""
    PASS      = "PASS"
    WARN      = "WARN"
    BREACH    = "BREACH"
    BLOCKED   = "BLOCKED"
    UNKNOWN   = "UNKNOWN"


class RiskControlType(str, enum.Enum):
    """Type of risk control policy."""
    VOLATILITY_LIMIT     = "VOLATILITY_LIMIT"
    DAILY_LOSS_LIMIT     = "DAILY_LOSS_LIMIT"
    WEEKLY_LOSS_LIMIT    = "WEEKLY_LOSS_LIMIT"
    MONTHLY_LOSS_LIMIT   = "MONTHLY_LOSS_LIMIT"
    DRAWDOWN_LIMIT       = "DRAWDOWN_LIMIT"
    CONCENTRATION_LIMIT  = "CONCENTRATION_LIMIT"
    CORRELATION_LIMIT    = "CORRELATION_LIMIT"
    LIQUIDITY_LIMIT      = "LIQUIDITY_LIMIT"
    CASH_RESERVE         = "CASH_RESERVE"
    RISK_BUDGET          = "RISK_BUDGET"


class RiskActionType(str, enum.Enum):
    """Recommended action — always RESEARCH_ONLY, never auto-executed."""
    NO_ACTION            = "NO_ACTION"
    WARN_ONLY            = "WARN_ONLY"
    REVIEW_RECOMMENDED   = "REVIEW_RECOMMENDED"
    REDUCE_RECOMMENDED   = "REDUCE_RECOMMENDED"
    HALT_RECOMMENDED     = "HALT_RECOMMENDED"


class DrawdownEpisodeStatus(str, enum.Enum):
    """Status of a drawdown episode."""
    OPEN      = "OPEN"
    CLOSED    = "CLOSED"
    PARTIAL   = "PARTIAL"


class AttributionType(str, enum.Enum):
    """Dimension for drawdown attribution."""
    POSITION  = "POSITION"
    INDUSTRY  = "INDUSTRY"
    THEME     = "THEME"
    CLUSTER   = "CLUSTER"


class StressScenarioType(str, enum.Enum):
    """Type of drawdown stress scenario."""
    HISTORICAL_REPEAT       = "HISTORICAL_REPEAT"
    VOLATILITY_SPIKE        = "VOLATILITY_SPIKE"
    CORRELATION_BREAKDOWN   = "CORRELATION_BREAKDOWN"
    LIQUIDITY_CRISIS        = "LIQUIDITY_CRISIS"
    FLASH_CRASH             = "FLASH_CRASH"
    BEAR_MARKET             = "BEAR_MARKET"
    SECTOR_ROTATION         = "SECTOR_ROTATION"
    COMBINED                = "COMBINED"
