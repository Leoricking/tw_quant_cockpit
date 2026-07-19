"""
paper_trading/small_capital_strategy/paper_cockpit_health_v200.py
v2.0.0 Paper Cockpit Unified Entry & Strategy Decision Console — Health Check
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

HEALTH_VERSION = "2.0.0"
HEALTH_RELEASE = "Paper Cockpit Unified Entry & Strategy Decision Console"


def run_health_check():
    """Run all health checks for v2.0.0 paper cockpit. Returns result dict."""
    passed = 0
    failed = 0
    errors = []

    def chk(name, fn):
        nonlocal passed, failed
        try:
            fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(f"FAIL:{name}:{e}")

    # --- module import ---
    chk("import_paper_cockpit_v200", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200",
        fromlist=["VERSION"]))

    # --- version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION, SCHEMA_VERSION
    chk("version_is_200", lambda: None if VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.0 got {VERSION}")))
    chk("schema_version_is_200", lambda: None if SCHEMA_VERSION == "200" else (_ for _ in ()).throw(
        AssertionError(f"Expected 200 got {SCHEMA_VERSION}")))

    # --- 23 models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        PaperCockpitInput, PaperCockpitResult, PaperCockpitWatchlist, PaperCockpitCandidate,
        PaperCockpitSignalScore, PaperCockpitThemeScore, PaperCockpitFundamentalScore,
        PaperCockpitTechnicalScore, PaperCockpitInstitutionalScore, PaperCockpitMarginScore,
        PaperCockpitEntryCheck, PaperCockpitABCDecision, PaperCockpitPortfolioRiskCheck,
        PaperCockpitPositionSizingCheck, PaperCockpitNoEntryCondition, PaperCockpitDecisionTicket,
        PaperCockpitHumanReviewRequest, PaperCockpitDashboard, PaperCockpitReport,
        PaperCockpitAuditTrail, PaperCockpitValidationResult, PaperCockpitHealthSummary,
        PaperCockpitReleaseSummary, _ALL_MODEL_NAMES,
    )
    chk("model_PaperCockpitInput", lambda: PaperCockpitInput())
    chk("model_PaperCockpitResult", lambda: PaperCockpitResult())
    chk("model_PaperCockpitWatchlist", lambda: PaperCockpitWatchlist())
    chk("model_PaperCockpitCandidate", lambda: PaperCockpitCandidate())
    chk("model_PaperCockpitSignalScore", lambda: PaperCockpitSignalScore())
    chk("model_PaperCockpitThemeScore", lambda: PaperCockpitThemeScore())
    chk("model_PaperCockpitFundamentalScore", lambda: PaperCockpitFundamentalScore())
    chk("model_PaperCockpitTechnicalScore", lambda: PaperCockpitTechnicalScore())
    chk("model_PaperCockpitInstitutionalScore", lambda: PaperCockpitInstitutionalScore())
    chk("model_PaperCockpitMarginScore", lambda: PaperCockpitMarginScore())
    chk("model_PaperCockpitEntryCheck", lambda: PaperCockpitEntryCheck())
    chk("model_PaperCockpitABCDecision", lambda: PaperCockpitABCDecision())
    chk("model_PaperCockpitPortfolioRiskCheck", lambda: PaperCockpitPortfolioRiskCheck())
    chk("model_PaperCockpitPositionSizingCheck", lambda: PaperCockpitPositionSizingCheck())
    chk("model_PaperCockpitNoEntryCondition", lambda: PaperCockpitNoEntryCondition())
    chk("model_PaperCockpitDecisionTicket", lambda: PaperCockpitDecisionTicket())
    chk("model_PaperCockpitHumanReviewRequest", lambda: PaperCockpitHumanReviewRequest())
    chk("model_PaperCockpitDashboard", lambda: PaperCockpitDashboard())
    chk("model_PaperCockpitReport", lambda: PaperCockpitReport())
    chk("model_PaperCockpitAuditTrail", lambda: PaperCockpitAuditTrail())
    chk("model_PaperCockpitValidationResult", lambda: PaperCockpitValidationResult())
    chk("model_PaperCockpitHealthSummary", lambda: PaperCockpitHealthSummary())
    chk("model_PaperCockpitReleaseSummary", lambda: PaperCockpitReleaseSummary())
    chk("model_count_23", lambda: None if len(_ALL_MODEL_NAMES) == 23 else (_ for _ in ()).throw(
        AssertionError(f"Expected 23 models, got {len(_ALL_MODEL_NAMES)}")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS, HARD_BLOCK_CONDITIONS,
        NO_ENTRY_CONDITIONS, CLI_COMMANDS, GUI_TABS, ABC_DECISION_TYPES, COVERED_VERSIONS,
    )
    chk("safety_flags_count_30", lambda: None if len(SAFETY_FLAGS) == 30 else (_ for _ in ()).throw(
        AssertionError(f"Expected 30 safety flags")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_real_orders", lambda: None if SAFETY_FLAGS["no_real_orders"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_cockpit_executes_order_false", lambda: None if SAFETY_FLAGS["cockpit_executes_order"] is False else (
        _ for _ in ()).throw(AssertionError("cockpit_executes_order must be False")))
    chk("safety_cockpit_mutates_strategy_false", lambda: None if SAFETY_FLAGS["cockpit_mutates_strategy"] is False else (
        _ for _ in ()).throw(AssertionError("cockpit_mutates_strategy must be False")))
    chk("forbidden_actions_count_10", lambda: None if len(FORBIDDEN_ACTIONS) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 forbidden")))
    chk("allowed_actions_count_9", lambda: None if len(ALLOWED_ACTIONS) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 allowed")))
    chk("hard_block_count_22", lambda: None if len(HARD_BLOCK_CONDITIONS) == 22 else (_ for _ in ()).throw(
        AssertionError(f"Expected 22 hard block conditions")))
    chk("no_entry_count_8", lambda: None if len(NO_ENTRY_CONDITIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 no-entry conditions")))
    chk("cli_commands_count_17", lambda: None if len(CLI_COMMANDS) == 17 else (_ for _ in ()).throw(
        AssertionError(f"Expected 17 CLI commands")))
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs")))
    chk("abc_types_count_4", lambda: None if len(ABC_DECISION_TYPES) == 4 else (_ for _ in ()).throw(
        AssertionError(f"Expected 4 ABC types")))
    chk("covered_versions_count_29", lambda: None if len(COVERED_VERSIONS) == 29 else (_ for _ in ()).throw(
        AssertionError(f"Expected 29 covered versions")))

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        score_watchlist, score_candidate, classify_abc, check_portfolio_risk,
        check_position_sizing, evaluate_no_entry, generate_decision_ticket,
        generate_human_review_request, build_dashboard, build_report, build_audit_trail,
        validate_cockpit, run_cockpit, get_cockpit_summary, get_version_info, verify_version,
    )
    chk("fn_score_watchlist", lambda: score_watchlist(["2330"]))
    chk("fn_score_candidate", lambda: score_candidate("2330"))
    chk("fn_classify_abc_no_entry", lambda: classify_abc("2330", score_candidate("2330")))
    chk("fn_check_portfolio_risk", lambda: check_portfolio_risk())
    chk("fn_check_position_sizing", lambda: check_position_sizing())
    chk("fn_validate_cockpit", lambda: validate_cockpit(PaperCockpitInput()))
    chk("fn_run_cockpit", lambda: run_cockpit(PaperCockpitInput(watchlist=["2330"])))
    chk("fn_get_cockpit_summary", lambda: get_cockpit_summary())
    chk("fn_get_version_info", lambda: get_version_info())
    chk("fn_verify_version", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version failed")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v200 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_200", lambda: None if all(
        s["schema_version"] == "200" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_have_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))
    chk("scenarios_have_no_real_orders", lambda: None if all(
        s["no_real_orders"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing no_real_orders=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v200 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_200", lambda: None if all(
        f["schema_version"] == "200" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- GUI panel ---
    from gui.small_capital_strategy_panel import PANEL_VERSION, get_tab_names
    chk("panel_version_200", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.0 got {PANEL_VERSION}")))
    chk("gui_tab_paper_cockpit", lambda: None if "paper_cockpit" in get_tab_names() else (_ for _ in ()).throw(
        AssertionError("paper_cockpit tab missing")))
    chk("gui_tab_strategy_decision_console", lambda: None if "strategy_decision_console" in get_tab_names() else (
        _ for _ in ()).throw(AssertionError("strategy_decision_console tab missing")))
    chk("gui_tab_decision_ticket", lambda: None if "decision_ticket" in get_tab_names() else (_ for _ in ()).throw(
        AssertionError("decision_ticket tab missing")))

    # --- CLI ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-version", "paper-cockpit-run", "paper-cockpit-watchlist",
        "paper-cockpit-score", "paper-cockpit-abc-check", "paper-cockpit-risk-check",
        "paper-cockpit-sizing-check", "paper-cockpit-no-entry",
    ]:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v200] {passed}/{total} passed")
    return {
        "all_passed": all_passed,
        "passed": passed,
        "failed": failed,
        "total": total,
        "errors": errors,
        "version": HEALTH_VERSION,
        "release": HEALTH_RELEASE,
    }


if __name__ == "__main__":
    result = run_health_check()
    if not result["all_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
