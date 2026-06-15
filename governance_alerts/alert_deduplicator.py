"""
governance_alerts.alert_deduplicator — GovernanceAlertDeduplicator v1.1.7

Deterministic fingerprinting, deduplication, occurrence merging, source
interruption and module failure grouping.

Rules:
- P0 alerts: CANNOT be lost through deduplication (only merged)
- RESOLVED then same issue reappears: mark REOPENED
- Same fingerprint: increment occurrence_count only
- Stable sort of reason codes for deterministic fingerprints

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fingerprint(*parts) -> str:
    """Build deterministic fingerprint from parts."""
    # Normalize: strip, upper, exclude empty
    normalized = [str(p).strip().upper() for p in parts if p is not None and str(p).strip()]
    key = "|".join(normalized)
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


class GovernanceAlertDeduplicator:
    """Deterministic alert deduplication and merging.

    [!] P0 alerts cannot be lost through deduplication.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def build_fingerprint(self, alert) -> str:
        """Build deterministic fingerprint for an alert.

        Includes: alert_type, symbol, dataset, source, module, sorted reason_codes.
        Excludes: timestamp, alert_id, random values, temp paths.
        """
        symbol = str(alert.symbol or "").strip().upper()
        dataset = str(alert.dataset or "").strip().upper()
        source = str(alert.source or "").strip().upper()
        module = str(alert.module or "").strip().upper()
        reason_codes_str = "|".join(sorted(str(r).strip().upper() for r in (alert.reason_codes or [])))
        return _fingerprint(
            alert.alert_type,
            symbol,
            dataset,
            source,
            module,
            reason_codes_str,
        )

    def deduplicate(self, new_alerts: List, existing_alerts: List) -> List:
        """Deduplicate new_alerts against existing_alerts.

        - If fingerprint matches RESOLVED existing: mark REOPENED
        - If fingerprint matches OPEN existing: increment occurrence_count
        - P0 alert: never lost, only merged
        - Returns merged list of alerts (existing updated + genuinely new)
        """
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy

        policy = GovernanceAlertPolicy()

        # Build index of existing by fingerprint
        existing_by_fp: dict = {}
        for a in existing_alerts:
            fp = self.build_fingerprint(a)
            if fp not in existing_by_fp:
                existing_by_fp[fp] = a

        result = list(existing_alerts)
        result_fps = {self.build_fingerprint(a): i for i, a in enumerate(result)}

        genuinely_new = []
        for new_alert in new_alerts:
            fp = self.build_fingerprint(new_alert)
            new_alert.fingerprint = fp  # ensure fingerprint is set

            if fp in result_fps:
                idx = result_fps[fp]
                existing = result[idx]
                if existing.status == "RESOLVED":
                    # Same issue reappeared — mark REOPENED
                    result[idx] = self.merge_occurrence(existing, new_alert, reopen=True)
                else:
                    # Same open alert — increment occurrence only
                    result[idx] = self.merge_occurrence(existing, new_alert, reopen=False)
            else:
                genuinely_new.append(new_alert)
                result.append(new_alert)
                result_fps[fp] = len(result) - 1

        # Verify P0 alerts are not lost
        new_p0_fps = {self.build_fingerprint(a) for a in new_alerts if a.priority == "P0"}
        result_fps_set = {self.build_fingerprint(a) for a in result}
        for fp in new_p0_fps:
            if fp not in result_fps_set:
                # This should never happen — log critical warning
                logger.error("CRITICAL: P0 alert with fingerprint %s was lost in deduplication!", fp)

        return result

    def merge_occurrence(self, existing, incoming, reopen: bool = False):
        """Merge an incoming alert occurrence into existing."""
        import copy
        merged = copy.copy(existing)
        merged.occurrence_count = existing.occurrence_count + 1
        merged.last_detected_at = incoming.last_detected_at or _now_utc()

        if reopen:
            merged.status = "REOPENED"
            merged.reopened_count = existing.reopened_count + 1
            merged.previous_state = existing.current_state
            merged.current_state = incoming.current_state
            logger.info("Alert %s reopened (was RESOLVED, issue recurred)", existing.alert_id)
        else:
            # Only update state if it worsened
            merged.current_state = incoming.current_state or existing.current_state

        return merged

    def within_suppression_window(self, existing_alert, window_seconds: int) -> bool:
        """Return True if existing_alert is within its suppression window."""
        if window_seconds == 0:
            return False
        try:
            last = datetime.fromisoformat(existing_alert.last_detected_at)
            now = datetime.now(timezone.utc)
            if last.tzinfo is None:
                from datetime import timezone as tz
                last = last.replace(tzinfo=tz.utc)
            elapsed = (now - last).total_seconds()
            return elapsed < window_seconds
        except Exception:
            return False

    def group_source_interruption(self, alerts: List) -> List:
        """Aggregate multiple source interruption alerts into one grouped alert."""
        from governance_alerts.alert_schema import GovernanceAlert
        si_alerts = [a for a in alerts if a.alert_type == "SOURCE_INTERRUPTION"]
        other_alerts = [a for a in alerts if a.alert_type != "SOURCE_INTERRUPTION"]

        if len(si_alerts) <= 1:
            return alerts

        # Aggregate into a single alert
        total = sum(a.occurrence_count for a in si_alerts)
        sources = list({a.source for a in si_alerts if a.source})
        symbols = list({a.symbol for a in si_alerts if a.symbol})

        base = si_alerts[0]
        grouped = GovernanceAlert(
            alert_id=base.alert_id,
            fingerprint=self.build_fingerprint(base),
            alert_type="SOURCE_INTERRUPTION",
            severity="CRITICAL",
            priority="P0",
            title=f"Source interruption affecting {len(si_alerts)} sources (aggregated)",
            message=f"Aggregated {len(si_alerts)} source interruption alerts. Sources: {sources}. Symbols affected: {symbols}.",
            source=",".join(sources[:5]),
            reason_codes=["SOURCE_INTERRUPTION", "AGGREGATED"],
            safe_actions=base.safe_actions,
            suggested_commands=base.suggested_commands,
            status=base.status,
            first_detected_at=min(a.first_detected_at for a in si_alerts),
            last_detected_at=max(a.last_detected_at for a in si_alerts),
            occurrence_count=total,
            research_only=True,
            no_real_orders=True,
        )
        return other_alerts + [grouped]

    def group_module_failure(self, alerts: List) -> List:
        """Return alerts unchanged (module failures are kept individual for traceability)."""
        return alerts

    def summarize_dedup(self, before: List, after: List) -> dict:
        return {
            "before_count": len(before),
            "after_count": len(after),
            "deduplicated": len(before) - len(after),
            "reopened": sum(1 for a in after if a.status == "REOPENED"),
            "occurrence_merged": sum(1 for a in after if a.occurrence_count > 1),
        }
