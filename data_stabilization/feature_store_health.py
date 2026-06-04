"""data_stabilization/feature_store_health.py — FeatureStoreHealthChecker v0.5.5.

Aggregates readiness results into an overall Feature Store health score.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Overall status constants
# ---------------------------------------------------------------------------
HEALTH_HEALTHY  = "HEALTHY"
HEALTH_DEGRADED = "DEGRADED"
HEALTH_PARTIAL  = "PARTIAL"
HEALTH_BLOCKED  = "BLOCKED"
HEALTH_UNKNOWN  = "UNKNOWN"


class FeatureStoreHealthChecker:
    """Evaluates overall Feature Store health from readiness results.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        readiness_checker=None,
        lineage_tracker=None,
    ) -> None:
        self._readiness_checker = readiness_checker
        self._lineage_tracker   = lineage_tracker

    def run(self, readiness_results: Optional[List[dict]] = None) -> dict:
        """Compute health from readiness results (or run checker fresh)."""
        try:
            if readiness_results is None:
                if self._readiness_checker is not None:
                    readiness_results = self._readiness_checker.check_all()
                else:
                    from data_stabilization.feature_readiness_checker import FeatureReadinessChecker
                    checker = FeatureReadinessChecker()
                    readiness_results = checker.check_all()

            if not readiness_results:
                return self._empty_result("No readiness results available")

            ready_count        = 0
            partial_count      = 0
            missing_count      = 0
            stale_count        = 0
            leakage_risk_count = 0
            schema_error_count = 0
            blockers           = []
            warnings           = []

            for r in readiness_results:
                status = r.get("status", "UNKNOWN")
                name   = r.get("feature_group", r.get("dataset_name", "?"))
                notes  = r.get("notes", "")

                if status == "READY":
                    ready_count += 1
                elif status == "PARTIAL":
                    partial_count += 1
                    warnings.append(f"{name}: PARTIAL — {notes}")
                elif status == "MISSING":
                    missing_count += 1
                    warnings.append(f"{name}: MISSING")
                elif status == "STALE":
                    stale_count += 1
                    warnings.append(f"{name}: STALE — {notes}")
                elif status == "LEAKAGE_RISK":
                    leakage_risk_count += 1
                    blockers.append(f"{name}: LEAKAGE_RISK — {notes}")
                elif status == "FAILED":
                    schema_error_count += 1
                    warnings.append(f"{name}: FAILED — {notes}")

            total = len(readiness_results)
            if total == 0:
                return self._empty_result("No feature groups to evaluate")

            # Score: READY=100, PARTIAL/STALE=50, MISSING=0, LEAKAGE_RISK=-100 penalty
            score = (
                ready_count * 100.0
                + partial_count * 50.0
                + stale_count * 50.0
            ) / total
            score = max(0.0, min(100.0, score))

            # Determine overall status
            if leakage_risk_count > 0:
                overall_status = HEALTH_BLOCKED
            elif missing_count > total // 2:
                overall_status = HEALTH_PARTIAL
            elif ready_count == total:
                overall_status = HEALTH_HEALTHY
            elif ready_count >= total * 0.7:
                overall_status = HEALTH_DEGRADED
            else:
                overall_status = HEALTH_PARTIAL

            return {
                "health_score":      round(score, 1),
                "ready_count":       ready_count,
                "partial_count":     partial_count,
                "missing_count":     missing_count,
                "stale_count":       stale_count,
                "leakage_risk_count": leakage_risk_count,
                "schema_error_count": schema_error_count,
                "overall_status":    overall_status,
                "blockers":          blockers,
                "warnings":          warnings,
                "no_real_orders":    True,
                "production_blocked": True,
            }

        except Exception as exc:
            logger.warning("FeatureStoreHealthChecker.run() failed: %s", exc)
            return self._empty_result(str(exc))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _empty_result(self, reason: str = "") -> dict:
        return {
            "health_score":      0.0,
            "ready_count":       0,
            "partial_count":     0,
            "missing_count":     0,
            "stale_count":       0,
            "leakage_risk_count": 0,
            "schema_error_count": 0,
            "overall_status":    HEALTH_UNKNOWN,
            "blockers":          [],
            "warnings":          [reason] if reason else [],
            "no_real_orders":    True,
            "production_blocked": True,
        }
