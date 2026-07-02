"""
paper_trading/performance_attribution/enums_v167.py
Attribution enums for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True

FORBIDDEN_MODES = frozenset({"LIVE", "REAL", "BROKER", "PRODUCTION", "FORMAL_LEDGER"})


class AttributionLevel(Enum):
    PORTFOLIO  = "PORTFOLIO"
    STRATEGY   = "STRATEGY"
    SESSION    = "SESSION"
    SYMBOL     = "SYMBOL"
    SECTOR     = "SECTOR"
    INDUSTRY   = "INDUSTRY"
    POSITION   = "POSITION"
    TRADE      = "TRADE"


class AttributionDimension(Enum):
    RETURN     = "RETURN"
    PNL        = "PNL"
    SELECTION  = "SELECTION"
    ALLOCATION = "ALLOCATION"
    TIMING     = "TIMING"
    EXPOSURE   = "EXPOSURE"
    EXECUTION  = "EXECUTION"
    COST       = "COST"
    SLIPPAGE   = "SLIPPAGE"
    TURNOVER   = "TURNOVER"
    RISK       = "RISK"
    DRAWDOWN   = "DRAWDOWN"
    REGIME     = "REGIME"
    BENCHMARK  = "BENCHMARK"
    FACTOR     = "FACTOR"
    RESIDUAL   = "RESIDUAL"


class AttributionMethod(Enum):
    BRINSON_HOOD_BEEBOWER = "BRINSON_HOOD_BEEBOWER"
    BRINSON_FACHLER       = "BRINSON_FACHLER"
    ARITHMETIC            = "ARITHMETIC"
    GEOMETRIC             = "GEOMETRIC"
    FACTOR_BASED          = "FACTOR_BASED"
    RETURNS_BASED         = "RETURNS_BASED"
    HOLDINGS_BASED        = "HOLDINGS_BASED"
    TRANSACTION_BASED     = "TRANSACTION_BASED"
    CUSTOM                = "CUSTOM"


class ContributionType(Enum):
    AMOUNT         = "AMOUNT"
    RETURN         = "RETURN"
    BASIS_POINTS   = "BASIS_POINTS"
    PERCENT        = "PERCENT"
    NORMALIZED     = "NORMALIZED"


class ReturnBasis(Enum):
    GROSS          = "GROSS"
    NET            = "NET"
    REALIZED       = "REALIZED"
    UNREALIZED     = "UNREALIZED"
    TOTAL          = "TOTAL"
    TIME_WEIGHTED  = "TIME_WEIGHTED"
    MONEY_WEIGHTED = "MONEY_WEIGHTED"
    ACTIVE         = "ACTIVE"


class CostType(Enum):
    COMMISSION     = "COMMISSION"
    TRANSACTION_TAX = "TRANSACTION_TAX"
    EXCHANGE_FEE   = "EXCHANGE_FEE"
    BORROW_COST    = "BORROW_COST"
    FINANCING_COST = "FINANCING_COST"
    SPREAD_COST    = "SPREAD_COST"
    SLIPPAGE       = "SLIPPAGE"
    IMPACT_COST    = "IMPACT_COST"
    TURNOVER_DRAG  = "TURNOVER_DRAG"
    OTHER          = "OTHER"
    UNKNOWN        = "UNKNOWN"


class CostQuality(Enum):
    KNOWN      = "KNOWN"
    ESTIMATED  = "ESTIMATED"
    UNKNOWN    = "UNKNOWN"


class ExecutionQuality(Enum):
    EXCELLENT  = "EXCELLENT"
    GOOD       = "GOOD"
    NEUTRAL    = "NEUTRAL"
    POOR       = "POOR"
    VERY_POOR  = "VERY_POOR"
    UNAVAILABLE = "UNAVAILABLE"


class ExecutionReference(Enum):
    SIGNAL_PRICE   = "SIGNAL_PRICE"
    DECISION_PRICE = "DECISION_PRICE"
    ORDER_PRICE    = "ORDER_PRICE"
    FILL_PRICE     = "FILL_PRICE"
    CLOSE_PRICE    = "CLOSE_PRICE"
    NEXT_BAR       = "NEXT_BAR"
    VWAP           = "VWAP"
    TWAP           = "TWAP"


class RiskSource(Enum):
    MARKET       = "MARKET"
    BETA         = "BETA"
    CONCENTRATION = "CONCENTRATION"
    CORRELATION  = "CORRELATION"
    LEVERAGE     = "LEVERAGE"
    LIQUIDITY    = "LIQUIDITY"
    GAP          = "GAP"
    OVERNIGHT    = "OVERNIGHT"
    TURNOVER     = "TURNOVER"
    TAIL         = "TAIL"
    SECTOR       = "SECTOR"
    FACTOR       = "FACTOR"
    RESIDUAL     = "RESIDUAL"


class DrawdownSource(Enum):
    SYMBOL       = "SYMBOL"
    STRATEGY     = "STRATEGY"
    SESSION      = "SESSION"
    SECTOR       = "SECTOR"
    INDUSTRY     = "INDUSTRY"
    TIMING       = "TIMING"
    ALLOCATION   = "ALLOCATION"
    CONCENTRATION = "CONCENTRATION"
    LEVERAGE     = "LEVERAGE"
    GAP          = "GAP"
    EXECUTION    = "EXECUTION"
    COST         = "COST"
    RESIDUAL     = "RESIDUAL"


class RegimeType(Enum):
    BULL            = "BULL"
    BEAR            = "BEAR"
    SIDEWAYS        = "SIDEWAYS"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY  = "LOW_VOLATILITY"
    RISK_ON         = "RISK_ON"
    RISK_OFF        = "RISK_OFF"
    LIQUID          = "LIQUID"
    ILLIQUID        = "ILLIQUID"
    GAP_UP          = "GAP_UP"
    GAP_DOWN        = "GAP_DOWN"
    EVENT_DRIVEN    = "EVENT_DRIVEN"
    UNKNOWN         = "UNKNOWN"


class BenchmarkMode(Enum):
    MARKET_BENCHMARK  = "MARKET_BENCHMARK"
    POLICY_BASELINE   = "POLICY_BASELINE"
    STRATEGY_BASELINE = "STRATEGY_BASELINE"
    UNIVERSE_BASELINE = "UNIVERSE_BASELINE"
    NONE              = "NONE"


class ReconciliationStatus(Enum):
    RECONCILED              = "RECONCILED"
    RECONCILED_WITH_ROUNDING = "RECONCILED_WITH_ROUNDING"
    DEGRADED                = "DEGRADED"
    FAILED                  = "FAILED"
    INSUFFICIENT_DATA       = "INSUFFICIENT_DATA"


class AttributionStatus(Enum):
    COMPLETE          = "COMPLETE"
    DEGRADED          = "DEGRADED"
    FAILED            = "FAILED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNSUPPORTED       = "UNSUPPORTED"
    BLOCKED           = "BLOCKED"


class DataQualityStatus(Enum):
    COMPLETE     = "COMPLETE"
    PARTIAL      = "PARTIAL"
    DEGRADED     = "DEGRADED"
    INSUFFICIENT = "INSUFFICIENT"
    UNKNOWN      = "UNKNOWN"


class ConfidenceLevel(Enum):
    HIGH    = "HIGH"
    MEDIUM  = "MEDIUM"
    LOW     = "LOW"
    UNKNOWN = "UNKNOWN"


class PeriodType(Enum):
    DAILY       = "DAILY"
    WEEKLY      = "WEEKLY"
    MONTHLY     = "MONTHLY"
    QUARTERLY   = "QUARTERLY"
    ANNUAL      = "ANNUAL"
    ROLLING_N   = "ROLLING_N"
    ARBITRARY   = "ARBITRARY"
    INCEPTION   = "INCEPTION"


class TradeDirection(Enum):
    LONG    = "LONG"
    SHORT   = "SHORT"
    NEUTRAL = "NEUTRAL"


class PositionState(Enum):
    OPEN       = "OPEN"
    CLOSED     = "CLOSED"
    PARTIAL    = "PARTIAL"
    UNDEFINED  = "UNDEFINED"


class SessionState(Enum):
    ACTIVE     = "ACTIVE"
    INACTIVE   = "INACTIVE"
    STALE      = "STALE"
    FAILED     = "FAILED"
    RECOVERING = "RECOVERING"
    UNKNOWN    = "UNKNOWN"


class FixtureUsageType(Enum):
    UNIT_TEST       = "UNIT_TEST"
    INTEGRATION     = "INTEGRATION"
    SCENARIO        = "SCENARIO"
    REGRESSION      = "REGRESSION"
    HEALTH_CHECK    = "HEALTH_CHECK"
    GATE_CHECK      = "GATE_CHECK"
    VALIDATION      = "VALIDATION"


class AttributionPurpose(Enum):
    RESEARCH         = "RESEARCH"
    PAPER_REVIEW     = "PAPER_REVIEW"
    STRATEGY_DIAGNOSTICS = "STRATEGY_DIAGNOSTICS"
    PORTFOLIO_DIAGNOSTICS = "PORTFOLIO_DIAGNOSTICS"
    RISK_DIAGNOSTICS = "RISK_DIAGNOSTICS"
    EXECUTION_DIAGNOSTICS = "EXECUTION_DIAGNOSTICS"
    REGRESSION       = "REGRESSION"


# Forbidden field names — must never appear in attribution models
FORBIDDEN_FIELDS = frozenset({
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "shioaji_login", "broker_api_key", "production_ledger",
})
