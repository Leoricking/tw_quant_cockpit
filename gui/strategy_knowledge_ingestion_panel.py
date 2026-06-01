"""
gui/strategy_knowledge_ingestion_panel.py — StrategyKnowledgeIngestionPanel PySide6 widget (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] auto_activated=False. Transcript-only confidence ≤ PARTIAL.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem,
        QGroupBox, QHeaderView, QFrame, QSizePolicy,
        QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available; StrategyKnowledgeIngestionPanel will be a stub.")


# ---------------------------------------------------------------------------
# Workers (only defined when PySide6 is available)
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:

    class _RunWorker(QObject):
        """Background worker for ingestion pipeline run."""
        result = Signal(dict)
        error = Signal(str)

        def __init__(self, adapter, dry_run: bool = True, mode: str = "real", parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._dry_run = dry_run
            self._mode = mode

        def run(self):
            try:
                res = self._adapter.run_ingestion(mode=self._mode, dry_run=self._dry_run)
                self.result.emit(res)
            except Exception as exc:
                logger.error("_RunWorker.run: %s", exc)
                self.error.emit(str(exc))

    class _ReportWorker(QObject):
        """Background worker for report generation."""
        result = Signal(dict)
        error = Signal(str)

        def __init__(self, adapter, mode: str = "real", parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._mode = mode

        def run(self):
            try:
                res = self._adapter.generate_report(mode=self._mode)
                self.result.emit(res)
            except Exception as exc:
                logger.error("_ReportWorker.run: %s", exc)
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Panel (stub if no PySide6)
# ---------------------------------------------------------------------------

if not _PYSIDE6_OK:

    class StrategyKnowledgeIngestionPanel:  # type: ignore[no-redef]
        """Stub class — PySide6 not available."""

        def __init__(self, mode: str = "real", parent=None):
            logger.warning(
                "StrategyKnowledgeIngestionPanel: PySide6 not available. "
                "Panel is a stub and will not render."
            )

        def refresh(self):
            pass

else:

    class StrategyKnowledgeIngestionPanel(QWidget):  # type: ignore[no-redef]
        """
        PySide6 panel for Strategy Knowledge Ingestion.

        Sections:
          A. Safety banner
          B. Controls (Run Dry Run, Run Ingestion, Generate Report)
          C. Summary cards
          D. Source Table
          E. Knowledge Items Table
          F. Rule Candidate Table
          G. Risk/Avoid notice
        """

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._adapter = None
            self._run_thread: QThread | None = None
            self._run_worker: _RunWorker | None = None
            self._report_thread: QThread | None = None
            self._report_worker: _ReportWorker | None = None

            self._init_adapter()
            self._build_ui()
            self.refresh()

        # ------------------------------------------------------------------
        # Adapter init
        # ------------------------------------------------------------------

        def _init_adapter(self):
            try:
                from gui.strategy_knowledge_ingestion_adapter import StrategyKnowledgeIngestionAdapter
                self._adapter = StrategyKnowledgeIngestionAdapter()
            except Exception as exc:
                logger.warning("StrategyKnowledgeIngestionPanel: adapter unavailable — %s", exc)
                self._adapter = None

        # ------------------------------------------------------------------
        # UI Construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root_layout = QVBoxLayout(self)
            root_layout.setContentsMargins(8, 8, 8, 8)
            root_layout.setSpacing(6)

            # A. Safety Banner
            banner = QLabel(
                "Strategy Knowledge Ingestion  |  Knowledge Only  |  Research Only  "
                "|  No Real Orders  |  Production Trading BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner_font = QFont()
            banner_font.setBold(True)
            banner.setFont(banner_font)
            banner.setStyleSheet(
                "background-color: #1a1a2e; color: #e94560; "
                "padding: 6px; border-radius: 4px;"
            )
            root_layout.addWidget(banner)

            # B. Controls
            ctrl_group = QGroupBox("Controls")
            ctrl_layout = QHBoxLayout(ctrl_group)
            ctrl_layout.setSpacing(8)

            self._btn_dry_run = QPushButton("Run Dry Run")
            self._btn_dry_run.setToolTip("Analyse transcripts without writing files")
            self._btn_dry_run.clicked.connect(self._on_dry_run)

            self._btn_run = QPushButton("Run Ingestion")
            self._btn_run.setToolTip("Run full ingestion and persist results")
            self._btn_run.clicked.connect(self._on_run)

            self._btn_report = QPushButton("Generate Report")
            self._btn_report.setToolTip("Generate Markdown knowledge report")
            self._btn_report.clicked.connect(self._on_report)

            self._status_label = QLabel("Ready.")
            self._status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            ctrl_layout.addWidget(self._btn_dry_run)
            ctrl_layout.addWidget(self._btn_run)
            ctrl_layout.addWidget(self._btn_report)
            ctrl_layout.addWidget(self._status_label)
            root_layout.addWidget(ctrl_group)

            # C. Summary Cards
            summary_group = QGroupBox("Summary")
            summary_layout = QHBoxLayout(summary_group)
            self._card_sources = self._make_card("Sources", "0")
            self._card_items = self._make_card("Knowledge Items", "0")
            self._card_rule_cands = self._make_card("Rule Candidates", "0")
            self._card_avoid = self._make_card("Avoid Conditions", "0")
            self._card_risk = self._make_card("Risk Conditions", "0")
            self._card_factors = self._make_card("Factor Candidates", "0")
            for card in [
                self._card_sources, self._card_items, self._card_rule_cands,
                self._card_avoid, self._card_risk, self._card_factors,
            ]:
                summary_layout.addWidget(card)
            root_layout.addWidget(summary_group)

            # D. Source Table
            src_group = QGroupBox("Knowledge Sources")
            src_layout = QVBoxLayout(src_group)
            self._source_table = QTableWidget(0, 5)
            self._source_table.setHorizontalHeaderLabels(
                ["Source ID", "Title", "Type", "Media Source", "Generated At"]
            )
            self._source_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._source_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._source_table.setSelectionBehavior(QTableWidget.SelectRows)
            src_layout.addWidget(self._source_table)
            root_layout.addWidget(src_group)

            # E. Knowledge Items Table
            items_group = QGroupBox("Knowledge Items")
            items_layout = QVBoxLayout(items_group)
            self._items_table = QTableWidget(0, 6)
            self._items_table.setHorizontalHeaderLabels(
                ["Category", "Statement", "Timeframe", "Polarity", "Confidence", "Suggested Rule ID"]
            )
            self._items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._items_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._items_table.setSelectionBehavior(QTableWidget.SelectRows)
            items_layout.addWidget(self._items_table)
            root_layout.addWidget(items_group)

            # F. Rule Candidate Table
            rc_group = QGroupBox("Rule Candidates")
            rc_layout = QVBoxLayout(rc_group)
            self._rc_table = QTableWidget(0, 4)
            self._rc_table.setHorizontalHeaderLabels(
                ["Suggested Rule ID", "Existing Rule Match", "Status", "Auto Activated"]
            )
            self._rc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._rc_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._rc_table.setSelectionBehavior(QTableWidget.SelectRows)
            rc_layout.addWidget(self._rc_table)
            root_layout.addWidget(rc_group)

            # G. Risk/Avoid notice
            self._risk_notice = QLabel(
                "[!] Long-cycle risk items are NOT short-term sell signals.  "
                "[!] auto_activated=False for ALL rule candidates.  "
                "[!] Not investment advice."
            )
            self._risk_notice.setWordWrap(True)
            self._risk_notice.setStyleSheet("color: #e94560; font-style: italic; padding: 4px;")
            root_layout.addWidget(self._risk_notice)

        # ------------------------------------------------------------------
        # Card helper
        # ------------------------------------------------------------------

        @staticmethod
        def _make_card(label: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet(
                "QFrame { border: 1px solid #444; border-radius: 4px; padding: 4px; }"
            )
            layout = QVBoxLayout(frame)
            layout.setSpacing(2)
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            val = QLabel(value)
            val.setAlignment(Qt.AlignCenter)
            val_font = QFont()
            val_font.setBold(True)
            val_font.setPointSize(14)
            val.setFont(val_font)
            val.setObjectName("card_value")
            layout.addWidget(lbl)
            layout.addWidget(val)
            return frame

        @staticmethod
        def _set_card_value(card: QFrame, value: str):
            for child in card.findChildren(QLabel):
                if child.objectName() == "card_value":
                    child.setText(value)
                    break

        # ------------------------------------------------------------------
        # Data refresh
        # ------------------------------------------------------------------

        def refresh(self):
            """Load latest data from store and update all tables."""
            if self._adapter is None:
                self._show_empty_state()
                return
            try:
                summary = self._adapter.load_latest_summary()
                self._update_summary_cards(summary)

                from knowledge.knowledge_store import StrategyKnowledgeStore
                store = StrategyKnowledgeStore()
                sources = store.load_sources()
                items = store.load_items()
                rule_candidates = store.load_rule_candidates()

                self._populate_source_table(sources)
                self._populate_items_table(items)
                self._populate_rc_table(rule_candidates)
            except Exception as exc:
                logger.warning("StrategyKnowledgeIngestionPanel.refresh: %s", exc)
                self._show_empty_state()

        def _show_empty_state(self):
            _empty_msg = "No transcripts found. Import .txt/.md files to knowledge/transcripts/"
            for table in [self._source_table, self._items_table, self._rc_table]:
                table.setRowCount(1)
                cols = table.columnCount()
                item = QTableWidgetItem(_empty_msg)
                item.setForeground(QColor("#888888"))
                table.setItem(0, 0, item)
                for col in range(1, cols):
                    table.setItem(0, col, QTableWidgetItem(""))

        # ------------------------------------------------------------------
        # Summary card update
        # ------------------------------------------------------------------

        def _update_summary_cards(self, summary: dict):
            self._set_card_value(self._card_sources, str(summary.get("sources_count", 0)))
            self._set_card_value(self._card_items, str(summary.get("total_items", 0)))
            self._set_card_value(self._card_rule_cands, str(summary.get("rule_candidates_count", 0)))
            avoid_count = summary.get("by_category", {}).get("avoid_condition", 0)
            risk_count = summary.get("by_category", {}).get("risk_condition", 0)
            self._set_card_value(self._card_avoid, str(avoid_count))
            self._set_card_value(self._card_risk, str(risk_count))
            self._set_card_value(self._card_factors, str(summary.get("factor_candidates_count", 0)))

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _populate_source_table(self, sources: list):
            self._source_table.setRowCount(0)
            if not sources:
                self._source_table.setRowCount(1)
                self._source_table.setItem(
                    0, 0, QTableWidgetItem("No sources found.")
                )
                return
            self._source_table.setRowCount(len(sources))
            for row, s in enumerate(sources):
                self._source_table.setItem(row, 0, QTableWidgetItem(str(s.get("source_id", ""))))
                self._source_table.setItem(row, 1, QTableWidgetItem(str(s.get("title", ""))[:50]))
                self._source_table.setItem(row, 2, QTableWidgetItem(str(s.get("source_type", ""))))
                self._source_table.setItem(row, 3, QTableWidgetItem(str(s.get("media_source", ""))))
                self._source_table.setItem(row, 4, QTableWidgetItem(str(s.get("generated_at", ""))))

        def _populate_items_table(self, items: list):
            self._items_table.setRowCount(0)
            if not items:
                self._items_table.setRowCount(1)
                self._items_table.setItem(
                    0, 0, QTableWidgetItem("No knowledge items found.")
                )
                return
            self._items_table.setRowCount(len(items))
            for row, item in enumerate(items):
                self._items_table.setItem(row, 0, QTableWidgetItem(str(item.get("category", ""))))
                self._items_table.setItem(row, 1, QTableWidgetItem(str(item.get("statement", ""))[:80]))
                self._items_table.setItem(row, 2, QTableWidgetItem(str(item.get("timeframe", ""))))
                self._items_table.setItem(row, 3, QTableWidgetItem(str(item.get("polarity", ""))))
                self._items_table.setItem(row, 4, QTableWidgetItem(str(item.get("confidence", ""))))
                self._items_table.setItem(row, 5, QTableWidgetItem(str(item.get("suggested_rule_id", ""))))

        def _populate_rc_table(self, rule_candidates: list):
            self._rc_table.setRowCount(0)
            if not rule_candidates:
                self._rc_table.setRowCount(1)
                self._rc_table.setItem(
                    0, 0, QTableWidgetItem("No rule candidates found.")
                )
                return
            self._rc_table.setRowCount(len(rule_candidates))
            for row, rc in enumerate(rule_candidates):
                self._rc_table.setItem(row, 0, QTableWidgetItem(str(rc.get("suggested_rule_id", ""))))
                self._rc_table.setItem(row, 1, QTableWidgetItem(str(rc.get("existing_rule_match", ""))))
                self._rc_table.setItem(row, 2, QTableWidgetItem(str(rc.get("governance_status", ""))))
                # auto_activated is always False — show it explicitly
                auto_val = str(rc.get("auto_activated", False))
                auto_item = QTableWidgetItem(auto_val)
                auto_item.setForeground(QColor("#00aa00"))
                self._rc_table.setItem(row, 3, auto_item)

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_dry_run(self):
            self._status_label.setText("Running dry run…")
            self._btn_dry_run.setEnabled(False)
            self._launch_run_worker(dry_run=True)

        def _on_run(self):
            self._status_label.setText("Running ingestion…")
            self._btn_run.setEnabled(False)
            self._launch_run_worker(dry_run=False)

        def _launch_run_worker(self, dry_run: bool):
            if self._adapter is None:
                self._status_label.setText("Adapter unavailable.")
                self._btn_dry_run.setEnabled(True)
                self._btn_run.setEnabled(True)
                return
            self._run_thread = QThread()
            self._run_worker = _RunWorker(self._adapter, dry_run=dry_run, mode=self._mode)
            self._run_worker.moveToThread(self._run_thread)
            self._run_thread.started.connect(self._run_worker.run)
            self._run_worker.result.connect(self._on_run_result)
            self._run_worker.error.connect(self._on_run_error)
            self._run_worker.result.connect(self._run_thread.quit)
            self._run_worker.error.connect(self._run_thread.quit)
            self._run_thread.start()

        def _on_run_result(self, res: dict):
            items = res.get("knowledge_items_count", 0)
            srcs = res.get("sources_count", 0)
            dry = " (dry run)" if res.get("dry_run") else ""
            self._status_label.setText(
                f"Done{dry}: {srcs} sources, {items} items extracted."
            )
            self._btn_dry_run.setEnabled(True)
            self._btn_run.setEnabled(True)
            self.refresh()

        def _on_run_error(self, err: str):
            self._status_label.setText(f"Error: {err}")
            self._btn_dry_run.setEnabled(True)
            self._btn_run.setEnabled(True)

        def _on_report(self):
            self._status_label.setText("Generating report…")
            self._btn_report.setEnabled(False)
            if self._adapter is None:
                self._status_label.setText("Adapter unavailable.")
                self._btn_report.setEnabled(True)
                return
            self._report_thread = QThread()
            self._report_worker = _ReportWorker(self._adapter, mode=self._mode)
            self._report_worker.moveToThread(self._report_thread)
            self._report_thread.started.connect(self._report_worker.run)
            self._report_worker.result.connect(self._on_report_result)
            self._report_worker.error.connect(self._on_report_error)
            self._report_worker.result.connect(self._report_thread.quit)
            self._report_worker.error.connect(self._report_thread.quit)
            self._report_thread.start()

        def _on_report_result(self, res: dict):
            path = res.get("report_path", "")
            if res.get("ok"):
                self._status_label.setText(f"Report: {path}")
            else:
                self._status_label.setText(f"Report error: {res.get('error', '?')}")
            self._btn_report.setEnabled(True)

        def _on_report_error(self, err: str):
            self._status_label.setText(f"Report error: {err}")
            self._btn_report.setEnabled(True)

        # ------------------------------------------------------------------
        # Close event — clean up threads
        # ------------------------------------------------------------------

        def closeEvent(self, event):
            for thread in [self._run_thread, self._report_thread]:
                if thread is not None and thread.isRunning():
                    thread.quit()
                    thread.wait(2000)
            super().closeEvent(event)
