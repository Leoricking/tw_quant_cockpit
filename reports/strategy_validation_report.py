# reports/strategy_validation_report.py
# TW Quant Cockpit — Strategy Validation Score Report
# v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading
#
# DISCLAIMER: This report is for research and educational purposes ONLY.
# It does NOT issue, suggest, or authorise any real trading orders.
# NOT investment advice. Production trading is BLOCKED.
# VALIDATED grade = research validated ONLY. Does NOT enable trading.

from __future__ import annotations

import logging
import os
from datetime import date
from typing import List

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_FORBIDDEN_RENDER = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])

_GRADE_ORDER = [
    "VALIDATED", "VALIDATING", "OBSERVATIONAL",
    "INSUFFICIENT", "CONFLICTED", "REJECTED",
]

_MISSING_DATA_MSG = (
    "INSUFFICIENT_DATA — run: python main.py strategy-validation --mode real"
)


def _safe(value: str, default: str = "REVIEW") -> str:
    """Replace forbidden action strings with a safe default."""
    if str(value).upper() in _FORBIDDEN_RENDER:
        return default
    return str(value)


def _val(obj, *keys, default="—"):
    """Safe nested dict/attr get."""
    cur = obj
    for k in keys:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    if cur is None:
        return default
    return cur


def _as_list(obj) -> list:
    if isinstance(obj, list):
        return obj
    if obj is None:
        return []
    return [obj]


class StrategyValidationReportBuilder:
    """
    Build a Markdown strategy validation score report.

    RESEARCH ONLY — No Real Orders — Production Trading BLOCKED
    VALIDATED does not enable trading — Not Investment Advice
    """

    read_only = True
    no_real_orders = True
    production_blocked = True
    validated_does_not_enable_trading = True

    def build(self, mode: str = "real", output_dir: str = "reports") -> str:
        """
        Build markdown report.

        Returns absolute path to written file.
        Never raises exceptions.
        """
        try:
            if not os.path.isabs(output_dir):
                output_dir = os.path.join(_BASE_DIR, output_dir)

            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception:
                pass

            scores, components, summary = self._load_data(mode)
            md = self._build_markdown(scores, components, summary, mode)
            filepath = self._report_filename(output_dir)

            try:
                with open(filepath, "w", encoding="utf-8") as fh:
                    fh.write(md)
            except Exception as write_err:
                logger.warning("StrategyValidationReportBuilder: write failed: %s", write_err)
                return f"ERROR: Could not write report — {write_err}"

            return filepath
        except Exception as exc:
            logger.warning("StrategyValidationReportBuilder.build() failed: %s", exc)
            return f"ERROR: build() failed — {exc}"

    # ------------------------------------------------------------------
    # Filename
    # ------------------------------------------------------------------

    def _report_filename(self, output_dir: str = None) -> str:
        today = date.today().strftime("%Y-%m-%d")
        filename = f"strategy_validation_report_{today}.md"
        if output_dir:
            return os.path.join(output_dir, filename)
        base = os.path.join(_BASE_DIR, "reports")
        return os.path.join(base, filename)

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self, mode: str = "real"):
        """
        Try StrategyValidationEngine first; fall back to StrategyValidationStore.
        Returns (scores, components, summary) — each may be empty list/dict.
        """
        scores = []
        components = []
        summary = {}

        # 1) Try engine
        try:
            from strategy_validation.validation_engine import StrategyValidationEngine
            engine = StrategyValidationEngine()
            result = engine.run(mode=mode)
            if isinstance(result, dict):
                raw_scores = result.get("scores", [])
                raw_components = result.get("components", [])
                raw_summary = result.get("summary")
                scores = [
                    (s.to_dict() if hasattr(s, "to_dict") else dict(s))
                    for s in _as_list(raw_scores)
                ]
                components = [
                    (c.to_dict() if hasattr(c, "to_dict") else dict(c))
                    for c in _as_list(raw_components)
                ]
                if raw_summary is not None:
                    summary = (
                        raw_summary.to_dict()
                        if hasattr(raw_summary, "to_dict")
                        else dict(raw_summary)
                    )
                return scores, components, summary
        except Exception as exc:
            logger.debug("StrategyValidationReportBuilder: engine failed: %s", exc)

        # 2) Fall back to store
        try:
            from strategy_validation.validation_store import StrategyValidationStore
            store = StrategyValidationStore()
            raw_scores = store.load_latest_scores() or []
            raw_components = store.load_latest_components() or []
            raw_summary = store.load_latest_summary()
            scores = [
                (s.to_dict() if hasattr(s, "to_dict") else dict(s))
                for s in raw_scores
            ]
            components = [
                (c.to_dict() if hasattr(c, "to_dict") else dict(c))
                for c in raw_components
            ]
            if raw_summary is not None:
                summary = (
                    raw_summary.to_dict()
                    if hasattr(raw_summary, "to_dict")
                    else dict(raw_summary)
                )
        except Exception as exc:
            logger.debug("StrategyValidationReportBuilder: store failed: %s", exc)

        return scores, components, summary

    # ------------------------------------------------------------------
    # Markdown builder
    # ------------------------------------------------------------------

    def _build_markdown(
        self,
        scores: list,
        components: list,
        summary: dict,
        mode: str,
    ) -> str:
        lines: List[str] = []

        today = date.today().strftime("%Y-%m-%d")

        lines.append("# Strategy Validation Score Report")
        lines.append("")
        lines.append(
            "> **RESEARCH ONLY — No Real Orders — Production Trading BLOCKED"
            " — VALIDATED does not enable trading — Not Investment Advice**"
        )
        lines.append("")
        lines.append(
            f"*Generated: {today}  |  Mode: {mode}  |  Version: {VERSION}*"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # Section 一: 總覽
        lines += self._section_overview(summary)
        lines.append("")

        # Section 二: Validation Grade Board
        lines += self._section_grade_board(scores)
        lines.append("")

        # Section 三: Validated Research Rules
        lines += self._section_validated_rules(scores)
        lines.append("")

        # Section 四: Observational / Validating
        lines += self._section_observational_validating(scores)
        lines.append("")

        # Section 五: Conflicted / Rejected
        lines += self._section_conflicted_rejected(scores)
        lines.append("")

        # Section 六: Crash Reversal
        lines += self._section_crash_reversal(scores)
        lines.append("")

        # Section 七: Evidence Components
        lines += self._section_evidence_components(components)
        lines.append("")

        # Section 八: Safe Next Steps
        lines += self._section_safe_next_steps(scores)
        lines.append("")

        # Section 九: 安全聲明
        lines += self._section_safety_declaration()
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _section_overview(self, summary: dict) -> List[str]:
        lines = ["## 一、總覽", ""]
        if not summary:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        lines.append("| Item | Value |")
        lines.append("|------|-------|")
        lines.append("| Research Only | YES |")
        lines.append("| No Real Orders | YES |")
        lines.append("| VALIDATED does not enable trading | YES |")
        lines.append(f"| Total | {_val(summary, 'total_strategies', default=0)} |")
        lines.append(f"| INSUFFICIENT | {_val(summary, 'insufficient_count', default=0)} |")
        lines.append(f"| OBSERVATIONAL | {_val(summary, 'observational_count', default=0)} |")
        lines.append(f"| VALIDATING | {_val(summary, 'validating_count', default=0)} |")
        lines.append(f"| VALIDATED | {_val(summary, 'validated_count', default=0)} |")
        lines.append(f"| CONFLICTED | {_val(summary, 'conflicted_count', default=0)} |")
        lines.append(f"| REJECTED | {_val(summary, 'rejected_count', default=0)} |")
        avg = _val(summary, "avg_score", default="—")
        lines.append(f"| Avg Score | {avg} |")
        lines.append(f"| Forbidden Actions | {_val(summary, 'forbidden_action_count', default=0)} |")
        return lines

    def _section_grade_board(self, scores: list) -> List[str]:
        lines = ["## 二、Validation Grade Board", ""]
        if not scores:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        sorted_scores = sorted(
            scores,
            key=lambda s: float(_val(s, "final_score", default=0)),
            reverse=True,
        )[:20]

        lines.append("| Grade | Score | Strategy | Type | Source | Status | Next Step |")
        lines.append("|-------|-------|----------|------|--------|--------|-----------|")
        for s in sorted_scores:
            grade = _val(s, "validation_grade", default="—")
            score = _val(s, "final_score", default="—")
            strategy = _val(s, "strategy_name", default="—")
            stype = _val(s, "strategy_type", default="—")
            source = _val(s, "validation_id", default="—")
            status = _val(s, "status", default="—")
            next_step = _safe(_val(s, "suggested_next_step", default="—"))
            if str(grade).upper() == "VALIDATED":
                grade = "VALIDATED (research only)"
            lines.append(
                f"| {grade} | {score} | {strategy} | {stype} | {source} | {status} | {next_step} |"
            )
        return lines

    def _section_validated_rules(self, scores: list) -> List[str]:
        lines = ["## 三、Validated Research Rules", ""]
        lines.append(
            "> Note: VALIDATED = research evidence supports this rule."
            " **Does NOT enable trading or generate orders.**"
        )
        lines.append("")
        validated = [
            s for s in scores
            if str(_val(s, "validation_grade", default="")).upper() == "VALIDATED"
        ]
        if not validated:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        lines.append("| Strategy | Supporting Evidence | Limitation | Note |")
        lines.append("|----------|---------------------|------------|------|")
        for s in validated:
            strategy = _val(s, "strategy_name", default="—")
            reason = _val(s, "reason", default="—")
            limitation = _val(s, "limitations", default="—")
            lines.append(
                f"| {strategy} | {reason} | {limitation}"
                " | Research validated only — does not enable trading |"
            )
        return lines

    def _section_observational_validating(self, scores: list) -> List[str]:
        lines = ["## 四、Observational / Validating Rules", ""]
        filtered = [
            s for s in scores
            if str(_val(s, "validation_grade", default="")).upper()
            in ("OBSERVATIONAL", "VALIDATING")
        ]
        if not filtered:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        lines.append(
            "| Strategy | Grade | What Evidence Exists | What Is Still Missing | Required Actions |"
        )
        lines.append("|----------|-------|---------------------|----------------------|------------------|")
        for s in filtered:
            strategy = _val(s, "strategy_name", default="—")
            grade = _val(s, "validation_grade", default="—")
            reason = _val(s, "reason", default="—")
            limitation = _val(s, "limitations", default="—")
            next_step = _safe(_val(s, "suggested_next_step", default="—"))
            lines.append(
                f"| {strategy} | {grade} | {reason} | {limitation} | {next_step} |"
            )
        return lines

    def _section_conflicted_rejected(self, scores: list) -> List[str]:
        lines = ["## 五、Conflicted / Rejected Rules", ""]
        filtered = [
            s for s in scores
            if str(_val(s, "validation_grade", default="")).upper()
            in ("CONFLICTED", "REJECTED")
        ]
        if not filtered:
            lines.append(
                "> No conflicted or rejected strategies at this time."
            )
            return lines

        lines.append("| Strategy | Issue | Contradictions | Risk Guard | Why |")
        lines.append("|----------|-------|----------------|------------|-----|")
        for s in filtered:
            strategy = _val(s, "strategy_name", default="—")
            grade = _val(s, "validation_grade", default="—")
            reason = _val(s, "reason", default="—")
            limitation = _val(s, "limitations", default="—")
            status = _val(s, "status", default="—")
            lines.append(
                f"| {strategy} | {grade} | {reason} | {status} | {limitation} |"
            )
        return lines

    def _section_crash_reversal(self, scores: list) -> List[str]:
        lines = ["## 六、Crash Reversal Strategy Validation", ""]
        _CRASH_RULES = [
            "Crash Cause Classifier",
            "Post-Crash Stabilization Checklist",
            "Relative Strength After Crash Score",
            "Sakata EPS-backed Dip Buy Filter",
            "Moving Average Profit Discipline",
            "High-Risk Industry Exposure Guard",
        ]

        crash_scores = [
            s for s in scores
            if str(_val(s, "strategy_type", default="")).upper() in (
                "CRASH_REVERSAL_RULE", "CRASH_REVERSAL"
            )
            or any(
                r.lower() in str(_val(s, "strategy_name", default="")).lower()
                for r in _CRASH_RULES
            )
        ]

        if not crash_scores:
            lines.append(
                "> Run strategy-validation --mode real first"
            )
            lines.append("")
            lines.append("**Expected 6 Crash Reversal rules:**")
            for rule in _CRASH_RULES:
                lines.append(f"- {rule}")
            return lines

        lines.append(
            "| Rule | Score | Grade | Evidence | Risk Penalty | Next Step |"
        )
        lines.append(
            "|------|-------|-------|----------|--------------|-----------|"
        )
        for s in crash_scores:
            rule = _val(s, "strategy_name", default="—")
            score = _val(s, "final_score", default="—")
            grade = _val(s, "validation_grade", default="—")
            if str(grade).upper() == "VALIDATED":
                grade = "VALIDATED (research only)"
            reason = _val(s, "reason", default="—")
            limitation = _val(s, "limitations", default="—")
            next_step = _safe(_val(s, "suggested_next_step", default="—"))
            lines.append(
                f"| {rule} | {score} | {grade} | {reason} | {limitation} | {next_step} |"
            )
        return lines

    def _section_evidence_components(self, components: list) -> List[str]:
        lines = ["## 七、Evidence Components", ""]
        if not components:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        sorted_components = sorted(
            components,
            key=lambda c: float(_val(c, "weighted_score", default=0)),
            reverse=True,
        )[:10]

        lines.append(
            "| Strategy | Component | Score | Weight | Weighted Score | Evidence | Limitation |"
        )
        lines.append(
            "|----------|-----------|-------|--------|----------------|----------|------------|"
        )
        for c in sorted_components:
            strategy = _val(c, "strategy_name", default=_val(c, "strategy_id", default="—"))
            component = _val(c, "component", default="—")
            score = _val(c, "score", default="—")
            weight = _val(c, "weight", default="—")
            weighted = _val(c, "weighted_score", default="—")
            evidence = _val(c, "evidence", default="—")
            limitation = _val(c, "limitation", default="—")
            lines.append(
                f"| {strategy} | {component} | {score} | {weight} | {weighted}"
                f" | {evidence} | {limitation} |"
            )
        return lines

    def _section_safe_next_steps(self, scores: list) -> List[str]:
        lines = ["## 八、Suggested Safe Next Steps", ""]
        lines.append(
            "> All suggestions are research actions only."
            " No BUY/SELL/ORDER instructions."
        )
        lines.append("")

        if not scores:
            lines.append(f"> {_MISSING_DATA_MSG}")
            return lines

        step_counts: dict = {}
        for s in scores:
            step = _safe(_val(s, "suggested_next_step", default=""))
            if step and step != "—":
                step_counts[step] = step_counts.get(step, 0) + 1

        if not step_counts:
            lines.append("> No next steps available — run validation first.")
            return lines

        lines.append("| Suggested Next Step | Count |")
        lines.append("|---------------------|-------|")
        for step, count in sorted(step_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {step} | {count} |")

        return lines

    def _section_safety_declaration(self) -> List[str]:
        lines = ["## 九、安全聲明", ""]
        lines.append(
            "| Safety Guarantee | Status |"
        )
        lines.append("|------------------|--------|")
        lines.append(
            "| Research Only: All outputs are for research purposes only | **YES** |"
        )
        lines.append(
            "| No Real Orders: This system never places orders | **YES** |"
        )
        lines.append(
            "| No broker execution: Not connected to any broker | **YES** |"
        )
        lines.append(
            "| No auto trading: Strategy validation does not enable automated trading | **YES** |"
        )
        lines.append(
            "| VALIDATED does not enable trading: A VALIDATED grade means research validated only"
            " | **YES** |"
        )
        lines.append(
            "| Not investment advice | **YES** |"
        )
        lines.append("")
        lines.append(
            "> **VALIDATED** = The research evidence supports this strategy rule."
            " It is a research conclusion, not a trading signal."
            " No real orders are placed. Production trading remains BLOCKED."
        )
        return lines
