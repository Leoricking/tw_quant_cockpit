"""
paper_trading/small_capital_strategy/paper_cockpit_health_v201.py
v2.0.1 Paper Cockpit Usability & Daily Workflow Hardening — Health Check
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

HEALTH_VERSION = "2.0.1"
HEALTH_RELEASE = "Paper Cockpit Usability & Daily Workflow Hardening"


def run_health_check():
    """Run all health checks for v2.0.1 paper cockpit. Returns result dict."""
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
    chk("import_paper_cockpit_v201", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201",
        fromlist=["VERSION"]))

    # --- version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_201", lambda: None if VERSION == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.1 got {VERSION}")))
    chk("schema_version_is_201", lambda: None if SCHEMA_VERSION == "201" else (_ for _ in ()).throw(
        AssertionError(f"Expected 201 got {SCHEMA_VERSION}")))
    chk("release_name_correct", lambda: None if "Daily Workflow" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Daily Workflow': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- no-entry reasons (13) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_ENTRY_REASONS
    chk("no_entry_reasons_count_13", lambda: None if len(NO_ENTRY_REASONS) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 NO_ENTRY_REASONS, got {len(NO_ENTRY_REASONS)}")))
    for reason in [
        "trend_broken", "below_20ma", "below_60ma", "volume_overheated",
        "volume_dry_up_failed", "institutional_selling", "margin_overheated",
        "market_risk_high", "risk_budget_exceeded", "position_size_too_large",
        "stop_loss_too_wide", "missing_required_signal", "human_review_required",
    ]:
        chk(f"no_entry_reason_{reason}", lambda r=reason: None if r in NO_ENTRY_REASONS else (
            _ for _ in ()).throw(AssertionError(f"Missing reason: {r}")))

    # --- daily final actions (7) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import DAILY_FINAL_ACTIONS
    chk("daily_final_actions_count_7", lambda: None if len(DAILY_FINAL_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 DAILY_FINAL_ACTIONS, got {len(DAILY_FINAL_ACTIONS)}")))
    for action in ["WATCH", "WAIT", "PAPER_BUY_PLAN", "PAPER_ADD_PLAN",
                   "PAPER_REDUCE_PLAN", "PAPER_EXIT_PLAN", "NO_ENTRY"]:
        chk(f"final_action_{action}", lambda a=action: None if a in DAILY_FINAL_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing action: {a}")))

    # --- models (12) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        DailyWorkflowInput, CandidateRankEntry, NoEntryReasonDetail,
        EnhancedDecisionTicket, RiskBudgetStatus, CLIDisplayRow,
        CLIDisplayOutput, DailyWorkflowCandidateResult, DailyWorkflowSummary,
        DailyWorkflowResult, V201HealthSummary, V201ReleaseSummary,
        _ALL_MODEL_NAMES_V201,
    )
    chk("model_DailyWorkflowInput", lambda: DailyWorkflowInput())
    chk("model_CandidateRankEntry", lambda: CandidateRankEntry())
    chk("model_NoEntryReasonDetail", lambda: NoEntryReasonDetail())
    chk("model_EnhancedDecisionTicket", lambda: EnhancedDecisionTicket())
    chk("model_RiskBudgetStatus", lambda: RiskBudgetStatus())
    chk("model_CLIDisplayRow", lambda: CLIDisplayRow())
    chk("model_CLIDisplayOutput", lambda: CLIDisplayOutput())
    chk("model_DailyWorkflowCandidateResult", lambda: DailyWorkflowCandidateResult())
    chk("model_DailyWorkflowSummary", lambda: DailyWorkflowSummary())
    chk("model_DailyWorkflowResult", lambda: DailyWorkflowResult())
    chk("model_V201HealthSummary", lambda: V201HealthSummary())
    chk("model_V201ReleaseSummary", lambda: V201ReleaseSummary())
    chk("model_count_12", lambda: None if len(_ALL_MODEL_NAMES_V201) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V201)}")))

    # --- enhanced ticket 21 fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import ENHANCED_TICKET_FIELDS
    chk("enhanced_ticket_fields_22", lambda: None if len(ENHANCED_TICKET_FIELDS) == 22 else (_ for _ in ()).throw(
        AssertionError(f"Expected 22 ENHANCED_TICKET_FIELDS, got {len(ENHANCED_TICKET_FIELDS)}")))

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        run_daily_workflow, classify_final_action, evaluate_no_entry_reasons,
        build_enhanced_ticket, build_cli_display, build_candidate_ranking,
        get_risk_budget_status, get_version_info, verify_version, get_cockpit_summary_v201,
    )
    chk("fn_run_daily_workflow", lambda: run_daily_workflow())
    chk("fn_classify_final_action", lambda: classify_final_action("2330", "NO_ENTRY", [], True, True))
    chk("fn_evaluate_no_entry_reasons", lambda: evaluate_no_entry_reasons())
    chk("fn_build_enhanced_ticket", lambda: build_enhanced_ticket("2330"))
    chk("fn_build_candidate_ranking", lambda: build_candidate_ranking([]))
    chk("fn_get_risk_budget_status", lambda: get_risk_budget_status())
    chk("fn_get_version_info", lambda: get_version_info())
    chk("fn_verify_version", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version() failed")))
    chk("fn_get_cockpit_summary_v201", lambda: get_cockpit_summary_v201())

    # --- daily workflow callable ---
    chk("daily_workflow_callable", lambda: None if run_daily_workflow() is not None else (
        _ for _ in ()).throw(AssertionError("run_daily_workflow() returned None")))
    chk("daily_workflow_paper_only", lambda: None if run_daily_workflow().paper_only is True else (
        _ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("daily_workflow_no_order", lambda: None if run_daily_workflow().cockpit_executes_order is False else (
        _ for _ in ()).throw(AssertionError("cockpit_executes_order must be False")))

    # --- paper-only guards ---
    chk("safety_flags_paper_only", lambda: None if __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["SAFETY_FLAGS"]
    ).SAFETY_FLAGS["paper_only"] is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("safety_flags_no_broker", lambda: None if __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["SAFETY_FLAGS"]
    ).SAFETY_FLAGS["no_broker"] is True else (_ for _ in ()).throw(AssertionError("no_broker must be True")))
    chk("safety_cockpit_executes_order_false", lambda: None if __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["SAFETY_FLAGS"]
    ).SAFETY_FLAGS["cockpit_executes_order"] is False else (_ for _ in ()).throw(AssertionError("cockpit_executes_order must be False")))
    chk("safety_no_automatic_rebalance", lambda: None if __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["SAFETY_FLAGS"]
    ).SAFETY_FLAGS["no_automatic_rebalance"] is True else (_ for _ in ()).throw(AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["SAFETY_FLAGS"]
    ).SAFETY_FLAGS["no_real_account_sync"] is True else (_ for _ in ()).throw(AssertionError("no_real_account_sync must be True")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    chk("panel_version_201", lambda: None if PANEL_VERSION_V201 == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V201 2.0.1, got {PANEL_VERSION_V201}")))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v201_tab_names
    tab_names = get_tab_names()
    for tab in ["daily_workflow_v201", "no_entry_reason_detail", "decision_ticket_v201"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v201_tab_names_3", lambda: None if len(get_v201_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v201 tab names")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import CLI_COMMANDS_V201
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V201) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V201")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v201 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_201", lambda: None if all(
        s["schema_version"] == "201" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v201 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_201", lambda: None if all(
        f["schema_version"] == "201" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- backward compatibility ---
    chk("import_v200_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200",
        fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200
    chk("v200_version_unchanged", lambda: None if V200 == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.0 VERSION changed to {V200}")))

    # --- covered versions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    chk("covered_versions_include_200", lambda: None if "2.0.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("COVERED_VERSIONS must include 2.0.0")))
    chk("covered_versions_include_170", lambda: None if "1.7.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("COVERED_VERSIONS must include 1.7.0")))

    # --- tests exist ---
    import os as _os
    chk("test_v201_exists", lambda: None if _os.path.exists(
        _os.path.normpath("D:/code/Claude/tw_quant_cockpit/tests/test_paper_cockpit_v201.py")
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v201] {passed}/{total} passed")
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
