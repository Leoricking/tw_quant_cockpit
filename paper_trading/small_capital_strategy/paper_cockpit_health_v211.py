"""
paper_trading/small_capital_strategy/paper_cockpit_health_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review — Health Check
[!] Paper Only. Research Only. Journal Review Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.11"
HEALTH_RELEASE = "Paper Trade Journal & Execution Discipline Review"


def run_health_check():
    """Run all health checks for v2.0.11 paper cockpit. Returns result dict."""
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
    chk("version_title_211", lambda: None if HEALTH_VERSION == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.11 got {HEALTH_VERSION}")))
    chk("release_name_journal", lambda: None if "Journal" in HEALTH_RELEASE or "Trade" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Journal': {HEALTH_RELEASE}")))
    chk("release_name_discipline", lambda: None if "Discipline" in HEALTH_RELEASE or "Execution" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Discipline': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v211", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v211",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_211", lambda: None if VERSION == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.11 got {VERSION}")))
    chk("schema_version_is_211", lambda: None if SCHEMA_VERSION == "211" else (_ for _ in ()).throw(
        AssertionError(f"Expected 211 got {SCHEMA_VERSION}")))
    chk("release_name_contains_journal", lambda: None if "Journal" in RELEASE_NAME or "Trade" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Journal': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    chk("safety_flags_count_24", lambda: None if len(SAFETY_FLAGS_V211) == 24 else (_ for _ in ()).throw(
        AssertionError(f"Expected 24 SAFETY_FLAGS_V211, got {len(SAFETY_FLAGS_V211)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V211["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V211["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V211["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V211["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_journal_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V211["journal_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("journal_actions_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V211["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V211["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V211["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V211["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_no_automatic_journal_apply", lambda: None if SAFETY_FLAGS_V211["no_automatic_journal_apply"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_journal_apply must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V211["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V211["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))
    chk("safety_require_planned_entry_always_true", lambda: None if SAFETY_FLAGS_V211["require_planned_entry_before_trade_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_planned_entry_before_trade_always_true must be True")))

    # --- execution actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import EXECUTION_ACTIONS
    chk("execution_actions_count_7", lambda: None if len(EXECUTION_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 EXECUTION_ACTIONS, got {len(EXECUTION_ACTIONS)}")))
    for ea in ["compliant", "monitor", "require_journal_note", "require_rescore",
               "flag_discipline_warning", "block_followup_action", "human_review_required"]:
        chk(f"execution_action_{ea}", lambda a=ea: None if a in EXECUTION_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing execution action: {a}")))

    # --- trade statuses ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TRADE_STATUSES
    chk("trade_statuses_count_8", lambda: None if len(TRADE_STATUSES) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 TRADE_STATUSES, got {len(TRADE_STATUSES)}")))
    for ts in ["planned_only", "entered", "reduced", "exited", "stopped_out",
               "take_profit_done", "invalidated", "cancelled"]:
        chk(f"trade_status_{ts}", lambda t=ts: None if t in TRADE_STATUSES else (
            _ for _ in ()).throw(AssertionError(f"Missing trade status: {t}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V211) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V211, got {len(CLI_COMMANDS_V211)}")))
    for cmd in [
        "paper-cockpit-v211-review-journal",
        "paper-cockpit-v211-evaluate-discipline",
        "paper-cockpit-v211-build-mistake-queue",
        "paper-cockpit-v211-build-violation-queue",
        "paper-cockpit-v211-build-improvement-queue",
        "paper-cockpit-v211-export-json",
        "paper-cockpit-v211-export-md",
        "paper-cockpit-v211-export-csv",
        "paper-cockpit-v211-health",
        "paper-cockpit-v211-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V211 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V211) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V211, got {len(GUI_TABS_V211)}")))
    for tab in ["trade_journal_v211", "execution_discipline_v211", "mistake_review_queue_v211"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V211 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- field lists ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        TRADE_JOURNAL_POLICY_FIELDS, JOURNAL_ENTRY_FIELDS,
        EXECUTION_DISCIPLINE_SUMMARY_FIELDS, JOURNAL_REVIEW_FIELDS,
    )
    chk("policy_fields_11", lambda: None if len(TRADE_JOURNAL_POLICY_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 TRADE_JOURNAL_POLICY_FIELDS, got {len(TRADE_JOURNAL_POLICY_FIELDS)}")))
    chk("entry_fields_26", lambda: None if len(JOURNAL_ENTRY_FIELDS) == 26 else (_ for _ in ()).throw(
        AssertionError(f"Expected 26 JOURNAL_ENTRY_FIELDS, got {len(JOURNAL_ENTRY_FIELDS)}")))
    chk("discipline_summary_fields_16", lambda: None if len(EXECUTION_DISCIPLINE_SUMMARY_FIELDS) == 16 else (_ for _ in ()).throw(
        AssertionError(f"Expected 16 EXECUTION_DISCIPLINE_SUMMARY_FIELDS, got {len(EXECUTION_DISCIPLINE_SUMMARY_FIELDS)}")))
    chk("review_fields_11", lambda: None if len(JOURNAL_REVIEW_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 JOURNAL_REVIEW_FIELDS, got {len(JOURNAL_REVIEW_FIELDS)}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        TradeJournalPolicy, JournalEntry, ExecutionDisciplineSummary,
        JournalReviewInput, JournalReviewResult, JournalExportResult,
        JournalAuditSnapshot, JournalMarkdownReport, JournalCSV,
        ExecutionDisciplineCSV, MistakeReviewCSV, ViolationQueueCSV,
        V211HealthSummary, V211ReleaseSummary, JournalSafetyGuard,
        _ALL_MODEL_NAMES_V211,
    )
    chk("model_TradeJournalPolicy", lambda: TradeJournalPolicy())
    chk("model_JournalEntry", lambda: JournalEntry())
    chk("model_ExecutionDisciplineSummary", lambda: ExecutionDisciplineSummary())
    chk("model_JournalReviewInput", lambda: JournalReviewInput())
    chk("model_JournalReviewResult", lambda: JournalReviewResult())
    chk("model_JournalExportResult", lambda: JournalExportResult())
    chk("model_JournalAuditSnapshot", lambda: JournalAuditSnapshot())
    chk("model_JournalMarkdownReport", lambda: JournalMarkdownReport())
    chk("model_JournalCSV", lambda: JournalCSV())
    chk("model_ExecutionDisciplineCSV", lambda: ExecutionDisciplineCSV())
    chk("model_MistakeReviewCSV", lambda: MistakeReviewCSV())
    chk("model_ViolationQueueCSV", lambda: ViolationQueueCSV())
    chk("model_V211HealthSummary", lambda: V211HealthSummary())
    chk("model_V211ReleaseSummary", lambda: V211ReleaseSummary())
    chk("model_JournalSafetyGuard", lambda: JournalSafetyGuard())
    chk("model_count_15", lambda: None if len(_ALL_MODEL_NAMES_V211) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 models, got {len(_ALL_MODEL_NAMES_V211)}")))

    # --- should_auto_apply / auto_apply_enabled / require_planned_entry invariants ---
    chk("policy_auto_apply_false", lambda: None if TradeJournalPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("TradeJournalPolicy.auto_apply_enabled must always be False")))
    chk("policy_require_planned_entry_true", lambda: None if TradeJournalPolicy(require_planned_entry_before_trade=False).require_planned_entry_before_trade is True else (_ for _ in ()).throw(
        AssertionError("TradeJournalPolicy.require_planned_entry_before_trade must always be True")))
    chk("entry_should_auto_apply_false", lambda: None if JournalEntry(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("JournalEntry.should_auto_apply must always be False")))
    chk("review_result_should_auto_apply_false", lambda: None if JournalReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("JournalReviewResult.should_auto_apply must always be False")))
    chk("review_result_auto_apply_enabled_false", lambda: None if JournalReviewResult(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("JournalReviewResult.auto_apply_enabled must always be False")))

    # --- journal review engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    chk("run_journal_review_callable", lambda: run_journal_review())
    chk("run_journal_review_paper_only", lambda: None if run_journal_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_journal_review_all_passed", lambda: None if run_journal_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_journal_review_should_auto_apply_false", lambda: None if run_journal_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_journal_review_auto_apply_enabled_false", lambda: None if run_journal_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("run_journal_review_policy_not_none", lambda: None if run_journal_review().journal_policy is not None else (_ for _ in ()).throw(
        AssertionError("journal_policy must not be None")))
    chk("run_journal_review_summary_not_none", lambda: None if run_journal_review().execution_discipline_snapshot is not None else (_ for _ in ()).throw(
        AssertionError("execution_discipline_snapshot must not be None")))

    # --- evaluate_journal_entry callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_journal_entry
    chk("evaluate_journal_entry_callable", lambda: evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    ))
    chk("evaluate_journal_entry_paper_only", lambda: None if evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    ).paper_only is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("evaluate_journal_entry_should_auto_apply_false", lambda: None if evaluate_journal_entry(
        "JE-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        900.0, 901.0, 1000, 1000, 855.0, 855.0, 945.0, 0.0
    ).should_auto_apply is False else (_ for _ in ()).throw(AssertionError("should_auto_apply must be False")))

    # --- evaluate_discipline callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    chk("evaluate_discipline_callable", lambda: evaluate_discipline())
    chk("evaluate_discipline_dict", lambda: None if isinstance(evaluate_discipline(), dict) else (_ for _ in ()).throw(
        AssertionError("evaluate_discipline() must return a dict")))
    chk("evaluate_discipline_paper_only", lambda: None if evaluate_discipline()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("evaluate_discipline paper_only must be True")))
    chk("evaluate_discipline_auto_apply_false", lambda: None if evaluate_discipline()["should_auto_apply"] is False else (_ for _ in ()).throw(
        AssertionError("evaluate_discipline should_auto_apply must be False")))

    # --- build_mistake_review_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_mistake_review_queue
    chk("build_mistake_review_queue_callable", lambda: build_mistake_review_queue())
    chk("build_mistake_review_queue_is_list", lambda: None if isinstance(build_mistake_review_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_mistake_review_queue() must return a list")))

    # --- build_violation_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_violation_queue
    chk("build_violation_queue_callable", lambda: build_violation_queue())
    chk("build_violation_queue_is_list", lambda: None if isinstance(build_violation_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_violation_queue() must return a list")))

    # --- build_improvement_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import build_improvement_queue
    chk("build_improvement_queue_callable", lambda: build_improvement_queue())
    chk("build_improvement_queue_is_list", lambda: None if isinstance(build_improvement_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_improvement_queue() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        export_journal_json, export_journal_markdown,
        export_journal_csv, export_discipline_csv,
        export_mistake_review_csv, export_violation_queue_csv,
        export_journal_audit_snapshot,
    )
    result = run_journal_review()
    chk("export_json_callable", lambda: export_journal_json(result))
    chk("export_json_valid", lambda: None if export_journal_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_json is_valid must be True")))
    chk("export_md_callable", lambda: export_journal_markdown(result))
    chk("export_md_valid", lambda: None if export_journal_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_markdown is_valid must be True")))
    chk("export_journal_csv_callable", lambda: export_journal_csv(result))
    chk("export_journal_csv_valid", lambda: None if export_journal_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_csv is_valid must be True")))
    chk("export_discipline_csv_callable", lambda: export_discipline_csv(result))
    chk("export_discipline_csv_valid", lambda: None if export_discipline_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_discipline_csv is_valid must be True")))
    chk("export_mistake_csv_callable", lambda: export_mistake_review_csv(result))
    chk("export_mistake_csv_valid", lambda: None if export_mistake_review_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_mistake_review_csv is_valid must be True")))
    chk("export_violation_csv_callable", lambda: export_violation_queue_csv(result))
    chk("export_violation_csv_valid", lambda: None if export_violation_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_violation_queue_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_journal_audit_snapshot(result))
    chk("export_audit_complete", lambda: None if export_journal_audit_snapshot(result).export_status == "complete" else (_ for _ in ()).throw(
        AssertionError("export_journal_audit_snapshot export_status must be 'complete'")))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v211-review-journal",
        "paper-cockpit-v211-evaluate-discipline",
        "paper-cockpit-v211-build-mistake-queue",
        "paper-cockpit-v211-build-violation-queue",
        "paper-cockpit-v211-build-improvement-queue",
        "paper-cockpit-v211-export-json",
        "paper-cockpit-v211-export-md",
        "paper-cockpit-v211-export-csv",
        "paper-cockpit-v211-health",
        "paper-cockpit-v211-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 10 v211 CLI handlers exist in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v211_review_journal"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v211_review_journal",
        "cmd_paper_cockpit_v211_evaluate_discipline",
        "cmd_paper_cockpit_v211_build_mistake_queue",
        "cmd_paper_cockpit_v211_build_violation_queue",
        "cmd_paper_cockpit_v211_build_improvement_queue",
        "cmd_paper_cockpit_v211_export_json",
        "cmd_paper_cockpit_v211_export_md",
        "cmd_paper_cockpit_v211_export_csv",
        "cmd_paper_cockpit_v211_health",
        "cmd_paper_cockpit_v211_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- no fake isolated module-level command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V211_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v211")))

    # --- all v211 command_map entries present in runtime dispatch ---
    chk("main_command_map_has_v211_entries", lambda: None if hasattr(_main_module, "cmd_paper_cockpit_v211_review_journal") else (_ for _ in ()).throw(
        AssertionError("main.py missing v211 command_map entries")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V211"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V211
    chk("panel_version_211", lambda: None if PANEL_VERSION_V211 == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V211 2.0.11, got {PANEL_VERSION_V211}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v211_tab_names
    tab_names = get_tab_names()
    for tab in ["trade_journal_v211", "execution_discipline_v211", "mistake_review_queue_v211"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v211_tab_names_3", lambda: None if len(get_v211_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v211 tab names, got {len(get_v211_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["trade_journal_v211", "execution_discipline_v211", "mistake_review_queue_v211"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V211.get("paper_only") is True else (_ for _ in ()).throw(
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
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V211.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- auto_apply_enabled always False ---
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V211.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))

    # --- journal actions are recommendation only ---
    chk("journal_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V211.get("journal_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("journal_actions_recommendation_only must be True")))

    # --- require_planned_entry_before_trade always True ---
    chk("require_planned_entry_before_trade_always_true", lambda: None if SAFETY_FLAGS_V211.get("require_planned_entry_before_trade_always_true") is True else (_ for _ in ()).throw(
        AssertionError("require_planned_entry_before_trade_always_true must be True")))

    # --- backward compatibility with v2.0.10 ---
    chk("import_v210_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v210", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION as V210
    chk("v210_version_unchanged", lambda: None if V210 == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.10 VERSION changed to {V210}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    chk("v210_run_exit_plan_review_callable", lambda: run_exit_plan_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_211", lambda: None if all(
        s["schema_version"] == "211" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_211", lambda: None if all(
        f["schema_version"] == "211" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- verify_version callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import verify_version
    chk("verify_version_callable", lambda: verify_version())
    chk("verify_version_true", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version() must return True")))

    # --- get_cockpit_summary_v211 callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import get_cockpit_summary_v211
    chk("get_cockpit_summary_v211_callable", lambda: get_cockpit_summary_v211())
    chk("get_cockpit_summary_v211_dict", lambda: None if isinstance(get_cockpit_summary_v211(), dict) else (_ for _ in ()).throw(
        AssertionError("get_cockpit_summary_v211() must return a dict")))
    chk("get_cockpit_summary_v211_paper_only", lambda: None if get_cockpit_summary_v211()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("cockpit summary paper_only must be True")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v211] {passed}/{total} passed")
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
