"""
strategy_robustness/parameter_sensitivity_v142.py — Parameter sensitivity analysis for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Any

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ParameterSensitivityAnalyzer:
    """
    Analyzes sensitivity of strategy performance to parameter variations.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, baseline_metrics: dict, parameter_variants: list, config) -> dict:
        """
        Analyze parameter sensitivity.

        Parameters
        ----------
        baseline_metrics : dict with baseline performance metrics
        parameter_variants : list of dicts, each with keys: params (dict), metrics (dict)
        config : RobustnessConfiguration

        Returns
        -------
        dict with parameter sensitivity analysis
        """
        if not baseline_metrics:
            return {
                "status": "INSUFFICIENT_DATA",
                "variants": [],
                "checks": {},
                "warnings": ["NO_BASELINE"],
            }

        baseline_expectancy = baseline_metrics.get("expectancy", 0.0)
        baseline_win_rate = baseline_metrics.get("win_rate", 0.0)
        baseline_net_return = baseline_metrics.get("net_return", 0.0)

        variant_results = []
        for i, variant in enumerate(parameter_variants):
            params = variant.get("params", {})
            metrics = variant.get("metrics", {})
            v_expectancy = metrics.get("expectancy", 0.0)
            v_win_rate = metrics.get("win_rate", 0.0)
            v_net_return = metrics.get("net_return", 0.0)

            delta_expectancy = v_expectancy - baseline_expectancy
            delta_net_return = v_net_return - baseline_net_return

            # Cliff risk: large negative delta from small param change
            neighborhood = getattr(config, "parameter_neighborhood", 0.1)
            cliff_risk = abs(delta_expectancy) > 0.02

            variant_results.append({
                "rank": i + 1,
                "params": params,
                "metrics": metrics,
                "delta_vs_baseline": {
                    "expectancy": round(delta_expectancy, 6),
                    "win_rate": round(v_win_rate - baseline_win_rate, 4),
                    "net_return": round(delta_net_return, 6),
                },
                "stability": "STABLE" if abs(delta_expectancy) < 0.01 else (
                    "UNSTABLE" if abs(delta_expectancy) > 0.03 else "MODERATE"
                ),
                "cliff_risk": cliff_risk,
                "monotonicity": "UNKNOWN",
                "flat_region_width": 0,
                "confidence": "MEDIUM",
            })

        # Sort by net_return descending (all results preserved)
        variant_results.sort(key=lambda x: x["metrics"].get("net_return", 0.0), reverse=True)
        for i, v in enumerate(variant_results):
            v["rank"] = i + 1

        # Checks
        checks: dict = {}

        # Single-point performance
        if len(variant_results) > 0:
            stable_count = sum(1 for v in variant_results if v["stability"] == "STABLE")
            checks["single_point_performance"] = {
                "stable_variants": stable_count,
                "total_variants": len(variant_results),
                "stable_ratio": round(stable_count / len(variant_results), 4) if variant_results else 0.0,
                "pass": stable_count / len(variant_results) >= 0.5 if variant_results else False,
            }

        # Cliff risk
        cliff_variants = [v for v in variant_results if v["cliff_risk"]]
        checks["cliff_risk"] = {
            "cliff_variant_count": len(cliff_variants),
            "pass": len(cliff_variants) == 0,
        }

        # Flat region
        # If most variants cluster near baseline, it's a flat region (good)
        if variant_results:
            small_delta = sum(1 for v in variant_results if abs(v["delta_vs_baseline"]["expectancy"]) < 0.005)
            flat_region_width = small_delta
            checks["flat_region"] = {
                "flat_region_width": flat_region_width,
                "pass": flat_region_width > 0,
            }

        warnings = []
        if not parameter_variants:
            warnings.append("NO_PARAMETER_VARIANTS")
        if len(cliff_variants) > 0:
            warnings.append(f"CLIFF_RISK_IN_{len(cliff_variants)}_VARIANTS")

        return {
            "status": "PASS" if all(c.get("pass", True) for c in checks.values()) else "PARAMETER_SENSITIVE",
            "baseline_metrics": baseline_metrics,
            "parameter_set": [v["params"] for v in variant_results],
            "variants": variant_results,
            "checks": checks,
            "warnings": warnings,
        }
