"""
quality_gates.gate_policy — Coverage Quality Gate Policy Definitions v1.1.4

Research-only. Defines per-gate thresholds, required datasets, freshness
requirements, and blocking/warning reason codes. No broker connectivity.
No order placement.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True

from quality_gates.gate_schema import (
    RC_PRICE_DATA_MISSING,
    RC_HISTORY_INSUFFICIENT,
    RC_DAILY_COMPLETENESS_LOW,
    RC_INVALID_OHLC,
    RC_INVALID_VOLUME,
    RC_CONFLICTING_ROWS,
    RC_FUTURE_DATE,
    RC_DATE_REGRESSION,
    RC_DAILY_PRICE_STALE,
    RC_SOURCE_INTERRUPTED,
    RC_CRITICAL_REPAIR_OPEN,
    RC_MANUAL_REVIEW_OPEN,
    RC_MOCK_SOURCE,
    RC_FIXTURE_SOURCE,
    RC_CHIPS_MISSING,
    RC_REVENUE_MISSING,
    RC_FUNDAMENTALS_MISSING,
    RC_SHORT_INTEREST_MISSING,
    RC_SECTOR_DATA_MISSING,
)

# ---------------------------------------------------------------------------
# Gate name constants
# ---------------------------------------------------------------------------
GATE_PRICE_BACKTEST = "price_backtest"
GATE_BUY_POINT = "buy_point"
GATE_SCREENER = "screener"
GATE_STRATEGY_KNOWLEDGE = "strategy_knowledge"
GATE_KD_ADVANCED = "kd_advanced"
GATE_SHORT_INTEREST = "short_interest"
GATE_BOTTOM_REVERSAL = "bottom_reversal"
GATE_SECTOR_ROTATION = "sector_rotation"
GATE_FUNDAMENTAL_QUALITY = "fundamental_quality"
GATE_STOCK_REPORT = "stock_report"
GATE_LOCAL_ASSISTANT = "local_assistant"
GATE_KB_CONTEXT = "kb_context"

ALL_GATES = [
    GATE_PRICE_BACKTEST,
    GATE_BUY_POINT,
    GATE_SCREENER,
    GATE_STRATEGY_KNOWLEDGE,
    GATE_KD_ADVANCED,
    GATE_SHORT_INTEREST,
    GATE_BOTTOM_REVERSAL,
    GATE_SECTOR_ROTATION,
    GATE_FUNDAMENTAL_QUALITY,
    GATE_STOCK_REPORT,
    GATE_LOCAL_ASSISTANT,
    GATE_KB_CONTEXT,
]

# ---------------------------------------------------------------------------
# Gate definitions
# ---------------------------------------------------------------------------
_GATE_DEFINITIONS = {
    GATE_PRICE_BACKTEST: {
        "description": "Formal price backtest eligibility",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 120,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume", "chips", "revenue", "fundamentals"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_CONFLICTING_ROWS,
            RC_FUTURE_DATE, RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
            RC_DAILY_COMPLETENESS_LOW, RC_DAILY_PRICE_STALE, RC_SOURCE_INTERRUPTED,
            RC_CRITICAL_REPAIR_OPEN, RC_HISTORY_INSUFFICIENT,
        ],
        "optional_warn_codes": [
            RC_CHIPS_MISSING, RC_REVENUE_MISSING, RC_FUNDAMENTALS_MISSING,
            RC_MANUAL_REVIEW_OPEN, RC_INVALID_VOLUME,
        ],
    },
    GATE_BUY_POINT: {
        "description": "Buy point detection eligibility",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 120,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume", "chips"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_CONFLICTING_ROWS,
            RC_FUTURE_DATE, RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
            RC_DAILY_COMPLETENESS_LOW, RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
        ],
        "optional_warn_codes": [RC_CHIPS_MISSING, RC_INVALID_VOLUME],
    },
    GATE_SCREENER: {
        "description": "Screener eligibility (observational ok)",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 60,
        "observational_min_completeness": 0.80,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume", "chips", "revenue", "fundamentals"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_CONFLICTING_ROWS,
            RC_FUTURE_DATE, RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [
            RC_DAILY_COMPLETENESS_LOW, RC_CHIPS_MISSING, RC_HISTORY_INSUFFICIENT,
            RC_DAILY_PRICE_STALE, RC_REVENUE_MISSING,
        ],
    },
    GATE_STRATEGY_KNOWLEDGE: {
        "description": "Strategy knowledge base context eligibility",
        "formal_min_rows": 120,
        "formal_min_trading_days": 120,
        "formal_min_completeness": 0.90,
        "observational_min_rows": 60,
        "observational_min_completeness": 0.75,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume", "chips", "revenue", "fundamentals"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_FUTURE_DATE,
            RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [
            RC_CONFLICTING_ROWS, RC_DAILY_COMPLETENESS_LOW, RC_DAILY_PRICE_STALE,
            RC_HISTORY_INSUFFICIENT, RC_CHIPS_MISSING,
        ],
    },
    GATE_KD_ADVANCED: {
        "description": "KD advanced indicator eligibility",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 120,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_CONFLICTING_ROWS,
            RC_FUTURE_DATE, RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
            RC_DAILY_COMPLETENESS_LOW, RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
        ],
        "optional_warn_codes": [RC_INVALID_VOLUME, RC_CHIPS_MISSING],
    },
    GATE_SHORT_INTEREST: {
        "description": "Short interest strategy eligibility",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 120,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price", "short_interest"],
        "optional_datasets": ["chips"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_SHORT_INTEREST_MISSING, RC_INVALID_OHLC,
            RC_CONFLICTING_ROWS, RC_FUTURE_DATE, RC_DATE_REGRESSION,
            RC_MOCK_SOURCE, RC_FIXTURE_SOURCE, RC_DAILY_COMPLETENESS_LOW,
            RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
        ],
        "optional_warn_codes": [RC_CHIPS_MISSING],
    },
    GATE_BOTTOM_REVERSAL: {
        "description": "Bottom reversal pattern eligibility",
        "formal_min_rows": 300,
        "formal_min_trading_days": 300,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 180,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["volume", "chips"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_CONFLICTING_ROWS,
            RC_FUTURE_DATE, RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
            RC_DAILY_COMPLETENESS_LOW, RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
            RC_SOURCE_INTERRUPTED,
        ],
        "optional_warn_codes": [RC_CHIPS_MISSING, RC_MANUAL_REVIEW_OPEN],
    },
    GATE_SECTOR_ROTATION: {
        "description": "Sector rotation strategy eligibility",
        "formal_min_rows": 240,
        "formal_min_trading_days": 240,
        "formal_min_completeness": 0.98,
        "observational_min_rows": 120,
        "observational_min_completeness": 0.90,
        "required_datasets": ["daily_price", "sector_data"],
        "optional_datasets": ["chips", "revenue"],
        "freshness_required": ["FRESH", "ACCEPTABLE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_SECTOR_DATA_MISSING, RC_INVALID_OHLC,
            RC_CONFLICTING_ROWS, RC_FUTURE_DATE, RC_DATE_REGRESSION,
            RC_MOCK_SOURCE, RC_FIXTURE_SOURCE, RC_DAILY_COMPLETENESS_LOW,
            RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
        ],
        "optional_warn_codes": [RC_CHIPS_MISSING, RC_REVENUE_MISSING],
    },
    GATE_FUNDAMENTAL_QUALITY: {
        "description": "Fundamental quality validation eligibility",
        "formal_min_rows": 120,
        "formal_min_trading_days": 120,
        "formal_min_completeness": 0.90,
        "observational_min_rows": 60,
        "observational_min_completeness": 0.75,
        "required_datasets": ["daily_price", "revenue", "fundamentals"],
        "optional_datasets": ["chips"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_REVENUE_MISSING, RC_FUNDAMENTALS_MISSING,
            RC_INVALID_OHLC, RC_FUTURE_DATE, RC_DATE_REGRESSION,
            RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [RC_CONFLICTING_ROWS, RC_DAILY_COMPLETENESS_LOW, RC_CHIPS_MISSING],
    },
    GATE_STOCK_REPORT: {
        "description": "Stock report generation eligibility",
        "formal_min_rows": 60,
        "formal_min_trading_days": 60,
        "formal_min_completeness": 0.80,
        "observational_min_rows": 20,
        "observational_min_completeness": 0.60,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["chips", "revenue", "fundamentals", "sector_data"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_FUTURE_DATE,
            RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [
            RC_CONFLICTING_ROWS, RC_DAILY_COMPLETENESS_LOW, RC_CHIPS_MISSING,
            RC_REVENUE_MISSING, RC_FUNDAMENTALS_MISSING, RC_SECTOR_DATA_MISSING,
            RC_DAILY_PRICE_STALE, RC_HISTORY_INSUFFICIENT,
        ],
    },
    GATE_LOCAL_ASSISTANT: {
        "description": "Local assistant conclusion eligibility",
        "formal_min_rows": 60,
        "formal_min_trading_days": 60,
        "formal_min_completeness": 0.75,
        "observational_min_rows": 10,
        "observational_min_completeness": 0.50,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["chips", "revenue", "fundamentals"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED", "STALE"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_FUTURE_DATE,
            RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [
            RC_CONFLICTING_ROWS, RC_DAILY_PRICE_STALE, RC_CHIPS_MISSING,
            RC_REVENUE_MISSING, RC_FUNDAMENTALS_MISSING,
        ],
    },
    GATE_KB_CONTEXT: {
        "description": "Knowledge base context quality eligibility",
        "formal_min_rows": 60,
        "formal_min_trading_days": 60,
        "formal_min_completeness": 0.75,
        "observational_min_rows": 10,
        "observational_min_completeness": 0.50,
        "required_datasets": ["daily_price"],
        "optional_datasets": ["chips", "revenue", "fundamentals"],
        "freshness_required": ["FRESH", "ACCEPTABLE", "DELAYED"],
        "blocking_reason_codes": [
            RC_PRICE_DATA_MISSING, RC_INVALID_OHLC, RC_FUTURE_DATE,
            RC_DATE_REGRESSION, RC_MOCK_SOURCE, RC_FIXTURE_SOURCE,
        ],
        "optional_warn_codes": [RC_CONFLICTING_ROWS, RC_DAILY_PRICE_STALE, RC_CHIPS_MISSING],
    },
}


class CoverageQualityGatePolicy:
    """Policy definitions for all 12 coverage quality gates."""

    POLICY_VERSION = "1.1.4"

    def get_gate_policy(self, gate_name: str) -> dict:
        """Return full policy dict for a gate, or {} if unknown."""
        return _GATE_DEFINITIONS.get(gate_name, {})

    def required_datasets(self, gate_name: str) -> list:
        return self.get_gate_policy(gate_name).get("required_datasets", [])

    def optional_datasets(self, gate_name: str) -> list:
        return self.get_gate_policy(gate_name).get("optional_datasets", [])

    def minimum_rows(self, gate_name: str, level: str = "formal") -> int:
        policy = self.get_gate_policy(gate_name)
        if level == "formal":
            return policy.get("formal_min_rows", 240)
        return policy.get("observational_min_rows", 120)

    def minimum_completeness(self, gate_name: str, level: str = "formal") -> float:
        policy = self.get_gate_policy(gate_name)
        if level == "formal":
            return policy.get("formal_min_completeness", 0.98)
        return policy.get("observational_min_completeness", 0.90)

    def allowed_freshness(self, gate_name: str) -> list:
        return self.get_gate_policy(gate_name).get("freshness_required", ["FRESH", "ACCEPTABLE"])

    def blocking_reason_codes(self, gate_name: str) -> list:
        return self.get_gate_policy(gate_name).get("blocking_reason_codes", [])

    def policy_version(self) -> str:
        return self.POLICY_VERSION

    def list_gates(self) -> list:
        return list(ALL_GATES)

    def is_valid_gate(self, gate_name: str) -> bool:
        return gate_name in _GATE_DEFINITIONS
