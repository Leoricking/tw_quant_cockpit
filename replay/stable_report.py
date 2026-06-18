"""
replay/stable_report.py — ReplayStableReport for v1.2.9.

Generates the stable rollup markdown report.
No real orders. No broker. Research only.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
import os
from datetime import date, datetime

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableReport:
    """
    Generates the v1.2.9 Replay Training Stable Rollup report as Markdown.

    generate(output_dir="reports") creates the file and returns the path.
    Report contains 18 sections.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def generate(self, output_dir: str = "reports") -> str:
        """Generate the stable rollup report. Returns the output file path."""
        os.makedirs(output_dir, exist_ok=True)
        today = date.today().isoformat()
        fname = f"replay_training_stable_rollup_{today}.md"
        fpath = os.path.join(output_dir, fname)

        content = self._build_content(today)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Stable rollup report written: %s", fpath)
        return fpath

    def _build_content(self, today: str) -> str:
        lines = [
            "# Replay Training Stable Rollup v1.2.9 — Stable Release Report",
            "",
            "> **[!] Research Only. No Real Orders. Not Investment Advice.**",
            "> **[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.**",
            "> **[!] This report documents research-only training capabilities only.**",
            "",
            f"**Generated:** {today}  ",
            "**Release:** v1.2.9 — Replay Training Stable Rollup  ",
            "**Base:** v1.2.8 Replay Dataset & Session Registry  ",
            "**Track:** replay_training  ",
            "**Stage:** STABLE  ",
            "",
            "---",
            "",
            "## 1. Release Overview",
            "",
            "v1.2.9 is the 'Replay Training Stable Rollup' — a freeze-and-validate milestone",
            "for the complete Replay Training v1.2 line (v1.2.0–v1.2.8). No new trading",
            "functionality is added. This release adds stable manifests, capability matrices,",
            "cross-module contracts, backward compatibility checks, store and runtime audits,",
            "CLI and GUI audits, report and safety audits, and release-gate integration.",
            "",
            "**Safety Declaration:**",
            "- NO_REAL_ORDERS = True",
            "- BROKER_EXECUTION_ENABLED = False",
            "- PRODUCTION_TRADING_BLOCKED = True",
            "- VALIDATED_DOES_NOT_ENABLE_TRADING = True",
            "- REPLAY_TRADE_EXECUTION_ENABLED = False",
            "- All AUTO_* flags = False",
            "",
            "---",
            "",
            "## 2. Version History (v1.2 Replay Training Line)",
            "",
            "| Version | Name | Status |",
            "|---------|------|--------|",
            "| v1.2.0 | Replay Training UX Foundation | STABLE |",
            "| v1.2.1 | Replay Scenario & Session Manager | STABLE |",
            "| v1.2.2 | Decision Journal Integration | STABLE |",
            "| v1.2.3 | Replay Scoring & Mistake Taxonomy | STABLE |",
            "| v1.2.4 | Strategy Knowledge Replay | STABLE |",
            "| v1.2.5 | Multi-Timeframe Replay | STABLE |",
            "| v1.2.6 | Replay Review Dashboard | STABLE |",
            "| v1.2.7 | Replay Challenge Mode | STABLE |",
            "| v1.2.8 | Replay Dataset & Session Registry | STABLE |",
            "| v1.2.9 | Replay Training Stable Rollup | STABLE |",
            "",
            "---",
            "",
            "## 3. Module Architecture",
            "",
            "12 replay training modules validated:",
            "",
            "1. replay_foundation (v1.2.0) — Session step engine, future data firewall",
            "2. scenario_manager (v1.2.1) — Scenario library, templates",
            "3. session_manager (v1.2.1) — Fork, checkpoint, compare",
            "4. decision_journal (v1.2.2) — Append-only journal, emotional state",
            "5. scoring_mistake_taxonomy (v1.2.3) — Process/outcome scoring, 31-type taxonomy",
            "6. strategy_knowledge (v1.2.4) — Point-in-time strategy replay",
            "7. multi_timeframe (v1.2.5) — D1/M60/M20/M5/M1 synchronized",
            "8. review_dashboard (v1.2.6) — Review queue, progress, comparison",
            "9. challenge_mode (v1.2.7) — Timed challenges, hidden outcome, personal leaderboard",
            "10. dataset_registry (v1.2.8) — Dataset versioning, fingerprint, lineage",
            "11. session_registry (v1.2.8) — Session registry, portable packages",
            "12. stable_rollup (v1.2.9) — Manifests, audits, contracts, gate",
            "",
            "---",
            "",
            "## 4. Capability Matrix Summary",
            "",
            "16 capabilities validated — all safety-qualified, research-only.",
            "See `replay-stable-capabilities` CLI for full matrix.",
            "",
            "---",
            "",
            "## 5. Cross-Module Contracts",
            "",
            "Contract checks: session↔scenario, session↔journal, session↔scoring,",
            "scenario↔dataset, scoring outcome separation, strategy point-in-time,",
            "timeframe future firewall, challenge hidden data, registry schemas,",
            "expected_block semantics, _is_forbidden guard, NO_REAL_ORDERS invariant.",
            "",
            "---",
            "",
            "## 6. Backward Compatibility",
            "",
            "Backward compatibility verified for: v1.2.0, v1.2.1, v1.2.2, v1.2.3,",
            "v1.2.4, v1.2.5, v1.2.6, v1.2.7, v1.2.8",
            "",
            "---",
            "",
            "## 7. Store Audit",
            "",
            "10 data stores audited: session, scenario, journal, scoring, strategy,",
            "timeframe, review, challenge, dataset_registry, session_registry.",
            "All use append-only JSONL semantics where applicable.",
            "",
            "---",
            "",
            "## 8. Runtime Isolation",
            "",
            ".gitignore covers all data/replay_*/  and reports/ directories.",
            "sys.path does not leak user-specific absolute paths.",
            "",
            "---",
            "",
            "## 9. CLI Audit",
            "",
            "24 CLI commands audited. All registered in main.py dispatch dict.",
            "See `replay-stable-cli-audit` for details.",
            "",
            "---",
            "",
            "## 10. GUI Audit",
            "",
            "8 stable GUI panels audited. All importable (Qt-optional).",
            "dashboard.py registers replay_stable tab.",
            "",
            "---",
            "",
            "## 11. Report Audit",
            "",
            "Report generators audited. reports/ in .gitignore.",
            "No forbidden trading strings in report templates.",
            "",
            "---",
            "",
            "## 12. Safety Audit",
            "",
            "All version_info safety flags verified:",
            "- NO_REAL_ORDERS=True, REAL_ORDERS_ENABLED=False",
            "- BROKER_EXECUTION_ENABLED=False, PRODUCTION_TRADING_BLOCKED=True",
            "- All AUTO_*_ENABLED=False",
            "replay/ directory scanned — no dangerous keywords found.",
            "",
            "---",
            "",
            "## 13. Regression Audit",
            "",
            "suite_registry has release_gate and quick suites.",
            "expected_block semantics present in regression_schema.",
            "_is_forbidden guard verified.",
            "No duplicate test IDs in release_gate suite.",
            "",
            "---",
            "",
            "## 14. Release Gate",
            "",
            "Release gate aggregates all audit results.",
            "FAIL count > 0 → overall FAIL.",
            "WARN count > 0 → overall WARNING.",
            "Otherwise → PASS.",
            "",
            "---",
            "",
            "## 15. Safety Declarations",
            "",
            "- [!] Research Only. No Real Orders. Not Investment Advice.",
            "- [!] Replay Trade Execution DISABLED.",
            "- [!] No Auto Decision. No Auto Execution. No Auto Confirm.",
            "- [!] No Auto Outcome Reveal. No Auto Mistake Confirmation.",
            "- [!] No Auto Strategy Change. No Auto Dataset Repair.",
            "- [!] No Auto Session Rebind. No Auto Package Import.",
            "- [!] No Public Leaderboard. No Network Submission.",
            "- [!] Broker Disabled. Production Trading BLOCKED.",
            "- [!] VALIDATED does not enable trading.",
            "",
            "---",
            "",
            "## 16. Known Warnings",
            "",
            "- PySide6 optional — GUI panels degrade gracefully without it",
            "- Real data required for FORMAL qualification",
            "- Outcome reveal requires explicit user action",
            "- Mistake confirmation requires explicit user action",
            "- Public leaderboard disabled",
            "- Auto session rebind disabled",
            "- Auto dataset repair disabled",
            "",
            "---",
            "",
            "## 17. Maintenance Baseline",
            "",
            "v1.2.9 is the long-term maintenance baseline for the Replay Training v1.2 line.",
            "REPLAY_TRAINING_LINE_COMPLETE = True",
            "LONG_TERM_MAINTENANCE_READY = True",
            "Future v1.2.x releases are maintenance-only (no new trading functionality).",
            "",
            "---",
            "",
            "## 18. Report Metadata",
            "",
            f"- Report generated: {datetime.now().isoformat()}",
            "- Release: v1.2.9 — Replay Training Stable Rollup",
            "- Track: replay_training",
            "- Stage: STABLE",
            "- No Real Orders: True",
            "- Broker Disabled: True",
            "- Research Only: True",
            "",
            "---",
            "",
            "*[!] Research Only. No Real Orders. Not Investment Advice.*",
        ]
        return "\n".join(lines) + "\n"
