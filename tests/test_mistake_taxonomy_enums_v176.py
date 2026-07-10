"""tests/test_mistake_taxonomy_enums_v176.py — v1.7.6 enum tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
    CATEGORY_SEVERITY, SEVERITY_WEIGHT,
    get_all_enum_names, get_category_severity, get_severity_weight,
)


class TestMistakeCategoryEnum:
    def test_enum_count_18(self):
        assert len(MistakeCategory) == 18

    def test_fomo_chase_exists(self):
        assert MistakeCategory.FOMO_CHASE.value == "FOMO_CHASE"

    def test_no_stop_loss_exists(self):
        assert MistakeCategory.NO_STOP_LOSS.value == "NO_STOP_LOSS"

    def test_moved_stop_loss_exists(self):
        assert MistakeCategory.MOVED_STOP_LOSS.value == "MOVED_STOP_LOSS"

    def test_oversized_position_exists(self):
        assert MistakeCategory.OVERSIZED_POSITION.value == "OVERSIZED_POSITION"

    def test_margin_attempt_exists(self):
        assert MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT.value == "MARGIN_OR_LEVERAGE_ATTEMPT"

    def test_broker_attempt_exists(self):
        assert MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT.value == "BROKER_OR_REAL_ORDER_ATTEMPT"

    def test_revenge_trade_exists(self):
        assert MistakeCategory.REVENGE_TRADE.value == "REVENGE_TRADE"

    def test_ignore_market_regime_exists(self):
        assert MistakeCategory.IGNORE_MARKET_REGIME.value == "IGNORE_MARKET_REGIME"

    def test_unknown_exists(self):
        assert MistakeCategory.UNKNOWN.value == "UNKNOWN"


class TestMistakeSeverityEnum:
    def test_enum_count_6(self):
        assert len(MistakeSeverity) == 6

    def test_info_exists(self):
        assert MistakeSeverity.INFO.value == "INFO"

    def test_low_exists(self):
        assert MistakeSeverity.LOW.value == "LOW"

    def test_medium_exists(self):
        assert MistakeSeverity.MEDIUM.value == "MEDIUM"

    def test_high_exists(self):
        assert MistakeSeverity.HIGH.value == "HIGH"

    def test_critical_exists(self):
        assert MistakeSeverity.CRITICAL.value == "CRITICAL"

    def test_blocking_exists(self):
        assert MistakeSeverity.BLOCKING.value == "BLOCKING"


class TestBehaviorRiskLevelEnum:
    def test_enum_count_4(self):
        assert len(BehaviorRiskLevel) == 4

    def test_pass_exists(self):
        assert BehaviorRiskLevel.PASS.value == "PASS"

    def test_watch_exists(self):
        assert BehaviorRiskLevel.WATCH.value == "WATCH"

    def test_warning_exists(self):
        assert BehaviorRiskLevel.WARNING.value == "WARNING"

    def test_blocked_exists(self):
        assert BehaviorRiskLevel.BLOCKED.value == "BLOCKED"


class TestEnumHelpers:
    def test_get_all_enum_names_count_3(self):
        assert len(get_all_enum_names()) == 3

    def test_get_all_enum_names_contains_category(self):
        assert "MistakeCategory" in get_all_enum_names()

    def test_category_severity_no_stop_loss_high(self):
        assert get_category_severity(MistakeCategory.NO_STOP_LOSS) == MistakeSeverity.HIGH

    def test_category_severity_margin_blocking(self):
        assert get_category_severity(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT) == MistakeSeverity.BLOCKING

    def test_category_severity_revenge_critical(self):
        assert get_category_severity(MistakeCategory.REVENGE_TRADE) == MistakeSeverity.CRITICAL

    def test_severity_weight_blocking_100(self):
        assert get_severity_weight(MistakeSeverity.BLOCKING) == 100

    def test_severity_weight_info_gt_zero(self):
        assert get_severity_weight(MistakeSeverity.INFO) > 0

    def test_severity_weights_ordered(self):
        weights = [
            get_severity_weight(MistakeSeverity.INFO),
            get_severity_weight(MistakeSeverity.LOW),
            get_severity_weight(MistakeSeverity.MEDIUM),
            get_severity_weight(MistakeSeverity.HIGH),
            get_severity_weight(MistakeSeverity.CRITICAL),
            get_severity_weight(MistakeSeverity.BLOCKING),
        ]
        assert weights == sorted(weights)
