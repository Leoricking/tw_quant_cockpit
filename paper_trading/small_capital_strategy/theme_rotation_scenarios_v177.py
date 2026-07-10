"""
paper_trading/small_capital_strategy/theme_rotation_scenarios_v177.py
Test scenarios for Theme Rotation Scanner v1.7.7. 65+ scenarios.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def _sc(
    sid: str,
    name: str,
    desc: str,
    theme: str,
    expected_grade: str,
) -> Dict[str, Any]:
    return {
        "id": sid,
        "name": name,
        "description": desc,
        "theme": theme,
        "expected_grade": expected_grade,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
    }


_SCENARIOS: List[Dict[str, Any]] = [
    # AI_SERVER scenarios (6)
    _sc("SC177-001", "ai_server_leader",        "AI Server theme with breadth >80%, LEADER",        "AI_SERVER",               "LEADER"),
    _sc("SC177-002", "ai_server_strong",         "AI Server theme with breadth 65-79%, STRONG",      "AI_SERVER",               "STRONG"),
    _sc("SC177-003", "ai_server_watch",          "AI Server theme with breadth 50-64%, WATCH",       "AI_SERVER",               "WATCH"),
    _sc("SC177-004", "ai_server_weak",           "AI Server theme with breadth 35-49%, WEAK",        "AI_SERVER",               "WEAK"),
    _sc("SC177-005", "ai_server_excluded",       "AI Server theme with breadth <35%, EXCLUDED",      "AI_SERVER",               "EXCLUDED"),
    _sc("SC177-006", "ai_server_overheated",     "AI Server overheated, downgrade one level",        "AI_SERVER",               "STRONG"),

    # ASIC scenarios (4)
    _sc("SC177-007", "asic_leader",              "ASIC theme strong breadth, LEADER",                "ASIC",                    "LEADER"),
    _sc("SC177-008", "asic_margin_risk",         "ASIC with margin risk, downgrade",                 "ASIC",                    "WATCH"),
    _sc("SC177-009", "asic_single_stock",        "ASIC only one leader stock, cap at STRONG",        "ASIC",                    "STRONG"),
    _sc("SC177-010", "asic_weak_breadth",        "ASIC low breadth, WEAK",                           "ASIC",                    "WEAK"),

    # GPU_SERVER scenarios (4)
    _sc("SC177-011", "gpu_server_leader",        "GPU Server high momentum, LEADER",                 "GPU_SERVER",              "LEADER"),
    _sc("SC177-012", "gpu_server_risk_off",      "GPU Server in RISK_OFF regime, cap at WATCH",      "GPU_SERVER",              "WATCH"),
    _sc("SC177-013", "gpu_server_continuation",  "GPU Server 5 consecutive up days",                 "GPU_SERVER",              "STRONG"),
    _sc("SC177-014", "gpu_server_excluded",      "GPU Server very low breadth",                      "GPU_SERVER",              "EXCLUDED"),

    # COOLING scenarios (3)
    _sc("SC177-015", "cooling_leader",           "Cooling theme breakout, LEADER",                   "COOLING",                 "LEADER"),
    _sc("SC177-016", "cooling_watch",            "Cooling theme neutral, WATCH",                     "COOLING",                 "WATCH"),
    _sc("SC177-017", "cooling_excluded",         "Cooling theme declining, EXCLUDED",                "COOLING",                 "EXCLUDED"),

    # POWER_SUPPLY scenarios (3)
    _sc("SC177-018", "power_supply_leader",      "Power Supply theme rising, LEADER",                "POWER_SUPPLY",            "LEADER"),
    _sc("SC177-019", "power_supply_strong",      "Power Supply institutional buying, STRONG",        "POWER_SUPPLY",            "STRONG"),
    _sc("SC177-020", "power_supply_weak",        "Power Supply declining momentum, WEAK",            "POWER_SUPPLY",            "WEAK"),

    # PCB scenarios (3)
    _sc("SC177-021", "pcb_leader",               "PCB theme strong breadth, LEADER",                 "PCB",                     "LEADER"),
    _sc("SC177-022", "pcb_watch",                "PCB theme moderate breadth, WATCH",                "PCB",                     "WATCH"),
    _sc("SC177-023", "pcb_weak",                 "PCB theme low breadth, WEAK",                      "PCB",                     "WEAK"),

    # CCL scenarios (3)
    _sc("SC177-024", "ccl_leader",               "CCL theme high volume expansion, LEADER",          "CCL",                     "LEADER"),
    _sc("SC177-025", "ccl_strong",               "CCL moderate momentum, STRONG",                    "CCL",                     "STRONG"),
    _sc("SC177-026", "ccl_excluded",             "CCL very weak, EXCLUDED",                          "CCL",                     "EXCLUDED"),

    # HIGH_SPEED_TRANSMISSION scenarios (3)
    _sc("SC177-027", "hst_leader",               "High Speed Transmission new highs, LEADER",        "HIGH_SPEED_TRANSMISSION", "LEADER"),
    _sc("SC177-028", "hst_watch",                "High Speed Transmission sideways, WATCH",          "HIGH_SPEED_TRANSMISSION", "WATCH"),
    _sc("SC177-029", "hst_weak",                 "High Speed Transmission selling pressure, WEAK",   "HIGH_SPEED_TRANSMISSION", "WEAK"),

    # SEMICONDUCTOR scenarios (4)
    _sc("SC177-030", "semi_leader",              "Semiconductor all MA above, LEADER",               "SEMICONDUCTOR",           "LEADER"),
    _sc("SC177-031", "semi_strong",              "Semiconductor above MA20, STRONG",                 "SEMICONDUCTOR",           "STRONG"),
    _sc("SC177-032", "semi_watch",               "Semiconductor mixed signals, WATCH",               "SEMICONDUCTOR",           "WATCH"),
    _sc("SC177-033", "semi_overheated",          "Semiconductor overheated, downgraded",             "SEMICONDUCTOR",           "WATCH"),

    # ADVANCED_PACKAGING scenarios (3)
    _sc("SC177-034", "adv_pkg_leader",           "Advanced Packaging strong trend, LEADER",          "ADVANCED_PACKAGING",      "LEADER"),
    _sc("SC177-035", "adv_pkg_watch",            "Advanced Packaging consolidating, WATCH",          "ADVANCED_PACKAGING",      "WATCH"),
    _sc("SC177-036", "adv_pkg_excluded",         "Advanced Packaging breaking down, EXCLUDED",       "ADVANCED_PACKAGING",      "EXCLUDED"),

    # ROBOTICS scenarios (3)
    _sc("SC177-037", "robotics_leader",          "Robotics theme emerging, LEADER",                  "ROBOTICS",                "LEADER"),
    _sc("SC177-038", "robotics_strong",          "Robotics steady uptrend, STRONG",                  "ROBOTICS",                "STRONG"),
    _sc("SC177-039", "robotics_weak",            "Robotics theme losing steam, WEAK",                "ROBOTICS",                "WEAK"),

    # EDGE_AI scenarios (3)
    _sc("SC177-040", "edge_ai_leader",           "Edge AI theme breakout, LEADER",                   "EDGE_AI",                 "LEADER"),
    _sc("SC177-041", "edge_ai_watch",            "Edge AI early stage, WATCH",                       "EDGE_AI",                 "WATCH"),
    _sc("SC177-042", "edge_ai_excluded",         "Edge AI failed breakout, EXCLUDED",                "EDGE_AI",                 "EXCLUDED"),

    # EV scenarios (3)
    _sc("SC177-043", "ev_leader",                "EV theme positive regime, LEADER",                 "EV",                      "LEADER"),
    _sc("SC177-044", "ev_strong",                "EV moderate strength, STRONG",                     "EV",                      "STRONG"),
    _sc("SC177-045", "ev_weak",                  "EV theme declining, WEAK",                         "EV",                      "WEAK"),

    # ENERGY_STORAGE scenarios (3)
    _sc("SC177-046", "energy_storage_leader",    "Energy Storage high institutional buy, LEADER",    "ENERGY_STORAGE",          "LEADER"),
    _sc("SC177-047", "energy_storage_watch",     "Energy Storage mixed, WATCH",                      "ENERGY_STORAGE",          "WATCH"),
    _sc("SC177-048", "energy_storage_excluded",  "Energy Storage sector rotation out, EXCLUDED",     "ENERGY_STORAGE",          "EXCLUDED"),

    # FINANCIAL scenarios (3)
    _sc("SC177-049", "financial_strong",         "Financial theme stabilizing, STRONG",               "FINANCIAL",               "STRONG"),
    _sc("SC177-050", "financial_watch",          "Financial moderate activity, WATCH",                "FINANCIAL",               "WATCH"),
    _sc("SC177-051", "financial_excluded",       "Financial under distribution, EXCLUDED",            "FINANCIAL",               "EXCLUDED"),

    # SHIPPING scenarios (3)
    _sc("SC177-052", "shipping_leader",          "Shipping theme spike, LEADER",                     "SHIPPING",                "LEADER"),
    _sc("SC177-053", "shipping_watch",           "Shipping neutral, WATCH",                          "SHIPPING",                "WATCH"),
    _sc("SC177-054", "shipping_weak",            "Shipping declining rates, WEAK",                   "SHIPPING",                "WEAK"),

    # BIOTECH scenarios (3)
    _sc("SC177-055", "biotech_strong",           "Biotech FDA catalyst, STRONG",                     "BIOTECH",                 "STRONG"),
    _sc("SC177-056", "biotech_watch",            "Biotech mixed data, WATCH",                        "BIOTECH",                 "WATCH"),
    _sc("SC177-057", "biotech_excluded",         "Biotech sector rotation out, EXCLUDED",            "BIOTECH",                 "EXCLUDED"),

    # Market regime cap scenarios (4)
    _sc("SC177-058", "risk_off_cap_leader",      "LEADER grade capped to WATCH in RISK_OFF",         "AI_SERVER",               "WATCH"),
    _sc("SC177-059", "risk_off_cap_strong",      "STRONG grade capped to WATCH in RISK_OFF",         "SEMICONDUCTOR",           "WATCH"),
    _sc("SC177-060", "bull_no_cap",              "LEADER stays LEADER in BULL regime",               "GPU_SERVER",              "LEADER"),
    _sc("SC177-061", "bear_watch_ok",            "WATCH stays WATCH in BEAR regime",                 "PCB",                     "WATCH"),

    # Ranking scenarios (4)
    _sc("SC177-062", "rank_top_theme",           "Top ranked theme is AI_SERVER",                    "AI_SERVER",               "LEADER"),
    _sc("SC177-063", "rank_second_theme",        "Second ranked theme GPU_SERVER",                   "GPU_SERVER",              "STRONG"),
    _sc("SC177-064", "rank_tie_breaking",        "Tie breaking by score",                            "SEMICONDUCTOR",           "STRONG"),
    _sc("SC177-065", "rank_excluded_last",       "EXCLUDED always ranked last",                      "UNKNOWN",                 "EXCLUDED"),

    # Watchlist eligibility scenarios (3)
    _sc("SC177-066", "watchlist_leader_eligible", "LEADER grade is eligible for watchlist",          "AI_SERVER",               "LEADER"),
    _sc("SC177-067", "watchlist_strong_eligible", "STRONG grade is eligible for watchlist",          "GPU_SERVER",              "STRONG"),
    _sc("SC177-068", "watchlist_watch_ineligible","WATCH grade is NOT eligible for watchlist",       "PCB",                     "WATCH"),
]


def get_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(_SCENARIOS)


def count_scenarios() -> int:
    """Return number of scenarios."""
    return len(_SCENARIOS)


def get_scenario_by_id(sid: str) -> Optional[Dict[str, Any]]:
    """Return scenario by id, or None if not found."""
    for s in _SCENARIOS:
        if s["id"] == sid:
            return s
    return None
