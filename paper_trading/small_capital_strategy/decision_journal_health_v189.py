"""
paper_trading/small_capital_strategy/decision_journal_health_v189.py
Health check for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class DecisionJournalHealthCheck:
    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({"name": name, "passed": ok, "error": None if ok else str(result)})

    def run(self) -> "JournalHealthSummary":
        from paper_trading.small_capital_strategy.decision_journal_models_v189 import JournalHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_version_v189 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_journal_entry_states, get_review_dimensions,
            get_mistake_tags, get_quality_grades, get_allowed_journal_actions,
            get_forbidden_journal_actions, get_hard_block_conditions,
        )
        self._check("version_is_189", lambda: VERSION == "1.8.9")
        self._check("release_name_correct", lambda: RELEASE_NAME == "Paper Decision Journal & Review Loop")
        self._check("schema_version_189", lambda: SCHEMA_VERSION == "189")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v189", lambda: is_known_release("Paper Decision Journal & Review Loop v1.8.9"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_safety_v189 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_journal_action, FORBIDDEN_JOURNAL_ACTIONS,
            ALLOWED_JOURNAL_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_not_investment_advice", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_production_trading_blocked", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_flag_journal_only", lambda: SAFETY_FLAGS["journal_only"] is True)
        self._check("safety_flag_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)

        # ── journal entry states (3) ──────────────────────────────────────────
        self._check("journal_entry_states_16", lambda: len(get_journal_entry_states()) == 16)
        self._check("journal_states_contains_observe", lambda: "OBSERVE" in get_journal_entry_states())
        self._check("journal_states_contains_paper_plan_ready", lambda: "PAPER_PLAN_READY" in get_journal_entry_states())

        # ── review dimensions (3) ─────────────────────────────────────────────
        self._check("review_dimensions_20", lambda: len(get_review_dimensions()) == 20)
        self._check("review_dimensions_has_market_regime", lambda: "market_regime_alignment" in get_review_dimensions())
        self._check("review_dimensions_has_audit_traceability", lambda: "audit_traceability" in get_review_dimensions())

        # ── mistake tags (3) ──────────────────────────────────────────────────
        self._check("mistake_tags_18", lambda: len(get_mistake_tags()) == 18)
        self._check("mistake_tags_has_chase_high", lambda: "CHASE_HIGH" in get_mistake_tags())
        self._check("mistake_tags_has_no_mistake_found", lambda: "NO_MISTAKE_FOUND" in get_mistake_tags())

        # ── quality grades (3) ────────────────────────────────────────────────
        self._check("quality_grades_6", lambda: len(get_quality_grades()) == 6)
        self._check("quality_grades_has_excellent", lambda: "EXCELLENT" in get_quality_grades())
        self._check("quality_grades_has_invalid", lambda: "INVALID" in get_quality_grades())

        # ── models (22) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
            DecisionJournalEntry, DecisionJournalBook, DecisionReviewInput, DecisionReviewResult,
            DecisionOutcomeSnapshot, PaperDecisionLifecycle, PaperDecisionEvidenceLink,
            DecisionMistakeTag, DecisionQualityScore, DailyReviewSummary, WeeklyReviewSummary,
            MonthlyReviewSummary, ReviewChecklist, ReviewFinding, ReviewActionItem,
            ReviewBlockReason, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
            JournalHealthSummary as _JHS, JournalDashboard, JournalValidationResult,
            get_all_model_names,
        )
        self._check("model_count_22", lambda: len(get_all_model_names()) == 22)
        self._check("model_DecisionJournalEntry_paper_only", lambda: DecisionJournalEntry().paper_only is True)
        self._check("model_DecisionJournalBook_paper_only", lambda: DecisionJournalBook().paper_only is True)
        self._check("model_DecisionReviewInput_paper_only", lambda: DecisionReviewInput().paper_only is True)
        self._check("model_DecisionReviewResult_paper_only", lambda: DecisionReviewResult().paper_only is True)
        self._check("model_DecisionOutcomeSnapshot_paper_only", lambda: DecisionOutcomeSnapshot().paper_only is True)
        self._check("model_PaperDecisionLifecycle_paper_only", lambda: PaperDecisionLifecycle().paper_only is True)
        self._check("model_PaperDecisionEvidenceLink_paper_only", lambda: PaperDecisionEvidenceLink().paper_only is True)
        self._check("model_DecisionMistakeTag_paper_only", lambda: DecisionMistakeTag().paper_only is True)
        self._check("model_DecisionQualityScore_paper_only", lambda: DecisionQualityScore().paper_only is True)
        self._check("model_DailyReviewSummary_paper_only", lambda: DailyReviewSummary().paper_only is True)
        self._check("model_WeeklyReviewSummary_paper_only", lambda: WeeklyReviewSummary().paper_only is True)
        self._check("model_MonthlyReviewSummary_paper_only", lambda: MonthlyReviewSummary().paper_only is True)
        self._check("model_ReviewChecklist_paper_only", lambda: ReviewChecklist().paper_only is True)
        self._check("model_ReviewFinding_paper_only", lambda: ReviewFinding().paper_only is True)
        self._check("model_ReviewActionItem_paper_only", lambda: ReviewActionItem().paper_only is True)
        self._check("model_ReviewBlockReason_paper_only", lambda: ReviewBlockReason().paper_only is True)
        self._check("model_JournalExportManifest_paper_only", lambda: JournalExportManifest().paper_only is True)
        self._check("model_JournalEvidencePack_paper_only", lambda: JournalEvidencePack().paper_only is True)
        self._check("model_JournalAuditTrail_paper_only", lambda: JournalAuditTrail().paper_only is True)
        self._check("model_JournalHealthSummary_paper_only", lambda: _JHS().paper_only is True)
        self._check("model_JournalDashboard_paper_only", lambda: JournalDashboard().paper_only is True)
        self._check("model_JournalValidationResult_paper_only", lambda: JournalValidationResult().paper_only is True)

        # ── engine (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_engine_v189 import (
            validate_journal_action as eng_val_action,
            validate_journal_state, validate_quality_grade, validate_mistake_tag,
            validate_review_dimension, create_journal_entry, validate_journal_entry,
            create_journal_book, run_review, build_daily_review, build_weekly_review,
            build_monthly_review, build_quality_score, build_audit_trail,
            build_evidence_pack, build_export_manifest, build_dashboard,
            build_review_checklist, get_engine_info,
        )
        self._check("engine_validate_action_wait", lambda: eng_val_action("WAIT") is True)
        self._check("engine_validate_action_buy_false", lambda: eng_val_action("BUY") is False)
        self._check("engine_validate_state_observe", lambda: validate_journal_state("OBSERVE") is True)
        self._check("engine_validate_state_invalid_false", lambda: validate_journal_state("INVALID_STATE") is False)
        self._check("engine_validate_grade_excellent", lambda: validate_quality_grade("EXCELLENT") is True)
        self._check("engine_validate_mistake_tag", lambda: validate_mistake_tag("CHASE_HIGH") is True)
        self._check("engine_validate_review_dimension", lambda: validate_review_dimension("market_regime_alignment") is True)
        _entry = create_journal_entry(entry_id="HC-001", date_label="2026-W01-D1", state="OBSERVE",
                                      symbol="TSMC", rationale="Health check entry", workflow_id="WF-HC-001")
        self._check("engine_create_entry_paper_only", lambda: _entry.paper_only is True)
        self._check("engine_validate_entry_valid", lambda: validate_journal_entry(_entry).is_valid is True)
        _book = create_journal_book(book_id="BK-HC", period_label="2026-W01", entries=[_entry])
        self._check("engine_create_book_paper_only", lambda: _book.paper_only is True)

        # ── review engine (5) ─────────────────────────────────────────────────
        _rev_input = DecisionReviewInput(
            review_type="daily_review", date_label="2026-W01-D1",
            source_workflow_id="WF-HC-001", journal_book=_book,
        )
        _rev_result = run_review(_rev_input)
        self._check("engine_run_review_paper_only", lambda: _rev_result.paper_only is True)
        self._check("engine_run_review_not_blocked", lambda: _rev_result.blocked is False)
        _daily = build_daily_review(_rev_input)
        self._check("engine_build_daily_review_paper_only", lambda: _daily.paper_only is True)
        _weekly = build_weekly_review([_daily])
        self._check("engine_build_weekly_review_paper_only", lambda: _weekly.paper_only is True)
        _monthly = build_monthly_review([_weekly], month_label="2026-01")
        self._check("engine_build_monthly_review_paper_only", lambda: _monthly.paper_only is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_report_v189 import (
            export_daily_review_as_json, export_weekly_review_as_json,
            export_weekly_review_as_markdown, export_dashboard_as_json,
            export_manifest_as_json, export_console_summary, get_report_info,
        )
        self._check("report_daily_review_json_is_str", lambda: isinstance(export_daily_review_as_json(_daily), str))
        self._check("report_weekly_review_json_is_str", lambda: isinstance(export_weekly_review_as_json(_weekly), str))
        self._check("report_weekly_markdown_is_str", lambda: isinstance(export_weekly_review_as_markdown(_weekly), str))
        _dash = build_dashboard("2026-W01", _book, _weekly)
        self._check("report_dashboard_json_is_str", lambda: isinstance(export_dashboard_as_json(_dash), str))
        self._check("report_info_paper_only", lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_scenarios_v189 import (
            count_scenarios, get_scenarios, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: count_scenarios() == 75)
        self._check("scenarios_get_75", lambda: len(get_scenarios()) == 75)
        self._check("scenarios_get_by_id_dj189_001", lambda: get_scenario_by_id("DJ189-001") is not None)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_fixtures_v189 import (
            get_fixture_count, get_fixture_dir, get_fixture_info,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_dir_is_str", lambda: isinstance(get_fixture_dir(), str))
        self._check("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)

        # ── safety extras (3) ─────────────────────────────────────────────────
        self._check("safety_safe_path_reports", lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_path_prod_db", lambda: is_safe_output_path("production_db") is False)
        self._check("safety_forbidden_action_sell", lambda: is_forbidden_action("SELL") is True)

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_count_18", lambda: len(get_hard_block_conditions()) == 18)
        self._check("hard_block_has_real_order", lambda: "real_order_requested" in get_hard_block_conditions())
        self._check("hard_block_has_unsafe_export", lambda: "unsafe_export_path" in get_hard_block_conditions())

        # ── allowed/forbidden actions (4) ─────────────────────────────────────
        self._check("allowed_actions_16", lambda: len(get_allowed_journal_actions()) == 16)
        self._check("forbidden_actions_9", lambda: len(get_forbidden_journal_actions()) == 9)
        self._check("allowed_contains_audit_only", lambda: "AUDIT_ONLY" in get_allowed_journal_actions())
        self._check("forbidden_contains_broker_order", lambda: "BROKER_ORDER" in get_forbidden_journal_actions())

        total = len(self._checks)
        passed = sum(1 for c in self._checks if c["passed"])
        failed = total - passed
        return JournalHealthSummary(
            total=total, passed=passed, failed=failed,
            all_passed=(failed == 0), status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "JournalHealthSummary":
    return DecisionJournalHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Decision Journal Health v1.8.9: {result.status} ({result.passed}/{result.total})")
    if not result.all_passed:
        import sys; sys.exit(1)
