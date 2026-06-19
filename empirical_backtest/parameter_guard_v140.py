"""
empirical_backtest/parameter_guard_v140.py — Parameter Search Guard for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


class ParameterSearchGuard:
    """Guards against over-parameterization and AutoML abuse."""

    def __init__(self):
        self.max_parameter_combinations = 10
        self.max_rules = 5
        self.max_symbols = 20
        self.max_folds = 10
        self.search_budget = 100
        self.overfitting_warning = True

    def validate_search(
        self,
        parameter_grid: dict,
        rules: list,
        symbols: list,
        folds: list,
    ) -> dict:
        warnings = []
        blocked = False

        # Count combinations
        combinations = 1
        for v in parameter_grid.values():
            if isinstance(v, list):
                combinations *= len(v)

        if combinations > self.max_parameter_combinations:
            blocked = True
            warnings.append(
                "Parameter grid exceeds max_parameter_combinations — AutoML not allowed"
            )

        if len(rules) > self.max_rules:
            blocked = True
            warnings.append(
                f"Too many rules ({len(rules)}) — max is {self.max_rules}"
            )

        if len(symbols) > self.max_symbols:
            warnings.append(
                f"Large symbol count ({len(symbols)}) may slow search"
            )

        if self.overfitting_warning and combinations > 3:
            warnings.append(
                "Multiple parameter combinations increase overfitting risk — use OOS for validation"
            )

        return {
            "ok": not blocked,
            "blocked": blocked,
            "warnings": warnings,
            "combinations": combinations,
        }
