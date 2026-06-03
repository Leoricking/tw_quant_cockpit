"""
gui/gui_navigation_panel.py — GUINavigationPanel for TW Quant Cockpit v0.5.2.

GUI tab with registry table, search, favorites & recent, audit log,
and report generation.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# PySide6 guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
        QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
        QLineEdit, QPushButton, QListWidget, QSizePolicy, QSplitter,
        QFrame, QGroupBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("GUINavigationPanel: PySide6 not available — stub mode")

    class QWidget:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QThread:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class Signal:  # type: ignore[no-redef]
        def __init__(self, *a):
            pass


_SAFETY_TEXT = (
    "GUI Tab Grouping / Navigation Polish  |  "
    "GUI UX Only  |  Research Only  |  No Real Orders  |  Production Trading BLOCKED"
)


# ---------------------------------------------------------------------------
# Background worker: load registry
# ---------------------------------------------------------------------------

class _NavRegistryWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Load GUITabRegistry in background thread."""

    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)

    def run(self) -> None:
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg     = GUITabRegistry()
            data    = GUINavigationReportData(registry=reg)
            summary = data.build_summary()
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(summary)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Background worker: generate report
# ---------------------------------------------------------------------------

class _NavReportWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Generate GUINavigationReport in background thread."""

    if _PYSIDE6_AVAILABLE:
        finished = Signal(str)
        error    = Signal(str)

    def __init__(self, report_dir: str = "reports", parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._report_dir = report_dir

    def run(self) -> None:
        try:
            from reports.gui_navigation_report import GUINavigationReport
            rpt  = GUINavigationReport(report_dir=self._report_dir, mode="real")
            path = rpt.generate(mode="real")
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(path)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class GUINavigationPanel(QWidget):
    """GUI Navigation panel for TW Quant Cockpit v0.5.2.

    Sub-tabs: Group Table | Tab Registry | Search | Favorites & Recent | Audit Log

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._log_lines: list[str] = []
            self._registry_worker: _NavRegistryWorker | None = None
            self._report_worker: _NavReportWorker | None = None
            self._build_ui()
            self._load_data()
        else:
            logger.warning("GUINavigationPanel: PySide6 not available — stub mode")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)

        # Safety banner
        banner = QLabel(_SAFETY_TEXT)
        banner.setStyleSheet(
            "background: #1a1a2e; color: #e06c75; font-weight: bold; "
            "font-size: 11px; padding: 4px 8px; border-radius: 3px;"
        )
        root.addWidget(banner)

        # Summary cards row
        cards_row = QHBoxLayout()
        self._card_tabs    = self._make_card("Total Tabs", "—")
        self._card_groups  = self._make_card("Groups", "—")
        self._card_favs    = self._make_card("Favorites", "0")
        self._card_recent  = self._make_card("Recent", "0")
        self._card_search  = self._make_card("Search Results", "—")
        self._card_safety  = self._make_card("Safety Status", "PASS")
        for card in (
            self._card_tabs, self._card_groups, self._card_favs,
            self._card_recent, self._card_search, self._card_safety,
        ):
            cards_row.addWidget(card)
        root.addLayout(cards_row)

        # Sub-tabs
        sub_tabs = QTabWidget()
        sub_tabs.addTab(self._build_group_tab(),    "Group Table")
        sub_tabs.addTab(self._build_registry_tab(), "Tab Registry")
        sub_tabs.addTab(self._build_search_tab(),   "Search")
        sub_tabs.addTab(self._build_fav_recent_tab(), "Favorites & Recent")
        sub_tabs.addTab(self._build_audit_tab(),    "Audit Log")
        root.addWidget(sub_tabs, stretch=1)

        # Actions row
        actions = QHBoxLayout()
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self._load_data)
        btn_report  = QPushButton("Generate Report")
        btn_report.clicked.connect(self._generate_report)
        btn_open    = QPushButton("Open Latest Report")
        btn_open.clicked.connect(self._open_latest_report)
        btn_reset   = QPushButton("Reset Navigation State")
        btn_reset.clicked.connect(self._reset_nav_state)
        for btn in (btn_refresh, btn_report, btn_open, btn_reset):
            actions.addWidget(btn)
        actions.addStretch()
        root.addLayout(actions)

    def _make_card(self, title: str, value: str) -> QWidget:
        """Create a small summary card widget."""
        if not _PYSIDE6_AVAILABLE:
            return QWidget()
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet(
            "QFrame { background: #1e1e2e; border: 1px solid #444; border-radius: 4px; padding: 4px; }"
        )
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setMaximumHeight(60)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(6, 4, 6, 4)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #888; font-size: 10px;")
        lbl_val   = QLabel(value)
        lbl_val.setStyleSheet("color: #cdd6f4; font-size: 14px; font-weight: bold;")
        lbl_val.setObjectName(f"card_val_{title.replace(' ', '_').lower()}")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        return card

    def _build_group_tab(self) -> QWidget:
        """Build Group Table sub-tab."""
        w = QWidget()
        if not _PYSIDE6_AVAILABLE:
            return w
        lay = QVBoxLayout(w)
        self._group_table = QTableWidget(0, 4)
        self._group_table.setHorizontalHeaderLabels(["Group", "Tabs", "P0/P1", "Description"])
        self._group_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._group_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._group_table.setAlternatingRowColors(True)
        lay.addWidget(self._group_table)
        return w

    def _build_registry_tab(self) -> QWidget:
        """Build Tab Registry sub-tab."""
        w = QWidget()
        if not _PYSIDE6_AVAILABLE:
            return w
        lay = QVBoxLayout(w)
        self._registry_table = QTableWidget(0, 7)
        self._registry_table.setHorizontalHeaderLabels(
            ["Tab", "Group", "Priority", "Description", "Related CLI", "Safety", "Maturity"]
        )
        self._registry_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._registry_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._registry_table.setAlternatingRowColors(True)
        lay.addWidget(self._registry_table)
        return w

    def _build_search_tab(self) -> QWidget:
        """Build Search sub-tab."""
        w = QWidget()
        if not _PYSIDE6_AVAILABLE:
            return w
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search tabs by keyword, group, CLI command...")
        self._search_input.returnPressed.connect(self._do_search)
        row.addWidget(self._search_input)
        btn = QPushButton("Search")
        btn.clicked.connect(self._do_search)
        row.addWidget(btn)
        lay.addLayout(row)
        self._search_results_table = QTableWidget(0, 5)
        self._search_results_table.setHorizontalHeaderLabels(
            ["Tab", "Group", "Priority", "Description", "Keywords"]
        )
        self._search_results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._search_results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._search_results_table.setAlternatingRowColors(True)
        lay.addWidget(self._search_results_table)
        return w

    def _build_fav_recent_tab(self) -> QWidget:
        """Build Favorites & Recent sub-tab."""
        w = QWidget()
        if not _PYSIDE6_AVAILABLE:
            return w
        lay = QHBoxLayout(w)

        fav_group = QGroupBox("Favorites")
        fav_lay = QVBoxLayout(fav_group)
        self._fav_list = QListWidget()
        fav_lay.addWidget(self._fav_list)
        lay.addWidget(fav_group)

        rec_group = QGroupBox("Recently Used")
        rec_lay = QVBoxLayout(rec_group)
        self._recent_list = QListWidget()
        rec_lay.addWidget(self._recent_list)
        lay.addWidget(rec_group)

        return w

    def _build_audit_tab(self) -> QWidget:
        """Build Audit Log sub-tab."""
        w = QWidget()
        if not _PYSIDE6_AVAILABLE:
            return w
        lay = QVBoxLayout(w)
        self._audit_log = QTextEdit()
        self._audit_log.setReadOnly(True)
        self._audit_log.setStyleSheet("font-family: monospace; font-size: 11px;")
        lay.addWidget(self._audit_log)
        return w

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self) -> None:
        """Start background load of registry data."""
        if not _PYSIDE6_AVAILABLE:
            return
        self._log("Loading GUI navigation registry...")
        self._registry_worker = _NavRegistryWorker(self)
        self._registry_worker.finished.connect(self._on_registry_loaded)
        self._registry_worker.error.connect(self._on_registry_error)
        self._registry_worker.start()

    def _on_registry_loaded(self, summary: dict) -> None:
        """Handle registry load completion."""
        if not _PYSIDE6_AVAILABLE:
            return
        self._log(
            f"Registry loaded: {summary.get('total_tabs', 0)} tabs, "
            f"{summary.get('groups_count', 0)} groups"
        )
        self._update_cards(summary)
        self._populate_group_table()
        self._populate_registry_table()
        self._populate_fav_recent()

    def _on_registry_error(self, error_msg: str) -> None:
        self._log(f"ERROR loading registry: {error_msg}")

    def _update_cards(self, summary: dict) -> None:
        """Update summary card values."""
        if not _PYSIDE6_AVAILABLE:
            return
        self._set_card_val(self._card_tabs,   str(summary.get("total_tabs",   0)))
        self._set_card_val(self._card_groups, str(summary.get("groups_count", 0)))
        self._set_card_val(self._card_safety, str(summary.get("safety_status", "PASS")))

    def _set_card_val(self, card: QWidget, value: str) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        # Find the QLabel with object name "card_val_*"
        for child in card.findChildren(QLabel):
            if child.objectName().startswith("card_val_"):
                child.setText(value)
                return

    def _populate_group_table(self) -> None:
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_group_table"):
            return
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg     = GUITabRegistry()
            data    = GUINavigationReportData(registry=reg)
            rows    = data.build_group_table()

            tbl = self._group_table
            tbl.setRowCount(len(rows))
            for r_idx, row in enumerate(rows):
                tbl.setItem(r_idx, 0, QTableWidgetItem(row.get("group", "")))
                tbl.setItem(r_idx, 1, QTableWidgetItem(str(row.get("tab_count", 0))))
                tbl.setItem(r_idx, 2, QTableWidgetItem(
                    f"P0:{row.get('p0_count',0)} P1:{row.get('p1_count',0)}"
                ))
                tbl.setItem(r_idx, 3, QTableWidgetItem(row.get("description", "")))
        except Exception as exc:
            self._log(f"Group table error: {exc}")

    def _populate_registry_table(self) -> None:
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_registry_table"):
            return
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg  = GUITabRegistry()
            data = GUINavigationReportData(registry=reg)
            rows = data.build_tab_table()

            tbl = self._registry_table
            tbl.setRowCount(len(rows))
            for r_idx, row in enumerate(rows):
                tbl.setItem(r_idx, 0, QTableWidgetItem(row.get("tab", "")))
                tbl.setItem(r_idx, 1, QTableWidgetItem(row.get("group", "")))
                tbl.setItem(r_idx, 2, QTableWidgetItem(row.get("priority", "")))
                tbl.setItem(r_idx, 3, QTableWidgetItem(row.get("description", "")[:80]))
                tbl.setItem(r_idx, 4, QTableWidgetItem(row.get("related_cli", "")))
                tbl.setItem(r_idx, 5, QTableWidgetItem(row.get("safety", "")))
                tbl.setItem(r_idx, 6, QTableWidgetItem(row.get("maturity", "")))
        except Exception as exc:
            self._log(f"Registry table error: {exc}")

    def _populate_fav_recent(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            from gui.navigation.navigation_state import NavigationState
            state = NavigationState()
            state.load()
            favs   = state.get_favorites()
            recent = state.get_recent_tabs()

            self._set_card_val(self._card_favs,   str(len(favs)))
            self._set_card_val(self._card_recent,  str(len(recent)))

            if hasattr(self, "_fav_list"):
                self._fav_list.clear()
                for tid in favs:
                    self._fav_list.addItem(tid)
            if hasattr(self, "_recent_list"):
                self._recent_list.clear()
                for tid in recent:
                    self._recent_list.addItem(tid)
        except Exception as exc:
            self._log(f"Fav/Recent load error: {exc}")

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _do_search(self) -> None:
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_search_input"):
            return
        query = self._search_input.text().strip()
        self._log(f"Search: '{query}'")
        try:
            from gui.navigation.tab_search import GUITabSearch
            searcher = GUITabSearch()
            results  = searcher.search(query)
            self._set_card_val(self._card_search, str(len(results)))

            tbl = self._search_results_table
            tbl.setRowCount(len(results))
            for r_idx, t in enumerate(results):
                tbl.setItem(r_idx, 0, QTableWidgetItem(t.get("display_name", t.get("tab_id", ""))))
                tbl.setItem(r_idx, 1, QTableWidgetItem(t.get("group", "")))
                tbl.setItem(r_idx, 2, QTableWidgetItem(t.get("priority", "")))
                tbl.setItem(r_idx, 3, QTableWidgetItem(t.get("description", "")[:80]))
                tbl.setItem(r_idx, 4, QTableWidgetItem(", ".join(t.get("keywords", []))))
        except Exception as exc:
            self._log(f"Search error: {exc}")

    # ------------------------------------------------------------------
    # Report actions
    # ------------------------------------------------------------------

    def _generate_report(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        self._log("Generating GUI navigation report...")
        self._report_worker = _NavReportWorker(
            report_dir=os.path.join(BASE_DIR, "reports"), parent=self
        )
        self._report_worker.finished.connect(self._on_report_done)
        self._report_worker.error.connect(self._on_report_error)
        self._report_worker.start()

    def _on_report_done(self, path: str) -> None:
        self._log(f"Report generated: {path}")

    def _on_report_error(self, error_msg: str) -> None:
        self._log(f"ERROR generating report: {error_msg}")

    def _open_latest_report(self) -> None:
        """Open the latest gui_navigation_report_*.md in default viewer."""
        if not _PYSIDE6_AVAILABLE:
            return
        reports_dir = os.path.join(BASE_DIR, "reports")
        import glob
        pattern = os.path.join(reports_dir, "gui_navigation_report_*.md")
        matches = sorted(glob.glob(pattern))
        if not matches:
            self._log("No GUI navigation report found. Generate one first.")
            return
        latest = matches[-1]
        self._log(f"Opening: {latest}")
        try:
            if sys.platform == "win32":
                os.startfile(latest)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", latest])
        except Exception as exc:
            self._log(f"Could not open report: {exc}")

    def _reset_nav_state(self) -> None:
        """Reset navigation state (favorites, recent)."""
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            from gui.navigation.navigation_state import NavigationState
            state = NavigationState()
            state._state = {"favorites": [], "recent": [], "saved_at": ""}
            state.save()
            self._log("Navigation state reset.")
            self._populate_fav_recent()
        except Exception as exc:
            self._log(f"Reset state error: {exc}")

    # ------------------------------------------------------------------
    # Audit log helpers
    # ------------------------------------------------------------------

    def _log(self, message: str) -> None:
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {message}"
        self._log_lines.append(line)
        logger.debug(line)
        if _PYSIDE6_AVAILABLE and hasattr(self, "_audit_log"):
            self._audit_log.append(line)
