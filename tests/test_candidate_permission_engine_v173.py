"""
tests/test_candidate_permission_engine_v173.py
Tests for Market Regime Position Control candidate_permission_engine_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimePermissionStatus, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_candidate_permission, get_abc_regime_permission, list_all_tiers,
)


class TestGetCandidatePermission:
    # BULL regime
    def test_bull_core_allowed(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert perm.permission == RegimePermissionStatus.ALLOWED

    def test_bull_core_max_5(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert perm.max_candidates == 5

    def test_bull_core_abc_all_allowed(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert "A" in perm.buy_points_allowed
        assert "B" in perm.buy_points_allowed
        assert "C" in perm.buy_points_allowed

    def test_bull_main_theme_allowed(self):
        perm = get_candidate_permission(MarketRegime.BULL, "MAIN_THEME_SWING")
        assert perm.permission == RegimePermissionStatus.ALLOWED

    def test_bull_second_wave_selective(self):
        perm = get_candidate_permission(MarketRegime.BULL, "SECOND_WAVE_SETUP")
        assert perm.permission == RegimePermissionStatus.SELECTIVE

    def test_bull_training_limited(self):
        perm = get_candidate_permission(MarketRegime.BULL, "TRAINING")
        assert perm.permission == RegimePermissionStatus.LIMITED

    # RANGE regime
    def test_range_core_selective(self):
        perm = get_candidate_permission(MarketRegime.RANGE, "CORE")
        assert perm.permission == RegimePermissionStatus.SELECTIVE

    def test_range_main_theme_selective(self):
        perm = get_candidate_permission(MarketRegime.RANGE, "MAIN_THEME_SWING")
        assert perm.permission == RegimePermissionStatus.SELECTIVE

    # BEAR regime
    def test_bear_core_limited(self):
        perm = get_candidate_permission(MarketRegime.BEAR, "CORE")
        assert perm.permission == RegimePermissionStatus.LIMITED

    def test_bear_main_theme_blocked(self):
        perm = get_candidate_permission(MarketRegime.BEAR, "MAIN_THEME_SWING")
        assert perm.permission == RegimePermissionStatus.BLOCKED

    def test_bear_main_theme_block_reason(self):
        perm = get_candidate_permission(MarketRegime.BEAR, "MAIN_THEME_SWING")
        assert RegimeBlockReason.REGIME_BEAR in perm.block_reasons

    def test_bear_training_blocked(self):
        perm = get_candidate_permission(MarketRegime.BEAR, "TRAINING")
        assert perm.permission == RegimePermissionStatus.BLOCKED

    # RISK_OFF regime
    def test_risk_off_core_limited(self):
        perm = get_candidate_permission(MarketRegime.RISK_OFF, "CORE")
        assert perm.permission == RegimePermissionStatus.LIMITED

    def test_risk_off_main_theme_blocked(self):
        perm = get_candidate_permission(MarketRegime.RISK_OFF, "MAIN_THEME_SWING")
        assert perm.permission == RegimePermissionStatus.BLOCKED

    def test_risk_off_block_reason(self):
        perm = get_candidate_permission(MarketRegime.RISK_OFF, "MAIN_THEME_SWING")
        assert RegimeBlockReason.REGIME_RISK_OFF in perm.block_reasons

    # UNKNOWN regime
    def test_unknown_core_degraded(self):
        perm = get_candidate_permission(MarketRegime.UNKNOWN, "CORE")
        assert perm.permission == RegimePermissionStatus.DEGRADED

    def test_unknown_main_theme_degraded(self):
        perm = get_candidate_permission(MarketRegime.UNKNOWN, "MAIN_THEME_SWING")
        assert perm.permission == RegimePermissionStatus.DEGRADED

    def test_unknown_second_wave_blocked(self):
        perm = get_candidate_permission(MarketRegime.UNKNOWN, "SECOND_WAVE_SETUP")
        assert perm.permission == RegimePermissionStatus.BLOCKED

    # Safety
    def test_paper_only(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert perm.paper_only is True

    def test_no_real_orders(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert perm.no_real_orders is True

    def test_schema_version(self):
        perm = get_candidate_permission(MarketRegime.BULL, "CORE")
        assert perm.schema_version == "173"


class TestGetABCRegimePermission:
    def test_bull_all_abc_allowed(self):
        perm = get_abc_regime_permission(MarketRegime.BULL)
        assert perm.a_allowed is True
        assert perm.b_allowed is True
        assert perm.c_allowed is True

    def test_bear_all_abc_blocked(self):
        perm = get_abc_regime_permission(MarketRegime.BEAR)
        assert perm.a_allowed is False
        assert perm.b_allowed is False
        assert perm.c_allowed is False

    def test_risk_off_all_abc_blocked(self):
        perm = get_abc_regime_permission(MarketRegime.RISK_OFF)
        assert perm.a_allowed is False
        assert perm.b_allowed is False
        assert perm.c_allowed is False

    def test_range_a_allowed(self):
        perm = get_abc_regime_permission(MarketRegime.RANGE)
        assert perm.a_allowed is True

    def test_unknown_a_allowed(self):
        perm = get_abc_regime_permission(MarketRegime.UNKNOWN)
        assert perm.a_allowed is True

    def test_paper_only(self):
        perm = get_abc_regime_permission(MarketRegime.BULL)
        assert perm.paper_only is True


class TestListAllTiers:
    def test_returns_four_tiers(self):
        tiers = list_all_tiers()
        assert len(tiers) == 4

    def test_core_in_tiers(self):
        assert "CORE" in list_all_tiers()

    def test_training_in_tiers(self):
        assert "TRAINING" in list_all_tiers()
