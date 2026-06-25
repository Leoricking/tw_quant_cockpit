"""portfolio/stable_rollup/pit_contract_v159.py — PIT contract v1.5.9."""
from .models_v159 import StableContractRecord

PIT_CONTRACT = StableContractRecord(
    contract_id="portfolio_pit_contract_v159",
    contract_type="PIT",
    version="1.5.9",
    rules=[
        "effective_at <= as_of",
        "available_from <= as_of",
        "fetched_at must not substitute available_from",
        "current Universe must not backfill historical decisions",
        "current classifications must not backfill historical decisions",
        "future prices are forbidden",
        "future financials are forbidden",
        "future ATR is forbidden",
        "future volatility is forbidden",
        "future correlation matrices are forbidden",
        "future ETF holdings are forbidden",
        "future policy versions are forbidden",
        "future transactions are forbidden",
        "future benchmark values are forbidden",
        "future corporate actions are forbidden",
        "future risk limits are forbidden",
        "silent fallback to current/mock data is forbidden",
    ],
    blocking_violations=[
        "future_price_used",
        "future_universe_used",
        "fetched_at_used_as_available_from",
        "silent_fallback_to_current",
    ],
    status="VALID",
)

PIT_CONTRACT_MATRIX = [
    {"module": "portfolio", "input_type": "price", "required_timestamps": ["available_from", "effective_at"], "blocking": "BLOCK", "fallback": "INSUFFICIENT_DATA"},
    {"module": "portfolio.sizing", "input_type": "ATR", "required_timestamps": ["available_from"], "blocking": "BLOCK", "fallback": "BLOCK"},
    {"module": "portfolio.correlation", "input_type": "return_series", "required_timestamps": ["available_from"], "blocking": "BLOCK", "fallback": "INSUFFICIENT_DATA"},
    {"module": "portfolio.risk_controls", "input_type": "equity_curve", "required_timestamps": ["available_from", "effective_at"], "blocking": "BLOCK", "fallback": "PARTIAL"},
    {"module": "portfolio.walk_forward", "input_type": "all", "required_timestamps": ["available_from", "effective_at"], "blocking": "BLOCK", "fallback": "INSUFFICIENT_DATA"},
]


class PITContractV159:
    def get_contract(self):
        return PIT_CONTRACT

    def get_matrix(self):
        return PIT_CONTRACT_MATRIX

    def validate(self, data_item, as_of):
        violations = []
        af = data_item.get("available_from") if isinstance(data_item, dict) else None
        if af and af > as_of:
            violations.append("future_data_detected")
        if isinstance(data_item, dict) and data_item.get("fetched_at") and not data_item.get("available_from"):
            violations.append("fetched_at_used_as_available_from")
        return {"is_valid": len(violations) == 0, "violations": violations, "as_of": as_of}

    def check_drift(self):
        return []  # No drift in baseline
