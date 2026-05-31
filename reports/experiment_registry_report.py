"""
reports/experiment_registry_report.py — ExperimentRegistryReportBuilder (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import datetime
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_SECTION = """\
## 六、安全聲明

- Research Only: True
- Backtest Only: True
- No Real Orders: True
- No automatic trading: True
- Production Trading: BLOCKED
- REAL_ORDER_READY: False
"""


class ExperimentRegistryReportBuilder:
    """
    Generates a Markdown summary report of the Experiment Registry.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        registry_root: str = "experiments",
        report_dir: str = "reports",
    ):
        self._registry_root = os.path.join(BASE_DIR, registry_root)
        self._report_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, output_path: str = None) -> str:
        """
        Build the experiment registry report and write it to disk.
        Returns the absolute path to the written file.
        """
        try:
            if output_path is None:
                today = datetime.date.today().isoformat()
                fname = f"experiment_registry_report_{today}.md"
                output_path = os.path.join(self._report_dir, fname)

            content = self._build_content()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info("Experiment registry report written to %s", output_path)
            return output_path

        except Exception:
            logger.exception("ExperimentRegistryReportBuilder.build failed")
            return ""

    # ------------------------------------------------------------------
    # Internal rendering
    # ------------------------------------------------------------------

    def _build_content(self) -> str:
        """Assemble the full Markdown report content."""
        try:
            from experiments.experiment_registry import ExperimentRegistry
            from experiments.experiment_comparator import ExperimentComparator

            reg = ExperimentRegistry(
                registry_root=os.path.relpath(self._registry_root, BASE_DIR)
            )
            summary = reg.build_registry_summary()
            experiments = reg.list_experiments(limit=50)

        except Exception:
            logger.exception("_build_content: failed to load registry")
            summary = {"total": 0, "by_status": {}, "by_type": {}, "latest_experiment_id": "", "latest_created_at": ""}
            experiments = []

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = []

        # Header
        lines.append("# Research Notebook / Experiment Registry Report\n")
        lines.append(
            f"> Generated: {now} | [!] Research Only | Backtest Only | "
            "No Real Orders | Production Trading: BLOCKED\n"
        )

        # Section 一: Overview
        lines.append("## 一、總覽\n")
        by_status = summary.get("by_status", {})
        lines.append(f"- **Total Experiments**: {summary.get('total', 0)}")
        lines.append(f"- **Completed**: {by_status.get('COMPLETED', 0)}")
        lines.append(f"- **Partial**: {by_status.get('PARTIAL', 0)}")
        lines.append(f"- **Failed**: {by_status.get('FAILED', 0)}")
        lines.append(f"- **Archived**: {by_status.get('ARCHIVED', 0)}")
        latest_id = summary.get("latest_experiment_id", "—")
        latest_at = summary.get("latest_created_at", "—")
        lines.append(f"- **Latest Experiment**: {latest_id} ({latest_at})")
        lines.append("- **Read Only**: True")
        lines.append("- **No Real Orders**: True")
        lines.append("- **Production BLOCKED**: True")
        lines.append("")

        # Section 二: Recent experiments table
        lines.append("## 二、最近 Experiments\n")
        if experiments:
            lines.append(
                "| Experiment ID | Name | Type | Mode | Profile | Status | Created At | Universe | Score Summary |"
            )
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for exp in experiments[:20]:
                eid = exp.get("experiment_id", "")
                name = _trunc(exp.get("experiment_name", ""), 24)
                etype = exp.get("experiment_type", "")
                mode = exp.get("mode", "")
                profile = exp.get("profile", "")
                status = exp.get("status", "")
                created_at = exp.get("created_at", "")[:19]
                universe = exp.get("universe_name", "")

                # Try to load snapshot score summary
                score_summary = self._get_score_summary(reg, eid)

                lines.append(
                    f"| {eid} | {name} | {etype} | {mode} | {profile} | "
                    f"{status} | {created_at} | {universe} | {score_summary} |"
                )
        else:
            lines.append("*No experiments registered yet.*")
        lines.append("")

        # Section 三: Quality coverage
        lines.append("## 三、Experiment Quality\n")
        dq_count = bt_count = rule_count = report_count = 0
        for exp in experiments:
            eid = exp.get("experiment_id", "")
            meta = self._try_load_meta(reg, eid)
            if meta:
                if "data_quality" in meta.snapshots:
                    dq_count += 1
                if "rule_governance" in meta.snapshots:
                    rule_count += 1
                if "backtest" in meta.snapshots:
                    bt_count += 1
                if meta.reports:
                    report_count += 1
        lines.append(f"- **Experiments with data quality snapshot**: {dq_count}")
        lines.append(f"- **Experiments with rule snapshot**: {rule_count}")
        lines.append(f"- **Experiments with backtest snapshot**: {bt_count}")
        lines.append(f"- **Experiments with reports**: {report_count}")
        lines.append("")

        # Section 四: Experiment comparison (latest vs previous)
        lines.append("## 四、Experiment Comparison\n")
        if len(experiments) >= 2:
            left_id = experiments[1].get("experiment_id", "")
            right_id = experiments[0].get("experiment_id", "")
            try:
                from experiments.experiment_comparator import ExperimentComparator
                comp = ExperimentComparator(
                    registry_root=os.path.relpath(self._registry_root, BASE_DIR)
                )
                result = comp.compare_two(left_id, right_id)
                lines.append(f"**Comparing**: `{left_id}` → `{right_id}`\n")
                lines.append(f"- **Overall Direction**: {result.get('overall_direction', '—')}")
                lines.append(f"- **Recommendation**: {result.get('recommendation', '—')}")
                lines.append("")

                # Score changes
                scores = result.get("scores", {})
                if scores:
                    lines.append("**Score Changes:**")
                    for field, vals in scores.items():
                        d = vals.get("direction", "—")
                        lv = vals.get("left_value")
                        rv = vals.get("right_value")
                        chg = vals.get("change")
                        lines.append(f"- {field}: {lv} → {rv} ({d}, Δ {chg})")
                    lines.append("")

                # Backtest changes
                backtest = result.get("backtest", {})
                if backtest:
                    lines.append("**Backtest Changes:**")
                    for field, vals in backtest.items():
                        d = vals.get("direction", "—")
                        lv = vals.get("left_value")
                        rv = vals.get("right_value")
                        lines.append(f"- {field}: {lv} → {rv} ({d})")
                    lines.append("")

                # Rule changes
                rules = result.get("rules", {})
                if rules:
                    lines.append("**Rule Changes:**")
                    for field, vals in rules.items():
                        d = vals.get("direction", "—")
                        lv = vals.get("left_value")
                        rv = vals.get("right_value")
                        lines.append(f"- {field}: {lv} → {rv} ({d})")
                    lines.append("")

                # Universe changes
                universe = result.get("universe", {})
                if universe:
                    lines.append("**Universe Changes:**")
                    for field, vals in universe.items():
                        d = vals.get("direction", "—")
                        lv = vals.get("left_value")
                        rv = vals.get("right_value")
                        lines.append(f"- {field}: {lv} → {rv} ({d})")
                    lines.append("")

            except Exception:
                logger.exception("Section 四 comparison failed")
                lines.append("*Comparison failed. Run experiment-compare manually.*\n")
        else:
            lines.append("*At least 2 experiments required for comparison.*\n")

        # Section 五: Research notes
        lines.append("## 五、Research Notes\n")
        latest_notes = self._load_latest_notes(experiments)
        lines.append(f"- **Open questions**: {latest_notes.get('open_questions', '—')}")
        lines.append(f"- **Blockers**: {latest_notes.get('blockers', '—')}")
        lines.append(f"- **Next actions**: {latest_notes.get('next_actions', '—')}")
        lines.append("")

        # Section 六: Safety declaration
        lines.append(_SAFETY_SECTION)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_score_summary(self, reg, experiment_id: str) -> str:
        """Return a brief score string for a registry table cell."""
        try:
            meta = reg.get_experiment(experiment_id)
            if meta is None:
                return "—"
            dq = meta.snapshots.get("data_quality", {}).get("summary", {})
            prod_score = dq.get("production_readiness_score")
            bt_score = dq.get("backtest_readiness_score")
            if prod_score is not None or bt_score is not None:
                return f"P:{prod_score} B:{bt_score}"
            return "—"
        except Exception:
            return "—"

    def _try_load_meta(self, reg, experiment_id: str):
        """Safely load metadata; return None on failure."""
        try:
            return reg.get_experiment(experiment_id)
        except Exception:
            return None

    def _load_latest_notes(self, experiments: list) -> dict:
        """Try to read notes.md from the latest experiment; return empty dict on failure."""
        try:
            if not experiments:
                return {}
            eid = experiments[0].get("experiment_id", "")
            notes_path = os.path.join(self._registry_root, eid, "notes.md")
            if not os.path.exists(notes_path):
                return {}
            with open(notes_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Simple heuristics: look for keywords
            result = {}
            for line in content.splitlines():
                ll = line.lower()
                if "open question" in ll or "question:" in ll:
                    result["open_questions"] = line.strip("- #* \t")
                elif "blocker" in ll:
                    result["blockers"] = line.strip("- #* \t")
                elif "next action" in ll or "next step" in ll:
                    result["next_actions"] = line.strip("- #* \t")
            return result
        except Exception:
            return {}


def _trunc(s: str, n: int) -> str:
    """Truncate string to n characters."""
    return (s[:n] + "…") if len(s) > n else s
