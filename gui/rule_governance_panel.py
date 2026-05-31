"""
gui/rule_governance_panel.py — Rule Governance GUI panel (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
import logging

_LOG = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Guarded PySide6 import
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QMessageBox,
        QSizePolicy,
        QGroupBox,
        QFrame,
        QScrollArea,
        QAbstractItemView,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor

    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


# ---------------------------------------------------------------------------
# Stub when PySide6 is unavailable
# ---------------------------------------------------------------------------
if not _PYSIDE6_OK:
    class RuleGovernancePanel:  # type: ignore[no-redef]
        """
        Stub panel used when PySide6 is not installed.

        Safety invariants:
          read_only = True
          no_real_orders = True
          production_blocked = True
          Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
        """

        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, *args, **kwargs):
            _LOG.warning(
                "RuleGovernancePanel: PySide6 not available — panel disabled."
            )

# ---------------------------------------------------------------------------
# Full implementation when PySide6 is available
# ---------------------------------------------------------------------------
else:
    _SAFETY_TEXT = (
        "Strategy Rule Governance  |  Research Only  |  "
        "No Real Orders  |  No Auto Weight Apply  |  Production BLOCKED"
    )

    # -----------------------------------------------------------------------
    # Worker thread
    # -----------------------------------------------------------------------

    class _GovernanceWorker(QThread):
        """Runs governance pipeline in a background thread."""

        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.rule_governance_adapter import RuleGovernanceAdapter
                adapter = RuleGovernanceAdapter()
                result = adapter.run_governance(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                _LOG.warning("_GovernanceWorker error: %s", exc)
                self.error.emit(str(exc))

    # -----------------------------------------------------------------------
    # Main panel
    # -----------------------------------------------------------------------

    class RuleGovernancePanel(QWidget):
        """
        Full governance panel with summary cards, rule table, dependency
        table, and review queue.

        Safety invariants:
          read_only = True
          no_real_orders = True
          production_blocked = True
          Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
        """

        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._worker = None
            self._last_result: dict = {}
            self._build_ui()

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root_layout = QVBoxLayout(self)
            root_layout.setContentsMargins(8, 8, 8, 8)
            root_layout.setSpacing(6)

            # A. Safety banner
            banner = QLabel(_SAFETY_TEXT)
            banner.setAlignment(Qt.AlignCenter)
            banner_font = QFont()
            banner_font.setBold(True)
            banner.setFont(banner_font)
            banner.setStyleSheet(
                "background-color: #fff3cd; color: #856404; "
                "padding: 6px; border-radius: 4px; border: 1px solid #ffc107;"
            )
            root_layout.addWidget(banner)

            # B. Summary cards row
            cards_group = QGroupBox("Summary")
            cards_layout = QHBoxLayout(cards_group)
            cards_layout.setSpacing(8)

            self._card_total = self._make_card("Total Rules", "—")
            self._card_active = self._make_card("Active", "—")
            self._card_experimental = self._make_card("Experimental", "—")
            self._card_needs_review = self._make_card("Needs Review", "—")
            self._card_high_confidence = self._make_card("High Confidence", "—")
            self._card_unknown = self._make_card("Unknown Confidence", "—")

            for card in (
                self._card_total,
                self._card_active,
                self._card_experimental,
                self._card_needs_review,
                self._card_high_confidence,
                self._card_unknown,
            ):
                cards_layout.addWidget(card)

            root_layout.addWidget(cards_group)

            # C. Rule Table
            rule_group = QGroupBox("All Rules")
            rule_layout = QVBoxLayout(rule_group)
            self._rule_table = QTableWidget()
            self._rule_table.setColumnCount(10)
            self._rule_table.setHorizontalHeaderLabels([
                "Rule ID", "Name", "Category", "Version", "Status",
                "Enabled", "Experimental", "Confidence", "Sample Count", "Timeframe",
            ])
            self._rule_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeToContents
            )
            self._rule_table.setEditTriggers(
                QAbstractItemView.NoEditTriggers
            )
            self._rule_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._rule_table.setAlternatingRowColors(True)
            rule_layout.addWidget(self._rule_table)
            root_layout.addWidget(rule_group)

            # D. Dependency Table
            dep_group = QGroupBox("Dependency Graph")
            dep_layout = QVBoxLayout(dep_group)
            self._dep_table = QTableWidget()
            self._dep_table.setColumnCount(4)
            self._dep_table.setHorizontalHeaderLabels([
                "Rule", "Depends On (count)", "Dependent Count", "Cycle Warning",
            ])
            self._dep_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeToContents
            )
            self._dep_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self._dep_table.setAlternatingRowColors(True)
            dep_layout.addWidget(self._dep_table)
            root_layout.addWidget(dep_group)

            # E. Review Queue
            review_group = QGroupBox("Review Queue")
            review_layout = QVBoxLayout(review_group)
            self._review_table = QTableWidget()
            self._review_table.setColumnCount(4)
            self._review_table.setHorizontalHeaderLabels([
                "Rule", "Reason", "Severity", "Recommended Action",
            ])
            self._review_table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeToContents
            )
            self._review_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self._review_table.setAlternatingRowColors(True)
            review_layout.addWidget(self._review_table)
            root_layout.addWidget(review_group)

            # F. Action buttons
            btn_layout = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh Governance")
            self._btn_report = QPushButton("Generate Report")
            self._btn_snapshot = QPushButton("Export Snapshot")

            self._btn_refresh.clicked.connect(self._refresh)
            self._btn_report.clicked.connect(self._generate_report)
            self._btn_snapshot.clicked.connect(self._export_snapshot)

            btn_layout.addWidget(self._btn_refresh)
            btn_layout.addWidget(self._btn_report)
            btn_layout.addWidget(self._btn_snapshot)
            btn_layout.addStretch()

            root_layout.addLayout(btn_layout)

        # ------------------------------------------------------------------
        # Card helper
        # ------------------------------------------------------------------

        @staticmethod
        def _make_card(title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet(
                "background-color: #f8f9fa; border: 1px solid #dee2e6; "
                "border-radius: 4px; padding: 4px;"
            )
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(6, 4, 6, 4)
            title_lbl = QLabel(title)
            title_lbl.setAlignment(Qt.AlignCenter)
            title_font = QFont()
            title_font.setPointSize(8)
            title_lbl.setFont(title_font)
            value_lbl = QLabel(value)
            value_lbl.setAlignment(Qt.AlignCenter)
            value_font = QFont()
            value_font.setBold(True)
            value_font.setPointSize(14)
            value_lbl.setFont(value_font)
            layout.addWidget(title_lbl)
            layout.addWidget(value_lbl)
            # Store reference for updating
            frame.setProperty("_value_label", value_lbl)
            return frame

        @staticmethod
        def _set_card_value(card: QFrame, value: str):
            lbl = card.property("_value_label")
            if lbl is not None:
                lbl.setText(value)

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _refresh(self):
            """Start background governance run."""
            self._btn_refresh.setEnabled(False)
            self._btn_refresh.setText("Running…")

            self._worker = _GovernanceWorker(mode=self._mode)
            self._worker.finished.connect(self._on_governance_done)
            self._worker.error.connect(self._on_governance_error)
            self._worker.start()

        def _on_governance_done(self, result: dict):
            self._last_result = result
            self._btn_refresh.setEnabled(True)
            self._btn_refresh.setText("Refresh Governance")

            summary = result.get("registry_summary", {})
            self._update_summary_cards(summary)

            confidence_result = result.get("confidence_result", {})
            rules = self._build_rules_display(result)
            self._update_rule_table(rules)

            edges = result.get("dependency_edges", [])
            self._update_dependency_table(edges)

            review_queue = result.get("review_queue", [])
            self._update_review_queue(review_queue)

            # Update high confidence card
            high_count = len(confidence_result.get("high_confidence", []))
            self._set_card_value(self._card_high_confidence, str(high_count))
            unknown_count = len(confidence_result.get("unknown_confidence", []))
            self._set_card_value(self._card_unknown, str(unknown_count))

        def _on_governance_error(self, msg: str):
            self._btn_refresh.setEnabled(True)
            self._btn_refresh.setText("Refresh Governance")
            _LOG.warning("RuleGovernancePanel: governance error: %s", msg)
            QMessageBox.warning(
                self, "Governance Error",
                f"Failed to run governance:\n{msg}"
            )

        def _generate_report(self):
            """Generate Markdown report in background thread."""
            self._btn_report.setEnabled(False)
            self._btn_report.setText("Generating…")

            class _ReportWorker(QThread):
                done = Signal(str)
                err = Signal(str)

                def __init__(self, mode):
                    super().__init__()
                    self._mode = mode

                def run(self):
                    try:
                        from gui.rule_governance_adapter import RuleGovernanceAdapter
                        adapter = RuleGovernanceAdapter()
                        path = adapter.generate_report(mode=self._mode)
                        self.done.emit(path)
                    except Exception as exc:
                        self.err.emit(str(exc))

            worker = _ReportWorker(mode=self._mode)

            def _on_done(path):
                self._btn_report.setEnabled(True)
                self._btn_report.setText("Generate Report")
                if path:
                    QMessageBox.information(
                        self, "Report Generated", f"Report written to:\n{path}"
                    )
                else:
                    QMessageBox.warning(
                        self, "Report Error", "Report generation failed."
                    )

            def _on_err(msg):
                self._btn_report.setEnabled(True)
                self._btn_report.setText("Generate Report")
                QMessageBox.warning(self, "Report Error", f"Error:\n{msg}")

            worker.done.connect(_on_done)
            worker.err.connect(_on_err)
            # Keep reference
            self._report_worker = worker
            worker.start()

        def _export_snapshot(self):
            """Export snapshot in background thread."""
            self._btn_snapshot.setEnabled(False)
            self._btn_snapshot.setText("Exporting…")

            class _SnapshotWorker(QThread):
                done = Signal(dict)
                err = Signal(str)

                def run(self):
                    try:
                        from gui.rule_governance_adapter import RuleGovernanceAdapter
                        adapter = RuleGovernanceAdapter()
                        result = adapter.export_snapshot()
                        self.done.emit(result)
                    except Exception as exc:
                        self.err.emit(str(exc))

            worker = _SnapshotWorker()

            def _on_done(result):
                self._btn_snapshot.setEnabled(True)
                self._btn_snapshot.setText("Export Snapshot")
                if "error" in result:
                    QMessageBox.warning(
                        self, "Snapshot Error",
                        f"Export failed:\n{result['error']}"
                    )
                else:
                    msg = (
                        f"Snapshot: {result.get('snapshot_path', 'N/A')}\n"
                        f"Summary:  {result.get('summary_path', 'N/A')}"
                    )
                    QMessageBox.information(self, "Snapshot Exported", msg)

            def _on_err(msg):
                self._btn_snapshot.setEnabled(True)
                self._btn_snapshot.setText("Export Snapshot")
                QMessageBox.warning(self, "Snapshot Error", f"Error:\n{msg}")

            worker.done.connect(_on_done)
            worker.err.connect(_on_err)
            self._snapshot_worker = worker
            worker.start()

        # ------------------------------------------------------------------
        # Table update helpers
        # ------------------------------------------------------------------

        def _update_summary_cards(self, summary: dict):
            self._set_card_value(self._card_total, str(summary.get("total_rules", 0)))
            self._set_card_value(self._card_active, str(summary.get("active_count", 0)))
            self._set_card_value(
                self._card_experimental, str(summary.get("experimental_count", 0))
            )
            self._set_card_value(
                self._card_needs_review, str(summary.get("needs_review_count", 0))
            )

        def _update_rule_table(self, rules: list):
            self._rule_table.setRowCount(0)
            if not rules:
                self._rule_table.setRowCount(1)
                self._rule_table.setItem(
                    0, 0, QTableWidgetItem("No rules loaded")
                )
                return

            self._rule_table.setRowCount(len(rules))
            for row, r in enumerate(rules):
                self._rule_table.setItem(row, 0, QTableWidgetItem(str(r.get("rule_id", ""))))
                self._rule_table.setItem(row, 1, QTableWidgetItem(str(r.get("rule_name", ""))))
                self._rule_table.setItem(row, 2, QTableWidgetItem(str(r.get("category", ""))))
                self._rule_table.setItem(row, 3, QTableWidgetItem(str(r.get("version", ""))))
                self._rule_table.setItem(row, 4, QTableWidgetItem(str(r.get("status", ""))))
                self._rule_table.setItem(row, 5, QTableWidgetItem(str(r.get("enabled", ""))))
                self._rule_table.setItem(row, 6, QTableWidgetItem(str(r.get("experimental", ""))))
                self._rule_table.setItem(row, 7, QTableWidgetItem(str(r.get("confidence_level", ""))))
                self._rule_table.setItem(row, 8, QTableWidgetItem(str(r.get("sample_count", ""))))
                self._rule_table.setItem(row, 9, QTableWidgetItem(str(r.get("timeframe", ""))))

        def _update_dependency_table(self, edges: list):
            """Aggregate edges into per-rule stats and populate table."""
            self._dep_table.setRowCount(0)
            if not edges:
                self._dep_table.setRowCount(1)
                self._dep_table.setItem(0, 0, QTableWidgetItem("No dependency edges"))
                return

            # Aggregate
            dep_of: dict = {}  # rule_id -> set of rules it depends on
            dep_by: dict = {}  # rule_id -> set of rules that depend on it
            cycles_set = set(
                e.get("cycle", "") for e in edges if e.get("cycle")
            )

            for edge in edges:
                src = edge.get("from", "")
                dst = edge.get("to", "")
                if src:
                    dep_of.setdefault(src, set()).add(dst)
                if dst:
                    dep_by.setdefault(dst, set()).add(src)

            all_rules = sorted(set(dep_of.keys()) | set(dep_by.keys()))
            self._dep_table.setRowCount(len(all_rules))

            for row, rid in enumerate(all_rules):
                deps_count = len(dep_of.get(rid, set()))
                dep_count = len(dep_by.get(rid, set()))
                cycle_warn = "Yes" if rid in cycles_set else ""

                self._dep_table.setItem(row, 0, QTableWidgetItem(rid))
                self._dep_table.setItem(row, 1, QTableWidgetItem(str(deps_count)))
                self._dep_table.setItem(row, 2, QTableWidgetItem(str(dep_count)))
                self._dep_table.setItem(row, 3, QTableWidgetItem(cycle_warn))

        def _update_review_queue(self, rules: list):
            self._review_table.setRowCount(0)
            if not rules:
                self._review_table.setRowCount(1)
                self._review_table.setItem(
                    0, 0, QTableWidgetItem("No rules require review")
                )
                return

            self._review_table.setRowCount(len(rules))
            for row, item in enumerate(rules):
                self._review_table.setItem(
                    row, 0, QTableWidgetItem(str(item.get("rule_id", "")))
                )
                self._review_table.setItem(
                    row, 1, QTableWidgetItem(str(item.get("reason", "")))
                )
                self._review_table.setItem(
                    row, 2, QTableWidgetItem(str(item.get("severity", "")))
                )
                self._review_table.setItem(
                    row, 3, QTableWidgetItem(str(item.get("recommended_action", "")))
                )

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        @staticmethod
        def _build_rules_display(result: dict) -> list:
            """
            Build a list of rule dicts for display, merging confidence info.
            """
            try:
                from governance.rule_registry import RuleRegistry
                registry = RuleRegistry()
                registry.load_builtin_rules()
                rules = [r.to_dict() for r in registry.list_rules()]

                # Overlay confidence
                confidence_result = result.get("confidence_result", {})
                details = confidence_result.get("details", {})
                for r in rules:
                    rid = r.get("rule_id", "")
                    if rid in details:
                        r["confidence_level"] = details[rid].get(
                            "confidence_level", r.get("confidence_level", "")
                        )
                return rules
            except Exception as exc:
                _LOG.warning("_build_rules_display error: %s", exc)
                return []
