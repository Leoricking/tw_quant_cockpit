"""
workflow_automation/package_builder.py — ResearchPackageBuilder (v0.4.9).

Produces daily / weekly research packages: index.md + manifest.json.

Outputs (gitignored):
  data/backtest_results/research_workflow/daily_package_YYYY-MM-DD/index.md
  data/backtest_results/research_workflow/weekly_package_YYYY-MM-DD/index.md
  data/backtest_results/research_workflow/package_manifest.json

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from workflow_automation.workflow_schema import ResearchWorkflowRun

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchPackageBuilder:
    """
    Builds daily / weekly research packages.

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

    def build_daily_package(self, workflow_run: Optional[ResearchWorkflowRun] = None) -> str:
        """
        Build daily research package. Returns package directory path.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        pkg_dir = os.path.join(self._output_dir, f"daily_package_{today}")
        os.makedirs(pkg_dir, exist_ok=True)

        sections = self._daily_sections(workflow_run)
        index_path = os.path.join(pkg_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(sections))

        manifest = self._build_manifest("daily_research", pkg_dir, workflow_run)
        manifest_path = os.path.join(self._output_dir, "package_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)

        logger.info("[PackageBuilder] Daily package: %s", pkg_dir)
        return pkg_dir

    def build_weekly_package(self, workflow_run: Optional[ResearchWorkflowRun] = None) -> str:
        """
        Build weekly review package. Returns package directory path.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        pkg_dir = os.path.join(self._output_dir, f"weekly_package_{today}")
        os.makedirs(pkg_dir, exist_ok=True)

        sections = self._weekly_sections(workflow_run)
        index_path = os.path.join(pkg_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(sections))

        manifest = self._build_manifest("weekly_review", pkg_dir, workflow_run)
        manifest_path = os.path.join(self._output_dir, "package_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)

        logger.info("[PackageBuilder] Weekly package: %s", pkg_dir)
        return pkg_dir

    def collect_report_links(self) -> List[str]:
        """Collect links to existing report files."""
        links = []
        for pattern in [
            "research_review_dashboard_report_*.md",
            "research_assistant_report_*.md",
            "research_workflow_report_*.md",
            "auto_report_*.md",
        ]:
            matches = sorted(glob.glob(os.path.join(self._report_dir, pattern)))
            links.extend(matches[-2:])  # last 2 of each type
        return links

    def build_index_markdown(self) -> str:
        """Build a simple index markdown of available packages."""
        lines = ["# Research Workflow Package Index", ""]
        today = datetime.now().strftime("%Y-%m-%d")
        for prefix in ("daily_package", "weekly_package"):
            pattern = os.path.join(self._output_dir, f"{prefix}_*")
            dirs = sorted(glob.glob(pattern))
            if dirs:
                lines.append(f"## {prefix.replace('_', ' ').title()}")
                for d in dirs[-3:]:
                    lines.append(f"- {d}")
                lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _daily_sections(self, run: Optional[ResearchWorkflowRun]) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        lines = [
            "# Daily Research Package",
            "",
            f"> Generated: {today}",
            ">",
            "> **[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.**",
            "",
            "## 一、Workflow Summary",
            "",
        ]
        if run:
            lines += [
                f"| Field | Value |",
                f"|-------|-------|",
                f"| Workflow ID | {run.workflow_id} |",
                f"| Mode | {run.mode} |",
                f"| Status | {run.status} |",
                f"| Tasks Total | {run.tasks_total} |",
                f"| Tasks Passed | {run.tasks_passed} |",
                f"| Tasks Failed | {run.tasks_failed} |",
                f"| Tasks Blocked | {run.tasks_blocked} |",
                "",
            ]
        else:
            lines += ["_No workflow run data._", ""]

        lines += self._section_from_store("## 二、Coach Checklist Summary", "coach_checklist")
        lines += self._section_from_review("## 三、Research Review Summary")
        lines += self._section_from_notifications("## 四、Notification Summary")
        lines += self._section_from_journal("## 五、Journal Summary")
        lines += self._section_from_data_quality("## 六、Data Quality Summary")
        lines += self._section_from_provider("## 七、Provider Reliability Summary")
        lines += self._section_from_rule_governance("## 八、Rule Governance Summary")
        lines += self._section_from_ml("## 九、ML Knowledge Summary")
        lines += self._section_report_links("## 十、Report Links")
        lines += self._section_next_actions("## 十一、Next Action List")
        lines += self._section_safety()
        return lines

    def _weekly_sections(self, run: Optional[ResearchWorkflowRun]) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        lines = [
            "# Weekly Review Package",
            "",
            f"> Generated: {today}",
            ">",
            "> **[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.**",
            "",
            "## 一、Weekly Workflow Summary",
            "",
        ]
        if run:
            lines += [
                f"| Field | Value |",
                f"|-------|-------|",
                f"| Workflow ID | {run.workflow_id} |",
                f"| Mode | {run.mode} |",
                f"| Status | {run.status} |",
                f"| Tasks Passed | {run.tasks_passed} |",
                f"| Tasks Failed | {run.tasks_failed} |",
                "",
            ]
        else:
            lines += ["_No workflow run data._", ""]

        lines += self._section_from_review("## 二、Weekly Scorecard")
        lines += self._section_top_mistakes("## 三、Top Mistakes This Week")
        lines += self._section_from_rule_governance("## 四、Weak Rules")
        lines += self._section_from_data_quality("## 五、Data Blockers")
        lines += self._section_from_store("## 六、Replay Training Progress", "replay_training")
        lines += self._section_from_journal("## 七、Journal Review Backlog")
        lines += self._section_experiment("## 八、Experiment Summary")
        lines += self._section_from_ml("## 九、Model Monitoring Summary")
        lines += self._section_next_actions("## 十、Next Week Action Plan")
        lines += self._section_safety()
        return lines

    # ------------------------------------------------------------------
    # Data load helpers — all graceful fallback
    # ------------------------------------------------------------------

    def _section_from_store(self, header: str, section_type: str) -> List[str]:
        lines = [header, ""]
        try:
            from coach.coach_store import ResearchCoachStore
            store   = ResearchCoachStore()
            summary = store.load_latest_summary()
            if summary:
                lines.append(f"- Total recommendations: {summary.get('total_recommendations', 0)}")
                lines.append(f"- P0: {summary.get('p0_count', 0)}, P1: {summary.get('p1_count', 0)}")
                lines.append(f"- Replay tasks: {summary.get('replay_tasks_count', 0)}")
                lines.append(f"- Rule reviews: {summary.get('rule_review_count', 0)}")
                lines.append(f"- Data repairs: {summary.get('data_repair_count', 0)}")
            else:
                lines.append("_No coach data found._")
        except Exception:
            lines.append("_Coach data unavailable._")
        lines.append("")
        return lines

    def _section_from_review(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from review.review_store import ResearchReviewStore
            store   = ResearchReviewStore()
            summary = store.load_latest_summary()
            if summary:
                lines.append(f"- Open items: {summary.get('open_items', 0)}")
                lines.append(f"- Critical: {summary.get('critical_items', 0)}")
                lines.append(f"- Action items: {summary.get('action_items_count', 0)}")
                lines.append(f"- Most common mistake: {summary.get('most_common_mistake', '—')}")
            else:
                lines.append("_No review data found. Run: python main.py research-review --mode real --period daily_")
        except Exception:
            lines.append("_Review data unavailable._")
        lines.append("")
        return lines

    def _section_from_notifications(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from notifications.notification_center import NotificationCenter
            nc      = NotificationCenter()
            summary = nc.coach_summary()
            lines.append(f"- Critical: {summary.get('critical', 0)}")
            lines.append(f"- Warning: {summary.get('warning', 0)}")
            lines.append(f"- Unread: {summary.get('unread', 0)}")
        except Exception:
            lines.append("_Notification data unavailable._")
        lines.append("")
        return lines

    def _section_from_journal(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from journal.journal_analytics import JournalAnalytics
            analytics = JournalAnalytics()
            summary   = analytics.coach_summary()
            lines.append(f"- Total entries: {summary.get('total_entries', 0)}")
            lines.append(f"- Review backlog: {summary.get('review_backlog', 0)}")
            top = summary.get("top_mistakes", [])
            if top:
                lines.append(f"- Top mistakes: {', '.join(str(m) for m in top[:3])}")
        except Exception:
            lines.append("_Journal data unavailable._")
        lines.append("")
        return lines

    def _section_from_data_quality(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from quality.data_quality_gate import DataQualityGate
            gate    = DataQualityGate()
            summary = gate.coach_data_repair_candidates()
            lines.append(f"- Blockers: {summary.get('blocker_count', 0)}")
            lines.append(f"- Stale datasets: {len(summary.get('stale_datasets', []))}")
            lines.append(f"- Missing datasets: {len(summary.get('missing_datasets', []))}")
        except Exception:
            lines.append("_Data quality data unavailable._")
        lines.append("")
        return lines

    def _section_from_provider(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            prm     = ProviderReliabilityMatrix()
            summary = prm.coach_provider_repair_candidates()
            lines.append(f"- Failed providers: {len(summary.get('failed_providers', []))}")
        except Exception:
            lines.append("_Provider data unavailable._")
        lines.append("")
        return lines

    def _section_from_rule_governance(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from governance.rule_confidence import RuleConfidenceScorer
            scorer  = RuleConfidenceScorer()
            summary = scorer.coach_rule_review_candidates()
            lines.append(f"- Total rules: {summary.get('total_rules', 0)}")
            lines.append(f"- Low confidence: {len(summary.get('low_confidence_rules', []))}")
            lines.append(f"- Weak confidence: {len(summary.get('weak_rules', []))}")
        except Exception:
            lines.append("_Rule governance data unavailable._")
        lines.append("")
        return lines

    def _section_from_ml(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            lines.append("- Run `python main.py ml-knowledge-feature-summary` for ML status.")
        except Exception:
            pass
        lines.append("")
        return lines

    def _section_top_mistakes(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from journal.journal_analytics import JournalAnalytics
            analytics = JournalAnalytics()
            summary   = analytics.coach_summary()
            top = summary.get("top_mistakes", [])
            if top:
                for m in top[:5]:
                    lines.append(f"- {m}")
            else:
                lines.append("_No mistake data found._")
        except Exception:
            lines.append("_Mistake data unavailable._")
        lines.append("")
        return lines

    def _section_experiment(self, header: str) -> List[str]:
        lines = [header, ""]
        lines.append("- Run `python main.py experiment-list` for experiment status.")
        lines.append("")
        return lines

    def _section_report_links(self, header: str) -> List[str]:
        lines = [header, ""]
        links = self.collect_report_links()
        if links:
            for link in links:
                lines.append(f"- {link}")
        else:
            lines.append("_No reports found._")
        lines.append("")
        return lines

    def _section_next_actions(self, header: str) -> List[str]:
        lines = [header, ""]
        try:
            from review.review_store import ResearchReviewStore
            store   = ResearchReviewStore()
            actions = store.load_latest_action_plan()
            if actions:
                for a in actions[:5]:
                    t   = a.get("title", "")
                    cmd = a.get("suggested_command", "")
                    p   = a.get("priority", "")
                    lines.append(f"- [{p}] {t}")
                    if cmd:
                        lines.append(f"  → `{cmd}`")
            else:
                lines.append("_No action plan found._")
        except Exception:
            lines.append("_Action plan unavailable._")
        lines.append("")
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 安全聲明",
            "",
            "- **Workflow Only** — This is research workflow automation only.",
            "- **Research Only** — All tasks are read-only research commands.",
            "- **No Real Orders** — No buy/sell/order. No broker connection.",
            "- **Not Investment Advice** — Not financial advice. Not trading recommendation.",
            "- **Production Trading BLOCKED** — REAL_ORDER_READY=False.",
            "",
        ]

    def _build_manifest(
        self,
        package_type: str,
        pkg_dir:      str,
        run:          Optional[ResearchWorkflowRun],
    ) -> dict:
        today = datetime.now().strftime("%Y-%m-%d")
        manifest = {
            "generated_at":  datetime.now().isoformat(timespec="seconds"),
            "package_type":  package_type,
            "package_path":  pkg_dir,
            "workflow_only": True,
            "research_only": True,
            "no_real_orders": True,
            "production_blocked": True,
            "report_links":  self.collect_report_links(),
        }
        if run:
            manifest["workflow_id"]      = run.workflow_id
            manifest["tasks_total"]      = run.tasks_total
            manifest["tasks_passed"]     = run.tasks_passed
            manifest["tasks_failed"]     = run.tasks_failed
            manifest["tasks_blocked"]    = run.tasks_blocked
            manifest["workflow_status"]  = run.status
        return manifest
