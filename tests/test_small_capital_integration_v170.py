"""tests/test_small_capital_integration_v170.py — integration tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import (
    MarketRegime, AllocationBucket, BuyPointType, StopLossType,
)
from paper_trading.small_capital_strategy.capital_profile_v170 import (
    get_300k_template, TEMPLATE_300K_ID,
)
from paper_trading.small_capital_strategy.risk_budget_v170 import compute_risk_budget
from paper_trading.small_capital_strategy.allocation_template_v170 import get_allocation_for_regime
from paper_trading.small_capital_strategy.market_regime_filter_v170 import get_regime_control
from paper_trading.small_capital_strategy.position_sizing_v170 import (
    compute_position_size, PositionSizingInput,
)
from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
    compute_scorecard, SCORE_WEIGHTS,
)
from paper_trading.small_capital_strategy.strategy_report_v170 import (
    build_report, to_markdown, to_json,
)
from paper_trading.small_capital_strategy.strategy_template_v170 import (
    build_300k_template, validate_strategy_template,
)
from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
    run_paper_simulation,
)
from paper_trading.small_capital_strategy.models_v170 import SmallCapitalSimulationInput


def test_end_to_end_bull_strategy():
    """Full pipeline: profile -> budget -> allocation -> sizing -> scorecard -> report."""
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, profile.capital_twd)
    regime = get_regime_control(MarketRegime.BULL)

    sizing_inp = PositionSizingInput(
        symbol="2330",
        capital_twd=profile.capital_twd,
        max_loss_amount=budget.max_loss_per_trade,
        stop_loss_pct=0.06,
        bucket=AllocationBucket.MAIN_THEME_SWING,
        bucket_remaining_budget=105000.0,
    )
    sizing = compute_position_size(sizing_inp)
    assert sizing.status == "VALID"
    assert abs(sizing.position_size_twd - 50000.0) < 1.0

    scorecard = compute_scorecard(TEMPLATE_300K_ID, {k: 0.9 for k in SCORE_WEIGHTS})
    report = build_report(TEMPLATE_300K_ID, scorecard)
    md = to_markdown(report)
    assert "Not Investment Advice" in md
    assert "1.7.0" in md


def test_paper_simulation_integration():
    sim_input = SmallCapitalSimulationInput(
        template_id=TEMPLATE_300K_ID,
        symbol="2330",
        buy_point_type=BuyPointType.A_10MA_PULLBACK,
        entry_price=500.0,
        stop_loss_pct=0.06,
        capital_twd=300000.0,
        regime=MarketRegime.BULL,
    )
    result = run_paper_simulation(sim_input)
    assert result.paper_only is True
    assert result.position_size_twd > 0
    assert result.stop_loss_price < 500.0


def test_strategy_template_full_pipeline():
    tmpl = build_300k_template(regime=MarketRegime.BULL)
    validation = validate_strategy_template(tmpl)
    assert validation["valid"] is True
    assert tmpl.paper_only is True
    assert tmpl.no_real_orders is True


def test_bear_regime_cash_constraint():
    alloc = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
    assert alloc.cash_pct >= 0.49

    regime = get_regime_control(MarketRegime.BEAR)
    assert regime.short_term_training_allowed is False


def test_safety_never_real_execution():
    from paper_trading.small_capital_strategy.safety_v170 import audit_safety
    audit = audit_safety()
    assert audit["all_safe"] is True
    flags = audit["flags"]
    assert flags["LIVE_FALLBACK_ENABLED"] is False
    assert flags["BROKER_ENABLED"] is False


def test_scorecard_weights_sum_100_in_integration():
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_report_json_has_all_required_fields():
    import json
    scorecard = compute_scorecard(TEMPLATE_300K_ID, {k: 1.0 for k in SCORE_WEIGHTS})
    report = build_report(TEMPLATE_300K_ID, scorecard)
    parsed = json.loads(to_json(report))
    assert parsed["paper_only"] is True
    assert parsed["research_only"] is True
    assert parsed["no_real_orders"] is True
    assert parsed["not_investment_advice"] is True
