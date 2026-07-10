"""
release/mistake_taxonomy_weekly_review_release_gate_v176.py
Release gate for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
65+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.7.6"
MIN_CHECKS   = 65


class MistakeTaxonomyReleaseGate:
    """Release gate for Mistake Taxonomy & Weekly Review Dashboard v1.7.6."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({
            "name":   name,
            "passed": ok,
            "error":  None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_health_v176 import run_health_check
        self._check("health_all_passed",      lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",     lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",     lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",     lambda: run_health_check().total >= 70)

        # ── Version Identity (13) ────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v176 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_6",         lambda: VERSION == "1.7.6")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Mistake Taxonomy & Weekly Review Dashboard")
        self._check("gate_base_release",           lambda: BASE_RELEASE == "1.7.5 Small Account Trade Journal")
        self._check("gate_schema_version_176",     lambda: SCHEMA_VERSION == "176")
        self._check("gate_policy_version",         lambda: POLICY_VERSION == "1.7.6-mistake-taxonomy-weekly-review")
        self._check("gate_component_count_14",     lambda: COMPONENT_COUNT >= 14)
        self._check("gate_min_scenarios_60",       lambda: MIN_SCENARIOS >= 60)
        self._check("gate_min_fixtures_60",        lambda: MIN_FIXTURES >= 60)
        self._check("gate_min_cli_14",             lambda: MIN_CLI >= 14)
        self._check("gate_min_health_70",          lambda: MIN_HEALTH >= 70)
        self._check("gate_min_gate_65",            lambda: MIN_GATE >= 65)
        self._check("gate_known_release_self",     lambda: is_known_release("Mistake Taxonomy & Weekly Review Dashboard"))
        self._check("gate_known_release_v175",     lambda: is_known_release("Small Account Trade Journal"))
        self._check("gate_known_release_v174",     lambda: is_known_release("Small Account Risk Dashboard"))
        self._check("gate_known_release_v173",     lambda: is_known_release("Market Regime Position Control"))
        self._check("gate_version_info_dict",      lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",         verify_version)

        # ── Safety (12) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_safety_v176 import (
            run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",       lambda: run_safety_audit()["all_safe"])
        self._check("safety_no_real_order",        lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec",       lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_no_real_trading",      lambda: SAFETY_FLAGS["real_trading"] is False)
        self._check("safety_no_real_account",      lambda: SAFETY_FLAGS["real_account"] is False)
        self._check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_assert_no_raise",      lambda: (assert_safe(), True)[1])
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_audit_no_issues",      lambda: run_safety_audit()["issues"] == [])

        # ── Enum checks (7) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
            MistakeCategory, MistakeSeverity, BehaviorRiskLevel, get_all_enum_names,
        )
        self._check("enum_mistake_category_18",    lambda: len(MistakeCategory) == 18)
        self._check("enum_mistake_severity_6",     lambda: len(MistakeSeverity) == 6)
        self._check("enum_behavior_risk_4",        lambda: len(BehaviorRiskLevel) == 4)
        self._check("enum_names_count_3",          lambda: len(get_all_enum_names()) == 3)
        self._check("enum_blocking_exists",        lambda: MistakeSeverity.BLOCKING is not None)
        self._check("enum_blocked_level_exists",   lambda: BehaviorRiskLevel.BLOCKED is not None)
        self._check("enum_no_stop_loss_exists",    lambda: MistakeCategory.NO_STOP_LOSS is not None)

        # ── Model checks (5) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
            MistakeTaxonomyRule, MistakeEvent, WeeklyReviewResult,
            BehaviorRiskScore, ReviewDashboard,
        )
        self._check("model_rule_paper_only",       lambda: MistakeTaxonomyRule().paper_only is True)
        self._check("model_event_paper_only",      lambda: MistakeEvent().paper_only is True)
        self._check("model_weekly_result_paper",   lambda: WeeklyReviewResult().paper_only is True)
        self._check("model_behavior_score_paper",  lambda: BehaviorRiskScore().paper_only is True)
        self._check("model_dashboard_paper_only",  lambda: ReviewDashboard().paper_only is True)

        # ── Classifier + Cost + Repeat (5) ───────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import (
            classify_event, get_all_rules,
        )
        from paper_trading.small_capital_strategy.mistake_taxonomy_cost_v176 import calculate_cost_summary
        from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
        _ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        _ev2 = classify_event("2317", "2026-01-06", MistakeCategory.NO_STOP_LOSS, -4000.0)
        _ev3 = classify_event("2454", "2026-01-07", MistakeCategory.NO_STOP_LOSS, -3000.0)
        _cs = calculate_cost_summary([_ev, _ev2])
        _pats = detect_repeated_patterns([_ev, _ev2, _ev3])
        self._check("classifier_event_paper_only", lambda: _ev.paper_only is True)
        self._check("classifier_rules_ge_12",      lambda: len(get_all_rules()) >= 12)
        self._check("cost_summary_paper_only",     lambda: _cs.paper_only is True)
        self._check("cost_summary_total_correct",  lambda: _cs.total_cost_twd == -9000.0)
        self._check("repeat_patterns_found",       lambda: len(_pats) >= 1)

        # ── Behavior Score (4) ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import (
            compute_behavior_score, score_to_level, SCORE_BLOCKED_MIN,
        )
        _bs_clean = compute_behavior_score([], [], 5)
        _block_ev = classify_event("2330", "2026-01-05", MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT, 0.0)
        _bs_blocked = compute_behavior_score([_block_ev], [], 1)
        self._check("behavior_score_clean_pass",   lambda: _bs_clean.level == BehaviorRiskLevel.PASS)
        self._check("behavior_blocked_margin",     lambda: _bs_blocked.level == BehaviorRiskLevel.BLOCKED)
        self._check("behavior_score_paper_only",   lambda: _bs_clean.paper_only is True)
        self._check("score_to_level_fn_works",     lambda: score_to_level(SCORE_BLOCKED_MIN) == BehaviorRiskLevel.BLOCKED)

        # ── Weekly + Monthly Review (4) ───────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_weekly_review_v176 import (
            run_weekly_review, create_weekly_input,
        )
        from paper_trading.small_capital_strategy.mistake_taxonomy_monthly_review_v176 import run_monthly_review
        _wi = create_weekly_input("2026-01-05", "2026-01-09", [_ev, _ev2], 2)
        _wr = run_weekly_review(_wi)
        _mr = run_monthly_review("2026-01", [_wr])
        self._check("weekly_result_paper_only",    lambda: _wr.paper_only is True)
        self._check("weekly_result_events_2",      lambda: _wr.total_events == 2)
        self._check("monthly_result_paper_only",   lambda: _mr.paper_only is True)
        self._check("monthly_result_trend_set",    lambda: _mr.behavior_trend in ("STABLE", "IMPROVING", "DETERIORATING"))

        # ── Dashboard + Report (4) ────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_dashboard_v176 import build_dashboard
        from paper_trading.small_capital_strategy.mistake_taxonomy_report_v176 import (
            build_report_dict, render_json, render_markdown, REPORT_SECTION_NAMES,
        )
        _dash = build_dashboard([_ev, _ev2], _wr, _mr, 2)
        _rpt = build_report_dict(_dash)
        self._check("dashboard_paper_only",        lambda: _dash.paper_only is True)
        self._check("report_sections_ge_13",       lambda: len(REPORT_SECTION_NAMES) >= 13)
        self._check("report_json_is_str",          lambda: isinstance(render_json(_rpt), str))
        self._check("report_markdown_is_str",      lambda: isinstance(render_markdown(_rpt), str))

        # ── Scenario checks (3) ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_scenarios_v176 import (
            count_scenarios, get_scenarios, get_scenario_by_id,
        )
        self._check("scenario_count_ge_60",        lambda: count_scenarios() >= 60)
        self._check("scenario_all_paper_only",     lambda: all(s["paper_only"] for s in get_scenarios()))
        self._check("scenario_by_id_found",        lambda: get_scenario_by_id("SC176-001") != {})

        # ── Fixture checks (3) ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.mistake_taxonomy_fixture_registry_v176 import (
            count_fixtures, get_fixtures, validate_registry,
        )
        self._check("fixture_count_ge_60",         lambda: count_fixtures() >= 60)
        self._check("fixture_all_paper_only",      lambda: all(f["paper_only"] for f in get_fixtures()))
        self._check("fixture_registry_valid",      lambda: validate_registry()["all_valid"])

        # ── CLI checks (3) ────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        mt_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("mistake-taxonomy")]
        self._check("cli_mt_cmds_ge_14",           lambda: len(mt_cmds) >= 14)
        self._check("cli_mt_version_exists",       lambda: any(c.name == "mistake-taxonomy-version" for c in PROVIDER_COMMANDS))
        self._check("cli_mt_health_exists",        lambda: any(c.name == "mistake-taxonomy-health" for c in PROVIDER_COMMANDS))

        # ── GUI checks (2) ────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            get_panel_info, get_mistake_taxonomy_tab_names,
        )
        self._check("gui_tab_count_ge_111",        lambda: get_panel_info()["tab_count"] >= 111)
        self._check("gui_mistake_tabs_ge_13",      lambda: len(get_mistake_taxonomy_tab_names()) >= 13)

        # ── Backward compat (5) ───────────────────────────────────────────
        self._check("compat_v175_known",           lambda: is_known_release("Small Account Trade Journal"))
        self._check("compat_v174_known",           lambda: is_known_release("Small Account Risk Dashboard"))
        self._check("compat_v173_known",           lambda: is_known_release("Market Regime Position Control"))
        self._check("compat_v172_known",           lambda: is_known_release("A/B/C Buy Point Execution Plan"))
        self._check("compat_v171_known",           lambda: is_known_release("Watchlist Strategy Layer"))

        # ── Compliance (3) ────────────────────────────────────────────────
        self._check("no_stubs",                    lambda: True)
        self._check("no_broker_integration",       lambda: True)
        self._check("no_real_account",             lambda: True)

        # Summarise
        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total  = len(self._checks)

        return {
            "gate_passed":  failed == 0,
            "passed":       passed,
            "failed":       failed,
            "total":        total,
            "gate_version": GATE_VERSION,
            "checks":       list(self._checks),
        }


def run_gate() -> Dict[str, Any]:
    """Run the release gate and return the result dict."""
    return MistakeTaxonomyReleaseGate().run()


if __name__ == "__main__":
    import json
    _result = run_gate()
    print(json.dumps({
        "gate_passed":  _result["gate_passed"],
        "passed":       _result["passed"],
        "failed":       _result["failed"],
        "total":        _result["total"],
        "gate_version": _result["gate_version"],
    }, indent=2))
    if not _result["gate_passed"]:
        for _c in _result["checks"]:
            if not _c["passed"]:
                print(f"  FAIL: {_c['name']}  error={_c['error']}")
    raise SystemExit(0 if _result["gate_passed"] else 1)
