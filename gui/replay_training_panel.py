"""gui/replay_training_panel.py — ReplayTrainingPanel for TW Replay Training Cockpit v0.6.3.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice.
[!] Actions run in QThread to avoid GUI freeze.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
        QLineEdit, QComboBox, QScrollArea, QSizePolicy, QMessageBox,
        QInputDialog, QCheckBox, QDateEdit, QTextEdit, QSlider, QSpinBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QDate, QTimer
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ReplayTrainingPanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _SessionWorker(QThread):
        finished = Signal(dict)

        def __init__(self, symbol: str, trade_date: str, timeframe: str, mode: str, adapter):
            super().__init__()
            self._symbol     = symbol
            self._trade_date = trade_date
            self._timeframe  = timeframe
            self._mode       = mode
            self._adapter    = adapter

        def run(self):
            try:
                result = self._adapter.create_session(
                    self._symbol, self._trade_date, self._timeframe, self._mode
                )
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReviewWorker(QThread):
        finished = Signal(dict)

        def __init__(self, session_id: str, adapter):
            super().__init__()
            self._session_id = session_id
            self._adapter    = adapter

        def run(self):
            try:
                result = self._adapter.run_ai_review(self._session_id)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReportWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str, adapter):
            super().__init__()
            self._mode    = mode
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.generate_report(self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Main Panel
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class ReplayTrainingPanel(QWidget):
        """TW Replay Training Cockpit GUI Panel.

        [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode       = mode
            self._adapter    = None
            self._session_id: str = ""
            self._workers    = []  # keep alive
            self._play_timer = QTimer(self)
            self._play_timer.timeout.connect(self._on_play_tick)
            self._is_playing = False
            self._setup_adapter()
            self._build_ui()

        def _setup_adapter(self):
            try:
                from gui.replay_training_adapter import ReplayTrainingAdapter
                self._adapter = ReplayTrainingAdapter()
            except Exception as exc:
                logger.warning("[ReplayTrainingPanel] adapter init error: %s", exc)

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(4, 4, 4, 4)
            root.setSpacing(4)

            # I. Safety banner (top)
            root.addWidget(self._build_safety_banner())

            # Scroll area for the rest
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            inner  = QWidget()
            inner_layout = QVBoxLayout(inner)
            inner_layout.setSpacing(6)

            # A. Session Control
            inner_layout.addWidget(self._build_controls())

            # B. Replay Control
            inner_layout.addWidget(self._build_replay_control())

            # Session Status bar
            inner_layout.addWidget(self._build_session_status())

            # C. Market View (bar table)
            inner_layout.addWidget(self._build_chart_area())

            # D. Marker buttons
            inner_layout.addWidget(self._build_marker_buttons())

            # E. AI Review panel
            inner_layout.addWidget(self._build_ai_review_panel())

            # F. Score panel
            inner_layout.addWidget(self._build_score_panel())

            # G. Mistake table
            inner_layout.addWidget(self._build_mistake_table())

            # H. Drill table
            inner_layout.addWidget(self._build_drill_table())

            # I. Multi-timeframe Replay Context
            inner_layout.addWidget(self._build_mtf_panel())

            # Journal/Coach panel
            inner_layout.addWidget(self._build_journal_panel())

            # Actions
            inner_layout.addWidget(self._build_actions())

            scroll.setWidget(inner)
            root.addWidget(scroll)

        def _build_safety_banner(self) -> QFrame:
            frame  = QFrame()
            layout = QHBoxLayout(frame)
            frame.setStyleSheet("background-color: #8B0000; border-radius: 4px;")
            self._banner_label = QLabel(
                "  TW Replay Training Cockpit  |  Replay Training Only  |  "
                "Research Only  |  No Real Orders  |  Production Trading BLOCKED  "
                "|  Future Data Hidden: True  "
            )
            font = self._banner_label.font()
            font.setBold(True)
            self._banner_label.setFont(font)
            self._banner_label.setStyleSheet("color: white; padding: 6px;")
            layout.addWidget(self._banner_label)
            return frame

        def _build_controls(self) -> QGroupBox:
            box    = QGroupBox("A. Session Control")
            layout = QHBoxLayout(box)

            # Symbol
            layout.addWidget(QLabel("Symbol:"))
            self._symbol_edit = QLineEdit("2454")
            self._symbol_edit.setMaximumWidth(80)
            layout.addWidget(self._symbol_edit)

            # Date
            layout.addWidget(QLabel("Date:"))
            self._date_edit = QDateEdit(QDate.currentDate())
            self._date_edit.setDisplayFormat("yyyy-MM-dd")
            self._date_edit.setCalendarPopup(True)
            layout.addWidget(self._date_edit)

            # Timeframe
            layout.addWidget(QLabel("Timeframe:"))
            self._timeframe_combo = QComboBox()
            self._timeframe_combo.addItems(["1min", "5min"])
            layout.addWidget(self._timeframe_combo)

            # Hide future data toggle
            self._hide_future_cb = QCheckBox("Hide Future Data")
            self._hide_future_cb.setChecked(True)
            layout.addWidget(self._hide_future_cb)

            layout.addStretch()

            # Load Session button
            self._load_btn = QPushButton("Load Session")
            self._load_btn.clicked.connect(self._on_load_session)
            layout.addWidget(self._load_btn)

            # Reset Session button
            self._reset_btn = QPushButton("Reset Session")
            self._reset_btn.clicked.connect(self._on_reset_session)
            layout.addWidget(self._reset_btn)

            return box

        def _build_replay_control(self) -> QGroupBox:
            box    = QGroupBox("B. Replay Control")
            layout = QVBoxLayout(box)

            top = QHBoxLayout()

            # Prev / Next / Play / Pause
            self._prev_btn = QPushButton("◀ Prev")
            self._prev_btn.clicked.connect(self._on_prev_bar)
            top.addWidget(self._prev_btn)

            self._next_btn = QPushButton("Next ▶")
            self._next_btn.clicked.connect(self._on_next_bar)
            top.addWidget(self._next_btn)

            self._play_btn = QPushButton("▶ Play")
            self._play_btn.clicked.connect(self._on_play_pause)
            top.addWidget(self._play_btn)

            # Speed
            top.addWidget(QLabel("Speed:"))
            self._speed_combo = QComboBox()
            self._speed_combo.addItems(["1x", "2x", "4x", "8x"])
            top.addWidget(self._speed_combo)

            top.addStretch()

            # Jump to bar
            top.addWidget(QLabel("Jump to bar:"))
            self._jump_spin = QSpinBox()
            self._jump_spin.setMinimum(0)
            self._jump_spin.setMaximum(9999)
            self._jump_spin.setMaximumWidth(70)
            top.addWidget(self._jump_spin)

            jump_btn = QPushButton("Go")
            jump_btn.setMaximumWidth(40)
            jump_btn.clicked.connect(self._on_jump_to_bar)
            top.addWidget(jump_btn)

            layout.addLayout(top)

            # Progress slider
            slider_row = QHBoxLayout()
            slider_row.addWidget(QLabel("Progress:"))
            self._progress_slider = QSlider(Qt.Horizontal)
            self._progress_slider.setMinimum(0)
            self._progress_slider.setMaximum(100)
            self._progress_slider.setValue(0)
            self._progress_slider.sliderReleased.connect(self._on_progress_slider_released)
            slider_row.addWidget(self._progress_slider)
            layout.addLayout(slider_row)

            return box

        def _build_session_status(self) -> QFrame:
            frame  = QFrame()
            layout = QHBoxLayout(frame)
            frame.setStyleSheet("background-color: #1a1a2e; border-radius: 3px;")
            self._status_label = QLabel(
                "Current Bar: — / —  |  Bar Time: —  |  Session Status: —"
            )
            self._status_label.setStyleSheet("color: #90caf9; padding: 4px; font-family: monospace;")
            layout.addWidget(self._status_label)
            layout.addStretch()
            return frame

        def _build_chart_area(self) -> QGroupBox:
            box    = QGroupBox("C. Market View — Visible Bars Only / Future Data Hidden")
            layout = QVBoxLayout(box)

            # Info row: current price, OR high/low, volume, marker count
            info_row = QHBoxLayout()
            self._cur_price_label  = QLabel("Price: —")
            self._or_high_label    = QLabel("OR High: —")
            self._or_low_label     = QLabel("OR Low: —")
            self._volume_label     = QLabel("Volume: —")
            self._marker_cnt_label = QLabel("Markers: 0")
            self._future_hidden_label = QLabel("Future Hidden: True")
            self._future_hidden_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            for lbl in (self._cur_price_label, self._or_high_label, self._or_low_label,
                        self._volume_label, self._marker_cnt_label):
                lbl.setStyleSheet("color: #4fc3f7; padding: 2px 6px;")
                info_row.addWidget(lbl)
            info_row.addWidget(self._future_hidden_label)
            info_row.addStretch()
            layout.addLayout(info_row)

            self._bar_table = QTableWidget(0, 9)
            self._bar_table.setHorizontalHeaderLabels(
                ["Time", "Open", "High", "Low", "Close", "Volume", "VWAP", "OR High", "OR Low"]
            )
            self._bar_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._bar_table.setMaximumHeight(200)
            layout.addWidget(self._bar_table)

            self._no_data_label = QLabel(
                "Empty State — No intraday data loaded. Load a session to begin replay practice."
            )
            self._no_data_label.setAlignment(Qt.AlignCenter)
            self._no_data_label.setStyleSheet("color: gray; font-style: italic; padding: 8px;")
            layout.addWidget(self._no_data_label)

            return box

        def _build_marker_buttons(self) -> QGroupBox:
            box    = QGroupBox("D. Marker / Annotate — Research Only / No Real Orders")
            layout = QVBoxLayout(box)

            btn_row = QHBoxLayout()
            marker_types = [
                ("Entry",       "ENTRY"),
                ("Exit",        "EXIT"),
                ("Stop Loss",   "STOP_LOSS"),
                ("Take Profit", "TAKE_PROFIT"),
                ("Fake BO",     "FAKE_BREAKOUT"),
                ("VWAP Loss",   "VWAP_LOSS"),
                ("OR Fail",     "OPENING_RANGE_FAIL"),
            ]
            for label, mtype in marker_types:
                btn = QPushButton(label)
                btn.setMaximumWidth(90)
                btn.clicked.connect(lambda checked=False, t=mtype: self._on_add_marker(t))
                btn_row.addWidget(btn)

            note_btn = QPushButton("Add Note")
            note_btn.clicked.connect(self._on_add_note)
            btn_row.addWidget(note_btn)

            btn_row.addStretch()
            layout.addLayout(btn_row)

            # Reason input and Tags input
            input_row = QHBoxLayout()
            input_row.addWidget(QLabel("Reason:"))
            self._marker_reason_edit = QLineEdit()
            self._marker_reason_edit.setPlaceholderText("Marker reason / note...")
            self._marker_reason_edit.setMaximumWidth(300)
            input_row.addWidget(self._marker_reason_edit)
            input_row.addWidget(QLabel("Tags:"))
            self._marker_tags_edit = QLineEdit()
            self._marker_tags_edit.setPlaceholderText("tag1,tag2,...")
            self._marker_tags_edit.setMaximumWidth(200)
            input_row.addWidget(self._marker_tags_edit)
            input_row.addStretch()
            layout.addLayout(input_row)

            return box

        def _build_ai_review_panel(self) -> QGroupBox:
            box    = QGroupBox("E. AI Replay Review — Rule-Based Only / No External API")
            layout = QVBoxLayout(box)

            top = QHBoxLayout()
            self._run_review_btn = QPushButton("Run AI Review")
            self._run_review_btn.clicked.connect(self._on_run_review)
            top.addWidget(self._run_review_btn)

            self._score_label    = QLabel("Score: —")
            self._mistakes_label = QLabel("Mistakes: —")
            self._violations_label = QLabel("Violations: —")
            font = QFont()
            font.setBold(True)
            self._score_label.setFont(font)
            top.addWidget(self._score_label)
            top.addWidget(self._mistakes_label)
            top.addWidget(self._violations_label)
            top.addStretch()
            layout.addLayout(top)

            self._feedback_text = QTextEdit()
            self._feedback_text.setReadOnly(True)
            self._feedback_text.setMaximumHeight(80)
            self._feedback_text.setPlaceholderText(
                "AI review feedback will appear here... [Replay Training Only / No Real Orders]"
            )
            layout.addWidget(self._feedback_text)

            # Next drills summary
            drills_row = QHBoxLayout()
            drills_row.addWidget(QLabel("Next Drills:"))
            self._next_drills_label = QLabel("—")
            self._next_drills_label.setWordWrap(True)
            self._next_drills_label.setStyleSheet("color: #a5d6a7; font-style: italic;")
            drills_row.addWidget(self._next_drills_label)
            drills_row.addStretch()
            layout.addLayout(drills_row)

            return box

        def _build_score_panel(self) -> QGroupBox:
            box    = QGroupBox("F. Score Breakdown")
            layout = QHBoxLayout(box)

            self._score_labels = {}
            components = [
                ("entry_quality",           "Entry Q"),
                ("exit_stop_discipline",    "Exit/Stop"),
                ("fake_breakout_avoidance", "Fake BO"),
                ("vwap_opening_range",      "VWAP/OR"),
                ("strategy_adherence",      "Strategy"),
                ("notes_completeness",      "Notes"),
            ]
            for k, label in components:
                lbl = QLabel(f"{label}: —")
                self._score_labels[k] = lbl
                layout.addWidget(lbl)

            layout.addStretch()
            return box

        def _build_mistake_table(self) -> QGroupBox:
            box    = QGroupBox("G. Detected Mistakes")
            layout = QVBoxLayout(box)

            self._mistake_table = QTableWidget(0, 6)
            self._mistake_table.setHorizontalHeaderLabels(
                ["Mistake Type", "Severity", "Bar Time", "Price", "Suggested Fix", "Related Marker"]
            )
            self._mistake_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._mistake_table.setMaximumHeight(150)

            self._mistake_empty_label = QLabel("No mistakes detected — empty state.")
            self._mistake_empty_label.setAlignment(Qt.AlignCenter)
            self._mistake_empty_label.setStyleSheet("color: gray; font-style: italic;")
            self._mistake_empty_label.setVisible(True)

            layout.addWidget(self._mistake_table)
            layout.addWidget(self._mistake_empty_label)
            return box

        def _build_drill_table(self) -> QGroupBox:
            box    = QGroupBox("H. Drill Suggestions")
            layout = QVBoxLayout(box)

            self._drill_table = QTableWidget(0, 5)
            self._drill_table.setHorizontalHeaderLabels(
                ["Drill", "Priority", "Reason", "Focus Points", "Expected Skill"]
            )
            self._drill_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._drill_table.setMaximumHeight(150)

            self._drill_empty_label = QLabel("No drills yet — run AI Review first.")
            self._drill_empty_label.setAlignment(Qt.AlignCenter)
            self._drill_empty_label.setStyleSheet("color: gray; font-style: italic;")
            self._drill_empty_label.setVisible(True)

            layout.addWidget(self._drill_table)
            layout.addWidget(self._drill_empty_label)
            return box

        def _build_mtf_panel(self) -> QGroupBox:
            box    = QGroupBox("I. Multi-Timeframe Replay Context — Research Only / No Auto-Trade")
            layout = QVBoxLayout(box)

            row1 = QHBoxLayout()
            row1.addWidget(QLabel("Replay Timestamp:"))
            self._mtf_timestamp_label = QLabel("—")
            self._mtf_timestamp_label.setStyleSheet("color: #4fc3f7; font-family: monospace;")
            row1.addWidget(self._mtf_timestamp_label)
            row1.addSpacing(16)
            row1.addWidget(QLabel("Primary TF:"))
            self._mtf_primary_tf_label = QLabel("—")
            self._mtf_primary_tf_label.setStyleSheet("color: #a5d6a7;")
            row1.addWidget(self._mtf_primary_tf_label)
            row1.addSpacing(16)
            row1.addWidget(QLabel("Trigger TF:"))
            self._mtf_trigger_tf_label = QLabel("—")
            self._mtf_trigger_tf_label.setStyleSheet("color: #a5d6a7;")
            row1.addWidget(self._mtf_trigger_tf_label)
            row1.addStretch()
            layout.addLayout(row1)

            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Available TFs:"))
            self._mtf_available_tfs_label = QLabel("—")
            self._mtf_available_tfs_label.setStyleSheet("color: #fff176;")
            row2.addWidget(self._mtf_available_tfs_label)
            row2.addSpacing(16)
            row2.addWidget(QLabel("Agreement:"))
            self._mtf_agreement_label = QLabel("—")
            self._mtf_agreement_label.setStyleSheet("color: #80cbc4;")
            row2.addWidget(self._mtf_agreement_label)
            row2.addSpacing(16)
            row2.addWidget(QLabel("Conflicts:"))
            self._mtf_conflicts_label = QLabel("—")
            self._mtf_conflicts_label.setStyleSheet("color: #ef9a9a;")
            row2.addWidget(self._mtf_conflicts_label)
            row2.addStretch()
            layout.addLayout(row2)

            row3 = QHBoxLayout()
            self._mtf_partial_bar_warning = QLabel("")
            self._mtf_partial_bar_warning.setStyleSheet("color: #ff8a65; font-weight: bold;")
            row3.addWidget(self._mtf_partial_bar_warning)
            row3.addStretch()
            self._open_mtf_btn = QPushButton("Open Multi-timeframe Replay")
            self._open_mtf_btn.clicked.connect(self._on_open_mtf_replay)
            row3.addWidget(self._open_mtf_btn)
            layout.addLayout(row3)

            return box

        def _build_journal_panel(self) -> QGroupBox:
            box    = QGroupBox("Journal / Coach Integration — Research Only / No Real Trade Entries")
            layout = QHBoxLayout(box)

            export_btn = QPushButton("Export to Journal")
            export_btn.clicked.connect(self._on_export_journal)
            layout.addWidget(export_btn)

            self._journal_status_label = QLabel("Journal: —")
            layout.addWidget(self._journal_status_label)
            layout.addStretch()
            return box

        def _build_actions(self) -> QGroupBox:
            box    = QGroupBox("Actions")
            layout = QHBoxLayout(box)

            gen_btn = QPushButton("Generate Report")
            gen_btn.clicked.connect(self._on_generate_report)
            layout.addWidget(gen_btn)

            open_btn = QPushButton("Open Latest Report")
            open_btn.clicked.connect(self._on_open_latest_report)
            layout.addWidget(open_btn)

            refresh_btn = QPushButton("Refresh")
            refresh_btn.clicked.connect(self._on_refresh)
            layout.addWidget(refresh_btn)

            layout.addStretch()
            return box

        # ------------------------------------------------------------------
        # Event handlers
        # ------------------------------------------------------------------

        def _on_load_session(self):
            symbol     = self._symbol_edit.text().strip() or "2454"
            trade_date = self._date_edit.date().toString("yyyy-MM-dd")
            timeframe  = self._timeframe_combo.currentText()
            if self._adapter is None:
                QMessageBox.warning(self, "Error", "Adapter not available.")
                return
            self._load_btn.setEnabled(False)
            self._load_btn.setText("Loading...")
            worker = _SessionWorker(symbol, trade_date, timeframe, self._mode, self._adapter)
            worker.finished.connect(self._on_session_loaded)
            self._workers.append(worker)
            worker.start()

        def _on_session_loaded(self, result: dict):
            self._load_btn.setEnabled(True)
            self._load_btn.setText("Load Session")
            if result.get("ok"):
                session = result.get("session", {})
                self._session_id = session.get("session_id", "")
                total = session.get("total_bars", 0)
                self._jump_spin.setMaximum(max(total - 1, 0))
                self._progress_slider.setMaximum(max(total - 1, 1))
                self._feedback_text.setPlainText(
                    f"Session loaded: {session.get('session_id', '')} | "
                    f"Bars: {total} | "
                    f"Status: {session.get('status', '')}\n"
                    f"[Replay Training Only / No Real Orders]"
                )
                self._update_bar_table()
                self._update_status_bar()
            else:
                self._feedback_text.setPlainText(f"Load failed: {result.get('error', 'Unknown')}")

        def _on_next_bar(self):
            if not self._session_id or self._adapter is None:
                return
            result = self._adapter.next_bar(self._session_id)
            if result.get("ok"):
                self._update_bar_table()
                self._update_status_bar()

        def _on_prev_bar(self):
            if not self._session_id or self._adapter is None:
                return
            result = self._adapter.prev_bar(self._session_id)
            if result.get("ok"):
                self._update_bar_table()
                self._update_status_bar()

        def _on_reset_session(self):
            if self._is_playing:
                self._play_timer.stop()
                self._is_playing = False
                self._play_btn.setText("▶ Play")
            self._session_id = ""
            self._bar_table.setRowCount(0)
            self._no_data_label.setVisible(True)
            self._status_label.setText("Current Bar: — / —  |  Bar Time: —  |  Session Status: —")
            self._feedback_text.setPlainText("Session reset. Load a new session to begin.")
            self._score_label.setText("Score: —")
            self._mistakes_label.setText("Mistakes: —")
            self._violations_label.setText("Violations: —")
            self._mistake_table.setRowCount(0)
            self._mistake_empty_label.setVisible(True)
            self._drill_table.setRowCount(0)
            self._drill_empty_label.setVisible(True)
            self._progress_slider.setValue(0)

        def _on_play_pause(self):
            if not self._session_id:
                return
            if self._is_playing:
                self._play_timer.stop()
                self._is_playing = False
                self._play_btn.setText("▶ Play")
            else:
                speed_text = self._speed_combo.currentText()
                speeds = {"1x": 1000, "2x": 500, "4x": 250, "8x": 125}
                interval = speeds.get(speed_text, 1000)
                self._play_timer.start(interval)
                self._is_playing = True
                self._play_btn.setText("⏸ Pause")

        def _on_play_tick(self):
            if not self._session_id or self._adapter is None:
                self._play_timer.stop()
                self._is_playing = False
                self._play_btn.setText("▶ Play")
                return
            result = self._adapter.next_bar(self._session_id)
            if result.get("ok"):
                self._update_bar_table()
                self._update_status_bar()
            else:
                # End of bars or error — stop playback
                self._play_timer.stop()
                self._is_playing = False
                self._play_btn.setText("▶ Play")

        def _on_jump_to_bar(self):
            if not self._session_id or self._adapter is None:
                return
            bar_index = self._jump_spin.value()
            result = self._adapter.jump_to_bar(self._session_id, bar_index)
            if result.get("ok"):
                self._update_bar_table()
                self._update_status_bar()

        def _on_progress_slider_released(self):
            if not self._session_id or self._adapter is None:
                return
            bar_index = self._progress_slider.value()
            result = self._adapter.jump_to_bar(self._session_id, bar_index)
            if result.get("ok"):
                self._update_bar_table()
                self._update_status_bar()

        def _update_bar_table(self):
            if self._adapter is None or not self._session_id:
                return
            try:
                engine = self._adapter._get_engine()
                if engine is None:
                    return
                bars = engine.get_visible_bars_table(self._session_id, limit=100)
                self._bar_table.setRowCount(len(bars))
                self._no_data_label.setVisible(len(bars) == 0)
                for row_idx, bar in enumerate(bars):
                    time_val = str(bar.get("datetime", bar.get("time", bar.get("date", row_idx))))
                    self._bar_table.setItem(row_idx, 0, QTableWidgetItem(time_val))

                    def _fmt(v):
                        try:
                            return f"{float(v):.2f}"
                        except (TypeError, ValueError):
                            return str(v)

                    for col, key in enumerate(["open", "high", "low", "close", "volume"], 1):
                        self._bar_table.setItem(row_idx, col, QTableWidgetItem(_fmt(bar.get(key, bar.get(key.upper(), "")))))
                    self._bar_table.setItem(row_idx, 6, QTableWidgetItem(_fmt(bar.get("vwap_computed", bar.get("vwap", "")))))
                    self._bar_table.setItem(row_idx, 7, QTableWidgetItem(_fmt(bar.get("or_high", ""))))
                    self._bar_table.setItem(row_idx, 8, QTableWidgetItem(_fmt(bar.get("or_low",  ""))))

                if bars:
                    self._bar_table.scrollToBottom()
                    last = bars[-1]
                    cur_price = last.get("close", last.get("CLOSE", "—"))
                    or_h = last.get("or_high", "—")
                    or_l = last.get("or_low",  "—")
                    vol  = last.get("volume", last.get("VOLUME", "—"))
                    try: self._cur_price_label.setText(f"Price: {float(cur_price):.2f}")
                    except: self._cur_price_label.setText(f"Price: {cur_price}")
                    try: self._or_high_label.setText(f"OR High: {float(or_h):.2f}")
                    except: self._or_high_label.setText(f"OR High: {or_h}")
                    try: self._or_low_label.setText(f"OR Low: {float(or_l):.2f}")
                    except: self._or_low_label.setText(f"OR Low: {or_l}")
                    try: self._volume_label.setText(f"Volume: {int(float(vol)):,}")
                    except: self._volume_label.setText(f"Volume: {vol}")

                # Update marker count
                marker_count = len(self._adapter._current_markers) if self._adapter else 0
                self._marker_cnt_label.setText(f"Markers: {marker_count}")

                # Update future hidden indicator
                hidden = engine.is_future_hidden(self._session_id)
                self._future_hidden_label.setText(f"Future Hidden: {'True' if hidden else 'False'}")
                self._banner_label.setText(
                    "  TW Replay Training Cockpit  |  Replay Training Only  |  "
                    "Research Only  |  No Real Orders  |  Production Trading BLOCKED  "
                    f"|  Future Data Hidden: {'True' if hidden else 'False'}  "
                )

            except Exception as exc:
                logger.warning("[ReplayTrainingPanel] update_bar_table error: %s", exc)

        def _update_status_bar(self):
            if self._adapter is None or not self._session_id:
                return
            try:
                engine = self._adapter._get_engine()
                if engine is None:
                    return
                progress = engine.get_progress(self._session_id)
                cur = progress.get("current_bar", 0)
                total = progress.get("total_bars", 0)
                current_bar = engine.get_current_bar(self._session_id)
                bar_time = str(current_bar.get(
                    "datetime", current_bar.get("time", current_bar.get("date", "—"))
                ))
                session_state = self._adapter._sessions_meta() if hasattr(self._adapter, "_sessions_meta") else {}
                status_text = f"Current Bar: {cur} / {total}  |  Bar Time: {bar_time}  |  Session: {self._session_id[:24]}"
                self._status_label.setText(status_text)

                # Sync progress slider without triggering the signal
                self._progress_slider.blockSignals(True)
                self._progress_slider.setValue(cur)
                self._progress_slider.blockSignals(False)
                self._jump_spin.blockSignals(True)
                self._jump_spin.setValue(cur)
                self._jump_spin.blockSignals(False)
            except Exception as exc:
                logger.warning("[ReplayTrainingPanel] update_status_bar error: %s", exc)

        def _on_add_marker(self, marker_type: str):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            note = self._marker_reason_edit.text().strip()
            result = self._adapter.add_marker(self._session_id, marker_type, note=note)
            if result.get("ok"):
                m = result.get("marker", {})
                self._feedback_text.setPlainText(
                    f"Marker added: {marker_type} at bar {m.get('bar_index', '?')} "
                    f"[Research Only / No Real Orders]"
                )
                self._marker_cnt_label.setText(f"Markers: {len(self._adapter._current_markers)}")
            else:
                self._feedback_text.setPlainText(f"Marker error: {result.get('error', '')}")

        def _on_add_note(self):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            # Use reason input if filled, else prompt
            note = self._marker_reason_edit.text().strip()
            if not note:
                note, ok = QInputDialog.getText(self, "Add Note", "Note text:")
                if not (ok and note):
                    return
            tags = self._marker_tags_edit.text().strip()
            result = self._adapter.add_note(self._session_id, note=note, tags=tags)
            if result.get("ok"):
                self._feedback_text.setPlainText(f"Note added: {note[:60]} [Research Only]")
                self._marker_reason_edit.clear()
            else:
                self._feedback_text.setPlainText(f"Note error: {result.get('error', '')}")

        def _on_run_review(self):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            self._run_review_btn.setEnabled(False)
            self._run_review_btn.setText("Reviewing...")
            worker = _ReviewWorker(self._session_id, self._adapter)
            worker.finished.connect(self._on_review_done)
            self._workers.append(worker)
            worker.start()

        def _on_review_done(self, result: dict):
            self._run_review_btn.setEnabled(True)
            self._run_review_btn.setText("Run AI Review")
            if not result.get("ok"):
                self._feedback_text.setPlainText(f"Review failed: {result.get('error', '')}")
                return

            review   = result.get("review", {})
            mistakes = result.get("mistakes", [])
            score    = result.get("score", {})
            drills   = result.get("drills", [])

            # Update score label
            total_score = score.get("total_score", 0.0)
            grade       = score.get("grade", "N/A")
            self._score_label.setText(f"Score: {total_score:.1f}/100 ({grade})")
            self._mistakes_label.setText(f"Mistakes: {len(mistakes)}")

            # Strategy violations
            violations = review.get("strategy_violations", [])
            self._violations_label.setText(f"Violations: {len(violations)}")

            # Update feedback
            feedback = review.get("tape_reading_feedback", review.get("summary", ""))
            self._feedback_text.setPlainText(
                f"AI Review Complete [Replay Training Only / No Real Orders]\n"
                f"{feedback}\n"
                f"Next Focus: {review.get('next_training_focus', 'N/A')}"
            )

            # Next drills summary
            if drills:
                drill_names = [d.get("drill_name", d.get("name", "")) for d in drills[:3]]
                self._next_drills_label.setText("  |  ".join(drill_names) + ("..." if len(drills) > 3 else ""))
            else:
                self._next_drills_label.setText("No drills suggested")

            # Update score breakdown
            breakdown = score.get("breakdown", {})
            for k, lbl in self._score_labels.items():
                v = breakdown.get(k, "—")
                lbl.setText(f"{lbl.text().split(':')[0]}: {v}")

            # Update mistake table
            self._mistake_table.setRowCount(len(mistakes))
            self._mistake_empty_label.setVisible(len(mistakes) == 0)
            for row_idx, m in enumerate(mistakes):
                self._mistake_table.setItem(row_idx, 0, QTableWidgetItem(m.get("mistake_type", "")))
                self._mistake_table.setItem(row_idx, 1, QTableWidgetItem(m.get("severity", "")))
                self._mistake_table.setItem(row_idx, 2, QTableWidgetItem(m.get("bar_time", "")))
                self._mistake_table.setItem(row_idx, 3, QTableWidgetItem(str(m.get("price", ""))))
                self._mistake_table.setItem(row_idx, 4, QTableWidgetItem(m.get("suggested_fix", "")))
                self._mistake_table.setItem(row_idx, 5, QTableWidgetItem(m.get("related_marker_id", "")))

            # Update drill table
            self._drill_table.setRowCount(len(drills))
            self._drill_empty_label.setVisible(len(drills) == 0)
            for row_idx, d in enumerate(drills):
                self._drill_table.setItem(row_idx, 0, QTableWidgetItem(d.get("drill_name", d.get("name", ""))))
                self._drill_table.setItem(row_idx, 1, QTableWidgetItem(d.get("priority", "")))
                self._drill_table.setItem(row_idx, 2, QTableWidgetItem(d.get("reason", "")))
                focus = d.get("focus_points", d.get("focus", ""))
                if isinstance(focus, list):
                    focus = ", ".join(str(f) for f in focus)
                self._drill_table.setItem(row_idx, 3, QTableWidgetItem(str(focus)))
                self._drill_table.setItem(row_idx, 4, QTableWidgetItem(d.get("expected_skill", d.get("skill", ""))))

        def _on_generate_report(self):
            if self._adapter is None:
                QMessageBox.information(self, "Error", "Adapter not available.")
                return
            worker = _ReportWorker(self._mode, self._adapter)
            worker.finished.connect(self._on_report_done)
            self._workers.append(worker)
            worker.start()

        def _on_report_done(self, result: dict):
            if result.get("ok"):
                path = result.get("report_path", "")
                QMessageBox.information(
                    self, "Report Generated",
                    f"Report saved:\n{path}\n\n[Replay Training Only / No Real Orders]"
                )
            else:
                QMessageBox.warning(self, "Report Error", result.get("error", "Unknown"))

        def _on_open_latest_report(self):
            if self._adapter is None:
                return
            path = self._adapter.load_latest_report_path()
            if path and os.path.isfile(path):
                try:
                    import subprocess, sys
                    if sys.platform.startswith("win"):
                        os.startfile(path)
                    elif sys.platform == "darwin":
                        subprocess.Popen(["open", path])
                    else:
                        subprocess.Popen(["xdg-open", path])
                except Exception as exc:
                    QMessageBox.information(self, "Report Path", path)
            else:
                QMessageBox.information(self, "No Report", "No replay training report found yet.")

        def _on_export_journal(self):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            result = self._adapter.export_to_journal(self._session_id)
            status = result.get("status", "unknown")
            self._journal_status_label.setText(f"Journal: {status}")

        def _on_open_mtf_replay(self):
            try:
                from gui.replay_multi_timeframe_panel import ReplayMultiTimeframePanel
                symbol = self._symbol_edit.text().strip() or "2454"
                trade_date = self._date_edit.date().toString("yyyy-MM-dd")
                panel = ReplayMultiTimeframePanel(symbol=symbol, trade_date=trade_date, parent=None)
                panel.show()
            except Exception as exc:
                if _PYSIDE6_OK:
                    from PySide6.QtWidgets import QMessageBox
                    QMessageBox.information(
                        self, "Multi-timeframe Replay",
                        f"[Research Only] MTF panel: {exc}"
                    )

        def update_mtf_context(self, context: dict) -> None:
            """Update MTF display fields from a MultiTimeframeReplaySession context dict."""
            self._mtf_timestamp_label.setText(str(context.get("replay_timestamp", "—")))
            self._mtf_primary_tf_label.setText(str(context.get("primary_timeframe", "—")))
            self._mtf_trigger_tf_label.setText(str(context.get("trigger_timeframe", "—")))
            available = context.get("available_timeframes", [])
            self._mtf_available_tfs_label.setText(", ".join(available) if available else "—")
            agreement = context.get("agreement", {})
            self._mtf_agreement_label.setText(str(agreement.get("status", "—")))
            conflicts = context.get("conflicts", [])
            self._mtf_conflicts_label.setText(str(len(conflicts)) if isinstance(conflicts, list) else "—")
            partial_warns = context.get("partial_bar_warnings", [])
            if partial_warns:
                self._mtf_partial_bar_warning.setText(
                    "[!] Partial Bar: " + "; ".join(str(w) for w in partial_warns[:2])
                )
            else:
                self._mtf_partial_bar_warning.setText("")

        def _on_refresh(self):
            self._update_bar_table()
            self._update_status_bar()
            summary = self._adapter.load_latest_summary() if self._adapter else {}
            if summary.get("ok"):
                s = summary.get("summary", {})
                self._feedback_text.setPlainText(
                    f"Summary loaded | Score: {s.get('latest_score', 'N/A')} | "
                    f"Mistakes: {s.get('mistakes_count', 'N/A')} | "
                    f"[Replay Training Only / No Real Orders]"
                )

        def closeEvent(self, event):
            """Stop play timer and wait for workers on close to avoid QThread destroyed warning."""
            if self._is_playing:
                self._play_timer.stop()
                self._is_playing = False
            for w in self._workers:
                try:
                    if w.isRunning():
                        w.quit()
                        w.wait(500)
                except Exception:
                    pass
            super().closeEvent(event)

else:
    # Stub when PySide6 not available
    class ReplayTrainingPanel:  # type: ignore
        """Stub ReplayTrainingPanel — PySide6 not available."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *args, **kwargs):
            logger.warning("[ReplayTrainingPanel] PySide6 not available — stub mode")
