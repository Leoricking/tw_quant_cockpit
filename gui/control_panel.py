"""
gui/control_panel.py - Top toolbar for TW Quant Cockpit.

Provides mode switching, data source selection, and action buttons
for the main cockpit window.
"""

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox, QSizePolicy,
    )
    from PySide6.QtCore import Signal, Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _btn(text, color=None, bold=False):
    """Create a styled QPushButton."""
    b = QPushButton(text)
    style = "padding:4px 10px; border-radius:3px;"
    if color:
        style += f"background:{color}; color:#FFFFFF;"
    if bold:
        style += "font-weight:bold;"
    b.setStyleSheet(style)
    b.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return b


class ControlPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Top toolbar widget.

    Signals
    -------
    mode_changed(str)           : 'mock' or 'real'
    source_changed(str)         : 'watchlist', 'profile', 'screener'
    refresh_screener_requested()
    data_check_requested()
    report_requested()
    import_requested()
    """

    if _PYSIDE6_AVAILABLE:
        mode_changed = Signal(str)
        source_changed = Signal(str)
        refresh_screener_requested = Signal()
        data_check_requested = Signal()
        report_requested = Signal()
        import_requested = Signal()

    def __init__(self, gui_state=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self._state = gui_state
        if _PYSIDE6_AVAILABLE:
            self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        # Mode selector
        layout.addWidget(QLabel("模式："))
        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["MOCK", "REAL"])
        self._mode_combo.setFixedWidth(80)
        self._mode_combo.setStyleSheet(
            "QComboBox { background:#252540; color:#FFFFFF; padding:2px 4px; }"
        )
        self._mode_combo.currentTextChanged.connect(self._on_mode_changed)
        layout.addWidget(self._mode_combo)

        # Source selector
        layout.addWidget(QLabel("自選股："))
        self._source_combo = QComboBox()
        self._source_combo.addItems(["screener", "profile CSV", "watchlist"])
        self._source_combo.setFixedWidth(110)
        self._source_combo.setStyleSheet(
            "QComboBox { background:#252540; color:#FFFFFF; padding:2px 4px; }"
        )
        self._source_combo.currentTextChanged.connect(self._on_source_changed)
        layout.addWidget(self._source_combo)

        layout.addSpacing(6)

        # Action buttons
        self._btn_refresh = _btn("⟳ 刷新篩選", "#2266AA", bold=True)
        self._btn_refresh.clicked.connect(self.refresh_screener_requested)
        layout.addWidget(self._btn_refresh)

        self._btn_dcheck = _btn("✔ Data Check", "#226644")
        self._btn_dcheck.clicked.connect(self.data_check_requested)
        layout.addWidget(self._btn_dcheck)

        self._btn_report = _btn("📋 產生報告", "#664422")
        self._btn_report.clicked.connect(self.report_requested)
        layout.addWidget(self._btn_report)

        self._btn_import = _btn("⬆ 匯入 CSV", "#334466")
        self._btn_import.clicked.connect(self.import_requested)
        layout.addWidget(self._btn_import)

        self._btn_open_report = _btn("📂 報告資料夾", "#2A2A2A")
        self._btn_open_report.clicked.connect(self._open_report_folder)
        layout.addWidget(self._btn_open_report)

        self._btn_open_data = _btn("📁 資料資料夾", "#2A2A2A")
        self._btn_open_data.clicked.connect(self._open_data_folder)
        layout.addWidget(self._btn_open_data)

        layout.addStretch()

        # Status display
        self._lbl_mode = QLabel("[MOCK]")
        self._lbl_mode.setStyleSheet("color:#33CCFF; font-weight:bold;")
        layout.addWidget(self._lbl_mode)

        self._lbl_refresh_time = QLabel("Last: —")
        self._lbl_refresh_time.setStyleSheet("color:#888888; font-size:11px;")
        layout.addWidget(self._lbl_refresh_time)

        self._lbl_warning = QLabel("")
        self._lbl_warning.setStyleSheet("color:#FF8888; font-size:11px;")
        layout.addWidget(self._lbl_warning)

        self.setStyleSheet("background:#1A1A2E; border-bottom:1px solid #333355;")

    def _on_mode_changed(self, text):
        mode = 'real' if text == 'REAL' else 'mock'
        if self._state:
            self._state.set_mode(mode)
        tag = '[REAL]' if mode == 'real' else '[MOCK]'
        color = '#FF8800' if mode == 'real' else '#33CCFF'
        self._lbl_mode.setText(tag)
        self._lbl_mode.setStyleSheet(f"color:{color}; font-weight:bold;")
        self.mode_changed.emit(mode)

    def _on_source_changed(self, text):
        src_map = {'screener': 'screener', 'profile CSV': 'profile', 'watchlist': 'watchlist'}
        src = src_map.get(text, 'screener')
        if self._state:
            self._state.watchlist_source = src
        self.source_changed.emit(src)

    def _open_report_folder(self):
        import subprocess
        try:
            folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  'data', 'reports')
            os.makedirs(folder, exist_ok=True)
            subprocess.Popen(f'explorer "{folder}"')
        except Exception as exc:
            logger.warning("Cannot open report folder: %s", exc)

    def _open_data_folder(self):
        import subprocess
        try:
            folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  'data', 'import')
            os.makedirs(folder, exist_ok=True)
            subprocess.Popen(f'explorer "{folder}"')
        except Exception as exc:
            logger.warning("Cannot open data folder: %s", exc)

    def update_status(self, refresh_time=None, warning=None):
        if not _PYSIDE6_AVAILABLE:
            return
        if refresh_time:
            self._lbl_refresh_time.setText(f"Last: {refresh_time}")
        if warning is not None:
            self._lbl_warning.setText(warning)

    def get_mode(self) -> str:
        if not _PYSIDE6_AVAILABLE:
            return 'mock'
        return 'real' if self._mode_combo.currentText() == 'REAL' else 'mock'
