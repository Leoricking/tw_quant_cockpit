"""
tests/test_market_regime_scorecard_v173.py
Tests for Market Regime Position Control scorecard_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, RegimeScorecardGrade,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeDetectionResult, CashRatioPlan, ExposureControlPlan,
    CandidateRegimePermission, ABCRegimePermission, MarketRegimeInput,
)
from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_candidate_permission, get_abc_regime_permission,
)
from paper_trading.small_capital_strategy.market_regime_scorecard_v173 import (
    build_regime_scorecard, get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
    GRADE_B_MIN, GRADE_C_MIN, GRADE_D_MIN,
    WEIGHT_REGIME_DETECTION, WEIGHT_CASH_RATIO, WEIGHT_EXPOSURE_CONTROL,
    WEIGHT_CANDIDATE_PERM, WEIGHT_ABC_COMPATIBILITY, WEIGHT_SAFETY,
)


def _build_full_scorecard(regime: MarketRegime):
    inp = {
        MarketRegime.BULL: MarketRegimeInput(
            index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500,
            index_ma240=16000, advance_decline_ratio=1.8, volatility_score=20.0,
            risk_event_flag=False, major_index_trend_score=1.0, institutional_market_bias=0.5,
        ),
        MarketRegime.BEAR: MarketRegimeInput(
            index_close=15000, index_ma20=16000, index_ma60=17000, index_ma120=18000,
            index_ma240=19000, advance_decline_ratio=0.4, volatility_score=60.0,
            risk_event_flag=False, major_index_trend_score=-1.0,
        ),
    }.get(regime, MarketRegimeInput())

    detection     = detect_market_regime(inp)
    cash_plan     = build_cash_ratio_plan(regime)
    exposure_plan = build_exposure_control_plan(regime)
    cand_perm     = get_candidate_permission(regime, "MAIN_THEME_SWING")
    abc_perm      = get_abc_regime_permission(regime)
    return build_regime_scorecard(regime, detection, cash_plan, exposure_plan, cand_perm, abc_perm)


class TestBuildRegimeScorecard:
    def test_bull_scorecard_high_grade(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.grade in (RegimeScorecardGrade.A, RegimeScorecardGrade.B)

    def test_bear_scorecard_not_a(self):
        scorecard = _build_full_scorecard(MarketRegime.BEAR)
        # Bear has blocked permissions; grade will not be A (no full allocation/execution)
        assert scorecard.grade != RegimeScorecardGrade.A

    def test_weights_sum_100(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.weights_sum == 100

    def test_safety_score_100(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.safety_score == 100.0

    def test_total_score_in_range(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert 0.0 <= scorecard.total_score <= 100.0

    def test_paper_only(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.paper_only is True

    def test_no_real_orders(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.no_real_orders is True

    def test_schema_version(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.schema_version == "173"

    def test_grade_not_a_plus(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.grade != "A+"
        assert not hasattr(RegimeScorecardGrade, "A_PLUS")

    def test_regime_stored(self):
        scorecard = _build_full_scorecard(MarketRegime.BULL)
        assert scorecard.regime == MarketRegime.BULL


class TestWeightTable:
    def test_weights_sum_100(self):
        assert WEIGHTS_SUM == 100

    def test_regime_detection_weight_25(self):
        assert WEIGHT_REGIME_DETECTION == 25

    def test_cash_ratio_weight_20(self):
        assert WEIGHT_CASH_RATIO == 20

    def test_exposure_control_weight_20(self):
        assert WEIGHT_EXPOSURE_CONTROL == 20

    def test_candidate_perm_weight_15(self):
        assert WEIGHT_CANDIDATE_PERM == 15

    def test_abc_weight_10(self):
        assert WEIGHT_ABC_COMPATIBILITY == 10

    def test_safety_weight_10(self):
        assert WEIGHT_SAFETY == 10

    def test_get_weight_table_returns_dict(self):
        table = get_weight_table()
        assert isinstance(table, dict)

    def test_weight_table_total_100(self):
        table = get_weight_table()
        assert table["total"] == 100


class TestGradeThresholds:
    def test_a_min_85(self):
        assert GRADE_A_MIN == 85.0

    def test_b_min_70(self):
        assert GRADE_B_MIN == 70.0

    def test_c_min_55(self):
        assert GRADE_C_MIN == 55.0

    def test_d_min_40(self):
        assert GRADE_D_MIN == 40.0
