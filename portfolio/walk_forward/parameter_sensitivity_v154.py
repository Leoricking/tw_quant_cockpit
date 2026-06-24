"""
portfolio/walk_forward/parameter_sensitivity_v154.py — Parameter Sensitivity Analyzer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
selection_applied=False always. Grid: fixed, deterministic.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional

from portfolio.walk_forward.models_v154 import ParameterSensitivityResult

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
SENSITIVITY_VERSION = "1.5.4"

SUPPORTED_PARAMETERS = [
    "sizing_risk_pct",
    "stop_distance",
    "atr_multiplier",
    "max_position_weight",
    "max_cluster_weight",
    "drawdown_warning_threshold",
    "cash_reserve",
    "correlation_threshold",
]

# Cliff effect threshold: adjacent values differ by > 50% in return
CLIFF_EFFECT_THRESHOLD = 0.50


class ParameterSensitivityAnalyzer:
    """Analyze parameter sensitivity for walk-forward parameters."""

    def __init__(self):
        self.version = SENSITIVITY_VERSION

    def analyze(
        self,
        parameter_name: str,
        tested_values: List[Any],
        simulate_fn: Optional[Callable] = None,
    ) -> ParameterSensitivityResult:
        """
        Analyze sensitivity of a parameter.
        Grid: fixed, deterministic.
        selection_applied=False always.
        Detect cliff_effect if adjacent values differ by >50%.
        """
        if parameter_name not in SUPPORTED_PARAMETERS:
            return ParameterSensitivityResult(
                parameter_name=parameter_name,
                tested_values=tested_values,
                results_by_value={},
                local_stability=None,
                cliff_effect=False,
                selected_value=None,
                selection_applied=False,
                status="UNSUPPORTED_PARAMETER",
                metadata={"supported": SUPPORTED_PARAMETERS, "research_only": True},
            )

        # Run simulations (use simulate_fn if provided, else demo fixture)
        results_by_value: Dict[str, Any] = {}
        returns_list = []

        for val in tested_values:
            if simulate_fn is not None:
                result = simulate_fn(parameter_name, val)
            else:
                # Demo fixture: deterministic return based on value index
                idx = tested_values.index(val)
                demo_return = 0.05 + idx * 0.01 - (idx ** 2) * 0.002
                result = {"return": demo_return, "status": "VALID", "fixture": True}

            results_by_value[str(val)] = result
            r = result.get("return", 0.0) if isinstance(result, dict) else 0.0
            returns_list.append(r)

        # Detect cliff effect
        cliff_effect = False
        for i in range(len(returns_list) - 1):
            r_curr = returns_list[i]
            r_next = returns_list[i + 1]
            if abs(r_curr) > 1e-9:
                rel_change = abs(r_next - r_curr) / abs(r_curr)
                if rel_change > CLIFF_EFFECT_THRESHOLD:
                    cliff_effect = True
                    break

        # Local stability: std / mean of returns
        local_stability = None
        if len(returns_list) >= 2:
            mean_r = sum(returns_list) / len(returns_list)
            if abs(mean_r) > 1e-9:
                variance = sum((r - mean_r) ** 2 for r in returns_list) / len(returns_list)
                import math
                local_stability = 1.0 - min(math.sqrt(variance) / abs(mean_r), 1.0)

        return ParameterSensitivityResult(
            parameter_name=parameter_name,
            tested_values=tested_values,
            results_by_value=results_by_value,
            local_stability=local_stability,
            cliff_effect=cliff_effect,
            selected_value=None,      # Never auto-selected
            selection_applied=False,  # ALWAYS False
            status="VALID",
            metadata={
                "version": SENSITIVITY_VERSION,
                "cliff_threshold": CLIFF_EFFECT_THRESHOLD,
                "research_only": True,
                "selection_applied": False,
            },
        )
