"""
coach/data_repair_planner.py — DataRepairPlanner (v0.4.8).

Builds data repair priority list from Data Quality Gate / Provider Reliability.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT modify .env. Does NOT show tokens. Does NOT auto-fetch real data.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from coach.coach_schema import (
    CoachRecommendation,
    REC_DATA_REPAIR,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    CAT_DATA, CAT_PROVIDER,
    EFFORT_QUICK, EFFORT_MEDIUM,
    DUE_TODAY, DUE_THIS_WEEK,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)


class DataRepairPlanner:
    """
    Builds data repair priority recommendations.

    Data repair actions:
      - update-data dry-run
      - provider-reliability check
      - provider-health check
      - data-quality-gate check
      - intraday-quality check
      - api-fetch-diagnostics
      - check FINMIND_TOKEN setup (no token shown)
      - check XQ intraday folder

    Safety:
      Does NOT modify .env.
      Does NOT show token values.
      Does NOT auto-fetch real data.
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def build(
        self,
        repair_data:    dict = None,
        review_summary: dict = None,
    ) -> List[CoachRecommendation]:
        """Build data repair priority recommendations."""
        repair_data    = repair_data    or {}
        review_summary = review_summary or {}

        quality_data  = repair_data.get("quality", {}) or {}
        provider_data = repair_data.get("provider", {}) or {}

        items: List[CoachRecommendation] = []

        # Provider failures from provider reliability
        failed_providers = provider_data.get("failed_providers", [])
        if isinstance(failed_providers, list):
            for p in failed_providers[:3]:
                provider_name = p.get("name", "unknown") if isinstance(p, dict) else str(p)
                items.append(CoachRecommendation(
                    recommendation_type=REC_DATA_REPAIR,
                    priority=PRIORITY_P0,
                    category=CAT_PROVIDER,
                    title=f"Provider Failure: {provider_name}",
                    summary=f"Provider '{provider_name}' is failing. Check health and fallback.",
                    suggested_command="python main.py provider-reliability --mode real",
                    expected_benefit="Restore data provider before research session.",
                    effort_level=EFFORT_QUICK,
                    due_type=DUE_TODAY,
                    tags=["provider", "repair", "urgent"],
                    status=STATUS_OPEN,
                ))

        # API token missing (no token shown)
        token_missing = provider_data.get("token_missing", [])
        if isinstance(token_missing, list) and token_missing:
            items.append(CoachRecommendation(
                recommendation_type=REC_DATA_REPAIR,
                priority=PRIORITY_P1,
                category=CAT_PROVIDER,
                title="API Token Setup Required",
                summary="One or more API tokens are missing. Check .env setup (do not share token).",
                suggested_command="python main.py provider-reliability --mode real",
                expected_benefit="Enable data provider access for research.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_TODAY,
                tags=["provider", "token", "setup"],
                status=STATUS_OPEN,
            ))

        # Stale data from data quality gate
        stale_datasets = quality_data.get("stale_datasets", [])
        if isinstance(stale_datasets, list):
            for ds in stale_datasets[:3]:
                ds_name = ds.get("dataset", "unknown") if isinstance(ds, dict) else str(ds)
                items.append(CoachRecommendation(
                    recommendation_type=REC_DATA_REPAIR,
                    priority=PRIORITY_P1,
                    category=CAT_DATA,
                    title=f"Stale Data: {ds_name}",
                    summary=f"Dataset '{ds_name}' is stale. Run update-data dry-run to check.",
                    suggested_command="python main.py data-quality-gate --mode real",
                    expected_benefit="Ensure data freshness before backtest or research.",
                    effort_level=EFFORT_QUICK,
                    due_type=DUE_TODAY,
                    tags=["data", "stale", "repair"],
                    status=STATUS_OPEN,
                ))

        # Missing datasets
        missing_datasets = quality_data.get("missing_datasets", [])
        if isinstance(missing_datasets, list):
            for ds in missing_datasets[:3]:
                ds_name = ds.get("dataset", "unknown") if isinstance(ds, dict) else str(ds)
                items.append(CoachRecommendation(
                    recommendation_type=REC_DATA_REPAIR,
                    priority=PRIORITY_P1,
                    category=CAT_DATA,
                    title=f"Missing Dataset: {ds_name}",
                    summary=f"Dataset '{ds_name}' is missing. Check data source and fetch status.",
                    suggested_command="python main.py data-quality-gate --mode real",
                    expected_benefit="Fill data gaps required for research.",
                    effort_level=EFFORT_MEDIUM,
                    due_type=DUE_TODAY,
                    tags=["data", "missing", "repair"],
                    status=STATUS_OPEN,
                ))

        # Intraday data issues
        intraday_issues = quality_data.get("intraday_missing", [])
        if isinstance(intraday_issues, list) and intraday_issues:
            items.append(CoachRecommendation(
                recommendation_type=REC_DATA_REPAIR,
                priority=PRIORITY_P2,
                category=CAT_DATA,
                title="Intraday Data Missing",
                summary="Some intraday data is missing. Check XQ intraday folder and provider.",
                suggested_command="python main.py data-quality-gate --mode real",
                expected_benefit="Ensure intraday data is available for replay and backtest.",
                effort_level=EFFORT_MEDIUM,
                due_type=DUE_TODAY,
                tags=["data", "intraday", "repair"],
                status=STATUS_OPEN,
            ))

        # From review_summary: data_blockers
        blockers = int(review_summary.get("data_blockers", 0) or 0)
        if blockers > 0 and not items:
            items.append(CoachRecommendation(
                recommendation_type=REC_DATA_REPAIR,
                priority=PRIORITY_P1,
                category=CAT_DATA,
                title=f"{blockers} Data Blocker(s) Detected",
                summary=f"Research Review found {blockers} data blocker(s). Run data-quality-gate to identify.",
                suggested_command="python main.py data-quality-gate --mode real",
                expected_benefit="Resolve data blockers before backtest or research.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_TODAY,
                tags=["data", "blocker", "repair"],
                status=STATUS_OPEN,
            ))

        # Always: suggest diagnostics check
        provider_warnings = int(review_summary.get("provider_warnings", 0) or 0)
        if provider_warnings > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_DATA_REPAIR,
                priority=PRIORITY_P2,
                category=CAT_PROVIDER,
                title=f"{provider_warnings} Provider Warning(s)",
                summary=f"{provider_warnings} provider warning(s) in Research Review. Run reliability check.",
                suggested_command="python main.py provider-reliability --mode real",
                expected_benefit="Identify and resolve provider degradation before research.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_TODAY,
                tags=["provider", "warning"],
                status=STATUS_OPEN,
            ))

        return items
