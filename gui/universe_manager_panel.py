"""
gui/universe_manager_panel.py - Universe Manager Panel (v0.3.25).

PySide6 GUI panel for Universe Expansion & Sector Classification.

[!] Research Only. No Real Orders. No strategy change. No weight change.
[!] Research Universe Only.
"""

from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Graceful stub when PySide6 is unavailable
# ---------------------------------------------------------------------------
try:
    from PySide6.QtCore import Qt, QThread, Signal, Slot
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QApplication,
        QComboBox,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSplitter,
        QStackedWidget,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

    class QWidget:  # type: ignore
        pass

    class Signal:  # type: ignore
        def __init__(self, *a, **k):
            pass
        def emit(self, *a):
            pass
        def connect(self, *a):
            pass

    class QThread:  # type: ignore
        pass

    logger.warning("PySide6 not available — UniverseManagerPanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:

    class _BuildDefaultsWorker(QThread):
        """Background worker: build default universe configs."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, force: bool = False, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._force   = force

        def run(self):
            try:
                result = self._adapter.build_default_universes(force=self._force)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _AnalyzeQualityWorker(QThread):
        """Background worker: analyze universe quality."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, universe_name: str, parent=None):
            super().__init__(parent)
            self._adapter       = adapter
            self._universe_name = universe_name

        def run(self):
            try:
                result = self._adapter.analyze_universe_quality(self._universe_name)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _GenerateReportWorker(QThread):
        """Background worker: generate universe expansion report."""

        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, adapter, universe_name: str, parent=None):
            super().__init__(parent)
            self._adapter       = adapter
            self._universe_name = universe_name

        def run(self):
            try:
                path = self._adapter.generate_report(universe_name=self._universe_name)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class _LoadUniverseWorker(QThread):
        """Background worker: load universe rows."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, universe_name: str, parent=None):
            super().__init__(parent)
            self._adapter       = adapter
            self._universe_name = universe_name

        def run(self):
            try:
                result = self._adapter.load_universe(self._universe_name)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

if _PYSIDE6_AVAILABLE:

    class UniverseManagerPanel(QWidget):
        """
        Universe Manager Panel — Universe Expansion & Sector Classification.

        Safety invariants:
        - read_only = True
        - no_real_orders = True
        - production_blocked = True
        - no strategy changes
        - no weight changes
        """

        read_only         = True
        no_real_orders    = True
        production_blocked = True

        # Signals for parent dashboard integration
        status_message    = Signal(str)
        report_generated  = Signal(str)

        # Universe table columns
        _COLUMNS = [
            "Symbol", "Name", "Sector", "Theme Primary", "Theme Secondary",
            "Supply Chain Role", "Data Coverage", "AI Exposure",
            "Liquidity Tier", "Notes",
        ]

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode    = mode
            self._adapter = self._make_adapter()
            self._workers: list = []
            self._current_universe: str = "core_50"
            self._universe_data: dict = {}
            self._quality_data:  dict = {}

            self._build_ui()
            self._refresh_universe_list()

        # ------------------------------------------------------------------
        # Adapter factory
        # ------------------------------------------------------------------

        def _make_adapter(self):
            try:
                from gui.universe_manager_adapter import UniverseManagerAdapter
                return UniverseManagerAdapter()
            except Exception as exc:
                logger.error("UniverseManagerAdapter unavailable: %s", exc)
                return None

        # ------------------------------------------------------------------
        # UI construction
        # ------------------------------------------------------------------

        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            root.addWidget(self._make_safety_banner())
            root.addWidget(self._make_toolbar())

            splitter = QSplitter(Qt.Vertical)
            splitter.addWidget(self._make_top_section())
            splitter.addWidget(self._make_quality_section())
            splitter.setSizes([400, 200])
            root.addWidget(splitter)

            root.addWidget(self._make_action_bar())

        def _make_safety_banner(self) -> QLabel:
            banner = QLabel(
                "[!] Research Universe Only  |  Read Only  |  No Real Orders  |  "
                "Not Investment Advice  |  Production BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background-color: #1a1a2e; color: #e0e0e0; font-weight: bold; "
                "padding: 6px; border-radius: 4px; font-size: 11px;"
            )
            return banner

        def _make_toolbar(self) -> QWidget:
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)

            layout.addWidget(QLabel("Universe:"))

            self._universe_combo = QComboBox()
            self._universe_combo.setMinimumWidth(180)
            self._universe_combo.currentTextChanged.connect(self._on_universe_changed)
            layout.addWidget(self._universe_combo)

            self._count_label = QLabel("Symbols: —")
            layout.addWidget(self._count_label)

            self._readiness_label = QLabel("Readiness: —")
            self._readiness_label.setStyleSheet("font-weight: bold;")
            layout.addWidget(self._readiness_label)

            layout.addStretch()
            return w

        def _make_top_section(self) -> QWidget:
            w = QWidget()
            layout = QVBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)

            # Stack: empty state vs table
            self._stack = QStackedWidget()

            # Empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            self._empty_label = QLabel(
                "No universe configuration found.\n"
                "Click Build Default Universes to generate safe research universes."
            )
            self._empty_label.setAlignment(Qt.AlignCenter)
            self._empty_label.setStyleSheet("color: #888; font-size: 13px;")
            empty_layout.addWidget(self._empty_label)
            self._stack.addWidget(empty_widget)

            # Table
            self._universe_table = QTableWidget(0, len(self._COLUMNS))
            self._universe_table.setHorizontalHeaderLabels(self._COLUMNS)
            self._universe_table.horizontalHeader().setStretchLastSection(True)
            self._universe_table.setAlternatingRowColors(True)
            self._universe_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._universe_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._stack.addWidget(self._universe_table)

            layout.addWidget(self._stack)

            # Sector summary below table
            self._sector_label = QLabel("Sector distribution: —")
            self._sector_label.setWordWrap(True)
            self._sector_label.setStyleSheet("color: #aaa; font-size: 11px; padding: 4px;")
            layout.addWidget(self._sector_label)

            return w

        def _make_quality_section(self) -> QWidget:
            group = QGroupBox("Universe Quality")
            layout = QHBoxLayout(group)
            layout.setSpacing(8)

            card_defs = [
                ("Coverage",            "coverage_score"),
                ("Freshness",           "freshness_score"),
                ("Provider Reliability","provider_reliability_score"),
                ("Sector Balance",      "sector_balance_score"),
                ("Backtest Readiness",  "backtest_sample_readiness_score"),
                ("Overall Score",       "overall_universe_score"),
            ]
            self._quality_cards: dict = {}
            for label, key in card_defs:
                card = self._make_quality_card(label)
                layout.addWidget(card["widget"])
                self._quality_cards[key] = card

            return group

        def _make_quality_card(self, title: str) -> dict:
            card_widget = QGroupBox(title)
            card_widget.setMinimumWidth(100)
            card_layout = QVBoxLayout(card_widget)
            score_label = QLabel("—")
            score_label.setAlignment(Qt.AlignCenter)
            score_label.setFont(QFont("Arial", 18, QFont.Bold))
            card_layout.addWidget(score_label)
            level_label = QLabel("")
            level_label.setAlignment(Qt.AlignCenter)
            level_label.setStyleSheet("font-size: 10px; color: #aaa;")
            card_layout.addWidget(level_label)
            return {"widget": card_widget, "score": score_label, "level": level_label}

        def _make_action_bar(self) -> QWidget:
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)

            btn_load = QPushButton("Load Universe")
            btn_load.clicked.connect(self._on_load_universe)
            layout.addWidget(btn_load)

            btn_build = QPushButton("Build Default Universes")
            btn_build.clicked.connect(self._on_build_defaults)
            layout.addWidget(btn_build)

            btn_analyze = QPushButton("Analyze Universe Quality")
            btn_analyze.clicked.connect(self._on_analyze_quality)
            layout.addWidget(btn_analyze)

            btn_report = QPushButton("Generate Universe Report")
            btn_report.clicked.connect(self._on_generate_report)
            layout.addWidget(btn_report)

            btn_manifest = QPushButton("Export Manifest")
            btn_manifest.clicked.connect(self._on_export_manifest)
            layout.addWidget(btn_manifest)

            layout.addStretch()

            self._status_bar = QLabel("Ready")
            self._status_bar.setStyleSheet("color: #888; font-size: 11px;")
            layout.addWidget(self._status_bar)

            return w

        # ------------------------------------------------------------------
        # Universe list refresh
        # ------------------------------------------------------------------

        def _refresh_universe_list(self):
            if not self._adapter:
                return
            try:
                universes = self._adapter.list_universes()
                self._universe_combo.blockSignals(True)
                self._universe_combo.clear()
                for u in universes:
                    self._universe_combo.addItem(u["name"])
                # Default to core_50 if available
                idx = self._universe_combo.findText("core_50")
                if idx >= 0:
                    self._universe_combo.setCurrentIndex(idx)
                self._universe_combo.blockSignals(False)
                self._current_universe = self._universe_combo.currentText()
            except Exception as exc:
                logger.error("_refresh_universe_list: %s", exc)

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------

        def _on_universe_changed(self, name: str):
            self._current_universe = name

        def _on_load_universe(self):
            if not self._adapter:
                self._set_status("Adapter not available")
                return
            name = self._current_universe
            if not name:
                return
            self._set_status(f"Loading {name}...")
            worker = _LoadUniverseWorker(self._adapter, name, parent=self)
            worker.finished.connect(self._on_load_universe_done)
            worker.error.connect(self._on_worker_error)
            self._workers.append(worker)
            worker.start()

        def _on_load_universe_done(self, result: dict):
            self._universe_data = result
            rows = result.get("rows", [])
            if not rows:
                self._stack.setCurrentIndex(0)
                self._count_label.setText("Symbols: 0")
                self._readiness_label.setText("Readiness: INSUFFICIENT")
                self._set_status("Universe empty or not found. Build defaults first.")
                return

            self._stack.setCurrentIndex(1)
            self._populate_table(rows)
            self._update_sector_label(result.get("sector_summary", {}))
            n = len(rows)
            self._count_label.setText(f"Symbols: {n}")
            readiness = "RESEARCH_READY" if n >= 50 else "OBSERVATIONAL" if n >= 30 else "INSUFFICIENT"
            self._readiness_label.setText(f"Readiness: {readiness}")
            self._set_status(f"Loaded {n} symbols from {result.get('universe_name', '?')}")

        def _on_build_defaults(self):
            if not self._adapter:
                self._set_status("Adapter not available")
                return
            self._set_status("Building default universes...")
            worker = _BuildDefaultsWorker(self._adapter, force=False, parent=self)
            worker.finished.connect(self._on_build_defaults_done)
            worker.error.connect(self._on_worker_error)
            self._workers.append(worker)
            worker.start()

        def _on_build_defaults_done(self, result: dict):
            if "error" in result:
                self._set_status(f"Build failed: {result['error']}")
                return
            n = len([k for k in result if k != "manifest"])
            self._set_status(f"Built {n} universe config(s). Refreshing...")
            self._refresh_universe_list()
            self._on_load_universe()

        def _on_analyze_quality(self):
            if not self._adapter:
                self._set_status("Adapter not available")
                return
            name = self._current_universe
            self._set_status(f"Analyzing quality for {name}...")
            worker = _AnalyzeQualityWorker(self._adapter, name, parent=self)
            worker.finished.connect(self._on_analyze_quality_done)
            worker.error.connect(self._on_worker_error)
            self._workers.append(worker)
            worker.start()

        def _on_analyze_quality_done(self, result: dict):
            self._quality_data = result
            self._update_quality_cards(result)
            score   = result.get("overall_universe_score", 0)
            level   = result.get("readiness_level", "INSUFFICIENT")
            self._set_status(f"Quality analysis complete: {score} ({level})")

        def _on_generate_report(self):
            if not self._adapter:
                self._set_status("Adapter not available")
                return
            name = self._current_universe
            self._set_status(f"Generating universe report for {name}...")
            worker = _GenerateReportWorker(self._adapter, name, parent=self)
            worker.finished.connect(self._on_generate_report_done)
            worker.error.connect(self._on_worker_error)
            self._workers.append(worker)
            worker.start()

        def _on_generate_report_done(self, path: str):
            if path:
                self._set_status(f"Report generated: {path}")
                self.report_generated.emit(path)
            else:
                self._set_status("Report generation failed.")

        def _on_export_manifest(self):
            if not self._adapter:
                self._set_status("Adapter not available")
                return
            try:
                from universe.universe_registry import UniverseRegistry
                reg = UniverseRegistry()
                path = reg.export_universe_manifest()
                self._set_status(f"Manifest exported: {path}")
            except Exception as exc:
                self._set_status(f"Export manifest failed: {exc}")

        def _on_worker_error(self, msg: str):
            self._set_status(f"Error: {msg}")
            logger.error("Worker error: %s", msg)

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _populate_table(self, rows: List[dict]):
            col_keys = [
                "symbol", "name", "sector", "theme_primary", "theme_secondary",
                "supply_chain_role", "data_coverage", "ai_exposure",
                "liquidity_tier", "notes",
            ]
            self._universe_table.setRowCount(0)
            for row in rows:
                r = self._universe_table.rowCount()
                self._universe_table.insertRow(r)
                for c, key in enumerate(col_keys):
                    val = str(row.get(key, "") or "")
                    item = QTableWidgetItem(val)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    # Color ai_exposure
                    if key == "ai_exposure":
                        if val == "HIGH":
                            item.setForeground(QColor("#00c896"))
                        elif val == "MEDIUM":
                            item.setForeground(QColor("#f0a500"))
                        else:
                            item.setForeground(QColor("#aaaaaa"))
                    self._universe_table.setItem(r, c, item)
            self._universe_table.resizeColumnsToContents()

        # ------------------------------------------------------------------
        # Quality cards update
        # ------------------------------------------------------------------

        def _update_quality_cards(self, data: dict):
            level = data.get("readiness_level", "INSUFFICIENT")
            for key, card in self._quality_cards.items():
                val = data.get(key)
                if val is None:
                    card["score"].setText("—")
                    card["level"].setText("")
                    continue
                score_text = str(val)
                card["score"].setText(score_text)
                # Color code
                try:
                    fval = float(val)
                    if fval >= 75:
                        card["score"].setStyleSheet("color: #00c896; font-size: 18px; font-weight: bold;")
                    elif fval >= 60:
                        card["score"].setStyleSheet("color: #f0a500; font-size: 18px; font-weight: bold;")
                    else:
                        card["score"].setStyleSheet("color: #e74c3c; font-size: 18px; font-weight: bold;")
                except (ValueError, TypeError):
                    pass
                if key == "overall_universe_score":
                    card["level"].setText(level)

        # ------------------------------------------------------------------
        # Sector summary
        # ------------------------------------------------------------------

        def _update_sector_label(self, sector_summary: dict):
            if not sector_summary:
                self._sector_label.setText("Sector distribution: —")
                return
            by_sector = sector_summary.get("by_sector", {})
            total     = sector_summary.get("total", 0)
            parts = [f"{sec}: {cnt}" for sec, cnt in sorted(by_sector.items(), key=lambda x: -x[1])[:6]]
            conc  = sector_summary.get("concentration", 0)
            text  = f"Total: {total} | Concentration: {conc:.0%} | " + " | ".join(parts)
            self._sector_label.setText(text)

        # ------------------------------------------------------------------
        # Status
        # ------------------------------------------------------------------

        def _set_status(self, msg: str):
            self._status_bar.setText(msg)
            self.status_message.emit(msg)
            logger.info("[UniverseManagerPanel] %s", msg)

else:
    # ---------------------------------------------------------------------------
    # Stub class when PySide6 is not available
    # ---------------------------------------------------------------------------

    class UniverseManagerPanel:  # type: ignore
        """Stub: PySide6 not available."""

        read_only         = True
        no_real_orders    = True
        production_blocked = True

        def __init__(self, mode: str = "real", parent=None):
            logger.warning("UniverseManagerPanel: PySide6 not available — panel is a stub.")
            self._mode = mode

        def show(self):
            logger.warning("UniverseManagerPanel.show(): stub — PySide6 not installed.")
