"""
tests/test_risk_dashboard_concentration_v174.py
Tests for concentration risk monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, ConcentrationLevel, RiskBlockReason
from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import (
    evaluate_concentration_risk, get_concentration_thresholds,
    MAX_SINGLE_POSITION_PCT, MAX_SECTOR_EXPOSURE_PCT,
)


def _inp(single=20.0, sector=40.0):
    return SmallAccountRiskInput(max_single_position_pct=single, sector_exposure_pct=sector)


class TestThresholds:
    def test_max_single_35(self):
        assert MAX_SINGLE_POSITION_PCT == 35.0

    def test_max_sector_60(self):
        assert MAX_SECTOR_EXPOSURE_PCT == 60.0

    def test_thresholds_dict(self):
        t = get_concentration_thresholds()
        assert t["max_single_position_pct"] == 35.0
        assert t["max_sector_exposure_pct"] == 60.0

    def test_thresholds_paper_only(self):
        assert get_concentration_thresholds()["paper_only"] is True


class TestPassCases:
    def test_single_20_pass(self):
        assert evaluate_concentration_risk(_inp(20.0, 40.0)).status == RiskStatus.PASS

    def test_single_35_pass(self):
        assert evaluate_concentration_risk(_inp(35.0, 40.0)).status == RiskStatus.PASS

    def test_sector_40_pass(self):
        assert evaluate_concentration_risk(_inp(20.0, 40.0)).status == RiskStatus.PASS

    def test_pass_level(self):
        assert evaluate_concentration_risk(_inp(20.0, 40.0)).level == ConcentrationLevel.PASS


class TestWarningCases:
    def test_sector_56_warning(self):
        r = evaluate_concentration_risk(_inp(20.0, 56.0))
        assert r.status == RiskStatus.WARNING

    def test_warning_level(self):
        assert evaluate_concentration_risk(_inp(20.0, 56.0)).level == ConcentrationLevel.WARNING


class TestBlockedCases:
    def test_single_36_blocked(self):
        r = evaluate_concentration_risk(_inp(36.0, 40.0))
        assert r.status == RiskStatus.BLOCKED
        assert RiskBlockReason.POSITION_TOO_LARGE in r.block_reasons

    def test_sector_61_blocked(self):
        r = evaluate_concentration_risk(_inp(20.0, 61.0))
        assert r.status == RiskStatus.BLOCKED
        assert RiskBlockReason.SECTOR_CONCENTRATION_TOO_HIGH in r.block_reasons

    def test_both_exceeded_blocked(self):
        r = evaluate_concentration_risk(_inp(40.0, 65.0))
        assert r.status == RiskStatus.BLOCKED

    def test_blocked_level(self):
        assert evaluate_concentration_risk(_inp(40.0, 40.0)).level == ConcentrationLevel.BLOCKED


class TestResultFields:
    def test_paper_only(self):
        assert evaluate_concentration_risk(_inp()).paper_only is True

    def test_single_pct_stored(self):
        r = evaluate_concentration_risk(_inp(25.0, 40.0))
        assert r.max_single_position_pct == 25.0

    def test_sector_pct_stored(self):
        r = evaluate_concentration_risk(_inp(20.0, 45.0))
        assert r.sector_exposure_pct == 45.0

    def test_detail_not_empty(self):
        assert len(evaluate_concentration_risk(_inp()).detail) > 0
