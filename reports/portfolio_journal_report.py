"""
reports/portfolio_journal_report.py — Portfolio Journal & Trade Review Report (v0.4.6).

Generates an 8-section Markdown report for the research-only portfolio journal.

Sections:
  1. 總覽 (Overview)
  2. Recent Journal Entries
  3. Signal vs Outcome
  4. Mistake Analysis
  5. Replay Training Notes
  6. Portfolio Review
  7. Action Items
  8. Safety Declaration

Output: reports/portfolio_journal_report_YYYY-MM-DD_HHMMSS.md  (gitignored)

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not investment advice. No broker order ID. No real execution fills.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PortfolioJournalReport:
    """
    Markdown report generator for Portfolio Journal & Trade Review (v0.4.6).

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, report_dir: str = "reports"):
        if os.path.isabs(report_dir):
            self._report_dir = report_dir
        else:
            self._report_dir = os.path.join(BASE_DIR, report_dir)
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(
        self,
        entries:         list,
        summary:         dict,
        signal_outcomes: Optional[dict] = None,
        replay_summary:  Optional[dict] = None,
        analytics:       Optional[dict] = None,
        mode:            str            = "real",
        dry_run:         bool           = False,
    ) -> str:
        """Generate and write the Markdown report. Returns path."""
        now      = datetime.now()
        ts       = now.strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_journal_report_{ts}.md"
        path     = os.path.join(self._report_dir, filename)

        sections = [
            self._section_overview(now, mode, summary),
            self._section_recent_entries(entries),
            self._section_signal_outcome(signal_outcomes or {}),
            self._section_mistake_analysis(analytics or {}, entries),
            self._section_replay_notes(replay_summary or {}),
            self._section_portfolio_review(summary, entries),
            self._section_action_items(summary, analytics or {}, signal_outcomes or {}),
            self._section_safety_declaration(),
        ]
        content = "\n\n".join(sections)

        if not dry_run:
            try:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
                logger.info("PortfolioJournalReport: written → %s", path)
            except Exception as exc:
                logger.warning("PortfolioJournalReport.generate: %s", exc)
        else:
            logger.info("PortfolioJournalReport: dry_run — not written")

        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_overview(self, now: datetime, mode: str, summary: dict) -> str:
        total   = summary.get("entries_count", 0)
        planned = summary.get("by_status", {}).get("PLANNED", 0)
        open_s  = summary.get("by_status", {}).get("OPEN_SIMULATED", 0)
        closed  = summary.get("closed_simulated_count", 0)
        reviewed = summary.get("reviewed_count", 0)
        review_req = summary.get("review_required_count", 0)
        latest  = summary.get("latest_entry_at", "—")
        return f"""# Portfolio Journal & Trade Review Report — v0.4.6

> **[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. No broker connection. No real execution fills.**
> **[!] Simulated / paper / replay / manual research notes only.**

| Field | Value |
|-------|-------|
| Generated | {now.strftime("%Y-%m-%d %H:%M:%S")} |
| Mode | {mode} |
| Version | v0.4.6 |
| Journal Only | True |
| No Real Orders | True |

## 一、總覽

| Metric | Value |
|--------|-------|
| Total Entries | {total} |
| Planned | {planned} |
| Open Simulated | {open_s} |
| Closed Simulated | {closed} |
| Reviewed | {reviewed} |
| Review Required | {review_req} |
| Latest Entry | {latest} |"""

    def _section_recent_entries(self, entries: list) -> str:
        recent = entries[:20]
        lines = ["## 二、Recent Journal Entries", ""]
        if not recent:
            lines.append("_No journal entries recorded._")
            return "\n".join(lines)
        lines += [
            "| Created | Symbol | Entry Type | Signal Source | Status | Outcome | Return % | Mistake Tags | Review? |",
            "|---------|--------|------------|---------------|--------|---------|----------|--------------|---------|",
        ]
        for e in recent:
            if hasattr(e, "to_dict"):
                d = e.to_dict()
            else:
                d = e
            created    = str(d.get("created_at", ""))[:10]
            symbol     = d.get("symbol", "—")
            etype      = d.get("entry_type", "")
            sig_src    = d.get("signal_source", "—")
            status     = d.get("status", "")
            outcome    = d.get("outcome_label", "—")
            ret        = d.get("actual_return_pct")
            ret_s      = f"{ret:.2f}%" if ret is not None else "—"
            mistakes   = "|".join(d.get("mistake_tags", [])) or "—"
            review_req = "Yes" if d.get("needs_review", False) or (
                status == "CLOSED_SIMULATED" and outcome == "UNKNOWN"
            ) else ""
            lines.append(
                f"| {created} | {symbol} | {etype} | {sig_src} | {status} | {outcome} "
                f"| {ret_s} | {mistakes} | {review_req} |"
            )
        if len(entries) > 20:
            lines.append(f"\n_Showing 20 most recent of {len(entries)} entries._")
        return "\n".join(lines)

    def _section_signal_outcome(self, signal_outcomes: dict) -> str:
        lines = ["## 三、Signal vs Outcome", ""]
        if not signal_outcomes or signal_outcomes.get("total", 0) == 0:
            lines.append("_No signal-linked entries with outcome data._")
            return "\n".join(lines)

        total    = signal_outcomes.get("total", 0)
        wins     = signal_outcomes.get("wins", 0)
        losses   = signal_outcomes.get("losses", 0)
        false_s  = signal_outcomes.get("false_signals", 0)
        win_rate = signal_outcomes.get("win_rate", 0)
        avg_ret  = signal_outcomes.get("avg_return_pct")
        avg_mfe  = signal_outcomes.get("avg_mfe")
        avg_mae  = signal_outcomes.get("avg_mae")
        review_r = signal_outcomes.get("review_required", 0)

        lines += [
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Signal-Linked Entries | {total} |",
            f"| Wins | {wins} |",
            f"| Losses | {losses} |",
            f"| False Signals | {false_s} |",
            f"| Win Rate | {win_rate:.1%} |",
            f"| Avg Return % | {f'{avg_ret:.2f}%' if avg_ret is not None else '—'} |",
            f"| Avg MFE | {f'{avg_mfe:.2f}%' if avg_mfe is not None else '—'} |",
            f"| Avg MAE | {f'{avg_mae:.2f}%' if avg_mae is not None else '—'} |",
            f"| Review Required | {review_r} |",
        ]

        outcomes = signal_outcomes.get("outcomes", [])
        if outcomes:
            lines += [
                "",
                "### Signal Outcome Detail",
                "",
                "| Symbol | Signal Source | Planned Entry | Actual Entry | Return % | Outcome | Process |",
                "|--------|--------------|---------------|--------------|----------|---------|---------|",
            ]
            for o in outcomes[:15]:
                lines.append(
                    f"| {o.get('symbol','')} "
                    f"| {o.get('signal_source','')} "
                    f"| {o.get('planned_entry') or '—'} "
                    f"| {o.get('actual_entry') or '—'} "
                    f"| {(str(round(o['return_pct'], 2)) + '%') if o.get('return_pct') is not None else '—'} "
                    f"| {o.get('outcome_label','')} "
                    f"| {o.get('process_quality','')} |"
                )
        return "\n".join(lines)

    def _section_mistake_analysis(self, analytics: dict, entries: list) -> str:
        lines = ["## 四、Mistake Analysis", ""]

        mistake_counts = {}
        for e in entries:
            tags = e.mistake_tags if hasattr(e, "mistake_tags") else e.get("mistake_tags", [])
            for t in tags:
                mistake_counts[t] = mistake_counts.get(t, 0) + 1

        if not mistake_counts:
            lines.append("_No mistake tags recorded._")
            return "\n".join(lines)

        lines += [
            "| Mistake Tag | Count | Severity | Category |",
            "|-------------|-------|----------|----------|",
        ]
        try:
            from journal.mistake_taxonomy import MistakeTaxonomy
            taxonomy = MistakeTaxonomy()
        except Exception:
            taxonomy = None

        for tag, count in sorted(mistake_counts.items(), key=lambda x: -x[1]):
            sev = taxonomy.severity(tag) if taxonomy else "—"
            cat = taxonomy.category(tag) if taxonomy else "—"
            lines.append(f"| {tag} | {count} | {sev} | {cat} |")

        by_mistake = analytics.get("by_mistake_tag", [])
        if by_mistake:
            lines += ["", "### Win Rate by Mistake Tag", "",
                      "| Mistake Tag | Count | Win Rate |",
                      "|-------------|-------|----------|"]
            for item in by_mistake[:10]:
                wr = item.get("win_rate")
                lines.append(
                    f"| {item['mistake_tag']} | {item['count']} "
                    f"| {f'{wr:.1%}' if wr is not None else '—'} |"
                )
        return "\n".join(lines)

    def _section_replay_notes(self, replay_summary: dict) -> str:
        lines = ["## 五、Replay Training Notes", ""]
        if not replay_summary or replay_summary.get("total_notes", 0) == 0:
            lines.append("_No replay training notes recorded._")
            return "\n".join(lines)

        total  = replay_summary.get("total_notes", 0)
        score  = replay_summary.get("avg_training_score")
        latest = replay_summary.get("latest_note_at", "—")
        focus  = replay_summary.get("most_common_mistakes", [])

        lines += [
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Replay Notes | {total} |",
            f"| Avg Training Score | {f'{score:.1f}/10' if score is not None else '—'} |",
            f"| Latest Note | {latest} |",
        ]
        if focus:
            lines += ["", "**Most Common Replay Mistakes:**"]
            for m in focus:
                lines.append(f"- {m}")
        mistake_counts = replay_summary.get("mistake_counts", {})
        if mistake_counts:
            lines += ["", "| Mistake | Count |", "|---------|-------|"]
            for m, c in sorted(mistake_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {m} | {c} |")
        return "\n".join(lines)

    def _section_portfolio_review(self, summary: dict, entries: list) -> str:
        lines = ["## 六、Portfolio Review", ""]
        by_outcome = summary.get("by_outcome", {})
        by_status  = summary.get("by_status", {})

        lines += [
            "### Simulated Positions",
            "",
            "| Status | Count |",
            "|--------|-------|",
        ]
        for s, c in sorted(by_status.items(), key=lambda x: -x[1]):
            lines.append(f"| {s} | {c} |")

        if by_outcome:
            lines += ["", "### Outcome Distribution", "",
                      "| Outcome | Count |", "|---------|-------|"]
            for o, c in sorted(by_outcome.items(), key=lambda x: -x[1]):
                lines.append(f"| {o} | {c} |")

        # Sector / symbol concentration
        symbols = {}
        for e in entries:
            sym = e.symbol if hasattr(e, "symbol") else e.get("symbol", "")
            if sym:
                symbols[sym] = symbols.get(sym, 0) + 1
        if symbols:
            top_symbols = sorted(symbols.items(), key=lambda x: -x[1])[:10]
            lines += ["", "### Symbol Concentration (Top 10)", "",
                      "| Symbol | Entry Count |", "|--------|------------|"]
            for sym, cnt in top_symbols:
                lines.append(f"| {sym} | {cnt} |")

        return "\n".join(lines)

    def _section_action_items(
        self,
        summary: dict,
        analytics: dict,
        signal_outcomes: dict,
    ) -> str:
        lines = ["## 七、Action Items", ""]
        items = []

        review_req = summary.get("review_required_count", 0)
        if review_req > 0:
            items.append(f"Review {review_req} closed simulated entries awaiting outcome review")

        mistakes = analytics.get("most_common_mistakes", [])
        if mistakes:
            items.append(f"Study most common mistakes: {', '.join(mistakes[:3])}")

        if signal_outcomes.get("false_signals", 0) >= 2:
            items.append(
                f"Validate signal source for {signal_outcomes['false_signals']} false signals"
            )

        worst_process = analytics.get("worst_process_tags", [])
        if worst_process:
            items.append(f"Review rule governance for: {', '.join(worst_process[:3])}")

        if not items:
            items.append("No immediate action items — continue journaling and reviewing entries")

        for item in items:
            lines.append(f"- {item}")

        return "\n".join(lines)

    def _section_safety_declaration(self) -> str:
        return """## 八、安全聲明

> **[!] Journal Only** — This report records research notes only.
> **[!] Research Only** — No investment recommendations are made.
> **[!] No Real Orders** — No broker connection. No order submission.
> **[!] Not Investment Advice** — Not a solicitation to buy or sell.
> **[!] Production Trading BLOCKED** — REAL_ORDER_READY=False.
> **[!] Simulation only** — All entries are simulated / paper / replay / manual notes.

---

_Portfolio Journal & Trade Review v0.4.6 — Journal Only. Research Only. No Real Orders._"""
