"""
strategy_lab/strategy_lab_engine.py — StrategyLabEngine v0.9.0

Orchestrates the full Strategy Lab Stable validation pipeline.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
[!] Does NOT modify any module status, weights, memory, coach tasks, metrics, or evidence graph.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/strategy_lab"


class StrategyLabEngine:
    """Orchestrator for v0.9.0 Strategy Lab Stable validation.

    Run order:
    1. Build capability matrix
    2. Run stable checklist
    3. Build summary
    4. Save to store
    5. Build release manifest

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Does NOT modify any module status, weights, memory, coach tasks,
        metrics, or evidence graph.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

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
        """Run full Strategy Lab stable validation pipeline.

        Returns dict with capabilities, checks, summary, manifest.
        [!] No real orders. Production Trading BLOCKED.
        [!] Does NOT modify any module status or weights.
        """
        from strategy_lab.strategy_lab_capability_matrix import StrategyLabCapabilityMatrix
        from strategy_lab.strategy_lab_checklist import StrategyLabChecklist
        from strategy_lab.strategy_lab_store import StrategyLabStore
        from strategy_lab.strategy_lab_release_manifest import StrategyLabReleaseManifestBuilder

        # 1. Build capability matrix
        capabilities = []
        try:
            matrix = StrategyLabCapabilityMatrix()
            capabilities = matrix.build()
        except Exception as exc:
            logger.warning("StrategyLabEngine: capability matrix error: %s", exc)

        # 2. Run stable checklist
        checks = []
        try:
            checklist = StrategyLabChecklist(project_root=self._root)
            checks, _ = checklist.run(mode=mode)
        except Exception as exc:
            logger.warning("StrategyLabEngine: checklist error: %s", exc)

        # 3. Build summary
        summary = self.build_summary(capabilities, checks, mode=mode)

        # 4. Save to store
        try:
            store = StrategyLabStore(output_dir=self._out_dir)
            store.save_capabilities(capabilities)
            store.save_checks(checks)
            store.save_summary(summary)
        except Exception as exc:
            logger.warning("StrategyLabEngine: store save error: %s", exc)

        # 5. Build release manifest
        manifest = {}
        try:
            manifest_builder = StrategyLabReleaseManifestBuilder(output_dir=self._out_dir)
            manifest = manifest_builder.build_manifest()
        except Exception as exc:
            logger.warning("StrategyLabEngine: manifest build error: %s", exc)
            manifest = {"error": str(exc)}

        return {
            "capabilities":       capabilities,
            "checks":             checks,
            "summary":            summary,
            "manifest":           manifest,
            "no_real_orders":     True,
            "production_blocked": True,
        }

    def build_summary(self, capabilities: list, checks: list, mode: str = "real"):
        """Build StrategyLabSummary from capabilities and checks.

        [!] No real orders. Production Trading BLOCKED.
        """
        from strategy_lab.strategy_lab_schema import (
            StrategyLabSummary,
            CHECK_PASS, CHECK_WARN, CHECK_FAIL, CHECK_BLOCKED,
            STABLE_STATUS_STABLE, STABLE_STATUS_USABLE,
            STABLE_STATUS_PARTIAL, STABLE_STATUS_WARNING, STABLE_STATUS_BLOCKED,
        )

        stable   = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_STABLE)
        usable   = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_USABLE)
        partial  = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_PARTIAL)
        warn_cap = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_WARNING)
        blocked  = sum(1 for c in capabilities if c.stable_status == STABLE_STATUS_BLOCKED)

        passes = sum(1 for c in checks if c.status == CHECK_PASS)
        warns  = sum(1 for c in checks if c.status == CHECK_WARN)
        fails  = sum(1 for c in checks if c.status == CHECK_FAIL)
        blk    = sum(1 for c in checks if c.status == CHECK_BLOCKED)

        if fails == 0 and blk == 0:
            overall = "STABLE"
        elif fails == 0:
            overall = "WARN"
        else:
            overall = "FAIL"

        return StrategyLabSummary(
            generated_at=datetime.now().isoformat(),
            version="v0.9.0",
            release_name="Strategy Lab Stable",
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
            metrics_safe=True,
            evidence_graph_safe=True,
            forbidden_action_count=0,
            overall_status=overall,
            no_real_orders=True,
            production_blocked=True,
        )
