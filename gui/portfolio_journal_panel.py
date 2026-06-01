"""
gui/portfolio_journal_panel.py — PortfolioJournalPanel (v0.4.6).

PySide6 panel for Portfolio Journal & Trade Review tab in the Cockpit.

Features:
  - Safety banner (Journal Only / Research Only / No Real Orders)
  - 6 summary cards: Total, Open Simulated, Closed Simulated, Reviewed,
    Review Required, Most Common Mistake
  - Journal Entry Table with colour coding
  - Entry Detail Panel
  - New Entry Form
  - Review Panel
  - Action buttons: Add Entry, Refresh, Generate Report, Mark Reviewed,
    Link Replay Session
  - QThread worker for non-blocking report generation
  - Empty-state display when no entries exist

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT connect to broker. Does NOT submit orders.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout,
        QFrame, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
        QPushButton, QScrollArea, QSplitter, QTableWidget, QTableWidgetItem,
        QTextEdit, QVBoxLayout, QWidget,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — PortfolioJournalPanel disabled")

from gui.portfolio_journal_adapter import PortfolioJournalAdapter

_SAFETY_BANNER = (
    "[!] Journal Only  |  Research Only  |  No Real Orders  |  "
    "Production Trading: BLOCKED  |  No Broker Connection"
)

_STATUS_COLORS = {
    "PLANNED":          "#3498db",
    "OPEN_SIMULATED":   "#e67e22",
    "CLOSED_SIMULATED": "#9b59b6",
    "REVIEWED":         "#27ae60",
    "CANCELLED":        "#7f8c8d",
    "INVALIDATED":      "#c0392b",
    "ARCHIVED":         "#555555",
}

_ALL_ENTRY_TYPES = [
    "simulated_trade", "paper_trade", "replay_note",
    "signal_review", "portfolio_review", "manual_note",
]

_ALL_OUTCOME_LABELS = [
    "UNKNOWN", "WIN", "LOSS", "BREAKEVEN",
    "MISSED_OPPORTUNITY", "AVOIDED_BAD_TRADE", "FALSE_SIGNAL",
    "GOOD_PROCESS_BAD_OUTCOME", "BAD_PROCESS_GOOD_OUTCOME", "NEEDS_REVIEW",
]

_ALL_MISTAKE_TAGS = [
    "chase_high", "ignored_stop", "oversized_position", "bought_weak_stock",
    "ignored_data_quality", "ignored_provider_warning", "ignored_fake_breakout",
    "ignored_vwap_loss", "ignored_top_pattern", "ignored_fundamental_deterioration",
    "no_plan", "emotional_trade", "overtrading",
]


if _PYSIDE6_AVAILABLE:

    class _ReportWorker(QThread):
        """QThread worker for non-blocking report generation."""
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter: PortfolioJournalAdapter):
            super().__init__()
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.generate_report()
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    # -----------------------------------------------------------------------

    class PortfolioJournalPanel(QWidget):
        """
        Portfolio Journal & Trade Review panel for the TW Quant Cockpit.

        [!] Journal Only. Research Only. No Real Orders.
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode    = mode
            self._adapter = PortfolioJournalAdapter(mode=mode)
            self._worker: _ReportWorker | None = None
            self._entries: list = []
            self._setup_ui()
            self._refresh_data()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            root = QVBoxLayout(self)
            root.setSpacing(6)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background:#8e44ad; color:white; font-weight:bold; padding:6px; border-radius:4px;"
            )
            root.addWidget(banner)

            # Summary cards
            root.addLayout(self._build_summary_cards())

            # Action buttons
            root.addLayout(self._build_buttons())

            # Splitter: left = table, right = detail + form + review
            splitter = QSplitter(Qt.Horizontal)

            # Left: entry table
            left_w = QWidget()
            left_layout = QVBoxLayout(left_w)
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.addWidget(QLabel("Journal Entries:"))
            self._table = QTableWidget()
            self._table.setColumnCount(9)
            self._table.setHorizontalHeaderLabels([
                "Created", "Symbol", "Type", "Signal Source",
                "Status", "Outcome", "Return %", "Mistake Tags", "Review?"
            ])
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.horizontalHeader().setStretchLastSection(True)
            self._table.selectionModel().selectionChanged.connect(self._on_row_selected)
            left_layout.addWidget(self._table)
            splitter.addWidget(left_w)

            # Right: detail, new entry form, review panel
            right_w = QWidget()
            right_layout = QVBoxLayout(right_w)
            right_layout.setContentsMargins(0, 0, 0, 0)

            right_layout.addWidget(self._build_detail_panel())
            right_layout.addWidget(self._build_new_entry_form())
            right_layout.addWidget(self._build_review_panel())
            right_layout.addStretch()
            splitter.addWidget(right_w)
            splitter.setSizes([620, 380])
            root.addWidget(splitter, 1)

            # Status bar
            self._status_label = QLabel("Ready.")
            self._status_label.setStyleSheet("color:#888; font-size:11px;")
            root.addWidget(self._status_label)

        def _build_summary_cards(self) -> QHBoxLayout:
            row = QHBoxLayout()
            self._card_total    = self._make_card("Total", "0", "#2c3e50")
            self._card_open     = self._make_card("Open Sim", "0", "#e67e22")
            self._card_closed   = self._make_card("Closed Sim", "0", "#9b59b6")
            self._card_reviewed = self._make_card("Reviewed", "0", "#27ae60")
            self._card_review_req = self._make_card("Need Review", "0", "#c0392b")
            self._card_mistake  = self._make_card("Top Mistake", "—", "#34495e")
            for c in (self._card_total, self._card_open, self._card_closed,
                      self._card_reviewed, self._card_review_req, self._card_mistake):
                row.addWidget(c)
            return row

        def _make_card(self, label: str, value: str, color: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet(f"background:{color}; border-radius:6px; padding:4px;")
            layout = QVBoxLayout(frame)
            layout.setSpacing(2)
            val_lbl = QLabel(value)
            val_lbl.setAlignment(Qt.AlignCenter)
            val_lbl.setFont(QFont("Arial", 14, QFont.Bold))
            val_lbl.setStyleSheet("color:white;")
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color:white; font-size:10px;")
            layout.addWidget(val_lbl)
            layout.addWidget(lbl)
            frame._val = val_lbl  # type: ignore[attr-defined]
            return frame

        def _update_card(self, frame: QFrame, value) -> None:
            frame._val.setText(str(value))  # type: ignore[attr-defined]

        def _build_buttons(self) -> QHBoxLayout:
            row = QHBoxLayout()
            self._btn_add      = QPushButton("Add Entry")
            self._btn_refresh  = QPushButton("Refresh")
            self._btn_mark_rev = QPushButton("Mark Reviewed")
            self._btn_link_rep = QPushButton("Link Replay")
            self._btn_report   = QPushButton("Generate Report")

            self._btn_add.clicked.connect(self._on_add_entry)
            self._btn_refresh.clicked.connect(self._refresh_data)
            self._btn_mark_rev.clicked.connect(self._on_mark_reviewed)
            self._btn_link_rep.clicked.connect(self._on_link_replay)
            self._btn_report.clicked.connect(self._on_generate_report)

            for btn in (self._btn_add, self._btn_refresh, self._btn_mark_rev,
                        self._btn_link_rep, self._btn_report):
                row.addWidget(btn)
            row.addStretch()
            return row

        def _build_detail_panel(self) -> QGroupBox:
            group = QGroupBox("Entry Detail")
            layout = QVBoxLayout(group)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setFixedHeight(180)
            layout.addWidget(self._detail_text)
            return group

        def _build_new_entry_form(self) -> QGroupBox:
            group = QGroupBox("New Entry Form")
            form  = QFormLayout(group)

            self._form_symbol    = QLineEdit()
            self._form_symbol.setPlaceholderText("e.g. 2330")
            self._form_etype     = QComboBox()
            self._form_etype.addItems(_ALL_ENTRY_TYPES)
            self._form_timeframe = QLineEdit()
            self._form_timeframe.setPlaceholderText("e.g. daily, 60min")
            self._form_signal    = QLineEdit()
            self._form_signal.setPlaceholderText("e.g. signal_quality / rule_governance")
            self._form_planned_entry = QLineEdit()
            self._form_planned_entry.setPlaceholderText("e.g. 580.0")
            self._form_planned_stop  = QLineEdit()
            self._form_planned_stop.setPlaceholderText("e.g. 565.0")
            self._form_planned_target = QLineEdit()
            self._form_planned_target.setPlaceholderText("e.g. 610.0")
            self._form_reason   = QLineEdit()
            self._form_reason.setPlaceholderText("Short reason for entry")
            self._form_thesis   = QTextEdit()
            self._form_thesis.setFixedHeight(60)
            self._form_thesis.setPlaceholderText("Research thesis / hypothesis")
            self._form_inv_cond = QLineEdit()
            self._form_inv_cond.setPlaceholderText("What would invalidate the thesis?")

            form.addRow("Symbol:",           self._form_symbol)
            form.addRow("Entry Type:",        self._form_etype)
            form.addRow("Timeframe:",         self._form_timeframe)
            form.addRow("Signal Source:",     self._form_signal)
            form.addRow("Planned Entry:",     self._form_planned_entry)
            form.addRow("Planned Stop:",      self._form_planned_stop)
            form.addRow("Planned Target:",    self._form_planned_target)
            form.addRow("Reason:",            self._form_reason)
            form.addRow("Thesis:",            self._form_thesis)
            form.addRow("Invalidation:",      self._form_inv_cond)

            btn_submit = QPushButton("Add Journal Entry")
            btn_submit.clicked.connect(self._on_submit_form)
            form.addRow("", btn_submit)
            return group

        def _build_review_panel(self) -> QGroupBox:
            group = QGroupBox("Review Panel")
            form  = QFormLayout(group)

            self._rev_outcome  = QComboBox()
            self._rev_outcome.addItems(_ALL_OUTCOME_LABELS)
            self._rev_mistakes = QLineEdit()
            self._rev_mistakes.setPlaceholderText("comma-separated: chase_high,ignored_stop,…")
            self._rev_notes    = QTextEdit()
            self._rev_notes.setFixedHeight(50)
            self._rev_notes.setPlaceholderText("Review notes: what went right / wrong")

            form.addRow("Outcome Label:",  self._rev_outcome)
            form.addRow("Mistake Tags:",   self._rev_mistakes)
            form.addRow("Review Notes:",   self._rev_notes)

            btn_save = QPushButton("Save Review")
            btn_save.clicked.connect(self._on_save_review)
            form.addRow("", btn_save)
            return group

        # ------------------------------------------------------------------
        # Data loading
        # ------------------------------------------------------------------

        def _refresh_data(self):
            self._set_status("Loading journal entries…")
            entries  = self._adapter.list_entries(limit=500)
            self._entries = entries
            self._populate_table(entries)
            summary = self._adapter.build_summary()
            self._update_summary_cards(summary)
            self._set_status(
                f"Loaded {len(entries)} entries. "
                f"Review required: {summary.get('review_required_count', 0)}"
            )

        def _update_summary_cards(self, summary: dict):
            self._update_card(self._card_total,     summary.get("entries_count", 0))
            self._update_card(self._card_open,      summary.get("open_simulated_count", 0))
            self._update_card(self._card_closed,    summary.get("closed_simulated_count", 0))
            self._update_card(self._card_reviewed,  summary.get("reviewed_count", 0))
            self._update_card(self._card_review_req, summary.get("review_required_count", 0))
            mm = summary.get("most_common_mistake", "—") or "—"
            self._update_card(self._card_mistake,   mm[:16])

        def _populate_table(self, entries: list):
            self._table.setRowCount(0)
            if not entries:
                self._table.setRowCount(1)
                item = QTableWidgetItem("No journal entries recorded.")
                item.setFlags(Qt.ItemIsEnabled)
                self._table.setItem(0, 2, item)
                return
            self._table.setRowCount(len(entries))
            for row, e in enumerate(entries):
                status  = e.get("status", "PLANNED")
                color   = QColor(_STATUS_COLORS.get(status, "#555"))
                ret     = e.get("actual_return_pct")
                ret_s   = f"{ret:.2f}%" if ret is not None else ""
                mistakes = "|".join(e.get("mistake_tags", [])) or ""
                status_cs = e.get("status", "CLOSED_SIMULATED")
                outcome   = e.get("outcome_label", "UNKNOWN")
                review_req = "Yes" if (
                    status_cs == "CLOSED_SIMULATED" and outcome == "UNKNOWN"
                ) else ""
                vals = [
                    e.get("created_at", "")[:10],
                    e.get("symbol", ""),
                    e.get("entry_type", ""),
                    e.get("signal_source", ""),
                    status,
                    outcome,
                    ret_s,
                    mistakes,
                    review_req,
                ]
                for col, val in enumerate(vals):
                    item = QTableWidgetItem(str(val))
                    item.setBackground(color)
                    item.setForeground(QColor("white"))
                    self._table.setItem(row, col, item)

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_add_entry(self):
            """Show the New Entry Form scroll area (it's always visible; just set focus)."""
            self._form_symbol.setFocus()
            self._set_status("Fill in the New Entry Form below and click 'Add Journal Entry'.")

        def _on_submit_form(self):
            symbol = self._form_symbol.text().strip()
            if not symbol:
                self._set_status("Symbol is required.")
                return

            def _parse_float(text: str):
                try:
                    return float(text.strip()) if text.strip() else None
                except ValueError:
                    return None

            payload = {
                "symbol":           symbol,
                "entry_type":       self._form_etype.currentText(),
                "timeframe":        self._form_timeframe.text().strip(),
                "signal_source":    self._form_signal.text().strip(),
                "planned_entry_price":  _parse_float(self._form_planned_entry.text()),
                "planned_stop_loss":    _parse_float(self._form_planned_stop.text()),
                "planned_take_profit":  _parse_float(self._form_planned_target.text()),
                "reason":               self._form_reason.text().strip(),
                "thesis":               self._form_thesis.toPlainText().strip(),
                "invalidation_condition": self._form_inv_cond.text().strip(),
            }
            result = self._adapter.add_entry(payload)
            if result.get("status") == "OK":
                jid = result.get("journal_id", "")
                self._set_status(f"Entry added: {jid}")
                self._clear_form()
                self._refresh_data()
            else:
                self._set_status(f"Add failed: {result.get('error', '')}")

        def _clear_form(self):
            self._form_symbol.clear()
            self._form_timeframe.clear()
            self._form_signal.clear()
            self._form_planned_entry.clear()
            self._form_planned_stop.clear()
            self._form_planned_target.clear()
            self._form_reason.clear()
            self._form_thesis.clear()
            self._form_inv_cond.clear()

        def _on_mark_reviewed(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._entries):
                self._set_status("Select an entry first.")
                return
            entry = self._entries[row]
            jid   = entry.get("journal_id", "")
            outcome = self._rev_outcome.currentText()
            notes   = self._rev_notes.toPlainText().strip()
            raw_tags = self._rev_mistakes.text().strip()
            result = self._adapter.update_review(jid, {
                "outcome_label": outcome,
                "mistake_tags":  raw_tags,
                "review_notes":  notes,
            })
            if result.get("status") == "OK":
                self._set_status(f"Reviewed: {jid} → {outcome}")
                self._refresh_data()
            else:
                self._set_status(f"Review update failed: {result.get('error', '')}")

        def _on_save_review(self):
            self._on_mark_reviewed()

        def _on_link_replay(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._entries):
                self._set_status("Select a journal entry first.")
                return
            entry = self._entries[row]
            jid   = entry.get("journal_id", "")
            session_id, ok = self._prompt_text("Link Replay Session",
                                               "Enter Replay Session ID (e.g. REPLAY-xxxx):")
            if not ok or not session_id:
                return
            result = self._adapter.link_replay_session(jid, session_id)
            if result.get("status") == "OK":
                self._set_status(f"Linked {jid} → {session_id}")
                self._refresh_data()
            else:
                self._set_status(f"Link failed: {result.get('error', '')}")

        def _on_generate_report(self):
            if self._worker and self._worker.isRunning():
                return
            self._btn_report.setEnabled(False)
            self._set_status("Generating Portfolio Journal report…")
            self._worker = _ReportWorker(self._adapter)
            self._worker.finished.connect(self._on_report_done)
            self._worker.error.connect(lambda msg: (
                self._set_status(f"Report error: {msg}"),
                self._btn_report.setEnabled(True),
            ))
            self._worker.start()

        def _on_report_done(self, result: dict):
            self._btn_report.setEnabled(True)
            path = result.get("report_path", "")
            if result.get("status") == "OK":
                self._set_status(f"Report written → {path}")
            else:
                self._set_status(f"Report failed: {result.get('error', '')}")

        # ------------------------------------------------------------------
        # Row selection → detail panel
        # ------------------------------------------------------------------

        def _on_row_selected(self):
            row = self._table.currentRow()
            if row < 0 or row >= len(self._entries):
                self._detail_text.clear()
                return
            e = self._entries[row]
            lines = [
                f"ID:              {e.get('journal_id', '')}",
                f"Symbol:          {e.get('symbol', '')}",
                f"Entry Type:      {e.get('entry_type', '')}",
                f"Status:          {e.get('status', '')}",
                f"Signal Source:   {e.get('signal_source', '')}",
                f"Timeframe:       {e.get('timeframe', '')}",
                f"",
                f"Thesis:          {e.get('thesis', '')}",
                f"Reason:          {e.get('reason', '')}",
                f"Invalidation:    {e.get('invalidation_condition', '')}",
                f"",
                f"Planned Entry:   {e.get('planned_entry_price') or '—'}",
                f"Planned Stop:    {e.get('planned_stop_loss') or '—'}",
                f"Planned Target:  {e.get('planned_take_profit') or '—'}",
                f"Actual Entry:    {e.get('actual_entry_price') or '—'}",
                f"Actual Exit:     {e.get('actual_exit_price') or '—'}",
                f"Return %:        {e.get('actual_return_pct') or '—'}",
                f"",
                f"Outcome:         {e.get('outcome_label', '')}",
                f"Mistake Tags:    {', '.join(e.get('mistake_tags', []))}",
                f"Review Notes:    {e.get('review_notes', '')}",
                f"Replay Session:  {e.get('replay_session_id', '')}",
                f"Related Reports: {', '.join(e.get('related_reports', []))}",
            ]
            self._detail_text.setPlainText("\n".join(lines))

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        def _set_status(self, msg: str):
            self._status_label.setText(msg)

        def _prompt_text(self, title: str, prompt: str):
            """Simple text input dialog. Returns (text, ok)."""
            from PySide6.QtWidgets import QInputDialog
            return QInputDialog.getText(self, title, prompt)


else:
    class PortfolioJournalPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not available."""
        def __init__(self, *args, **kwargs):
            logger.warning("PortfolioJournalPanel: PySide6 not available — panel disabled")
