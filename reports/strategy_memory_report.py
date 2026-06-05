"""
reports/strategy_memory_report.py — StrategyMemoryReportBuilder v0.8.1

Generates a Markdown research memory report from StrategyMemoryStore outputs.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice.
[!] ACCEPTED status = research conclusion accepted. NOT a trading signal.
"""
from __future__ import annotations
import os
import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_HEADER = (
    "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice  "
    "|  ACCEPTED = Research Finding Only, NOT a trading signal"
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

        # Helpers
        from strategy_memory.memory_query import StrategyMemoryQuery
        from strategy_memory.strategy_memory_schema import (
            PRIORITY_P0, PRIORITY_P1,
            MEMORY_TYPE_RULE_CANDIDATE, MEMORY_TYPE_STRATEGY_HYPOTHESIS,
            MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_JOURNAL_PATTERN,
            MEMORY_TYPE_DATA_GAP, MEMORY_TYPE_REPORT_GAP,
            MEMORY_TYPE_PROVIDER_LIMITATION,
        )

        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        active = [m for m in memories if not m.archived]
        top_mems = sorted(active, key=lambda m: (priority_order.get(m.priority, 9), m.created_at))

        # Compute today focus
        today_focus = ""
        focus_mem = None
        for m in top_mems:
            if m.status in ("NEW", "REVIEWING", "VALIDATING", "NEEDS_MORE_EVIDENCE"):
                today_focus = m.title
                focus_mem = m
                break

        # --- Section 1: Header ---
        lines += [
            f"# TW Quant Cockpit — Strategy Research Memory Report v0.8.1",
            f"",
            f"> **v0.8.1 | {today}**",
            f">",
            f"> {_SAFETY_HEADER}",
            f"",
            "---",
            "",
        ]

        # --- Section 2: Today Memory Focus ---
        lines += ["## 1. Today Memory Focus", ""]
        if focus_mem:
            lines += [
                f"**Top Memory:** {focus_mem.title}",
                f"",
                f"- **Priority:** {focus_mem.priority}",
                f"- **Status:** {focus_mem.status}",
                f"- **Type:** {focus_mem.memory_type}",
                f"- **Source:** {focus_mem.source_module}",
                f"- **Why it matters:** {focus_mem.summary[:120] or 'See evidence below.'}",
                f"",
            ]
            if focus_mem.suggested_commands:
                lines += [f"**Suggested Safe Command:** `{focus_mem.suggested_commands[0]}`", ""]
            else:
                lines += [f"**Suggested Safe Command:** `python main.py strategy-memory-summary`", ""]
        else:
            lines += ["_No active memories found._", ""]
        lines += ["---", ""]

        # --- Section 3: Memory Status Board ---
        lines += ["## 2. Memory Status Board", ""]
        if summary:
            s = summary
            lines += [
                f"| Status | Count |",
                f"|--------|-------|",
                f"| NEW | {s.new_count} |",
                f"| REVIEWING | {s.reviewing_count} |",
                f"| VALIDATING | {s.validating_count} |",
                f"| ACCEPTED | {s.accepted_count} — *research only, not trading* |",
                f"| REJECTED | {s.rejected_count} |",
                f"| NEEDS_MORE_EVIDENCE | {s.needs_more_evidence_count} |",
                f"| ARCHIVED | {s.archived_count} |",
                f"| **Total** | **{s.total_memories}** |",
                f"| P0 | {s.p0_count} |",
                f"| P1 | {s.p1_count} |",
                f"| Research Only | YES |",
                f"| No Real Orders | YES |",
                "",
            ]
        else:
            lines += ["_No summary available. Run: `python main.py strategy-memory --mode real`_", ""]
        lines += ["---", ""]

        # --- Section 4: Active Research Threads ---
        lines += ["## 3. Active Research Threads", ""]
        type_groups = {
            "Strategy Hypotheses": MEMORY_TYPE_STRATEGY_HYPOTHESIS,
            "Rule Candidates": MEMORY_TYPE_RULE_CANDIDATE,
            "Replay Mistakes": MEMORY_TYPE_REPLAY_MISTAKE_PATTERN,
            "Journal Patterns": MEMORY_TYPE_JOURNAL_PATTERN,
            "Data Gaps": MEMORY_TYPE_DATA_GAP,
        }
        for group_name, mtype in type_groups.items():
            group_mems = [m for m in active if m.memory_type == mtype and m.status not in ("ARCHIVED", "REJECTED")]
            if group_mems:
                lines += [f"### {group_name} ({len(group_mems)})", ""]
                lines += ["| ID | Priority | Status | Title | Seen |", "|-----|----------|--------|-------|------|"]
                for m in group_mems[:8]:
                    lines.append(f"| {m.memory_id} | {m.priority} | {m.status} | {m.title[:50]} | {m.seen_count} |")
                lines.append("")
        lines += ["---", ""]

        # --- Section 5: Validation Queue ---
        lines += ["## 4. Validation Queue", ""]
        val_queue = [m for m in active if
                     m.status in ("VALIDATING", "REVIEWING") or
                     (m.validation_plan and m.status in ("NEW", "REVIEWING"))]
        val_queue = sorted(val_queue, key=lambda m: priority_order.get(m.priority, 9))
        if val_queue:
            lines += ["| ID | Priority | Status | Title | Validation Plan | Suggested Command |",
                      "|----|----------|--------|-------|-----------------|-------------------|"]
            for m in val_queue[:10]:
                vp = (m.validation_plan or "—")[:60]
                cmd = m.suggested_commands[0] if m.suggested_commands else "—"
                lines.append(f"| {m.memory_id} | {m.priority} | {m.status} | {m.title[:45]} | {vp} | `{cmd[:50]}` |")
            lines.append("")
        else:
            lines += ["_No memories in validation queue._", ""]
        lines += ["---", ""]

        # --- Section 6: Repeated Patterns ---
        lines += ["## 5. Repeated Patterns", ""]
        repeated = sorted([m for m in active if m.seen_count > 1], key=lambda m: m.seen_count, reverse=True)
        if repeated:
            lines += ["| Title | Seen | Source | Priority | Next Step |",
                      "|-------|------|--------|----------|-----------|"]
            for m in repeated[:10]:
                nxt = m.next_step or (m.suggested_commands[0] if m.suggested_commands else "—")
                lines.append(f"| {m.title[:50]} | {m.seen_count} | {m.source_module} | {m.priority} | `{nxt[:50]}` |")
            lines.append("")
        else:
            lines += ["_No repeated patterns found._", ""]
        lines += ["---", ""]

        # --- Section 7: Memory Links ---
        lines += ["## 6. Memory Links", ""]
        if links:
            lines += [
                "| Relation | Source | Target | Why Linked |",
                "|----------|--------|--------|------------|",
            ]
            for lk in links[:30]:
                why = getattr(lk, "why_linked", "") or lk.description[:50]
                lines.append(
                    f"| {lk.relation_type} | {lk.source_memory_id} "
                    f"| {getattr(lk, 'target_title', None) or lk.target_id[:20]} | {why[:60]} |"
                )
            if len(links) > 30:
                lines.append(f"_... and {len(links) - 30} more links._")
            lines.append("")
        else:
            lines += ["_No links found._", ""]
        lines += ["---", ""]

        # --- Section 8: Suggested Safe Commands ---
        lines += ["## 7. Suggested Safe Commands", ""]
        safe_cmd_rows = []
        for m in top_mems[:5]:
            for cmd in m.suggested_commands[:2]:
                label = "SAFE_READ_ONLY"
                if "report" in cmd:
                    label = "SAFE_REPORT"
                elif "regression" in cmd:
                    label = "SAFE_REGRESSION"
                elif "replay" in cmd:
                    label = "SAFE_REPLAY"
                elif "data" in cmd:
                    label = "SAFE_DATA_CHECK"
                safe_cmd_rows.append((cmd, label, m.title[:40]))
        if safe_cmd_rows:
            lines += ["| Command | Safety Label | Purpose |", "|---------|--------------|---------|"]
            for cmd, label, purpose in safe_cmd_rows[:10]:
                lines.append(f"| `{cmd[:60]}` | {label} | {purpose} |")
            lines.append("")
        else:
            lines += ["_No suggested commands found in active memories._", ""]
        lines += ["---", ""]

        # --- Section 9: What Not To Do ---
        lines += [
            "## 8. What Not To Do",
            "",
            "- Do NOT interpret ACCEPTED status as a signal to enable or run a trading strategy.",
            "- Do NOT auto-execute any suggested command — all commands are research-only safe reads.",
            "- Do NOT connect memory outputs to broker APIs — this system has no broker connection.",
            "- Do NOT treat memory counts or priorities as real-money position sizing signals.",
            "",
            "---",
            "",
        ]

        # --- Section 10: Safety Declaration ---
        lines += [
            "## 9. Safety Declaration",
            "",
            "| Safety Property | Value |",
            "|-----------------|-------|",
            "| Research Only | YES |",
            "| No Real Orders | YES |",
            "| Production Trading | BLOCKED |",
            "| ACCEPTED = Trading Enabled | NO — ACCEPTED means research finding only |",
            "| Auto-Accept Memory | NO |",
            "| Auto-Reject Memory | NO |",
            "| Modify Rule Weights | NO |",
            "| Connect to Broker | NO |",
            "| Real Order Ready | NO |",
            "",
            "---",
            "",
            "_Generated by TW Quant Cockpit v0.8.1 — Strategy Research Memory._",
            "_[!] Research Only. No Real Orders. Production Trading BLOCKED. Not Investment Advice._",
        ]

        content = "\n".join(lines) + "\n"
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("StrategyMemoryReportBuilder: report saved → %s", out_path)
        except Exception as exc:
            logger.error("StrategyMemoryReportBuilder: write failed: %s", exc)

        return out_path
