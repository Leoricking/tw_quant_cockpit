"""
reports/replay_mistake_taxonomy_report.py — Mistake taxonomy report for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayMistakeTaxonomyReport:
    """
    Builds mistake taxonomy reference report.
    [!] Research Only. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._reports_dir = os.path.join(self._repo_root, "reports")
        os.makedirs(self._reports_dir, exist_ok=True)

    def build(self) -> str:
        from replay.mistake_taxonomy import MistakeTaxonomy, MISTAKE_CATEGORY_MAP

        lines = [
            "# Replay Mistake Taxonomy Reference v1.2.3",
            "",
            "> [!] Research Only. No Real Orders. Simulation Training Only.",
            "> [!] WAIT/SKIP with good rationale is NOT a mistake.",
            "> [!] Planned stop is NOT PANIC_SELL. Planned reduce is NOT EXITED_TOO_EARLY.",
            "> [!] Single loss != mistake. Single profit != good decision.",
            "> [!] Emotional types: self-reported or rule-triggered only. NOT psychological diagnosis.",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
        ]

        # Group by category
        from replay.mistake_taxonomy import MistakeCategory
        categories = [
            MistakeCategory.ENTRY, MistakeCategory.EXIT,
            MistakeCategory.RISK, MistakeCategory.PROCESS,
            MistakeCategory.EMOTIONAL, MistakeCategory.DATA,
            MistakeCategory.OTHER,
        ]

        for cat in categories:
            types = MistakeTaxonomy.list_by_category(cat)
            if not types:
                continue
            lines.append(f"## {cat}")
            lines.append("")
            for mtype in types:
                desc = MistakeTaxonomy.get_description(mtype)
                is_emotional = MistakeTaxonomy.is_emotional(mtype)
                lines.append(f"### {mtype}")
                lines.append(f"{desc}")
                if is_emotional:
                    lines.append("> [!] Self-reported or rule-triggered only. NOT psychological diagnosis.")
                lines.append("")

        lines += [
            "---",
            "*[!] Research Only | No Real Orders | Not Investment Advice*",
        ]
        return "\n".join(lines)

    def save(self) -> str:
        content = self.build()
        ts = datetime.now(timezone.utc).strftime("%Y%m%d")
        path = os.path.join(self._reports_dir, f"replay_mistake_taxonomy_report_{ts}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
