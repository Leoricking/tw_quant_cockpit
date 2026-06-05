"""research_intelligence/recommendation_engine.py — ResearchRecommendationEngine v0.7.1.

Converts ResearchSignals into ranked ResearchRecommendations.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
[!] NO BUY/SELL/ORDER output. All recommendations are research actions only.
"""
from __future__ import annotations

import logging
import uuid
from typing import Dict, List

from research_intelligence.research_intelligence_schema import (
    ResearchSignal, ResearchRecommendation,
    PRI_P0, PRI_P1, PRI_P2, PRI_P3,
    SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM,
    CAT_DATA_GAP, CAT_REPORT_GAP, CAT_REPLAY_MISTAKE, CAT_JOURNAL_PATTERN,
    CAT_RULE_REVIEW, CAT_STRATEGY_RESEARCH, CAT_SYSTEM_RISK, CAT_TRAINING_TASK,
    CAT_PROVIDER_LIMIT, CAT_REGRESSION_WARN, CAT_STABLE_NOTE,
    ACT_FIX_DATA, ACT_GENERATE_REPORT, ACT_REVIEW_RULE, ACT_PRACTICE_REPLAY,
    ACT_REVIEW_JOURNAL, ACT_RUN_BACKTEST, ACT_RUN_REGRESSION, ACT_READ_REPORT,
    ACT_WAIT,
    _validate_action,
    classify_command_safety,
    CMD_SAFE_READ_ONLY,
)

logger = logging.getLogger(__name__)

_PRIORITY_ORDER = {PRI_P0: 0, PRI_P1: 1, PRI_P2: 2, PRI_P3: 3}
_SEVERITY_ORDER = {SEV_CRITICAL: 0, SEV_HIGH: 1, SEV_MEDIUM: 2, "LOW": 3, "INFO": 4}


def _rec_id() -> str:
    return f"REC-{uuid.uuid4().hex[:8].upper()}"


# ---------------------------------------------------------------------------
# UX helper functions (v0.7.1)
# ---------------------------------------------------------------------------

def build_why_now(sig: "ResearchSignal") -> str:
    """Return a concise why-now rationale for the signal."""
    _why = {
        CAT_DATA_GAP:         "Data gap blocks downstream analysis",
        CAT_REPORT_GAP:       "Missing report leaves research blind spot",
        CAT_REPLAY_MISTAKE:   "Replay score indicates skill gap",
        CAT_JOURNAL_PATTERN:  "Recurring journal pattern needs attention",
        CAT_RULE_REVIEW:      "Rule governance needs verification",
        CAT_STRATEGY_RESEARCH:"Strategy knowledge has gaps",
        CAT_SYSTEM_RISK:      "System risk may invalidate research results",
        CAT_TRAINING_TASK:    "Training task pending",
        CAT_PROVIDER_LIMIT:   "Provider limitation restricts available data",
        CAT_REGRESSION_WARN:  "Regression failure blocks reliable research",
        CAT_STABLE_NOTE:      "Stable release check required",
    }
    base = _why.get(sig.category, "Research quality at risk")
    if sig.evidence:
        return f"{base}. Evidence: {sig.evidence[:80]}"
    return base


def build_risk_if_ignored(sig: "ResearchSignal") -> str:
    """Return risk-if-ignored text for the signal."""
    _risk = {
        CAT_DATA_GAP:         "Analysis based on incomplete data; conclusions may be wrong",
        CAT_REPORT_GAP:       "Review cycle will miss this module's status",
        CAT_REPLAY_MISTAKE:   "Tape reading errors will compound without correction",
        CAT_JOURNAL_PATTERN:  "Process errors repeat; decision quality degrades",
        CAT_RULE_REVIEW:      "Rule drift goes undetected; strategy integrity at risk",
        CAT_STRATEGY_RESEARCH:"Strategy candidates remain unvalidated",
        CAT_SYSTEM_RISK:      "Unstable system produces untrustworthy research outputs",
        CAT_TRAINING_TASK:    "Skill development stalls",
        CAT_PROVIDER_LIMIT:   "Data availability remains restricted until resolved",
        CAT_REGRESSION_WARN:  "Breaking changes may silently corrupt results",
        CAT_STABLE_NOTE:      "Release health unknown; deployment risk elevated",
    }
    return _risk.get(sig.category, "Research quality may degrade over time")


def make_user_friendly_title(sig: "ResearchSignal") -> str:
    """Return a shorter, user-friendly title for a signal."""
    title = sig.title or ""
    # Trim module prefix patterns like "data_coverage: ..."
    for prefix in (
        "data_coverage:", "report_pack:", "replay_training:", "journal:",
        "rule_governance:", "strategy_knowledge:", "regression:", "stable_release:",
    ):
        if title.lower().startswith(prefix):
            title = title[len(prefix):].strip()
            break
    # Capitalise and truncate
    title = title.strip().capitalize()
    if len(title) > 80:
        title = title[:77] + "..."
    return title or sig.title


class ResearchRecommendationEngine:
    """Converts ResearchSignals into ranked ResearchRecommendations.

    All suggested_commands are safe research-only commands.
    No BUY/SELL/ORDER outputs are produced.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Main entry points
    # ------------------------------------------------------------------

    def build_recommendations(
        self,
        signals: List[ResearchSignal],
        mode: str = "real",
        memory_summary: object = None,
    ) -> List[ResearchRecommendation]:
        """Build recommendations from signals. Returns deduplicated, ranked list.

        v0.8.1: Optional memory_summary parameter. If provided, P3 recommendations
        that match existing memory titles get a '(seen)' suffix in rationale.
        P0/P1 items are never filtered or downgraded regardless of seen_before.
        """
        # Build keyword set from existing memories (if memory_summary provided)
        memory_keywords: set = set()
        if memory_summary is not None:
            try:
                memories = getattr(memory_summary, "memories", [])
                for m in memories:
                    if hasattr(m, "title"):
                        for word in m.title.lower().split():
                            if len(word) > 3:
                                memory_keywords.add(word)
            except Exception:
                pass

        recs = []
        for sig in signals:
            try:
                rec = self._signal_to_recommendation(sig, memory_keywords=memory_keywords)
                if rec is not None:
                    recs.append(rec)
            except Exception as exc:
                logger.warning("[RecommendationEngine] signal→rec error: %s", exc)
        recs = self.deduplicate(recs)
        recs = self.rank_recommendations(recs)
        # Assign display_order after final ranking
        for i, rec in enumerate(recs):
            rec.display_order = i + 1
        return recs

    def rank_recommendations(
        self, recommendations: List[ResearchRecommendation]
    ) -> List[ResearchRecommendation]:
        """Sort by priority (P0 first), then by action_type importance."""
        action_rank = {
            ACT_RUN_REGRESSION: 0,
            ACT_FIX_DATA:       1,
            ACT_GENERATE_REPORT: 2,
            ACT_PRACTICE_REPLAY: 3,
            ACT_REVIEW_JOURNAL:  4,
            ACT_REVIEW_RULE:     5,
            ACT_RUN_BACKTEST:    6,
            ACT_READ_REPORT:     7,
            ACT_WAIT:            8,
        }
        return sorted(
            recommendations,
            key=lambda r: (
                _PRIORITY_ORDER.get(r.priority, 9),
                action_rank.get(r.action_type, 9),
            ),
        )

    def deduplicate(
        self, recommendations: List[ResearchRecommendation]
    ) -> List[ResearchRecommendation]:
        """Remove duplicate recommendations (same action_type + first command)."""
        seen: Dict[str, bool] = {}
        deduped = []
        for rec in recommendations:
            key = f"{rec.action_type}::{rec.suggested_commands[0] if rec.suggested_commands else rec.title}"
            if key not in seen:
                seen[key] = True
                deduped.append(rec)
        return deduped

    # ------------------------------------------------------------------
    # Plan builders
    # ------------------------------------------------------------------

    def build_daily_plan(
        self, recommendations: List[ResearchRecommendation]
    ) -> List[ResearchRecommendation]:
        """Select up to 7 recommendations for today's research plan.

        Quota:
          1 system health check
          2 data/report fix
          2 replay/journal practice
          1 rule/strategy review
          1 optional improvement
        """
        plan: List[ResearchRecommendation] = []
        quotas = {
            "system":  (1, {CAT_SYSTEM_RISK, CAT_REGRESSION_WARN, CAT_STABLE_NOTE}),
            "data":    (2, {CAT_DATA_GAP, CAT_REPORT_GAP, CAT_PROVIDER_LIMIT}),
            "practice":(2, {CAT_REPLAY_MISTAKE, CAT_TRAINING_TASK, CAT_JOURNAL_PATTERN}),
            "rule":    (1, {CAT_RULE_REVIEW, CAT_STRATEGY_RESEARCH}),
            "optional":(1, set()),
        }
        used: Dict[str, int] = {k: 0 for k in quotas}
        assigned: set = set()

        for slot, (limit, cats) in quotas.items():
            for rec in recommendations:
                if rec.recommendation_id in assigned:
                    continue
                if slot == "optional":
                    if used[slot] < limit:
                        plan.append(rec)
                        assigned.add(rec.recommendation_id)
                        used[slot] += 1
                elif rec.category in cats and used[slot] < limit:
                    plan.append(rec)
                    assigned.add(rec.recommendation_id)
                    used[slot] += 1

        return self.rank_recommendations(plan)[:7]

    def build_weekly_plan(
        self, recommendations: List[ResearchRecommendation]
    ) -> List[ResearchRecommendation]:
        """Select up to 12 recommendations for the weekly research plan."""
        cats_order = [
            CAT_DATA_GAP, CAT_REPORT_GAP, CAT_REPLAY_MISTAKE,
            CAT_JOURNAL_PATTERN, CAT_RULE_REVIEW, CAT_STRATEGY_RESEARCH,
            CAT_SYSTEM_RISK, CAT_REGRESSION_WARN, CAT_TRAINING_TASK,
            CAT_PROVIDER_LIMIT, CAT_STABLE_NOTE,
        ]
        plan = []
        assigned: set = set()
        for cat in cats_order:
            for rec in recommendations:
                if rec.recommendation_id not in assigned and rec.category == cat:
                    plan.append(rec)
                    assigned.add(rec.recommendation_id)
                    break
        # Fill remaining slots
        for rec in recommendations:
            if rec.recommendation_id not in assigned and len(plan) < 12:
                plan.append(rec)
                assigned.add(rec.recommendation_id)
        return self.rank_recommendations(plan)[:12]

    # ------------------------------------------------------------------
    # Signal → Recommendation
    # ------------------------------------------------------------------

    def _signal_to_recommendation(
        self,
        sig: ResearchSignal,
        memory_keywords: set = None,
    ) -> ResearchRecommendation:
        """Convert a signal to a recommendation.

        v0.8.1: Optional memory_keywords set. If a P3 signal title overlaps
        with existing memory keywords, append '(seen)' to rationale.
        P0/P1 items are never modified regardless of seen_before.
        """
        action = sig.suggested_action or ACT_READ_REPORT
        _validate_action(action)
        cmd = sig.suggested_command or ""
        cmd_safety = classify_command_safety(cmd)
        friendly_title = make_user_friendly_title(sig)
        is_optional = sig.priority in (PRI_P2, PRI_P3)
        rationale = sig.description or sig.evidence or ""

        # v0.8.1: Mark P3 items as seen if they match existing memory keywords
        seen_before = False
        if memory_keywords and sig.priority == PRI_P3:
            title_words = set(friendly_title.lower().split())
            overlap = title_words & memory_keywords
            if len(overlap) >= 2:
                seen_before = True
                rationale = f"{rationale} (seen)" if rationale else "(seen)"

        return ResearchRecommendation(
            recommendation_id=_rec_id(),
            title=friendly_title,
            category=sig.category,
            priority=sig.priority,
            action_type=action,
            rationale=rationale,
            expected_benefit=self._expected_benefit(sig),
            required_inputs=[],
            suggested_commands=[cmd] if cmd else [],
            related_signals=[sig.signal_id],
            related_modules=[sig.source_module],
            due_hint="Today" if sig.priority in (PRI_P0, PRI_P1) else "This week",
            why_now=build_why_now(sig),
            risk_if_ignored=build_risk_if_ignored(sig),
            command_safety=cmd_safety,
            safe_command_label=cmd_safety,
            optional=is_optional,
            dismissible=is_optional,
        )

    def _expected_benefit(self, sig: ResearchSignal) -> str:
        cat_benefit = {
            CAT_DATA_GAP:         "Restore data completeness; unblock analysis",
            CAT_REPORT_GAP:       "Generate missing reports for review",
            CAT_REPLAY_MISTAKE:   "Improve tape reading accuracy and stop discipline",
            CAT_JOURNAL_PATTERN:  "Identify recurring process errors; improve decision quality",
            CAT_RULE_REVIEW:      "Maintain rule governance quality and strategy confidence",
            CAT_STRATEGY_RESEARCH:"Discover and validate new strategy candidates",
            CAT_SYSTEM_RISK:      "Restore system reliability and research trust",
            CAT_TRAINING_TASK:    "Build trading skills through structured practice",
            CAT_PROVIDER_LIMIT:   "Expand data availability once environment is configured",
            CAT_REGRESSION_WARN:  "Prevent regression failures from blocking research",
            CAT_STABLE_NOTE:      "Confirm stable release health",
        }
        return cat_benefit.get(sig.category, "Improve research quality")
