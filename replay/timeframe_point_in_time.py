"""
replay/timeframe_point_in_time.py — MultiTimeframePointInTimeVerifier v1.2.5

Per-timeframe independent point-in-time verification.
One fail → BLOCKED for that timeframe only.
Overall verified=True only if all required timeframes PASS.
Optional missing doesn't block overall.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class MultiTimeframePointInTimeVerifier:
    """
    Verifies point-in-time integrity independently per timeframe.

    Rules:
    - Each timeframe verified independently.
    - One fail → BLOCKED for that timeframe only.
    - overall verified=True only if all required timeframes PASS.
    - Optional missing → does not block overall.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def verify_bar(
        self,
        bar: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
        required: bool = True,
    ) -> Dict[str, Any]:
        """Verify a single bar is valid as of replay_timestamp."""
        warnings = []
        violations = []

        if not bar:
            if required:
                return self.build_result(
                    timeframe, False, "BLOCKED", ["No bar data — required timeframe"],
                    replay_timestamp
                )
            return self.build_result(timeframe, True, "MISSING_OPTIONAL", [], replay_timestamp)

        bar_ts   = bar.get("timestamp", "")
        avail_at = bar.get("available_at") or bar_ts

        # Check timestamp
        if bar_ts and bar_ts > replay_timestamp:
            violations.append(f"Bar timestamp {bar_ts} > replay {replay_timestamp}")

        # Check available_at
        if avail_at and avail_at > replay_timestamp:
            violations.append(f"available_at {avail_at} > replay {replay_timestamp}")

        # Check forbidden fields
        from replay.timeframe_future_firewall import FORBIDDEN_FIELDS
        for f in FORBIDDEN_FIELDS:
            if f in bar:
                violations.append(f"Forbidden field: {f}")

        if violations:
            return self.build_result(timeframe, False, "BLOCKED", violations, replay_timestamp)
        return self.build_result(timeframe, True, "PASS", warnings, replay_timestamp)

    def verify_snapshot(
        self,
        snapshot: Dict[str, Any],
        replay_timestamp: Optional[str] = None,
        required: bool = True,
    ) -> Dict[str, Any]:
        """Verify a single timeframe snapshot."""
        rts = replay_timestamp or snapshot.get("replay_timestamp", "")
        tf  = snapshot.get("timeframe", "UNKNOWN")

        warnings  = []
        violations = []

        # Check current bar
        current_bar = snapshot.get("current_bar") or {}
        if current_bar:
            bar_result = self.verify_bar(current_bar, rts, tf, required=False)
            if not bar_result["verified"]:
                violations.extend(bar_result["violations"])

        # Check latest_completed_bar
        completed_bar = snapshot.get("latest_completed_bar") or {}
        if completed_bar:
            bar_result = self.verify_bar(completed_bar, rts, tf, required=False)
            if not bar_result["verified"]:
                violations.extend(bar_result["violations"])

        # Check forbidden fields
        from replay.timeframe_future_firewall import FORBIDDEN_FIELDS
        for f in FORBIDDEN_FIELDS:
            if f in snapshot:
                violations.append(f"Forbidden field in snapshot: {f}")

        if violations:
            return self.build_result(tf, False, "BLOCKED", violations, rts)
        return self.build_result(tf, True, "PASS", warnings, rts)

    def verify_multi_snapshot(
        self,
        multi_snapshot: Dict[str, Any],
        required_timeframes: Optional[List[str]] = None,
        optional_timeframes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Verify all timeframes in a multi-snapshot."""
        rts = multi_snapshot.get("replay_timestamp", "")
        required  = required_timeframes  or []
        optional  = optional_timeframes  or []
        snapshots = multi_snapshot.get("snapshots", {})

        results: Dict[str, Dict[str, Any]] = {}
        all_pass = True

        for tf, snap in snapshots.items():
            is_required = tf in required or (not required and tf not in optional)
            result = self.verify_snapshot(snap, rts, required=is_required)
            results[tf] = result
            if is_required and not result["verified"]:
                all_pass = False

        # Check multi_snapshot itself for forbidden fields
        from replay.timeframe_future_firewall import FORBIDDEN_FIELDS
        overall_violations = []
        for f in FORBIDDEN_FIELDS:
            if f in multi_snapshot:
                overall_violations.append(f"Forbidden field in multi_snapshot: {f}")
                all_pass = False

        return {
            "verified": all_pass and not overall_violations,
            "replay_timestamp": rts,
            "timeframe_results": results,
            "overall_violations": overall_violations,
            "research_only": True,
            "no_real_orders": True,
        }

    def verify_indicator_inputs(
        self,
        indicators: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """Verify indicator inputs are point-in-time safe."""
        violations = []
        for k, v in indicators.items():
            if isinstance(v, dict):
                calc_at = v.get("calculated_at", "")
                if calc_at and calc_at > replay_timestamp:
                    violations.append(f"Indicator {k} calculated_at {calc_at} > replay")
        return self.build_result(
            timeframe,
            len(violations) == 0,
            "PASS" if not violations else "BLOCKED",
            violations,
            replay_timestamp,
        )

    def verify_strategy_inputs(
        self,
        strategy_output: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """Verify strategy inputs contain no future data."""
        from replay.timeframe_future_firewall import FORBIDDEN_FIELDS
        violations = [f"Forbidden field: {f}" for f in FORBIDDEN_FIELDS if f in strategy_output]
        return self.build_result(
            timeframe,
            len(violations) == 0,
            "PASS" if not violations else "BLOCKED",
            violations,
            replay_timestamp,
        )

    def verify_source_available_at(
        self,
        bar: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """Verify bar's available_at does not exceed replay_timestamp."""
        avail_at = bar.get("available_at", "")
        violations = []
        if avail_at and avail_at > replay_timestamp:
            violations.append(f"available_at {avail_at} > replay {replay_timestamp}")
        return self.build_result(
            timeframe,
            len(violations) == 0,
            "PASS" if not violations else "BLOCKED",
            violations,
            replay_timestamp,
        )

    def verify_parent_child_boundary(
        self,
        parent_bar: Optional[Dict[str, Any]],
        child_bars: List[Dict[str, Any]],
        replay_timestamp: str,
        parent_tf: str,
        child_tf: str,
    ) -> Dict[str, Any]:
        """Verify parent and child bars respect each other's boundaries."""
        violations = []
        if parent_bar:
            parent_ts = parent_bar.get("timestamp", "")
            for cb in child_bars:
                child_ts = cb.get("timestamp", "")
                if child_ts and parent_ts and child_ts < parent_ts:
                    violations.append(
                        f"Child bar {child_ts} ({child_tf}) before parent {parent_ts} ({parent_tf})"
                    )
        return {
            "verified": len(violations) == 0,
            "parent_timeframe": parent_tf,
            "child_timeframe": child_tf,
            "violations": violations,
            "replay_timestamp": replay_timestamp,
            "research_only": True,
        }

    def verify_partial_status(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> Dict[str, Any]:
        """Verify that partial bar status is correctly assigned."""
        violations = []
        from replay.timeframe_bar_state import ReplayBarStateEvaluator
        evaluator = ReplayBarStateEvaluator()
        state = evaluator.evaluate(bar, replay_timestamp, timeframe)
        if bar.get("is_complete") and state["is_partial"]:
            violations.append(
                f"Bar claims is_complete=True but is actually partial at {replay_timestamp}"
            )
        return self.build_result(
            timeframe,
            len(violations) == 0,
            "PASS" if not violations else "BLOCKED",
            violations,
            replay_timestamp,
        )

    def build_result(
        self,
        timeframe: str,
        verified: bool,
        status: str,
        violations: List[str],
        replay_timestamp: str,
    ) -> Dict[str, Any]:
        """Build standard verification result dict."""
        return {
            "verified": verified,
            "timeframe": timeframe,
            "status": status,
            "violations": violations,
            "replay_timestamp": replay_timestamp,
            "research_only": True,
            "no_real_orders": True,
        }
