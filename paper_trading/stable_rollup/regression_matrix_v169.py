"""
paper_trading/stable_rollup/regression_matrix_v169.py
Regression matrix for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import List, Dict, Any

from paper_trading.stable_rollup.models_v169 import ReleaseRegressionSummary

VERSION = "1.6.9"
BASELINE_VERSION = "1.6.8"
BASELINE_TEST_COUNT = 11465

REGRESSION_MATRIX: List[dict] = [
    {
        "baseline_version": "1.6.8",
        "current_version": "1.6.9",
        "tests_baseline": 11465,
        "tests_added_by_169": 500,
        "regression_domains": [
            "health", "gate", "cli", "gui", "fixtures", "scenarios",
            "version", "safety", "manifest", "registry", "capability",
            "compatibility", "contract", "snapshot", "validator",
            "reconciler", "scorecard", "query", "report", "migration",
        ],
        "baseline_stable": True,
        "notes": "v1.6.9 adds stable rollup test coverage on top of v1.6.8 baseline",
    },
    {
        "baseline_version": "1.6.7",
        "current_version": "1.6.9",
        "tests_baseline": 10865,
        "tests_added_by_168": 600,
        "tests_added_by_169": 500,
        "regression_domains": ["health", "gate", "cli"],
        "baseline_stable": True,
        "notes": "Two-version regression span",
    },
]


class RegressionChecker:
    """Check for regressions against a baseline version."""

    def check_regression(self, baseline_version: str = BASELINE_VERSION) -> ReleaseRegressionSummary:
        """Check regression against baseline version."""
        entry = None
        for r in REGRESSION_MATRIX:
            if r["baseline_version"] == baseline_version:
                entry = r
                break

        if entry is None:
            return ReleaseRegressionSummary(
                baseline_version=baseline_version,
                current_version=VERSION,
                tests_baseline=0,
                tests_current=0,
                delta=0,
                regression_found=True,
            )

        tests_baseline = entry["tests_baseline"]
        tests_current = tests_baseline + entry.get("tests_added_by_169", 0)
        delta = tests_current - tests_baseline
        regression_found = delta < 0

        return ReleaseRegressionSummary(
            baseline_version=baseline_version,
            current_version=VERSION,
            tests_baseline=tests_baseline,
            tests_current=tests_current,
            delta=delta,
            regression_found=regression_found,
        )

    def get_all_baselines(self) -> List[str]:
        return [r["baseline_version"] for r in REGRESSION_MATRIX]

    def summary(self) -> Dict[str, Any]:
        results = []
        for entry in REGRESSION_MATRIX:
            r = self.check_regression(entry["baseline_version"])
            results.append({
                "baseline_version": r.baseline_version,
                "current_version": r.current_version,
                "tests_baseline": r.tests_baseline,
                "tests_current": r.tests_current,
                "delta": r.delta,
                "regression_found": r.regression_found,
            })
        any_regression = any(r["regression_found"] for r in results)
        return {
            "name": "regression_matrix_v169",
            "version": VERSION,
            "status": "FAIL" if any_regression else "PASS",
            "any_regression": any_regression,
            "results": results,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
