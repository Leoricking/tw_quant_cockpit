"""
strategy_robustness/report_v142.py — Report generator for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class StrategyRobustnessReport:
    """
    Generates structured and text reports for strategy robustness results.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def generate(self, result) -> dict:
        """
        Generate report dict from a StrategyRobustnessResult or dict.

        Parameters
        ----------
        result : StrategyRobustnessResult or dict

        Returns
        -------
        dict with report sections
        """
        if hasattr(result, "to_dict"):
            d = result.to_dict()
        else:
            d = dict(result)

        return {
            "report_type": "STRATEGY_ROBUSTNESS",
            "version": "1.4.2",
            "rule_id": d.get("rule_id"),
            "universe": d.get("universe"),
            "date_range": {"start": d.get("start_date"), "end": d.get("end_date")},
            "summary": {
                "overall_score": d.get("overall_score", 0.0),
                "robustness_status": d.get("robustness_status", "UNKNOWN"),
                "formal_conclusion_allowed": d.get("formal_conclusion_allowed", False),
                "trade_count": d.get("trade_count", 0),
                "symbol_count": d.get("symbol_count", 0),
            },
            "time_robustness": d.get("time_robustness", {}),
            "cross_sectional": d.get("cross_sectional", {}),
            "industry_robustness": d.get("industry_robustness", {}),
            "regime_robustness": d.get("regime_robustness", {}),
            "parameter_sensitivity": d.get("parameter_sensitivity", {}),
            "cost_stress": d.get("cost_stress", {}),
            "trade_concentration": d.get("trade_concentration", {}),
            "bootstrap": d.get("bootstrap", {}),
            "monte_carlo": d.get("monte_carlo", {}),
            "rolling_stability": d.get("rolling_stability", {}),
            "decay": d.get("decay", {}),
            "stress_scenarios": d.get("stress_scenarios", {}),
            "failure_modes": d.get("failure_modes", []),
            "dimension_scores": d.get("dimension_scores", {}),
            "warnings": d.get("warnings", []),
            "blocked_reasons": d.get("blocked_reasons", []),
            "reproducibility_hash": d.get("reproducibility_hash", ""),
            "safety": {
                "no_real_orders": True,
                "broker_execution_enabled": False,
                "production_trading_blocked": True,
                "mock_formal_conclusion_allowed": False,
                "research_only": True,
            },
        }

    def format_text(self, d: dict) -> str:
        """Format report dict as plain text."""
        lines = [
            "=" * 60,
            "  Strategy Robustness & Regime Validation Report v1.4.2",
            "  [!] Research Only. No Real Orders. Not Investment Advice.",
            "=" * 60,
        ]
        summary = d.get("summary", {})
        lines.append(f"  Rule:           {d.get('rule_id', 'N/A')}")
        lines.append(f"  Universe:       {d.get('universe', 'N/A')}")
        lines.append(f"  Date Range:     {d.get('date_range', {}).get('start')} to {d.get('date_range', {}).get('end')}")
        lines.append(f"  Overall Score:  {summary.get('overall_score', 0.0):.1f}/100")
        lines.append(f"  Status:         {summary.get('robustness_status', 'UNKNOWN')}")
        lines.append(f"  Trade Count:    {summary.get('trade_count', 0)}")
        lines.append(f"  Symbol Count:   {summary.get('symbol_count', 0)}")
        lines.append(f"  Formal Conclusion Allowed: {summary.get('formal_conclusion_allowed', False)}")
        lines.append("")

        # Dimension scores
        dim_scores = d.get("dimension_scores", {})
        if dim_scores:
            lines.append("  Dimension Scores:")
            for dim, score in dim_scores.items():
                lines.append(f"    {dim:20s}: {score:.1f}")
            lines.append("")

        # Failure modes
        failure_modes = d.get("failure_modes", [])
        if failure_modes:
            lines.append("  Failure Modes:")
            for fm in failure_modes:
                lines.append(f"    [{fm.get('severity','?')}] {fm.get('type','?')}: {fm.get('recommended_research_action','?')}")
            lines.append("")

        # Warnings
        warnings = d.get("warnings", [])
        if warnings:
            lines.append("  Warnings:")
            for w in warnings:
                lines.append(f"    - {w}")
            lines.append("")

        lines.append(f"  Hash: {d.get('reproducibility_hash', 'N/A')}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def format_markdown(self, d: dict) -> str:
        """Format report dict as Markdown."""
        summary = d.get("summary", {})
        lines = [
            "# Strategy Robustness & Regime Validation Report v1.4.2",
            "",
            "> **[!] Research Only. No Real Orders. Not Investment Advice.**",
            "",
            "## Summary",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Rule ID | `{d.get('rule_id', 'N/A')}` |",
            f"| Universe | {d.get('universe', 'N/A')} |",
            f"| Date Range | {d.get('date_range', {}).get('start')} to {d.get('date_range', {}).get('end')} |",
            f"| Overall Score | **{summary.get('overall_score', 0.0):.1f}**/100 |",
            f"| Status | **{summary.get('robustness_status', 'UNKNOWN')}** |",
            f"| Trade Count | {summary.get('trade_count', 0)} |",
            f"| Symbol Count | {summary.get('symbol_count', 0)} |",
            f"| Formal Conclusion | {summary.get('formal_conclusion_allowed', False)} |",
            "",
        ]

        dim_scores = d.get("dimension_scores", {})
        if dim_scores:
            lines += [
                "## Dimension Scores",
                "",
                "| Dimension | Score |",
                "|-----------|-------|",
            ]
            for dim, score in dim_scores.items():
                lines.append(f"| {dim} | {score:.1f} |")
            lines.append("")

        failure_modes = d.get("failure_modes", [])
        if failure_modes:
            lines += ["## Failure Modes", ""]
            for fm in failure_modes:
                lines.append(f"- **[{fm.get('severity','?')}]** `{fm.get('type','?')}`: {fm.get('recommended_research_action','?')}")
            lines.append("")

        warnings = d.get("warnings", [])
        if warnings:
            lines += ["## Warnings", ""]
            for w in warnings:
                lines.append(f"- {w}")
            lines.append("")

        lines += [
            "---",
            f"*Reproducibility hash: `{d.get('reproducibility_hash', 'N/A')}`*",
        ]
        return "\n".join(lines)
