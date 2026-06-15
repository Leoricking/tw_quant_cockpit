"""report_pack/report_collector.py — ReportCollector for TW Quant Cockpit v0.5.4.

Scans known output locations to determine status of each report type.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from report_pack.report_pack_schema import (
    ReportPackItem,
    STATUS_READY, STATUS_MISSING, STATUS_FAILED,
    STATUS_ENV_LIMITED, STATUS_NOT_GENERATED,
    REPORT_DAILY_MARKET, REPORT_AUTO_REPORT, REPORT_DATA_QUALITY,
    REPORT_PROVIDER, REPORT_STRATEGY_FILTER, REPORT_SIGNAL_QUALITY,
    REPORT_RULE_GOVERNANCE, REPORT_PORTFOLIO_JOURNAL, REPORT_RESEARCH_REVIEW,
    REPORT_RESEARCH_COACH, REPORT_RESEARCH_WORKFLOW, REPORT_RESEARCH_OS,
    REPORT_REGRESSION, REPORT_CLI_UX, REPORT_GUI_NAVIGATION,
    REPORT_NOTIFICATION, REPORT_INTRADAY_REPLAY, REPORT_EXPERIMENT,
    REPORT_RELEASE, REPORT_SAFETY, REPORT_DATA_STABILIZATION,
    REPORT_REPLAY_TRAINING, REPORT_STABLE_RELEASE_V060, REPORT_RELEASE_MANIFEST,
    REPORT_DATA_COVERAGE, REPORT_RESEARCH_INTELLIGENCE,
    REPORT_STRATEGY_MEMORY,
    REPORT_BACKTEST_COACH,
    REPORT_INTELLIGENCE_STABLE,
    REPORT_TRAINING_METRICS,
    REPORT_EVIDENCE_GRAPH,
    REPORT_STRATEGY_LAB_STABLE,
    OPTIONAL_REPORT_TYPES, ENV_LIMITED_REPORT_TYPES,
)
# v0.9.0.1 crash reversal; v1.0.0 research cockpit stable; v1.0.2 hygiene; v1.0.7 kb search
from report_pack.report_registry import (
    REPORT_CRASH_REVERSAL,
    REPORT_STRATEGY_VALIDATION,
    REPORT_RESEARCH_COCKPIT_STABLE,
    REPORT_DATA_REPORT_HYGIENE,
    REPORT_GUI_USABILITY,
    REPORT_REGRESSION_HARDENING,
    REPORT_DOCUMENTATION_HEALTH,
    REPORT_WORKFLOW_TEMPLATES,
    REPORT_KNOWLEDGE_BASE_SEARCH,
    REPORT_LOCAL_RESEARCH_ASSISTANT,
    REPORT_DATA_IMPORT_ONBOARDING,
    REPORT_COVERAGE_REPAIR,
    REPORT_DATA_FRESHNESS,
    REPORT_COVERAGE_QUALITY_GATE,
    REPORT_GATE_ENFORCEMENT_AUDIT,
    REPORT_GATE_RUN_SUMMARY,
    REPORT_GATE_EXCLUSION_SUMMARY,
    REPORT_GATE_REPRODUCIBILITY,
    REPORT_DATA_GOVERNANCE_OPERATIONS,
    REPORT_GOVERNANCE_ACTION_QUEUE,
    REPORT_GOVERNANCE_MODULE_HEALTH,
    REPORT_GOVERNANCE_AUDIT_SUMMARY,
    REPORT_GOVERNANCE_ALERTS_DAILY_OPS,
    REPORT_GOVERNANCE_MORNING_DIGEST,
    REPORT_GOVERNANCE_EOD_DIGEST,
    REPORT_GOVERNANCE_WEEKLY_DIGEST,
    REPORT_GOVERNANCE_ALERT_TREND,
    REPORT_GOVERNANCE_CHECKLIST,
    REPORT_RESEARCH_RUN_REGISTRY,
    REPORT_LATEST_RUN_SUMMARY,
    REPORT_RUN_COMPARISON_SUMMARY,
    REPORT_MISSING_ARTIFACT_SUMMARY,
    REPORT_DUPLICATE_RUN_SUMMARY,
    REPORT_DATA_GOVERNANCE_STABLE_ROLLUP,
    REPORT_GOVERNANCE_ROLLUP_CONSISTENCY,
    REPORT_GOVERNANCE_ROLLUP_HEALTH_MATRIX,
    REPORT_GOVERNANCE_STORE_INVENTORY,
    REPORT_GOVERNANCE_STORE_VALIDATION,
    REPORT_GOVERNANCE_ROLLUP_HISTORY,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Pattern map: report_type -> list of glob patterns (relative to BASE_DIR)
# ---------------------------------------------------------------------------
_REPORT_PATTERNS = {
    REPORT_DAILY_MARKET:      ["reports/auto_report_center/*/daily_market_summary*.md",
                                "reports/auto_report_center/*/executive_summary.md"],
    REPORT_AUTO_REPORT:       ["reports/auto_report_center/*/index.md"],
    REPORT_DATA_QUALITY:      [
        # flat patterns (preserved)
        "reports/data_quality_gate_report*.md",
        "data/backtest_results/data_quality_gate*.csv",
        # nested auto_report_center patterns
        "reports/auto_report_center/*/data_quality_gate/*.md",
        "reports/auto_report_center/*/data_quality_gate/**/*.md",
    ],
    REPORT_PROVIDER:          ["reports/provider_reliability_report*.md",
                                "data/backtest_results/provider_reliability*.csv"],
    REPORT_STRATEGY_FILTER:   ["reports/strategy_filter_report*.md",
                                "data/backtest_results/strategy_filter_pack*.csv"],
    REPORT_SIGNAL_QUALITY:    ["reports/signal_quality_report*.md",
                                "data/backtest_results/signal_quality*.csv"],
    REPORT_RULE_GOVERNANCE:   ["reports/rule_governance_report*.md",
                                "data/backtest_results/governance*.csv"],
    REPORT_PORTFOLIO_JOURNAL: ["reports/portfolio_journal_report*.md",
                                "data/backtest_results/portfolio_journal_summary.csv"],
    REPORT_RESEARCH_REVIEW:   [
        # flat patterns (preserved)
        "reports/research_review_report*.md",
        "data/backtest_results/research_review*.csv",
        # nested auto_report_center patterns
        "reports/auto_report_center/*/research_review.md",
        "reports/auto_report_center/*/research_review/*.md",
        "reports/auto_report_center/*/research_review/**/*.md",
        "reports/research_review_dashboard_report*.md",
    ],
    REPORT_RESEARCH_COACH:    [
        # flat patterns (preserved)
        "reports/research_coach_report*.md",
        "data/backtest_results/research_coach*.csv",
        # nested auto_report_center patterns
        "reports/auto_report_center/*/research_coach.md",
        "reports/auto_report_center/*/research_coach/*.md",
        "reports/auto_report_center/*/research_coach/**/*.md",
        "reports/research_assistant_report*.md",
    ],
    REPORT_RESEARCH_WORKFLOW: ["reports/research_workflow_report*.md",
                                "data/backtest_results/research_workflow*.csv"],
    REPORT_RESEARCH_OS:       [
        # flat patterns (preserved)
        "reports/research_os_report*.md",
        "data/backtest_results/research_os*.csv",
        # nested auto_report_center patterns
        "reports/auto_report_center/*/research_os.md",
        "reports/auto_report_center/*/research_os/*.md",
        "reports/auto_report_center/*/research_os/**/*.md",
        "reports/research_os_stabilization_report*.md",
        "reports/stable_release_v0.6.0_report*.md",
    ],
    REPORT_REGRESSION:        [
        # flat and nested regression patterns
        "data/backtest_results/regression/regression_summary*.csv",
        "data/backtest_results/regression/regression_results*.csv",
        "data/backtest_results/regression/regression_coverage_matrix*.csv",
        "data/backtest_results/regression_suite_*.csv",
        "reports/regression_consolidation_report.md",
    ],
    REPORT_CLI_UX:            ["reports/cli_ux_report*.md",
                                "data/backtest_results/cli_ux*.csv"],
    REPORT_GUI_NAVIGATION:    ["reports/gui_navigation_report*.md",
                                "data/backtest_results/gui_navigation*.csv"],
    REPORT_NOTIFICATION:      ["reports/notification_center_report*.md",
                                "data/backtest_results/notification*.csv"],
    REPORT_INTRADAY_REPLAY:   ["reports/intraday_replay_report*.md",
                                "data/backtest_results/intraday_replay*.csv"],
    REPORT_EXPERIMENT:        ["reports/experiment_registry_report*.md",
                                "data/backtest_results/experiment*.csv"],
    REPORT_RELEASE:           ["reports/stable_release_checklist_report*.md",
                                "data/backtest_results/stable_release_checklist*.csv"],
    REPORT_SAFETY:            ["reports/stable_release_checklist_report*.md"],
    REPORT_DATA_STABILIZATION: [
        # flat patterns (preserved)
        "reports/data_stabilization_report_*.md",
        "data/backtest_results/data_stabilization/data_stabilization_summary_*.csv",
        # additional flat and nested patterns
        "reports/data_stabilization_report*.md",
        "reports/auto_report_center/*/data_stabilization.md",
        "reports/auto_report_center/*/data_stabilization/*.md",
        "reports/auto_report_center/*/data_stabilization/**/*.md",
    ],
    # v0.6.0 new report types
    REPORT_REPLAY_TRAINING: [
        "reports/replay_training_report*.md",
        "reports/replay_training_session_report_*.md",  # v1.2.0 session reports
        "reports/auto_report_center/*/replay_training.md",
        "reports/auto_report_center/*/replay_training/*.md",
        "reports/auto_report_center/*/replay_training/**/*.md",
        "data/backtest_results/replay_training/replay_training_summary*.csv",
        "data/backtest_results/replay_training/replay_ai_reviews*.csv",
        "data/backtest_results/replay_training/replay_scores*.csv",
    ],
    REPORT_STABLE_RELEASE_V060: [
        "reports/stable_release_v0.6.0_report*.md",
        "reports/stable_release_v060_report*.md",
        "reports/auto_report_center/*/stable_release.md",
        "reports/auto_report_center/*/stable_release/*.md",
        "reports/auto_report_center/*/stable_release/**/*.md",
    ],
    REPORT_RELEASE_MANIFEST: [
        "data/backtest_results/stable_release/release_manifest_v0.6.0.json",
        "data/backtest_results/stable_release/release_manifest_v0.6.0.md",
        "data/backtest_results/stable_release/release_manifest*.json",
        "data/backtest_results/stable_release/release_manifest*.md",
    ],
    # v0.6.2 Data Coverage Expansion
    REPORT_DATA_COVERAGE: [
        "reports/data_coverage_report*.md",
        "data/backtest_results/data_coverage/data_coverage_summary*.csv",
    ],
    # v0.7.0 Research Intelligence
    REPORT_RESEARCH_INTELLIGENCE: [
        "reports/research_intelligence_report*.md",
        "data/backtest_results/research_intelligence/research_intelligence_summary.csv",
    ],
    # v0.7.2 Strategy Research Memory
    REPORT_STRATEGY_MEMORY: [
        "reports/strategy_memory_report_*.md",
        "data/backtest_results/strategy_memory/strategy_memory_summary*.csv",
    ],
    # v0.7.3 Backtest-to-Coach Loop
    REPORT_BACKTEST_COACH: [
        "reports/backtest_coach_report_*.md",
        "data/backtest_results/backtest_coach/backtest_coach_summary*.csv",
    ],
    # v0.8.0 Research Intelligence Stable
    REPORT_INTELLIGENCE_STABLE: [
        "reports/intelligence_stable_report_*.md",
        "data/backtest_results/intelligence_stable/intelligence_stable_summary*.csv",
        "data/backtest_results/intelligence_stable/intelligence_release_manifest*.json",
        "data/backtest_results/intelligence_stable/intelligence_release_manifest*.md",
    ],
    # v0.8.2 Backtest Training Metrics
    REPORT_TRAINING_METRICS: [
        "reports/training_metrics_report_*.md",
        "data/backtest_results/training_metrics/training_metrics_summary*.csv",
    ],
    # v0.8.3 Research Intelligence Evidence Graph
    REPORT_EVIDENCE_GRAPH: [
        "reports/evidence_graph_report_*.md",
        "data/backtest_results/evidence_graph/evidence_graph_summary_*.csv",
    ],
    # v0.9.0 Strategy Lab Stable
    REPORT_STRATEGY_LAB_STABLE: [
        "reports/strategy_lab_stable_report_*.md",
        "data/backtest_results/strategy_lab/strategy_lab_summary_*.csv",
        "data/backtest_results/strategy_lab/strategy_lab_release_manifest_*.json",
    ],
    # v0.9.0.1 Crash Reversal & Risk Discipline Strategy Pack
    REPORT_CRASH_REVERSAL: [
        "reports/crash_reversal_strategy_report*.md",
        "data/backtest_results/crash_reversal/*.csv",
    ],
    # v0.9.2 Strategy Validation Score
    REPORT_STRATEGY_VALIDATION: [
        "reports/strategy_validation_report*.md",
        "data/backtest_results/strategy_validation/*.csv",
    ],
    # v0.9.3 Strategy Lab Dashboard
    "strategy_lab_dashboard_report": [
        "reports/strategy_lab_dashboard_report*.md",
        "data/backtest_results/strategy_lab_dashboard/*.csv",
    ],
    # v1.0.0 Research Trading Cockpit Stable
    REPORT_RESEARCH_COCKPIT_STABLE: [
        "reports/research_trading_cockpit_stable_report*.md",
        "data/backtest_results/release/*.csv",
        "data/backtest_results/release/*.json",
    ],
    # v1.0.2 Data & Report Hygiene
    REPORT_DATA_REPORT_HYGIENE: [
        "reports/data_report_hygiene_report*.md",
        "data/backtest_results/maintenance/*.csv",
    ],
    # v1.0.3 GUI Stability & Usability Polish
    REPORT_GUI_USABILITY: [
        "reports/gui_usability_report*.md",
    ],
    # v1.0.4 Regression & Release Gate Hardening
    REPORT_REGRESSION_HARDENING: [
        "reports/regression_hardening_report*.md",
    ],
    # v1.0.5 Documentation & User Guide Polish
    REPORT_DOCUMENTATION_HEALTH: [
        "reports/documentation_health_report*.md",
    ],
    # v1.0.6 Example Workflows & Templates
    REPORT_WORKFLOW_TEMPLATES: [
        "reports/workflow_templates_report*.md",
    ],
    # v1.0.7 Knowledge Base Search Polish
    REPORT_KNOWLEDGE_BASE_SEARCH: [
        "reports/knowledge_base_search_report*.md",
        "data/backtest_results/knowledge_base/*.csv",
    ],
    # v1.0.8 Local Research Assistant Polish
    REPORT_LOCAL_RESEARCH_ASSISTANT: [
        "reports/local_research_assistant_report*.md",
        "data/backtest_results/local_assistant/*.csv",
    ],
    # v1.0.9 Final Maintenance Rollup
    "final_maintenance_rollup_report": [
        "reports/final_maintenance_rollup_report*.md",
        "data/backtest_results/final_rollup/*.csv",
    ],
    # v1.1.0 Data Universe Expansion
    "data_universe_expansion_report": [
        "reports/data_universe_expansion_report*.md",
        "data/backtest_results/universe/*.csv",
    ],
    # v1.1.1 Data Import UX & Batch Onboarding
    REPORT_DATA_IMPORT_ONBOARDING: [
        "reports/data_import_onboarding_report*.md",
        "data/import_reports/*.csv",
    ],
    # v1.1.2 Coverage Repair Workflow
    REPORT_COVERAGE_REPAIR: [
        "reports/coverage_repair_report*.md",
        "data/repair_reports/*.csv",
    ],
    # v1.1.3 Data Freshness Monitor
    REPORT_DATA_FRESHNESS: [
        "reports/data_freshness_report*.md",
        "data/freshness_reports/*.csv",
    ],
    # v1.1.4 Coverage Quality Gates
    REPORT_COVERAGE_QUALITY_GATE: [
        "reports/coverage_quality_gate_report*.md",
        "data/quality_gate_reports/*.csv",
    ],
    # v1.1.5 Quality Gate Enforcement & Audit
    REPORT_GATE_ENFORCEMENT_AUDIT: [
        "reports/quality_gate_enforcement_audit_report*.md",
        "data/quality_gate_enforcement/*.csv",
        "data/quality_gate_audit/*.jsonl",
    ],
    REPORT_GATE_RUN_SUMMARY: [
        "data/quality_gate_enforcement/run_results.csv",
        "data/quality_gate_enforcement/run_requests.csv",
    ],
    REPORT_GATE_EXCLUSION_SUMMARY: [
        "data/quality_gate_enforcement/symbol_exclusions.csv",
        "data/quality_gate_audit/exclusion_records.csv",
    ],
    REPORT_GATE_REPRODUCIBILITY: [
        "data/quality_gate_enforcement/run_hashes.csv",
        "data/quality_gate_audit/reproducibility_hashes.csv",
    ],
    # v1.1.6 Data Governance Operations Dashboard
    REPORT_DATA_GOVERNANCE_OPERATIONS: [
        "reports/data_governance_operations_report*.md",
        "data/governance_ops/governance_summary.json",
        "data/governance_ops/daily_history.jsonl",
    ],
    REPORT_GOVERNANCE_ACTION_QUEUE: [
        "data/governance_ops/action_queue.csv",
        "data/governance_ops/action_audit.jsonl",
    ],
    REPORT_GOVERNANCE_MODULE_HEALTH: [
        "data/governance_ops/module_health.csv",
    ],
    REPORT_GOVERNANCE_AUDIT_SUMMARY: [
        "data/governance_ops/audit_summary.csv",
        "data/governance_ops/enforcement_runs.csv",
    ],
    # v1.1.7 Governance Alerts & Daily Operations
    REPORT_GOVERNANCE_ALERTS_DAILY_OPS: [
        "reports/governance_alerts_daily_operations_report*.md",
        "data/governance_alerts/alerts.jsonl",
        "data/governance_alerts/alert_index.csv",
    ],
    REPORT_GOVERNANCE_MORNING_DIGEST: [
        "data/governance_alerts/digests.jsonl",
        "data/governance_alerts/daily_metrics.csv",
    ],
    REPORT_GOVERNANCE_EOD_DIGEST: [
        "data/governance_alerts/digests.jsonl",
    ],
    REPORT_GOVERNANCE_WEEKLY_DIGEST: [
        "data/governance_alerts/digests.jsonl",
    ],
    REPORT_GOVERNANCE_ALERT_TREND: [
        "data/governance_alerts/daily_metrics.csv",
        "data/governance_alerts/alert_index.csv",
    ],
    REPORT_GOVERNANCE_CHECKLIST: [
        "data/governance_alerts/daily_checklists.jsonl",
    ],
    # v1.1.8 Research Run Registry patterns
    REPORT_RESEARCH_RUN_REGISTRY: [
        "reports/research_run_registry_report*.md",
    ],
    REPORT_LATEST_RUN_SUMMARY: [
        "data/research_registry/registry_summary.json",
    ],
    REPORT_RUN_COMPARISON_SUMMARY: [
        "data/research_registry/comparisons.jsonl",
    ],
    REPORT_MISSING_ARTIFACT_SUMMARY: [
        "data/research_registry/artifact_index.csv",
    ],
    REPORT_DUPLICATE_RUN_SUMMARY: [
        "data/research_registry/duplicate_index.csv",
    ],
    # v1.1.9 Data Governance Stable Rollup patterns
    REPORT_DATA_GOVERNANCE_STABLE_ROLLUP: [
        "reports/data_governance_stable_rollup_report*.md",
    ],
    REPORT_GOVERNANCE_ROLLUP_CONSISTENCY: [
        "data/governance_rollup/consistency_report*.json",
    ],
    REPORT_GOVERNANCE_ROLLUP_HEALTH_MATRIX: [
        "data/governance_rollup/health_matrix*.json",
    ],
    REPORT_GOVERNANCE_STORE_INVENTORY: [
        "data/governance_rollup/store_inventory*.json",
    ],
    REPORT_GOVERNANCE_STORE_VALIDATION: [
        "data/governance_rollup/store_validation*.json",
    ],
    REPORT_GOVERNANCE_ROLLUP_HISTORY: [
        "data/governance_rollup/rollup_history.jsonl",
    ],
    # v0.9.1 Evidence Graph UX patterns
    "evidence_graph_gaps": [
        "data/backtest_results/evidence_graph/evidence_graph_gaps*.csv",
    ],
    "evidence_thread_paths": [
        "data/backtest_results/evidence_graph/evidence_thread_paths*.csv",
    ],
}


class ReportCollector:
    """Scans output directories to collect report status for each report type.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir or BASE_DIR

    def collect(self, report_types: List[str], report_date: Optional[str] = None) -> List[ReportPackItem]:
        """Collect status for each report_type. Returns list of ReportPackItem."""
        today = report_date or datetime.now().strftime("%Y-%m-%d")
        items: List[ReportPackItem] = []
        for rt in report_types:
            item = self._collect_one(rt, today)
            items.append(item)
        return items

    def _collect_one(self, report_type: str, report_date: str) -> ReportPackItem:
        """Check file system for a given report type."""
        try:
            patterns = _REPORT_PATTERNS.get(report_type, [])
            found_path = ""
            found_size = 0

            for pattern in patterns:
                full_pattern = os.path.join(self.base_dir, pattern)
                matches = sorted(glob.glob(full_pattern, recursive=True))
                if matches:
                    found_path = matches[-1]
                    try:
                        found_size = os.path.getsize(found_path)
                    except Exception:
                        found_size = 0
                    break

            if found_path and found_size > 0:
                return ReportPackItem(
                    report_type=report_type,
                    status=STATUS_READY,
                    path=found_path,
                    report_date=report_date,
                    size_bytes=found_size,
                    generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            # Classify missing reports by type
            if report_type in ENV_LIMITED_REPORT_TYPES:
                missing_status = STATUS_ENV_LIMITED
                notes = f"Environment-limited: {report_type} requires provider token setup"
            elif report_type in OPTIONAL_REPORT_TYPES:
                missing_status = STATUS_NOT_GENERATED
                notes = f"Optional report not yet generated: {report_type}"
            else:
                missing_status = STATUS_MISSING
                notes = f"No output found for {report_type}"
            return ReportPackItem(
                report_type=report_type,
                status=missing_status,
                report_date=report_date,
                notes=notes,
            )
        except Exception as exc:
            logger.warning("ReportCollector._collect_one(%s) failed: %s", report_type, exc)
            return ReportPackItem(
                report_type=report_type,
                status=STATUS_FAILED,
                report_date=report_date,
                error=str(exc),
            )
