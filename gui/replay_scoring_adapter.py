"""
gui/replay_scoring_adapter.py — Adapter for QThread-based async scoring for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Scoring NEVER triggers paper orders or broker execution.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SCORING_TRIGGERS_NO_ORDERS = True

try:
    from PySide6.QtCore import QThread, Signal, QObject
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


if _QT_AVAILABLE:
    class ReplayScoringWorker(QObject):
        """Worker for running scoring in a background thread."""
        finished = Signal(dict)
        error = Signal(str)

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        SCORING_TRIGGERS_NO_ORDERS = True

        def __init__(
            self,
            task: str,
            session_id: str,
            repo_root: Optional[str] = None,
            kwargs: Optional[Dict[str, Any]] = None,
        ):
            super().__init__()
            self._task = task
            self._session_id = session_id
            self._repo_root = repo_root
            self._kwargs = kwargs or {}

        def run(self) -> None:
            try:
                result = self._execute()
                result["simulation_only"] = True
                result["research_only"] = True
                result["no_real_orders"] = True
                self.finished.emit(result)
            except Exception as exc:
                logger.error("Scoring worker error: %s", exc, exc_info=True)
                self.error.emit(str(exc))

        def _execute(self) -> Dict[str, Any]:
            if self._task == "score_process":
                from replay.process_score_engine import ReplayProcessScoreEngine
                engine = ReplayProcessScoreEngine()
                score = engine.score(
                    session_id=self._session_id,
                    **self._kwargs,
                )
                return score.to_dict()
            elif self._task == "detect_mistakes":
                from replay.mistake_detector import ReplayMistakeDetector
                detector = ReplayMistakeDetector()
                mistakes = detector.detect(
                    session_id=self._session_id,
                    **self._kwargs,
                )
                return {
                    "mistakes": [m.to_dict() for m in mistakes],
                    "count": len(mistakes),
                }
            elif self._task == "preview_reveal":
                from replay.outcome_reveal import ReplayOutcomeRevealManager
                mgr = ReplayOutcomeRevealManager()
                preview = mgr.preview(
                    session_id=self._session_id,
                    **self._kwargs,
                )
                return preview
            else:
                return {"error": f"Unknown task: {self._task}"}

    class ReplayScoringAdapter:
        """
        Adapter that manages QThread workers for scoring operations.
        [!] Research Only. Scoring never triggers orders.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        SCORING_TRIGGERS_NO_ORDERS = True

        def __init__(self, repo_root: Optional[str] = None):
            self._repo_root = repo_root
            self._threads = []

        def run_async(
            self,
            task: str,
            session_id: str,
            on_finished: Callable[[Dict[str, Any]], None],
            on_error: Callable[[str], None],
            kwargs: Optional[Dict[str, Any]] = None,
        ) -> None:
            """Run a scoring task asynchronously in a QThread."""
            thread = QThread()
            worker = ReplayScoringWorker(
                task=task,
                session_id=session_id,
                repo_root=self._repo_root,
                kwargs=kwargs,
            )
            worker.moveToThread(thread)
            thread.started.connect(worker.run)
            worker.finished.connect(on_finished)
            worker.error.connect(on_error)
            worker.finished.connect(thread.quit)
            worker.error.connect(thread.quit)
            thread.finished.connect(thread.deleteLater)
            self._threads.append(thread)
            thread.start()

else:
    # Stub when Qt not available
    class ReplayScoringAdapter:
        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        SCORING_TRIGGERS_NO_ORDERS = True

        def __init__(self, repo_root=None):
            self._repo_root = repo_root

        def run_async(self, task, session_id, on_finished, on_error, kwargs=None):
            logger.warning("PySide6 not available — async scoring not supported.")
            on_error("PySide6 not available")
