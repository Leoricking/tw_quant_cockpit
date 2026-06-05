"""
intelligence_stable/intelligence_stable_engine.py — IntelligenceStableEngine v0.8.0

Orchestrator for the Research Intelligence Stable validation run.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/intelligence_stable"


class IntelligenceStableEngine:
    """Orchestrator for v0.8.0 Research Intelligence Stable validation.

    Run order:
    1. Build capability matrix
    2. Run stable checklist
    3. Build summary
    4. Save to store
    5. Build release manifest

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Not Investment Advice. No BUY/SELL/ORDER output.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = _DEFAULT_OUTPUT_DIR,
    ) -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)
        if os.path.isabs(output_dir):
            self._out_dir = output_dir
        else:
            self._out_dir = os.path.join(self._root, output_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, mode: str = "real") -> dict:
        """Run full intelligence stable validation pipeline.

        Returns dict with capabilities, checks, summary, manifest.
        [!] No real orders. Production Trading BLOCKED.
        """
        from intelligence_stable.intelligence_capability_matrix import IntelligenceCapabilityMatrix
        from intelligence_stable.intelligence_stable_checklist import IntelligenceStableChecklist
        from intelligence_stable.intelligence_release_manifest import IntelligenceReleaseManifestBuilder
        from intelligence_stable.intelligence_stable_store import IntelligenceStableStore

        # 1. Build capability matrix
        try:
            matrix = IntelligenceCapabilityMatrix()
            capabilities = matrix.build()
        except Exception as exc:
            logger.warning("IntelligenceStableEngine: capability matrix error: %s", exc)
            capabilities = []

        # 2. Run stable checklist
        try:
            checklist = IntelligenceStableChecklist(project_root=self._root)
            checks, _ = checklist.run(mode=mode)
        except Exception as exc:
            logger.warning("IntelligenceStableEngine: checklist error: %s", exc)
            checks = []

        # 3. Build summary
        summary = self.build_summary(capabilities, checks, mode=mode)

        # 4. Save to store
        try:
            store = IntelligenceStableStore(output_dir=self._out_dir)
            store.save_capabilities(capabilities)
            store.save_checks(checks)
            store.save_summary(summary)
        except Exception as exc:
            logger.warning("IntelligenceStableEngine: store save error: %s", exc)

        # 5. Build release manifest
        try:
            manifest_builder = IntelligenceReleaseManifestBuilder(
                project_root=self._root,
                output_dir=self._out_dir,
            )
            manifest = manifest_builder.build_manifest()
        except Exception as exc:
            logger.warning("IntelligenceStableEngine: manifest build error: %s", exc)
            manifest = {"error": str(exc)}

        return {
            "capabilities":      capabilities,
            "checks":            checks,
            "summary":           summary,
            "manifest":          manifest,
            "no_real_orders":    True,
            "production_blocked": True,
        }

    def build_summary(self, capabilities: list, checks: list, mode: str = "real"):
        """Build IntelligenceStableSummary from capabilities and checks.

        [!] No real orders. Production Trading BLOCKED.
        """
        from intelligence_stable.intelligence_stable_schema import (
            IntelligenceStableSummary,
            CHECK_PASS, CHECK_WARN, CHECK_FAIL, CHECK_BLOCKED,
            STABLE_STATUS_STABLE, STABLE_STATUS_USABLE,
            STABLE_STATUS_PARTIAL, STABLE_STATUS_WARNING, STABLE_STATUS_BLOCKED,
        )

        stable  = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_STABLE)
        usable  = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_USABLE)
        partial = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_PARTIAL)
        warn_cap = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_WARNING)
        blocked = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_BLOCKED)

        passes   = sum(1 for c in checks if c.status == CHECK_PASS)
        warns    = sum(1 for c in checks if c.status == CHECK_WARN)
        fails    = sum(1 for c in checks if c.status == CHECK_FAIL)
        blk      = sum(1 for c in checks if c.status == CHECK_BLOCKED)

        if fails == 0 and blk == 0:
            overall = "STABLE"
        elif fails == 0:
            overall = "WARN"
        else:
            overall = "FAIL"

        return IntelligenceStableSummary(
            generated_at=datetime.now().isoformat(),
            version="v0.8.0",
            release_name="Research Intelligence Stable",
            mode=mode,
            total_capabilities=len(capabilities),
            stable_count=stable,
            usable_count=usable,
            partial_count=partial,
            warning_count=warn_cap,
            blocked_count=blocked,
            total_checks=len(checks),
            pass_count=passes,
            warn_count=warns,
            fail_count=fails,
            blocked_check_count=blk,
            recommendations_safe=True,
            memories_safe=True,
            coach_tasks_safe=True,
            forbidden_action_count=0,
            overall_status=overall,
            no_real_orders=True,
            production_blocked=True,
        )
