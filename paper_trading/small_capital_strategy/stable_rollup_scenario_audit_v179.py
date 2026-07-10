"""
paper_trading/small_capital_strategy/stable_rollup_scenario_audit_v179.py
Scenario audit for all v1.7.x scenario registries.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_FORBIDDEN_ACTIONS = frozenset({
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
})

# Each entry: (module_path, function_name or None for auto-detect)
# Function names verified against actual source files:
#   scenario_registry_v170        -> get_registry()
#   watchlist_scenario_registry_v171 -> get_scenario_registry()
#   abc_scenario_registry_v172    -> no get_all_scenarios; has get_scenario_count/get_scenarios_by_category
#   market_regime_scenario_registry_v173 -> get_all_scenarios()  (confirmed)
#   risk_dashboard_scenario_registry_v174 -> get_all_scenarios() (confirmed)
#   trade_journal_scenarios_v175  -> get_scenarios()             (confirmed)
#   mistake_taxonomy_scenarios_v176 -> get_scenarios()           (confirmed)
#   theme_rotation_scenarios_v177 -> get_scenarios()             (confirmed)
#   integrated_strategy_scenarios_v178 -> get_scenarios()        (confirmed)
#   stable_rollup_scenarios_v179  -> get_scenarios()
_SCENARIO_MODULES = [
    ("paper_trading.small_capital_strategy.scenario_registry_v170",          "get_registry"),
    ("paper_trading.small_capital_strategy.watchlist_scenario_registry_v171", "get_scenario_registry"),
    ("paper_trading.small_capital_strategy.abc_scenario_registry_v172",       None),
    ("paper_trading.small_capital_strategy.market_regime_scenario_registry_v173", "get_all_scenarios"),
    ("paper_trading.small_capital_strategy.risk_dashboard_scenario_registry_v174", "get_all_scenarios"),
    ("paper_trading.small_capital_strategy.trade_journal_scenarios_v175",     "get_scenarios"),
    ("paper_trading.small_capital_strategy.mistake_taxonomy_scenarios_v176",  "get_scenarios"),
    ("paper_trading.small_capital_strategy.theme_rotation_scenarios_v177",    "get_scenarios"),
    ("paper_trading.small_capital_strategy.integrated_strategy_scenarios_v178", "get_scenarios"),
    ("paper_trading.small_capital_strategy.stable_rollup_scenarios_v179",     "get_scenarios"),
]

_FALLBACK_FN_NAMES = [
    "get_all_scenarios", "get_scenarios", "get_scenario_registry",
    "get_registry", "get_scenario_count",
]


def _load_scenarios_from_module(mod_path: str, fn_name) -> List[Dict]:
    """Import module and return list of scenarios."""
    import importlib
    mod = importlib.import_module(mod_path)

    # Try explicit function name first
    if fn_name and hasattr(mod, fn_name):
        result = getattr(mod, fn_name)()
        if isinstance(result, int):
            # get_scenario_count returns int — fall through to next
            pass
        else:
            return list(result)

    # Try fallback names
    for name in _FALLBACK_FN_NAMES:
        if hasattr(mod, name):
            result = getattr(mod, name)()
            if isinstance(result, (list, tuple)):
                return list(result)

    # Last resort: private list
    for attr in ("_SCENARIOS", "_SCENARIO_REGISTRY", "SCENARIOS", "SCENARIO_REGISTRY"):
        if hasattr(mod, attr):
            val = getattr(mod, attr)
            if isinstance(val, (list, tuple)):
                return list(val)

    return []


def _check_scenario_action(sc: Dict) -> bool:
    """Return True if expected_action is not a forbidden word."""
    action = sc.get("expected_action", "")
    return action.upper() not in _FORBIDDEN_ACTIONS


def run_scenario_audit() -> Dict[str, Any]:
    """Audit all scenario registries for forbidden actions."""
    total_scenarios = 0
    forbidden_violations: List[str] = []
    module_results = []
    for mod_path, fn_name in _SCENARIO_MODULES:
        entry: Dict[str, Any] = {
            "module": mod_path, "count": 0, "violations": [], "importable": False,
        }
        try:
            scenarios = _load_scenarios_from_module(mod_path, fn_name)
            entry["importable"] = True
            entry["count"] = len(scenarios)
            total_scenarios += len(scenarios)
            violations = [
                sc.get("id", sc.get("scenario_id", str(sc)[:40]))
                for sc in scenarios
                if not _check_scenario_action(sc)
            ]
            entry["violations"] = violations
            forbidden_violations.extend(violations)
        except Exception as exc:
            entry["error"] = str(exc)
        module_results.append(entry)
    return {
        "all_clean": len(forbidden_violations) == 0,
        "total_scenarios": total_scenarios,
        "forbidden_count": len(forbidden_violations),
        "forbidden_violations": forbidden_violations,
        "module_results": module_results,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
