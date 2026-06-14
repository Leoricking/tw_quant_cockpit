"""
quality_gates.symbol_gate_evaluator — Per-symbol quality gate evaluation v1.1.4

Research-only. Evaluates a single symbol against any of the 12 defined quality
gates. Gracefully degrades when optional integrations (universe, freshness,
coverage_repair, onboarding) are unavailable. No broker connectivity.
No order placement.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from quality_gates.gate_schema import (
    CONFIDENCE_DEMO_ONLY,
    CONFIDENCE_INSUFFICIENT,
    CONFIDENCE_OBSERVATIONAL,
    CONFIDENCE_RELIABLE,
    CONFIDENCE_UNKNOWN,
    DECISION_BLOCKED_DATA_QUALITY,
    DECISION_BLOCKED_FRESHNESS,
    DECISION_BLOCKED_INSUFFICIENT_HISTORY,
    DECISION_BLOCKED_INVALID_DATA,
    DECISION_BLOCKED_MISSING_PRICE,
    DECISION_BLOCKED_MOCK_DATA,
    DECISION_BLOCKED_SOURCE_UNKNOWN,
    DECISION_DEMO_ONLY,
    DECISION_ELIGIBLE_FORMAL,
    DECISION_ELIGIBLE_OBSERVATIONAL,
    GATE_LEVEL_BLOCKED,
    GATE_LEVEL_DEMO,
    GATE_LEVEL_FORMAL,
    GATE_LEVEL_OBSERVATIONAL,
    QualityGateDecision,
    QualityGateInput,
    RC_CHIPS_MISSING,
    RC_CONFLICTING_ROWS,
    RC_COVERAGE_UNKNOWN,
    RC_CRITICAL_REPAIR_OPEN,
    RC_DATE_REGRESSION,
    RC_DAILY_COMPLETENESS_LOW,
    RC_DAILY_PRICE_STALE,
    RC_DUPLICATE_ROWS,
    RC_FIXTURE_SOURCE,
    RC_FRESHNESS_UNKNOWN,
    RC_FUNDAMENTALS_MISSING,
    RC_FUTURE_DATE,
    RC_HISTORY_INSUFFICIENT,
    RC_INVALID_OHLC,
    RC_INVALID_VOLUME,
    RC_MANUAL_REVIEW_OPEN,
    RC_MOCK_SOURCE,
    RC_PRICE_DATA_MISSING,
    RC_REVENUE_MISSING,
    RC_SECTOR_DATA_MISSING,
    RC_SHORT_INTEREST_MISSING,
    RC_SOURCE_INTERRUPTED,
    RC_SOURCE_UNKNOWN,
    REASON_CODE_METADATA,
)
from quality_gates.gate_policy import (
    ALL_GATES,
    CoverageQualityGatePolicy,
)


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class SymbolQualityGateEvaluator:
    """Evaluates a single symbol against one or all quality gates."""

    def __init__(self, repo_path: Optional[str] = None):
        self._repo_path = repo_path or BASE_DIR
        self._policy: Optional[CoverageQualityGatePolicy] = None

    @property
    def policy(self) -> CoverageQualityGatePolicy:
        if self._policy is None:
            self._policy = CoverageQualityGatePolicy()
        return self._policy

    # ------------------------------------------------------------------
    # Input building
    # ------------------------------------------------------------------

    def build_input(self, symbol: str, gate_name: str, mode: str = "real") -> QualityGateInput:
        """
        Assemble QualityGateInput from all available integrations.
        Each integration block degrades gracefully on ImportError or any Exception.
        """
        inp = QualityGateInput(symbol=symbol, mode=mode)

        # --- Universe / coverage data ---
        try:
            from data_coverage import coverage_store  # type: ignore
            cov = coverage_store.get_coverage(symbol)
            if cov:
                inp.name = cov.get("name", "")
                inp.tier = cov.get("tier", "unknown")
                inp.source_type = cov.get("source_type", "unknown")
                inp.daily_status = cov.get("daily_status", "UNKNOWN")
                inp.daily_rows = int(cov.get("daily_rows", 0))
                inp.daily_completeness = float(cov.get("daily_completeness", 0.0))
                inp.first_date = cov.get("first_date", "")
                inp.last_date = cov.get("last_date", "")
                inp.trading_days = int(cov.get("trading_days", 0))
                inp.missing_ratio = float(cov.get("missing_ratio", 0.0))
                inp.duplicate_count = int(cov.get("duplicate_count", 0))
                inp.conflict_count = int(cov.get("conflict_count", 0))
                inp.invalid_ohlc_count = int(cov.get("invalid_ohlc_count", 0))
                inp.invalid_volume_count = int(cov.get("invalid_volume_count", 0))
                inp.future_date_detected = bool(cov.get("future_date_detected", False))
                inp.date_regression_detected = bool(cov.get("date_regression_detected", False))
                inp.chips_status = cov.get("chips_status", "UNKNOWN")
                inp.revenue_status = cov.get("revenue_status", "UNKNOWN")
                inp.fundamental_status = cov.get("fundamental_status", "UNKNOWN")
                inp.data_origin = cov.get("data_origin", "UNKNOWN")
        except ImportError:
            logger.warning("data_coverage not available — using defaults for %s", symbol)
        except Exception as exc:
            logger.warning("data_coverage error for %s: %s", symbol, exc)

        # --- Freshness data ---
        try:
            from data_freshness import freshness_store  # type: ignore
            fresh = freshness_store.get_freshness(symbol)
            if fresh:
                inp.freshness_status = fresh.get("freshness_status", "UNKNOWN")
                inp.trading_day_lag = int(fresh.get("trading_day_lag", -1))
                inp.source_health = fresh.get("source_health", "UNKNOWN")
        except ImportError:
            logger.warning("data_freshness not available — using defaults for %s", symbol)
        except Exception as exc:
            logger.warning("data_freshness error for %s: %s", symbol, exc)

        # --- Coverage repair issues ---
        try:
            from coverage_repair import repair_store  # type: ignore
            issues = repair_store.get_open_issues(symbol)
            if issues:
                inp.open_repair_issue_count = len(issues)
                inp.critical_repair_issue_count = sum(
                    1 for i in issues if i.get("severity", "") == "CRITICAL"
                )
                inp.unresolved_manual_review_count = sum(
                    1 for i in issues if i.get("type", "") == "MANUAL_REVIEW"
                )
        except ImportError:
            logger.warning("coverage_repair not available — using defaults for %s", symbol)
        except Exception as exc:
            logger.warning("coverage_repair error for %s: %s", symbol, exc)

        # --- Onboarding / statistical confidence ---
        try:
            from data_onboarding import onboarding_store  # type: ignore
            onb = onboarding_store.get_status(symbol)
            if onb:
                inp.statistical_confidence = onb.get("statistical_confidence", "UNKNOWN")
        except ImportError:
            logger.warning("data_onboarding not available — using defaults for %s", symbol)
        except Exception as exc:
            logger.warning("data_onboarding error for %s: %s", symbol, exc)

        # --- Mock / fixture detection ---
        if mode == "mock" or "mock" in inp.source_type.lower() or "fixture" in inp.source_type.lower():
            inp.mock_detected = True
            inp.source_type = "mock"
            inp.evidence = (inp.evidence + " mock_detected").strip()

        if symbol.startswith("TST"):
            inp.evidence = (inp.evidence + " test_fixture").strip()
            inp.mock_detected = True

        return inp

    # ------------------------------------------------------------------
    # Evaluation entry points
    # ------------------------------------------------------------------

    def evaluate(self, symbol: str, gate_name: str, mode: str = "real") -> QualityGateDecision:
        """Build input from integrations then evaluate."""
        gate_input = self.build_input(symbol, gate_name, mode=mode)
        return self.evaluate_input(gate_input, gate_name)

    def evaluate_input(self, gate_input: QualityGateInput, gate_name: str) -> QualityGateDecision:
        """Full evaluation pipeline given a pre-built QualityGateInput."""
        req_result = self.evaluate_required_datasets(gate_input, gate_name)
        opt_result = self.evaluate_optional_datasets(gate_input, gate_name)
        hist_result = self.evaluate_history(gate_input, gate_name)
        integrity_result = self.evaluate_integrity(gate_input, gate_name)
        fresh_result = self.evaluate_freshness(gate_input, gate_name)
        source_result = self.evaluate_source(gate_input, gate_name)
        repair_result = self.evaluate_repairs(gate_input, gate_name)
        conf_result = self.evaluate_confidence(gate_input, gate_name)

        all_results = {
            "required_datasets": req_result,
            "optional_datasets": opt_result,
            "history": hist_result,
            "integrity": integrity_result,
            "freshness": fresh_result,
            "source": source_result,
            "repairs": repair_result,
            "confidence": conf_result,
        }

        blocking_codes, warning_codes, reasons = self.build_reason_codes(all_results)
        required_actions = self.build_required_actions(blocking_codes, warning_codes)
        return self.build_decision(
            gate_input, gate_name, blocking_codes, warning_codes, reasons, required_actions
        )

    # ------------------------------------------------------------------
    # Individual evaluation checks
    # ------------------------------------------------------------------

    def evaluate_required_datasets(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check required datasets availability."""
        required = self.policy.required_datasets(gate_name)
        results: dict = {}

        for ds in required:
            if ds == "daily_price":
                available = gate_input.daily_rows > 0 and gate_input.daily_status != "MISSING"
                results[ds] = {"available": available, "status": gate_input.daily_status}
            elif ds == "revenue":
                missing_vals = ("UNKNOWN", "MISSING")
                available = gate_input.revenue_status not in missing_vals
                results[ds] = {"available": available, "status": gate_input.revenue_status}
            elif ds == "fundamentals":
                missing_vals = ("UNKNOWN", "MISSING")
                available = gate_input.fundamental_status not in missing_vals
                results[ds] = {"available": available, "status": gate_input.fundamental_status}
            elif ds == "short_interest":
                # No dedicated short_interest_status field; use chips_status as proxy
                missing_vals = ("UNKNOWN", "MISSING")
                available = gate_input.chips_status not in missing_vals
                results[ds] = {
                    "available": available,
                    "status": gate_input.chips_status,
                    "note": "approximated via chips_status field",
                }
            elif ds == "sector_data":
                # No dedicated sector field — mark as missing, add warning
                results[ds] = {
                    "available": False,
                    "status": "UNKNOWN",
                    "note": "no sector_data field in gate_input",
                }
            else:
                results[ds] = {"available": False, "status": "UNKNOWN"}

        return results

    def evaluate_optional_datasets(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check optional datasets — produces warnings, not blocking."""
        optional = self.policy.optional_datasets(gate_name)
        results: dict = {}

        for ds in optional:
            if ds == "volume":
                available = gate_input.invalid_volume_count == 0
                results[ds] = {"available": available, "status": "OK" if available else "INVALID"}
            elif ds == "chips":
                available = gate_input.chips_status not in ("UNKNOWN", "MISSING")
                results[ds] = {"available": available, "status": gate_input.chips_status}
            elif ds == "revenue":
                available = gate_input.revenue_status not in ("UNKNOWN", "MISSING")
                results[ds] = {"available": available, "status": gate_input.revenue_status}
            elif ds == "fundamentals":
                available = gate_input.fundamental_status not in ("UNKNOWN", "MISSING")
                results[ds] = {"available": available, "status": gate_input.fundamental_status}
            elif ds == "sector_data":
                results[ds] = {"available": False, "status": "UNKNOWN", "note": "no sector_data field"}
            else:
                results[ds] = {"available": False, "status": "UNKNOWN"}

        return results

    def evaluate_history(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check trading day history vs formal/observational thresholds."""
        formal_min = self.policy.minimum_rows(gate_name, "formal")
        obs_min = self.policy.minimum_rows(gate_name, "observational")
        rows = gate_input.daily_rows
        days = max(gate_input.trading_days, rows)  # use whichever is larger

        formal_ok = days >= formal_min
        obs_ok = days >= obs_min

        blocking_codes = []
        if not obs_ok:
            blocking_codes.append(RC_HISTORY_INSUFFICIENT)

        return {
            "formal_ok": formal_ok,
            "observational_ok": obs_ok,
            "rows": rows,
            "trading_days": gate_input.trading_days,
            "formal_min": formal_min,
            "obs_min": obs_min,
            "blocking_codes": blocking_codes,
        }

    def evaluate_integrity(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check OHLC, conflict, duplicate, future-date, date-regression integrity."""
        codes = []

        if gate_input.invalid_ohlc_count > 0:
            codes.append(RC_INVALID_OHLC)
        if gate_input.conflict_count > 0:
            codes.append(RC_CONFLICTING_ROWS)
        if gate_input.duplicate_count > 0:
            codes.append(RC_DUPLICATE_ROWS)
        if gate_input.future_date_detected:
            codes.append(RC_FUTURE_DATE)
        if gate_input.date_regression_detected:
            codes.append(RC_DATE_REGRESSION)
        if gate_input.invalid_volume_count > 0:
            codes.append(RC_INVALID_VOLUME)

        policy_blocking = self.policy.blocking_reason_codes(gate_name)
        blocking_codes = [c for c in codes if c in policy_blocking]
        warn_codes = [c for c in codes if c not in policy_blocking]

        return {
            "clean": len(blocking_codes) == 0,
            "blocking_codes": blocking_codes,
            "warn_codes": warn_codes,
        }

    def evaluate_freshness(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check freshness_status against allowed values for this gate."""
        allowed = self.policy.allowed_freshness(gate_name)
        policy_blocking = self.policy.blocking_reason_codes(gate_name)

        freshness = gate_input.freshness_status
        blocking_codes = []
        warn_codes = []

        if freshness == "UNKNOWN":
            warn_codes.append(RC_FRESHNESS_UNKNOWN)
        elif freshness not in allowed:
            if RC_DAILY_PRICE_STALE in policy_blocking:
                blocking_codes.append(RC_DAILY_PRICE_STALE)
            else:
                warn_codes.append(RC_DAILY_PRICE_STALE)

        if gate_input.source_health == "INTERRUPTED":
            if RC_SOURCE_INTERRUPTED in policy_blocking:
                blocking_codes.append(RC_SOURCE_INTERRUPTED)
            else:
                warn_codes.append(RC_SOURCE_INTERRUPTED)

        return {
            "freshness_ok": len(blocking_codes) == 0,
            "freshness_status": freshness,
            "allowed": allowed,
            "blocking_codes": blocking_codes,
            "warn_codes": warn_codes,
        }

    def evaluate_source(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check for mock/fixture sources and unknown origins."""
        blocking_codes = []
        warn_codes = []
        policy_blocking = self.policy.blocking_reason_codes(gate_name)

        if gate_input.mock_detected:
            if RC_MOCK_SOURCE in policy_blocking:
                blocking_codes.append(RC_MOCK_SOURCE)
            else:
                warn_codes.append(RC_MOCK_SOURCE)

        if "fixture" in gate_input.evidence.lower() or "fixture" in gate_input.source_type.lower():
            if RC_FIXTURE_SOURCE in policy_blocking:
                blocking_codes.append(RC_FIXTURE_SOURCE)
            else:
                warn_codes.append(RC_FIXTURE_SOURCE)

        if gate_input.source_type in ("unknown", "UNKNOWN") and gate_input.data_origin in ("UNKNOWN", "unknown"):
            warn_codes.append(RC_SOURCE_UNKNOWN)

        return {
            "source_ok": len(blocking_codes) == 0,
            "blocking_codes": blocking_codes,
            "warn_codes": warn_codes,
        }

    def evaluate_repairs(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Check open repair and manual review issues."""
        blocking_codes = []
        warn_codes = []
        policy_blocking = self.policy.blocking_reason_codes(gate_name)

        if gate_input.critical_repair_issue_count > 0:
            if RC_CRITICAL_REPAIR_OPEN in policy_blocking:
                blocking_codes.append(RC_CRITICAL_REPAIR_OPEN)
            else:
                warn_codes.append(RC_CRITICAL_REPAIR_OPEN)

        if gate_input.unresolved_manual_review_count > 0:
            if RC_MANUAL_REVIEW_OPEN in policy_blocking:
                blocking_codes.append(RC_MANUAL_REVIEW_OPEN)
            else:
                warn_codes.append(RC_MANUAL_REVIEW_OPEN)

        return {
            "repairs_ok": len(blocking_codes) == 0,
            "blocking_codes": blocking_codes,
            "warn_codes": warn_codes,
        }

    def evaluate_confidence(self, gate_input: QualityGateInput, gate_name: str) -> dict:
        """Map statistical_confidence field to CONFIDENCE_* constants."""
        sc = gate_input.statistical_confidence.upper() if gate_input.statistical_confidence else "UNKNOWN"

        if sc in ("HIGH", "RELIABLE", "STRONG"):
            mapped = CONFIDENCE_RELIABLE
        elif sc in ("MEDIUM", "OBSERVATIONAL", "MODERATE"):
            mapped = CONFIDENCE_OBSERVATIONAL
        elif sc in ("LOW", "INSUFFICIENT", "WEAK"):
            mapped = CONFIDENCE_INSUFFICIENT
        elif sc in ("DEMO", "DEMO_ONLY", "MOCK"):
            mapped = CONFIDENCE_DEMO_ONLY
        else:
            mapped = CONFIDENCE_UNKNOWN

        return {"confidence": mapped, "raw": sc}

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def build_reason_codes(self, eval_results: dict) -> tuple:
        """
        Aggregate blocking_codes, warning_codes, and human reasons from
        all evaluation sub-results.

        Returns (blocking_codes, warning_codes, reasons)
        """
        blocking_codes: list = []
        warning_codes: list = []
        reasons: list = []

        def _add_blocking(code: str) -> None:
            if code not in blocking_codes:
                blocking_codes.append(code)
                meta = REASON_CODE_METADATA.get(code, {})
                reasons.append(f"[BLOCKING] {meta.get('explanation', code)}")

        def _add_warning(code: str) -> None:
            if code not in warning_codes:
                warning_codes.append(code)
                meta = REASON_CODE_METADATA.get(code, {})
                reasons.append(f"[WARNING] {meta.get('explanation', code)}")

        # Required datasets
        req = eval_results.get("required_datasets", {})
        for ds, info in req.items():
            if not info.get("available", True):
                code_map = {
                    "daily_price": RC_PRICE_DATA_MISSING,
                    "revenue": RC_REVENUE_MISSING,
                    "fundamentals": RC_FUNDAMENTALS_MISSING,
                    "short_interest": RC_SHORT_INTEREST_MISSING,
                    "sector_data": RC_SECTOR_DATA_MISSING,
                }
                code = code_map.get(ds)
                if code:
                    _add_blocking(code)

        # Optional datasets
        opt = eval_results.get("optional_datasets", {})
        for ds, info in opt.items():
            if not info.get("available", True):
                code_map = {
                    "chips": RC_CHIPS_MISSING,
                    "revenue": RC_REVENUE_MISSING,
                    "fundamentals": RC_FUNDAMENTALS_MISSING,
                    "sector_data": RC_SECTOR_DATA_MISSING,
                }
                code = code_map.get(ds)
                if code:
                    _add_warning(code)

        # History
        hist = eval_results.get("history", {})
        for code in hist.get("blocking_codes", []):
            _add_blocking(code)

        # Integrity
        integ = eval_results.get("integrity", {})
        for code in integ.get("blocking_codes", []):
            _add_blocking(code)
        for code in integ.get("warn_codes", []):
            _add_warning(code)

        # Freshness
        fresh = eval_results.get("freshness", {})
        for code in fresh.get("blocking_codes", []):
            _add_blocking(code)
        for code in fresh.get("warn_codes", []):
            _add_warning(code)

        # Source
        src = eval_results.get("source", {})
        for code in src.get("blocking_codes", []):
            _add_blocking(code)
        for code in src.get("warn_codes", []):
            _add_warning(code)

        # Repairs
        rep = eval_results.get("repairs", {})
        for code in rep.get("blocking_codes", []):
            _add_blocking(code)
        for code in rep.get("warn_codes", []):
            _add_warning(code)

        # Completeness check (derives from history + coverage data indirectly)
        # handled via history blocking_codes above

        return blocking_codes, warning_codes, reasons

    def build_required_actions(
        self, blocking_codes: list, warning_codes: list
    ) -> list:
        """Map reason codes to safe_actions (deduplicated, ordered)."""
        seen: set = set()
        actions: list = []
        for code in blocking_codes + warning_codes:
            meta = REASON_CODE_METADATA.get(code, {})
            action = meta.get("safe_action", "REVIEW")
            if action not in seen:
                seen.add(action)
                actions.append(action)
        return actions

    def build_decision(
        self,
        gate_input: QualityGateInput,
        gate_name: str,
        blocking_codes: list,
        warning_codes: list,
        reasons: list,
        required_actions: list,
    ) -> QualityGateDecision:
        """Assemble the final QualityGateDecision from all evaluation outputs."""

        # --- Determine decision and gate level ---
        decision_str = DECISION_BLOCKED_DATA_QUALITY
        gate_level = GATE_LEVEL_BLOCKED
        eligible = False
        confidence = CONFIDENCE_UNKNOWN

        # Mock/fixture always blocked to DEMO_ONLY
        if gate_input.mock_detected:
            decision_str = DECISION_BLOCKED_MOCK_DATA
            gate_level = GATE_LEVEL_BLOCKED
            confidence = CONFIDENCE_DEMO_ONLY
        elif blocking_codes:
            # Priority ordering for decision label
            if RC_PRICE_DATA_MISSING in blocking_codes:
                decision_str = DECISION_BLOCKED_MISSING_PRICE
            elif any(c in blocking_codes for c in (
                RC_INVALID_OHLC, RC_CONFLICTING_ROWS, RC_FUTURE_DATE, RC_DATE_REGRESSION
            )):
                decision_str = DECISION_BLOCKED_INVALID_DATA
            elif any(c in blocking_codes for c in (RC_DAILY_PRICE_STALE, RC_SOURCE_INTERRUPTED)):
                decision_str = DECISION_BLOCKED_FRESHNESS
            elif RC_HISTORY_INSUFFICIENT in blocking_codes:
                decision_str = DECISION_BLOCKED_INSUFFICIENT_HISTORY
            else:
                decision_str = DECISION_BLOCKED_DATA_QUALITY
            gate_level = GATE_LEVEL_BLOCKED
            confidence = CONFIDENCE_INSUFFICIENT
        else:
            # Check formal eligibility
            formal_min = self.policy.minimum_rows(gate_name, "formal")
            formal_comp = self.policy.minimum_completeness(gate_name, "formal")
            obs_min = self.policy.minimum_rows(gate_name, "observational")
            obs_comp = self.policy.minimum_completeness(gate_name, "observational")

            rows = max(gate_input.daily_rows, gate_input.trading_days)
            comp = gate_input.daily_completeness

            freshness_ok_formal = (
                gate_input.freshness_status in self.policy.allowed_freshness(gate_name)
                or gate_input.freshness_status == "UNKNOWN"
            )

            if (
                rows >= formal_min
                and comp >= formal_comp
                and freshness_ok_formal
            ):
                decision_str = DECISION_ELIGIBLE_FORMAL
                gate_level = GATE_LEVEL_FORMAL
                eligible = True
                confidence = CONFIDENCE_RELIABLE
            elif rows >= obs_min and comp >= obs_comp:
                decision_str = DECISION_ELIGIBLE_OBSERVATIONAL
                gate_level = GATE_LEVEL_OBSERVATIONAL
                eligible = True
                confidence = CONFIDENCE_OBSERVATIONAL
            else:
                decision_str = DECISION_BLOCKED_DATA_QUALITY
                gate_level = GATE_LEVEL_BLOCKED
                confidence = CONFIDENCE_INSUFFICIENT

        # Separate blocking vs optional issues for output
        blocking_issues = [
            f"{c}: {REASON_CODE_METADATA.get(c, {}).get('explanation', c)}"
            for c in blocking_codes
        ]
        optional_issues = [
            f"{c}: {REASON_CODE_METADATA.get(c, {}).get('explanation', c)}"
            for c in warning_codes
        ]

        return QualityGateDecision(
            symbol=gate_input.symbol,
            gate_name=gate_name,
            gate_level=gate_level,
            eligible=eligible,
            decision=decision_str,
            confidence=confidence,
            reason_codes=list(blocking_codes) + list(warning_codes),
            reasons=reasons,
            warnings=[f"[WARN] {c}" for c in warning_codes],
            required_actions=required_actions,
            blocking_issues=blocking_issues,
            optional_issues=optional_issues,
            policy_version="1.1.4",
            research_only=True,
            no_real_orders=True,
        )

    # ------------------------------------------------------------------
    # All-gates evaluation
    # ------------------------------------------------------------------

    def evaluate_all_gates(self, symbol: str, mode: str = "real") -> dict:
        """
        Evaluate all 12 quality gates for a symbol.
        Returns {gate_name: QualityGateDecision}.
        """
        results: dict = {}
        for gate_name in ALL_GATES:
            try:
                results[gate_name] = self.evaluate(symbol, gate_name, mode=mode)
            except Exception as exc:
                logger.warning("Error evaluating gate %s for %s: %s", gate_name, symbol, exc)
                # Produce a safe blocked decision on error
                results[gate_name] = QualityGateDecision(
                    symbol=symbol,
                    gate_name=gate_name,
                    gate_level=GATE_LEVEL_BLOCKED,
                    eligible=False,
                    decision=DECISION_BLOCKED_DATA_QUALITY,
                    confidence=CONFIDENCE_UNKNOWN,
                    reasons=[f"Evaluation error: {exc}"],
                    research_only=True,
                    no_real_orders=True,
                )
        return results
