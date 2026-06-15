"""
gui/research_run_registry_adapter.py — ResearchRunRegistryAdapter v1.1.8

Background QThread adapter for ResearchRunRegistryEngine.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry does NOT execute research commands. No Auto Rerun. No Trading.
"""
from __future__ import annotations

import logging
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtCore import QThread, Signal
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


if not _PYSIDE6_AVAILABLE:
    class ResearchRunRegistryAdapter:
        """Stub adapter when PySide6 is not available."""
        def __init__(self, *args, **kwargs):
            logger.info("ResearchRunRegistryAdapter: PySide6 not available, adapter is a stub.")
else:
    class _RegistryEngineWorker(QThread):
        """Background worker for registry engine operations."""

        operation_finished = Signal(dict)
        operation_error = Signal(str)

        def __init__(self, operation: str, kwargs: dict, parent=None):
            super().__init__(parent)
            self._operation = operation
            self._kwargs = kwargs

        def run(self):
            try:
                from research_registry.registry_engine import ResearchRunRegistryEngine
                engine = ResearchRunRegistryEngine()

                if self._operation == "validate":
                    result = engine.validate_registry()
                elif self._operation == "build_summary":
                    result = engine.build_summary().to_dict()
                elif self._operation == "backfill_preview":
                    result = engine.backfill_existing_runs(dry_run=True, allow_write=False)
                elif self._operation == "rebuild_indexes":
                    ok = engine.rebuild_indexes()
                    result = {"success": ok}
                elif self._operation == "compare_runs":
                    run_a = self._kwargs.get("run_a", "")
                    run_b = self._kwargs.get("run_b", "")
                    comp = engine.compare_runs(run_a, run_b)
                    result = comp.to_dict() if comp else {"error": "Comparison failed"}
                else:
                    result = {"error": f"Unknown operation: {self._operation}"}

                self.operation_finished.emit(result)
            except Exception as exc:
                logger.warning("_RegistryEngineWorker error: %s", exc)
                self.operation_error.emit(str(exc))

    class ResearchRunRegistryAdapter:
        """
        Adapter for running ResearchRunRegistryEngine in a background QThread.

        [!] Research Only. No Real Orders.
        [!] Registry does NOT execute research commands.
        """

        no_real_orders = True
        research_only = True

        def __init__(self):
            self._workers: List[_RegistryEngineWorker] = []

        def validate_async(self, on_finished=None, on_error=None):
            """Run registry validation asynchronously."""
            self._run_operation("validate", {}, on_finished, on_error)

        def build_summary_async(self, on_finished=None, on_error=None):
            """Build registry summary asynchronously."""
            self._run_operation("build_summary", {}, on_finished, on_error)

        def backfill_preview_async(self, on_finished=None, on_error=None):
            """Preview backfill asynchronously (dry_run=True)."""
            self._run_operation("backfill_preview", {}, on_finished, on_error)

        def rebuild_indexes_async(self, on_finished=None, on_error=None):
            """Rebuild indexes asynchronously."""
            self._run_operation("rebuild_indexes", {}, on_finished, on_error)

        def compare_runs_async(self, run_a: str, run_b: str, on_finished=None, on_error=None):
            """Compare two runs asynchronously."""
            self._run_operation("compare_runs", {"run_a": run_a, "run_b": run_b}, on_finished, on_error)

        def _run_operation(self, operation: str, kwargs: dict, on_finished=None, on_error=None):
            worker = _RegistryEngineWorker(operation=operation, kwargs=kwargs)
            if on_finished:
                worker.operation_finished.connect(on_finished)
            if on_error:
                worker.operation_error.connect(on_error)
            self._workers.append(worker)
            worker.start()
