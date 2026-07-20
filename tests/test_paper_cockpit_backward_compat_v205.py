"""
tests/test_paper_cockpit_backward_compat_v205.py
v2.0.5 Backward Compatibility Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# -------------------------------------------------------------------------
# v2.0.4 backward compat
# -------------------------------------------------------------------------
def test_import_v204_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v204

def test_v204_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION
    assert VERSION == "2.0.4"

def test_v204_run_portfolio_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.paper_only is True

def test_v204_build_weekly_improvement_pack_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.should_auto_apply is False

def test_v204_should_auto_apply_still_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    rec = ImprovementRecommendation(should_auto_apply=True)
    assert rec.should_auto_apply is False

def test_v204_gui_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    for tab in ["weekly_review_v204", "improvement_pack_v204", "review_metrics_v204"]:
        assert tab in tab_names

def test_v204_cli_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v204-review-weekly",
        "paper-cockpit-v204-health",
        "paper-cockpit-v204-gate",
    ]:
        assert cmd in cmd_names

def test_v204_health_still_runs():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v204 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True

# -------------------------------------------------------------------------
# v2.0.3 backward compat
# -------------------------------------------------------------------------
def test_import_v203_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v203

def test_v203_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION
    assert VERSION == "2.0.3"

def test_v203_simulate_one_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, SimulationInput
    result = simulate_one(SimulationInput())
    assert result.paper_only is True

# -------------------------------------------------------------------------
# v2.0.2 backward compat
# -------------------------------------------------------------------------
def test_import_v202_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v202

def test_v202_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION
    assert VERSION == "2.0.2"

# -------------------------------------------------------------------------
# v2.0.1 backward compat
# -------------------------------------------------------------------------
def test_import_v201_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v201

def test_v201_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION
    assert VERSION == "2.0.1"

def test_v201_health_relative_path():
    import os
    health_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "..",
            "paper_trading", "small_capital_strategy",
            "paper_cockpit_health_v201.py"
        )
    )
    assert os.path.exists(health_path)

# -------------------------------------------------------------------------
# v2.0.0 backward compat
# -------------------------------------------------------------------------
def test_import_v200_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v200

def test_v200_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"

# -------------------------------------------------------------------------
# v201 health relative-path compatibility preserved
# -------------------------------------------------------------------------
def test_v201_health_test_file_exists_via_relative_path():
    import os
    test_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "..",
            "paper_trading", "small_capital_strategy",
            "paper_cockpit_health_v201.py"
        )
    )
    assert os.path.exists(test_path), f"v201 health not found at {test_path}"

def test_v201_health_no_d_drive_path():
    from paper_trading.small_capital_strategy import paper_cockpit_health_v201
    import inspect
    src = inspect.getsource(paper_cockpit_health_v201)
    # The hardcoded D: path was fixed in v2.0.4 — it should not appear anymore
    assert "D:/code/Claude/tw_quant_cockpit/tests/test_paper_cockpit_v201.py" not in src
