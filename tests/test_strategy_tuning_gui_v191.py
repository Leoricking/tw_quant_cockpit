"""tests/test_strategy_tuning_gui_v191.py
Tests for strategy tuning GUI panel v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    get_tab_names, get_strategy_tuning_tab_names,
    render_strategy_rule_tuning_tab,
    render_guardrail_review_tab,
    render_rule_recommendations_tab,
)


def test_panel_version_191():
    assert PANEL_VERSION in ("1.9.1", "1.9.2", "1.9.3")

def test_panel_title_contains_191():
    assert "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE or "1.9.3" in PANEL_TITLE

def test_panel_title_contains_tuning():
    assert "Tuning" in PANEL_TITLE or "tuning" in PANEL_TITLE.lower() or "Sandbox" in PANEL_TITLE or "Shadow" in PANEL_TITLE or "Promotion" in PANEL_TITLE or "Rollback" in PANEL_TITLE

def test_strategy_tuning_tab_names_count():
    tabs = get_strategy_tuning_tab_names()
    assert len(tabs) == 3

def test_strategy_tuning_tab_names_has_rule_tuning():
    assert "strategy_rule_tuning" in get_strategy_tuning_tab_names()

def test_strategy_tuning_tab_names_has_guardrail_review():
    assert "guardrail_review" in get_strategy_tuning_tab_names()

def test_strategy_tuning_tab_names_has_rule_recommendations():
    assert "rule_recommendations" in get_strategy_tuning_tab_names()

def test_all_tabs_includes_tuning_tabs():
    all_tabs = get_tab_names()
    assert "strategy_rule_tuning" in all_tabs

def test_all_tabs_includes_guardrail_review():
    all_tabs = get_tab_names()
    assert "guardrail_review" in all_tabs

def test_all_tabs_includes_rule_recommendations():
    all_tabs = get_tab_names()
    assert "rule_recommendations" in all_tabs


# ── render_strategy_rule_tuning_tab ──────────────────────────────────────────

def test_render_rule_tuning_tab_returns_dict():
    assert isinstance(render_strategy_rule_tuning_tab(), dict)

def test_render_rule_tuning_tab_tab_name():
    assert render_strategy_rule_tuning_tab()["tab"] == "strategy_rule_tuning"

def test_render_rule_tuning_tab_paper_only():
    assert render_strategy_rule_tuning_tab()["paper_only"] is True

def test_render_rule_tuning_tab_tuning_only():
    assert render_strategy_rule_tuning_tab()["tuning_only"] is True

def test_render_rule_tuning_tab_guardrail_only():
    assert render_strategy_rule_tuning_tab()["guardrail_only"] is True

def test_render_rule_tuning_tab_no_real_orders():
    assert render_strategy_rule_tuning_tab()["no_real_orders"] is True

def test_render_rule_tuning_tab_no_broker():
    assert render_strategy_rule_tuning_tab()["no_broker"] is True

def test_render_rule_tuning_tab_not_investment_advice():
    assert render_strategy_rule_tuning_tab()["not_investment_advice"] is True

def test_render_rule_tuning_tab_no_production_mutation():
    assert render_strategy_rule_tuning_tab()["no_production_strategy_mutation"] is True

def test_render_rule_tuning_tab_production_blocked():
    assert render_strategy_rule_tuning_tab()["production_trading_blocked"] is True

def test_render_rule_tuning_tab_schema_191():
    assert render_strategy_rule_tuning_tab()["schema_version"] == "191"

def test_render_rule_tuning_tab_has_empty_state():
    assert "empty_state" in render_strategy_rule_tuning_tab()


# ── render_guardrail_review_tab ───────────────────────────────────────────────

def test_render_guardrail_review_tab_returns_dict():
    assert isinstance(render_guardrail_review_tab(), dict)

def test_render_guardrail_review_tab_tab_name():
    assert render_guardrail_review_tab()["tab"] == "guardrail_review"

def test_render_guardrail_review_tab_paper_only():
    assert render_guardrail_review_tab()["paper_only"] is True

def test_render_guardrail_review_tab_guardrail_only():
    assert render_guardrail_review_tab()["guardrail_only"] is True

def test_render_guardrail_review_tab_no_real_orders():
    assert render_guardrail_review_tab()["no_real_orders"] is True

def test_render_guardrail_review_tab_no_production_mutation():
    assert render_guardrail_review_tab()["no_production_strategy_mutation"] is True

def test_render_guardrail_review_tab_schema_191():
    assert render_guardrail_review_tab()["schema_version"] == "191"

def test_render_guardrail_review_tab_has_empty_state():
    assert "empty_state" in render_guardrail_review_tab()


# ── render_rule_recommendations_tab ──────────────────────────────────────────

def test_render_rule_recommendations_tab_returns_dict():
    assert isinstance(render_rule_recommendations_tab(), dict)

def test_render_rule_recommendations_tab_tab_name():
    assert render_rule_recommendations_tab()["tab"] == "rule_recommendations"

def test_render_rule_recommendations_tab_paper_only():
    assert render_rule_recommendations_tab()["paper_only"] is True

def test_render_rule_recommendations_tab_tuning_only():
    assert render_rule_recommendations_tab()["tuning_only"] is True

def test_render_rule_recommendations_tab_no_real_orders():
    assert render_rule_recommendations_tab()["no_real_orders"] is True

def test_render_rule_recommendations_tab_no_production_mutation():
    assert render_rule_recommendations_tab()["no_production_strategy_mutation"] is True

def test_render_rule_recommendations_tab_schema_191():
    assert render_rule_recommendations_tab()["schema_version"] == "191"

def test_render_rule_recommendations_tab_has_empty_state():
    assert "empty_state" in render_rule_recommendations_tab()
