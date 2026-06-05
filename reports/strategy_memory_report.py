"""
reports/strategy_memory_report.py — StrategyMemoryReportBuilder v0.7.2

Generates a Markdown research memory report from StrategyMemoryStore outputs.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations
import os
import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_HEADER = (
    "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice"
)


class StrategyMemoryReportBuilder:
    """
    Builds a Markdown report from strategy memory data.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build(
        self,
        mode: str = "real",
        output_dir: str = "reports",
        memory_output_dir: str = "data/backtest_results/strategy_memory",
    ) -> str:
        """
        Generate strategy memory Markdown report.

        Returns path to generated report file.
        """
        # Resolve absolute paths
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        if not os.path.isabs(memory_output_dir):
            memory_output_dir = os.path.join(_BASE_DIR, memory_output_dir)

        os.makedirs(output_dir, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        out_path = os.path.join(output_dir, f"strategy_memory_report_{today}.md")

        # Load data
        memories = []
        links = []
        summary = None
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=memory_output_dir)
            memories = store.load_memories()
            links = store.load_links()
            summary = store.load_latest_summary()
        except Exception as exc:
            logger.warning("StrategyMemoryReportBuilder: load failed: %s", exc)

        lines = []

        # --- Section 1: Header ---
        lines += [
            f"# TW Quant Cockpit — Strategy Research Memory Report",
            f"",
            f"> **v0.7.2 | {today}**",
            f">",
            f"> {_SAFETY_HEADER}",
            f"",
            "---",
            "",
        ]

        # --- Section 2: 總覽 Overview ---
        lines += ["## 1. 總覽 (Overview)", ""]
        if summary:
            s = summary
            lines += [
                f"| Item | Value |",
                f"|------|-------|",
                f"| Total Memories | {s.total_memories} |",
                f"| Active | {s.active_count} |",
                f"| Archived | {s.archived_count} |",
                f"| New | {s.new_count} |",
                f"| Reviewing | {s.reviewing_count} |",
                f"| Validating | {s.validating_count} |",
                f"| Accepted | {s.accepted_count} |",
                f"| Rejected | {s.rejected_count} |",
                f"| Needs Evidence | {s.needs_more_evidence_count} |",
                f"| P0 | {s.p0_count} |",
                f"| P1 | {s.p1_count} |",
                f"| Duplicates | {s.duplicate_count} |",
                f"| Top Memory | {s.top_memory or '—'} |",
                f"| Overall Status | {s.overall_status} |",
                f"| Research Only | YES |",
                f"| No Real Orders | YES |",
                f"| Production BLOCKED | YES |",
                "",
            ]
        else:
            lines += [
                "_No summary available. Run: `python main.py strategy-memory --mode real`_",
                "",
            ]

        # --- Section 3: Memory Timeline ---
        lines += ["## 2. Memory Timeline", ""]
        active = [m for m in memories if not m.archived]
        timeline = sorted(active, key=lambda m: m.created_at, reverse=True)[:20]
        if timeline:
            lines += [
                f"| Memory ID | Type | Priority | Status | Title | Created |",
                f"|-----------|------|----------|--------|-------|---------|",
            ]
            for m in timeline:
                lines.append(
                    f"| {m.memory_id} | {m.memory_type[:20]} | {m.priority} | {m.status} "
                    f"| {m.title[:50]} | {m.created_at[:10]} |"
                )
            lines.append("")
        else:
            lines += ["_No memories in timeline._", ""]

        # --- Section 4: Top Active Memories ---
        lines += ["## 3. Top Active Memories", ""]
        from strategy_memory.strategy_memory_schema import PRIORITY_P0, PRIORITY_P1
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        top_mems = sorted(active, key=lambda m: (priority_order.get(m.priority, 9), m.created_at))[:10]
        for i, m in enumerate(top_mems, 1):
            lines += [
                f"### {i}. [{m.priority}] {m.title}",
                f"",
                f"- **Type:** {m.memory_type}",
                f"- **Status:** {m.status}",
                f"- **Source:** {m.source_module}",
                f"- **Confidence:** {m.confidence:.2f}",
                f"- **Seen:** {m.seen_count}x (last: {m.last_seen_at[:10]})",
                f"",
            ]
            if m.hypothesis:
                lines += [f"**Hypothesis:** {m.hypothesis}", ""]
            if m.evidence:
                lines += [f"**Evidence:** {m.evidence}", ""]
            if m.validation_plan:
                lines += [f"**Validation Plan:** {m.validation_plan}", ""]
            if m.suggested_commands:
                lines += [f"**Suggested Commands:**"]
                for cmd in m.suggested_commands:
                    lines.append(f"  - `{cmd}`")
                lines.append("")
            if m.risk_notes:
                lines += [f"**Risk Notes:** {m.risk_notes}", ""]
            lines.append("---")
            lines.append("")

        # --- Section 5: Rule / Strategy Memories ---
        lines += ["## 4. Rule / Strategy Memories", ""]
        from strategy_memory.strategy_memory_schema import (
            MEMORY_TYPE_RULE_CANDIDATE, MEMORY_TYPE_STRATEGY_HYPOTHESIS
        )
        rule_strat = [m for m in active if m.memory_type in (
            MEMORY_TYPE_RULE_CANDIDATE, MEMORY_TYPE_STRATEGY_HYPOTHESIS)]
        if rule_strat:
            lines += [
                "| Memory ID | Type | Priority | Status | Title |",
                "|-----------|------|----------|--------|-------|",
            ]
            for m in rule_strat:
                lines.append(
                    f"| {m.memory_id} | {m.memory_type} | {m.priority} | {m.status} | {m.title[:60]} |"
                )
            lines.append("")
        else:
            lines += ["_No rule/strategy memories._", ""]

        # --- Section 6: Replay / Journal Memories ---
        lines += ["## 5. Replay / Journal Memories", ""]
        from strategy_memory.strategy_memory_schema import (
            MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_JOURNAL_PATTERN
        )
        replay_journal = [m for m in active if m.memory_type in (
            MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_JOURNAL_PATTERN)]
        if replay_journal:
            lines += [
                "| Memory ID | Type | Priority | Status | Title |",
                "|-----------|------|----------|--------|-------|",
            ]
            for m in replay_journal:
                lines.append(
                    f"| {m.memory_id} | {m.memory_type} | {m.priority} | {m.status} | {m.title[:60]} |"
                )
            lines.append("")
        else:
            lines += ["_No replay/journal memories._", ""]

        # --- Section 7: Data / Report Gap Memories ---
        lines += ["## 6. Data / Report Gap Memories", ""]
        from strategy_memory.strategy_memory_schema import (
            MEMORY_TYPE_DATA_GAP, MEMORY_TYPE_REPORT_GAP,
            MEMORY_TYPE_PROVIDER_LIMITATION
        )
        gaps = [m for m in active if m.memory_type in (
            MEMORY_TYPE_DATA_GAP, MEMORY_TYPE_REPORT_GAP, MEMORY_TYPE_PROVIDER_LIMITATION)]
        if gaps:
            lines += [
                "| Memory ID | Type | Priority | Status | Title |",
                "|-----------|------|----------|--------|-------|",
            ]
            for m in gaps:
                lines.append(
                    f"| {m.memory_id} | {m.memory_type} | {m.priority} | {m.status} | {m.title[:60]} |"
                )
            lines.append("")
        else:
            lines += ["_No data/report gap memories._", ""]

        # --- Section 8: Memory Links ---
        lines += ["## 7. Memory Links", ""]
        if links:
            lines += [
                "| Link ID | Source | Relation | Target | Description |",
                "|---------|--------|----------|--------|-------------|",
            ]
            for lk in links[:30]:
                lines.append(
                    f"| {lk.link_id} | {lk.source_memory_id} | {lk.relation_type} "
                    f"| {lk.target_id[:20]} | {lk.description[:50]} |"
                )
            if len(links) > 30:
                lines.append(f"_... and {len(links) - 30} more links._")
            lines.append("")
        else:
            lines += ["_No links found._", ""]

        # --- Section 9: Safety ---
        lines += [
            "## 8. Safety",
            "",
            "| Safety Property | Value |",
            "|-----------------|-------|",
            "| Research Only | YES |",
            "| No Real Orders | YES |",
            "| Production Trading | BLOCKED |",
            "| Auto-Accept Memory | NO |",
            "| Auto-Reject Memory | NO |",
            "| Modify Rule Weights | NO |",
            "| Connect to Broker | NO |",
            "| Real Order Ready | NO |",
            "",
            "---",
            "",
            "_Generated by TW Quant Cockpit v0.7.2 — Strategy Research Memory._",
            "_[!] Research Only. No Real Orders. Production Trading BLOCKED._",
        ]

        content = "\n".join(lines) + "\n"
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("StrategyMemoryReportBuilder: report saved → %s", out_path)
        except Exception as exc:
            logger.error("StrategyMemoryReportBuilder: write failed: %s", exc)

        return out_path
