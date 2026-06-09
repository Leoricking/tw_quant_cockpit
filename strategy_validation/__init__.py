# strategy_validation/__init__.py
# TW Quant Cockpit — Strategy Validation Score Package
# v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading
from .strategy_validation_schema import (
    StrategyValidationScore, StrategyValidationComponent, StrategyValidationSummary,
    GRADE_INSUFFICIENT, GRADE_OBSERVATIONAL, GRADE_VALIDATING, GRADE_VALIDATED,
    GRADE_CONFLICTED, GRADE_REJECTED,
)
__all__ = [
    "StrategyValidationScore", "StrategyValidationComponent", "StrategyValidationSummary",
    "GRADE_INSUFFICIENT", "GRADE_OBSERVATIONAL", "GRADE_VALIDATING", "GRADE_VALIDATED",
    "GRADE_CONFLICTED", "GRADE_REJECTED",
]
