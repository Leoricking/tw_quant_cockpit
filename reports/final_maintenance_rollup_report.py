"""
reports/final_maintenance_rollup_report.py — Final Maintenance Rollup Report for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class FinalMaintenanceRollupReportBuilder:
    """Builds the Final Maintenance Rollup Markdown report.

    [!] Research Only. No Real Orders. Not Investment Advice.
    Output: reports/final_maintenance_rollup_report_YYYY-MM-DD.md
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    def __init__(
        self,
        mode: str = "real",
        output_dir: Optional[str] = None,
        project_root: Optional[str] = None,
    ) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._output_dir = output_dir or os.path.join(self._root, "reports")
        self.mode = mode
        os.makedirs(self._output_dir, exist_ok=True)

    def build(self) -> str:
        """Build the report and return the Markdown content."""
        from final_rollup.final_rollup_engine import FinalRollupEngine
        engine = FinalRollupEngine(project_root=self._root, mode=self.mode)
        history = engine.build_release_history()
        checks, health_summary = engine.run_final_health()
        smoke = engine.build_smoke_summary()
        plan = engine.build_maintenance_plan()

        today = datetime.now().strftime("%Y-%m-%d")
        lines = []

        # Header
        lines.append(f"# Final Maintenance Rollup Report v1.0.9")
        lines.append(f"")
        lines.append(f"> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**")
        lines.append(f"> **[!] VALIDATED does not enable trading. Not Investment Advice.**")
        lines.append(f"> **[!] No external API. Broker Execution Disabled.**")
        lines.append(f"")
        lines.append(f"Generated: {today}")
        lines.append(f"")

        # 一、總覽
        lines.append(f"## 一、總覽")
        lines.append(f"")
        lines.append(f"| Item | Value |")
        lines.append(f"|------|-------|")
        lines.append(f"| Version | 1.0.9 |")
        lines.append(f"| Release | Final Maintenance Rollup |")
        lines.append(f"| Research Only | True |")
        lines.append(f"| No Real Orders | True |")
        lines.append(f"| Production Trading BLOCKED | True |")
        lines.append(f"| Broker Execution Disabled | True |")
        lines.append(f"| External API Disabled | True |")
        lines.append(f"| v1.0 Maintenance Line Complete | True |")
        lines.append(f"| Long-term Maintenance Ready | True |")
        lines.append(f"")

        # 二、v1.0.x Release History
        lines.append(f"## 二、v1.0.x Release History")
        lines.append(f"")
        lines.append(f"| Version | Title | Commit | Tag | Status |")
        lines.append(f"|---------|-------|--------|-----|--------|")
        for entry in history:
            lines.append(
                f"| {entry.version} | {entry.title} | `{entry.commit}` | `{entry.tag}` | {entry.safety_status} |"
            )
        lines.append(f"")

        # 三、Final Health Check
        lines.append(f"## 三、Final Health Check")
        lines.append(f"")
        pass_count    = health_summary.get("pass_count", 0)
        warn_count    = health_summary.get("warn_count", 0)
        fail_count    = health_summary.get("fail_count", 0)
        blocked_count = health_summary.get("blocked_count", 0)
        overall       = health_summary.get("overall_status", "UNKNOWN")
        lines.append(f"**Overall: {overall}** | PASS: {pass_count} | WARN: {warn_count} | FAIL: {fail_count} | BLOCKED: {blocked_count}")
        lines.append(f"")
        lines.append(f"| Check | Category | Status | Detail |")
        lines.append(f"|-------|----------|--------|--------|")
        for c in checks:
            detail = (c.get("detail") or "")[:80]
            lines.append(f"| {c.get('name','')} | {c.get('category','')} | **{c.get('status','')}** | {detail} |")
        lines.append(f"")
        known_warnings = [c for c in checks if c.get("status") == "WARN"]
        if known_warnings:
            lines.append(f"**Known Warnings ({len(known_warnings)}):**")
            for w in known_warnings:
                lines.append(f"- [{w.get('category','')}] {w.get('name','')}: {(w.get('detail') or '')[:80]}")
            lines.append(f"")

        # 四、Final Smoke Summary
        lines.append(f"## 四、Final Smoke Summary")
        lines.append(f"")
        lines.append(f"| Suite | Status | Note |")
        lines.append(f"|-------|--------|------|")
        for r in smoke:
            lines.append(f"| {r.get('suite','')} | **{r.get('status','')}** | {r.get('note','')[:80]} |")
        lines.append(f"")

        # 五、System Coverage
        lines.append(f"## 五、System Coverage")
        lines.append(f"")
        coverage_items = [
            ("Stable release", "v1.0.0 Research Trading Cockpit Stable"),
            ("Maintenance", "v1.0.1 Maintenance & Polish"),
            ("Data hygiene", "v1.0.2 Data & Report Hygiene"),
            ("GUI stability", "v1.0.3 GUI Stability & Usability Polish"),
            ("Regression hardening", "v1.0.4 Regression & Release Gate Hardening"),
            ("Documentation", "v1.0.5 Documentation & User Guide Polish"),
            ("Examples/templates", "v1.0.6 Example Workflows & Templates"),
            ("Knowledge base", "v1.0.7 Knowledge Base Search Polish"),
            ("Local assistant", "v1.0.8 Local Research Assistant Polish"),
            ("Final rollup", "v1.0.9 Final Maintenance Rollup"),
        ]
        lines.append(f"| Area | Release |")
        lines.append(f"|------|---------|")
        for area, release in coverage_items:
            lines.append(f"| {area} | {release} |")
        lines.append(f"")

        # 六、Long-term Maintenance Plan
        lines.append(f"## 六、Long-term Maintenance Plan")
        lines.append(f"")
        from final_rollup.rollup_schema import (
            CADENCE_DAILY, CADENCE_WEEKLY, CADENCE_MONTHLY, CADENCE_RELEASE, CADENCE_INCIDENT
        )
        for cadence in [CADENCE_DAILY, CADENCE_WEEKLY, CADENCE_MONTHLY, CADENCE_RELEASE, CADENCE_INCIDENT]:
            cadence_tasks = [t for t in plan if t.cadence == cadence]
            if cadence_tasks:
                lines.append(f"### {cadence}")
                lines.append(f"")
                lines.append(f"| Task | Command | Expected | Safe Action |")
                lines.append(f"|------|---------|----------|-------------|")
                for t in cadence_tasks:
                    lines.append(f"| {t.title} | `{t.command}` | {t.expected_result} | {t.safe_action} |")
                lines.append(f"")

        # 七、Known Warnings
        lines.append(f"## 七、Known Warnings")
        lines.append(f"")
        lines.append(f"- Paper smoke test: may show KNOWN_WARNING for missing data (simulation only)")
        lines.append(f"- no_real_orders safety guard: BLOCKED if broker command attempted (expected behavior)")
        lines.append(f"- mock-realtime: simulation only, no real market data")
        lines.append(f"")

        # 八、What Not To Do
        lines.append(f"## 八、What Not To Do")
        lines.append(f"")
        lines.append(f"- **No broker API** — do not connect to Shioaji, Mega Broker, or any broker")
        lines.append(f"- **No auto trading** — this system never places real orders")
        lines.append(f"- **No real orders** — all trading outputs are BLOCKED")
        lines.append(f"- **No strategy auto-enabling** — VALIDATED status does not enable trading")
        lines.append(f"- **No tag moving** — do not move existing git tags")
        lines.append(f"- **No runtime output commit** — CSV/MD outputs in data/ and reports/ are not committed")
        lines.append(f"")

        # 九、結論
        lines.append(f"## 九、結論")
        lines.append(f"")
        lines.append(f"- v1.0.x maintenance line complete (v1.0.0 through v1.0.9)")
        lines.append(f"- Ready for long-term maintenance under current SOP")
        lines.append(f"- Next major (optional): **v1.1.0 Data Universe Expansion**")
        lines.append(f"- v1.2.0 Replay Training UX (future)")
        lines.append(f"- v1.3.0 Research Notebook / Journal Intelligence (future)")
        lines.append(f"- Do not proceed to broker API without explicit planning")
        lines.append(f"")

        # 十、安全聲明
        lines.append(f"## 十、安全聲明")
        lines.append(f"")
        lines.append(f"- **No Real Orders** — this system does not place any real orders")
        lines.append(f"- **No broker execution** — Broker Execution Disabled")
        lines.append(f"- **No auto trading** — Auto trading is not implemented")
        lines.append(f"- **Not Investment Advice** — all outputs are for research only")
        lines.append(f"- **VALIDATED does not enable trading** — validation is research status only")
        lines.append(f"- **Paper trading is simulation only**")
        lines.append(f"- **Mock realtime is simulation only**")
        lines.append(f"- **No external API** — no OpenAI, Claude API, embedding API, or external vector DB")
        lines.append(f"")

        return "\n".join(lines)

    def save(self) -> str:
        """Build and save the report. Returns the file path."""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"final_maintenance_rollup_report_{today}.md"
        path = os.path.join(self._output_dir, filename)
        content = self.build()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("Saved final maintenance rollup report to %s", path)
        return path
