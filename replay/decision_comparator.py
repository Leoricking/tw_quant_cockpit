"""
replay/decision_comparator.py — DecisionJournalComparator for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] FORBIDDEN fields NEVER shown: realized_return, future_return,
    hindsight_score, final_result, future_max_gain, future_max_loss.
[!] Raises ValueError if any forbidden field detected in output.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_COMPARATOR_FIELDS = [
    "realized_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
    "realized_pnl", "final_label", "outcome",
]


def _strip_forbidden(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove forbidden fields from a dict."""
    return {k: v for k, v in d.items() if k not in FORBIDDEN_COMPARATOR_FIELDS}


def _check_forbidden(d: Dict[str, Any], context: str = "") -> None:
    """Raise ValueError if any forbidden field is present."""
    found = [k for k in FORBIDDEN_COMPARATOR_FIELDS if k in d]
    if found:
        raise ValueError(
            f"Forbidden field(s) detected in comparator output{' (' + context + ')' if context else ''}: "
            f"{found}. These fields are not allowed. [!] No future results allowed."
        )


class DecisionJournalComparator:
    """
    Compares decision journal entries.

    [!] FORBIDDEN fields never returned in output.
    [!] Raises ValueError on any attempt to include forbidden fields.
    """

    no_real_orders = True
    research_only = True

    FORBIDDEN_FIELDS = FORBIDDEN_COMPARATOR_FIELDS

    def compare_entries(
        self, entry_a: Dict[str, Any], entry_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two journal entries side by side."""
        safe_a = _strip_forbidden(entry_a)
        safe_b = _strip_forbidden(entry_b)

        compared_fields = [
            "action", "confidence", "decision_reason", "notes",
            "tags", "status", "replay_date", "symbol",
            "pre_decision_notes", "post_decision_notes",
            "planned_action", "fallback_action",
            "confirmation_conditions", "invalidation_conditions",
            "evidence_for", "evidence_against",
            "thesis_id", "risk_plan_id", "emotional_state_id",
        ]

        diff: Dict[str, Any] = {}
        same: Dict[str, Any] = {}

        for fld in compared_fields:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a == val_b:
                same[fld] = val_a
            else:
                diff[fld] = {"entry_a": val_a, "entry_b": val_b}

        result = {
            "entry_id_a": safe_a.get("journal_entry_id"),
            "entry_id_b": safe_b.get("journal_entry_id"),
            "differences": diff,
            "same_fields": same,
            "total_differences": len(diff),
            "simulation_only": True,
            "qualification": "NOT_QUALIFIED — comparison for research only",
            "no_real_orders": True,
        }

        _check_forbidden(result, "compare_entries")
        return result

    def compare_thesis(
        self, thesis_a: Dict[str, Any], thesis_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two trade theses."""
        safe_a = _strip_forbidden(thesis_a)
        safe_b = _strip_forbidden(thesis_b)

        fields = [
            "setup_type", "time_horizon", "title", "summary", "thesis_text",
            "key_triggers", "confirmation_conditions", "invalidation_conditions",
            "expected_scenario", "alternative_scenario",
        ]

        diff: Dict[str, Any] = {}
        for fld in fields:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a != val_b:
                diff[fld] = {"thesis_a": val_a, "thesis_b": val_b}

        result = {"thesis_differences": diff, "simulation_only": True}
        _check_forbidden(result, "compare_thesis")
        return result

    def compare_risk_plans(
        self, plan_a: Dict[str, Any], plan_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two risk plans."""
        safe_a = _strip_forbidden(plan_a)
        safe_b = _strip_forbidden(plan_b)

        fields = [
            "stop_type", "stop_price_note", "target_type", "target_price_note",
            "max_risk_note", "position_sizing_note", "max_loss_pct",
            "max_position_pct", "event_risk", "liquidity_risk",
        ]

        diff: Dict[str, Any] = {}
        for fld in fields:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a != val_b:
                diff[fld] = {"plan_a": val_a, "plan_b": val_b}

        result = {"risk_plan_differences": diff, "simulation_only": True}
        _check_forbidden(result, "compare_risk_plans")
        return result

    def compare_emotional_states(
        self, state_a: Dict[str, Any], state_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two emotional state records."""
        safe_a = _strip_forbidden(state_a)
        safe_b = _strip_forbidden(state_b)

        fields = [
            "primary_emotion", "confidence_level", "anxiety_level",
            "focus_level", "stress_level", "fomo",
            "revenge_trading_risk", "loss_aversion_risk",
            "cognitive_bias_flags",
        ]

        diff: Dict[str, Any] = {}
        for fld in fields:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a != val_b:
                diff[fld] = {"state_a": val_a, "state_b": val_b}

        result = {
            "emotional_differences": diff,
            "simulation_only": True,
            "note": "Self-reported emotional data. NOT psychological assessment.",
        }
        _check_forbidden(result, "compare_emotional_states")
        return result

    def compare_checklists(
        self, checklist_a: Dict[str, Any], checklist_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two discipline checklist results."""
        safe_a = _strip_forbidden(checklist_a)
        safe_b = _strip_forbidden(checklist_b)

        diff: Dict[str, Any] = {}
        for fld in ["passed_count", "total_count", "all_required_passed", "warnings"]:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a != val_b:
                diff[fld] = {"checklist_a": val_a, "checklist_b": val_b}

        result = {"checklist_differences": diff, "simulation_only": True}
        _check_forbidden(result, "compare_checklists")
        return result

    def compare_revisions(
        self, rev_a: Dict[str, Any], rev_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two revision records."""
        safe_a = _strip_forbidden(rev_a)
        safe_b = _strip_forbidden(rev_b)

        fields = [
            "revision_number", "reason", "changed_fields",
            "confidence_before", "confidence_after",
        ]

        diff: Dict[str, Any] = {}
        for fld in fields:
            val_a = safe_a.get(fld)
            val_b = safe_b.get(fld)
            if val_a != val_b:
                diff[fld] = {"rev_a": val_a, "rev_b": val_b}

        result = {"revision_differences": diff, "simulation_only": True}
        _check_forbidden(result, "compare_revisions")
        return result

    def summarize(self, comparison_result: Dict[str, Any]) -> str:
        """Return human-readable comparison summary."""
        n_diff = comparison_result.get("total_differences", 0)
        entry_a = comparison_result.get("entry_id_a", "?")
        entry_b = comparison_result.get("entry_id_b", "?")
        return (
            f"Comparison: {entry_a} vs {entry_b}\n"
            f"Differences: {n_diff} field(s)\n"
            f"[!] SIMULATION DECISION ONLY — NO PERFORMANCE DATA INCLUDED"
        )

    def render_markdown(self, comparison_result: Dict[str, Any]) -> str:
        """Render comparison as markdown."""
        lines = [
            "## Decision Journal Comparison",
            f"",
            f"**Entry A**: {comparison_result.get('entry_id_a', 'N/A')}",
            f"**Entry B**: {comparison_result.get('entry_id_b', 'N/A')}",
            f"",
            f"> [!] SIMULATION DECISION ONLY. No performance data. No real orders.",
            f"",
            "### Differences",
        ]
        for fld, vals in comparison_result.get("differences", {}).items():
            lines.append(f"- **{fld}**: A=`{vals.get('entry_a')}` → B=`{vals.get('entry_b')}`")

        if not comparison_result.get("differences"):
            lines.append("_(No differences in compared fields)_")

        return "\n".join(lines)
