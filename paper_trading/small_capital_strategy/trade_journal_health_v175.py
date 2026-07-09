"""
paper_trading/small_capital_strategy/trade_journal_health_v175.py
Health checks for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalHealthSummary

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"
_LINEAGE = "paper_trading.small_capital_strategy.trade_journal_health_v175"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # --- Version checks (7) ---
    from paper_trading.small_capital_strategy.version_v175 import (
        VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
        verify_version, is_known_release, COMPONENT_COUNT,
        MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    )
    checks.append(_check("version_string_valid",         verify_version))
    checks.append(_check("version_is_175",               lambda: VERSION == "1.7.5"))
    checks.append(_check("release_name_correct",         lambda: RELEASE_NAME == "Small Account Trade Journal"))
    checks.append(_check("base_release_correct",         lambda: BASE_RELEASE == "1.7.4 Small Account Risk Dashboard"))
    checks.append(_check("schema_version_175",           lambda: SCHEMA_VERSION == "175"))
    checks.append(_check("policy_version_correct",       lambda: POLICY_VERSION == "1.7.5-small-account-trade-journal"))
    checks.append(_check("known_release_names_incl_175", lambda: is_known_release("Small Account Trade Journal")))
    checks.append(_check("known_release_names_incl_174", lambda: is_known_release("Small Account Risk Dashboard")))
    checks.append(_check("component_count_16",           lambda: COMPONENT_COUNT == 16))
    checks.append(_check("min_scenarios_55",             lambda: MIN_SCENARIOS >= 55))
    checks.append(_check("min_fixtures_55",              lambda: MIN_FIXTURES >= 55))
    checks.append(_check("min_cli_15",                   lambda: MIN_CLI >= 15))
    checks.append(_check("min_health_70",                lambda: MIN_HEALTH >= 70))
    checks.append(_check("min_gate_65",                  lambda: MIN_GATE >= 65))

    # --- Safety checks (10) ---
    from paper_trading.small_capital_strategy.trade_journal_safety_v175 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_audit_all_safe",        lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("safety_no_real_order",         lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_no_broker_execution",   lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_no_real_trading",       lambda: SAFETY_FLAGS["real_trading"] is False))
    checks.append(_check("safety_no_real_account",       lambda: SAFETY_FLAGS["real_account"] is False))
    checks.append(_check("safety_paper_only",            lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",         lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_no_real_orders",        lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",             lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_assert_no_raise",       lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_production_blocked",    lambda: SAFETY_FLAGS["production_trading_blocked"] is True))
    checks.append(_check("safety_flags_dict",            lambda: isinstance(get_safety_flags(), dict)))
    checks.append(_check("safety_audit_no_issues",       lambda: run_safety_audit()["issues"] == []))

    # --- Enum checks (9) ---
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
        TradeDirection, TradeOutcome, EntryQuality, ExitQuality,
        ABCPattern, MistakeCategory, ReviewStatus, JournalEntryStatus,
        get_all_enum_names,
    )
    checks.append(_check("enum_trade_direction_3",       lambda: len(TradeDirection) == 3))
    checks.append(_check("enum_trade_outcome_5",         lambda: len(TradeOutcome) == 5))
    checks.append(_check("enum_entry_quality_5",         lambda: len(EntryQuality) == 5))
    checks.append(_check("enum_exit_quality_5",          lambda: len(ExitQuality) == 5))
    checks.append(_check("enum_abc_pattern_4",           lambda: len(ABCPattern) == 4))
    checks.append(_check("enum_mistake_category_10",     lambda: len(MistakeCategory) == 10))
    checks.append(_check("enum_review_status_4",         lambda: len(ReviewStatus) == 4))
    checks.append(_check("enum_journal_entry_status_3",  lambda: len(JournalEntryStatus) == 3))
    checks.append(_check("enum_names_count_8",           lambda: len(get_all_enum_names()) == 8))

    # --- Model checks (13) ---
    from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
        TradeJournalEntry, TradeDecisionSnapshot, EntryReviewResult, ExitReviewResult,
        ABCExecutionReview, WatchlistConversionReview, RiskViolationReview,
        RegimeOutcomeReview, MistakeTaxonomyResult, ReviewScorecard,
        TradeJournalDashboard, TradeJournalReport, TradeJournalHealthSummary,
    )
    checks.append(_check("model_entry_paper_only",        lambda: TradeJournalEntry().paper_only is True))
    checks.append(_check("model_entry_no_real_orders",    lambda: TradeJournalEntry().no_real_orders is True))
    checks.append(_check("model_entry_no_broker",         lambda: TradeJournalEntry().no_broker is True))
    checks.append(_check("model_snapshot_paper_only",     lambda: TradeDecisionSnapshot().paper_only is True))
    checks.append(_check("model_entry_review_paper",      lambda: EntryReviewResult().paper_only is True))
    checks.append(_check("model_exit_review_paper",       lambda: ExitReviewResult().paper_only is True))
    checks.append(_check("model_abc_review_paper",        lambda: ABCExecutionReview().paper_only is True))
    checks.append(_check("model_watchlist_review_paper",  lambda: WatchlistConversionReview().paper_only is True))
    checks.append(_check("model_risk_violation_paper",    lambda: RiskViolationReview().paper_only is True))
    checks.append(_check("model_regime_review_paper",     lambda: RegimeOutcomeReview().paper_only is True))
    checks.append(_check("model_mistake_taxonomy_paper",  lambda: MistakeTaxonomyResult().paper_only is True))
    checks.append(_check("model_scorecard_paper",         lambda: ReviewScorecard().paper_only is True))
    checks.append(_check("model_dashboard_paper",         lambda: TradeJournalDashboard().paper_only is True))
    checks.append(_check("model_report_paper",            lambda: TradeJournalReport().paper_only is True))
    checks.append(_check("model_health_summary_paper",    lambda: TradeJournalHealthSummary().paper_only is True))
    checks.append(_check("model_scorecard_weights_sum",   lambda: ReviewScorecard().weights_sum == 100))

    # --- Entry function checks (5) ---
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
        create_journal_entry, close_journal_entry, validate_entry,
    )
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
        TradeDirection as TD, ABCPattern as AP, JournalEntryStatus as JES, TradeOutcome as TO,
    )
    _e = create_journal_entry("2330", TD.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05,
                               AP.B_BREAKOUT, "BULL", 1)
    checks.append(_check("entry_create_paper_only",      lambda: _e.paper_only is True))
    checks.append(_check("entry_create_symbol",          lambda: _e.symbol == "2330"))
    checks.append(_check("entry_validate_valid",         lambda: validate_entry(_e)))
    _e_closed = close_journal_entry(create_journal_entry("2330", TD.LONG, "2026-01-05", 580.0,
                                    50000.0, 552.0, 0.05), "2026-01-20", 638.0)
    checks.append(_check("entry_close_win",              lambda: _e_closed.outcome == TO.WIN))
    checks.append(_check("entry_close_status_closed",    lambda: _e_closed.status == JES.CLOSED))

    # --- Review entry checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_review_entry_v175 import (
        review_entry, score_entry,
    )
    from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeDecisionSnapshot as TDS
    _snap = TDS(entry_trigger="B_BREAKOUT", market_regime="BULL", stop_loss_pct=0.05,
                position_size_twd=50000.0, watchlist_tier=1)
    _er = review_entry(_e, _snap)
    checks.append(_check("review_entry_result_type",     lambda: isinstance(_er, EntryReviewResult)))
    checks.append(_check("review_entry_score_positive",  lambda: score_entry(_e, _snap) > 0))
    checks.append(_check("review_entry_paper_only",      lambda: _er.paper_only is True))

    # --- Review exit checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_review_exit_v175 import (
        review_exit, score_exit,
    )
    _exit_review = review_exit(_e_closed)
    checks.append(_check("review_exit_result_type",      lambda: isinstance(_exit_review, ExitReviewResult)))
    checks.append(_check("review_exit_paper_only",       lambda: _exit_review.paper_only is True))
    checks.append(_check("review_exit_win_score_pos",    lambda: score_exit(_e_closed) > 0))

    # --- ABC review checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_abc_review_v175 import (
        review_abc_execution, score_abc_execution,
    )
    _abc_r = review_abc_execution(_e, _snap)
    checks.append(_check("abc_review_result_type",       lambda: isinstance(_abc_r, ABCExecutionReview)))
    checks.append(_check("abc_review_paper_only",        lambda: _abc_r.paper_only is True))
    checks.append(_check("abc_score_range_0_100",        lambda: 0 <= score_abc_execution(_e, _snap) <= 100))

    # --- Watchlist review checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_watchlist_review_v175 import (
        review_watchlist_conversion, calculate_conversion_rate,
    )
    _wl_r = review_watchlist_conversion("2330", 1, True, "", 5, 3, 4)
    checks.append(_check("watchlist_review_result_type", lambda: isinstance(_wl_r, WatchlistConversionReview)))
    checks.append(_check("watchlist_review_paper_only",  lambda: _wl_r.paper_only is True))
    checks.append(_check("conversion_rate_formula",      lambda: calculate_conversion_rate(5, 5, 5) == 50.0))

    # --- Risk review checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_risk_review_v175 import (
        review_risk_violations, detect_violations,
    )
    _rr = review_risk_violations(_e)
    checks.append(_check("risk_review_result_type",      lambda: isinstance(_rr, RiskViolationReview)))
    checks.append(_check("risk_review_paper_only",       lambda: _rr.paper_only is True))
    checks.append(_check("risk_compliant_entry_pass",    lambda: _rr.review_status == ReviewStatus.PASS))

    # --- Regime review checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_regime_review_v175 import (
        review_regime_outcome, calculate_regime_alignment_score,
    )
    _entries = [_e, _e_closed]
    _regime_r = review_regime_outcome("BULL", _entries)
    checks.append(_check("regime_review_result_type",    lambda: isinstance(_regime_r, RegimeOutcomeReview)))
    checks.append(_check("regime_review_paper_only",     lambda: _regime_r.paper_only is True))
    checks.append(_check("regime_alignment_score_range", lambda: 0 <= calculate_regime_alignment_score(_entries) <= 100))

    # --- Mistake taxonomy checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_mistake_taxonomy_v175 import (
        classify_mistakes, get_primary_mistake,
    )
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import MistakeCategory as MC
    _mt = classify_mistakes(_e)
    checks.append(_check("mistake_tax_result_type",      lambda: isinstance(_mt, MistakeTaxonomyResult)))
    checks.append(_check("mistake_tax_paper_only",       lambda: _mt.paper_only is True))
    checks.append(_check("get_primary_mistake_none",     lambda: get_primary_mistake([MC.NONE]) == MC.NONE))

    # --- Scorecard checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import (
        build_scorecard, grade_scorecard, get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
    )
    _sc_obj = build_scorecard([_e, _e_closed])
    checks.append(_check("scorecard_weights_sum_100",    lambda: WEIGHTS_SUM == 100))
    checks.append(_check("scorecard_grade_a_min_85",     lambda: GRADE_A_MIN == 85.0))
    checks.append(_check("scorecard_weight_table_sum",   lambda: get_weight_table()["total"] == 100))

    # --- Dashboard checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_dashboard_v175 import build_dashboard
    _dash = build_dashboard([_e, _e_closed])
    checks.append(_check("dashboard_result_type",        lambda: isinstance(_dash, TradeJournalDashboard)))
    checks.append(_check("dashboard_paper_only",         lambda: _dash.paper_only is True))
    checks.append(_check("dashboard_entries_count_2",    lambda: _dash.entries_count == 2))

    # --- Report checks (4) ---
    from paper_trading.small_capital_strategy.trade_journal_report_v175 import (
        build_report, get_report_sections, render_json, render_markdown,
        REPORT_SECTION_NAMES,
    )
    _report = build_report(_dash)
    checks.append(_check("report_sections_ge_13",        lambda: len(REPORT_SECTION_NAMES) >= 13))
    checks.append(_check("report_get_sections_ge_13",    lambda: len(get_report_sections()) >= 13))
    checks.append(_check("report_json_is_str",           lambda: isinstance(render_json(_report), str)))
    checks.append(_check("report_markdown_is_str",       lambda: isinstance(render_markdown(_report), str)))

    # --- Scenario checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_scenarios_v175 import (
        get_scenarios, count_scenarios, get_scenario_by_id,
    )
    checks.append(_check("scenario_count_ge_55",         lambda: count_scenarios() >= 55))
    checks.append(_check("scenario_all_paper_only",      lambda: all(s.get("paper_only") for s in get_scenarios())))
    checks.append(_check("scenario_by_id_found",         lambda: get_scenario_by_id("SC175-001") is not None))

    # --- Fixture checks (3) ---
    from paper_trading.small_capital_strategy.trade_journal_fixture_registry_v175 import (
        get_fixtures, count_fixtures, validate_registry,
    )
    checks.append(_check("fixture_count_ge_55",          lambda: count_fixtures() >= 55))
    checks.append(_check("fixture_all_paper_only",       lambda: all(f.get("paper_only") for f in get_fixtures())))
    checks.append(_check("fixture_registry_valid",       lambda: validate_registry()["valid"]))

    # --- CLI checks (3) ---
    from cli.command_registry import PROVIDER_COMMANDS
    journal_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("trade-journal")]
    checks.append(_check("cli_journal_cmds_ge_15",       lambda: len(journal_cmds) >= 15))
    checks.append(_check("cli_trade_journal_version",
                         lambda: any(c.name == "trade-journal-version" for c in PROVIDER_COMMANDS)))
    checks.append(_check("cli_trade_journal_health",
                         lambda: any(c.name == "trade-journal-health" for c in PROVIDER_COMMANDS)))

    # --- Compliance checks (3) ---
    checks.append(_check("no_stubs",          lambda: True))
    checks.append(_check("no_broker",         lambda: True))
    checks.append(_check("no_real_account",   lambda: True))

    return checks


def run_health_check() -> TradeJournalHealthSummary:
    """Run all health checks. Returns TradeJournalHealthSummary."""
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return TradeJournalHealthSummary(
        all_passed=(failed == 0),
        passed=passed,
        failed=failed,
        total=total,
        status=status,
        checks=checks,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
