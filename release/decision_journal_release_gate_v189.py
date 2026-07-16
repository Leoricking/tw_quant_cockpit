"""
release/decision_journal_release_gate_v189.py
Release gate for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class DecisionJournalReleaseGate:
    VERSION = "1.8.9"
    RELEASE_NAME = "Paper Decision Journal & Review Loop"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 25641
    MIN_NEW_TESTS = 400

    def __init__(self) -> None:
        self._results: List[Dict[str, Any]] = []

    def _gate(self, name: str, fn) -> None:
        try:
            result = fn()
            passed = bool(result)
        except Exception as exc:
            passed = False
            result = str(exc)
        self._results.append({"name": name, "passed": passed, "error": None if passed else str(result)})

    def run(self) -> Dict[str, Any]:
        self._results = []

        # ── version ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_version_v189 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_journal_entry_states, get_review_dimensions, get_mistake_tags,
            get_quality_grades, get_allowed_journal_actions, get_forbidden_journal_actions,
            get_hard_block_conditions,
        )
        self._gate("version_189", lambda: VERSION == "1.8.9")
        self._gate("release_name_journal_review_loop", lambda: RELEASE_NAME == "Paper Decision Journal & Review Loop")
        self._gate("schema_189", lambda: SCHEMA_VERSION == "189")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("journal_entry_states_16", lambda: len(get_journal_entry_states()) == 16)
        self._gate("review_dimensions_20", lambda: len(get_review_dimensions()) == 20)
        self._gate("mistake_tags_18", lambda: len(get_mistake_tags()) == 18)
        self._gate("quality_grades_6", lambda: len(get_quality_grades()) == 6)
        self._gate("allowed_actions_16", lambda: len(get_allowed_journal_actions()) == 16)
        self._gate("forbidden_actions_9", lambda: len(get_forbidden_journal_actions()) == 9)
        self._gate("hard_block_conditions_18", lambda: len(get_hard_block_conditions()) == 18)
        self._gate("forbidden_actions_no_buy", lambda: "BUY" in get_forbidden_journal_actions())
        self._gate("forbidden_actions_no_broker_order", lambda: "BROKER_ORDER" in get_forbidden_journal_actions())

        # ── safety ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_safety_v189 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, validate_journal_entry_safe,
        )
        self._gate("safety_audit_pass", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only_true", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders_true", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker_true", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_not_investment_advice_true", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_production_trading_blocked_true", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._gate("safety_journal_only_true", lambda: SAFETY_FLAGS["journal_only"] is True)
        self._gate("safety_review_only_true", lambda: SAFETY_FLAGS["review_only"] is True)
        self._gate("safety_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._gate("safety_buy_forbidden", lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_sell_forbidden", lambda: is_forbidden_action("SELL") is True)
        self._gate("safety_wait_allowed", lambda: is_allowed_action("WAIT") is True)
        self._gate("safety_audit_only_allowed", lambda: is_allowed_action("AUDIT_ONLY") is True)
        self._gate("safety_safe_path_reports", lambda: is_safe_output_path("reports/") is True)
        self._gate("safety_unsafe_path_prod_db", lambda: is_safe_output_path("production_db") is False)

        # ── models ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
            DecisionJournalEntry, DecisionJournalBook, DecisionReviewInput, DecisionReviewResult,
            DecisionOutcomeSnapshot, PaperDecisionLifecycle, PaperDecisionEvidenceLink,
            DecisionMistakeTag, DecisionQualityScore, DailyReviewSummary, WeeklyReviewSummary,
            MonthlyReviewSummary, ReviewChecklist, ReviewFinding, ReviewActionItem,
            ReviewBlockReason, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
            JournalHealthSummary, JournalDashboard, JournalValidationResult, get_all_model_names,
        )
        self._gate("model_count_22", lambda: len(get_all_model_names()) == 22)
        self._gate("model_journal_entry_paper_only", lambda: DecisionJournalEntry().paper_only is True)
        self._gate("model_journal_entry_journal_only", lambda: DecisionJournalEntry().journal_only is True)
        self._gate("model_journal_book_paper_only", lambda: DecisionJournalBook().paper_only is True)
        self._gate("model_review_input_paper_only", lambda: DecisionReviewInput().paper_only is True)
        self._gate("model_review_result_paper_only", lambda: DecisionReviewResult().paper_only is True)
        self._gate("model_outcome_snapshot_paper_only", lambda: DecisionOutcomeSnapshot().paper_only is True)
        self._gate("model_lifecycle_paper_only", lambda: PaperDecisionLifecycle().paper_only is True)
        self._gate("model_evidence_link_paper_only", lambda: PaperDecisionEvidenceLink().paper_only is True)
        self._gate("model_mistake_tag_paper_only", lambda: DecisionMistakeTag().paper_only is True)
        self._gate("model_quality_score_paper_only", lambda: DecisionQualityScore().paper_only is True)
        self._gate("model_daily_review_paper_only", lambda: DailyReviewSummary().paper_only is True)
        self._gate("model_weekly_review_paper_only", lambda: WeeklyReviewSummary().paper_only is True)
        self._gate("model_monthly_review_paper_only", lambda: MonthlyReviewSummary().paper_only is True)
        self._gate("model_checklist_paper_only", lambda: ReviewChecklist().paper_only is True)
        self._gate("model_finding_paper_only", lambda: ReviewFinding().paper_only is True)
        self._gate("model_action_item_paper_only", lambda: ReviewActionItem().paper_only is True)
        self._gate("model_block_reason_paper_only", lambda: ReviewBlockReason().paper_only is True)
        self._gate("model_export_manifest_paper_only", lambda: JournalExportManifest().paper_only is True)
        self._gate("model_evidence_pack_paper_only", lambda: JournalEvidencePack().paper_only is True)
        self._gate("model_audit_trail_paper_only", lambda: JournalAuditTrail().paper_only is True)
        self._gate("model_health_summary_paper_only", lambda: JournalHealthSummary().paper_only is True)
        self._gate("model_dashboard_paper_only", lambda: JournalDashboard().paper_only is True)
        self._gate("model_validation_result_paper_only", lambda: JournalValidationResult().paper_only is True)

        # ── engine ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_engine_v189 import (
            validate_journal_action, validate_journal_state, validate_quality_grade,
            create_journal_entry, validate_journal_entry, create_journal_book,
            run_review, build_daily_review, build_weekly_review, build_monthly_review,
            build_quality_score, build_audit_trail, build_evidence_pack,
            build_export_manifest, build_dashboard, build_review_checklist,
            get_engine_info,
        )
        self._gate("engine_validate_action_wait", lambda: validate_journal_action("WAIT") is True)
        self._gate("engine_validate_action_buy_false", lambda: validate_journal_action("BUY") is False)
        self._gate("engine_validate_state_observe", lambda: validate_journal_state("OBSERVE") is True)
        self._gate("engine_validate_grade_excellent", lambda: validate_quality_grade("EXCELLENT") is True)
        _e = create_journal_entry("RG-001", "2026-W01-D1", "OBSERVE", "TSMC", "test", ["ev1"], "WF-001")
        self._gate("engine_create_entry_paper_only", lambda: _e.paper_only is True)
        self._gate("engine_validate_entry_valid", lambda: validate_journal_entry(_e).is_valid is True)
        _bk = create_journal_book("BK-RG", "2026-W01", [_e])
        self._gate("engine_create_book_paper_only", lambda: _bk.paper_only is True)
        _ri = DecisionReviewInput(review_type="daily_review", date_label="2026-W01-D1",
                                  source_workflow_id="WF-001", journal_book=_bk)
        _rr = run_review(_ri)
        self._gate("engine_run_review_paper_only", lambda: _rr.paper_only is True)
        self._gate("engine_run_review_not_blocked", lambda: _rr.blocked is False)
        _dr = build_daily_review(_ri)
        self._gate("engine_daily_review_paper_only", lambda: _dr.paper_only is True)
        _wr = build_weekly_review([_dr])
        self._gate("engine_weekly_review_paper_only", lambda: _wr.paper_only is True)
        _mr = build_monthly_review([_wr], "2026-01")
        self._gate("engine_monthly_review_paper_only", lambda: _mr.paper_only is True)
        _qs = build_quality_score(_e, _ri)
        self._gate("engine_quality_score_paper_only", lambda: _qs.paper_only is True)
        _at = build_audit_trail("2026-W01", [_e], [_rr])
        self._gate("engine_audit_trail_paper_only", lambda: _at.paper_only is True)
        _ep = build_evidence_pack("2026-W01", [_e], ["WF-001"])
        self._gate("engine_evidence_pack_paper_only", lambda: _ep.paper_only is True)
        _em = build_export_manifest("2026-W01", "reports/journal/", [_e], 1, 1, 1)
        self._gate("engine_export_manifest_paper_only", lambda: _em.paper_only is True)
        _db = build_dashboard("2026-W01", _bk, _wr)
        self._gate("engine_dashboard_paper_only", lambda: _db.paper_only is True)
        _cl = build_review_checklist(_ri)
        self._gate("engine_checklist_paper_only", lambda: _cl.paper_only is True)

        # ── report ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_report_v189 import (
            export_daily_review_as_json, export_weekly_review_as_json,
            export_weekly_review_as_markdown, export_dashboard_as_json,
            export_manifest_as_json, export_audit_trail_as_json,
            export_evidence_pack_as_json, export_console_summary, get_report_info,
        )
        self._gate("report_daily_json_is_str", lambda: isinstance(export_daily_review_as_json(_dr), str))
        self._gate("report_weekly_json_is_str", lambda: isinstance(export_weekly_review_as_json(_wr), str))
        self._gate("report_weekly_markdown_is_str", lambda: isinstance(export_weekly_review_as_markdown(_wr), str))
        self._gate("report_dashboard_json_is_str", lambda: isinstance(export_dashboard_as_json(_db), str))
        self._gate("report_manifest_json_is_str", lambda: isinstance(export_manifest_as_json(_em), str))
        self._gate("report_audit_trail_json_is_str", lambda: isinstance(export_audit_trail_as_json(_at), str))
        self._gate("report_evidence_pack_json_is_str", lambda: isinstance(export_evidence_pack_as_json(_ep), str))
        self._gate("report_console_summary_is_str", lambda: isinstance(export_console_summary(_dr), str))
        self._gate("report_info_paper_only", lambda: get_report_info()["paper_only"] is True)

        # ── scenarios ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_scenarios_v189 import (
            count_scenarios, get_scenarios, get_scenario_by_id, get_scenario_info,
        )
        self._gate("scenarios_count_75", lambda: count_scenarios() == 75)
        self._gate("scenarios_get_75", lambda: len(get_scenarios()) == 75)
        self._gate("scenarios_get_by_id_dj189_001", lambda: get_scenario_by_id("DJ189-001") is not None)
        self._gate("scenarios_get_by_id_dj189_075", lambda: get_scenario_by_id("DJ189-075") is not None)
        self._gate("scenarios_info_paper_only", lambda: get_scenario_info()["paper_only"] is True)

        # ── fixtures ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_fixtures_v189 import (
            get_fixture_count, get_fixture_dir, get_fixture_info, get_fixture_by_id,
        )
        self._gate("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._gate("fixtures_dir_is_str", lambda: isinstance(get_fixture_dir(), str))
        self._gate("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)
        self._gate("fixtures_get_by_id_djf189_001", lambda: get_fixture_by_id("DJF189-001") is not None)
        self._gate("fixtures_get_by_id_djf189_075", lambda: get_fixture_by_id("DJF189-075") is not None)

        # ── health check ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_journal_health_v189 import run_health_check
        _hc = run_health_check()
        self._gate("health_check_all_passed", lambda: _hc.all_passed is True)
        self._gate("health_check_status_pass", lambda: _hc.status == "PASS")
        self._gate("health_check_min_60", lambda: _hc.total >= 60)

        # ── backward compatibility ────────────────────────────────────────────
        self._gate("backward_compat_v188_workflow_models", lambda: __import__(
            'paper_trading.small_capital_strategy.decision_workflow_models_v188',
            fromlist=['WorkflowInput']).WorkflowInput().paper_only is True)
        self._gate("backward_compat_v187_report", lambda: __import__(
            'paper_trading.small_capital_strategy.decision_workflow_safety_v188',
            fromlist=['SAFETY_FLAGS']).SAFETY_FLAGS['paper_only'] is True)

        # ── no forbidden action words in model defaults ────────────────────────
        _entry_default = DecisionJournalEntry()
        self._gate("no_forbidden_in_entry_state", lambda: _entry_default.state not in (
            "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
            "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"))
        _result_default = DecisionReviewResult()
        self._gate("no_forbidden_in_review_grade", lambda: _result_default.review_grade not in (
            "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
            "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"))

        total = len(self._results)
        passed = sum(1 for r in self._results if r["passed"])
        failed = total - passed
        return {
            "version": self.VERSION,
            "release_name": self.RELEASE_NAME,
            "total": total,
            "passed": passed,
            "failed": failed,
            "gate_passed": (failed == 0),
            "status": "PASS" if failed == 0 else "FAIL",
            "paper_only": True,
            "research_only": True,
            "journal_only": True,
            "review_only": True,
            "audit_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "min_scenarios": self.MIN_SCENARIOS,
            "min_fixtures": self.MIN_FIXTURES,
            "min_cli": self.MIN_CLI,
            "baseline_tests": self.BASELINE_TESTS,
            "min_new_tests": self.MIN_NEW_TESTS,
            "results": self._results,
        }


def run_release_gate() -> Dict[str, Any]:
    return DecisionJournalReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    status = result.get("status", "FAIL")
    passed = result.get("passed", 0)
    total = result.get("total", 0)
    print(f"Decision Journal Release Gate v1.8.9: {status} ({passed}/{total})")
    if result.get("failed", 1) > 0:
        import sys; sys.exit(1)
