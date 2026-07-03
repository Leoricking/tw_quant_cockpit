"""
paper_trading/operational_integration/integration_context_v168.py
Integration Context Builder for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict
from datetime import datetime, timezone

from .models_v168 import IntegrationContext
from .enums_v168 import IntegrationMode

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class IntegrationContextBuilder:
    """Builds and validates IntegrationContext instances. Research only."""

    def build(
        self,
        run_id: str,
        session_id: str,
        mode: IntegrationMode = IntegrationMode.RESEARCH_ONLY,
        period_start: str = "2024-01-01",
        period_end: str = "2024-12-31",
        timezone: str = "Asia/Taipei",
        component_id: str = "integration_pipeline",
        source_lineage: str = "",
    ) -> IntegrationContext:
        """Build an IntegrationContext with validated inputs."""
        if not run_id:
            raise ValueError("run_id cannot be empty")
        if not session_id:
            raise ValueError("session_id cannot be empty")
        if period_start > period_end:
            raise ValueError(f"period_start {period_start!r} > period_end {period_end!r}")
        return IntegrationContext(
            run_id=run_id,
            session_id=session_id,
            component_id=component_id,
            period_start=period_start,
            period_end=period_end,
            timezone=timezone,
            created_at=_utcnow_iso(),
            source_lineage=source_lineage or f"integration_context:{run_id}",
            mode=mode,
        )

    def validate_context(self, ctx: IntegrationContext) -> Dict[str, Any]:
        """Validate a context object for completeness and safety."""
        errors = []
        warnings = []

        if not ctx.run_id:
            errors.append("missing run_id")
        if not ctx.session_id:
            errors.append("missing session_id")
        if not ctx.period_start:
            errors.append("missing period_start")
        if not ctx.period_end:
            errors.append("missing period_end")
        if ctx.period_start > ctx.period_end:
            errors.append(f"reversed_period: {ctx.period_start} > {ctx.period_end}")
        if not ctx.paper_only:
            errors.append("paper_only must be True")
        if not ctx.research_only:
            errors.append("research_only must be True")
        if not ctx.read_only:
            errors.append("read_only must be True")
        if not ctx.no_real_orders:
            errors.append("no_real_orders must be True")
        if not ctx.timezone:
            warnings.append("missing timezone, defaulting to Asia/Taipei")

        valid = len(errors) == 0
        return {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
            "paper_only": True,
            "research_only": True,
        }

    def build_from_fixture(self, fixture: dict) -> IntegrationContext:
        """Build an IntegrationContext from a fixture dict."""
        if not fixture.get("paper_only", False):
            raise ValueError("fixture must have paper_only=True")
        if not fixture.get("research_only", False):
            raise ValueError("fixture must have research_only=True")

        inp = fixture.get("input", fixture)
        return self.build(
            run_id=inp.get("run_id", "fixture_run"),
            session_id=inp.get("session_id", "fixture_session"),
            mode=IntegrationMode(inp.get("mode", "RESEARCH_ONLY")),
            period_start=inp.get("period_start", "2024-01-01"),
            period_end=inp.get("period_end", "2024-12-31"),
            timezone=inp.get("timezone", "Asia/Taipei"),
            component_id=inp.get("component_id", "fixture_component"),
            source_lineage=inp.get("source_lineage", fixture.get("fixture_id", "fixture")),
        )
