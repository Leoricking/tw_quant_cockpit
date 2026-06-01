"""gui/intraday_replay_panel.py — Intraday Replay Cockpit GUI Panel (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice.
[!] Actions run in QThread to avoid GUI freeze."""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
        QLineEdit, QComboBox, QButtonGroup, QRadioButton, QScrollArea,
        QSizePolicy, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — IntradayReplayPanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _LoadWorker(QThread):
        finished = Signal(dict)

        def __init__(self, symbol: str, date: str, freq: str):
            super().__init__()
            self._symbol = symbol
            self._date = date or None
            self._freq = freq

        def run(self):
            try:
                from gui.intraday_replay_adapter import IntradayReplayAdapter
                result = IntradayReplayAdapter().prepare_replay(
                    symbol=self._symbol,
                    date=self._date,
                    freq=self._freq,
                )
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _StepWorker(QThread):
        finished = Signal(dict)

        def __init__(self, direction: str = "forward", adapter=None):
            super().__init__()
            self._direction = direction
            self._adapter = adapter

        def run(self):
            try:
                if self._adapter is None:
                    from gui.intraday_replay_adapter import IntradayReplayAdapter
                    self._adapter = IntradayReplayAdapter()
                if self._direction == "forward":
                    result = self._adapter.step_forward()
                else:
                    result = self._adapter.step_backward()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _StateWorker(QThread):
        finished = Signal(dict)

        def __init__(self, adapter=None):
            super().__init__()
            self._adapter = adapter

        def run(self):
            try:
                if self._adapter is None:
                    from gui.intraday_replay_adapter import IntradayReplayAdapter
                    self._adapter = IntradayReplayAdapter()
                result = self._adapter.build_current_state()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReportWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str = "real", adapter=None):
            super().__init__()
            self._mode = mode
            self._adapter = adapter

        def run(self):
            try:
                if self._adapter is None:
                    from gui.intraday_replay_adapter import IntradayReplayAdapter
                    self._adapter = IntradayReplayAdapter()
                result = self._adapter.generate_report(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lbl(text, bold=False, color=None, size=None):
    if not _PYSIDE6_OK:
        return None
    lbl = QLabel(text)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if size:
        parts.append(f"font-size:{size}px")
    if parts:
        lbl.setStyleSheet(";".join(parts))
    return lbl


def _make_table(headers):
    if not _PYSIDE6_OK:
        return None
    t = QTableWidget()
    t.setColumnCount(len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.setStyleSheet("""
        QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
        QTableWidget::item:alternate { background:#1A1A2E; }
        QHeaderView::section { background:#252540; color:#AAFFAA; font-weight:bold; }
    """)
    return t


_BTN_STYLE = (
    "QPushButton { background:#252540; color:#CCCCFF; border:1px solid #444488; "
    "border-radius:3px; padding:4px 10px; } "
    "QPushButton:hover { background:#334466; } "
    "QPushButton:disabled { color:#555555; }"
)

_GRP_STYLE = (
    "QGroupBox { color:#AAFFAA; font-weight:bold; border:1px solid #335533; "
    "border-radius:4px; margin-top:6px; } "
    "QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }"
)

_INPUT_STYLE = (
    "QLineEdit { background:#1A1A2E; color:#CCCCFF; border:1px solid #444488; "
    "border-radius:3px; padding:3px 6px; } "
    "QComboBox { background:#1A1A2E; color:#CCCCFF; border:1px solid #444488; "
    "border-radius:3px; padding:3px 6px; } "
)


# ---------------------------------------------------------------------------
# Card widget
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _CardLabel(QFrame):
        def __init__(self, title: str, value: str = "—", color: str = "#AAAAAA"):
            super().__init__()
            self.setStyleSheet(
                "background:#1A1A2E; border:1px solid #334466; border-radius:4px; padding:4px"
            )
            layout = QVBoxLayout(self)
            layout.setSpacing(2)
            layout.setContentsMargins(6, 4, 6, 4)
            self._title_lbl = QLabel(title)
            self._title_lbl.setStyleSheet("color:#888888; font-size:10px;")
            self._value_lbl = QLabel(value)
            self._value_lbl.setStyleSheet(f"color:{color}; font-weight:bold; font-size:13px;")
            layout.addWidget(self._title_lbl)
            layout.addWidget(self._value_lbl)

        def set_value(self, value: str, color: str = None):
            self._value_lbl.setText(str(value))
            if color:
                self._value_lbl.setStyleSheet(f"color:{color}; font-weight:bold; font-size:13px;")


# ---------------------------------------------------------------------------
# IntradayReplayPanel
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class IntradayReplayPanel(QWidget):
        """Intraday Replay Cockpit GUI Panel (v0.4.4).

        Replay Training Only / Read Only / No Real Orders / Production Trading BLOCKED.
        """

        def __init__(self, parent=None, mode: str = "real"):
            super().__init__(parent)
            self._mode = mode
            self._workers: list = []
            self._adapter = None  # shared adapter instance
            self._current_question = None
            self._question_buttons: list = []
            self._question_group = None
            self._build_ui()

        def _get_adapter(self):
            if self._adapter is None:
                try:
                    from gui.intraday_replay_adapter import IntradayReplayAdapter
                    self._adapter = IntradayReplayAdapter()
                except Exception as exc:
                    logger.error("[IntradayReplayPanel] adapter init error: %s", exc)
            return self._adapter

        # ------------------------------------------------------------------
        # UI Construction
        # ------------------------------------------------------------------
        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setSpacing(6)
            root.setContentsMargins(8, 8, 8, 8)

            # ── A. Safety Banner ──────────────────────────────────────────
            banner = QFrame()
            banner.setStyleSheet(
                "background:#0A1A0A; border:1px solid #335533; border-radius:4px; padding:4px"
            )
            ban_layout = QHBoxLayout(banner)
            ban_layout.addWidget(_lbl("Intraday Replay Cockpit", bold=True, color="#AAFFAA", size=13))
            ban_layout.addSpacing(10)
            for text, color in [
                ("Replay Training Only", "#AAFFAA"),
                ("No Live Prediction",   "#FFDDAA"),
                ("No Real Orders",       "#FFAAAA"),
                ("Production Trading BLOCKED", "#FF6666"),
            ]:
                tag = QLabel(f"[{text}]")
                tag.setStyleSheet(f"color:{color};font-weight:bold;font-size:11px")
                ban_layout.addWidget(tag)
            ban_layout.addStretch()
            root.addWidget(banner)

            # ── B. Controls Row ───────────────────────────────────────────
            ctrl_box = QGroupBox("Replay Controls")
            ctrl_box.setStyleSheet(_GRP_STYLE)
            ctrl_layout = QHBoxLayout(ctrl_box)

            self._inp_symbol = QLineEdit()
            self._inp_symbol.setPlaceholderText("Symbol (e.g. AAPL)")
            self._inp_symbol.setStyleSheet(_INPUT_STYLE)
            self._inp_symbol.setMaximumWidth(120)

            self._inp_date = QLineEdit()
            self._inp_date.setPlaceholderText("Date YYYY-MM-DD")
            self._inp_date.setStyleSheet(_INPUT_STYLE)
            self._inp_date.setMaximumWidth(120)

            self._cmb_freq = QComboBox()
            self._cmb_freq.addItems(["1min", "5min"])
            self._cmb_freq.setStyleSheet(_INPUT_STYLE)
            self._cmb_freq.setMaximumWidth(80)

            self._btn_load = QPushButton("Load")
            self._btn_step_fwd = QPushButton("Step ▶")
            self._btn_step_bwd = QPushButton("◀ Step")

            self._inp_jump = QLineEdit()
            self._inp_jump.setPlaceholderText("Jump to time HH:MM")
            self._inp_jump.setStyleSheet(_INPUT_STYLE)
            self._inp_jump.setMaximumWidth(120)
            self._btn_jump = QPushButton("Jump")

            self._btn_reset = QPushButton("Reset")
            self._btn_report = QPushButton("Generate Report")

            for btn in [
                self._btn_load, self._btn_step_fwd, self._btn_step_bwd,
                self._btn_jump, self._btn_reset, self._btn_report,
            ]:
                btn.setStyleSheet(_BTN_STYLE)

            ctrl_layout.addWidget(QLabel("Symbol:"))
            ctrl_layout.addWidget(self._inp_symbol)
            ctrl_layout.addWidget(QLabel("Date:"))
            ctrl_layout.addWidget(self._inp_date)
            ctrl_layout.addWidget(QLabel("Freq:"))
            ctrl_layout.addWidget(self._cmb_freq)
            ctrl_layout.addWidget(self._btn_load)
            ctrl_layout.addSpacing(10)
            ctrl_layout.addWidget(self._btn_step_bwd)
            ctrl_layout.addWidget(self._btn_step_fwd)
            ctrl_layout.addSpacing(10)
            ctrl_layout.addWidget(self._inp_jump)
            ctrl_layout.addWidget(self._btn_jump)
            ctrl_layout.addSpacing(10)
            ctrl_layout.addWidget(self._btn_reset)
            ctrl_layout.addWidget(self._btn_report)
            ctrl_layout.addStretch()
            root.addWidget(ctrl_box)

            # ── C. Summary Cards ──────────────────────────────────────────
            cards_box = QGroupBox("Current State")
            cards_box.setStyleSheet(_GRP_STYLE)
            cards_layout = QHBoxLayout(cards_box)

            self._card_price      = _CardLabel("Current Price",     "—", "#CCCCFF")
            self._card_vwap       = _CardLabel("VWAP State",        "—", "#AAFFDD")
            self._card_or         = _CardLabel("Opening Range State","—", "#FFDDAA")
            self._card_fb         = _CardLabel("Fake Breakout Risk", "—", "#FFAAAA")
            self._card_bars       = _CardLabel("Bars Replayed",     "—", "#AAAACC")
            self._card_events     = _CardLabel("Events Detected",   "—", "#FFFFAA")

            for card in [
                self._card_price, self._card_vwap, self._card_or,
                self._card_fb, self._card_bars, self._card_events,
            ]:
                cards_layout.addWidget(card)
            cards_layout.addStretch()
            root.addWidget(cards_box)

            # ── D. Visible Bars Table ──────────────────────────────────────
            bars_box = QGroupBox("Visible Bars")
            bars_box.setStyleSheet(_GRP_STYLE)
            bars_layout = QVBoxLayout(bars_box)
            self._bars_table = _make_table(["Time", "Open", "High", "Low", "Close", "Volume"])
            self._bars_table.setMaximumHeight(180)
            self._bars_empty = _lbl(
                "No intraday data loaded. Enter symbol, date, and click Load.",
                color="#888888"
            )
            bars_layout.addWidget(self._bars_table)
            bars_layout.addWidget(self._bars_empty)
            root.addWidget(bars_box)

            # ── E. Event Timeline Table ────────────────────────────────────
            evt_box = QGroupBox("Event Timeline")
            evt_box.setStyleSheet(_GRP_STYLE)
            evt_layout = QVBoxLayout(evt_box)
            self._evt_table = _make_table(
                ["Time", "Type", "Title", "Severity", "Source", "Description"]
            )
            self._evt_table.setMaximumHeight(150)
            self._evt_empty = _lbl("No events detected.", color="#888888")
            evt_layout.addWidget(self._evt_table)
            evt_layout.addWidget(self._evt_empty)
            root.addWidget(evt_box)

            # ── F. Training Panel ──────────────────────────────────────────
            train_box = QGroupBox("Training Mode")
            train_box.setStyleSheet(_GRP_STYLE)
            train_layout = QVBoxLayout(train_box)

            self._lbl_question = QLabel("No training question available yet. Load and step through data.")
            self._lbl_question.setStyleSheet("color:#FFFFCC; font-size:12px;")
            self._lbl_question.setWordWrap(True)
            train_layout.addWidget(self._lbl_question)

            self._choices_layout = QVBoxLayout()
            self._question_group = QButtonGroup(self)
            train_layout.addLayout(self._choices_layout)

            btn_row = QHBoxLayout()
            self._btn_submit = QPushButton("Submit Answer")
            self._btn_submit.setStyleSheet(_BTN_STYLE)
            self._btn_submit.setEnabled(False)
            btn_row.addWidget(self._btn_submit)
            btn_row.addStretch()
            train_layout.addLayout(btn_row)

            self._lbl_explanation = QLabel("")
            self._lbl_explanation.setStyleSheet("color:#AAFFAA; font-size:11px;")
            self._lbl_explanation.setWordWrap(True)
            train_layout.addWidget(self._lbl_explanation)

            self._lbl_score = QLabel("Training Score: —")
            self._lbl_score.setStyleSheet("color:#CCCCFF; font-weight:bold;")
            train_layout.addWidget(self._lbl_score)

            root.addWidget(train_box)

            # ── G. Session Metrics ─────────────────────────────────────────
            metrics_box = QGroupBox("Session Metrics")
            metrics_box.setStyleSheet(_GRP_STYLE)
            metrics_layout = QHBoxLayout(metrics_box)

            self._lbl_session_id      = _lbl("Session: —",      color="#AAAAAA")
            self._lbl_session_status  = _lbl("Status: —",        color="#AAAAAA")
            self._lbl_total_bars      = _lbl("Total Bars: —",    color="#AAAAAA")
            self._lbl_session_dur     = _lbl("Duration: —",      color="#AAAAAA")
            self._lbl_quiz_accuracy   = _lbl("Quiz Accuracy: —", color="#AAAAAA")
            self._lbl_grade           = _lbl("Grade: —",         color="#FFFFAA", bold=True)

            for lbl in [
                self._lbl_session_id, self._lbl_session_status,
                self._lbl_total_bars, self._lbl_session_dur,
                self._lbl_quiz_accuracy, self._lbl_grade,
            ]:
                metrics_layout.addWidget(lbl)
            metrics_layout.addStretch()
            root.addWidget(metrics_box)

            # ── Connect Signals ────────────────────────────────────────────
            self._btn_load.clicked.connect(self._on_load)
            self._btn_step_fwd.clicked.connect(self._on_step_forward)
            self._btn_step_bwd.clicked.connect(self._on_step_backward)
            self._btn_jump.clicked.connect(self._on_jump)
            self._btn_reset.clicked.connect(self._on_reset)
            self._btn_report.clicked.connect(self._on_generate_report)
            self._btn_submit.clicked.connect(self._on_submit_answer)

            # Initial state
            self._set_controls_enabled(False)

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------
        def _set_controls_enabled(self, enabled: bool):
            for btn in [
                self._btn_step_fwd, self._btn_step_bwd,
                self._btn_jump, self._btn_reset, self._btn_report,
            ]:
                btn.setEnabled(enabled)

        def _register_worker(self, worker):
            self._workers.append(worker)
            worker.finished.connect(lambda _: self._cleanup_workers())
            return worker

        def _cleanup_workers(self):
            self._workers = [w for w in self._workers if w.isRunning()]

        def _populate_bars_table(self, bars: list):
            self._bars_table.setRowCount(0)
            if not bars:
                self._bars_empty.setVisible(True)
                self._bars_table.setVisible(False)
                return
            self._bars_empty.setVisible(False)
            self._bars_table.setVisible(True)

            col_map = {
                "Time":   ["datetime", "time", "timestamp"],
                "Open":   ["open", "o"],
                "High":   ["high", "h"],
                "Low":    ["low", "l"],
                "Close":  ["close", "c"],
                "Volume": ["volume", "vol", "v"],
            }

            for bar in bars[-50:]:  # show last 50 bars
                row = self._bars_table.rowCount()
                self._bars_table.insertRow(row)
                for col_idx, (col_name, candidates) in enumerate(col_map.items()):
                    val = ""
                    for cand in candidates:
                        if cand in bar:
                            val = bar[cand]
                            break
                    item = QTableWidgetItem(str(val) if val is not None else "")
                    item.setTextAlignment(Qt.AlignCenter)
                    self._bars_table.setItem(row, col_idx, item)

            # Scroll to bottom
            self._bars_table.scrollToBottom()

        def _populate_events_table(self, events: list):
            self._evt_table.setRowCount(0)
            if not events:
                self._evt_empty.setVisible(True)
                self._evt_table.setVisible(False)
                return
            self._evt_empty.setVisible(False)
            self._evt_table.setVisible(True)

            severity_colors = {
                "INFO": "#AAFFAA",
                "WARNING": "#FFDDAA",
                "CRITICAL": "#FF6666",
            }

            for evt in events:
                row = self._evt_table.rowCount()
                self._evt_table.insertRow(row)
                vals = [
                    str(evt.get("time", "")),
                    str(evt.get("event_type", "")),
                    str(evt.get("title", "")),
                    str(evt.get("severity", "")),
                    str(evt.get("source", "")),
                    str(evt.get("description", ""))[:80],
                ]
                sev = evt.get("severity", "INFO")
                color = severity_colors.get(sev, "#EEEEEE")
                for col_idx, val in enumerate(vals):
                    item = QTableWidgetItem(val)
                    item.setForeground(QColor(color))
                    self._evt_table.setItem(row, col_idx, item)

        def _update_state_cards(self, state: dict):
            bar = state.get("current_bar", {})
            close_val = bar.get("close", bar.get("c", "—"))
            self._card_price.set_value(str(close_val), "#CCCCFF")

            vwap = state.get("vwap", {})
            self._card_vwap.set_value(
                str(vwap.get("vwap_state", "—")),
                "#AAFFDD" if vwap.get("above_vwap") else "#FFAAAA",
            )

            or_state = state.get("opening_range", {})
            self._card_or.set_value(
                str(or_state.get("range_break_status", "—")), "#FFDDAA"
            )

            fb = state.get("fake_breakout", {})
            risk = fb.get("risk_level", "—")
            fb_color = {"LOW": "#AAFFAA", "MEDIUM": "#FFDDAA", "HIGH": "#FF9966", "CRITICAL": "#FF4444"}.get(risk, "#AAAAAA")
            self._card_fb.set_value(risk, fb_color)

            self._card_bars.set_value(str(state.get("bar_index", "—")))
            self._card_events.set_value(str(len(state.get("events", []))))

        def _show_training_question(self, events: list):
            """Show a training question for the most recent significant event."""
            if not events:
                return

            # Find first event with a meaningful type
            interesting = ["OPENING_RANGE_BREAK", "VWAP_RECLAIM", "VWAP_LOST",
                           "FAKE_BREAKOUT_WARNING", "VOLUME_SPIKE", "POC_TOUCH"]
            target_evt = None
            for evt in reversed(events):
                if evt.get("event_type") in interesting:
                    target_evt = evt
                    break

            if target_evt is None:
                return

            try:
                from replay.training_mode import ReplayTrainingMode
                from replay.replay_events import ReplayEvent

                # Build a ReplayEvent from dict
                class _EvtObj:
                    def __init__(self, d):
                        self.event_type = d.get("event_type", "")
                        self.bar_index = d.get("bar_index", 0)
                        self.event_id = d.get("event_id", "")
                        self.time = d.get("time", "")

                mode_obj = ReplayTrainingMode()
                questions = mode_obj.generate_questions([_EvtObj(target_evt)], None)
                if not questions:
                    return

                q = questions[0]
                self._current_question = (q, mode_obj)

                self._lbl_question.setText(f"[Training Question]\n{q.prompt}")
                self._lbl_explanation.setText("")

                # Clear old radio buttons
                for btn in self._question_buttons:
                    self._choices_layout.removeWidget(btn)
                    btn.deleteLater()
                self._question_buttons.clear()
                self._question_group = QButtonGroup(self)

                for i, choice in enumerate(q.choices):
                    rb = QRadioButton(choice)
                    rb.setStyleSheet("color:#FFFFCC;")
                    self._choices_layout.addWidget(rb)
                    self._question_group.addButton(rb, i)
                    self._question_buttons.append(rb)

                self._btn_submit.setEnabled(True)

            except Exception as exc:
                logger.warning("[IntradayReplayPanel] show_training_question error: %s", exc)

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------
        def _on_load(self):
            symbol = self._inp_symbol.text().strip().upper()
            if not symbol:
                QMessageBox.warning(self, "Input Required", "Please enter a symbol.")
                return
            date = self._inp_date.text().strip() or None
            freq = self._cmb_freq.currentText()

            self._btn_load.setEnabled(False)
            self._bars_empty.setText("Loading intraday data…")

            worker = _LoadWorker(symbol=symbol, date=date, freq=freq)
            worker.finished.connect(self._on_load_done)
            self._register_worker(worker)
            worker.start()

        def _on_load_done(self, result: dict):
            self._btn_load.setEnabled(True)
            if not result.get("ok"):
                err = result.get("error", "unknown")
                self._bars_empty.setText(
                    f"[!] Load failed: {err}\n"
                    f"No intraday data found. Check symbol/date/freq."
                )
                self._set_controls_enabled(False)
                return

            summary = result.get("summary", {})
            total = summary.get("total_bars", 0)
            self._lbl_total_bars.setText(f"Total Bars: {total}")
            self._lbl_session_status.setText("Status: READY")
            self._set_controls_enabled(True)

            # Show initial bar
            current_bar = result.get("current_bar", {})
            self._populate_bars_table([current_bar] if current_bar else [])
            self._card_bars.set_value("0")
            self._card_events.set_value("0")

            # Rebuild adapter reference
            from gui.intraday_replay_adapter import IntradayReplayAdapter
            self._adapter = IntradayReplayAdapter()
            # Re-prepare to share state (engine is module-level in adapter instance)
            self._adapter.prepare_replay(
                symbol=self._inp_symbol.text().strip().upper(),
                date=self._inp_date.text().strip() or None,
                freq=self._cmb_freq.currentText(),
            )

        def _on_step_forward(self):
            self._do_step("forward")

        def _on_step_backward(self):
            self._do_step("backward")

        def _do_step(self, direction: str):
            adapter = self._get_adapter()
            if adapter is None:
                return
            worker = _StepWorker(direction=direction, adapter=adapter)
            worker.finished.connect(self._on_step_done)
            self._register_worker(worker)
            worker.start()

        def _on_step_done(self, result: dict):
            if not result.get("ok"):
                return

            index = result.get("index", 0)
            total = result.get("total", 0)
            self._card_bars.set_value(f"{index} / {total}")
            self._lbl_total_bars.setText(f"Total Bars: {total}")

            # Build full state
            adapter = self._get_adapter()
            if adapter is None:
                return
            state_worker = _StateWorker(adapter=adapter)
            state_worker.finished.connect(self._on_state_done)
            self._register_worker(state_worker)
            state_worker.start()

        def _on_state_done(self, result: dict):
            if not result.get("ok"):
                return
            state = result.get("state", {})
            self._update_state_cards(state)

            # Update bars table
            adapter = self._get_adapter()
            if adapter:
                bars_result = adapter.get_visible_bars()
                if bars_result.get("ok"):
                    self._populate_bars_table(bars_result.get("bars", []))

            # Update events table
            events = state.get("events", [])
            self._populate_events_table(events)

            # Show training question if applicable
            self._show_training_question(events)

        def _on_jump(self):
            time_str = self._inp_jump.text().strip()
            if not time_str:
                return
            adapter = self._get_adapter()
            if adapter is None:
                return
            result = adapter.jump_to_time(time_str)
            if result.get("ok"):
                self._on_step_done(result)

        def _on_reset(self):
            adapter = self._get_adapter()
            if adapter is None:
                return
            engine = adapter._get_engine()
            if engine:
                engine.reset()
            self._card_bars.set_value("0")
            self._populate_bars_table([])
            self._populate_events_table([])
            self._lbl_question.setText("No training question available yet. Load and step through data.")
            self._lbl_explanation.setText("")
            self._lbl_score.setText("Training Score: —")
            for btn in self._question_buttons:
                self._choices_layout.removeWidget(btn)
                btn.deleteLater()
            self._question_buttons.clear()
            self._btn_submit.setEnabled(False)

        def _on_submit_answer(self):
            if self._current_question is None:
                return
            q, mode_obj = self._current_question
            checked = self._question_group.checkedButton()
            if checked is None:
                QMessageBox.information(self, "Select Answer", "Please select an answer first.")
                return

            answer_text = checked.text().strip()
            answer_letter = answer_text[0] if answer_text else ""
            result = mode_obj.answer_question(q.question_id, answer_letter)

            if result.get("correct"):
                self._lbl_explanation.setStyleSheet("color:#AAFFAA; font-size:11px;")
                self._lbl_explanation.setText(f"[Correct] {result.get('explanation', '')}")
            else:
                self._lbl_explanation.setStyleSheet("color:#FFAAAA; font-size:11px;")
                self._lbl_explanation.setText(
                    f"[Incorrect] Correct: {q.correct_answer}\n{result.get('explanation', '')}"
                )

            score = mode_obj.score_session()
            self._lbl_score.setText(
                f"Training Score: {score.get('training_score', 0):.0f} / 100  "
                f"Grade: {score.get('grade', '—')}  "
                f"Accuracy: {score.get('accuracy', 0):.1%}"
            )
            self._lbl_grade.setText(f"Grade: {score.get('grade', '—')}")
            self._btn_submit.setEnabled(False)
            self._current_question = None

        def _on_generate_report(self):
            self._btn_report.setEnabled(False)
            adapter = self._get_adapter()
            worker = _ReportWorker(mode=self._mode, adapter=adapter)
            worker.finished.connect(self._on_report_done)
            self._register_worker(worker)
            worker.start()

        def _on_report_done(self, result: dict):
            self._btn_report.setEnabled(True)
            if not result.get("ok"):
                QMessageBox.warning(self, "Report Error", f"Failed: {result.get('error', 'unknown')}")
                return
            path = result.get("report_path", "")
            reply = QMessageBox.information(
                self, "Report Generated",
                f"Report saved:\n{path}\n\nOpen in system viewer?",
                QMessageBox.Ok | QMessageBox.Cancel,
            )
            if reply == QMessageBox.Ok and path:
                try:
                    import subprocess
                    import sys
                    if sys.platform == "win32":
                        os.startfile(path)
                    elif sys.platform == "darwin":
                        subprocess.Popen(["open", path])
                    else:
                        subprocess.Popen(["xdg-open", path])
                except Exception as exc:
                    logger.warning("[IntradayReplayPanel] open report error: %s", exc)

        # ------------------------------------------------------------------
        # Cleanup
        # ------------------------------------------------------------------
        def closeEvent(self, event):
            for worker in self._workers:
                if worker.isRunning():
                    worker.quit()
                    worker.wait(2000)
            super().closeEvent(event)

else:
    # Stub when PySide6 is not available
    class IntradayReplayPanel:
        pass
