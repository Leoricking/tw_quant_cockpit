"""
experiments/experiment_notebook.py — ExperimentNotebookBuilder: generate markdown notebooks (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import datetime
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_FOOTER = """\
## 十、安全聲明

- Research Only: True
- Backtest Only: True
- No Real Orders: True
- Production Trading: BLOCKED
- Auto Weight Application: DISABLED
- Real Order Execution: BLOCKED
"""


class ExperimentNotebookBuilder:
    """
    Builds markdown research notebooks for individual experiments.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, registry_root: str = "experiments"):
        self._registry_root = os.path.join(BASE_DIR, registry_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_notebook(self, experiment_id: str) -> str:
        """
        Build notebook.md for the given experiment_id.
        Returns the absolute path to the written file.
        """
        try:
            content = self.build_summary_markdown(experiment_id)
            nb_path = os.path.join(self._registry_root, experiment_id, "notebook.md")
            os.makedirs(os.path.dirname(nb_path), exist_ok=True)
            with open(nb_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Notebook written to %s", nb_path)
            return nb_path
        except Exception:
            logger.exception("build_notebook failed for %s", experiment_id)
            return ""

    def append_note(self, experiment_id: str, note: str) -> bool:
        """Append a free-text note to notes.md for the given experiment."""
        try:
            notes_path = os.path.join(self._registry_root, experiment_id, "notes.md")
            os.makedirs(os.path.dirname(notes_path), exist_ok=True)
            timestamp = datetime.datetime.now().isoformat()
            with open(notes_path, "a", encoding="utf-8") as f:
                f.write(f"\n---\n**{timestamp}**\n\n{note}\n")
            logger.info("Note appended to %s", notes_path)
            return True
        except Exception:
            logger.exception("append_note failed for %s", experiment_id)
            return False

    def build_summary_markdown(self, experiment_id: str) -> str:
        """
        Build and return notebook markdown content (does not write to disk).
        """
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(
                registry_root=os.path.relpath(self._registry_root, BASE_DIR)
            )
            meta = reg.get_experiment(experiment_id)
            if meta is None:
                return f"# Experiment Not Found: {experiment_id}\n\n[!] No metadata available.\n"

            return self._render_notebook(meta)

        except Exception:
            logger.exception("build_summary_markdown failed for %s", experiment_id)
            return f"# Experiment Notebook: {experiment_id}\n\n[Error generating notebook]\n"

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _render_notebook(self, meta) -> str:
        """Render the full notebook markdown from ExperimentMetadata."""
        lines = []

        # Title and safety banner
        lines.append(f"# Experiment Notebook: {meta.experiment_id}\n")
        lines.append(
            "> [!] Research Only. Backtest Only. No Real Orders. Production Trading: BLOCKED.\n"
        )

        # Section 一: Basic info
        lines.append("## 一、基本資訊\n")
        lines.append(f"- **Experiment ID**: {meta.experiment_id}")
        lines.append(f"- **Name**: {meta.experiment_name or '—'}")
        lines.append(f"- **Type**: {meta.experiment_type}")
        lines.append(f"- **Mode**: {meta.mode}")
        lines.append(f"- **Profile**: {meta.profile}")
        lines.append(f"- **Status**: {meta.status}")
        lines.append(f"- **Created At**: {meta.created_at}")
        lines.append(f"- **Git Commit**: {meta.git_commit or '—'}")
        lines.append(f"- **Git Tag**: {meta.git_tag or '—'}")
        lines.append(f"- **Source Command**: `{meta.source_command or '—'}`")
        if meta.tags:
            lines.append(f"- **Tags**: {', '.join(meta.tags)}")
        if meta.universe_name:
            lines.append(f"- **Universe**: {meta.universe_name}")
        lines.append("")

        # Section 二: Research purpose / notes
        lines.append("## 二、研究目的\n")
        lines.append(meta.notes if meta.notes else "No notes recorded.")
        lines.append("")

        # Section 三: Data quality snapshot
        lines.append("## 三、Data Quality Snapshot\n")
        lines.append(self._render_snapshot_section(meta, "data_quality"))

        # Section 四: Universe snapshot
        lines.append("## 四、Universe Snapshot\n")
        lines.append(self._render_snapshot_section(meta, "universe"))

        # Section 五: Rule snapshot
        lines.append("## 五、Rule Snapshot\n")
        lines.append(self._render_snapshot_section(meta, "rule_governance"))

        # Section 六: Backtest snapshot
        lines.append("## 六、Backtest Snapshot\n")
        lines.append(self._render_snapshot_section(meta, "backtest"))

        # Section 七: Generated reports
        lines.append("## 七、Generated Reports\n")
        self._render_reports_section(meta, lines)
        lines.append("")

        # Section 八: Observations (placeholder)
        lines.append("## 八、Observation\n")
        lines.append("*(Add observations here)*\n")

        # Section 九: Next actions (placeholder)
        lines.append("## 九、Next Action\n")
        lines.append("*(Add next actions here)*\n")

        # Section 十: Safety declaration
        lines.append(_SAFETY_FOOTER)

        return "\n".join(lines)

    def _render_snapshot_section(self, meta, snap_type: str) -> str:
        """Render a snapshot summary block, or a 'Not available' message."""
        try:
            snap_ref = meta.snapshots.get(snap_type)
            if not snap_ref:
                return "Not available.\n"

            summary = snap_ref.get("summary", {})
            generated_at = snap_ref.get("generated_at", "")
            path = snap_ref.get("path", "")

            out = []
            if generated_at:
                out.append(f"- **Generated At**: {generated_at}")
            if path:
                out.append(f"- **Path**: `{path}`")

            if summary:
                out.append("- **Summary**:")
                for k, v in summary.items():
                    if isinstance(v, list):
                        out.append(f"  - {k}: {', '.join(str(x) for x in v[:10])}")
                    elif isinstance(v, dict):
                        out.append(f"  - {k}: {v}")
                    else:
                        out.append(f"  - {k}: {v}")
            else:
                out.append("- (no summary data)")

            return "\n".join(out) + "\n"

        except Exception:
            logger.exception("_render_snapshot_section failed for %s", snap_type)
            return "Not available.\n"

    def _render_reports_section(self, meta, lines: list) -> None:
        """Append report list to the lines buffer."""
        try:
            if not meta.reports:
                lines.append("No reports linked.\n")
                return
            for rep in meta.reports:
                name = rep.get("name", "—")
                path = rep.get("path", "")
                generated_at = rep.get("generated_at", "")
                summary = rep.get("summary", "")
                entry = f"- **{name}**"
                if path:
                    entry += f" — `{path}`"
                if generated_at:
                    entry += f" ({generated_at})"
                if summary:
                    entry += f"\n  - {summary}"
                lines.append(entry)
        except Exception:
            logger.exception("_render_reports_section failed")
            lines.append("Not available.\n")
