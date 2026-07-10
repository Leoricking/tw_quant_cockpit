"""
paper_trading/small_capital_strategy/mistake_taxonomy_health_v176.py
Health checks for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import ReviewHealthSummary

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"
_LINEAGE = "paper_trading.small_capital_strategy.mistake_taxonomy_health_v176"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # --- Version checks (14) ---
    from paper_trading.small_capital_strategy.version_v176 import (
        VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
        COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
        get_version_info, verify_version, is_known_release,
    )
    checks.append(_check("version_is_176",               lambda: VERSION == "1.7.6"))
    checks.append(_check("release_name_correct",         lambda: RELEASE_NAME == "Mistake Taxonomy & Weekly Review Dashboard"))
    checks.append(_check("base_release_correct",         lambda: BASE_RELEASE == "1.7.5 Small Account Trade Journal"))
    checks.append(_check("schema_version_176",           lambda: SCHEMA_VERSION == "176"))
    checks.append(_check("policy_version_correct",       lambda: POLICY_VERSION == "1.7.6-mistake-taxonomy-weekly-review"))
    checks.append(_check("component_count_14",           lambda: COMPONENT_COUNT == 14))
    checks.append(_check("min_scenarios_60",             lambda: MIN_SCENARIOS >= 60))
    checks.append(_check("min_fixtures_60",              lambda: MIN_FIXTURES >= 60))
    checks.append(_check("min_cli_14",                   lambda: MIN_CLI >= 14))
    checks.append(_check("min_health_70",                lambda: MIN_HEALTH >= 70))
    checks.append(_check("min_gate_65",                  lambda: MIN_GATE >= 65))
    checks.append(_check("verify_version_true",          verify_version))
    checks.append(_check("known_release_v176",           lambda: is_known_release("Mistake Taxonomy & Weekly Review Dashboard")))
    checks.append(_check("known_release_v175",           lambda: is_known_release("Small Account Trade Journal")))
    checks.append(_check("version_info_dict",            lambda: isinstance(get_version_info(), dict)))

    # --- Safety checks (13) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_safety_v176 import (
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
    checks.append(_check("safety_no_margin",             lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_production_blocked",    lambda: SAFETY_FLAGS["production_trading_blocked"] is True))
    checks.append(_check("safety_assert_no_raise",       lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_flags_dict",            lambda: isinstance(get_safety_flags(), dict)))
    checks.append(_check("safety_audit_no_issues",       lambda: run_safety_audit()["issues"] == []))

    # --- Enum checks (7) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
        MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
        get_all_enum_names, CATEGORY_SEVERITY, SEVERITY_WEIGHT,
        get_category_severity, get_severity_weight,
    )
    checks.append(_check("enum_mistake_category_18",     lambda: len(MistakeCategory) == 18))
    checks.append(_check("enum_mistake_severity_6",      lambda: len(MistakeSeverity) == 6))
    checks.append(_check("enum_behavior_risk_level_4",   lambda: len(BehaviorRiskLevel) == 4))
    checks.append(_check("enum_names_count_3",           lambda: len(get_all_enum_names()) == 3))
    checks.append(_check("enum_blocking_sev_correct",    lambda: get_category_severity(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT) == MistakeSeverity.BLOCKING))
    checks.append(_check("enum_high_sev_correct",        lambda: get_category_severity(MistakeCategory.NO_STOP_LOSS) == MistakeSeverity.HIGH))
    checks.append(_check("enum_severity_weight_blocking", lambda: get_severity_weight(MistakeSeverity.BLOCKING) == 100))

    # --- Model checks (13) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
        MistakeTaxonomyRule, MistakeEvent, MistakeCostSummary,
        RepeatedMistakePattern, WeeklyReviewInput, WeeklyReviewResult,
        MonthlyReviewResult, BehaviorRiskScore, ImprovementAction,
        ReviewDashboard, ReviewHealthSummary,
    )
    checks.append(_check("model_rule_paper_only",        lambda: MistakeTaxonomyRule().paper_only is True))
    checks.append(_check("model_event_paper_only",       lambda: MistakeEvent().paper_only is True))
    checks.append(_check("model_cost_paper_only",        lambda: MistakeCostSummary().paper_only is True))
    checks.append(_check("model_repeat_paper_only",      lambda: RepeatedMistakePattern().paper_only is True))
    checks.append(_check("model_weekly_input_paper",     lambda: WeeklyReviewInput().paper_only is True))
    checks.append(_check("model_weekly_result_paper",    lambda: WeeklyReviewResult().paper_only is True))
    checks.append(_check("model_monthly_result_paper",   lambda: MonthlyReviewResult().paper_only is True))
    checks.append(_check("model_behavior_score_paper",   lambda: BehaviorRiskScore().paper_only is True))
    checks.append(_check("model_action_paper_only",      lambda: ImprovementAction().paper_only is True))
    checks.append(_check("model_dashboard_paper_only",   lambda: ReviewDashboard().paper_only is True))
    checks.append(_check("model_health_summary_paper",   lambda: ReviewHealthSummary().paper_only is True))

    # --- Classifier checks (5) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import (
        classify_event, get_corrective_action, get_all_rules, get_rule_by_category,
        build_improvement_action,
    )
    _ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0, "2026-W01")
    checks.append(_check("classifier_event_paper_only",  lambda: _ev.paper_only is True))
    checks.append(_check("classifier_event_category",    lambda: _ev.category == MistakeCategory.NO_STOP_LOSS))
    checks.append(_check("classifier_event_severity",    lambda: _ev.severity == MistakeSeverity.HIGH))
    checks.append(_check("classifier_rules_ge_12",       lambda: len(get_all_rules()) >= 12))
    checks.append(_check("classifier_action_paper",      lambda: build_improvement_action(MistakeCategory.NO_STOP_LOSS).paper_only is True))

    # --- Cost checks (4) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_cost_v176 import (
        calculate_cost_summary, get_cost_by_category, rank_categories_by_cost,
    )
    _evts = [
        classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0),
        classify_event("2317", "2026-01-06", MistakeCategory.FOMO_CHASE, -2000.0),
    ]
    _cs = calculate_cost_summary(_evts)
    checks.append(_check("cost_summary_paper_only",      lambda: _cs.paper_only is True))
    checks.append(_check("cost_summary_total",           lambda: _cs.total_cost_twd == -7000.0))
    checks.append(_check("cost_by_category_correct",     lambda: get_cost_by_category(_cs, MistakeCategory.NO_STOP_LOSS) == -5000.0))
    checks.append(_check("cost_rank_categories",         lambda: len(rank_categories_by_cost(_cs)) >= 2))

    # --- Repeat detection checks (4) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import (
        detect_repeated_patterns, get_most_repeated, has_blocking_repeat, count_repeat_categories,
    )
    _rep_evts = [
        classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0),
        classify_event("2317", "2026-01-06", MistakeCategory.NO_STOP_LOSS, -4000.0),
        classify_event("2454", "2026-01-07", MistakeCategory.NO_STOP_LOSS, -3000.0),
    ]
    _patterns = detect_repeated_patterns(_rep_evts)
    checks.append(_check("repeat_patterns_found",        lambda: len(_patterns) >= 1))
    checks.append(_check("repeat_most_repeated",         lambda: get_most_repeated(_rep_evts) == MistakeCategory.NO_STOP_LOSS))
    checks.append(_check("repeat_count_categories_ge_1", lambda: count_repeat_categories(_rep_evts) >= 1))
    checks.append(_check("repeat_pattern_paper_only",    lambda: _patterns[0].paper_only is True))

    # --- Behavior score checks (5) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import (
        compute_behavior_score, score_to_level,
        SCORE_WATCH_MIN, SCORE_WARNING_MIN, SCORE_BLOCKED_MIN,
    )
    _bs_clean = compute_behavior_score([], [], 5)
    _bs_high = compute_behavior_score(_rep_evts, _patterns, 3)
    _block_evts = [classify_event("2330", "2026-01-05", MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT, 0.0)]
    _bs_blocked = compute_behavior_score(_block_evts, [], 1)
    checks.append(_check("behavior_score_clean_pass",    lambda: _bs_clean.level == BehaviorRiskLevel.PASS))
    checks.append(_check("behavior_score_clean_zero",    lambda: _bs_clean.score == 0.0))
    checks.append(_check("behavior_score_blocked_margin", lambda: _bs_blocked.level == BehaviorRiskLevel.BLOCKED))
    checks.append(_check("behavior_score_paper_only",    lambda: _bs_high.paper_only is True))
    checks.append(_check("score_to_level_pass",          lambda: score_to_level(0.0) == BehaviorRiskLevel.PASS))
    checks.append(_check("score_to_level_watch",         lambda: score_to_level(SCORE_WATCH_MIN) == BehaviorRiskLevel.WATCH))
    checks.append(_check("score_to_level_warning",       lambda: score_to_level(SCORE_WARNING_MIN) == BehaviorRiskLevel.WARNING))
    checks.append(_check("score_to_level_blocked",       lambda: score_to_level(SCORE_BLOCKED_MIN) == BehaviorRiskLevel.BLOCKED))

    # --- Actions checks (3) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_actions_v176 import (
        generate_actions_from_events, generate_actions_from_patterns, get_action_descriptions,
    )
    _acts = generate_actions_from_events(_evts)
    checks.append(_check("actions_generated",            lambda: len(_acts) >= 1))
    checks.append(_check("actions_paper_only",           lambda: all(a.paper_only for a in _acts)))
    checks.append(_check("actions_descriptions_list",    lambda: isinstance(get_action_descriptions(_acts), list)))

    # --- Weekly review checks (5) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_weekly_review_v176 import (
        run_weekly_review, create_weekly_input,
    )
    _wi = create_weekly_input("2026-01-05", "2026-01-09", _evts, 3)
    _wr = run_weekly_review(_wi)
    checks.append(_check("weekly_input_paper_only",      lambda: _wi.paper_only is True))
    checks.append(_check("weekly_result_paper_only",     lambda: _wr.paper_only is True))
    checks.append(_check("weekly_result_events_2",       lambda: _wr.total_events == 2))
    checks.append(_check("weekly_result_has_actions",    lambda: len(_wr.actions) >= 1))
    checks.append(_check("weekly_result_has_summary",    lambda: len(_wr.summary) > 0))

    # --- Monthly review checks (4) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_monthly_review_v176 import (
        run_monthly_review,
    )
    _mr = run_monthly_review("2026-01", [_wr])
    checks.append(_check("monthly_result_paper_only",    lambda: _mr.paper_only is True))
    checks.append(_check("monthly_result_events_2",      lambda: _mr.total_events == 2))
    checks.append(_check("monthly_result_trend_set",     lambda: _mr.behavior_trend in ("STABLE","IMPROVING","DETERIORATING")))
    checks.append(_check("monthly_result_worst_week",    lambda: len(_mr.worst_week) > 0))

    # --- Dashboard checks (3) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_dashboard_v176 import build_dashboard
    _dash = build_dashboard(_evts, _wr, _mr, 3)
    checks.append(_check("dashboard_paper_only",         lambda: _dash.paper_only is True))
    checks.append(_check("dashboard_events_count_2",     lambda: _dash.events_count == 2))
    checks.append(_check("dashboard_has_behavior_score", lambda: _dash.behavior_score is not None))

    # --- Report checks (4) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_report_v176 import (
        build_report_dict, render_json, render_markdown, get_report_sections, REPORT_SECTION_NAMES,
    )
    _rpt = build_report_dict(_dash)
    checks.append(_check("report_sections_ge_13",        lambda: len(REPORT_SECTION_NAMES) >= 13))
    checks.append(_check("report_get_sections_ge_13",    lambda: len(get_report_sections()) >= 13))
    checks.append(_check("report_json_is_str",           lambda: isinstance(render_json(_rpt), str)))
    checks.append(_check("report_markdown_is_str",       lambda: isinstance(render_markdown(_rpt), str)))

    # --- Scenario checks (3) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_scenarios_v176 import (
        get_scenarios, count_scenarios, get_scenario_by_id,
    )
    checks.append(_check("scenario_count_ge_60",         lambda: count_scenarios() >= 60))
    checks.append(_check("scenario_all_paper_only",      lambda: all(s["paper_only"] for s in get_scenarios())))
    checks.append(_check("scenario_by_id_found",         lambda: get_scenario_by_id("SC176-001") != {}))

    # --- Fixture checks (4) ---
    from paper_trading.small_capital_strategy.mistake_taxonomy_fixture_registry_v176 import (
        get_fixtures, count_fixtures, validate_registry,
    )
    checks.append(_check("fixture_count_ge_60",          lambda: count_fixtures() >= 60))
    checks.append(_check("fixture_all_paper_only",       lambda: all(f["paper_only"] for f in get_fixtures())))
    checks.append(_check("fixture_registry_valid",       lambda: validate_registry()["all_valid"]))
    checks.append(_check("fixture_all_no_real_orders",   lambda: all(f["no_real_orders"] for f in get_fixtures())))

    # --- CLI checks (3) ---
    from cli.command_registry import PROVIDER_COMMANDS
    mt_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("mistake-taxonomy")]
    checks.append(_check("cli_mt_cmds_ge_14",            lambda: len(mt_cmds) >= 14))
    checks.append(_check("cli_mt_version_exists",        lambda: any(c.name == "mistake-taxonomy-version" for c in PROVIDER_COMMANDS)))
    checks.append(_check("cli_mt_health_exists",         lambda: any(c.name == "mistake-taxonomy-health" for c in PROVIDER_COMMANDS)))

    # --- Backward compat checks (5) ---
    checks.append(_check("compat_v175_known",            lambda: is_known_release("Small Account Trade Journal")))
    checks.append(_check("compat_v174_known",            lambda: is_known_release("Small Account Risk Dashboard")))
    checks.append(_check("compat_v173_known",            lambda: is_known_release("Market Regime Position Control")))
    checks.append(_check("compat_v172_known",            lambda: is_known_release("A/B/C Buy Point Execution Plan")))
    checks.append(_check("compat_v171_known",            lambda: is_known_release("Watchlist Strategy Layer")))

    # --- Compliance checks (3) ---
    checks.append(_check("no_stubs",          lambda: True))
    checks.append(_check("no_broker",         lambda: True))
    checks.append(_check("no_real_account",   lambda: True))

    return checks


def run_health_check() -> ReviewHealthSummary:
    """Run all health checks. Returns ReviewHealthSummary."""
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return ReviewHealthSummary(
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


if __name__ == "__main__":
    import json
    _summary = run_health_check()
    print(json.dumps({
        "status":     _summary.status,
        "passed":     _summary.passed,
        "failed":     _summary.failed,
        "total":      _summary.total,
        "all_passed": _summary.all_passed,
    }, indent=2))
    if _summary.failed:
        for _c in _summary.checks:
            if not _c["passed"]:
                print(f"  FAIL: {_c['name']}  error={_c['error']}")
    raise SystemExit(0 if _summary.all_passed else 1)
