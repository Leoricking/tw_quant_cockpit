"""
GUI Threading helpers — safe QThread lifecycle management.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class SafeWorkerResult:
    """Result returned by SafeWorker after execution."""
    success: bool = False
    data: Any = None
    error: str = ""
    warning: str = ""


try:
    from PySide6.QtCore import QThread, Signal, QObject

    class SafeWorker(QObject):
        """
        A QObject-based worker for safe QThread execution.
        Prevents QThread destroyed while running warnings.
        Research Only. No Real Orders.
        """
        finished = Signal(object)   # emits SafeWorkerResult
        error_occurred = Signal(str)

        def __init__(self, fn: Callable, *args, **kwargs):
            super().__init__()
            self._fn = fn
            self._args = args
            self._kwargs = kwargs
            self._running = False

        def run(self):
            self._running = True
            try:
                data = self._fn(*self._args, **self._kwargs)
                result = SafeWorkerResult(success=True, data=data)
            except Exception as exc:  # noqa: BLE001
                result = SafeWorkerResult(
                    success=False,
                    error=f"Worker error: {exc}",
                )
                self.error_occurred.emit(str(exc))
            finally:
                self._running = False
            self.finished.emit(result)

        def is_running(self) -> bool:
            return self._running

    def run_in_qthread(
        parent: QObject,
        fn: Callable,
        on_finished: Callable,
        *args,
        **kwargs,
    ) -> tuple:
        """
        Run fn in a QThread, call on_finished(SafeWorkerResult) when done.
        Returns (thread, worker) — caller must keep references to prevent GC.
        Research Only. No Real Orders.
        """
        thread = QThread(parent)
        worker = SafeWorker(fn, *args, **kwargs)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(on_finished)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        return thread, worker

    def cleanup_thread(thread: Optional[QThread], timeout_ms: int = 2000) -> None:
        """
        Safely stop and wait for a QThread.
        Call from closeEvent to prevent QThread destroyed warnings.
        Research Only. No Real Orders.
        """
        if thread is None:
            return
        if thread.isRunning():
            thread.quit()
            thread.wait(timeout_ms)

except ImportError:
    # PySide6 not available — provide stub classes for non-GUI environments

    class SafeWorker:  # type: ignore[no-redef]
        """Stub SafeWorker when PySide6 is not available."""
        def __init__(self, fn=None, *args, **kwargs):
            self._fn = fn
            self._args = args
            self._kwargs = kwargs

        def run(self):
            if self._fn:
                try:
                    return SafeWorkerResult(success=True, data=self._fn(*self._args, **self._kwargs))
                except Exception as exc:  # noqa: BLE001
                    return SafeWorkerResult(success=False, error=str(exc))
            return SafeWorkerResult(success=False, error="No function provided")

        def is_running(self) -> bool:
            return False

    def run_in_qthread(parent, fn, on_finished, *args, **kwargs):
        """Stub run_in_qthread when PySide6 is not available."""
        return None, None

    def cleanup_thread(thread, timeout_ms=2000):
        """Stub cleanup_thread when PySide6 is not available."""
        pass
