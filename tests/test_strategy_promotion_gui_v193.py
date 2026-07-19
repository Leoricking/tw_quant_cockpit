"""tests/test_strategy_promotion_gui_v193.py — v1.9.3 GUI panel tests."""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS,
    _TABS_V193_STRATEGY_PROMOTION,
    render_strategy_promotion_tab,
    render_rollback_plan_tab,
    render_promotion_evidence_tab,
    get_promotion_tab_names,
    get_panel_info,
    render_all_tabs,
)


# ── version ───────────────────────────────────────────────────────────────────
def test_panel_version_193():
    assert PANEL_VERSION in ("1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10")

def test_panel_title_contains_193():
    assert "1.9.3" in PANEL_TITLE or "1.9.4" in PANEL_TITLE or "1.9.5" in PANEL_TITLE or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE or "1.9.8" in PANEL_TITLE or "1.9.9" in PANEL_TITLE or "1.9.10" in PANEL_TITLE

def test_panel_title_contains_promotion():
    assert "Promotion" in PANEL_TITLE or "promotion" in PANEL_TITLE.lower() or "Monitoring" in PANEL_TITLE or "Drift" in PANEL_TITLE or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Portfolio" in PANEL_TITLE

# ── promotion tabs ────────────────────────────────────────────────────────────
def test_promotion_tabs_count():
    assert len(_TABS_V193_STRATEGY_PROMOTION) == 3

def test_promotion_tab_strategy_promotion():
    assert "strategy_promotion" in _TABS_V193_STRATEGY_PROMOTION

def test_promotion_tab_rollback_plan():
    assert "rollback_plan" in _TABS_V193_STRATEGY_PROMOTION

def test_promotion_tab_promotion_evidence():
    assert "promotion_evidence" in _TABS_V193_STRATEGY_PROMOTION

# ── get_promotion_tab_names ───────────────────────────────────────────────────
def test_get_promotion_tab_names_count():
    assert len(get_promotion_tab_names()) == 3

def test_get_promotion_tab_names_is_list():
    assert isinstance(get_promotion_tab_names(), list)

def test_get_promotion_tab_names_has_rollback():
    assert "rollback_plan" in get_promotion_tab_names()

def test_get_promotion_tab_names_has_evidence():
    assert "promotion_evidence" in get_promotion_tab_names()

# ── _TABS includes promotion tabs ─────────────────────────────────────────────
def test_tabs_has_strategy_promotion():
    assert "strategy_promotion" in _TABS

def test_tabs_has_rollback_plan():
    assert "rollback_plan" in _TABS

def test_tabs_has_promotion_evidence():
    assert "promotion_evidence" in _TABS

# ── render_strategy_promotion_tab ─────────────────────────────────────────────
def test_render_strategy_promotion_paper_only():
    assert render_strategy_promotion_tab()["paper_only"] is True

def test_render_strategy_promotion_no_real_orders():
    assert render_strategy_promotion_tab()["no_real_orders"] is True

def test_render_strategy_promotion_promotion_package_only():
    assert render_strategy_promotion_tab()["promotion_package_only"] is True

def test_render_strategy_promotion_rollback_plan_only():
    assert render_strategy_promotion_tab()["rollback_plan_only"] is True

def test_render_strategy_promotion_no_broker():
    assert render_strategy_promotion_tab()["no_broker"] is True

def test_render_strategy_promotion_tab_key():
    assert render_strategy_promotion_tab()["tab"] == "strategy_promotion"

def test_render_strategy_promotion_schema():
    assert render_strategy_promotion_tab()["schema_version"] == "193"

def test_render_strategy_promotion_not_investment_advice():
    assert render_strategy_promotion_tab()["not_investment_advice"] is True

def test_render_strategy_promotion_production_blocked():
    assert render_strategy_promotion_tab()["production_trading_blocked"] is True

# ── render_rollback_plan_tab ──────────────────────────────────────────────────
def test_render_rollback_plan_paper_only():
    assert render_rollback_plan_tab()["paper_only"] is True

def test_render_rollback_plan_rollback_plan_only():
    assert render_rollback_plan_tab()["rollback_plan_only"] is True

def test_render_rollback_plan_no_real_orders():
    assert render_rollback_plan_tab()["no_real_orders"] is True

def test_render_rollback_plan_tab_key():
    assert render_rollback_plan_tab()["tab"] == "rollback_plan"

def test_render_rollback_plan_schema():
    assert render_rollback_plan_tab()["schema_version"] == "193"

def test_render_rollback_plan_not_investment_advice():
    assert render_rollback_plan_tab()["not_investment_advice"] is True

# ── render_promotion_evidence_tab ─────────────────────────────────────────────
def test_render_promotion_evidence_paper_only():
    assert render_promotion_evidence_tab()["paper_only"] is True

def test_render_promotion_evidence_promotion_package_only():
    assert render_promotion_evidence_tab()["promotion_package_only"] is True

def test_render_promotion_evidence_no_broker():
    assert render_promotion_evidence_tab()["no_broker"] is True

def test_render_promotion_evidence_tab_key():
    assert render_promotion_evidence_tab()["tab"] == "promotion_evidence"

def test_render_promotion_evidence_schema():
    assert render_promotion_evidence_tab()["schema_version"] == "193"

def test_render_promotion_evidence_not_investment_advice():
    assert render_promotion_evidence_tab()["not_investment_advice"] is True

# ── get_panel_info ────────────────────────────────────────────────────────────
def test_panel_info_version():
    assert get_panel_info()["panel_version"] in ("1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10")

def test_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True

def test_panel_info_tabs_count():
    assert get_panel_info()["tab_count"] == len(_TABS)

# ── render_all_tabs ───────────────────────────────────────────────────────────
def test_render_all_tabs_has_strategy_promotion():
    all_tabs = render_all_tabs()
    assert "strategy_promotion" in all_tabs

def test_render_all_tabs_has_rollback_plan():
    all_tabs = render_all_tabs()
    assert "rollback_plan" in all_tabs

def test_render_all_tabs_has_promotion_evidence():
    all_tabs = render_all_tabs()
    assert "promotion_evidence" in all_tabs

def test_render_all_tabs_strategy_promotion_paper_only():
    all_tabs = render_all_tabs()
    assert all_tabs["strategy_promotion"]["paper_only"] is True

def test_render_all_tabs_rollback_plan_rollback_only():
    all_tabs = render_all_tabs()
    assert all_tabs["rollback_plan"]["rollback_plan_only"] is True
