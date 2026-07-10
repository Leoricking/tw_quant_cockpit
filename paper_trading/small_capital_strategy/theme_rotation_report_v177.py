"""
paper_trading/small_capital_strategy/theme_rotation_report_v177.py
Report builder for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"

_REPORT_SECTIONS = [
    "executive_summary",
    "theme_ranking",
    "leader_analysis",
    "risk_flags",
    "watchlist_candidates",
]


def get_report_sections() -> List[str]:
    """Return list of standard report section names."""
    return list(_REPORT_SECTIONS)


def build_report(dashboard: object) -> object:
    """Build a ThemeRotationReport from a ThemeRotationDashboard."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationReport

    top_themes = getattr(dashboard, "top_themes", [])
    if top_themes:
        top_theme = getattr(top_themes[0], "theme", ThemeCategory.UNKNOWN)
    else:
        top_theme = ThemeCategory.UNKNOWN

    return ThemeRotationReport(
        date=getattr(dashboard, "date", ""),
        sections=list(_REPORT_SECTIONS),
        top_theme=top_theme,
        report_format="text",
    )
