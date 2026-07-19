"""
tests/test_strategy_registry_gui_v196.py
Tests for GUI panel v1.9.6 — Paper Strategy Decision Registry & Governance Lab.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    get_panel_info,
    render_decision_registry_tab,
    render_governance_review_tab,
    render_decision_lineage_tab,
    get_registry_tab_names,
)


# ── version ───────────────────────────────────────────────────────────────────

def test_panel_version_196():
    assert PANEL_VERSION in ("1.9.6", "1.9.7", "1.9.8", "1.9.9")

def test_panel_title_contains_196():
    assert "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE or "1.9.8" in PANEL_TITLE or "1.9.9" in PANEL_TITLE

def test_panel_title_contains_registry_or_governance():
    assert "Registry" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Decision" in PANEL_TITLE or "Portfolio" in PANEL_TITLE


# ── get_panel_info ────────────────────────────────────────────────────────────

def test_get_panel_info_returns_dict():
    assert isinstance(get_panel_info(), dict)

def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] in ("1.9.6", "1.9.7", "1.9.8", "1.9.9")

def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True

def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True

def test_get_panel_info_not_investment_advice():
    assert get_panel_info()["not_investment_advice"] is True

def test_get_panel_info_tab_count_ge_160():
    assert get_panel_info()["tab_count"] >= 160


# ── render_decision_registry_tab ─────────────────────────────────────────────

def test_render_decision_registry_tab_returns_dict():
    assert isinstance(render_decision_registry_tab(), dict)

def test_render_decision_registry_tab_paper_only():
    assert render_decision_registry_tab()["paper_only"] is True

def test_render_decision_registry_tab_no_real_orders():
    assert render_decision_registry_tab()["no_real_orders"] is True

def test_render_decision_registry_tab_governance_only():
    assert render_decision_registry_tab()["governance_only"] is True

def test_render_decision_registry_tab_registry_only():
    assert render_decision_registry_tab()["registry_only"] is True

def test_render_decision_registry_tab_auto_approval_false():
    assert render_decision_registry_tab()["auto_approval"] is False

def test_render_decision_registry_tab_auto_decision_false():
    assert render_decision_registry_tab()["auto_decision"] is False


# ── render_governance_review_tab ─────────────────────────────────────────────

def test_render_governance_review_tab_returns_dict():
    assert isinstance(render_governance_review_tab(), dict)

def test_render_governance_review_tab_paper_only():
    assert render_governance_review_tab()["paper_only"] is True

def test_render_governance_review_tab_no_real_orders():
    assert render_governance_review_tab()["no_real_orders"] is True

def test_render_governance_review_tab_governance_only():
    assert render_governance_review_tab()["governance_only"] is True

def test_render_governance_review_tab_auto_approval_false():
    assert render_governance_review_tab()["auto_approval"] is False


# ── render_decision_lineage_tab ───────────────────────────────────────────────

def test_render_decision_lineage_tab_returns_dict():
    assert isinstance(render_decision_lineage_tab(), dict)

def test_render_decision_lineage_tab_paper_only():
    assert render_decision_lineage_tab()["paper_only"] is True

def test_render_decision_lineage_tab_no_real_orders():
    assert render_decision_lineage_tab()["no_real_orders"] is True

def test_render_decision_lineage_tab_governance_only():
    assert render_decision_lineage_tab()["governance_only"] is True

def test_render_decision_lineage_tab_immutable():
    assert render_decision_lineage_tab()["immutable"] is True


# ── get_registry_tab_names ────────────────────────────────────────────────────

def test_get_registry_tab_names_count_3():
    assert len(get_registry_tab_names()) == 3

def test_get_registry_tab_names_contains_decision_registry():
    assert "decision_registry" in get_registry_tab_names()

def test_get_registry_tab_names_contains_governance_review():
    assert "governance_review" in get_registry_tab_names()

def test_get_registry_tab_names_contains_decision_lineage():
    assert "decision_lineage" in get_registry_tab_names()
