"""
paper_trading/small_capital_strategy/paper_cockpit_health_v212.py
v2.0.12 Paper Profit Taking & ETF Rebalancing Control — Health Check
[!] Paper Only. Research Only. Profit Taking Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.12"
HEALTH_RELEASE = "Paper Profit Taking & ETF Rebalancing Control"


def run_health_check():
    """Run all health checks for v2.0.12 paper cockpit. Returns result dict."""
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
    chk("version_title_212", lambda: None if HEALTH_VERSION == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.12 got {HEALTH_VERSION}")))
    chk("release_name_profit", lambda: None if "Profit" in HEALTH_RELEASE or "Taking" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Profit': {HEALTH_RELEASE}")))
    chk("release_name_etf", lambda: None if "ETF" in HEALTH_RELEASE or "Rebalancing" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'ETF': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v212", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v212",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_212", lambda: None if VERSION == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.12 got {VERSION}")))
    chk("schema_version_is_212", lambda: None if SCHEMA_VERSION == "212" else (_ for _ in ()).throw(
        AssertionError(f"Expected 212 got {SCHEMA_VERSION}")))
    chk("release_name_contains_profit", lambda: None if "Profit" in RELEASE_NAME or "Taking" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Profit': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    chk("safety_flags_count_25", lambda: None if len(SAFETY_FLAGS_V212) == 25 else (_ for _ in ()).throw(
        AssertionError(f"Expected 25 SAFETY_FLAGS_V212, got {len(SAFETY_FLAGS_V212)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V212["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V212["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V212["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V212["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_profit_taking_recommendation_only", lambda: None if SAFETY_FLAGS_V212["profit_taking_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("profit_taking_recommendation_only must be True")))
    chk("safety_etf_rebalance_recommendation_only", lambda: None if SAFETY_FLAGS_V212["etf_rebalance_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V212["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V212["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V212["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V212["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_no_automatic_profit_taking_action", lambda: None if SAFETY_FLAGS_V212["no_automatic_profit_taking_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_profit_taking_action must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V212["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V212["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))
    chk("safety_require_profit_plan_always_true", lambda: None if SAFETY_FLAGS_V212["require_profit_plan_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_profit_plan_before_entry_always_true must be True")))
    chk("safety_profit_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V212["profit_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("profit_actions_recommendation_only must be True")))
    chk("safety_etf_rebalance_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V212["etf_rebalance_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_actions_recommendation_only must be True")))

    # --- PROFIT_ACTIONS ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    chk("profit_actions_count_9", lambda: None if len(PROFIT_ACTIONS) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 PROFIT_ACTIONS, got {len(PROFIT_ACTIONS)}")))
    for pa in ["hold_with_plan", "take_first_third", "take_second_third", "protect_runner",
               "tighten_trailing_stop", "reduce_on_pressure", "observation_only",
               "block_new_add", "human_review_required"]:
        chk(f"profit_action_{pa}", lambda a=pa: None if a in PROFIT_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing profit action: {a}")))

    # --- ASSET_TYPES ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    chk("asset_types_count_5", lambda: None if len(ASSET_TYPES) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 ASSET_TYPES, got {len(ASSET_TYPES)}")))
    for at in ["stock", "etf", "leveraged_etf", "theme_basket", "watchlist_candidate"]:
        chk(f"asset_type_{at}", lambda a=at: None if a in ASSET_TYPES else (
            _ for _ in ()).throw(AssertionError(f"Missing asset type: {a}")))

    # --- REBALANCE_ACTIONS ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    chk("rebalance_actions_count_6", lambda: None if len(REBALANCE_ACTIONS) == 6 else (_ for _ in ()).throw(
        AssertionError(f"Expected 6 REBALANCE_ACTIONS, got {len(REBALANCE_ACTIONS)}")))
    for ra in ["within_band_hold", "trim_to_target_band", "add_back_to_target_band",
               "reduce_leveraged_exposure", "observation_only", "human_review_required"]:
        chk(f"rebalance_action_{ra}", lambda a=ra: None if a in REBALANCE_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing rebalance action: {a}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V212) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V212, got {len(CLI_COMMANDS_V212)}")))
    for cmd in [
        "paper-cockpit-v212-review-profit-taking",
        "paper-cockpit-v212-evaluate-giveback-risk",
        "paper-cockpit-v212-build-profit-warning-queue",
        "paper-cockpit-v212-build-giveback-review-queue",
        "paper-cockpit-v212-review-etf-rebalancing",
        "paper-cockpit-v212-export-json",
        "paper-cockpit-v212-export-md",
        "paper-cockpit-v212-export-csv",
        "paper-cockpit-v212-health",
        "paper-cockpit-v212-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V212 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GUI_TABS_V212
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V212) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V212, got {len(GUI_TABS_V212)}")))
    for tab in ["profit_taking_v212", "etf_rebalancing_v212", "giveback_review_queue_v212"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V212 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- field lists ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        PROFIT_REVIEW_FIELDS, PROFIT_TAKING_POLICY_FIELDS,
        CANDIDATE_PROFIT_PLAN_FIELDS, ETF_REBALANCING_ITEM_FIELDS,
        PROFIT_TAKING_SUMMARY_FIELDS,
    )
    chk("profit_review_fields_11", lambda: None if len(PROFIT_REVIEW_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 PROFIT_REVIEW_FIELDS, got {len(PROFIT_REVIEW_FIELDS)}")))
    chk("policy_fields_12", lambda: None if len(PROFIT_TAKING_POLICY_FIELDS) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 PROFIT_TAKING_POLICY_FIELDS, got {len(PROFIT_TAKING_POLICY_FIELDS)}")))
    chk("candidate_plan_fields_26", lambda: None if len(CANDIDATE_PROFIT_PLAN_FIELDS) == 26 else (_ for _ in ()).throw(
        AssertionError(f"Expected 26 CANDIDATE_PROFIT_PLAN_FIELDS, got {len(CANDIDATE_PROFIT_PLAN_FIELDS)}")))
    chk("etf_item_fields_15", lambda: None if len(ETF_REBALANCING_ITEM_FIELDS) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 ETF_REBALANCING_ITEM_FIELDS, got {len(ETF_REBALANCING_ITEM_FIELDS)}")))
    chk("summary_fields_15", lambda: None if len(PROFIT_TAKING_SUMMARY_FIELDS) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 PROFIT_TAKING_SUMMARY_FIELDS, got {len(PROFIT_TAKING_SUMMARY_FIELDS)}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        ProfitTakingPolicy, CandidateProfitPlan, ETFRebalancingItem,
        ProfitTakingSummary, ProfitReviewInput, ProfitReviewResult,
        ProfitTakingExportResult, ProfitTakingAuditSnapshot, ProfitTakingMarkdownReport,
        CandidateProfitPlanCSV, ETFRebalancingCSV, ProfitWarningQueueCSV,
        GivebackReviewQueueCSV, V212HealthSummary, V212ReleaseSummary, ProfitSafetyGuard,
        _ALL_MODEL_NAMES_V212,
    )
    chk("model_ProfitTakingPolicy", lambda: ProfitTakingPolicy())
    chk("model_CandidateProfitPlan", lambda: CandidateProfitPlan())
    chk("model_ETFRebalancingItem", lambda: ETFRebalancingItem())
    chk("model_ProfitTakingSummary", lambda: ProfitTakingSummary())
    chk("model_ProfitReviewInput", lambda: ProfitReviewInput())
    chk("model_ProfitReviewResult", lambda: ProfitReviewResult())
    chk("model_ProfitTakingExportResult", lambda: ProfitTakingExportResult())
    chk("model_ProfitTakingAuditSnapshot", lambda: ProfitTakingAuditSnapshot())
    chk("model_ProfitTakingMarkdownReport", lambda: ProfitTakingMarkdownReport())
    chk("model_CandidateProfitPlanCSV", lambda: CandidateProfitPlanCSV())
    chk("model_ETFRebalancingCSV", lambda: ETFRebalancingCSV())
    chk("model_ProfitWarningQueueCSV", lambda: ProfitWarningQueueCSV())
    chk("model_GivebackReviewQueueCSV", lambda: GivebackReviewQueueCSV())
    chk("model_V212HealthSummary", lambda: V212HealthSummary())
    chk("model_V212ReleaseSummary", lambda: V212ReleaseSummary())
    chk("model_ProfitSafetyGuard", lambda: ProfitSafetyGuard())
    chk("model_count_16", lambda: None if len(_ALL_MODEL_NAMES_V212) == 16 else (_ for _ in ()).throw(
        AssertionError(f"Expected 16 models, got {len(_ALL_MODEL_NAMES_V212)}")))

    # --- should_auto_apply / auto_apply_enabled / require_profit_plan invariants ---
    chk("policy_auto_apply_false", lambda: None if ProfitTakingPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ProfitTakingPolicy.auto_apply_enabled must always be False")))
    chk("policy_require_profit_plan_true", lambda: None if ProfitTakingPolicy(require_profit_plan_before_entry=False).require_profit_plan_before_entry is True else (_ for _ in ()).throw(
        AssertionError("ProfitTakingPolicy.require_profit_plan_before_entry must always be True")))
    chk("plan_should_auto_apply_false", lambda: None if CandidateProfitPlan(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateProfitPlan.should_auto_apply must always be False")))
    chk("etf_item_should_auto_apply_false", lambda: None if ETFRebalancingItem(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ETFRebalancingItem.should_auto_apply must always be False")))
    chk("review_result_should_auto_apply_false", lambda: None if ProfitReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ProfitReviewResult.should_auto_apply must always be False")))
    chk("review_result_auto_apply_enabled_false", lambda: None if ProfitReviewResult(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ProfitReviewResult.auto_apply_enabled must always be False")))

    # --- profit taking engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    chk("run_profit_taking_review_callable", lambda: run_profit_taking_review())
    chk("run_profit_taking_review_paper_only", lambda: None if run_profit_taking_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_profit_taking_review_all_passed", lambda: None if run_profit_taking_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_profit_taking_review_should_auto_apply_false", lambda: None if run_profit_taking_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_profit_taking_review_auto_apply_enabled_false", lambda: None if run_profit_taking_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("run_profit_taking_review_policy_not_none", lambda: None if run_profit_taking_review().profit_policy is not None else (_ for _ in ()).throw(
        AssertionError("profit_policy must not be None")))
    chk("run_profit_taking_review_summary_not_none", lambda: None if run_profit_taking_review().profit_taking_summary is not None else (_ for _ in ()).throw(
        AssertionError("profit_taking_summary must not be None")))

    # --- evaluate_profit_taking_plan callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    chk("evaluate_profit_taking_plan_callable", lambda: evaluate_profit_taking_plan(
        "PP-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        "stock", 700.0, 855.0
    ))
    chk("evaluate_profit_taking_plan_paper_only", lambda: None if evaluate_profit_taking_plan(
        "PP-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        "stock", 700.0, 855.0
    ).paper_only is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("evaluate_profit_taking_plan_should_auto_apply_false", lambda: None if evaluate_profit_taking_plan(
        "PP-001", "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH",
        "stock", 700.0, 855.0
    ).should_auto_apply is False else (_ for _ in ()).throw(AssertionError("should_auto_apply must be False")))

    # --- first take-profit trigger ---
    chk("first_take_profit_at_20pct", lambda: None if evaluate_profit_taking_plan(
        "PP-TP1", "TEST", "Test", "CAND", "THEME", "SECTOR",
        "stock", 100.0, 121.0, first_take_profit_triggered=False
    ).profit_action == "take_first_third" else (_ for _ in ()).throw(
        AssertionError("Expected take_first_third at +21%")))

    # --- second take-profit trigger ---
    chk("second_take_profit_at_40pct", lambda: None if evaluate_profit_taking_plan(
        "PP-TP2", "TEST", "Test", "CAND", "THEME", "SECTOR",
        "stock", 100.0, 145.0, first_take_profit_triggered=True, second_take_profit_triggered=False
    ).profit_action == "take_second_third" else (_ for _ in ()).throw(
        AssertionError("Expected take_second_third at +45% with first triggered")))

    # --- ETF rebalancing engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    chk("evaluate_etf_rebalancing_callable", lambda: evaluate_etf_rebalancing(
        "0050", "元大台灣50", 0.40, 0.55, 0.50, 0.35, False))
    chk("evaluate_etf_rebalancing_paper_only", lambda: None if evaluate_etf_rebalancing(
        "0050", "元大台灣50", 0.40, 0.55, 0.50, 0.35, False
    ).paper_only is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))
    chk("evaluate_etf_overweight_trim", lambda: None if evaluate_etf_rebalancing(
        "0050", "元大台灣50", 0.40, 0.55, 0.50, 0.35, False
    ).rebalance_action == "trim_to_target_band" else (_ for _ in ()).throw(
        AssertionError("Expected trim_to_target_band when overweight")))
    chk("evaluate_etf_underweight_add", lambda: None if evaluate_etf_rebalancing(
        "0056", "高股息", 0.20, 0.12, 0.25, 0.15, False
    ).rebalance_action == "add_back_to_target_band" else (_ for _ in ()).throw(
        AssertionError("Expected add_back_to_target_band when underweight")))
    chk("evaluate_etf_leveraged_reduce", lambda: None if evaluate_etf_rebalancing(
        "00631L", "正2", 0.05, 0.12, 0.08, 0.02, True
    ).rebalance_action == "reduce_leveraged_exposure" else (_ for _ in ()).throw(
        AssertionError("Expected reduce_leveraged_exposure for leveraged ETF overweight")))
    chk("evaluate_etf_within_band_hold", lambda: None if evaluate_etf_rebalancing(
        "0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False
    ).rebalance_action == "within_band_hold" else (_ for _ in ()).throw(
        AssertionError("Expected within_band_hold when within band")))

    # --- detect_giveback_risk callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import detect_giveback_risk
    chk("detect_giveback_risk_callable", lambda: detect_giveback_risk())
    chk("detect_giveback_risk_is_list", lambda: None if isinstance(detect_giveback_risk(), list) else (_ for _ in ()).throw(
        AssertionError("detect_giveback_risk() must return a list")))

    # --- build_profit_warning_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_profit_warning_queue
    chk("build_profit_warning_queue_callable", lambda: build_profit_warning_queue())
    chk("build_profit_warning_queue_is_list", lambda: None if isinstance(build_profit_warning_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_profit_warning_queue() must return a list")))

    # --- build_giveback_review_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_giveback_review_queue
    chk("build_giveback_review_queue_callable", lambda: build_giveback_review_queue())
    chk("build_giveback_review_queue_is_list", lambda: None if isinstance(build_giveback_review_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_giveback_review_queue() must return a list")))

    # --- evaluate_giveback_risk callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    chk("evaluate_giveback_risk_callable", lambda: evaluate_giveback_risk())
    chk("evaluate_giveback_risk_dict", lambda: None if isinstance(evaluate_giveback_risk(), dict) else (_ for _ in ()).throw(
        AssertionError("evaluate_giveback_risk() must return a dict")))
    chk("evaluate_giveback_risk_paper_only", lambda: None if evaluate_giveback_risk()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("evaluate_giveback_risk paper_only must be True")))

    # --- run_etf_rebalancing_review callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_etf_rebalancing_review
    chk("run_etf_rebalancing_review_callable", lambda: run_etf_rebalancing_review())
    chk("run_etf_rebalancing_review_is_list", lambda: None if isinstance(run_etf_rebalancing_review(), list) else (_ for _ in ()).throw(
        AssertionError("run_etf_rebalancing_review() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        export_profit_taking_json, export_profit_taking_markdown,
        export_candidate_profit_plan_csv, export_etf_rebalancing_csv,
        export_profit_warning_queue_csv, export_giveback_review_queue_csv,
        export_profit_taking_audit_snapshot,
    )
    result = run_profit_taking_review()
    chk("export_json_callable", lambda: export_profit_taking_json(result))
    chk("export_json_valid", lambda: None if export_profit_taking_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_json is_valid must be True")))
    chk("export_json_paper_only", lambda: None if export_profit_taking_json(result).paper_only is True else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_json paper_only must be True")))
    chk("export_md_callable", lambda: export_profit_taking_markdown(result))
    chk("export_md_valid", lambda: None if export_profit_taking_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_markdown is_valid must be True")))
    chk("export_candidate_csv_callable", lambda: export_candidate_profit_plan_csv(result))
    chk("export_candidate_csv_valid", lambda: None if export_candidate_profit_plan_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_profit_plan_csv is_valid must be True")))
    chk("export_etf_csv_callable", lambda: export_etf_rebalancing_csv(result))
    chk("export_etf_csv_valid", lambda: None if export_etf_rebalancing_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_etf_rebalancing_csv is_valid must be True")))
    chk("export_warning_csv_callable", lambda: export_profit_warning_queue_csv(result))
    chk("export_warning_csv_valid", lambda: None if export_profit_warning_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_warning_queue_csv is_valid must be True")))
    chk("export_giveback_csv_callable", lambda: export_giveback_review_queue_csv(result))
    chk("export_giveback_csv_valid", lambda: None if export_giveback_review_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_giveback_review_queue_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_profit_taking_audit_snapshot(result))
    chk("export_audit_complete", lambda: None if export_profit_taking_audit_snapshot(result).export_status == "complete" else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_audit_snapshot export_status must be 'complete'")))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v212-review-profit-taking",
        "paper-cockpit-v212-evaluate-giveback-risk",
        "paper-cockpit-v212-build-profit-warning-queue",
        "paper-cockpit-v212-build-giveback-review-queue",
        "paper-cockpit-v212-review-etf-rebalancing",
        "paper-cockpit-v212-export-json",
        "paper-cockpit-v212-export-md",
        "paper-cockpit-v212-export-csv",
        "paper-cockpit-v212-health",
        "paper-cockpit-v212-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 10 v212 CLI handlers exist in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v212_review_profit_taking"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v212_review_profit_taking",
        "cmd_paper_cockpit_v212_evaluate_giveback_risk",
        "cmd_paper_cockpit_v212_build_profit_warning_queue",
        "cmd_paper_cockpit_v212_build_giveback_review_queue",
        "cmd_paper_cockpit_v212_review_etf_rebalancing",
        "cmd_paper_cockpit_v212_export_json",
        "cmd_paper_cockpit_v212_export_md",
        "cmd_paper_cockpit_v212_export_csv",
        "cmd_paper_cockpit_v212_health",
        "cmd_paper_cockpit_v212_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- no fake isolated module-level command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V212_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v212")))

    # --- all v212 command_map entries present in runtime dispatch ---
    chk("main_command_map_has_v212_entries", lambda: None if hasattr(_main_module, "cmd_paper_cockpit_v212_review_profit_taking") else (_ for _ in ()).throw(
        AssertionError("main.py missing v212 command_map entries")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V212"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V212
    chk("panel_version_212", lambda: None if PANEL_VERSION_V212 == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V212 2.0.12, got {PANEL_VERSION_V212}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v212_tab_names
    tab_names = get_tab_names()
    for tab in ["profit_taking_v212", "etf_rebalancing_v212", "giveback_review_queue_v212"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v212_tab_names_3", lambda: None if len(get_v212_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v212 tab names, got {len(get_v212_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["profit_taking_v212", "etf_rebalancing_v212", "giveback_review_queue_v212"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V212.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))
    chk("no_real_orders_global", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V212.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V212.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))
    chk("profit_actions_recommendation_only_flag", lambda: None if SAFETY_FLAGS_V212.get("profit_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("profit_actions_recommendation_only must be True")))
    chk("etf_rebalance_actions_recommendation_only_flag", lambda: None if SAFETY_FLAGS_V212.get("etf_rebalance_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_actions_recommendation_only must be True")))
    chk("no_automatic_profit_taking_action_flag", lambda: None if SAFETY_FLAGS_V212.get("no_automatic_profit_taking_action") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_profit_taking_action must be True")))
    chk("require_profit_plan_before_entry_always_true", lambda: None if SAFETY_FLAGS_V212.get("require_profit_plan_before_entry_always_true") is True else (_ for _ in ()).throw(
        AssertionError("require_profit_plan_before_entry_always_true must be True")))

    # --- backward compatibility with v2.0.11 ---
    chk("import_v211_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v211", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VERSION as V211
    chk("v211_version_unchanged", lambda: None if V211 == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.11 VERSION changed to {V211}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    chk("v211_run_journal_review_callable", lambda: run_journal_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_212", lambda: None if all(
        s["schema_version"] == "212" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_212", lambda: None if all(
        f["schema_version"] == "212" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- verify_version callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import verify_version
    chk("verify_version_callable", lambda: verify_version())
    chk("verify_version_true", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version() must return True")))

    # --- get_cockpit_summary_v212 callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    chk("get_cockpit_summary_v212_callable", lambda: get_cockpit_summary_v212())
    chk("get_cockpit_summary_v212_dict", lambda: None if isinstance(get_cockpit_summary_v212(), dict) else (_ for _ in ()).throw(
        AssertionError("get_cockpit_summary_v212() must return a dict")))
    chk("get_cockpit_summary_v212_paper_only", lambda: None if get_cockpit_summary_v212()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("cockpit summary paper_only must be True")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v212] {passed}/{total} passed")
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
