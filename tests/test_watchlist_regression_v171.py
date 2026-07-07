"""tests/test_watchlist_regression_v171.py — regression tests for v1.7.1 (no v1.7.0 breakage)."""
import pytest


def test_v170_version_still_present():
    from paper_trading.small_capital_strategy.version_v170 import VERSION
    assert VERSION == "1.7.0"


def test_v170_known_releases_includes_v171():
    from paper_trading.small_capital_strategy.version_v170 import KNOWN_RELEASE_NAMES
    assert "Watchlist Strategy Layer" in KNOWN_RELEASE_NAMES


def test_v170_enums_still_importable():
    from paper_trading.small_capital_strategy.enums_v170 import WatchlistTier
    assert WatchlistTier.CORE is not None


def test_v170_safety_still_importable():
    from paper_trading.small_capital_strategy.safety_v170 import audit_safety
    result = audit_safety()
    assert isinstance(result, dict)


def test_v170_models_still_importable():
    from paper_trading.small_capital_strategy.models_v170 import AllocationBucket
    assert AllocationBucket is not None


def test_v171_does_not_override_v170_enums():
    from paper_trading.small_capital_strategy import enums_v170 as e170
    from paper_trading.small_capital_strategy import watchlist_enums_v171 as e171
    # v170 CORE still exists
    assert e170.WatchlistTier.CORE.value == "CORE"
    # v171 CORE also exists independently
    assert e171.WatchlistTier.CORE.value == "CORE"


def test_v171_theme_strength_adds_leading():
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
    assert ThemeStrength.LEADING is not None


def test_v170_theme_strength_no_leading():
    from paper_trading.small_capital_strategy.enums_v170 import ThemeStrength as TS170
    assert not hasattr(TS170, "LEADING")


def test_init_has_watchlist_safety_flags():
    import paper_trading.small_capital_strategy as pkg
    assert hasattr(pkg, "WATCHLIST_STRATEGY_AVAILABLE")
    assert pkg.WATCHLIST_STRATEGY_AVAILABLE is True


def test_init_watchlist_real_trading_disabled():
    import paper_trading.small_capital_strategy as pkg
    assert pkg.WATCHLIST_REAL_TRADING_ENABLED is False


def test_v171_schema_version_is_171():
    from paper_trading.small_capital_strategy.version_v171 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "171"


def test_v171_policy_version_contains_171():
    from paper_trading.small_capital_strategy.version_v171 import POLICY_VERSION
    assert "1.7.1" in POLICY_VERSION


def test_v171_component_count_25():
    from paper_trading.small_capital_strategy.version_v171 import COMPONENT_COUNT
    assert COMPONENT_COUNT == 25


def test_v170_health_still_runs():
    from paper_trading.small_capital_strategy.health_v170 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)
    assert result.get("all_passed") is True


def test_v170_gate_still_runs():
    from release.small_capital_growth_strategy_release_gate_v170 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)
    assert result.get("gate_passed") is True


def test_v171_watchlist_health_runs():
    from paper_trading.small_capital_strategy.watchlist_health_v171 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True


def test_v171_watchlist_gate_runs():
    from release.watchlist_strategy_layer_release_gate_v171 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True
