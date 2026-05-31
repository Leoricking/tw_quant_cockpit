"""
reports/universe_expansion_report.py - Universe Expansion Report builder (v0.3.25).

Generates: reports/universe_expansion_report_YYYY-MM-DD.md

[!] Research Only. Not investment advice. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UniverseExpansionReportBuilder:
    """
    Builds the Universe Expansion & Sector Classification report.

    Parameters
    ----------
    report_date   : YYYY-MM-DD string
    universe_data : dict from UniverseQualityAnalyzer.run()
    registry_data : dict from UniverseRegistry.list_universes()
    expansion_data: dict from UniverseExpander.propose_expansion()
    classifier_data: dict from SectorClassifier.get_sector_summary()
    """

    def __init__(
        self,
        report_date:    Optional[str] = None,
        universe_data:  Optional[dict] = None,
        registry_data:  Optional[list] = None,
        expansion_data: Optional[dict] = None,
        classifier_data: Optional[dict] = None,
        mode: str = "real",
    ):
        self.report_date     = report_date or datetime.now().strftime("%Y-%m-%d")
        self.universe_data   = universe_data  or {}
        self.registry_data   = registry_data  or []
        self.expansion_data  = expansion_data or {}
        self.classifier_data = classifier_data or {}
        self.mode            = mode

    def build(self, output_dir: Optional[str] = None) -> str:
        out_dir = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)
        fname = f"universe_expansion_report_{self.report_date}.md"
        fpath = os.path.join(out_dir, fname)

        lines: List[str] = []
        lines += self._header()
        lines += self._section_overview()
        lines += self._section_universe_list()
        lines += self._section_sector_distribution()
        lines += self._section_universe_quality()
        lines += self._section_expansion_candidates()
        lines += self._section_weaknesses()
        lines += self._section_recommendations()
        lines += self._section_safety()

        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            logger.info("Universe expansion report written: %s", fpath)
        except Exception as exc:
            logger.error("Cannot write report: %s", exc)
        return fpath

    def _header(self) -> List[str]:
        uname = self.universe_data.get("universe_name", "?")
        return [
            "# Universe Expansion & Sector Classification Report",
            "",
            f"> Date: {self.report_date}  |  Universe: {uname}  |  Mode: {self.mode.upper()}  |  v0.3.25",
            "> **[!] Research Only | No Real Orders | Not Investment Advice**",
            "",
        ]

    def _section_overview(self) -> List[str]:
        ud = self.universe_data
        total_universes = len(self.registry_data)
        configured = sum(1 for u in self.registry_data if u.get("exists", False))
        return [
            "## 一、總覽",
            "",
            "| Item | Value |",
            "|---|---|",
            f"| Mode | {self.mode.upper()} |",
            f"| Read Only | Yes |",
            f"| No Real Orders | Yes |",
            f"| Production BLOCKED | Yes |",
            f"| Universe Groups | {total_universes} |",
            f"| Configured | {configured} |",
            f"| Target Universe | {ud.get('universe_name', '?')} ({ud.get('symbol_count', 0)} symbols) |",
            f"| Overall Universe Readiness | {ud.get('overall_universe_score', 'N/A')} ({ud.get('readiness_level', 'N/A')}) |",
            "",
        ]

    def _section_universe_list(self) -> List[str]:
        lines = [
            "## 二、Universe List",
            "",
            "| Universe | Symbol Count | Readiness | Note |",
            "|---|---|---|---|",
        ]
        for u in self.registry_data:
            note = "" if u.get("exists") else "Not yet built — run universe-build-defaults"
            lines.append(f"| {u['name']} | {u['symbol_count']} | {u['readiness']} | {note} |")
        lines.append("")
        return lines

    def _section_sector_distribution(self) -> List[str]:
        cd = self.classifier_data
        if not cd:
            return ["## 三、Sector / Theme Distribution", "", "*No sector data available.*", ""]
        lines = [
            "## 三、Sector / Theme Distribution",
            "",
            f"- Total Symbols: **{cd.get('total', 0)}**",
            f"- Top Sector: **{cd.get('top_sector', '?')}**",
            f"- Concentration: **{cd.get('concentration', 0):.1%}**",
            "",
            "| Sector | Count |",
            "|---|---|",
        ]
        for sec, cnt in sorted(cd.get("by_sector", {}).items(), key=lambda x: -x[1]):
            lines.append(f"| {sec} | {cnt} |")
        lines.append("")
        return lines

    def _section_universe_quality(self) -> List[str]:
        ud = self.universe_data
        if not ud:
            return ["## 四、Universe Quality", "", "*No quality data.*", ""]
        return [
            "## 四、Universe Quality",
            "",
            "| Dimension | Score |",
            "|---|---|",
            f"| Coverage | {ud.get('coverage_score', 'N/A')} |",
            f"| Freshness | {ud.get('freshness_score', 'N/A')} |",
            f"| Provider Reliability | {ud.get('provider_reliability_score', 'N/A')} |",
            f"| Sector Balance | {ud.get('sector_balance_score', 'N/A')} |",
            f"| Liquidity Readiness | {ud.get('liquidity_readiness_score', 'N/A')} |",
            f"| Backtest Sample Readiness | {ud.get('backtest_sample_readiness_score', 'N/A')} |",
            f"| **Overall** | **{ud.get('overall_universe_score', 'N/A')} ({ud.get('readiness_level', 'N/A')})** |",
            "",
        ]

    def _section_expansion_candidates(self) -> List[str]:
        ed = self.expansion_data
        candidates = ed.get("candidates", [])
        if not candidates:
            return ["## 五、Expansion Candidates", "", "*No candidates available.*", ""]
        lines = [
            "## 五、Expansion Candidates",
            "",
            f"Source: {ed.get('source_universe', '?')} ({ed.get('source_size', 0)} symbols) -> Target: {ed.get('target_size', 0)}",
            "",
            "| Symbol | Name | Sector | Theme | Data Coverage | Liquidity | Reason |",
            "|---|---|---|---|---|---|---|",
        ]
        for c in candidates[:20]:
            lines.append(
                f"| {c['symbol']} | {c['name']} | {c['sector']} | {c['theme_primary']} "
                f"| {c['data_coverage']} | {c['liquidity_tier']} | {c['reason']} |"
            )
        lines.append("")
        return lines

    def _section_weaknesses(self) -> List[str]:
        ud = self.universe_data
        missing = ud.get("missing_symbols", [])
        weak_sec = ud.get("weak_sectors", [])
        lines = ["## 六、Weakness / Blockers", ""]
        if missing:
            lines.append(f"- **Missing data** for {len(missing)} symbols: {missing[:5]}")
        if weak_sec:
            lines.append(f"- **Weak sectors** (< 5% representation): {weak_sec}")
        if ud.get("symbol_count", 0) < 30:
            lines.append(f"- **Insufficient symbols** ({ud.get('symbol_count', 0)} < 30) — max OBSERVATIONAL level")
        if not missing and not weak_sec:
            lines.append("*No critical blockers identified.*")
        lines.append("")
        return lines

    def _section_recommendations(self) -> List[str]:
        lines = ["## 七、Recommendations", ""]
        for rec in self.universe_data.get("recommendations", []):
            lines.append(f"- {rec}")
        lines += [
            "- Run `python main.py universe-build-defaults` to create all universe configs",
            "- Run `python main.py provider-auto-fetch` to fill missing data",
            "- Research universe is for simulation only — not for production trading",
            "",
        ]
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 八、安全聲明",
            "",
            "- **Research Only** — for research and simulation, not for trading decisions",
            "- **No Real Orders** — `no_real_orders=True`",
            "- **No Auto Trading** — system does not place or execute trades",
            "- **No Auto Weight Changes** — rule weights are not modified automatically",
            "- **Not Investment Advice** — this universe is a research tool only",
            "- **Production Trading: BLOCKED** — `REAL_ORDER_READY=False`",
            "",
        ]
