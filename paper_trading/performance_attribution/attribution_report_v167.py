"""
paper_trading/performance_attribution/attribution_report_v167.py
Attribution Report Engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 31 fixed sections. Read-only. Deterministic. Not for real trading.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

REPORT_SECTIONS = [
    "attribution_summary",
    "gross_vs_net_return",
    "realized_vs_unrealized",
    "active_return_decomposition",
    "selection_attribution",
    "allocation_attribution",
    "timing_attribution",
    "execution_attribution",
    "cost_attribution",
    "slippage_attribution",
    "turnover_attribution",
    "exposure_attribution",
    "risk_attribution",
    "drawdown_attribution",
    "regime_attribution",
    "benchmark_attribution",
    "factor_attribution",
    "strategy_attribution",
    "session_attribution",
    "symbol_attribution",
    "sector_attribution",
    "industry_attribution",
    "position_attribution",
    "trade_attribution",
    "portfolio_attribution",
    "reconciliation_status",
    "quality_scorecard",
    "top_bottom_contributors",
    "data_quality_summary",
    "disclaimer",
    "not_for_real_trading",
]
assert len(REPORT_SECTIONS) == 31


class AttributionReportEngine:
    """
    Generates 31-section attribution reports in Markdown, JSON, CSV, console, and GUI-model formats.
    Read-only. Deterministic. Never emits real-order fields.
    """

    def __init__(self, run_data: Optional[Dict[str, Any]] = None) -> None:
        self._run = run_data or {}
        self._paper_only = True
        self._research_only = True

    def _s(self, key: str) -> Any:
        return self._run.get(key, {})

    def _header(self) -> Dict[str, Any]:
        return {
            "run_id": self._run.get("run_id", ""),
            "portfolio_id": self._run.get("portfolio_id", ""),
            "period_start": self._run.get("period_start", ""),
            "period_end": self._run.get("period_end", ""),
            "status": self._run.get("status", "UNKNOWN"),
            "schema_version": self._run.get("schema_version", "167"),
            "policy_version": self._run.get("policy_version", "1.6.7-paper-attribution"),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "not_for_real_trading": True,
        }

    def build_section(self, section_name: str) -> Dict[str, Any]:
        """Return a single named section as a dict."""
        if section_name not in REPORT_SECTIONS:
            return {"error": f"unknown_section: {section_name}"}
        if not self._run:
            return {"section": section_name, "status": "EMPTY", "paper_only": True}

        if section_name == "attribution_summary":
            pa = self._s("portfolio_attribution")
            return {
                "section": "attribution_summary",
                "run_id": self._run.get("run_id", ""),
                "portfolio_id": self._run.get("portfolio_id", ""),
                "period_start": self._run.get("period_start", ""),
                "period_end": self._run.get("period_end", ""),
                "status": self._run.get("status", "UNKNOWN"),
                "active_return": pa.get("active_return") if pa else None,
                "gross_return": pa.get("gross_return") if pa else None,
                "net_return": pa.get("net_return") if pa else None,
                "confidence": pa.get("confidence", "UNKNOWN") if pa else "UNKNOWN",
                "reconciled": pa.get("reconciled") if pa else None,
                "paper_only": True,
            }

        if section_name == "gross_vs_net_return":
            pa = self._s("portfolio_attribution")
            return {
                "section": "gross_vs_net_return",
                "gross_return": pa.get("gross_return") if pa else None,
                "net_return": pa.get("net_return") if pa else None,
                "total_cost_pct": pa.get("total_cost_pct") if pa else None,
                "cost_bps": pa.get("cost_bps") if pa else None,
                "paper_only": True,
            }

        if section_name == "realized_vs_unrealized":
            pa = self._s("portfolio_attribution")
            return {
                "section": "realized_vs_unrealized",
                "realized_pnl": pa.get("realized_pnl") if pa else None,
                "unrealized_pnl": pa.get("unrealized_pnl") if pa else None,
                "total_pnl": pa.get("total_pnl") if pa else None,
                "paper_only": True,
            }

        if section_name == "active_return_decomposition":
            pa = self._s("portfolio_attribution")
            return {
                "section": "active_return_decomposition",
                "active_return": pa.get("active_return") if pa else None,
                "selection": pa.get("selection") if pa else None,
                "allocation": pa.get("allocation") if pa else None,
                "timing": pa.get("timing") if pa else None,
                "execution": pa.get("execution") if pa else None,
                "cost": pa.get("cost") if pa else None,
                "risk": pa.get("risk") if pa else None,
                "regime": pa.get("regime") if pa else None,
                "benchmark": pa.get("benchmark") if pa else None,
                "factor": pa.get("factor") if pa else None,
                "residual": pa.get("residual") if pa else None,
                "paper_only": True,
            }

        if section_name == "reconciliation_status":
            return {
                "section": "reconciliation_status",
                "reconciliation": self._s("reconciliation"),
                "paper_only": True,
            }

        if section_name == "quality_scorecard":
            return {
                "section": "quality_scorecard",
                "quality_score": self._s("quality_score"),
                "paper_only": True,
            }

        if section_name == "top_bottom_contributors":
            sym = self._s("symbol_attribution")
            if isinstance(sym, dict) and sym:
                sorted_items = sorted(
                    sym.items(),
                    key=lambda x: x[1].get("return", 0.0) if isinstance(x[1], dict) else 0.0,
                    reverse=True,
                )
                top5 = sorted_items[:5]
                bot5 = sorted_items[-5:][::-1]
            else:
                top5, bot5 = [], []
            return {
                "section": "top_bottom_contributors",
                "top_contributors": top5,
                "bottom_contributors": bot5,
                "paper_only": True,
            }

        if section_name == "data_quality_summary":
            return {
                "section": "data_quality_summary",
                "data_quality": self._run.get("data_quality", "UNKNOWN"),
                "missing_fields": self._run.get("missing_fields", []),
                "warnings": self._run.get("warnings", []),
                "paper_only": True,
            }

        if section_name == "disclaimer":
            return {
                "section": "disclaimer",
                "text": (
                    "This report is for paper/simulation research only. "
                    "It does not represent real trading results, real accounts, "
                    "or investment advice. All returns are simulated. "
                    "No broker. No real capital at risk."
                ),
                "paper_only": True,
                "research_only": True,
                "no_real_orders": True,
            }

        if section_name == "not_for_real_trading":
            return {
                "section": "not_for_real_trading",
                "warning": "NOT FOR REAL TRADING. PAPER RESEARCH ONLY.",
                "paper_only": True,
                "research_only": True,
                "no_real_orders": True,
                "not_for_production": True,
                "not_investment_advice": True,
            }

        # All other sections: return the stored sub-dict
        key_map = {
            "selection_attribution": "selection_attribution",
            "allocation_attribution": "allocation_attribution",
            "timing_attribution": "timing_attribution",
            "execution_attribution": "execution_attribution",
            "cost_attribution": "cost_attribution",
            "slippage_attribution": "slippage_attribution",
            "turnover_attribution": "turnover_attribution",
            "exposure_attribution": "exposure_attribution",
            "risk_attribution": "risk_attribution",
            "drawdown_attribution": "drawdown_attribution",
            "regime_attribution": "regime_attribution",
            "benchmark_attribution": "benchmark_attribution",
            "factor_attribution": "factor_attribution",
            "strategy_attribution": "strategy_attribution",
            "session_attribution": "session_attribution",
            "symbol_attribution": "symbol_attribution",
            "sector_attribution": "sector_attribution",
            "industry_attribution": "industry_attribution",
            "position_attribution": "position_attribution",
            "trade_attribution": "trade_attribution",
            "portfolio_attribution": "portfolio_attribution",
        }
        store_key = key_map.get(section_name, section_name)
        return {
            "section": section_name,
            "data": self._run.get(store_key, {"status": "EMPTY"}),
            "paper_only": True,
        }

    def build_all_sections(self) -> Dict[str, Any]:
        """Build all 31 sections."""
        sections = {}
        for s in REPORT_SECTIONS:
            sections[s] = self.build_section(s)
        return {
            "header": self._header(),
            "sections": sections,
            "section_count": len(sections),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    # ── Markdown output ───────────────────────────────────────────────────────

    def to_markdown(self, run_id: str = "") -> str:
        """Render all 31 sections as Markdown."""
        hdr = self._header()
        lines = [
            "# Paper Performance Attribution Report",
            "",
            "> [!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NOT INVESTMENT ADVICE.",
            "",
            f"**Run ID:** {hdr.get('run_id', run_id)}  ",
            f"**Portfolio:** {hdr.get('portfolio_id', '')}  ",
            f"**Period:** {hdr.get('period_start', '')} → {hdr.get('period_end', '')}  ",
            f"**Status:** {hdr.get('status', 'UNKNOWN')}  ",
            "",
        ]
        for i, section_name in enumerate(REPORT_SECTIONS, 1):
            sec = self.build_section(section_name)
            lines.append(f"## {i}. {section_name.replace('_', ' ').title()}")
            lines.append("")
            if "error" in sec:
                lines.append(f"*Error: {sec['error']}*")
            elif sec.get("status") == "EMPTY":
                lines.append("*No data available.*")
            elif section_name in ("disclaimer", "not_for_real_trading"):
                lines.append(sec.get("text") or sec.get("warning", ""))
            else:
                for k, v in sec.items():
                    if k in ("section", "paper_only", "research_only", "no_real_orders", "not_for_production"):
                        continue
                    lines.append(f"- **{k}:** {v}")
            lines.append("")
        return "\n".join(lines)

    # ── JSON output ───────────────────────────────────────────────────────────

    def to_json(self) -> str:
        """Render all 31 sections as JSON string."""
        report = self.build_all_sections()
        return json.dumps(report, default=str, sort_keys=True, indent=2)

    # ── CSV output ────────────────────────────────────────────────────────────

    def to_csv(self) -> str:
        """Render top-level attribution metrics as CSV."""
        hdr = self._header()
        pa = self._run.get("portfolio_attribution", {}) or {}
        header_row = (
            "run_id,portfolio_id,period_start,period_end,status,"
            "active_return,gross_return,net_return,total_cost_pct,"
            "reconciled,confidence,paper_only\n"
        )
        row = ",".join([
            str(hdr.get("run_id", "")),
            str(hdr.get("portfolio_id", "")),
            str(hdr.get("period_start", "")),
            str(hdr.get("period_end", "")),
            str(hdr.get("status", "")),
            str(pa.get("active_return", "")),
            str(pa.get("gross_return", "")),
            str(pa.get("net_return", "")),
            str(pa.get("total_cost_pct", "")),
            str(pa.get("reconciled", "")),
            str(pa.get("confidence", "")),
            "True",
        ])
        return header_row + row

    # ── Console summary output ────────────────────────────────────────────────

    def to_console(self) -> str:
        """Render a compact console summary."""
        hdr = self._header()
        pa = self._run.get("portfolio_attribution", {}) or {}
        qs = self._run.get("quality_score", {}) or {}
        lines = [
            "=" * 60,
            "PAPER ATTRIBUTION REPORT (Research Only)",
            "=" * 60,
            f"Run:       {hdr.get('run_id', 'N/A')}",
            f"Portfolio: {hdr.get('portfolio_id', 'N/A')}",
            f"Period:    {hdr.get('period_start', '')} → {hdr.get('period_end', '')}",
            f"Status:    {hdr.get('status', 'UNKNOWN')}",
            "-" * 60,
            f"Active Return:  {pa.get('active_return', 'N/A')}",
            f"Gross Return:   {pa.get('gross_return', 'N/A')}",
            f"Net Return:     {pa.get('net_return', 'N/A')}",
            f"Total Cost %:   {pa.get('total_cost_pct', 'N/A')}",
            f"Reconciled:     {pa.get('reconciled', 'N/A')}",
            f"Confidence:     {pa.get('confidence', 'UNKNOWN')}",
            "-" * 60,
            f"Quality Score:  {qs.get('total_score', 'N/A')}",
            f"Grade:          {qs.get('grade', 'N/A')}",
            "=" * 60,
            "NOT FOR REAL TRADING. PAPER RESEARCH ONLY.",
            "=" * 60,
        ]
        return "\n".join(lines)

    # ── GUI model output ──────────────────────────────────────────────────────

    def to_gui_model(self) -> Dict[str, Any]:
        """
        Return a headless-safe GUI model dict for rendering in the attribution panel.
        Structure: {tabs: [{tab_name, content}, ...]}
        """
        tabs = []
        for i, section_name in enumerate(REPORT_SECTIONS, 1):
            sec = self.build_section(section_name)
            tabs.append({
                "tab_index": i,
                "tab_name": section_name.replace("_", " ").title(),
                "section_key": section_name,
                "content": sec,
                "paper_only": True,
            })
        return {
            "report_type": "paper_attribution",
            "header": self._header(),
            "tabs": tabs,
            "tab_count": len(tabs),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "not_for_real_trading": True,
        }
