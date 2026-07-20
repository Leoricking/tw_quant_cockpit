"""
tests/test_paper_cockpit_backward_compat_v201.py
v2.0.1 Paper Cockpit — Backward Compatibility Tests (25+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))


# --- v2.0.0 still importable ---

def test_v200_module_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"

def test_v200_schema_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "200"

def test_v200_release_name_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import RELEASE_NAME
    assert "Unified Entry" in RELEASE_NAME

def test_v200_models_still_instantiate():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        PaperCockpitInput, PaperCockpitResult, PaperCockpitWatchlist,
        PaperCockpitCandidate, PaperCockpitSignalScore,
    )
    assert PaperCockpitInput().schema_version == "200"
    assert PaperCockpitResult().schema_version == "200"
    assert PaperCockpitWatchlist().schema_version == "200"
    assert PaperCockpitCandidate().schema_version == "200"
    assert PaperCockpitSignalScore().schema_version == "200"

def test_v200_more_models_instantiate():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        PaperCockpitDecisionTicket, PaperCockpitDashboard, PaperCockpitReport,
        PaperCockpitAuditTrail, PaperCockpitValidationResult,
    )
    assert PaperCockpitDecisionTicket().schema_version == "200"
    assert PaperCockpitDashboard().schema_version == "200"
    assert PaperCockpitReport().schema_version == "200"
    assert PaperCockpitAuditTrail().schema_version == "200"
    assert PaperCockpitValidationResult().schema_version == "200"

def test_v200_functions_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        score_watchlist, score_candidate, check_portfolio_risk,
        check_position_sizing, verify_version, run_cockpit, get_cockpit_summary,
    )
    assert score_watchlist(["2330"]) is not None
    assert score_candidate("2330") is not None
    assert check_portfolio_risk() is not None
    assert check_position_sizing() is not None
    assert verify_version() is True
    assert run_cockpit() is not None
    assert get_cockpit_summary() is not None

def test_v200_safety_flags_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SAFETY_FLAGS
    assert SAFETY_FLAGS["paper_only"] is True
    assert SAFETY_FLAGS["no_real_orders"] is True
    assert SAFETY_FLAGS["cockpit_executes_order"] is False

def test_v200_no_entry_conditions_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import NO_ENTRY_CONDITIONS
    assert len(NO_ENTRY_CONDITIONS) == 8

def test_v200_abc_decision_types_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import ABC_DECISION_TYPES
    assert len(ABC_DECISION_TYPES) == 4
    assert "NO_ENTRY" in ABC_DECISION_TYPES

def test_v200_cli_commands_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import CLI_COMMANDS
    assert len(CLI_COMMANDS) == 17

def test_v200_gui_tabs_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import GUI_TABS
    assert len(GUI_TABS) == 3

def test_v200_model_count_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import _ALL_MODEL_NAMES
    assert len(_ALL_MODEL_NAMES) == 23

def test_v200_scenarios_still_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v200 import SCENARIOS
    assert len(SCENARIOS) == 80
    assert all(s["schema_version"] == "200" for s in SCENARIOS)

def test_v200_fixtures_still_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v200 import FIXTURES
    assert len(FIXTURES) == 80
    assert all(f["schema_version"] == "200" for f in FIXTURES)


# --- v2.0.1 COVERED_VERSIONS includes past versions ---

def test_v201_covers_v200():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert "2.0.0" in COVERED_VERSIONS

def test_v201_covers_v170():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert "1.7.0" in COVERED_VERSIONS

def test_v201_covers_v180():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert "1.8.0" in COVERED_VERSIONS

def test_v201_covers_v190():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert "1.9.0" in COVERED_VERSIONS

def test_v201_covers_v1910():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert "1.9.10" in COVERED_VERSIONS

def test_v201_covered_versions_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    assert len(COVERED_VERSIONS) == 30


# --- Both v200 and v201 can be imported simultaneously ---

def test_both_versions_importable_simultaneously():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION as V201
    assert V200 == "2.0.0"
    assert V201 == "2.0.1"

def test_both_versions_schema_different():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SCHEMA_VERSION as S200
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import SCHEMA_VERSION as S201
    assert S200 == "200"
    assert S201 == "201"

def test_v200_run_cockpit_still_works_after_v201_import():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import run_cockpit
    result_v200 = run_cockpit()
    result_v201 = run_daily_workflow()
    assert result_v200.paper_only is True
    assert result_v201.paper_only is True

def test_v200_health_still_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v200 import (
        HEALTH_VERSION, HEALTH_RELEASE,
    )
    assert HEALTH_VERSION == "2.0.0"

def test_v200_release_gate_still_importable():
    from release.paper_cockpit_release_gate_v200 import GATE_VERSION, GATE_RELEASE
    assert GATE_VERSION == "2.0.0"
