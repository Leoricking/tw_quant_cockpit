"""
data/governance/quality/coverage_gate_v146.py — Coverage Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Backtest stricter than exploratory.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import CoverageStatus, GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Coverage thresholds
_PASS_PCT = 0.95       # 95% coverage = PASS
_ACCEPTABLE_PCT = 0.80  # 80% = ACCEPTABLE (WARN)
_BACKTEST_PASS_PCT = 0.98  # backtest needs 98%
_BACKTEST_ACCEPTABLE_PCT = 0.90


class CoverageGate:
    """Symbol/date/market/batch completeness check. Backtest is stricter."""

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        coverage_pct = ctx.get("coverage_pct", None)
        coverage_status = ctx.get("coverage_status", CoverageStatus.UNKNOWN.value)
        is_backtest = ctx.get("is_backtest", False)

        pass_thresh = _BACKTEST_PASS_PCT if is_backtest else _PASS_PCT
        acceptable_thresh = _BACKTEST_ACCEPTABLE_PCT if is_backtest else _ACCEPTABLE_PCT

        if coverage_pct is None:
            if coverage_status == CoverageStatus.COMPLETE.value:
                status = GateStatus.PASS.value
                evidence = "Coverage: COMPLETE"
            elif coverage_status == CoverageStatus.ACCEPTABLE.value:
                status = GateStatus.WARN.value
                evidence = "Coverage: ACCEPTABLE"
            elif coverage_status == CoverageStatus.INSUFFICIENT.value:
                status = GateStatus.FAIL.value
                evidence = "Coverage: INSUFFICIENT"
            elif coverage_status == CoverageStatus.BLOCKED.value:
                status = GateStatus.BLOCKED.value
                evidence = "Coverage: BLOCKED"
            else:
                status = GateStatus.UNKNOWN.value
                evidence = "Coverage: UNKNOWN"
        elif coverage_pct >= pass_thresh:
            status = GateStatus.PASS.value
            evidence = f"Coverage {coverage_pct:.1%} >= {pass_thresh:.0%}"
        elif coverage_pct >= acceptable_thresh:
            status = GateStatus.WARN.value
            evidence = f"Coverage {coverage_pct:.1%} acceptable (>= {acceptable_thresh:.0%})"
        else:
            status = GateStatus.FAIL.value
            evidence = f"Coverage {coverage_pct:.1%} < {acceptable_thresh:.0%} — insufficient"

        return QualityGateResult(
            gate_id="coverage", gate_name="Coverage Gate",
            scope="DATASET", subject_id=subject_id,
            status=status, passed=(status == GateStatus.PASS.value),
            blocking=(status == GateStatus.BLOCKED.value),
            evidence=evidence,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
