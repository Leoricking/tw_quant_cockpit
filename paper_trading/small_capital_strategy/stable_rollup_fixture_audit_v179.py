"""
paper_trading/small_capital_strategy/stable_rollup_fixture_audit_v179.py
Fixture audit for all v1.7.x fixture registries.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_REQUIRED_SAFETY_KEYS = [
    "paper_only", "research_only", "no_real_orders",
    "no_broker", "not_investment_advice", "demo_only", "not_for_production",
]

# Minimal required keys for older fixture registries (v1.7.0-v1.7.8)
_MINIMAL_SAFETY_KEYS = ["paper_only", "no_real_orders"]

# Each entry: (module_path, function_name, strict_check)
# strict_check=True: full 7-key audit (v1.7.9 fixtures)
# strict_check=False: minimal audit (older versions)
_FIXTURE_MODULES = [
    ("paper_trading.small_capital_strategy.fixture_registry_v170",           None,              False),
    ("paper_trading.small_capital_strategy.watchlist_fixture_registry_v171", "get_fixture_registry", False),
    ("paper_trading.small_capital_strategy.abc_fixture_registry_v172",       None,              False),
    ("paper_trading.small_capital_strategy.market_regime_fixture_registry_v173", "get_all_fixtures", False),
    ("paper_trading.small_capital_strategy.risk_dashboard_fixture_registry_v174", "get_all_fixtures", False),
    ("paper_trading.small_capital_strategy.trade_journal_fixture_registry_v175", "get_fixtures", False),
    ("paper_trading.small_capital_strategy.mistake_taxonomy_fixture_registry_v176", "get_fixtures", False),
    ("paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177", "get_fixtures", False),
    ("paper_trading.small_capital_strategy.integrated_strategy_fixture_registry_v178", "get_fixtures", False),
    ("paper_trading.small_capital_strategy.stable_rollup_fixture_registry_v179", "get_all_fixtures", True),
]

# Candidate function names to try if explicit name is None
_FALLBACK_FN_NAMES = [
    "get_all_fixtures", "get_fixtures", "get_fixture_registry",
    "get_registry",
]


def _load_fixtures_from_module(mod_path: str, fn_name) -> List[Dict]:
    """Import module and return list of fixtures using fn_name or fallback."""
    import importlib
    mod = importlib.import_module(mod_path)

    # Try explicit function name first
    if fn_name and hasattr(mod, fn_name):
        return list(getattr(mod, fn_name)())

    # Try fallback names
    for name in _FALLBACK_FN_NAMES:
        if hasattr(mod, name):
            return list(getattr(mod, name)())

    # Last resort: look for _FIXTURE_REGISTRY or _FIXTURES private list
    for attr in ("_FIXTURE_REGISTRY", "_FIXTURES", "FIXTURE_REGISTRY", "FIXTURES"):
        if hasattr(mod, attr):
            val = getattr(mod, attr)
            if isinstance(val, (list, tuple)):
                return list(val)

    return []


def _check_fixtures_safe(fixtures: List[Dict], strict: bool = True) -> List[str]:
    """Return list of fixture IDs missing required safety keys."""
    keys = _REQUIRED_SAFETY_KEYS if strict else _MINIMAL_SAFETY_KEYS
    missing = []
    for fx in fixtures:
        for key in keys:
            if not fx.get(key):
                fid = fx.get("fixture_id", fx.get("id", str(fx)[:40]))
                missing.append(f"{fid}:{key}")
    return missing


def run_fixture_audit() -> Dict[str, Any]:
    """Audit all fixture registries for safety compliance."""
    total_fixtures = 0
    all_violations: List[str] = []
    module_results = []
    for mod_path, fn_name, strict in _FIXTURE_MODULES:
        entry: Dict[str, Any] = {
            "module": mod_path, "count": 0, "violations": [], "importable": False,
        }
        try:
            fixtures = _load_fixtures_from_module(mod_path, fn_name)
            entry["importable"] = True
            entry["count"] = len(fixtures)
            total_fixtures += len(fixtures)
            violations = _check_fixtures_safe(fixtures, strict=strict)
            entry["violations"] = violations
            all_violations.extend(violations)
        except Exception as exc:
            entry["error"] = str(exc)
        module_results.append(entry)
    return {
        "all_safe": len(all_violations) == 0,
        "total_fixtures": total_fixtures,
        "violation_count": len(all_violations),
        "violations": all_violations,
        "module_results": module_results,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_required_safety_keys() -> List[str]:
    return list(_REQUIRED_SAFETY_KEYS)
