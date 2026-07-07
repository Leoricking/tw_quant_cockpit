"""
paper_trading/small_capital_strategy/capital_profile_v170.py
Capital profile for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import CapitalProfileType
from paper_trading.small_capital_strategy.models_v170 import CapitalProfile

# Canonical 300k template
TEMPLATE_300K_ID = "small_capital_300k_v170"
TEMPLATE_300K_CAPITAL = 300000.0
TEMPLATE_300K_MAX_LOSS_DEFAULT = 3000.0
TEMPLATE_300K_MAX_LOSS_MIN = 2400.0
TEMPLATE_300K_MAX_LOSS_MAX = 4500.0
TEMPLATE_300K_RISK_PCT_DEFAULT = 0.01   # 1.0%
TEMPLATE_300K_RISK_PCT_MIN = 0.008      # 0.8%
TEMPLATE_300K_RISK_PCT_MAX = 0.015      # 1.5%
TEMPLATE_300K_MAX_HOLDINGS_DEFAULT = 4
TEMPLATE_300K_MAX_HOLDINGS_MIN = 1
TEMPLATE_300K_MAX_HOLDINGS_MAX = 4


def get_300k_template() -> CapitalProfile:
    """Return the canonical 300k capital profile template."""
    return CapitalProfile(
        template_id=TEMPLATE_300K_ID,
        capital_twd=TEMPLATE_300K_CAPITAL,
        max_loss_default=TEMPLATE_300K_MAX_LOSS_DEFAULT,
        max_loss_min=TEMPLATE_300K_MAX_LOSS_MIN,
        max_loss_max=TEMPLATE_300K_MAX_LOSS_MAX,
        risk_pct_default=TEMPLATE_300K_RISK_PCT_DEFAULT,
        risk_pct_min=TEMPLATE_300K_RISK_PCT_MIN,
        risk_pct_max=TEMPLATE_300K_RISK_PCT_MAX,
        max_holdings_default=TEMPLATE_300K_MAX_HOLDINGS_DEFAULT,
        max_holdings_min=TEMPLATE_300K_MAX_HOLDINGS_MIN,
        max_holdings_max=TEMPLATE_300K_MAX_HOLDINGS_MAX,
        profile_type=CapitalProfileType.SMALL_300K,
    )


def validate_capital_profile(profile: CapitalProfile) -> Dict[str, Any]:
    """Validate a CapitalProfile. Returns {valid, issues}."""
    issues = []

    if profile.capital_twd <= 0:
        issues.append(f"capital_twd must be > 0, got {profile.capital_twd}")

    if profile.max_loss_min <= 0:
        issues.append(f"max_loss_min must be > 0, got {profile.max_loss_min}")

    if profile.max_loss_min > profile.max_loss_max:
        issues.append(
            f"max_loss_min ({profile.max_loss_min}) > max_loss_max ({profile.max_loss_max})"
        )

    if not (profile.max_loss_min <= profile.max_loss_default <= profile.max_loss_max):
        issues.append(
            f"max_loss_default {profile.max_loss_default} not in "
            f"[{profile.max_loss_min}, {profile.max_loss_max}]"
        )

    if profile.risk_pct_min <= 0:
        issues.append(f"risk_pct_min must be > 0, got {profile.risk_pct_min}")

    if profile.risk_pct_min > profile.risk_pct_max:
        issues.append(
            f"risk_pct_min ({profile.risk_pct_min}) > risk_pct_max ({profile.risk_pct_max})"
        )

    if not (profile.risk_pct_min <= profile.risk_pct_default <= profile.risk_pct_max):
        issues.append(
            f"risk_pct_default {profile.risk_pct_default} not in "
            f"[{profile.risk_pct_min}, {profile.risk_pct_max}]"
        )

    if profile.max_holdings_max > 4:
        issues.append(f"max_holdings_max must be <= 4, got {profile.max_holdings_max}")

    if profile.max_holdings_min < 1:
        issues.append(f"max_holdings_min must be >= 1, got {profile.max_holdings_min}")

    if not profile.paper_only:
        issues.append("paper_only must be True")

    if not profile.no_real_orders:
        issues.append("no_real_orders must be True")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "template_id": profile.template_id,
    }
