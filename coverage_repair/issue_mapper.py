"""coverage_repair/issue_mapper.py — CoverageRepairIssueMapper for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] DEMO_ONLY_DATA is always BLOCKED — cannot be converted to REAL data.
[!] No fake data generation. No mock fallback substitution.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairActionType,
    RepairIssueType,
    RepairPriority,
    RepairTaskStatus,
    _now_iso,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ---------------------------------------------------------------------------
# Issue-type -> repair action mapping
# ---------------------------------------------------------------------------
_ISSUE_ACTION_MAP: Dict[str, List[str]] = {
    RepairIssueType.MISSING_DATA:            [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.PARTIAL_DATA:            [RepairActionType.REFRESH_PROVIDER, RepairActionType.RETRY_PROVIDER],
    RepairIssueType.STALE_DATA:              [RepairActionType.REFRESH_PROVIDER, RepairActionType.REBUILD_CACHE],
    RepairIssueType.BLOCKED_DATA:            [RepairActionType.MANUAL_REVIEW, RepairActionType.NO_SAFE_ACTION],
    RepairIssueType.UNAVAILABLE_SOURCE:      [RepairActionType.WAIT_FOR_SOURCE, RepairActionType.ENABLE_CONFIGURED_PROVIDER],
    RepairIssueType.SOURCE_CONFLICT:         [RepairActionType.REVIEW_SOURCE_CONFLICT],
    RepairIssueType.DEMO_ONLY_DATA:          [RepairActionType.NO_SAFE_ACTION],
    RepairIssueType.MISSING_CAPABILITY:      [RepairActionType.ENABLE_CONFIGURED_PROVIDER, RepairActionType.MANUAL_REVIEW],
    RepairIssueType.INVALID_SCHEMA:          [RepairActionType.FIX_SCHEMA, RepairActionType.MANUAL_REVIEW],
    RepairIssueType.MALFORMED_RESPONSE:      [RepairActionType.RETRY_PROVIDER, RepairActionType.FIX_SCHEMA],
    RepairIssueType.CACHE_STALE:             [RepairActionType.REBUILD_CACHE, RepairActionType.INVALIDATE_CACHE],
    RepairIssueType.CACHE_CORRUPTION:        [RepairActionType.INVALIDATE_CACHE, RepairActionType.REBUILD_CACHE],
    RepairIssueType.INSUFFICIENT_HISTORY:    [RepairActionType.EXTEND_HISTORY],
    RepairIssueType.MISSING_TECHNICAL_INDICATOR: [RepairActionType.RECALCULATE_INDICATORS],
    RepairIssueType.MISSING_INSTITUTIONAL:   [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.MISSING_MARGIN:          [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.MISSING_REVENUE:         [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.MISSING_FINANCIAL:       [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.MISSING_SHAREHOLDER:     [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.MISSING_ETF_OVERLAP:     [RepairActionType.REFRESH_PROVIDER, RepairActionType.WAIT_FOR_SOURCE],
    RepairIssueType.CORPORATE_ACTION_UNKNOWN: [RepairActionType.MANUAL_REVIEW],
    RepairIssueType.DUPLICATE_BAR:           [RepairActionType.MANUAL_REVIEW, RepairActionType.REVALIDATE_QUALITY],
    RepairIssueType.MISSING_BAR:             [RepairActionType.REFRESH_PROVIDER, RepairActionType.RETRY_PROVIDER],
    RepairIssueType.MARKET_CONFLICT:         [RepairActionType.REVIEW_MARKET_CONFLICT],
    RepairIssueType.PROVIDER_DISABLED:       [RepairActionType.ENABLE_CONFIGURED_PROVIDER],
    RepairIssueType.PROVIDER_AUTH_REQUIRED:  [RepairActionType.REQUEST_AUTH_CONFIGURATION],
    RepairIssueType.PROVIDER_RATE_LIMITED:   [RepairActionType.WAIT_FOR_RATE_LIMIT],
    RepairIssueType.UNKNOWN:                 [RepairActionType.MANUAL_REVIEW],
}

# Source status text -> canonical RepairIssueType
_STATUS_ISSUE_MAP: Dict[str, str] = {
    "MISSING": RepairIssueType.MISSING_DATA,
    "MISSING_DATA": RepairIssueType.MISSING_DATA,
    "PARTIAL": RepairIssueType.PARTIAL_DATA,
    "PARTIAL_DATA": RepairIssueType.PARTIAL_DATA,
    "STALE": RepairIssueType.STALE_DATA,
    "STALE_DATA": RepairIssueType.STALE_DATA,
    "BLOCKED": RepairIssueType.BLOCKED_DATA,
    "BLOCKED_DATA": RepairIssueType.BLOCKED_DATA,
    "UNAVAILABLE": RepairIssueType.UNAVAILABLE_SOURCE,
    "UNAVAILABLE_SOURCE": RepairIssueType.UNAVAILABLE_SOURCE,
    "DEMO_ONLY": RepairIssueType.DEMO_ONLY_DATA,
    "DEMO_ONLY_DATA": RepairIssueType.DEMO_ONLY_DATA,
    "SOURCE_CONFLICT": RepairIssueType.SOURCE_CONFLICT,
    "CONFLICT": RepairIssueType.SOURCE_CONFLICT,
    "INSUFFICIENT_HISTORY": RepairIssueType.INSUFFICIENT_HISTORY,
    "PROVIDER_DISABLED": RepairIssueType.PROVIDER_DISABLED,
    "DISABLED": RepairIssueType.PROVIDER_DISABLED,
    "AUTH_REQUIRED": RepairIssueType.PROVIDER_AUTH_REQUIRED,
    "PROVIDER_AUTH_REQUIRED": RepairIssueType.PROVIDER_AUTH_REQUIRED,
    "RATE_LIMITED": RepairIssueType.PROVIDER_RATE_LIMITED,
    "PROVIDER_RATE_LIMITED": RepairIssueType.PROVIDER_RATE_LIMITED,
    "SCHEMA_MISMATCH": RepairIssueType.INVALID_SCHEMA,
    "INVALID_SCHEMA": RepairIssueType.INVALID_SCHEMA,
    "CACHE_STALE": RepairIssueType.CACHE_STALE,
    "CACHE_CORRUPTION": RepairIssueType.CACHE_CORRUPTION,
    "MALFORMED": RepairIssueType.MALFORMED_RESPONSE,
    "MALFORMED_RESPONSE": RepairIssueType.MALFORMED_RESPONSE,
    "MARKET_CONFLICT": RepairIssueType.MARKET_CONFLICT,
    "DUPLICATE_BAR": RepairIssueType.DUPLICATE_BAR,
    "MISSING_BAR": RepairIssueType.MISSING_BAR,
    "UNKNOWN": RepairIssueType.UNKNOWN,
}


class CoverageRepairIssueMapper:
    """Maps coverage records, quality reports, and provider errors to CoverageRepairTask objects.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    no_real_orders = True
    production_trading_blocked = True

    def map_issue_type(self, source_status: str) -> str:
        """Map a source status string to a canonical RepairIssueType."""
        key = str(source_status).upper().strip()
        # Handle substrings
        if "INSUFFICIENT_HISTORY" in key or "MA60" in key or "INSUFFICIENT" in key:
            return RepairIssueType.INSUFFICIENT_HISTORY
        if "AUTH" in key:
            return RepairIssueType.PROVIDER_AUTH_REQUIRED
        if "RATE_LIMIT" in key or "RATE LIMIT" in key:
            return RepairIssueType.PROVIDER_RATE_LIMITED
        if "CACHE_CORRUPT" in key:
            return RepairIssueType.CACHE_CORRUPTION
        if "CACHE_STALE" in key or "CACHE STALE" in key:
            return RepairIssueType.CACHE_STALE
        if "SCHEMA_MISMATCH" in key or "INVALID_SCHEMA" in key:
            return RepairIssueType.INVALID_SCHEMA
        if "MARKET_CONFLICT" in key:
            return RepairIssueType.MARKET_CONFLICT
        if "SOURCE_CONFLICT" in key or "CONFLICT" in key:
            return RepairIssueType.SOURCE_CONFLICT
        return _STATUS_ISSUE_MAP.get(key, RepairIssueType.UNKNOWN)

    def map_repair_actions(self, issue_type: str) -> List[str]:
        """Return the list of suggested repair actions for an issue type."""
        return list(_ISSUE_ACTION_MAP.get(issue_type, [RepairActionType.MANUAL_REVIEW]))

    def build_task(
        self,
        symbol: str,
        issue_type: str,
        *,
        market: str = "",
        universe_id: str = "",
        universe_tier: str = "",
        profile: str = "",
        issue_code: str = "",
        issue_field: str = "",
        quality_status: str = "",
        quality_score: Optional[float] = None,
        coverage_status: str = "",
        provider_id: Optional[str] = None,
        provider_status: Optional[str] = None,
        provider_capability: Optional[str] = None,
        source: str = "",
        blocking_reason: str = "",
        warnings: Optional[List[str]] = None,
        missing_fields: Optional[List[str]] = None,
        stale_fields: Optional[List[str]] = None,
        invalid_fields: Optional[List[str]] = None,
        inconsistent_fields: Optional[List[str]] = None,
        source_report_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CoverageRepairTask:
        """Build a CoverageRepairTask from field values."""
        suggested = self.map_repair_actions(issue_type)
        selected = suggested[0] if suggested else RepairActionType.NO_SAFE_ACTION

        # DEMO_ONLY is always BLOCKED
        if issue_type == RepairIssueType.DEMO_ONLY_DATA:
            status = RepairTaskStatus.BLOCKED
            blocking_reason = blocking_reason or "DEMO_ONLY_DATA cannot be converted to REAL data."
            retryable = False
            auto_retry_allowed = False
        elif issue_type in (RepairIssueType.SOURCE_CONFLICT, RepairIssueType.MARKET_CONFLICT):
            status = RepairTaskStatus.CONFLICT_REVIEW
            retryable = False
            auto_retry_allowed = False
        elif issue_type == RepairIssueType.PROVIDER_AUTH_REQUIRED:
            status = RepairTaskStatus.WAITING_AUTH
            retryable = True
            auto_retry_allowed = False
        elif issue_type == RepairIssueType.PROVIDER_RATE_LIMITED:
            status = RepairTaskStatus.WAITING_RATE_LIMIT
            retryable = True
            auto_retry_allowed = False
        elif issue_type == RepairIssueType.UNAVAILABLE_SOURCE:
            status = RepairTaskStatus.WAITING_SOURCE
            retryable = True
            auto_retry_allowed = False
        elif issue_type == RepairIssueType.UNKNOWN:
            status = RepairTaskStatus.OPEN
            retryable = False
            auto_retry_allowed = False
        else:
            status = RepairTaskStatus.OPEN
            retryable = RepairActionType.is_safe_auto(selected)
            auto_retry_allowed = False  # always False by default

        task = CoverageRepairTask(
            task_id=str(uuid.uuid4()),
            symbol=symbol,
            market=market,
            universe_id=universe_id,
            universe_tier=universe_tier,
            profile=profile,
            issue_type=issue_type,
            issue_code=issue_code,
            issue_field=issue_field,
            status=status,
            quality_status=quality_status,
            quality_score=quality_score,
            coverage_status=coverage_status,
            provider_id=provider_id,
            provider_status=provider_status,
            provider_capability=provider_capability,
            source=source,
            blocking_reason=blocking_reason,
            warnings=warnings or [],
            missing_fields=missing_fields or [],
            stale_fields=stale_fields or [],
            invalid_fields=invalid_fields or [],
            inconsistent_fields=inconsistent_fields or [],
            suggested_actions=suggested,
            selected_action=selected,
            retryable=retryable,
            auto_retry_allowed=auto_retry_allowed,
            destructive=False,
            source_report_id=source_report_id,
            metadata=metadata or {},
            no_real_orders=True,
            production_trading_blocked=True,
        )
        task.dedup_key = task.build_dedup_key()
        return task

    def from_coverage_record(self, record: Any) -> List[CoverageRepairTask]:
        """Build tasks from a UniverseCoverageRecord or dict."""
        tasks: List[CoverageRepairTask] = []
        try:
            if hasattr(record, "__dict__"):
                d = {k: v for k, v in record.__dict__.items()}
            elif isinstance(record, dict):
                d = record
            else:
                return tasks

            symbol = d.get("symbol") or d.get("ticker") or ""
            market = d.get("market", "")
            universe_id = d.get("universe_id", "")
            universe_tier = d.get("tier", "") or d.get("universe_tier", "")
            profile = d.get("profile", "")
            coverage_status = d.get("coverage_status") or d.get("status", "")
            quality_status = d.get("quality_status", "")
            quality_score = d.get("quality_score")
            provider_id = d.get("provider_id")
            source_report_id = d.get("report_id", "") or d.get("source_report_id", "")

            # Map coverage status to issue type
            issue_type = self.map_issue_type(coverage_status)
            if issue_type == RepairIssueType.UNKNOWN and coverage_status in ("COVERED", "PASS", "OK"):
                return tasks  # no issue

            missing_fields = d.get("missing_fields") or []
            stale_fields = d.get("stale_fields") or []
            invalid_fields = d.get("invalid_fields") or []

            task = self.build_task(
                symbol=symbol,
                issue_type=issue_type,
                market=market,
                universe_id=universe_id,
                universe_tier=universe_tier,
                profile=profile,
                quality_status=quality_status,
                quality_score=quality_score,
                coverage_status=coverage_status,
                provider_id=provider_id,
                missing_fields=missing_fields,
                stale_fields=stale_fields,
                invalid_fields=invalid_fields,
                source="coverage_record",
                source_report_id=source_report_id,
            )
            tasks.append(task)
        except Exception as exc:
            logger.warning("from_coverage_record error: %s", exc)
        return tasks

    def from_quality_report(self, report: Any) -> List[CoverageRepairTask]:
        """Build tasks from a quality report dict or object."""
        tasks: List[CoverageRepairTask] = []
        try:
            if hasattr(report, "to_dict"):
                d = report.to_dict()
            elif isinstance(report, dict):
                d = report
            else:
                return tasks

            symbol = d.get("symbol") or d.get("ticker") or ""
            profile = d.get("profile", "")
            quality_status = d.get("overall_status") or d.get("status", "")
            quality_score = d.get("score") or d.get("quality_score")
            source_report_id = d.get("report_id", "")
            provider_id = d.get("provider_id")

            issues = d.get("issues") or []
            if not issues and quality_status not in ("PASS", "OK", ""):
                issues = [{"type": quality_status, "field": "", "detail": ""}]

            for iss in issues:
                issue_type = self.map_issue_type(iss.get("type", "") or quality_status)
                issue_field = iss.get("field", "") or ""
                issue_code = iss.get("code", "") or ""
                task = self.build_task(
                    symbol=symbol,
                    issue_type=issue_type,
                    profile=profile,
                    issue_field=issue_field,
                    issue_code=issue_code,
                    quality_status=quality_status,
                    quality_score=quality_score,
                    provider_id=provider_id,
                    source="quality_report",
                    source_report_id=source_report_id,
                )
                tasks.append(task)
        except Exception as exc:
            logger.warning("from_quality_report error: %s", exc)
        return tasks

    def from_provider_error(self, error: Any, symbol: str, profile: str) -> CoverageRepairTask:
        """Build a task from a provider error."""
        try:
            if hasattr(error, "status"):
                status_str = str(error.status)
            elif isinstance(error, dict):
                status_str = error.get("status") or error.get("error_type", "UNKNOWN")
            else:
                status_str = str(error)

            issue_type = self.map_issue_type(status_str)
            provider_id = getattr(error, "provider_id", None) or (
                error.get("provider_id") if isinstance(error, dict) else None
            )
            blocking = getattr(error, "message", "") or (
                error.get("message", "") if isinstance(error, dict) else ""
            )
            return self.build_task(
                symbol=symbol,
                issue_type=issue_type,
                profile=profile,
                provider_id=provider_id,
                blocking_reason=str(blocking),
                source="provider_error",
            )
        except Exception as exc:
            logger.warning("from_provider_error error: %s", exc)
            return self.build_task(symbol=symbol, issue_type=RepairIssueType.UNKNOWN, profile=profile)

    def from_provider_response(self, response: Any, symbol: str, profile: str) -> List[CoverageRepairTask]:
        """Build tasks from a provider response dict or object."""
        tasks: List[CoverageRepairTask] = []
        try:
            if hasattr(response, "__dict__"):
                d = dict(response.__dict__)
            elif isinstance(response, dict):
                d = response
            else:
                return tasks

            status = d.get("status", "")
            provider_id = d.get("provider_id")
            data_mode = d.get("data_mode", "")

            if status in ("SUCCESS", "OK", "PASS"):
                return tasks

            issue_type = self.map_issue_type(status)
            if data_mode in ("DEMO", "DEMO_ONLY", "MOCK"):
                issue_type = RepairIssueType.DEMO_ONLY_DATA

            task = self.build_task(
                symbol=symbol,
                issue_type=issue_type,
                profile=profile,
                provider_id=provider_id,
                blocking_reason=d.get("error", "") or "",
                source="provider_response",
            )
            tasks.append(task)
        except Exception as exc:
            logger.warning("from_provider_response error: %s", exc)
        return tasks

    def from_profile_result(self, result: Any, symbol: str, profile: str) -> List[CoverageRepairTask]:
        """Build tasks from a DQ profile result."""
        tasks: List[CoverageRepairTask] = []
        try:
            if hasattr(result, "to_dict"):
                d = result.to_dict()
            elif isinstance(result, dict):
                d = result
            else:
                return tasks

            status = d.get("status") or d.get("overall_status", "")
            if status in ("PASS", "OK", ""):
                return tasks

            issue_type = self.map_issue_type(status)
            task = self.build_task(
                symbol=symbol,
                issue_type=issue_type,
                profile=profile,
                quality_status=status,
                quality_score=d.get("score"),
                missing_fields=d.get("missing_fields") or [],
                stale_fields=d.get("stale_fields") or [],
                invalid_fields=d.get("invalid_fields") or [],
                source="profile_result",
            )
            tasks.append(task)
        except Exception as exc:
            logger.warning("from_profile_result error: %s", exc)
        return tasks
