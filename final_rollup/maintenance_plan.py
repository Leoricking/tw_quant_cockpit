"""
final_rollup/maintenance_plan.py — Long-Term Maintenance Plan for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
[!] All commands are single-step only. No compound commands.
"""
from __future__ import annotations

import logging
from typing import List

from final_rollup.rollup_schema import (
    LongTermMaintenanceTask,
    CADENCE_DAILY, CADENCE_WEEKLY, CADENCE_MONTHLY, CADENCE_RELEASE, CADENCE_INCIDENT,
    SAFE_REVIEW, SAFE_READ_REPORT, SAFE_FIX_DATA, SAFE_BACKTEST_MORE, SAFE_KEEP_OBSERVING, SAFE_WAIT,
)

logger = logging.getLogger(__name__)


class LongTermMaintenancePlanBuilder:
    """Builds the long-term maintenance SOP for TW Quant Cockpit v1.0.x.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    All commands are single-step only — no compound commands, no broker, no live trading.
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    def build(self) -> List[LongTermMaintenanceTask]:
        """Build the complete long-term maintenance task list."""
        tasks: List[LongTermMaintenanceTask] = []

        # --- DAILY ---
        tasks.extend([
            LongTermMaintenanceTask(
                task_id="daily_version_info",
                cadence=CADENCE_DAILY,
                title="Check version info",
                command="python main.py version-info",
                expected_result="Version: 1.0.9 displayed",
                owner_note="Confirm version and safety flags each session.",
                safe_action=SAFE_READ_REPORT,
            ),
            LongTermMaintenanceTask(
                task_id="daily_local_assistant_health",
                cadence=CADENCE_DAILY,
                title="Local assistant health",
                command="python main.py local-assistant-health",
                expected_result="All checks PASS or acceptable WARN",
                owner_note="Ensure local assistant is functional.",
                safe_action=SAFE_READ_REPORT,
            ),
            LongTermMaintenanceTask(
                task_id="daily_kb_health",
                cadence=CADENCE_DAILY,
                title="KB health check",
                command="python main.py kb-health-check",
                expected_result="Knowledge Base health PASS",
                owner_note="Verify KB index is intact.",
                safe_action=SAFE_READ_REPORT,
            ),
            LongTermMaintenanceTask(
                task_id="daily_data_hygiene",
                cadence=CADENCE_DAILY,
                title="Data report hygiene summary",
                command="python main.py data-report-hygiene-summary",
                expected_result="No unexpected tracked runtime outputs",
                owner_note="Check data hygiene daily.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="daily_strategy_lab",
                cadence=CADENCE_DAILY,
                title="Strategy lab dashboard summary",
                command="python main.py strategy-lab-dashboard-summary",
                expected_result="Strategy lab status visible",
                owner_note="Review strategy lab daily.",
                safe_action=SAFE_READ_REPORT,
            ),
        ])

        # --- WEEKLY ---
        tasks.extend([
            LongTermMaintenanceTask(
                task_id="weekly_report_pack",
                cadence=CADENCE_WEEKLY,
                title="Full report pack",
                command="python main.py report-pack --type full --mode real",
                expected_result="Report pack generated",
                owner_note="Run full report pack weekly.",
                safe_action=SAFE_READ_REPORT,
            ),
            LongTermMaintenanceTask(
                task_id="weekly_docs_health",
                cadence=CADENCE_WEEKLY,
                title="Docs health check",
                command="python main.py docs-health-check",
                expected_result="Documentation health PASS",
                owner_note="Check docs health weekly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="weekly_workflow_templates",
                cadence=CADENCE_WEEKLY,
                title="Workflow templates health",
                command="python main.py workflow-templates-health",
                expected_result="Workflow templates health PASS",
                owner_note="Verify workflow templates weekly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="weekly_safety_scan",
                cadence=CADENCE_WEEKLY,
                title="Safety scan all",
                command="python main.py safety-scan --target all",
                expected_result="448/448 PASS or stable count",
                owner_note="Run safety scan weekly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="weekly_cockpit_stable",
                cadence=CADENCE_WEEKLY,
                title="Research cockpit stable",
                command="python main.py research-cockpit-stable --mode real",
                expected_result="All stable checks PASS",
                owner_note="Verify cockpit stable weekly.",
                safe_action=SAFE_REVIEW,
            ),
        ])

        # --- MONTHLY ---
        tasks.extend([
            LongTermMaintenanceTask(
                task_id="monthly_stable_v060",
                cadence=CADENCE_MONTHLY,
                title="Stable v0.6.0 check",
                command="python main.py stable-v060-check --mode real",
                expected_result="stable-v060-check PASS",
                owner_note="Run stable v0.6.0 check monthly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="monthly_regression_release_gate",
                cadence=CADENCE_MONTHLY,
                title="Regression release gate",
                command="python main.py regression-run --suite release_gate --mode real",
                expected_result="release_gate suite PASS",
                owner_note="Run release gate regression monthly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="monthly_regression_quick",
                cadence=CADENCE_MONTHLY,
                title="Quick regression",
                command="python main.py regression-run --suite quick --mode real",
                expected_result="quick suite PASS",
                owner_note="Run quick regression monthly.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="monthly_review_docs",
                cadence=CADENCE_MONTHLY,
                title="Review docs/examples/templates",
                command="python main.py docs-health-check",
                expected_result="Docs health check PASS",
                owner_note="Review docs, examples, templates monthly.",
                safe_action=SAFE_REVIEW,
            ),
        ])

        # --- RELEASE ---
        tasks.extend([
            LongTermMaintenanceTask(
                task_id="release_compileall",
                cadence=CADENCE_RELEASE,
                title="Compile all Python",
                command="python -m compileall .",
                expected_result="No syntax errors",
                owner_note="Run before every release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_version_info",
                cadence=CADENCE_RELEASE,
                title="Version info check",
                command="python main.py version-info",
                expected_result="Correct version displayed",
                owner_note="Verify version before release.",
                safe_action=SAFE_READ_REPORT,
            ),
            LongTermMaintenanceTask(
                task_id="release_safety_scan_docs",
                cadence=CADENCE_RELEASE,
                title="Safety scan docs",
                command="python main.py safety-scan --target docs",
                expected_result="PASS",
                owner_note="Scan docs for forbidden actions before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_safety_scan_all",
                cadence=CADENCE_RELEASE,
                title="Safety scan all",
                command="python main.py safety-scan --target all",
                expected_result="PASS",
                owner_note="Full safety scan before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_cockpit_stable",
                cadence=CADENCE_RELEASE,
                title="Research cockpit stable",
                command="python main.py research-cockpit-stable --mode real",
                expected_result="STABLE",
                owner_note="Run stable check before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_stable_v060",
                cadence=CADENCE_RELEASE,
                title="Stable v0.6.0 check",
                command="python main.py stable-v060-check --mode real",
                expected_result="PASS",
                owner_note="Run v0.6.0 stable check before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_gate_regression",
                cadence=CADENCE_RELEASE,
                title="Release gate regression",
                command="python main.py regression-run --suite release_gate --mode real",
                expected_result="PASS",
                owner_note="Run release gate regression before tagging.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_quick_regression",
                cadence=CADENCE_RELEASE,
                title="Quick regression",
                command="python main.py regression-run --suite quick --mode real",
                expected_result="PASS",
                owner_note="Run quick regression before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_mock_realtime",
                cadence=CADENCE_RELEASE,
                title="Mock realtime smoke",
                command="python main.py mock-realtime --duration 10",
                expected_result="Smoke PASS",
                owner_note="Run mock-realtime smoke before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_paper",
                cadence=CADENCE_RELEASE,
                title="Paper smoke",
                command="python main.py paper",
                expected_result="Paper positions displayed",
                owner_note="Run paper smoke before release.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="release_git_status",
                cadence=CADENCE_RELEASE,
                title="Git status clean",
                command='git -C "C:/Users/Rossi/Documents/Claude/trading_master" status',
                expected_result="working tree clean",
                owner_note="Verify clean git state before tagging.",
                safe_action=SAFE_REVIEW,
            ),
        ])

        # --- INCIDENT ---
        tasks.extend([
            LongTermMaintenanceTask(
                task_id="incident_safety_scan",
                cadence=CADENCE_INCIDENT,
                title="Safety scan on incident",
                command="python main.py safety-scan --target all",
                expected_result="No forbidden actions",
                owner_note="Run safety scan immediately on incident.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="incident_release_gate_health",
                cadence=CADENCE_INCIDENT,
                title="Release gate health on incident",
                command="python main.py release-gate-health --mode real",
                expected_result="Release gate health PASS",
                owner_note="Check release gate health on incident.",
                safe_action=SAFE_REVIEW,
            ),
            LongTermMaintenanceTask(
                task_id="incident_data_hygiene",
                cadence=CADENCE_INCIDENT,
                title="Data hygiene on incident",
                command="python main.py data-report-hygiene-summary",
                expected_result="Hygiene summary clean",
                owner_note="Check data hygiene on incident.",
                safe_action=SAFE_FIX_DATA,
            ),
            LongTermMaintenanceTask(
                task_id="incident_local_assistant_unsafe",
                cadence=CADENCE_INCIDENT,
                title="Local assistant unsafe query test",
                command='python main.py local-assistant --ask "should I buy"',
                expected_result="BLOCKED_UNSAFE_QUERY",
                owner_note="Verify unsafe query blocking is intact.",
                safe_action=SAFE_REVIEW,
            ),
        ])

        return tasks

    def get_by_cadence(self, cadence: str) -> List[LongTermMaintenanceTask]:
        return [t for t in self.build() if t.cadence == cadence]

    def get_summary(self) -> dict:
        tasks = self.build()
        by_cadence: dict = {}
        for t in tasks:
            by_cadence.setdefault(t.cadence, 0)
            by_cadence[t.cadence] += 1
        return {
            "total_tasks": len(tasks),
            "by_cadence": by_cadence,
            "no_real_orders": True,
            "broker_disabled": True,
        }
