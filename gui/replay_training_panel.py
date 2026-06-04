"""gui/replay_training_panel.py — ReplayTrainingPanel for TW Replay Training Cockpit v0.5.6.

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
        QInputDialog, QCheckBox, QDateEdit, QTextEdit,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QDate
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

            # A. Safety banner
            root.addWidget(self._build_safety_banner())

            # Scroll area for the rest
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            inner  = QWidget()
            inner_layout = QVBoxLayout(inner)
            inner_layout.setSpacing(6)

            # B. Controls
            inner_layout.addWidget(self._build_controls())

            # C. Chart area (bar table)
            inner_layout.addWidget(self._build_chart_area())

            # D. Marker buttons
            inner_layout.addWidget(self._build_marker_buttons())

            # E. AI Review panel
            inner_layout.addWidget(self._build_ai_review_panel())

            # F. Score panel
            inner_layout.addWidget(self._build_score_panel())

            # G. Mistake table
            inner_layout.addWidget(self._build_mistake_table())

            # H. Journal/Coach panel
            inner_layout.addWidget(self._build_journal_panel())

            # I. Actions
            inner_layout.addWidget(self._build_actions())

            scroll.setWidget(inner)
            root.addWidget(scroll)

        def _build_safety_banner(self) -> QFrame:
            frame  = QFrame()
            layout = QHBoxLayout(frame)
            frame.setStyleSheet("background-color: #8B0000; border-radius: 4px;")
            label  = QLabel(
                "  TW Replay Training Cockpit  |  Replay Training Only  |  "
                "Research Only  |  No Real Orders  |  Production Trading BLOCKED  "
            )
            font = label.font()
            font.setBold(True)
            label.setFont(font)
            label.setStyleSheet("color: white; padding: 6px;")
            layout.addWidget(label)
            return frame

        def _build_controls(self) -> QGroupBox:
            box    = QGroupBox("Controls")
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

            # Prev / Play / Pause / Next
            self._prev_btn = QPushButton("Prev")
            self._prev_btn.clicked.connect(self._on_prev_bar)
            layout.addWidget(self._prev_btn)

            self._next_btn = QPushButton("Next")
            self._next_btn.clicked.connect(self._on_next_bar)
            layout.addWidget(self._next_btn)

            # Speed
            layout.addWidget(QLabel("Speed:"))
            self._speed_combo = QComboBox()
            self._speed_combo.addItems(["1x", "2x", "4x", "8x"])
            layout.addWidget(self._speed_combo)

            return box

        def _build_chart_area(self) -> QGroupBox:
            box    = QGroupBox("Chart — Visible Bars (Replay Training Only / No Future Data)")
            layout = QVBoxLayout(box)

            self._bar_table = QTableWidget(0, 7)
            self._bar_table.setHorizontalHeaderLabels(
                ["Time", "Open", "High", "Low", "Close", "Volume", "VWAP"]
            )
            self._bar_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._bar_table.setMaximumHeight(200)
            layout.addWidget(self._bar_table)

            self._no_data_label = QLabel("No data / Empty State — Load a session to begin.")
            self._no_data_label.setAlignment(Qt.AlignCenter)
            self._no_data_label.setStyleSheet("color: gray; font-style: italic;")
            layout.addWidget(self._no_data_label)

            return box

        def _build_marker_buttons(self) -> QGroupBox:
            box    = QGroupBox("Mark / Annotate — Research Only / No Real Orders")
            layout = QHBoxLayout(box)

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
                layout.addWidget(btn)

            note_btn = QPushButton("Add Note")
            note_btn.clicked.connect(self._on_add_note)
            layout.addWidget(note_btn)

            layout.addStretch()
            return box

        def _build_ai_review_panel(self) -> QGroupBox:
            box    = QGroupBox("AI Replay Review — Rule-Based Only / No External API")
            layout = QVBoxLayout(box)

            top = QHBoxLayout()
            self._run_review_btn = QPushButton("Run AI Review")
            self._run_review_btn.clicked.connect(self._on_run_review)
            top.addWidget(self._run_review_btn)

            self._score_label    = QLabel("Score: —")
            self._mistakes_label = QLabel("Mistakes: —")
            font = QFont()
            font.setBold(True)
            self._score_label.setFont(font)
            top.addWidget(self._score_label)
            top.addWidget(self._mistakes_label)
            top.addStretch()
            layout.addLayout(top)

            self._feedback_text = QTextEdit()
            self._feedback_text.setReadOnly(True)
            self._feedback_text.setMaximumHeight(80)
            self._feedback_text.setPlaceholderText("AI review feedback will appear here...")
            layout.addWidget(self._feedback_text)

            return box

        def _build_score_panel(self) -> QGroupBox:
            box    = QGroupBox("Score Breakdown")
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
            box    = QGroupBox("Detected Mistakes")
            layout = QVBoxLayout(box)

            self._mistake_table = QTableWidget(0, 4)
            self._mistake_table.setHorizontalHeaderLabels(
                ["Mistake", "Severity", "Bar Time", "Suggested Fix"]
            )
            self._mistake_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._mistake_table.setMaximumHeight(150)
            layout.addWidget(self._mistake_table)

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
                self._feedback_text.setPlainText(
                    f"Session loaded: {session.get('session_id', '')} | "
                    f"Bars: {session.get('total_bars', 0)} | "
                    f"Status: {session.get('status', '')}\n"
                    f"[Replay Training Only / No Real Orders]"
                )
                self._update_bar_table()
            else:
                self._feedback_text.setPlainText(f"Load failed: {result.get('error', 'Unknown')}")

        def _on_next_bar(self):
            if not self._session_id or self._adapter is None:
                return
            result = self._adapter.next_bar(self._session_id)
            if result.get("ok"):
                self._update_bar_table()

        def _on_prev_bar(self):
            if not self._session_id or self._adapter is None:
                return
            result = self._adapter.prev_bar(self._session_id)
            if result.get("ok"):
                self._update_bar_table()

        def _update_bar_table(self):
            if self._adapter is None or not self._session_id:
                return
            try:
                engine = self._adapter._get_engine()
                if engine is None:
                    return
                bars = engine.get_visible_bars(self._session_id)
                self._bar_table.setRowCount(len(bars))
                self._no_data_label.setVisible(len(bars) == 0)
                for row_idx, bar in enumerate(bars):
                    time_val = str(bar.get("datetime", bar.get("time", bar.get("date", row_idx))))
                    self._bar_table.setItem(row_idx, 0, QTableWidgetItem(time_val))
                    for col, key in enumerate(["open", "high", "low", "close", "volume", "vwap"], 1):
                        val = bar.get(key, bar.get(key.upper(), ""))
                        try:
                            val = f"{float(val):.2f}"
                        except (TypeError, ValueError):
                            val = str(val)
                        self._bar_table.setItem(row_idx, col, QTableWidgetItem(val))
                if bars:
                    self._bar_table.scrollToBottom()
            except Exception as exc:
                logger.warning("[ReplayTrainingPanel] update_bar_table error: %s", exc)

        def _on_add_marker(self, marker_type: str):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            result = self._adapter.add_marker(self._session_id, marker_type)
            if result.get("ok"):
                m = result.get("marker", {})
                self._feedback_text.setPlainText(
                    f"Marker added: {marker_type} at bar {m.get('bar_index', '?')} "
                    f"[Research Only / No Real Orders]"
                )
            else:
                self._feedback_text.setPlainText(f"Marker error: {result.get('error', '')}")

        def _on_add_note(self):
            if not self._session_id or self._adapter is None:
                QMessageBox.information(self, "No Session", "Load a session first.")
                return
            note, ok = QInputDialog.getText(self, "Add Note", "Note text:")
            if ok and note:
                ms = self._adapter._get_marker_store()
                if ms:
                    ms.add_note(self._session_id, bar_time="", note=note)
                self._feedback_text.setPlainText(f"Note added: {note[:60]}... [Research Only]")

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

            # Update feedback
            feedback = review.get("tape_reading_feedback", review.get("summary", ""))
            self._feedback_text.setPlainText(
                f"AI Review Complete [Replay Training Only / No Real Orders]\n"
                f"{feedback}\n"
                f"Next Focus: {review.get('next_training_focus', 'N/A')}"
            )

            # Update score breakdown
            breakdown = score.get("breakdown", {})
            for k, lbl in self._score_labels.items():
                v = breakdown.get(k, "—")
                lbl.setText(f"{lbl.text().split(':')[0]}: {v}")

            # Update mistake table
            self._mistake_table.setRowCount(len(mistakes))
            for row_idx, m in enumerate(mistakes):
                self._mistake_table.setItem(row_idx, 0, QTableWidgetItem(m.get("mistake_type", "")))
                self._mistake_table.setItem(row_idx, 1, QTableWidgetItem(m.get("severity", "")))
                self._mistake_table.setItem(row_idx, 2, QTableWidgetItem(m.get("bar_time", "")))
                self._mistake_table.setItem(row_idx, 3, QTableWidgetItem(m.get("suggested_fix", "")))

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

        def _on_refresh(self):
            self._update_bar_table()
            summary = self._adapter.load_latest_summary() if self._adapter else {}
            if summary.get("ok"):
                s = summary.get("summary", {})
                self._feedback_text.setPlainText(
                    f"Summary loaded | Score: {s.get('latest_score', 'N/A')} | "
                    f"Mistakes: {s.get('mistakes_count', 'N/A')} | "
                    f"[Replay Training Only / No Real Orders]"
                )

else:
    # Stub when PySide6 not available
    class ReplayTrainingPanel:  # type: ignore
        """Stub ReplayTrainingPanel — PySide6 not available."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *args, **kwargs):
            logger.warning("[ReplayTrainingPanel] PySide6 not available — stub mode")
