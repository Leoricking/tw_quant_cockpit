"""
abc_validation/report_v141.py — Report generator for A/B/C validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, Optional


class ABCValidationReport:
    """
    Generates validation reports for A/B/C buy point empirical validation.

    Sections: summary, signals, outcomes, holding_periods, stop_loss,
    take_profit, regimes, ablation, second_wave, institutional,
    margin, volume, walk_forward, blocked, provenance, limitations.
    """

    def generate_text(self, result: Dict[str, Any]) -> str:
        """Generate a human-readable text report."""
        lines = []
        lines.append("=" * 70)
        lines.append("  TW Quant Cockpit — A/B/C Buy Point Validation Report v1.4.1")
        lines.append("  [!] Research Only. No Real Orders. Not Investment Advice.")
        lines.append("=" * 70)
        lines.append("")

        # Section 1: Summary
        lines.append("1. SUMMARY")
        lines.append(f"  Validation ID:     {result.get('validation_id', 'N/A')}")
        lines.append(f"  Buy Point Type:    {result.get('buy_point_type', 'N/A')}")
        lines.append(f"  Universe:          {result.get('universe', 'N/A')}")
        lines.append(f"  Symbols Tested:    {len(result.get('symbols_tested', []))}")
        lines.append(f"  Symbols Blocked:   {len(result.get('symbols_blocked', []))}")
        lines.append(f"  Signal Count:      {result.get('signal_count', 0)}")
        lines.append(f"  Trade Count:       {result.get('trade_count', 0)}")
        lines.append(f"  No-Fill Count:     {result.get('no_fill_count', 0)}")
        lines.append(f"  Confidence:        {result.get('confidence', 'INSUFFICIENT')}")
        lines.append(f"  Formal Conclusion: {result.get('formal_conclusion_allowed', False)}")
        lines.append("")

        # Section 2: Holding Period Results
        lines.append("2. HOLDING PERIOD RESULTS")
        hp = result.get("holding_period_results", {})
        period_results = hp.get("period_results", {}) if isinstance(hp, dict) else {}
        for period, pr in sorted(period_results.items()):
            wr = pr.get("win_rate")
            exp = pr.get("expectancy")
            lines.append(
                f"  {period:2d}d: win_rate={wr:.1%} exp={exp:.4f} trades={pr.get('filled_trades', 0)}"
                if wr is not None and exp is not None
                else f"  {period:2d}d: INSUFFICIENT_DATA"
            )
        lines.append("")

        # Section 3: Outcomes
        lines.append("3. OUTCOME DISTRIBUTION")
        outcomes = result.get("outcome_distribution", {})
        for outcome, count in sorted(outcomes.items(), key=lambda x: -x[1]):
            lines.append(f"  {outcome:<35s}: {count}")
        lines.append("")

        # Section 4: Regime Results
        lines.append("4. REGIME BREAKDOWN")
        regime_r = result.get("regime_results", {})
        regime_data = regime_r.get("regime_results", {}) if isinstance(regime_r, dict) else {}
        for regime, rd in regime_data.items():
            if not isinstance(rd, dict) or rd.get("trade_count", 0) == 0:
                continue
            wr = rd.get("win_rate")
            exp = rd.get("expectancy")
            lines.append(
                f"  {regime:<20s}: win_rate={wr:.1%} exp={exp:.4f} trades={rd.get('trade_count', 0)}"
                if wr is not None and exp is not None
                else f"  {regime:<20s}: INSUFFICIENT_DATA"
            )
        lines.append("")

        # Section 5: Limitations & Warnings
        lines.append("5. LIMITATIONS & WARNINGS")
        for lim in result.get("limitations", []):
            lines.append(f"  [LIMITATION] {lim}")
        for warn in result.get("warnings", []):
            lines.append(f"  [WARNING] {warn}")
        lines.append("")

        # Section 6: Safety Footer
        lines.append("6. SAFETY")
        lines.append("  No Real Orders: True")
        lines.append("  Broker Execution Enabled: False")
        lines.append("  Production Trading BLOCKED: True")
        lines.append("  Mock Formal Conclusion Allowed: False")
        lines.append("  [!] This report is for research/training purposes only.")
        lines.append("=" * 70)

        return "\n".join(lines)

    def generate_dict(self, result: Dict[str, Any]) -> dict:
        """Generate structured report dict."""
        return {
            "report_type": "abc_validation",
            "version": "1.4.1",
            "validation_id": result.get("validation_id"),
            "buy_point_type": result.get("buy_point_type"),
            "summary": {
                "signal_count": result.get("signal_count", 0),
                "trade_count": result.get("trade_count", 0),
                "confidence": result.get("confidence"),
                "formal_conclusion_allowed": result.get("formal_conclusion_allowed", False),
            },
            "sections": [
                "summary", "signals", "outcomes", "holding_periods",
                "stop_loss", "take_profit", "regimes", "ablation",
                "second_wave", "institutional", "margin", "volume",
                "walk_forward", "blocked", "provenance", "limitations",
            ],
            "no_real_orders": True,
            "research_only": True,
        }
