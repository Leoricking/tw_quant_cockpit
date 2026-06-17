"""
replay/score_explainer.py — ReplayScoreExplainer for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Explanations are training feedback, not trading advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoreExplainer:
    """
    Generates human-readable explanations for replay scores.
    [!] Research Only. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def explain_process_score(self, process_score: Dict[str, Any]) -> str:
        total = process_score.get("total_score", 0.0)
        status = process_score.get("status", "UNKNOWN")
        confidence = process_score.get("confidence_level", "UNKNOWN")
        components = process_score.get("components", [])
        warnings = process_score.get("warnings", [])

        lines = [
            f"Process Score Explanation",
            f"  Total Score : {total:.1f} / 100",
            f"  Status      : {status}",
            f"  Confidence  : {confidence}",
            "",
            "  Dimension Breakdown:",
        ]

        for comp in components:
            dim = comp.get("dimension", "?")
            raw = comp.get("raw_score", 0.0)
            wt = comp.get("weight", 0)
            ws = comp.get("weighted_score", 0.0)
            rationale = comp.get("rationale", "")
            missing = comp.get("missing_items", [])
            lines.append(
                f"    {dim:<30} raw={raw:.2f}  weight={wt:2d}  weighted={ws:.1f}"
            )
            if rationale:
                lines.append(f"      -> {rationale}")
            if missing:
                lines.append(f"      -> Missing: {', '.join(missing)}")

        if warnings:
            lines.append("")
            lines.append("  Warnings:")
            for w in warnings:
                lines.append(f"    [!] {w}")

        lines.append("")
        lines.append(
            "  [!] Process score uses NO future data. Research Only. Not Investment Advice."
        )
        return "\n".join(lines)

    def explain_composite_score(self, composite_score: Dict[str, Any]) -> str:
        composite = composite_score.get("composite_score")
        classification = composite_score.get("classification", "UNKNOWN")
        status = composite_score.get("status", "UNKNOWN")
        ps = composite_score.get("process_score")
        os_ = composite_score.get("outcome_score")
        pw = composite_score.get("process_weight", 0.70)
        ow = composite_score.get("outcome_weight", 0.30)
        warnings = composite_score.get("warnings", [])

        lines = [
            f"Composite Score Explanation",
            f"  Status         : {status}",
            f"  Classification : {classification}",
            f"  Process Score  : {ps if ps is not None else 'N/A'} (weight={pw:.0%})",
            f"  Outcome Score  : {os_ if os_ is not None else 'BLOCKED'} (weight={ow:.0%})",
            f"  Composite      : {composite if composite is not None else 'N/A'}",
        ]

        if status == "PROCESS_ONLY":
            lines.append("")
            lines.append("  [!] Outcome not revealed — composite is PROCESS_ONLY.")

        if warnings:
            lines.append("")
            lines.append("  Warnings:")
            for w in warnings:
                lines.append(f"    [!] {w}")

        lines.append("")
        lines.append("  [!] Research Only. Not Investment Advice.")
        return "\n".join(lines)

    def explain_mistake(self, mistake: Dict[str, Any]) -> str:
        from replay.mistake_taxonomy import MistakeTaxonomy
        mtype = mistake.get("mistake_type", "UNKNOWN")
        status = mistake.get("status", "SUGGESTED")
        severity = mistake.get("severity", "LOW")
        source = mistake.get("source", "SYSTEM_SUGGESTED")
        evidence = mistake.get("evidence", [])
        description = MistakeTaxonomy.get_description(mtype)
        is_emotional = MistakeTaxonomy.is_emotional(mtype)

        lines = [
            f"Mistake Explanation",
            f"  Type     : {mtype}",
            f"  Status   : {status}",
            f"  Severity : {severity}",
            f"  Source   : {source}",
            f"  Description: {description}",
        ]

        if evidence:
            lines.append("  Evidence:")
            for ev in evidence:
                lines.append(f"    - {ev}")

        if is_emotional:
            lines.append(
                "\n  [!] Emotional pattern: self-reported or rule-triggered only. "
                "NOT psychological diagnosis."
            )

        lines.append(
            "\n  [!] Status=SUGGESTED — USER review required. "
            "System cannot auto-confirm."
        )
        return "\n".join(lines)

    def summary_banner(self, total_score: float, classification: str) -> str:
        if total_score >= 80:
            grade = "EXCELLENT"
        elif total_score >= 60:
            grade = "GOOD"
        elif total_score >= 40:
            grade = "NEEDS_IMPROVEMENT"
        else:
            grade = "POOR"

        return (
            f"[!] Process Score: {total_score:.1f}/100 ({grade}) | "
            f"Classification: {classification} | "
            f"Research Only | Not Investment Advice"
        )
