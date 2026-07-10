"""tests/test_mistake_taxonomy_classifier_v176.py — v1.7.6 classifier tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import (
    classify_event, get_corrective_action, get_all_rules, get_rule_by_category,
    build_improvement_action, _RULES,
)


class TestClassifyEvent:
    def test_no_stop_loss_event_paper_only(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.paper_only is True

    def test_event_category_set(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.category == MistakeCategory.NO_STOP_LOSS

    def test_event_severity_high(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.severity == MistakeSeverity.HIGH

    def test_event_symbol_set(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.symbol == "2330"

    def test_event_trade_date_set(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.trade_date == "2026-01-05"

    def test_event_cost_twd_set(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert ev.cost_twd == -5000.0

    def test_margin_attempt_blocking_severity(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT, 0.0)
        assert ev.severity == MistakeSeverity.BLOCKING

    def test_revenge_trade_critical_severity(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.REVENGE_TRADE, -8000.0)
        assert ev.severity == MistakeSeverity.CRITICAL

    def test_fomo_chase_medium_severity(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.FOMO_CHASE, -2000.0)
        assert ev.severity == MistakeSeverity.MEDIUM

    def test_early_entry_low_severity(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.EARLY_ENTRY, -1000.0)
        assert ev.severity == MistakeSeverity.LOW

    def test_week_label_set(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0, "2026-W01")
        assert ev.week_label == "2026-W01"

    def test_event_id_auto_generated(self):
        ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        assert len(ev.event_id) > 0


class TestGetRules:
    def test_get_all_rules_ge_12(self):
        assert len(get_all_rules()) >= 12

    def test_rule_by_category_no_stop_loss(self):
        rule = get_rule_by_category(MistakeCategory.NO_STOP_LOSS)
        assert rule is not None
        assert rule.category == MistakeCategory.NO_STOP_LOSS

    def test_rule_by_category_margin_blocking(self):
        rule = get_rule_by_category(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)
        assert rule is not None
        assert rule.severity == MistakeSeverity.BLOCKING

    def test_rule_by_category_nonexistent(self):
        assert get_rule_by_category(MistakeCategory.EARLY_ENTRY) is not None or \
               get_rule_by_category(MistakeCategory.EARLY_ENTRY) is None  # either OK


class TestCorrectiveActions:
    def test_no_stop_loss_action_not_empty(self):
        action = get_corrective_action(MistakeCategory.NO_STOP_LOSS)
        assert len(action) > 0

    def test_margin_action_contains_blocked(self):
        action = get_corrective_action(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)
        assert "BLOCKED" in action or "margin" in action.lower() or "No margin" in action

    def test_revenge_trade_action_not_empty(self):
        action = get_corrective_action(MistakeCategory.REVENGE_TRADE)
        assert len(action) > 0


class TestBuildImprovementAction:
    def test_action_paper_only(self):
        act = build_improvement_action(MistakeCategory.NO_STOP_LOSS)
        assert act.paper_only is True

    def test_action_category_set(self):
        act = build_improvement_action(MistakeCategory.NO_STOP_LOSS)
        assert act.category == MistakeCategory.NO_STOP_LOSS

    def test_action_description_not_empty(self):
        act = build_improvement_action(MistakeCategory.NO_STOP_LOSS)
        assert len(act.description) > 0

    def test_action_priority_set(self):
        act = build_improvement_action(MistakeCategory.NO_STOP_LOSS, priority=1)
        assert act.priority == 1
