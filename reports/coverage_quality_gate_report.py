"""
reports/coverage_quality_gate_report.py — CoverageQualityGateReportBuilder v1.1.4

Builds Markdown report for a Coverage Quality Gate evaluation session.

[!] Research Only. No Real Orders. Coverage Quality Gate does NOT enable trading.
[!] VALIDATED status does NOT enable trading or broker execution.
[!] Mock data cannot pass formal gate.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level safety constants — must remain True at all times
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
PRODUCTION_TRADING_BLOCKED = True
QUALITY_GATE_DOES_NOT_ENABLE_TRADING = True
VALIDATED_DOES_NOT_ENABLE_TRADING = True
MOCK_FORMAL_GATE_DISABLED = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageQualityGateReportBuilder:
    """Builds a Markdown Coverage Quality Gates report.

    [!] Research Only. No Real Orders.
    [!] Coverage Quality Gate does NOT enable trading.
    [!] VALIDATED does NOT enable trading.
    """

    research_only = True
    no_real_orders = True
    gate_does_not_enable_trading = True

    # Gate decision levels
    FORMAL = "FORMAL"
    OBSERVATIONAL = "OBSERVATIONAL"
    DEMO = "DEMO"
    BLOCKED = "BLOCKED"

    def build(
        self,
        decisions: List[Dict[str, Any]],
        universe_summary: Dict[str, Any],
        mode: str = "real",
        tier: Optional[str] = None,
        gate_name: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        """Build and save the Markdown report.

        Returns the path to the saved file.
        """
        content = self.build_text(
            decisions=decisions,
            universe_summary=universe_summary,
            mode=mode,
            tier=tier,
            gate_name=gate_name,
        )
        if output_dir is None:
            output_dir = os.path.join(BASE_DIR, "reports")
        os.makedirs(output_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(output_dir, f"coverage_quality_gate_report_{date_str}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Saved coverage quality gate report to %s", path)
        return path

    def build_text(
        self,
        decisions: List[Dict[str, Any]],
        universe_summary: Dict[str, Any],
        mode: str = "real",
        tier: Optional[str] = None,
        gate_name: Optional[str] = None,
    ) -> str:
        """Build and return the report as a string without saving."""
        decisions = decisions or []
        universe_summary = universe_summary or {}
        lines: List[str] = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append("# Coverage Quality Gates Report v1.1.4")
        lines.append("")
        lines.append(f"> Generated: {now}")
        lines.append(f"> Mode: {mode}")
        lines.append(f"> Tier: {tier or 'all'}")
        lines.append(f"> Gate: {gate_name or 'all'}")
        lines.append("> [!] Research Only. No Real Orders.")
        lines.append("> [!] Coverage Quality Gate does NOT enable trading.")
        lines.append("> [!] VALIDATED status does NOT enable trading or broker execution.")
        lines.append("")

        # ─── 一、總覽 ───────────────────────────────────────────────────────
        lines.append("## 一、總覽")
        lines.append("")
        try:
            try:
                from release.version_info import VERSION
            except Exception:
                VERSION = "1.1.4"
            formal   = [d for d in decisions if d.get("decision") == self.FORMAL]
            obs      = [d for d in decisions if d.get("decision") == self.OBSERVATIONAL]
            demo     = [d for d in decisions if d.get("decision") == self.DEMO]
            blocked  = [d for d in decisions if d.get("decision") == self.BLOCKED]
            evaluated = len(decisions)
            registered = universe_summary.get("registered", evaluated)
            confidence = universe_summary.get("statistical_confidence", "N/A")

            lines.append(f"- **Version**: {VERSION}")
            lines.append(f"- **Research Only**: True")
            lines.append(f"- **No Real Orders**: True")
            lines.append(f"- **Mode**: {mode}")
            lines.append(f"- **Tier**: {tier or 'all'}")
            lines.append(f"- **Gate**: {gate_name or 'all'}")
            lines.append("")
            lines.append(f"- **Registered**: {registered}")
            lines.append(f"- **Evaluated**: {evaluated}")
            lines.append(f"- **Formal Eligible**: {len(formal)}")
            lines.append(f"- **Observational**: {len(obs)}")
            lines.append(f"- **Demo Only**: {len(demo)}")
            lines.append(f"- **Blocked**: {len(blocked)}")
            lines.append(f"- **Statistical Confidence**: {confidence}")
        except Exception as exc:
            logger.warning("Section 一 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 二、Gate Policy ────────────────────────────────────────────────
        lines.append("## 二、Gate Policy")
        lines.append("")
        try:
            _FORMAL_CONDITIONS = (
                "≥ 240 trading days of real price data; "
                "freshness FRESH or ACCEPTABLE; "
                "no OHLC integrity violations; "
                "no unresolved conflicts; "
                "source health OK; "
                "no mock data contamination"
            )
            _OBS_CONDITIONS = (
                "≥ 120 and < 240 trading days; "
                "freshness not STALE; "
                "minor issues allowed with confidence limit"
            )
            _DEMO_CONDITIONS = (
                "< 120 trading days OR mock data; "
                "pattern demonstration only; "
                "no backtest significance"
            )
            _BLOCKED_CONDITIONS = (
                "missing price data; "
                "< 60 trading days; "
                "STALE (> SLA threshold); "
                "unresolved conflict; "
                "invalid OHLC; "
                "future dates detected; "
                "date regression; "
                "source interruption; "
                "mock source in real mode"
            )
            try:
                from quality_gates.gate_policy import (
                    REQUIRED_DATASETS,
                    OPTIONAL_DATASETS,
                )
                req_datasets = ", ".join(REQUIRED_DATASETS)
                opt_datasets = ", ".join(OPTIONAL_DATASETS)
            except Exception:
                req_datasets = "price_daily"
                opt_datasets = "chips, short_interest, fundamentals, sector_rotation"

            lines.append("### Formal Conditions")
            lines.append(f"> {_FORMAL_CONDITIONS}")
            lines.append("")
            lines.append("### Observational Conditions")
            lines.append(f"> {_OBS_CONDITIONS}")
            lines.append("")
            lines.append("### Demo Conditions")
            lines.append(f"> {_DEMO_CONDITIONS}")
            lines.append("")
            lines.append("### Blocked Conditions")
            lines.append(f"> {_BLOCKED_CONDITIONS}")
            lines.append("")
            lines.append(f"- **Required Datasets**: {req_datasets}")
            lines.append(f"- **Optional Datasets**: {opt_datasets}")
        except Exception as exc:
            logger.warning("Section 二 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 三、Symbol Decisions (table) ───────────────────────────────────
        lines.append("## 三、Symbol Decisions")
        lines.append("")
        try:
            if decisions:
                lines.append("| Symbol | Tier | Gate | Decision | Confidence | Top Reason Codes |")
                lines.append("|--------|------|------|----------|------------|-----------------|")
                for d in decisions[:60]:
                    sym        = d.get("symbol", "?")
                    sym_tier   = d.get("tier", tier or "?")
                    sym_gate   = d.get("gate", gate_name or "?")
                    decision   = d.get("decision", "?")
                    conf       = d.get("confidence", "?")
                    reasons    = d.get("reason_codes", [])
                    top_codes  = ", ".join(str(r) for r in reasons[:3])
                    lines.append(f"| {sym} | {sym_tier} | {sym_gate} | {decision} | {conf} | {top_codes} |")
                if len(decisions) > 60:
                    lines.append(f"| ... ({len(decisions) - 60} more) | | | | | |")
            else:
                lines.append("No decisions evaluated.")
        except Exception as exc:
            logger.warning("Section 三 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 四、Formal Eligible ────────────────────────────────────────────
        lines.append("## 四、Formal Eligible")
        lines.append("")
        try:
            formal_list = [d for d in decisions if d.get("decision") == self.FORMAL]
            if formal_list:
                for d in formal_list:
                    sym = d.get("symbol", "?")
                    dr  = d.get("data_readiness", "N/A")
                    fr  = d.get("freshness", "N/A")
                    it  = d.get("integrity", "N/A")
                    sh  = d.get("source_health", "N/A")
                    lines.append(
                        f"- **{sym}** — readiness={dr}, freshness={fr}, "
                        f"integrity={it}, source_health={sh}"
                    )
            else:
                lines.append("No symbols are Formal Eligible.")
            lines.append("")
            lines.append(
                "> [!] Formal Eligible does NOT mean trade-enabled. "
                "Research use only."
            )
        except Exception as exc:
            logger.warning("Section 四 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 五、Observational ──────────────────────────────────────────────
        lines.append("## 五、Observational")
        lines.append("")
        try:
            obs_list = [d for d in decisions if d.get("decision") == self.OBSERVATIONAL]
            if obs_list:
                for d in obs_list:
                    sym     = d.get("symbol", "?")
                    limits  = d.get("confidence_limit", "N/A")
                    missing = d.get("missing_optional_datasets", [])
                    miss_str = ", ".join(missing) if missing else "none"
                    lines.append(
                        f"- **{sym}** — confidence_limit={limits}, "
                        f"missing_optional={miss_str}"
                    )
            else:
                lines.append("No symbols in Observational tier.")
        except Exception as exc:
            logger.warning("Section 五 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 六、Blocked ────────────────────────────────────────────────────
        lines.append("## 六、Blocked")
        lines.append("")
        try:
            blocked_list = [d for d in decisions if d.get("decision") == self.BLOCKED]
            if blocked_list:
                # Group by primary reason
                groups: Dict[str, List[str]] = {}
                for d in blocked_list:
                    codes  = d.get("reason_codes", [])
                    primary = str(codes[0]) if codes else "UNKNOWN"
                    groups.setdefault(primary, []).append(d.get("symbol", "?"))

                REASON_LABELS = {
                    "MISSING_PRICE":        "Missing Price Data",
                    "INSUFFICIENT_HISTORY": "Insufficient History",
                    "STALE_DATA":           "Stale Data",
                    "CONFLICT":             "Data Conflict",
                    "INVALID_OHLC":         "Invalid OHLC",
                    "FUTURE_DATE":          "Future Date Detected",
                    "DATE_REGRESSION":      "Date Regression",
                    "SOURCE_INTERRUPTION":  "Source Interruption",
                    "MOCK_SOURCE":          "Mock Data Source",
                }
                for code, syms in groups.items():
                    label = REASON_LABELS.get(code, code)
                    lines.append(f"### {label} ({code})")
                    for s in syms:
                        lines.append(f"- {s}")
                    lines.append("")
            else:
                lines.append("No symbols are Blocked.")
        except Exception as exc:
            logger.warning("Section 六 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 七、Module-specific Gates ──────────────────────────────────────
        lines.append("## 七、Module-specific Gates")
        lines.append("")
        try:
            MODULE_GATES = [
                ("KD Advanced",        "price_daily ≥ 240d, KD params validated"),
                ("Short Interest",      "price_daily + short_interest dataset required"),
                ("Bottom Reversal",     "price_daily ≥ 240d, volume spike data required"),
                ("Sector Rotation",     "price_daily + sector_rotation dataset required"),
                ("Fundamental Quality", "price_daily + fundamentals dataset required"),
                ("Stock Report",        "price_daily + report_data dataset required"),
                ("Local Assistant",     "price_daily ≥ 120d minimum, knowledge base sync"),
            ]
            lines.append("| Module | Gate Requirements |")
            lines.append("|--------|-------------------|")
            for mod, req in MODULE_GATES:
                lines.append(f"| {mod} | {req} |")

            # Annotate decisions per module if available
            for d in decisions:
                mod_gates = d.get("module_gates", {})
                if mod_gates:
                    sym = d.get("symbol", "?")
                    for mod_key, status in mod_gates.items():
                        lines.append(f"\n- `{sym}` / {mod_key}: **{status}**")
        except Exception as exc:
            logger.warning("Section 七 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 八、Universe Quality ───────────────────────────────────────────
        lines.append("## 八、Universe Quality")
        lines.append("")
        try:
            tier_stats = universe_summary.get("tier_stats", {})
            TIERS = ["CORE_10", "RESEARCH_30", "EXPANDED_50", "BROAD_100"]
            lines.append("| Tier | Ready Ratio | Formal Ratio | Confidence |")
            lines.append("|------|------------|-------------|------------|")
            for t in TIERS:
                stats = tier_stats.get(t, {})
                ready  = stats.get("ready_ratio",  "N/A")
                formal = stats.get("formal_ratio", "N/A")
                conf   = stats.get("confidence",   "N/A")
                lines.append(f"| {t} | {ready} | {formal} | {conf} |")
        except Exception as exc:
            logger.warning("Section 八 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 九、Overrides ──────────────────────────────────────────────────
        lines.append("## 九、Overrides")
        lines.append("")
        try:
            overrides = universe_summary.get("overrides", {})
            requested = overrides.get("requested", 0)
            approved  = overrides.get("approved",  0)
            expired   = overrides.get("expired",   0)
            lines.append(f"- **Requested**: {requested}")
            lines.append(f"- **Approved**: {approved}")
            lines.append(f"- **Expired**: {expired}")
            lines.append("")
            lines.append(
                "> [!] Override is DISABLED by default. "
                "BLOCKED_INVALID_DATA, CONFLICT, and MOCK cannot be overridden to FORMAL."
            )
            lines.append(
                "> [!] Override does NOT enable real trading. "
                "Research use only."
            )
        except Exception as exc:
            logger.warning("Section 九 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 十、Safe Next Steps ────────────────────────────────────────────
        lines.append("## 十、Safe Next Steps")
        lines.append("")
        try:
            next_steps = universe_summary.get("next_steps", [])
            STEP_DESCRIPTIONS = {
                "FIX_DATA":           "Resolve OHLC, conflict, or duplicate issues in source data",
                "PROVIDE_SOURCE_DATA": "Import missing datasets via batch import workflow",
                "REFRESH_COVERAGE":   "Re-run coverage analysis after data changes",
                "REVIEW":             "Manual review of flagged anomalies before any backtest",
                "BACKTEST_MORE":      "Accumulate additional history before formal gate",
                "KEEP_OBSERVING":     "Continue observation period; check again after 30d",
            }
            if next_steps:
                for step in next_steps:
                    desc = STEP_DESCRIPTIONS.get(step, "")
                    lines.append(f"- **{step}**: {desc}")
            else:
                for step, desc in STEP_DESCRIPTIONS.items():
                    lines.append(f"- **{step}**: {desc}")
        except Exception as exc:
            logger.warning("Section 十 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        # ─── 十一、安全聲明 ─────────────────────────────────────────────────
        lines.append("## 十一、安全聲明")
        lines.append("")
        try:
            lines.append("| Safety Flag | Value |")
            lines.append("|-------------|-------|")
            lines.append("| No Real Orders | **True** |")
            lines.append("| No Broker Execution | **True** |")
            lines.append("| Quality Gate Does NOT Enable Trading | **True** |")
            lines.append("| VALIDATED Does NOT Enable Trading | **True** |")
            lines.append("| Mock Data Cannot Pass Formal Gate | **True** |")
            lines.append("| Override Disabled by Default | **True** |")
            lines.append("| Research Only | **True** |")
            lines.append("| Production Trading Blocked | **True** |")
            lines.append("")
            lines.append(
                "> [!] **Not Investment Advice.** "
                "All outputs are for research and educational purposes only."
            )
            lines.append(
                "> [!] Gate evaluation results indicate data readiness only. "
                "They do not constitute a trading signal, recommendation, or order."
            )
            lines.append(
                "> [!] No broker connectivity. No order placement. "
                "No position sizing. No execution."
            )
        except Exception as exc:
            logger.warning("Section 十一 failed: %s", exc)
            lines.append(f"- Section unavailable: {exc}")
        lines.append("")

        return "\n".join(lines)
