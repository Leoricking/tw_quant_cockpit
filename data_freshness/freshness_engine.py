"""
data_freshness/freshness_engine.py — Data Freshness Engine for v1.1.3.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Auto external refresh: DISABLED. Stale auto repair: DISABLED.
[!] Future date does NOT count as fresh.
[!] Mock data NOT used for formal freshness conclusions.
[!] No automatic data download. No broker connection.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from data_freshness.freshness_schema import (
    ALERT_COVERAGE_NOT_REFRESHED, ALERT_DATA_DELAY, ALERT_DATA_MISSING,
    ALERT_DATA_STALE, ALERT_DATE_REGRESSION, ALERT_FUTURE_DATE,
    ALERT_SOURCE_INTERRUPTION,
    ALERT_STATUS_OPEN,
    SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_INFO, SEVERITY_LOW, SEVERITY_MEDIUM,
    SOURCE_STATUS_INTERRUPTED,
    STATUS_DELAYED, STATUS_DATE_REGRESSION, STATUS_FRESH, STATUS_ACCEPTABLE,
    STATUS_FUTURE_DATE, STATUS_INTERRUPTED, STATUS_MISSING, STATUS_STALE,
    STATUS_UNKNOWN,
    DatasetFreshnessRecord, FreshnessAlert, FreshnessSummary, SourceFreshnessStatus,
)
from data_freshness.freshness_detector import DataFreshnessDetector
from data_freshness.source_monitor import DataSourceFreshnessMonitor
from data_freshness.freshness_prioritizer import FreshnessPrioritizer

logger = logging.getLogger(__name__)

# Module-level safety invariants — MUST NOT be changed
NO_REAL_ORDERS                     = True
AUTO_EXTERNAL_REFRESH_ENABLED      = False
STALE_DATA_AUTO_REPAIR_ENABLED     = False
FUTURE_DATE_COUNTS_AS_FRESH        = False
MOCK_DATA_FORMAL_FRESHNESS_ALLOWED = False
BROKER_DISABLED                    = True
RESEARCH_ONLY                      = True


class DataFreshnessEngine:
    """
    Orchestrates freshness detection, alerting, source health monitoring,
    and repair handoff generation.

    [!] Does NOT download data, connect to brokers, or execute repairs.
    [!] Alerts are informational only — they do NOT modify data.
    [!] mode='mock' outputs are labelled DEMO_ONLY and excluded from
        formal freshness conclusions.
    """

    def __init__(
        self,
        repo_path: Optional[str] = None,
        as_of: Optional[datetime] = None,
    ):
        self._repo_path = repo_path
        self._as_of = as_of
        self._detector = DataFreshnessDetector(
            repo_path=repo_path, as_of=as_of
        )
        self._source_monitor = DataSourceFreshnessMonitor()
        self._prioritizer = FreshnessPrioritizer()

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------

    def scan_symbol(self, symbol: str) -> List[DatasetFreshnessRecord]:
        """Scan freshness for a single symbol (DAILY_PRICE + VOLUME)."""
        return self._detector.detect_symbol(symbol)

    def scan_tier(self, tier: str) -> List[DatasetFreshnessRecord]:
        """Scan freshness for all symbols in a tier."""
        return self._detector.detect_tier(tier)

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(
        self,
        tier: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        datasets: Optional[List[str]] = None,
        mode: str = "real",
    ) -> Dict[str, Any]:
        """
        Run full freshness scan.

        mode='real'  — reads actual CSV data, no mock fallback.
        mode='mock'  — outputs labelled DEMO_ONLY; not for formal conclusions.

        [!] Does NOT auto-download data regardless of mode.
        [!] Does NOT auto-repair stale data.

        Returns dict: records, alerts, source_health, summary, (demo_only if mock).
        """
        is_mock = mode.lower() == "mock"
        if is_mock:
            logger.warning(
                "Engine running in MOCK mode — output labelled DEMO_ONLY, "
                "NOT suitable for formal freshness conclusions"
            )

        records: List[DatasetFreshnessRecord] = []

        if symbols:
            for sym in symbols:
                try:
                    recs = self.scan_symbol(sym)
                    records.extend(recs)
                except Exception as exc:
                    logger.warning("scan_symbol(%s) failed: %s", sym, exc)
        elif tier:
            try:
                records = self.scan_tier(tier)
            except Exception as exc:
                logger.warning("scan_tier(%s) failed: %s", tier, exc)
        else:
            logger.warning("run() called with no tier or symbols — nothing scanned")

        # Filter by datasets if requested
        if datasets:
            records = [r for r in records if r.dataset in datasets]

        # Mock mode: tag records, exclude from confidence
        if is_mock:
            for rec in records:
                rec.source = "mock"

        # Build outputs
        alerts = self.build_alerts(records)
        source_health = self.build_source_health(records)
        summary = self.build_summary(records)

        result: Dict[str, Any] = {
            "records": [r.to_dict() for r in records],
            "alerts": [a.to_dict() for a in alerts],
            "source_health": [s.to_dict() for s in source_health],
            "summary": summary.to_dict(),
            "record_objects": records,
            "alert_objects": alerts,
            "source_health_objects": source_health,
            "summary_object": summary,
        }
        if is_mock:
            result["demo_only"] = True
            result["mock_disclaimer"] = (
                "DEMO_ONLY: mock mode output. "
                "Not suitable for formal freshness conclusions. "
                "Mock data excluded from confidence calculation."
            )
        return result

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def build_alerts(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[FreshnessAlert]:
        """
        Build FreshnessAlert objects for problematic records.

        [!] Alerts do NOT modify data or trigger repair.
        Creates alerts for: DELAYED, STALE, INTERRUPTED, MISSING, FUTURE_DATE, DATE_REGRESSION.
        """
        alerts: List[FreshnessAlert] = []
        now_iso = datetime.utcnow().isoformat()

        status_to_alert = {
            STATUS_DELAYED:        (ALERT_DATA_DELAY,    SEVERITY_MEDIUM),
            STATUS_STALE:          (ALERT_DATA_STALE,    SEVERITY_HIGH),
            STATUS_INTERRUPTED:    (ALERT_DATA_STALE,    SEVERITY_CRITICAL),
            STATUS_MISSING:        (ALERT_DATA_MISSING,  SEVERITY_CRITICAL),
            STATUS_FUTURE_DATE:    (ALERT_FUTURE_DATE,   SEVERITY_CRITICAL),
            STATUS_DATE_REGRESSION:(ALERT_DATE_REGRESSION, SEVERITY_CRITICAL),
        }

        for rec in records:
            # Skip mock sources from formal alerting
            if rec.source == "mock":
                continue

            alert_info = status_to_alert.get(rec.status)
            if alert_info is None:
                continue

            alert_type, severity = alert_info

            msg = rec.reason or f"{rec.dataset} {rec.status} for {rec.symbol}"

            alerts.append(
                FreshnessAlert(
                    alert_id=str(uuid4()),
                    symbol=rec.symbol,
                    dataset=rec.dataset,
                    source=rec.source,
                    alert_type=alert_type,
                    severity=severity,
                    status=ALERT_STATUS_OPEN,
                    message=msg,
                    first_detected_at=now_iso,
                    last_detected_at=now_iso,
                    occurrence_count=1,
                    repair_issue_id=None,
                    acknowledged=False,
                    research_only=True,
                    no_real_orders=True,
                )
            )

        # Source-level interruption alerts
        source_statuses = self.build_source_health(records)
        for ss in source_statuses:
            if ss.status == SOURCE_STATUS_INTERRUPTED:
                alerts.append(
                    FreshnessAlert(
                        alert_id=str(uuid4()),
                        symbol="*",
                        dataset=ss.dataset,
                        source=ss.source_name,
                        alert_type=ALERT_SOURCE_INTERRUPTION,
                        severity=SEVERITY_CRITICAL,
                        status=ALERT_STATUS_OPEN,
                        message=ss.reason,
                        first_detected_at=now_iso,
                        last_detected_at=now_iso,
                        occurrence_count=1,
                        repair_issue_id=None,
                        acknowledged=False,
                        research_only=True,
                        no_real_orders=True,
                    )
                )

        return alerts

    # ------------------------------------------------------------------
    # Source health
    # ------------------------------------------------------------------

    def build_source_health(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[SourceFreshnessStatus]:
        """Build source-level health statuses from all records."""
        return self._source_monitor.summarize_sources(records)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(
        self, records: List[DatasetFreshnessRecord]
    ) -> FreshnessSummary:
        """Build a FreshnessSummary from a list of records."""
        now_iso = datetime.utcnow().isoformat()

        # Determine tier
        tiers = list({r.tier for r in records if r.tier})
        tier_str = tiers[0] if len(tiers) == 1 else ("mixed" if tiers else "unknown")

        symbols = sorted({r.symbol for r in records if r.symbol})
        datasets = sorted({r.dataset for r in records if r.dataset})

        fresh_count       = sum(1 for r in records if r.status == STATUS_FRESH)
        acceptable_count  = sum(1 for r in records if r.status == STATUS_ACCEPTABLE)
        delayed_count     = sum(1 for r in records if r.status == STATUS_DELAYED)
        stale_count       = sum(1 for r in records if r.status == STATUS_STALE)
        interrupted_count = sum(1 for r in records if r.status == STATUS_INTERRUPTED)
        missing_count     = sum(1 for r in records if r.status == STATUS_MISSING)
        critical_count    = sum(
            1 for r in records if r.severity == SEVERITY_CRITICAL
        )

        # Overall status
        if interrupted_count > 0 or missing_count > 0 or critical_count > 0:
            overall = STATUS_INTERRUPTED
        elif stale_count > 0:
            overall = STATUS_STALE
        elif delayed_count > 0:
            overall = STATUS_DELAYED
        elif acceptable_count > 0:
            overall = STATUS_ACCEPTABLE
        elif fresh_count > 0:
            overall = STATUS_FRESH
        else:
            overall = STATUS_UNKNOWN

        # Confidence: LOW if mock data present
        mock_present = any(r.source == "mock" for r in records)
        real_records = [r for r in records if r.source != "mock"]
        if mock_present:
            confidence = "DEMO_ONLY"
        elif not real_records:
            confidence = "LOW"
        else:
            fresh_ratio = (fresh_count + acceptable_count) / len(real_records) if real_records else 0
            if fresh_ratio >= 0.9:
                confidence = "HIGH"
            elif fresh_ratio >= 0.7:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"

        # Source health dict
        source_statuses = self._source_monitor.summarize_sources(records)
        source_health: Dict[str, Any] = {}
        for ss in source_statuses:
            source_health[ss.source_id] = ss.to_dict()

        summary = FreshnessSummary(
            generated_at=now_iso,
            tier=tier_str,
        )
        summary.symbols = symbols
        summary.datasets = datasets
        summary.fresh_count = fresh_count
        summary.acceptable_count = acceptable_count
        summary.delayed_count = delayed_count
        summary.stale_count = stale_count
        summary.interrupted_count = interrupted_count
        summary.missing_count = missing_count
        summary.critical_count = critical_count
        summary.source_health = source_health
        summary.overall_status = overall
        summary.confidence = confidence
        summary.research_only = True
        summary.no_real_orders = True
        return summary

    # ------------------------------------------------------------------
    # Repair handoff
    # ------------------------------------------------------------------

    def create_repair_handoff(
        self, alerts: List[FreshnessAlert]
    ) -> List[Dict[str, Any]]:
        """
        Map FreshnessAlerts to CoverageIssue-compatible handoff dicts.

        [!] Does NOT call repair executor or download data.
        [!] SOURCE_INTERRUPTION creates one source-level task only (NOT per symbol).

        Mapping:
          DATA_STALE           → issue_type=STALE_DATA, repairability=SOURCE_REQUIRED
          DATA_MISSING         → issue_type=MISSING_SYMBOL_DATA
          FUTURE_DATE          → action=REVIEW, priority=P0
          DATE_REGRESSION      → action=REVIEW, priority=P0
          COVERAGE_NOT_REFRESHED → action=REFRESH_COVERAGE, auto_safe=True
          SOURCE_INTERRUPTION  → source-level task only
        """
        handoff: List[Dict[str, Any]] = []
        source_interruption_seen = set()

        for alert in alerts:
            if alert.alert_type == ALERT_DATA_STALE:
                handoff.append({
                    "issue_id": str(uuid4()),
                    "alert_id": alert.alert_id,
                    "symbol": alert.symbol,
                    "dataset": alert.dataset,
                    "source": alert.source,
                    "issue_type": "STALE_DATA",
                    "repairability": "SOURCE_REQUIRED",
                    "action": "REVIEW",
                    "auto_safe": False,
                    "priority": "P1",
                    "message": alert.message,
                    "research_only": True,
                    "no_real_orders": True,
                })
            elif alert.alert_type == ALERT_DATA_MISSING:
                handoff.append({
                    "issue_id": str(uuid4()),
                    "alert_id": alert.alert_id,
                    "symbol": alert.symbol,
                    "dataset": alert.dataset,
                    "source": alert.source,
                    "issue_type": "MISSING_SYMBOL_DATA",
                    "repairability": "MANUAL_REQUIRED",
                    "action": "INVESTIGATE",
                    "auto_safe": False,
                    "priority": "P1",
                    "message": alert.message,
                    "research_only": True,
                    "no_real_orders": True,
                })
            elif alert.alert_type == ALERT_FUTURE_DATE:
                handoff.append({
                    "issue_id": str(uuid4()),
                    "alert_id": alert.alert_id,
                    "symbol": alert.symbol,
                    "dataset": alert.dataset,
                    "source": alert.source,
                    "issue_type": "FUTURE_DATE_DETECTED",
                    "repairability": "MANUAL_REQUIRED",
                    "action": "REVIEW",
                    "auto_safe": False,
                    "priority": "P0",
                    "message": alert.message,
                    "research_only": True,
                    "no_real_orders": True,
                })
            elif alert.alert_type == ALERT_DATE_REGRESSION:
                handoff.append({
                    "issue_id": str(uuid4()),
                    "alert_id": alert.alert_id,
                    "symbol": alert.symbol,
                    "dataset": alert.dataset,
                    "source": alert.source,
                    "issue_type": "DATE_REGRESSION",
                    "repairability": "MANUAL_REQUIRED",
                    "action": "REVIEW",
                    "auto_safe": False,
                    "priority": "P0",
                    "message": alert.message,
                    "research_only": True,
                    "no_real_orders": True,
                })
            elif alert.alert_type == ALERT_COVERAGE_NOT_REFRESHED:
                handoff.append({
                    "issue_id": str(uuid4()),
                    "alert_id": alert.alert_id,
                    "symbol": alert.symbol,
                    "dataset": alert.dataset,
                    "source": alert.source,
                    "issue_type": "COVERAGE_NOT_REFRESHED",
                    "repairability": "AUTO_SAFE",
                    "action": "REFRESH_COVERAGE",
                    "auto_safe": True,
                    "priority": "P2",
                    "message": alert.message,
                    "research_only": True,
                    "no_real_orders": True,
                })
            elif alert.alert_type == ALERT_SOURCE_INTERRUPTION:
                # One source-level task only — NOT per individual symbol
                src_key = f"{alert.source}::{alert.dataset}"
                if src_key not in source_interruption_seen:
                    source_interruption_seen.add(src_key)
                    handoff.append({
                        "issue_id": str(uuid4()),
                        "alert_id": alert.alert_id,
                        "symbol": None,          # source-level, not per symbol
                        "dataset": alert.dataset,
                        "source": alert.source,
                        "issue_type": "SOURCE_INTERRUPTION",
                        "repairability": "SOURCE_REQUIRED",
                        "action": "INVESTIGATE_SOURCE",
                        "auto_safe": False,
                        "priority": "P0",
                        "message": alert.message,
                        "research_only": True,
                        "no_real_orders": True,
                    })

        return handoff

    # ------------------------------------------------------------------
    # Cross-run comparison
    # ------------------------------------------------------------------

    def compare_previous_run(
        self,
        current_records: List[DatasetFreshnessRecord],
        previous_records: List[DatasetFreshnessRecord],
    ) -> Dict[str, Any]:
        """Compare current and previous run records for changes."""
        return self._source_monitor.compare_with_previous_run(
            current_records, previous_records
        )

    # ------------------------------------------------------------------
    # Daily monitor
    # ------------------------------------------------------------------

    def run_daily_monitor(self, tier: str = "research30") -> Dict[str, Any]:
        """
        Run daily freshness monitor for a tier and persist results via FreshnessStore.
        Returns summary dict.
        """
        try:
            from data_freshness.freshness_store import FreshnessStore  # type: ignore
            store = FreshnessStore(
                output_dir=None  # uses default data/freshness_reports/
            )
        except Exception as exc:
            logger.warning("Could not load FreshnessStore: %s", exc)
            store = None

        result = self.run(tier=tier, mode="real")
        records = result.get("record_objects", [])
        alerts  = result.get("alert_objects", [])
        source_health = result.get("source_health_objects", [])
        summary = result.get("summary_object")

        if store is not None:
            try:
                store.save_records(records)
            except Exception as exc:
                logger.warning("save_records failed: %s", exc)
            try:
                store.save_alerts(alerts)
            except Exception as exc:
                logger.warning("save_alerts failed: %s", exc)
            try:
                store.save_source_health(source_health)
            except Exception as exc:
                logger.warning("save_source_health failed: %s", exc)
            if summary is not None:
                try:
                    store.save_summary(summary)
                except Exception as exc:
                    logger.warning("save_summary failed: %s", exc)
            try:
                store.append_history(records)
            except Exception as exc:
                logger.warning("append_history failed: %s", exc)

            # Repair handoff
            handoff = self.create_repair_handoff(alerts)
            if handoff:
                try:
                    store.save_repair_handoff(handoff)
                except Exception as exc:
                    logger.warning("save_repair_handoff failed: %s", exc)

        return result.get("summary", {})
