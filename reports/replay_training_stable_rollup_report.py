"""
reports/replay_training_stable_rollup_report.py — ReplayTrainingStableRollupReport v1.2.9

Generates the Replay Training Stable Rollup markdown report.
Delegates to replay.stable_report.ReplayStableReport for the actual content.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTrainingStableRollupReport:
    """
    Generates the Replay Training Stable Rollup report.

    generate(output_dir="reports") creates the markdown report and returns path.
    Safety statements included throughout.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def generate(self, output_dir: str = "reports") -> str:
        """Generate the stable rollup report. Returns the output file path."""
        try:
            from replay.stable_report import ReplayStableReport
            report = ReplayStableReport()
            return report.generate(output_dir=output_dir)
        except Exception as exc:
            logger.error("ReplayStableReport unavailable: %s", exc)
            # Fallback: write minimal report
            os.makedirs(output_dir, exist_ok=True)
            from datetime import date
            today = date.today().isoformat()
            fname = f"replay_training_stable_rollup_{today}.md"
            fpath = os.path.join(output_dir, fname)
            content = (
                "# Replay Training Stable Rollup v1.2.9\n\n"
                "> [!] Research Only. No Real Orders. Not Investment Advice.\n\n"
                f"Report generation error: {exc}\n"
                "\n[!] Research Only. Not Investment Advice.\n"
            )
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            return fpath
