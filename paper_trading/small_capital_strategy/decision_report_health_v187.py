"""
paper_trading/small_capital_strategy/decision_report_health_v187.py
Health check for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class DecisionReportHealthCheck:
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

    def run(self) -> "ReportHealthSummary":
        from paper_trading.small_capital_strategy.decision_report_models_v187 import ReportHealthSummary
        self._checks = []

        # ── version (5) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_version_v187 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_report_types, get_export_formats, get_final_report_grades,
            check_minimum_version,
        )
        self._check("version_is_187", lambda: VERSION == "1.8.7")
        self._check("release_name_correct", lambda: RELEASE_NAME == "Decision Report Export & Evidence Pack")
        self._check("schema_version_187", lambda: SCHEMA_VERSION == "187")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v187", lambda: is_known_release("Decision Report Export & Evidence Pack v1.8.7"))

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_safety_v187 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_report_action, FORBIDDEN_REPORT_ACTIONS,
            ALLOWED_REPORT_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_not_investment_advice", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_production_trading_blocked", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_flag_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._check("safety_allowed_wait", lambda: is_allowed_action("WAIT") is True)

        # ── models (22) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_models_v187 import (
            DecisionReportInput, DecisionReportResult, DailyDecisionReport, WeeklyDecisionReport,
            CandidateEvidenceItem, CandidateEvidencePack, BlockReasonEvidence, BuyPointEvidence,
            RiskEvidence, PositionSizingEvidence, PortfolioEvidence, MonteCarloEvidence,
            ThemeEvidence, MarketRegimeEvidence, WatchlistReport, BlockedCandidateReport,
            ReduceRiskReport, PaperPlanReadyReport, DecisionAuditTrail, ReportExportManifest,
            ReportValidationResult, ReportHealthSummary as _RHS, get_all_model_names,
        )
        self._check("model_DecisionReportInput_paper_only", lambda: DecisionReportInput().paper_only is True)
        self._check("model_DecisionReportResult_paper_only", lambda: DecisionReportResult().paper_only is True)
        self._check("model_DailyDecisionReport_paper_only", lambda: DailyDecisionReport().paper_only is True)
        self._check("model_WeeklyDecisionReport_paper_only", lambda: WeeklyDecisionReport().paper_only is True)
        self._check("model_CandidateEvidenceItem_paper_only", lambda: CandidateEvidenceItem().paper_only is True)
        self._check("model_CandidateEvidencePack_paper_only", lambda: CandidateEvidencePack().paper_only is True)
        self._check("model_BlockReasonEvidence_paper_only", lambda: BlockReasonEvidence().paper_only is True)
        self._check("model_BuyPointEvidence_paper_only", lambda: BuyPointEvidence().paper_only is True)
        self._check("model_RiskEvidence_paper_only", lambda: RiskEvidence().paper_only is True)
        self._check("model_PositionSizingEvidence_paper_only", lambda: PositionSizingEvidence().paper_only is True)
        self._check("model_PortfolioEvidence_paper_only", lambda: PortfolioEvidence().paper_only is True)
        self._check("model_MonteCarloEvidence_paper_only", lambda: MonteCarloEvidence().paper_only is True)
        self._check("model_ThemeEvidence_paper_only", lambda: ThemeEvidence().paper_only is True)
        self._check("model_MarketRegimeEvidence_paper_only", lambda: MarketRegimeEvidence().paper_only is True)
        self._check("model_WatchlistReport_paper_only", lambda: WatchlistReport().paper_only is True)
        self._check("model_BlockedCandidateReport_paper_only", lambda: BlockedCandidateReport().paper_only is True)
        self._check("model_ReduceRiskReport_paper_only", lambda: ReduceRiskReport().paper_only is True)
        self._check("model_PaperPlanReadyReport_paper_only", lambda: PaperPlanReadyReport().paper_only is True)
        self._check("model_DecisionAuditTrail_paper_only", lambda: DecisionAuditTrail().paper_only is True)
        self._check("model_ReportExportManifest_paper_only", lambda: ReportExportManifest().paper_only is True)
        self._check("model_ReportValidationResult_paper_only", lambda: ReportValidationResult().paper_only is True)
        self._check("model_ReportHealthSummary_paper_only", lambda: _RHS().paper_only is True)

        # ── engine (6) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_engine_v187 import (
            validate_report_action as eng_validate_action,
            validate_report_grade, validate_report_type,
            build_daily_report, build_weekly_report, run_decision_report, get_engine_info,
        )
        self._check("engine_validate_report_action_wait", lambda: eng_validate_action("WAIT") is True)
        self._check("engine_validate_report_grade_complete", lambda: validate_report_grade("COMPLETE") is True)
        self._check("engine_validate_report_type_daily", lambda: validate_report_type("daily_decision_report") is True)
        self._check("engine_build_daily_report", lambda: build_daily_report(DecisionReportInput()).report_type == "daily_decision_report")
        self._check("engine_build_weekly_report", lambda: build_weekly_report(DecisionReportInput()).report_type == "weekly_decision_report")
        self._check("engine_run_decision_report", lambda: run_decision_report(DecisionReportInput()).paper_only is True)

        # ── export (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_export_v187 import (
            export_as_json, export_as_markdown, export_as_csv_rows,
            export_as_console_summary, export_as_dashboard_payload, get_export_info,
        )
        _result = run_decision_report(DecisionReportInput())
        self._check("export_as_json_returns_str", lambda: isinstance(export_as_json(_result), str))
        self._check("export_as_markdown_returns_str", lambda: isinstance(export_as_markdown(_result), str))
        self._check("export_as_csv_rows_returns_list", lambda: isinstance(export_as_csv_rows(_result), list))
        self._check("export_as_console_summary_returns_str", lambda: isinstance(export_as_console_summary(_result), str))
        self._check("export_as_dashboard_payload_returns_dict", lambda: isinstance(export_as_dashboard_payload(_result), dict))

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_scenarios_v187 import (
            count_scenarios, get_scenarios, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: count_scenarios() == 75)
        self._check("scenarios_get_scenarios_75", lambda: len(get_scenarios()) == 75)
        self._check("scenarios_get_by_id_dr187_001", lambda: get_scenario_by_id("DR187-001") is not None)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_fixtures_v187 import (
            get_fixture_count, get_fixture_dir, get_fixture_info,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_dir_is_str", lambda: isinstance(get_fixture_dir(), str))
        self._check("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)

        # ── safety_audit (3) ──────────────────────────────────────────────────
        self._check("safety_safe_output_path_reports", lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_output_path_production_db", lambda: is_safe_output_path("production_db") is False)
        self._check("safety_forbidden_action_buy", lambda: is_forbidden_action("BUY") is True)

        # ── export_formats (3) ────────────────────────────────────────────────
        self._check("export_formats_contains_json", lambda: "json" in get_export_formats())
        self._check("report_types_contains_daily", lambda: "daily_decision_report" in get_report_types())
        self._check("final_grades_contains_complete", lambda: "COMPLETE" in get_final_report_grades())

        total = len(self._checks)
        passed = sum(1 for c in self._checks if c["passed"])
        failed = total - passed
        return ReportHealthSummary(
            total=total, passed=passed, failed=failed,
            all_passed=(failed == 0), status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "ReportHealthSummary":
    return DecisionReportHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Decision Report Health v1.8.7: {result.status} ({result.passed}/{result.total})")
    if not result.all_passed:
        import sys; sys.exit(1)
