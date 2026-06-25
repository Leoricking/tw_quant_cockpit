"""portfolio/stable_rollup/safety_contract_v159.py — Safety contract v1.5.9."""
from .models_v159 import StableContractRecord

SAFETY_CONTRACT = StableContractRecord(
    contract_id="portfolio_safety_contract_v159",
    contract_type="SAFETY",
    version="1.5.9",
    rules=[
        "RESEARCH_ONLY: all outputs are research-only",
        "NO_REAL_ORDER: no real orders may be created",
        "NO_BROKER: no broker connectivity",
        "NO_LIVE_ACCOUNT_SYNC: no live account synchronization",
        "NO_FORMAL_LEDGER_WRITE_FROM_SIMULATION: simulation may not write formal ledger",
        "NO_AUTO_APPLY: no automatic application of proposals",
        "NO_AUTO_REBALANCE: no automatic rebalancing",
        "NO_AUTO_STOP: no automatic stop-loss execution",
        "NO_AUTO_REDUCTION: no automatic position reduction",
        "NO_LIVE_HEDGING: no live hedging execution",
        "NO_LEVERAGE: no leveraged positions",
        "NO_SHORT: no short selling",
        "PRODUCTION_TRADING_BLOCKED: production trading is permanently blocked",
    ],
    blocking_violations=[
        "real_order_created",
        "broker_connected",
        "live_account_synced",
        "formal_ledger_written_from_simulation",
        "auto_apply_executed",
        "production_trading_enabled",
    ],
    status="VALID",
)

FORBIDDEN_FLAGS = {
    "REAL_ORDER_CREATION_ENABLED": False,
    "REAL_ORDER_EXECUTION_ENABLED": False,
    "BROKER_CONNECTION_ENABLED": False,
    "LIVE_ACCOUNT_SYNC_ENABLED": False,
    "AUTO_APPLY_ENABLED": False,
    "AUTO_REBALANCE_ENABLED": False,
    "AUTO_STOP_ENABLED": False,
    "AUTO_REDUCTION_ENABLED": False,
    "LIVE_HEDGING_ENABLED": False,
    "MARGIN_ENABLED": False,
    "SHORT_SELLING_ENABLED": False,
    "LEVERAGE_ENABLED": False,
    "PORTFOLIO_OPTIMIZATION_ENABLED": False,
    "BROKER_EXECUTION_ENABLED": False,
}

REQUIRED_FLAGS = {
    "NO_REAL_ORDERS": True,
    "PRODUCTION_TRADING_BLOCKED": True,
    "RESEARCH_ONLY": True,
}


class SafetyContractV159:
    def get_contract(self):
        return SAFETY_CONTRACT

    def validate(self):
        violations = []
        try:
            from release.version_info import (
                NO_REAL_ORDERS,
                BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
            )
            if not NO_REAL_ORDERS:
                violations.append("NO_REAL_ORDERS_FALSE")
            if BROKER_EXECUTION_ENABLED:
                violations.append("BROKER_EXECUTION_ENABLED_TRUE")
            if not PRODUCTION_TRADING_BLOCKED:
                violations.append("PRODUCTION_TRADING_NOT_BLOCKED")
        except ImportError as e:
            violations.append(f"IMPORT_ERROR:{e}")
        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "forbidden_flags": FORBIDDEN_FLAGS,
        }

    def check_drift(self):
        return []
