"""
paper_trading/small_capital_strategy/stable_rollup_cli_audit_v179.py
CLI audit for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_REQUIRED_STABLE_CMDS: List[str] = [
    "small-capital-stable-version",
    "small-capital-stable-manifest",
    "small-capital-stable-health",
    "small-capital-stable-gate",
    "small-capital-stable-safety",
    "small-capital-stable-compat",
    "small-capital-stable-cli-audit",
    "small-capital-stable-gui-audit",
    "small-capital-stable-fixture-audit",
    "small-capital-stable-scenario-audit",
    "small-capital-stable-regression-audit",
    "small-capital-stable-report",
]


def run_cli_audit() -> Dict[str, Any]:
    """Audit CLI command registry for stable rollup completeness."""
    from cli.command_registry import PROVIDER_COMMANDS
    registered = {c.name for c in PROVIDER_COMMANDS}
    missing = [cmd for cmd in _REQUIRED_STABLE_CMDS if cmd not in registered]
    present = [cmd for cmd in _REQUIRED_STABLE_CMDS if cmd in registered]
    return {
        "all_registered": len(missing) == 0,
        "registered_count": len(present),
        "missing_count": len(missing),
        "missing": missing,
        "present": present,
        "total_required": len(_REQUIRED_STABLE_CMDS),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_required_stable_commands() -> List[str]:
    return list(_REQUIRED_STABLE_CMDS)
