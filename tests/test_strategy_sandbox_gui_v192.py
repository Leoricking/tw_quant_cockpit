"""tests/test_strategy_sandbox_gui_v192.py
Tests for strategy sandbox GUI panel v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    render_strategy_sandbox_tab,
    render_shadow_validation_tab,
    render_rule_comparison_tab,
    get_sandbox_tab_names,
    get_panel_info,
)


# ── PANEL_VERSION ─────────────────────────────────────────────────────────────

def test_panel_version_192():
    assert PANEL_VERSION in ("1.9.2", "1.9.3")


# ── render_strategy_sandbox_tab ───────────────────────────────────────────────

def test_render_strategy_sandbox_tab_returns_dict():
    assert isinstance(render_strategy_sandbox_tab(), dict)

def test_render_strategy_sandbox_tab_tab_name():
    assert render_strategy_sandbox_tab()["tab"] == "strategy_sandbox"

def test_render_strategy_sandbox_tab_paper_only():
    assert render_strategy_sandbox_tab()["paper_only"] is True

def test_render_strategy_sandbox_tab_sandbox_only():
    assert render_strategy_sandbox_tab()["sandbox_only"] is True

def test_render_strategy_sandbox_tab_no_real_orders():
    assert render_strategy_sandbox_tab()["no_real_orders"] is True

def test_render_strategy_sandbox_tab_no_broker():
    assert render_strategy_sandbox_tab()["no_broker"] is True

def test_render_strategy_sandbox_tab_no_production_strategy_mutation():
    assert render_strategy_sandbox_tab()["no_production_strategy_mutation"] is True

def test_render_strategy_sandbox_tab_not_investment_advice():
    assert render_strategy_sandbox_tab()["not_investment_advice"] is True

def test_render_strategy_sandbox_tab_production_trading_blocked():
    assert render_strategy_sandbox_tab()["production_trading_blocked"] is True

def test_render_strategy_sandbox_tab_schema_192():
    assert render_strategy_sandbox_tab()["schema_version"] == "192"

def test_render_strategy_sandbox_tab_has_empty_state():
    assert "empty_state" in render_strategy_sandbox_tab()


# ── render_shadow_validation_tab ──────────────────────────────────────────────

def test_render_shadow_validation_tab_returns_dict():
    assert isinstance(render_shadow_validation_tab(), dict)

def test_render_shadow_validation_tab_tab_name():
    assert render_shadow_validation_tab()["tab"] == "shadow_validation"

def test_render_shadow_validation_tab_paper_only():
    assert render_shadow_validation_tab()["paper_only"] is True

def test_render_shadow_validation_tab_sandbox_only():
    assert render_shadow_validation_tab()["sandbox_only"] is True

def test_render_shadow_validation_tab_shadow_only():
    assert render_shadow_validation_tab()["shadow_only"] is True

def test_render_shadow_validation_tab_no_real_orders():
    assert render_shadow_validation_tab()["no_real_orders"] is True

def test_render_shadow_validation_tab_no_production_strategy_mutation():
    assert render_shadow_validation_tab()["no_production_strategy_mutation"] is True

def test_render_shadow_validation_tab_not_investment_advice():
    assert render_shadow_validation_tab()["not_investment_advice"] is True

def test_render_shadow_validation_tab_schema_192():
    assert render_shadow_validation_tab()["schema_version"] == "192"

def test_render_shadow_validation_tab_has_empty_state():
    assert "empty_state" in render_shadow_validation_tab()


# ── render_rule_comparison_tab ────────────────────────────────────────────────

def test_render_rule_comparison_tab_returns_dict():
    assert isinstance(render_rule_comparison_tab(), dict)

def test_render_rule_comparison_tab_tab_name():
    assert render_rule_comparison_tab()["tab"] == "rule_comparison"

def test_render_rule_comparison_tab_paper_only():
    assert render_rule_comparison_tab()["paper_only"] is True

def test_render_rule_comparison_tab_sandbox_only():
    assert render_rule_comparison_tab()["sandbox_only"] is True

def test_render_rule_comparison_tab_no_real_orders():
    assert render_rule_comparison_tab()["no_real_orders"] is True

def test_render_rule_comparison_tab_no_production_strategy_mutation():
    assert render_rule_comparison_tab()["no_production_strategy_mutation"] is True

def test_render_rule_comparison_tab_not_investment_advice():
    assert render_rule_comparison_tab()["not_investment_advice"] is True

def test_render_rule_comparison_tab_schema_192():
    assert render_rule_comparison_tab()["schema_version"] == "192"

def test_render_rule_comparison_tab_has_empty_state():
    assert "empty_state" in render_rule_comparison_tab()


# ── get_sandbox_tab_names ─────────────────────────────────────────────────────

def test_get_sandbox_tab_names_returns_list():
    assert isinstance(get_sandbox_tab_names(), list)

def test_get_sandbox_tab_names_has_strategy_sandbox():
    assert "strategy_sandbox" in get_sandbox_tab_names()

def test_get_sandbox_tab_names_has_shadow_validation():
    assert "shadow_validation" in get_sandbox_tab_names()

def test_get_sandbox_tab_names_has_rule_comparison():
    assert "rule_comparison" in get_sandbox_tab_names()

def test_get_sandbox_tab_names_count_3():
    assert len(get_sandbox_tab_names()) == 3


# ── get_panel_info ────────────────────────────────────────────────────────────

def test_get_panel_info_returns_dict():
    assert isinstance(get_panel_info(), dict)

def test_get_panel_info_panel_version_192():
    assert get_panel_info()["panel_version"] in ("1.9.2", "1.9.3")

def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True

def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True

def test_get_panel_info_not_investment_advice():
    assert get_panel_info()["not_investment_advice"] is True

def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True
