"""
gui/replay_scoring_panel.py — Replay Scoring Panel for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Scoring NEVER triggers paper orders or broker execution.
[!] Safety banner ALWAYS visible.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SCORING_TRIGGERS_NO_ORDERS = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QFrame, QGroupBox, QScrollArea,
        QSizePolicy, QTextEdit,
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    _QT_AVAILABLE = True
except ImportError:
    _QT_AVAILABLE = False


def create_replay_scoring_panel(
    repo_root: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Optional[Any]:
    """
    Create the replay scoring panel widget.
    Returns None if Qt is not available.
    [!] Safety banner always visible.
    """
    if not _QT_AVAILABLE:
        logger.warning("PySide6 not available — replay_scoring_panel GUI not created.")
        return None

    panel = ReplayScoringPanel(repo_root=repo_root, session_id=session_id)
    return panel


if _QT_AVAILABLE:
    class ReplayScoringPanel(QWidget):
        """
        Main scoring panel with safety banner.
        [!] Research Only. No Real Orders. Scoring Triggers No Orders.
        """

        RESEARCH_ONLY = True
        NO_REAL_ORDERS = True
        SCORING_TRIGGERS_NO_ORDERS = True

        def __init__(
            self,
            repo_root: Optional[str] = None,
            session_id: Optional[str] = None,
            parent: Optional[Any] = None,
        ):
            super().__init__(parent)
            self._repo_root = repo_root
            self._session_id = session_id
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)
            layout.setSpacing(6)
            layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner — always visible
            banner = QLabel(
                "[!] Research Only | No Real Orders | "
                "Scoring NEVER Triggers Orders | Simulation Training Only"
            )
            banner.setStyleSheet(
                "background: #2c1a00; color: #ffcc00; "
                "padding: 6px; border-radius: 4px; font-weight: bold;"
            )
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # Header
            header = QLabel("Replay Scoring & Mistake Taxonomy v1.2.3")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            header.setFont(font)
            layout.addWidget(header)

            # Session info
            session_label = QLabel(
                f"Session: {self._session_id or '(none selected)'}"
            )
            layout.addWidget(session_label)

            # Score section
            score_group = QGroupBox("Process Score")
            score_layout = QVBoxLayout(score_group)

            self._process_score_label = QLabel("Process Score: Not scored")
            score_layout.addWidget(self._process_score_label)

            btn_score = QPushButton("Score Process")
            btn_score.clicked.connect(self._on_score_process)
            score_layout.addWidget(btn_score)

            layout.addWidget(score_group)

            # Outcome reveal section
            reveal_group = QGroupBox("Outcome Reveal")
            reveal_layout = QVBoxLayout(reveal_group)

            self._reveal_label = QLabel("Outcome Reveal: BLOCKED (explicit reveal required)")
            reveal_layout.addWidget(self._reveal_label)

            btn_preview = QPushButton("Preview Outcome (No Reveal)")
            btn_preview.clicked.connect(self._on_preview_outcome)
            reveal_layout.addWidget(btn_preview)

            layout.addWidget(reveal_group)

            # Mistake section
            mistake_group = QGroupBox("Mistake Detection")
            mistake_layout = QVBoxLayout(mistake_group)

            self._mistake_label = QLabel("Mistakes: Not detected")
            mistake_layout.addWidget(self._mistake_label)

            btn_detect = QPushButton("Detect Mistakes")
            btn_detect.clicked.connect(self._on_detect_mistakes)
            mistake_layout.addWidget(btn_detect)

            layout.addWidget(mistake_group)

            # Output area
            self._output = QTextEdit()
            self._output.setReadOnly(True)
            self._output.setMaximumHeight(200)
            self._output.setPlainText(
                "[!] Research Only | No Real Orders | Not Investment Advice\n"
                "Select a session and use the buttons above."
            )
            layout.addWidget(self._output)

            layout.addStretch()

        def _on_score_process(self) -> None:
            self._output.setPlainText(
                "[!] Score Process — Research Only | No Real Orders\n"
                f"Session: {self._session_id or '(none)'}\n"
                "Use: python main.py replay-score-process --session-id <id>"
            )

        def _on_preview_outcome(self) -> None:
            self._output.setPlainText(
                "[!] Outcome Preview — BLOCKED by default\n"
                "Use: python main.py replay-outcome-preview --session-id <id> --window 20\n"
                "Actual reveal requires --reveal --confirm-review flags."
            )

        def _on_detect_mistakes(self) -> None:
            self._output.setPlainText(
                "[!] Mistake Detection — All results are SUGGESTED status\n"
                "System cannot auto-confirm mistakes.\n"
                f"Session: {self._session_id or '(none)'}\n"
                "Use: python main.py replay-mistakes-detect --session-id <id>"
            )

        def set_session_id(self, session_id: str) -> None:
            self._session_id = session_id
