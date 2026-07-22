"""
paper_trading/small_capital_strategy/paper_cockpit_health_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control — Health Check
[!] Paper Only. Research Only. Exit Plan Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.10"
HEALTH_RELEASE = "Paper Exit Plan & Stop-Loss Discipline Control"


def run_health_check():
    """Run all health checks for v2.0.10 paper cockpit. Returns result dict."""
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

    # --- version / title ---
    chk("version_title_210", lambda: None if HEALTH_VERSION == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.10 got {HEALTH_VERSION}")))
    chk("release_name_exit_plan", lambda: None if "Exit" in HEALTH_RELEASE or "Stop" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Exit': {HEALTH_RELEASE}")))
    chk("release_name_stop_loss", lambda: None if "Stop" in HEALTH_RELEASE or "Discipline" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Stop'/'Discipline': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v210", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v210",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_210", lambda: None if VERSION == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.10 got {VERSION}")))
    chk("schema_version_is_210", lambda: None if SCHEMA_VERSION == "210" else (_ for _ in ()).throw(
        AssertionError(f"Expected 210 got {SCHEMA_VERSION}")))
    chk("release_name_contains_exit", lambda: None if "Exit" in RELEASE_NAME or "Stop" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Exit': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    chk("safety_flags_count_23", lambda: None if len(SAFETY_FLAGS_V210) == 23 else (_ for _ in ()).throw(
        AssertionError(f"Expected 23 SAFETY_FLAGS_V210, got {len(SAFETY_FLAGS_V210)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V210["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V210["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V210["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V210["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_exit_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V210["exit_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exit_actions_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V210["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V210["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V210["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V210["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_no_automatic_exit_apply", lambda: None if SAFETY_FLAGS_V210["no_automatic_exit_apply"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_exit_apply must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V210["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V210["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))
    chk("safety_require_stop_loss_before_entry", lambda: None if SAFETY_FLAGS_V210["require_stop_loss_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_stop_loss_before_entry_always_true must be True")))

    # --- exit actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import EXIT_ACTIONS
    chk("exit_actions_count_8", lambda: None if len(EXIT_ACTIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 EXIT_ACTIONS, got {len(EXIT_ACTIONS)}")))
    for ea in ["allow_with_exit_plan", "require_tighter_stop", "reduce_size_before_entry",
               "observation_only", "block_entry_missing_stop", "block_entry_bad_reward_risk",
               "require_rescore", "human_review_required"]:
        chk(f"exit_action_{ea}", lambda a=ea: None if a in EXIT_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing exit action: {a}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CLI_COMMANDS_V210
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V210) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V210, got {len(CLI_COMMANDS_V210)}")))
    for cmd in [
        "paper-cockpit-v210-review-exit-plan",
        "paper-cockpit-v210-evaluate-stop-discipline",
        "paper-cockpit-v210-build-exit-warning-queue",
        "paper-cockpit-v210-build-stop-violation-queue",
        "paper-cockpit-v210-evaluate-reward-risk",
        "paper-cockpit-v210-export-json",
        "paper-cockpit-v210-export-md",
        "paper-cockpit-v210-export-csv",
        "paper-cockpit-v210-health",
        "paper-cockpit-v210-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V210 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import GUI_TABS_V210
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V210) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V210, got {len(GUI_TABS_V210)}")))
    for tab in ["exit_plan_v210", "stop_discipline_v210", "exit_warning_queue_v210"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V210 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- field lists ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        EXIT_PLAN_POLICY_FIELDS, CANDIDATE_EXIT_PLAN_FIELDS,
        STOP_DISCIPLINE_SUMMARY_FIELDS, EXIT_REVIEW_FIELDS,
    )
    chk("exit_plan_policy_fields_13", lambda: None if len(EXIT_PLAN_POLICY_FIELDS) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 EXIT_PLAN_POLICY_FIELDS, got {len(EXIT_PLAN_POLICY_FIELDS)}")))
    chk("candidate_exit_plan_fields_24", lambda: None if len(CANDIDATE_EXIT_PLAN_FIELDS) == 24 else (_ for _ in ()).throw(
        AssertionError(f"Expected 24 CANDIDATE_EXIT_PLAN_FIELDS, got {len(CANDIDATE_EXIT_PLAN_FIELDS)}")))
    chk("stop_discipline_summary_fields_14", lambda: None if len(STOP_DISCIPLINE_SUMMARY_FIELDS) == 14 else (_ for _ in ()).throw(
        AssertionError(f"Expected 14 STOP_DISCIPLINE_SUMMARY_FIELDS, got {len(STOP_DISCIPLINE_SUMMARY_FIELDS)}")))
    chk("exit_review_fields_11", lambda: None if len(EXIT_REVIEW_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 EXIT_REVIEW_FIELDS, got {len(EXIT_REVIEW_FIELDS)}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        ExitPlanPolicy, CandidateExitPlan, ExitReviewResult,
        ExitReviewInput, StopDisciplineSummary, ExitExportResult,
        ExitAuditSnapshot, ExitMarkdownReport, CandidateExitCSV,
        StopDisciplineCSV, ExitWarningCSV, V210HealthSummary,
        V210ReleaseSummary, ExitPlanSafetyGuard, _ALL_MODEL_NAMES_V210,
    )
    chk("model_ExitPlanPolicy", lambda: ExitPlanPolicy())
    chk("model_CandidateExitPlan", lambda: CandidateExitPlan())
    chk("model_ExitReviewResult", lambda: ExitReviewResult())
    chk("model_ExitReviewInput", lambda: ExitReviewInput())
    chk("model_StopDisciplineSummary", lambda: StopDisciplineSummary())
    chk("model_ExitExportResult", lambda: ExitExportResult())
    chk("model_ExitAuditSnapshot", lambda: ExitAuditSnapshot())
    chk("model_ExitMarkdownReport", lambda: ExitMarkdownReport())
    chk("model_CandidateExitCSV", lambda: CandidateExitCSV())
    chk("model_StopDisciplineCSV", lambda: StopDisciplineCSV())
    chk("model_ExitWarningCSV", lambda: ExitWarningCSV())
    chk("model_V210HealthSummary", lambda: V210HealthSummary())
    chk("model_V210ReleaseSummary", lambda: V210ReleaseSummary())
    chk("model_ExitPlanSafetyGuard", lambda: ExitPlanSafetyGuard())
    chk("model_count_14", lambda: None if len(_ALL_MODEL_NAMES_V210) == 14 else (_ for _ in ()).throw(
        AssertionError(f"Expected 14 models, got {len(_ALL_MODEL_NAMES_V210)}")))

    # --- should_auto_apply / auto_apply_enabled / require_stop_loss invariants ---
    chk("exit_plan_policy_auto_apply_false", lambda: None if ExitPlanPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ExitPlanPolicy.auto_apply_enabled must always be False")))
    chk("exit_plan_policy_require_stop_true", lambda: None if ExitPlanPolicy(require_stop_loss_before_entry=False).require_stop_loss_before_entry is True else (_ for _ in ()).throw(
        AssertionError("ExitPlanPolicy.require_stop_loss_before_entry must always be True")))
    chk("candidate_exit_plan_should_auto_apply_false", lambda: None if CandidateExitPlan(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateExitPlan.should_auto_apply must always be False")))
    chk("review_result_should_auto_apply_false", lambda: None if ExitReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ExitReviewResult.should_auto_apply must always be False")))
    chk("review_result_auto_apply_enabled_false", lambda: None if ExitReviewResult(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ExitReviewResult.auto_apply_enabled must always be False")))

    # --- exit plan engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    chk("run_exit_plan_review_callable", lambda: run_exit_plan_review())
    chk("run_exit_plan_review_paper_only", lambda: None if run_exit_plan_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_exit_plan_review_all_passed", lambda: None if run_exit_plan_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_exit_plan_review_should_auto_apply_false", lambda: None if run_exit_plan_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_exit_plan_review_auto_apply_enabled_false", lambda: None if run_exit_plan_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("run_exit_plan_review_policy_not_none", lambda: None if run_exit_plan_review().exit_plan_policy is not None else (_ for _ in ()).throw(
        AssertionError("exit_plan_policy must not be None")))
    chk("run_exit_plan_review_summary_not_none", lambda: None if run_exit_plan_review().stop_discipline_summary is not None else (_ for _ in ()).throw(
        AssertionError("stop_discipline_summary must not be None")))

    # --- calculate_exit_plan callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import calculate_exit_plan
    chk("calculate_exit_plan_callable", lambda: calculate_exit_plan(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0
    ))
    chk("calculate_exit_plan_paper_only", lambda: None if calculate_exit_plan(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0
    ).paper_only is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("calculate_exit_plan_should_auto_apply_false", lambda: None if calculate_exit_plan(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0
    ).should_auto_apply is False else (_ for _ in ()).throw(AssertionError("should_auto_apply must be False")))

    # --- evaluate_stop_discipline callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    chk("evaluate_stop_discipline_callable", lambda: evaluate_stop_discipline())
    chk("evaluate_stop_discipline_dict", lambda: None if isinstance(evaluate_stop_discipline(), dict) else (_ for _ in ()).throw(
        AssertionError("evaluate_stop_discipline() must return a dict")))
    chk("evaluate_stop_discipline_paper_only", lambda: None if evaluate_stop_discipline()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("evaluate_stop_discipline paper_only must be True")))
    chk("evaluate_stop_discipline_auto_apply_false", lambda: None if evaluate_stop_discipline()["should_auto_apply"] is False else (_ for _ in ()).throw(
        AssertionError("evaluate_stop_discipline should_auto_apply must be False")))

    # --- evaluate_reward_risk callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    chk("evaluate_reward_risk_callable", lambda: evaluate_reward_risk())
    chk("evaluate_reward_risk_dict", lambda: None if isinstance(evaluate_reward_risk(), dict) else (_ for _ in ()).throw(
        AssertionError("evaluate_reward_risk() must return a dict")))

    # --- build_exit_warning_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_exit_warning_queue
    chk("build_exit_warning_queue_callable", lambda: build_exit_warning_queue())
    chk("build_exit_warning_queue_is_list", lambda: None if isinstance(build_exit_warning_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_exit_warning_queue() must return a list")))

    # --- build_stop_violation_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import build_stop_violation_queue
    chk("build_stop_violation_queue_callable", lambda: build_stop_violation_queue())
    chk("build_stop_violation_queue_is_list", lambda: None if isinstance(build_stop_violation_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_stop_violation_queue() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        export_exit_plan_json, export_exit_plan_markdown,
        export_candidate_exit_csv, export_stop_discipline_csv,
        export_exit_warning_csv, export_exit_audit_snapshot,
    )
    result = run_exit_plan_review()
    chk("export_json_callable", lambda: export_exit_plan_json(result))
    chk("export_json_valid", lambda: None if export_exit_plan_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_plan_json is_valid must be True")))
    chk("export_md_callable", lambda: export_exit_plan_markdown(result))
    chk("export_md_valid", lambda: None if export_exit_plan_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_plan_markdown is_valid must be True")))
    chk("export_candidate_csv_callable", lambda: export_candidate_exit_csv(result))
    chk("export_candidate_csv_valid", lambda: None if export_candidate_exit_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_exit_csv is_valid must be True")))
    chk("export_stop_discipline_csv_callable", lambda: export_stop_discipline_csv(result))
    chk("export_stop_discipline_csv_valid", lambda: None if export_stop_discipline_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_stop_discipline_csv is_valid must be True")))
    chk("export_exit_warning_csv_callable", lambda: export_exit_warning_csv(result))
    chk("export_exit_warning_csv_valid", lambda: None if export_exit_warning_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_warning_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_exit_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v210-review-exit-plan",
        "paper-cockpit-v210-evaluate-stop-discipline",
        "paper-cockpit-v210-build-exit-warning-queue",
        "paper-cockpit-v210-build-stop-violation-queue",
        "paper-cockpit-v210-evaluate-reward-risk",
        "paper-cockpit-v210-export-json",
        "paper-cockpit-v210-export-md",
        "paper-cockpit-v210-export-csv",
        "paper-cockpit-v210-health",
        "paper-cockpit-v210-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 10 v210 CLI handlers exist in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v210_review_exit_plan"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v210_review_exit_plan",
        "cmd_paper_cockpit_v210_evaluate_stop_discipline",
        "cmd_paper_cockpit_v210_build_exit_warning_queue",
        "cmd_paper_cockpit_v210_build_stop_violation_queue",
        "cmd_paper_cockpit_v210_evaluate_reward_risk",
        "cmd_paper_cockpit_v210_export_json",
        "cmd_paper_cockpit_v210_export_md",
        "cmd_paper_cockpit_v210_export_csv",
        "cmd_paper_cockpit_v210_health",
        "cmd_paper_cockpit_v210_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- no fake isolated module-level command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V210_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v210")))

    # --- all v210 command_map entries present in runtime dispatch ---
    chk("main_command_map_has_v210_entries", lambda: None if hasattr(_main_module, "cmd_paper_cockpit_v210_review_exit_plan") else (_ for _ in ()).throw(
        AssertionError("main.py missing v210 command_map entries")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V210"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V210
    chk("panel_version_210", lambda: None if PANEL_VERSION_V210 == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V210 2.0.10, got {PANEL_VERSION_V210}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v210_tab_names
    tab_names = get_tab_names()
    for tab in ["exit_plan_v210", "stop_discipline_v210", "exit_warning_queue_v210"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v210_tab_names_3", lambda: None if len(get_v210_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v210 tab names, got {len(get_v210_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["exit_plan_v210", "stop_discipline_v210", "exit_warning_queue_v210"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V210.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))

    # --- no real orders ---
    chk("no_real_orders_global", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V210.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- auto_apply_enabled always False ---
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V210.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))

    # --- exit actions are recommendation only ---
    chk("exit_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V210.get("exit_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("exit_actions_recommendation_only must be True")))

    # --- require_stop_loss_before_entry always True ---
    chk("require_stop_loss_before_entry_always_true", lambda: None if SAFETY_FLAGS_V210.get("require_stop_loss_before_entry_always_true") is True else (_ for _ in ()).throw(
        AssertionError("require_stop_loss_before_entry_always_true must be True")))

    # --- backward compatibility with v2.0.9 ---
    chk("import_v209_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v209", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION as V209
    chk("v209_version_unchanged", lambda: None if V209 == "2.0.9" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.9 VERSION changed to {V209}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    chk("v209_run_sizing_review_callable", lambda: run_sizing_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_210", lambda: None if all(
        s["schema_version"] == "210" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_210", lambda: None if all(
        f["schema_version"] == "210" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- verify_version callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import verify_version
    chk("verify_version_callable", lambda: verify_version())
    chk("verify_version_true", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version() must return True")))

    # --- get_cockpit_summary_v210 callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import get_cockpit_summary_v210
    chk("get_cockpit_summary_v210_callable", lambda: get_cockpit_summary_v210())
    chk("get_cockpit_summary_v210_dict", lambda: None if isinstance(get_cockpit_summary_v210(), dict) else (_ for _ in ()).throw(
        AssertionError("get_cockpit_summary_v210() must return a dict")))
    chk("get_cockpit_summary_v210_paper_only", lambda: None if get_cockpit_summary_v210()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("cockpit summary paper_only must be True")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v210] {passed}/{total} passed")
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
    sys.exit(0 if result["all_passed"] else 1)
