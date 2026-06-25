"""portfolio/stable_rollup/enum_registry_v159.py — Enum registry v1.5.9."""
from .models_v159 import StableEnumRecord

STABLE_ENUMS = [
    StableEnumRecord(enum_name="TransactionType", values=["BUY", "SELL", "DEPOSIT", "WITHDRAWAL", "DIVIDEND", "FEE", "TAX", "CORPORATE_ACTION", "ADJUSTMENT"], introduced_version="1.5.0", stable_version="1.5.0"),
    StableEnumRecord(enum_name="CostBasisMethod", values=["FIFO", "LIFO", "AVERAGE", "SPECIFIC_LOT"], introduced_version="1.5.0", stable_version="1.5.0"),
    StableEnumRecord(enum_name="EligibilityStatus", values=["ELIGIBLE", "INELIGIBLE", "BLOCKED", "PARTIAL", "UNKNOWN"], introduced_version="1.5.0", stable_version="1.5.0"),
    StableEnumRecord(enum_name="SizingMethod", values=["FIXED_FRACTIONAL", "STOP_DISTANCE", "ATR", "VOLATILITY_TARGET", "TARGET_WEIGHT", "CUSTOM"], introduced_version="1.5.1", stable_version="1.5.1"),
    StableEnumRecord(enum_name="SizingStatus", values=["VALID", "PARTIAL", "BLOCKED", "INSUFFICIENT_DATA", "FAILED"], introduced_version="1.5.1", stable_version="1.5.1"),
    StableEnumRecord(enum_name="ConstraintType", values=["CASH_LIMIT", "LIQUIDITY_CAP", "MAX_WEIGHT", "MIN_LOT", "VOLATILITY_LIMIT", "CONCENTRATION_LIMIT"], introduced_version="1.5.1", stable_version="1.5.1"),
    StableEnumRecord(enum_name="CorrelationMethod", values=["PEARSON", "SPEARMAN", "KENDALL", "ROLLING"], introduced_version="1.5.2", stable_version="1.5.2"),
    StableEnumRecord(enum_name="ExposureType", values=["INDUSTRY", "THEME", "MARKET", "ASSET", "ETF_DIRECT", "ETF_INDIRECT", "BETA", "CLUSTER"], introduced_version="1.5.2", stable_version="1.5.2"),
    StableEnumRecord(enum_name="RiskControlStatus", values=["WITHIN_LIMIT", "WARNING", "RESTRICTED", "BLOCKED", "UNKNOWN"], introduced_version="1.5.3", stable_version="1.5.3"),
    StableEnumRecord(enum_name="RiskActionType", values=["NO_ACTION", "MONITOR", "FREEZE_NEW_BUYS", "REDUCE_NEW_POSITION_SIZE", "REVIEW_POSITION", "REVIEW_CLUSTER", "REVIEW_INDUSTRY", "REVIEW_THEME", "RAISE_CASH_RESEARCH", "BLOCK_NEW_SIZING"], introduced_version="1.5.3", stable_version="1.5.3"),
    StableEnumRecord(enum_name="WindowType", values=["ROLLING", "EXPANDING", "ANCHORED"], introduced_version="1.5.4", stable_version="1.5.4"),
    StableEnumRecord(enum_name="ReplayStatus", values=["VALID", "PARTIAL", "BLOCKED", "NOT_BACKTESTABLE", "INSUFFICIENT_DATA", "FAILED"], introduced_version="1.5.4", stable_version="1.5.4"),
    StableEnumRecord(enum_name="CapabilityStage", values=["STABLE", "PLANNED", "DISABLED", "DEPRECATED", "REMOVED"], introduced_version="1.5.9", stable_version="1.5.9"),
]

for _e in STABLE_ENUMS:
    _e.fingerprint = _e.compute_fingerprint()


class EnumRegistryV159:
    def get_all(self):
        return list(STABLE_ENUMS)

    def get_by_name(self, name):
        return next((e for e in STABLE_ENUMS if e.enum_name == name), None)

    def get_fingerprints(self):
        return {e.enum_name: e.fingerprint for e in STABLE_ENUMS}

    def validate(self):
        issues = []
        names = [e.enum_name for e in STABLE_ENUMS]
        if len(names) != len(set(names)):
            issues.append("DUPLICATE_ENUM")
        for e in STABLE_ENUMS:
            vals = e.values
            if len(vals) != len(set(vals)):
                issues.append(f"DUPLICATE_VALUE:{e.enum_name}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(STABLE_ENUMS)}
