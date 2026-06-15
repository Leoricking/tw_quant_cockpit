"""
reports.data_governance_operations_report — DataGovernanceOperationsReportBuilder v1.1.6

Generates governance operations Markdown report.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Dashboard does NOT repair/download/override/enable trading. Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataGovernanceOperationsReportBuilder:
    """
    Builds Data Governance Operations Report v1.1.6 as a Markdown file.

    [!] Research Only. No Real Orders.
    [!] Not Investment Advice.
    """

    def build(self, tier: str = "research30", mode: str = "real",
              output_dir: str = "reports") -> str:
        """
        Generate reports/data_governance_operations_report_YYYY-MM-DD.md
        Returns path to generated report.
        """
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"data_governance_operations_report_{today}.md")

        # Run governance engine
        summary = None
        actions = []
        module_statuses = {}
        symbol_statuses = []
        runs = []

        try:
            from governance_ops.operations_engine import DataGovernanceOperationsEngine
            engine = DataGovernanceOperationsEngine()
            summary = engine.run(mode=mode, tier=tier)
            module_statuses = engine.build_module_health()
            symbol_statuses = engine.build_symbol_matrix(tier=tier)
            actions = engine.build_action_queue_from_data(symbol_statuses, module_statuses)
            runs = engine.build_run_audit_summary()
        except Exception as exc:
            logger.warning("DataGovernanceOperationsReportBuilder: engine error: %s", exc)

        lines = self._build_report(
            summary=summary,
            module_statuses=module_statuses,
            symbol_statuses=symbol_statuses,
            actions=actions,
            runs=runs,
            tier=tier,
            mode=mode,
            today=today,
        )

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            logger.info("DataGovernanceOperationsReportBuilder: report saved to %s", output_path)
        except Exception as exc:
            logger.warning("DataGovernanceOperationsReportBuilder: write error: %s", exc)

        return output_path

    def _build_report(self, summary, module_statuses, symbol_statuses, actions, runs,
                      tier, mode, today) -> List[str]:
        lines = []

        # Section 1: Title
        lines.append("# Data Governance Operations Report v1.1.6")
        lines.append("")
        lines.append(f"**Generated:** {today}")
        lines.append(f"**Tier:** {tier}  |  **Mode:** {mode}")
        lines.append("")

        # Section 2: Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("| ----- | ----- |")
        lines.append("| Version | 1.1.6 |")
        lines.append("| Research Only | True |")
        lines.append("| No Real Orders | True |")
        lines.append(f"| Mode | {mode} |")
        lines.append(f"| Tier | {tier} |")

        if summary:
            lines.append(f"| Overall Status | {summary.overall_status} |")
            lines.append(f"| Confidence | {summary.confidence:.0%} |")
            lines.append(f"| Generated At | {summary.generated_at} |")
            lines.append(f"| Registered Symbols | {summary.registered_symbols} |")
            lines.append(f"| Ready Symbols | {summary.ready_symbols} |")
            lines.append(f"| Formal Eligible | {summary.formal_eligible} |")
            lines.append(f"| P0 Actions | {summary.p0_actions} |")
            lines.append(f"| P1 Actions | {summary.p1_actions} |")
            lines.append(f"| Source Interruptions | {summary.source_interruptions} |")
            lines.append(f"| Audit Chain Failures | {summary.audit_chain_failures} |")
        else:
            lines.append("| Overall Status | UNKNOWN — engine not available |")
        lines.append("")

        # Section 3: Module Health
        lines.append("## Module Health")
        lines.append("")
        lines.append("| Module | Available | Status | PASS | WARN | FAIL | Version |")
        lines.append("| ------ | --------- | ------ | ---- | ---- | ---- | ------- |")

        module_list = [
            "UNIVERSE", "ONBOARDING", "COVERAGE_REPAIR", "FRESHNESS",
            "QUALITY_GATES", "GATE_ENFORCEMENT", "REPORT_PACK", "SYSTEM_HEALTH",
        ]
        for mod_name in module_list:
            mod = module_statuses.get(mod_name)
            if mod:
                lines.append(
                    f"| {mod.module_name} | {mod.available} | {mod.health_status} | "
                    f"{mod.pass_count} | {mod.warn_count} | {mod.fail_count} | {mod.version} |"
                )
            else:
                lines.append(f"| {mod_name} | UNAVAILABLE | UNAVAILABLE | - | - | - | - |")
        lines.append("")

        # Section 4: Universe Status
        lines.append("## Universe Status")
        lines.append("")
        if summary:
            lines.append(f"- Registered: {summary.registered_symbols}")
            lines.append(f"- Evaluated: {summary.evaluated_symbols}")
            lines.append(f"- Ready: {summary.ready_symbols}")
            lines.append(f"- Partial: {summary.partial_symbols}")
            lines.append(f"- Stale: {summary.stale_symbols}")
            lines.append(f"- Missing: {summary.missing_symbols}")
        else:
            lines.append("- Universe data unavailable (run governance-dashboard first)")
        lines.append("")

        # Section 5: Quality Gate Status
        lines.append("## Quality Gate Status")
        lines.append("")
        if summary:
            lines.append(f"- Formal Eligible: {summary.formal_eligible}")
            lines.append(f"- Observational Eligible: {summary.observational_eligible}")
            lines.append(f"- Demo Only: {summary.demo_only}")
            lines.append(f"- Blocked: {summary.blocked_symbols}")
        else:
            lines.append("- Quality gate data unavailable")
        lines.append("")

        # Section 6: Freshness & Source Health
        lines.append("## Freshness & Source Health")
        lines.append("")
        if summary:
            lines.append(f"- Stale/Delayed: {summary.stale_symbols}")
            lines.append(f"- Source Interruptions: {summary.source_interruptions}")
            lines.append("")
            lines.append("> **Calendar Approximation Warning:** Freshness uses Mon-Fri calendar.")
            lines.append("> Public holidays are not excluded. Verify actual trading calendar.")
        else:
            lines.append("- Freshness data unavailable")
        lines.append("")

        # Section 7: Import & Repair
        lines.append("## Import & Repair")
        lines.append("")
        if symbol_statuses:
            total_repair = sum(s.open_repair_issues for s in symbol_statuses)
            total_conflict = sum(s.conflict_count for s in symbol_statuses)
            total_invalid = sum(s.invalid_count for s in symbol_statuses)
            total_manual = sum(s.manual_review_count for s in symbol_statuses)
            total_import_fail = sum(s.import_failure_count for s in symbol_statuses)
            lines.append(f"- Open Repair Tasks: {total_repair}")
            lines.append(f"- Conflicts: {total_conflict}")
            lines.append(f"- Invalid Records: {total_invalid}")
            lines.append(f"- Manual Review Required: {total_manual}")
            lines.append(f"- Import Failures: {total_import_fail}")
        else:
            lines.append("- Import/repair data unavailable (run governance-dashboard first)")
        lines.append("")

        # Section 8: Gate Enforcement & Audit
        lines.append("## Gate Enforcement & Audit")
        lines.append("")
        if summary:
            lines.append(f"- Non-qualified Runs: {summary.non_qualified_runs}")
            lines.append(f"- Audit Chain Failures: {summary.audit_chain_failures}")
        lines.append(f"- Recent Runs: {len(runs)}")
        lines.append("")

        # Section 9: Priority Action Queue
        lines.append("## Priority Action Queue")
        lines.append("")
        p0 = [a for a in actions if a.priority == "P0"]
        p1 = [a for a in actions if a.priority == "P1"]
        p2 = [a for a in actions if a.priority == "P2"]
        p3 = [a for a in actions if a.priority == "P3"]

        for priority, action_list in [("P0", p0), ("P1", p1), ("P2", p2), ("P3", p3)]:
            lines.append(f"### {priority} Actions ({len(action_list)})")
            lines.append("")
            if action_list:
                lines.append("| Symbol/Source | Issue | Reason | Safe Action | Command | Status |")
                lines.append("| ------------- | ----- | ------ | ----------- | ------- | ------ |")
                for action in action_list[:10]:
                    sym = action.symbol or action.source or "(system)"
                    reason = ", ".join(action.reason_codes[:2]) if action.reason_codes else ""
                    cmd = action.suggested_command[:50] if action.suggested_command else ""
                    lines.append(
                        f"| {sym} | {action.title[:40]} | {reason} | "
                        f"{action.safe_action} | `{cmd}` | {action.status} |"
                    )
            else:
                lines.append(f"_No {priority} actions._")
            lines.append("")

        # Section 10: Symbol Matrix
        lines.append("## Symbol Matrix")
        lines.append("")
        if symbol_statuses:
            lines.append("| Symbol | Tier | Coverage | Freshness | Gate | Qualification | Repair | Priority |")
            lines.append("| ------ | ---- | -------- | --------- | ---- | ------------- | ------ | -------- |")
            for s in symbol_statuses[:30]:
                lines.append(
                    f"| {s.symbol} | {s.tier} | {s.coverage_status} | {s.freshness_status} | "
                    f"{s.quality_gate_level[:15]} | {s.qualification} | {s.open_repair_issues} | {s.priority} |"
                )
        else:
            lines.append("_No symbol data available. Run governance-dashboard first._")
        lines.append("")

        # Section 11: Safe Next Steps
        lines.append("## Safe Next Steps")
        lines.append("")
        next_steps = [
            "REVIEW: `python main.py governance-health` — Check all module health",
            "READ_REPORT: `python main.py governance-module-health` — View module status",
            "READ_REPORT: `python main.py governance-actions` — View action queue",
            "READ_REPORT: `python main.py governance-top-actions --limit 10` — View top actions",
        ]
        if p0:
            next_steps.insert(0, f"VERIFY_AUDIT: `python main.py governance-audit-summary` — {len(p0)} P0 actions require immediate attention")
        for step in next_steps:
            lines.append(f"- {step}")
        lines.append("")

        # Section 12: Safety Declaration (Chinese)
        lines.append("## 安全聲明 / Safety Declaration")
        lines.append("")
        lines.append("- **No Real Orders:** This dashboard is research-only. No real orders are placed.")
        lines.append("- **Broker Execution Disabled:** No broker API connection. No order submission.")
        lines.append("- **Dashboard does NOT:** auto-repair data, auto-download data, override quality gates, or enable trading.")
        lines.append("- **Not Investment Advice:** All outputs are for research and analysis only.")
        lines.append("- **VALIDATED does not mean tradable.** Research acceptance is not trading authorization.")
        lines.append("")
        lines.append("本儀表板僅供研究用途。不構成投資建議。無實盤下單。不接券商。不自動修復資料。")
        lines.append("不自動下載資料。不覆蓋品質門檻。不啟用交易。")
        lines.append("")

        return lines
