"""
gui/report_panel.py - Stock report display panel for TW Quant Cockpit.

Shows the most recently generated stock-report, the output file path,
and a button to generate a new report for the currently selected symbol.
"""

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTextEdit, QSizePolicy,
    )
    from PySide6.QtCore import Signal, Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


class ReportPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Panel for generating and viewing stock analysis reports.
    """

    if _PYSIDE6_AVAILABLE:
        report_requested = Signal(str)  # emits selected symbol

    def __init__(self, gui_state=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self._state = gui_state
        if _PYSIDE6_AVAILABLE:
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Header + buttons row
        top = QHBoxLayout()
        top.addWidget(QLabel("Report"))

        self._lbl_symbol = QLabel("—")
        self._lbl_symbol.setStyleSheet("color:#AAAAFF; font-weight:bold;")
        top.addWidget(self._lbl_symbol)
        top.addStretch()

        gen_btn = QPushButton("📋 產生報告")
        gen_btn.setStyleSheet("background:#664422; color:#FFFFFF; padding:3px 10px;")
        gen_btn.clicked.connect(self._on_generate)
        top.addWidget(gen_btn)

        open_btn = QPushButton("📂 報告資料夾")
        open_btn.setStyleSheet("background:#333355; color:#FFFFFF; padding:3px 10px;")
        open_btn.clicked.connect(self._open_folder)
        top.addWidget(open_btn)

        layout.addLayout(top)

        # File path label
        self._lbl_path = QLabel("路徑：—")
        self._lbl_path.setStyleSheet("color:#888888; font-size:11px;")
        self._lbl_path.setWordWrap(True)
        layout.addWidget(self._lbl_path)

        # Report content display
        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setStyleSheet(
            "background:#0A0A14; color:#CCCCCC; font-family:monospace; font-size:11px;"
        )
        layout.addWidget(self._text)

    def _on_generate(self):
        if not _PYSIDE6_AVAILABLE:
            return
        sym = self._state.selected_symbol if self._state else None
        if sym:
            self.report_requested.emit(sym)
        else:
            self._text.setPlainText("請先在左側點選一支股票，再按產生報告。")

    def _open_folder(self):
        import subprocess
        try:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder = os.path.join(base, 'data', 'reports')
            os.makedirs(folder, exist_ok=True)
            subprocess.Popen(f'explorer "{folder}"')
        except Exception as exc:
            logger.warning("Cannot open report folder: %s", exc)

    def show_report(self, report_text: str, file_path: str = None, symbol: str = None):
        """Display a report string in the panel."""
        if not _PYSIDE6_AVAILABLE:
            return
        if symbol:
            self._lbl_symbol.setText(str(symbol))
        if file_path:
            self._lbl_path.setText(f"路徑：{file_path}")
        if report_text:
            # Show first ~80 lines as summary
            lines = report_text.splitlines()
            preview = '\n'.join(lines[:80])
            if len(lines) > 80:
                preview += f"\n\n… (共 {len(lines)} 行，完整報告見上方路徑)"
            self._text.setPlainText(preview)

    def show_status(self, msg: str):
        if not _PYSIDE6_AVAILABLE:
            return
        self._text.setPlainText(msg)
