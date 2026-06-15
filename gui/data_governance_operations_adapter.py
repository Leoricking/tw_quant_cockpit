"""
gui.data_governance_operations_adapter — DataGovernanceOperationsAdapter v1.1.6

Background QThread adapter for running DataGovernanceOperationsEngine
and emitting results to the panel.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtCore import QThread, Signal
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


if not _PYSIDE6_AVAILABLE:
    class DataGovernanceOperationsAdapter:
        """Stub adapter when PySide6 is unavailable."""
        def __init__(self, *args, **kwargs):
            logger.info("DataGovernanceOperationsAdapter: PySide6 not available, using stub.")

        def run_async(self, *args, **kwargs):
            pass

        def stop(self):
            pass
else:
    class DataGovernanceOperationsAdapter(QThread):
        """
        Background QThread adapter for governance operations engine.

        Emits finished signal with result dict.
        Emits error signal with error message string.

        [!] Research Only. No Real Orders.
        """

        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, mode: str = "real", tier: str = "research30", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._tier = tier
            self._running = False

        def run_async(self, mode: str = "real", tier: str = "research30"):
            """Start background refresh."""
            self._mode = mode
            self._tier = tier
            if not self.isRunning():
                self.start()

        def run(self):
            """Run governance engine in background."""
            self._running = True
            try:
                from governance_ops.operations_engine import DataGovernanceOperationsEngine
                engine = DataGovernanceOperationsEngine()
                summary = engine.run(mode=self._mode, tier=self._tier)
                module_health = engine.build_module_health()
                symbol_matrix = engine.build_symbol_matrix(tier=self._tier)
                actions = engine.build_action_queue_from_data(symbol_matrix, module_health)
                runs = engine.build_run_audit_summary()
                if self._running:
                    self.finished.emit({
                        "summary": summary,
                        "module_health": module_health,
                        "symbol_matrix": symbol_matrix,
                        "actions": actions,
                        "runs": runs,
                        "research_only": True,
                        "no_real_orders": True,
                    })
            except Exception as exc:
                logger.warning("DataGovernanceOperationsAdapter.run error: %s", exc)
                if self._running:
                    self.error.emit(str(exc))
            finally:
                self._running = False

        def stop(self):
            self._running = False
