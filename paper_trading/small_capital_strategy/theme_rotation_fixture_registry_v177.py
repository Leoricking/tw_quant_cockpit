"""
paper_trading/small_capital_strategy/theme_rotation_fixture_registry_v177.py
Fixture registry for Theme Rotation Scanner v1.7.7. 65+ fixtures.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"
_LINEAGE = "paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177"


def _f(
    fid: str,
    symbol: str,
    theme: str,
    grade: str,
    breadth_score: float,
    momentum_score: float = 0.0,
    is_leader: bool = False,
) -> Dict[str, Any]:
    return {
        "id": fid,
        "symbol": symbol,
        "theme": theme,
        "grade": grade,
        "breadth_score": breadth_score,
        "momentum_score": momentum_score,
        "is_leader": is_leader,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "source_lineage": _LINEAGE,
    }


_FIXTURES: List[Dict[str, Any]] = [
    # AI_SERVER fixtures (8)
    _f("F177-001", "2317", "AI_SERVER", "LEADER",   92.0, 85.0, True),
    _f("F177-002", "3711", "AI_SERVER", "LEADER",   88.0, 80.0, True),
    _f("F177-003", "4938", "AI_SERVER", "STRONG",   72.0, 65.0, False),
    _f("F177-004", "2382", "AI_SERVER", "STRONG",   68.0, 60.0, False),
    _f("F177-005", "3081", "AI_SERVER", "WATCH",    55.0, 45.0, False),
    _f("F177-006", "6770", "AI_SERVER", "WATCH",    52.0, 40.0, False),
    _f("F177-007", "3443", "AI_SERVER", "WEAK",     38.0, 25.0, False),
    _f("F177-008", "5347", "AI_SERVER", "EXCLUDED", 20.0, 10.0, False),

    # SEMICONDUCTOR fixtures (7)
    _f("F177-009", "2330", "SEMICONDUCTOR", "LEADER",   90.0, 82.0, True),
    _f("F177-010", "2454", "SEMICONDUCTOR", "LEADER",   85.0, 78.0, True),
    _f("F177-011", "3034", "SEMICONDUCTOR", "STRONG",   70.0, 62.0, False),
    _f("F177-012", "2303", "SEMICONDUCTOR", "STRONG",   66.0, 58.0, False),
    _f("F177-013", "2344", "SEMICONDUCTOR", "WATCH",    53.0, 42.0, False),
    _f("F177-014", "2449", "SEMICONDUCTOR", "WEAK",     40.0, 28.0, False),
    _f("F177-015", "2408", "SEMICONDUCTOR", "EXCLUDED", 22.0, 12.0, False),

    # GPU_SERVER fixtures (5)
    _f("F177-016", "2308", "GPU_SERVER", "LEADER",   88.0, 80.0, True),
    _f("F177-017", "2376", "GPU_SERVER", "STRONG",   74.0, 66.0, False),
    _f("F177-018", "6683", "GPU_SERVER", "STRONG",   68.0, 59.0, False),
    _f("F177-019", "3017", "GPU_SERVER", "WATCH",    56.0, 44.0, False),
    _f("F177-020", "2351", "GPU_SERVER", "WEAK",     36.0, 22.0, False),

    # COOLING fixtures (4)
    _f("F177-021", "6669", "COOLING", "LEADER",   86.0, 79.0, True),
    _f("F177-022", "3519", "COOLING", "STRONG",   70.0, 63.0, False),
    _f("F177-023", "2465", "COOLING", "WATCH",    54.0, 43.0, False),
    _f("F177-024", "1590", "COOLING", "WEAK",     37.0, 24.0, False),

    # POWER_SUPPLY fixtures (4)
    _f("F177-025", "6770", "POWER_SUPPLY", "LEADER",   84.0, 77.0, True),
    _f("F177-026", "3019", "POWER_SUPPLY", "STRONG",   69.0, 61.0, False),
    _f("F177-027", "6488", "POWER_SUPPLY", "WATCH",    53.0, 41.0, False),
    _f("F177-028", "1503", "POWER_SUPPLY", "EXCLUDED", 21.0, 11.0, False),

    # PCB fixtures (4)
    _f("F177-029", "2395", "PCB", "LEADER",   83.0, 76.0, True),
    _f("F177-030", "3037", "PCB", "STRONG",   67.0, 57.0, False),
    _f("F177-031", "2441", "PCB", "WATCH",    51.0, 39.0, False),
    _f("F177-032", "6274", "PCB", "WEAK",     35.0, 21.0, False),

    # CCL fixtures (3)
    _f("F177-033", "2345", "CCL", "LEADER",   82.0, 75.0, True),
    _f("F177-034", "4904", "CCL", "STRONG",   66.0, 56.0, False),
    _f("F177-035", "1516", "CCL", "WATCH",    50.0, 38.0, False),

    # HIGH_SPEED_TRANSMISSION fixtures (4)
    _f("F177-036", "2412", "HIGH_SPEED_TRANSMISSION", "LEADER",   87.0, 79.0, True),
    _f("F177-037", "3008", "HIGH_SPEED_TRANSMISSION", "STRONG",   71.0, 63.0, False),
    _f("F177-038", "3045", "HIGH_SPEED_TRANSMISSION", "WATCH",    55.0, 43.0, False),
    _f("F177-039", "6443", "HIGH_SPEED_TRANSMISSION", "WEAK",     37.0, 23.0, False),

    # ADVANCED_PACKAGING fixtures (4)
    _f("F177-040", "3034", "ADVANCED_PACKAGING", "LEADER",   85.0, 78.0, True),
    _f("F177-041", "2474", "ADVANCED_PACKAGING", "STRONG",   70.0, 62.0, False),
    _f("F177-042", "3711", "ADVANCED_PACKAGING", "WATCH",    53.0, 41.0, False),
    _f("F177-043", "2379", "ADVANCED_PACKAGING", "EXCLUDED", 20.0,  9.0, False),

    # ROBOTICS fixtures (3)
    _f("F177-044", "2049", "ROBOTICS", "LEADER",   81.0, 74.0, True),
    _f("F177-045", "1590", "ROBOTICS", "STRONG",   66.0, 55.0, False),
    _f("F177-046", "2059", "ROBOTICS", "WATCH",    50.0, 37.0, False),

    # EDGE_AI fixtures (3)
    _f("F177-047", "5274", "EDGE_AI", "LEADER",   80.0, 73.0, True),
    _f("F177-048", "6716", "EDGE_AI", "WATCH",    52.0, 40.0, False),
    _f("F177-049", "3686", "EDGE_AI", "EXCLUDED", 19.0,  8.0, False),

    # ASIC fixtures (3)
    _f("F177-050", "2379", "ASIC", "LEADER",   83.0, 76.0, True),
    _f("F177-051", "3029", "ASIC", "STRONG",   67.0, 56.0, False),
    _f("F177-052", "6271", "ASIC", "WEAK",     36.0, 22.0, False),

    # EV fixtures (3)
    _f("F177-053", "2207", "EV", "STRONG",   68.0, 60.0, False),
    _f("F177-054", "5483", "EV", "WATCH",    52.0, 40.0, False),
    _f("F177-055", "1513", "EV", "WEAK",     38.0, 25.0, False),

    # ENERGY_STORAGE fixtures (3)
    _f("F177-056", "1303", "ENERGY_STORAGE", "STRONG",   69.0, 61.0, False),
    _f("F177-057", "6409", "ENERGY_STORAGE", "WATCH",    53.0, 41.0, False),
    _f("F177-058", "1504", "ENERGY_STORAGE", "EXCLUDED", 20.0,  9.0, False),

    # FINANCIAL fixtures (3)
    _f("F177-059", "2882", "FINANCIAL", "WATCH",    55.0, 42.0, False),
    _f("F177-060", "2886", "FINANCIAL", "WATCH",    52.0, 39.0, False),
    _f("F177-061", "2891", "FINANCIAL", "WEAK",     37.0, 22.0, False),

    # SHIPPING fixtures (3)
    _f("F177-062", "2603", "SHIPPING", "STRONG",   70.0, 63.0, False),
    _f("F177-063", "2615", "SHIPPING", "WATCH",    54.0, 42.0, False),
    _f("F177-064", "2609", "SHIPPING", "WEAK",     38.0, 24.0, False),

    # BIOTECH fixtures (3)
    _f("F177-065", "4161", "BIOTECH", "STRONG",   68.0, 59.0, False),
    _f("F177-066", "6446", "BIOTECH", "WATCH",    52.0, 40.0, False),
    _f("F177-067", "4729", "BIOTECH", "EXCLUDED", 21.0, 10.0, False),
]


def get_fixtures() -> List[Dict[str, Any]]:
    """Return all fixtures."""
    return list(_FIXTURES)


def count_fixtures() -> int:
    """Return number of fixtures."""
    return len(_FIXTURES)


def validate_registry() -> Dict[str, Any]:
    """Validate all fixtures. Returns {valid, count, errors}."""
    from paper_trading.small_capital_strategy.theme_rotation_fixture_schema_v177 import validate_fixture
    errors: List[str] = []
    for f in _FIXTURES:
        result = validate_fixture(f)
        if not result["valid"]:
            errors.extend([f"{f['id']}: {e}" for e in result["errors"]])
    return {
        "valid": len(errors) == 0,
        "all_valid": len(errors) == 0,
        "count": len(_FIXTURES),
        "errors": errors,
    }


def validate_all_fixtures() -> List[Dict[str, Any]]:
    """Return per-fixture validation results."""
    from paper_trading.small_capital_strategy.theme_rotation_fixture_schema_v177 import validate_fixture
    return [validate_fixture(f) for f in _FIXTURES]


def get_fixtures_by_theme(theme_name: str) -> List[Dict[str, Any]]:
    """Return fixtures filtered by theme name string."""
    return [f for f in _FIXTURES if f.get("theme") == theme_name]
