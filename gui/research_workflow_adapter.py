"""
gui/research_workflow_adapter.py — ResearchWorkflowAdapter (v0.4.9).

GUI bridge for Research Workflow Automation panel.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchWorkflowAdapter:
    """
    GUI bridge for ResearchWorkflowPanel.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/research_workflow",
        report_dir: str = "reports",
    ):
        self._output_dir = (
            os.path.join(BASE_DIR, output_dir)
            if not os.path.isabs(output_dir)
            else output_dir
        )
        self._report_dir = (
            os.path.join(BASE_DIR, report_dir)
            if not os.path.isabs(report_dir)
            else report_dir
        )

    def run_workflow(
        self,
        mode:          str  = "real",
        workflow_type: str  = "daily_research",
        dry_run:       bool = True,
    ) -> dict:
        """
        Run the Research Workflow and save results.
        Returns summary dict.
        Does NOT execute any trading commands.
        """
        try:
            from workflow_automation.workflow_builder import ResearchWorkflowBuilder
            from workflow_automation.workflow_runner import ResearchWorkflowRunner
            from workflow_automation.package_builder import ResearchPackageBuilder
            from workflow_automation.workflow_store import ResearchWorkflowStore

            builder = ResearchWorkflowBuilder()
            runner  = ResearchWorkflowRunner(output_dir=self._output_dir, dry_run=dry_run)

            if workflow_type == "weekly_review":
                tasks = builder.build_weekly_review_workflow()
            elif workflow_type == "data_repair":
                tasks = builder.build_data_repair_workflow()
            elif workflow_type == "rule_review":
                tasks = builder.build_rule_review_workflow()
            elif workflow_type == "replay_training":
                tasks = builder.build_replay_training_workflow()
            elif workflow_type == "safety_check":
                tasks = builder.build_safety_check_workflow()
            else:
                tasks = builder.build_daily_research_workflow()

            wf_run = runner.run_workflow(tasks, mode=mode, workflow_type=workflow_type)

            # Build package
            package_path = ""
            try:
                pkg_builder = ResearchPackageBuilder(
                    output_dir=self._output_dir, report_dir=self._report_dir
                )
                if workflow_type == "weekly_review":
                    package_path = pkg_builder.build_weekly_package(wf_run)
                else:
                    package_path = pkg_builder.build_daily_package(wf_run)
            except Exception as pkg_exc:
                logger.warning("Package build failed: %s", pkg_exc)

            # Save results
            store = ResearchWorkflowStore(output_dir=self._output_dir)
            store.save_all(wf_run, runner.last_tasks, package_path=package_path)

            return {
                **wf_run.to_dict(),
                "tasks":        [t.to_dict() for t in runner.last_tasks],
                "package_path": package_path,
                "workflow_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("[ResearchWorkflowAdapter] run_workflow failed: %s", exc)
            return {"error": str(exc), "workflow_only": True, "no_real_orders": True}

    def generate_report(self, mode: str = "real", workflow_type: str = "daily_research") -> str:
        """Generate Research Workflow report. Returns report file path."""
        try:
            from workflow_automation.workflow_store import ResearchWorkflowStore
            from reports.research_workflow_report import ResearchWorkflowReport
            store    = ResearchWorkflowStore(output_dir=self._output_dir)
            summary  = store.load_latest_summary()
            tasks    = store.load_latest_tasks()
            reporter = ResearchWorkflowReport(report_dir=self._report_dir)
            from workflow_automation.workflow_schema import ResearchWorkflowRun
            run = ResearchWorkflowRun.from_dict(summary) if summary else None
            task_objs = []
            from workflow_automation.workflow_schema import ResearchWorkflowTask
            for t in tasks:
                task_objs.append(ResearchWorkflowTask.from_dict(t))
            pkg_path = summary.get("output_package_path", "") if summary else ""
            path = reporter.generate(
                workflow_run=run,
                tasks=task_objs,
                package_path=pkg_path,
                mode=mode,
                workflow_type=workflow_type,
            )
            return path
        except Exception as exc:
            logger.error("[ResearchWorkflowAdapter] generate_report failed: %s", exc)
            return ""

    def load_latest_summary(self) -> Optional[dict]:
        """Load latest workflow summary from persisted CSV."""
        try:
            from workflow_automation.workflow_store import ResearchWorkflowStore
            store = ResearchWorkflowStore(output_dir=self._output_dir)
            return store.load_latest_summary()
        except Exception as exc:
            logger.warning("[ResearchWorkflowAdapter] load_latest_summary failed: %s", exc)
            return None

    def load_latest_tasks(self) -> List[dict]:
        """Load latest workflow tasks from persisted CSV."""
        try:
            from workflow_automation.workflow_store import ResearchWorkflowStore
            store = ResearchWorkflowStore(output_dir=self._output_dir)
            return store.load_latest_tasks()
        except Exception as exc:
            logger.warning("[ResearchWorkflowAdapter] load_latest_tasks failed: %s", exc)
            return []

    def load_latest_package_path(self) -> str:
        """Return latest package directory path or empty string."""
        try:
            summary = self.load_latest_summary()
            if summary:
                return summary.get("output_package_path", "")
            return ""
        except Exception:
            return ""

    def load_latest_report_path(self) -> str:
        """Return path of the latest workflow report file, or empty string."""
        try:
            pattern = os.path.join(self._report_dir, "research_workflow_report_*.md")
            files   = sorted(glob.glob(pattern))
            return files[-1] if files else ""
        except Exception:
            return ""
