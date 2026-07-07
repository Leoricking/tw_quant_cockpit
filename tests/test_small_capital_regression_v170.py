"""tests/test_small_capital_regression_v170.py — regression tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.version_v170 import VERSION, KNOWN_RELEASE_NAMES
from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
    compute_scorecard, SCORE_WEIGHTS,
)
from paper_trading.small_capital_strategy.position_sizing_v170 import (
    compute_position_size, PositionSizingInput,
)
from paper_trading.small_capital_strategy.enums_v170 import AllocationBucket, SmallCapitalGrade

TEMPLATE_ID = "small_capital_300k_v170"


def test_version_unchanged():
    assert VERSION == "1.7.0"


def test_known_release_names_minimum_count():
    assert len(KNOWN_RELEASE_NAMES) >= 10


def test_position_sizing_formula_stable():
    inp = PositionSizingInput(
        symbol="2330",
        capital_twd=300000.0,
        max_loss_amount=3000.0,
        stop_loss_pct=0.06,
        bucket=AllocationBucket.MAIN_THEME_SWING,
        bucket_remaining_budget=105000.0,
    )
    result = compute_position_size(inp)
    assert abs(result.position_size_twd - 50000.0) < 1.0


def test_score_weights_stable():
    assert SCORE_WEIGHTS["risk_budget_compliance"] == 25
    assert SCORE_WEIGHTS["position_sizing_correctness"] == 20
    assert SCORE_WEIGHTS["safety_compliance"] == 5
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_grade_thresholds_stable():
    sc_a = compute_scorecard(TEMPLATE_ID, {k: 1.0 for k in SCORE_WEIGHTS})
    assert sc_a.grade == SmallCapitalGrade.A

    sc_b = compute_scorecard(TEMPLATE_ID, {k: 0.75 for k in SCORE_WEIGHTS})
    assert sc_b.grade == SmallCapitalGrade.B

    sc_c = compute_scorecard(TEMPLATE_ID, {k: 0.6 for k in SCORE_WEIGHTS})
    assert sc_c.grade == SmallCapitalGrade.C

    sc_f = compute_scorecard(TEMPLATE_ID, {k: 0.3 for k in SCORE_WEIGHTS})
    assert sc_f.grade == SmallCapitalGrade.F


def test_no_grade_a_plus():
    assert not hasattr(SmallCapitalGrade, "A_PLUS")


def test_safety_flags_never_enable_real():
    from paper_trading.small_capital_strategy.safety_v170 import get_safety_flags
    flags = get_safety_flags()
    dangerous = [
        "LIVE_FALLBACK_ENABLED", "BROKER_ENABLED", "REAL_ACCOUNT_ENABLED",
        "REAL_ORDER_ENABLED", "PRODUCTION_TRADING_ENABLED",
        "AUTO_ORDER_ENABLED", "MARGIN_ENABLED",
        "DAY_TRADING_PRIMARY_ENABLED",
    ]
    for key in dangerous:
        assert flags.get(key) is False, f"Dangerous flag enabled: {key}"


def test_backward_compat_all_prior_versions_known():
    expected = [
        "Small Capital Growth Strategy Template",
        "Stable Rollup Compatibility Hotfix",
        "Live Paper Trading Stable Rollup",
        "Operational Integration Hardening",
        "Paper Performance Attribution",
    ]
    for name in expected:
        assert name in KNOWN_RELEASE_NAMES, f"Missing: {name}"


def test_paper_simulation_never_real():
    from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
        get_simulation_safety_summary,
    )
    safety = get_simulation_safety_summary()
    assert safety["real_execution_enabled"] is False
    assert safety["broker_connected"] is False
    assert safety["live_account_enabled"] is False


def test_fixture_schema_markers_unchanged():
    from paper_trading.small_capital_strategy.fixture_schema_v170 import REQUIRED_MARKERS
    assert len(REQUIRED_MARKERS) == 10
    assert all(v is True for v in REQUIRED_MARKERS.values())


def test_scenario_registry_count_stable():
    from paper_trading.small_capital_strategy.scenario_registry_v170 import SCENARIO_REGISTRY
    assert len(SCENARIO_REGISTRY) == 80


def test_fixture_registry_count_stable():
    from paper_trading.small_capital_strategy.fixture_registry_v170 import count_fixtures
    assert count_fixtures() == 80
