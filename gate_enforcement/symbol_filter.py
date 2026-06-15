"""
gate_enforcement.symbol_filter — QualityGateSymbolFilter v1.1.5

Filters symbols by required gate level based on quality gate decisions.
Research Only. No Real Orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.

Filtering rules:
- FORMAL run: only ELIGIBLE_FORMAL
- OBSERVATIONAL run: ELIGIBLE_FORMAL + ELIGIBLE_OBSERVATIONAL (NOT DEMO_ONLY/BLOCKED)
- DEMO run: FORMAL/OBSERVATIONAL/DEMO_ONLY — NOT integrity-blocked
  (INVALID/CONFLICT/FUTURE_DATE) — label DEMO_ONLY
- OFF: preserve original, generate audit warning, cannot claim formal
- No eligible symbols => status=BLOCKED, friendly console, no crash
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from gate_enforcement.enforcement_schema import SymbolExclusionRecord
from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

# Decision constants (mirrors quality_gates.gate_schema)
DECISION_ELIGIBLE_FORMAL = "ELIGIBLE_FORMAL"
DECISION_ELIGIBLE_OBSERVATIONAL = "ELIGIBLE_OBSERVATIONAL"
DECISION_DEMO_ONLY = "DEMO_ONLY"
DECISION_BLOCKED = "BLOCKED"
DECISION_INVALID = "INVALID"
DECISION_CONFLICT = "CONFLICT"
DECISION_FUTURE_DATE = "FUTURE_DATE"

# Integrity-blocked decisions (cannot even be in DEMO)
_INTEGRITY_BLOCKED = {DECISION_INVALID, DECISION_CONFLICT, DECISION_FUTURE_DATE}

# Also treat any decision starting with BLOCKED_ as blocked
def _is_blocked(decision: str) -> bool:
    if decision in _INTEGRITY_BLOCKED:
        return True
    if decision == DECISION_BLOCKED:
        return True
    if str(decision).startswith("BLOCKED_"):
        return True
    return False

def _is_formal(decision: str) -> bool:
    return decision == DECISION_ELIGIBLE_FORMAL

def _is_observational(decision: str) -> bool:
    return decision == DECISION_ELIGIBLE_OBSERVATIONAL

def _is_demo_only(decision: str) -> bool:
    return decision == DECISION_DEMO_ONLY


class QualityGateSymbolFilter:
    """
    Filters symbols by requested level based on quality gate decisions.
    The decisions dict maps symbol -> decision string.
    """

    def __init__(self):
        self._policy = QualityGateEnforcementPolicy()

    def filter_symbols(
        self, symbols: List[str], decisions: Dict[str, str], required_level: str
    ) -> dict:
        """
        Main filter method. Returns a result dict with:
          included, excluded, formal, observational, demo, blocked,
          exclusion_records, status, warnings
        """
        warnings = []
        if required_level == "FORMAL":
            included = self.include_formal(symbols, decisions)
            excluded = [s for s in symbols if s not in included]
            formal = list(included)
            observational = []
            demo = []
        elif required_level == "OBSERVATIONAL":
            formal = self.include_formal(symbols, decisions)
            observational = self.include_observational(symbols, decisions)
            included = sorted(set(formal + observational))
            excluded = [s for s in symbols if s not in included]
            demo = []
        elif required_level == "DEMO":
            included = self.include_demo(symbols, decisions)
            excluded = [s for s in symbols if s not in included]
            formal = [s for s in included if _is_formal(decisions.get(s, ""))]
            observational = [s for s in included if _is_observational(decisions.get(s, ""))]
            demo = [s for s in included if not _is_formal(decisions.get(s, "")) and not _is_observational(decisions.get(s, ""))]
            if demo:
                warnings.append("DEMO_ONLY symbols included — results NOT formally qualified")
        elif required_level == "OFF":
            included = list(symbols)
            excluded = []
            formal = []
            observational = []
            demo = []
            warnings.append(self._policy.off_mode_label())
            warnings.append("OFF mode: results cannot claim formal qualification")
        else:
            # Unknown level — treat as BLOCKED
            included = []
            excluded = list(symbols)
            formal = []
            observational = []
            demo = []
            warnings.append(f"Unknown requested_level={required_level} — all symbols excluded")

        blocked = self.exclude_blocked(symbols, decisions)
        exclusion_records = self.build_exclusion_records(symbols, decisions, included, required_level)

        if not included:
            status = "BLOCKED"
            warnings.append("No eligible symbols after gate filtering. Run is BLOCKED.")
            logger.warning(
                "Gate filter: 0 symbols included for level=%s. Run is BLOCKED. "
                "Check quality gate decisions for your symbols.",
                required_level,
            )
        elif required_level == "FORMAL" and not formal:
            status = "BLOCKED"
            warnings.append("No FORMAL-eligible symbols. Run is BLOCKED for formal analysis.")
        elif required_level == "OBSERVATIONAL" and not included:
            status = "OBSERVATIONAL_ONLY"
        elif required_level == "DEMO":
            if demo and not formal and not observational:
                status = "DEMO_ONLY"
            else:
                status = "PASSED_WITH_WARNINGS" if warnings else "PASSED"
        elif warnings:
            status = "PASSED_WITH_WARNINGS"
        else:
            status = "PASSED"

        return {
            "included": included,
            "excluded": excluded,
            "formal": formal,
            "observational": observational,
            "demo": demo,
            "blocked": blocked,
            "exclusion_records": exclusion_records,
            "status": status,
            "warnings": warnings,
        }

    def include_formal(self, symbols: List[str], decisions: Dict[str, str]) -> List[str]:
        return [s for s in symbols if _is_formal(decisions.get(s, ""))]

    def include_observational(self, symbols: List[str], decisions: Dict[str, str]) -> List[str]:
        """Returns ELIGIBLE_OBSERVATIONAL symbols (not DEMO_ONLY or BLOCKED)."""
        return [
            s for s in symbols
            if _is_observational(decisions.get(s, ""))
        ]

    def include_demo(self, symbols: List[str], decisions: Dict[str, str]) -> List[str]:
        """FORMAL + OBSERVATIONAL + DEMO_ONLY, excluding integrity-blocked."""
        return [
            s for s in symbols
            if not _is_blocked(decisions.get(s, "BLOCKED"))
        ]

    def exclude_blocked(self, symbols: List[str], decisions: Dict[str, str]) -> List[str]:
        return [s for s in symbols if _is_blocked(decisions.get(s, "BLOCKED"))]

    def build_exclusion_records(
        self, symbols: List[str], decisions: Dict[str, str],
        included: List[str], required_level: str, run_id: str = ""
    ) -> List[SymbolExclusionRecord]:
        records = []
        included_set = set(included)
        for symbol in symbols:
            decision = decisions.get(symbol, "UNKNOWN")
            excluded = symbol not in included_set
            if excluded:
                reason_codes, reasons, required_actions = self._explain_exclusion(
                    decision, required_level
                )
                records.append(SymbolExclusionRecord(
                    run_id=run_id,
                    symbol=symbol,
                    gate_name="",
                    original_decision=decision,
                    required_level=required_level,
                    excluded=True,
                    reason_codes=reason_codes,
                    reasons=reasons,
                    required_actions=required_actions,
                    override_applied=False,
                    override_id=None,
                    evaluated_at="",
                ))
        return records

    def _explain_exclusion(self, decision: str, required_level: str):
        if _is_formal(decision):
            # Formal symbol excluded from non-formal? Shouldn't happen.
            return [], [], []
        if _is_observational(decision):
            if required_level == "FORMAL":
                return (
                    ["NOT_FORMAL_ELIGIBLE"],
                    ["Symbol is OBSERVATIONAL only; FORMAL requires higher data quality"],
                    ["FIX_DATA", "WAIT"],
                )
        if _is_demo_only(decision):
            if required_level in ("FORMAL", "OBSERVATIONAL"):
                return (
                    ["DEMO_ONLY_DATA"],
                    ["Symbol is DEMO_ONLY; not eligible for FORMAL/OBSERVATIONAL analysis"],
                    ["PROVIDE_SOURCE_DATA", "FIX_DATA"],
                )
        if _is_blocked(decision):
            return (
                ["BLOCKED_DATA"],
                [f"Symbol is blocked (decision={decision}); cannot be included in any formal run"],
                ["REVIEW", "FIX_DATA"],
            )
        return (
            [f"UNKNOWN_DECISION_{decision}"],
            [f"Unknown decision: {decision}"],
            ["REVIEW"],
        )

    def summarize_filter(self, filter_result: dict) -> dict:
        return {
            "included_count": len(filter_result.get("included", [])),
            "excluded_count": len(filter_result.get("excluded", [])),
            "formal_count": len(filter_result.get("formal", [])),
            "observational_count": len(filter_result.get("observational", [])),
            "demo_count": len(filter_result.get("demo", [])),
            "blocked_count": len(filter_result.get("blocked", [])),
            "status": filter_result.get("status", "UNKNOWN"),
            "warnings": filter_result.get("warnings", []),
        }

    def explain_exclusions(self, filter_result: dict) -> List[str]:
        explanations = []
        for record in filter_result.get("exclusion_records", []):
            reasons = record.reasons if hasattr(record, "reasons") else record.get("reasons", [])
            sym = record.symbol if hasattr(record, "symbol") else record.get("symbol", "?")
            explanations.append(f"{sym}: {'; '.join(reasons) if reasons else 'excluded'}")
        return explanations
