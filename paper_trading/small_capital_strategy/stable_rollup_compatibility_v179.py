"""
paper_trading/small_capital_strategy/stable_rollup_compatibility_v179.py
Backward compatibility checks for v1.7.0~v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import importlib
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_VERSION_MODULES = {
    "v1.7.0": ("paper_trading.small_capital_strategy.version_v170", "1.7.0"),
    "v1.7.1": ("paper_trading.small_capital_strategy.version_v171", "1.7.1"),
    "v1.7.2": ("paper_trading.small_capital_strategy.version_v172", "1.7.2"),
    "v1.7.3": ("paper_trading.small_capital_strategy.version_v173", "1.7.3"),
    "v1.7.4": ("paper_trading.small_capital_strategy.version_v174", "1.7.4"),
    "v1.7.5": ("paper_trading.small_capital_strategy.version_v175", "1.7.5"),
    "v1.7.6": ("paper_trading.small_capital_strategy.version_v176", "1.7.6"),
    "v1.7.7": ("paper_trading.small_capital_strategy.version_v177", "1.7.7"),
    "v1.7.8": ("paper_trading.small_capital_strategy.version_v178", "1.7.8"),
}


def check_version_importable(ver: str) -> Dict[str, Any]:
    mod_path, expected_ver = _VERSION_MODULES[ver]
    result = {"version": ver, "module": mod_path, "importable": False,
              "version_match": False, "safety_ok": False, "error": None,
              "paper_only": True, "research_only": True, "no_real_orders": True}
    try:
        mod = importlib.import_module(mod_path)
        result["importable"] = True
        result["version_match"] = getattr(mod, "VERSION", None) == expected_ver
        info = mod.get_version_info()
        result["safety_ok"] = (
            info.get("paper_only") is True and
            info.get("no_real_orders") is True and
            info.get("not_investment_advice") is True
        )
    except Exception as exc:
        result["error"] = str(exc)
    return result


def run_compatibility_check() -> Dict[str, Any]:
    """Check all v1.7.0~v1.7.8 versions are importable and backward compatible."""
    results = []
    all_pass = True
    for ver in sorted(_VERSION_MODULES.keys()):
        r = check_version_importable(ver)
        results.append(r)
        if not (r["importable"] and r["version_match"] and r["safety_ok"]):
            all_pass = False
    return {
        "all_compatible": all_pass,
        "versions_checked": len(results),
        "results": results,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def is_backward_compatible(ver: str) -> bool:
    r = check_version_importable(ver)
    return r["importable"] and r["version_match"] and r["safety_ok"]


def get_compatible_versions() -> List[str]:
    return [v for v in sorted(_VERSION_MODULES.keys()) if is_backward_compatible(v)]
