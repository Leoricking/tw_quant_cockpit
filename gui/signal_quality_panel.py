"""
gui/signal_quality_panel.py - Signal Quality Dashboard GUI panel (v0.3.14).

Displays consolidated signal quality results from all available backtests.

Sections:
  A. Header / Safety Banner
  B. Summary Cards — counts by recommendation type
  C. Recommendation Table — all signals with recommendation
  D. Group Quality Table — aggregated by signal group
  E. Rule Action Panel — BOOST / REDUCE / DISABLE / INSUFFICIENT lists
  F. Action buttons

Rules:
  - No order submission.
  - No automatic weight changes — recommendations are advisory only.
  - Empty state shown when no data exists — no crash.
  - Simulation Only / No Real Orders always visible.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTabWidget, QGroupBox, QFrame, QTextEdit, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — SignalQualityPanel will be stub.")

try:
    from gui.portfolio_widgets import (
        MetricCard, StatusBadge, RecommendationBadge,
        PortfolioTableView, EmptyStateWidget,
        _fmt_pct, _fmt_ratio,
    )
    from gui.signal_quality_data_adapter import SignalQualityDataAdapter
    _SQ_DEPS_OK = True
except Exception as _sq_exc:
    logger.warning("SignalQualityPanel deps unavailable: %s", _sq_exc)
    _SQ_DEPS_OK = False

_REC_COLORS = {
    "BOOST":               "#33CC66",
    "KEEP":                "#AAAAFF",
    "REDUCE":              "#FF8800",
    "DISABLE":             "#FF4444",
    "INSUFFICIENT_SAMPLE": "#888888",
}


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _SQWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Runs SignalQualityEngine in background thread."""

    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, adapter: "SignalQualityDataAdapter", mode: str):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self._adapter = adapter
        self._mode    = mode

    def run(self):
        try:
            result = self._adapter.run_signal_quality_engine(mode=self._mode)
            if _PYSIDE6_AVAILABLE:
                self.finished.emit(result)
        except Exception as exc:
            if _PYSIDE6_AVAILABLE:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Helper label factory
# ---------------------------------------------------------------------------

def _lbl(text: str, bold: bool = False, color: str = None, size: int = None) -> "QLabel":
    w = QLabel(text)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if size:
        parts.append(f"font-size:{size}px")
    if parts:
        w.setStyleSheet(";".join(parts))
    return w


# ---------------------------------------------------------------------------
# SignalQualityPanel
# ---------------------------------------------------------------------------

class SignalQualityPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Signal Quality Dashboard panel — embeds as a tab in CockpitWindow.
    """

    def __init__(self, mode: str = "mock", parent=None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._mode    = mode
        self._adapter = SignalQualityDataAdapter() if _SQ_DEPS_OK else None
        self._worker: Optional[_SQWorker] = None
        self._build_ui()
        self._load_data()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(4)

        root.addWidget(self._build_header())
        root.addWidget(self._build_buttons())

        self._status_lbl = QLabel("")
        self._status_lbl.setStyleSheet("color:#FF8800; font-size:11px;")
        root.addWidget(self._status_lbl)

        self._tabs = QTabWidget()
        _tab_style = (
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 12px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )
        self._tabs.setStyleSheet(_tab_style)
        root.addWidget(self._tabs, stretch=1)

        # B. Summary tab
        self._summary_tab = self._build_summary_tab()
        self._tabs.addTab(self._summary_tab, "Summary")

        # C. Recommendation table
        if _SQ_DEPS_OK:
            self._rec_view = PortfolioTableView("All Signal Recommendations")
        else:
            self._rec_view = QLabel("unavailable")
        self._tabs.addTab(self._rec_view, "Recommendations")

        # D. Group Quality table
        if _SQ_DEPS_OK:
            self._group_view = PortfolioTableView("Group Quality Summary")
        else:
            self._group_view = QLabel("unavailable")
        self._tabs.addTab(self._group_view, "Groups")

        # E. Rule Action panel
        self._action_tab = self._build_action_tab()
        self._tabs.addTab(self._action_tab, "Action List")

    def _build_header(self) -> QWidget:
        w = QFrame()
        w.setFrameShape(QFrame.StyledPanel)
        w.setStyleSheet("background:#0A1828; border:1px solid #335566; border-radius:4px;")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(3)

        title_row = QHBoxLayout()
        title_row.addWidget(_lbl("Signal Quality Dashboard", bold=True, color="#88CCFF", size=15))
        title_row.addStretch()
        mode_text  = "REAL" if self._mode == "real" else "MOCK"
        mode_color = "#FF8800" if self._mode == "real" else "#33CCFF"
        self._mode_badge = _lbl(f"Mode: {mode_text}", bold=True, color=mode_color, size=12)
        title_row.addWidget(self._mode_badge)
        layout.addLayout(title_row)

        safety_row = QHBoxLayout()
        safety_row.addWidget(_lbl("[ Simulation Only ]", bold=True, color="#FF4444", size=11))
        safety_row.addSpacing(12)
        safety_row.addWidget(_lbl("No Real Orders", bold=True, color="#FF4444", size=11))
        safety_row.addSpacing(12)
        safety_row.addWidget(_lbl(
            "Recommendations do not automatically change strategy weights",
            color="#FF8800", size=11
        ))
        safety_row.addStretch()
        if _SQ_DEPS_OK:
            self._conf_badge = StatusBadge("OBSERVATIONAL")
        else:
            self._conf_badge = QLabel("OBSERVATIONAL")
        safety_row.addWidget(_lbl("Confidence:", color="#AAAAAA", size=11))
        safety_row.addWidget(self._conf_badge)
        layout.addLayout(safety_row)
        return w

    def _build_buttons(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)
        _btn_style = (
            "QPushButton { background:#252545; color:#CCCCFF; border:1px solid #444466; "
            "border-radius:3px; padding:4px 10px; font-size:11px; } "
            "QPushButton:hover { background:#333366; } "
            "QPushButton:disabled { color:#555555; }"
        )
        self._btn_refresh = QPushButton("Refresh Signal Quality")
        self._btn_report  = QPushButton("Load Latest Report")
        self._btn_export  = QPushButton("Export Summary")
        for btn in [self._btn_refresh, self._btn_report, self._btn_export]:
            btn.setStyleSheet(_btn_style)
            layout.addWidget(btn)
        layout.addStretch()
        self._btn_refresh.clicked.connect(self._on_refresh)
        self._btn_report.clicked.connect(self._on_open_report)
        self._btn_export.clicked.connect(self._on_export)
        return w

    def _build_summary_tab(self) -> QWidget:
        """B. Summary Cards + E. Rule action overview."""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        if _SQ_DEPS_OK:
            cards_widget = QWidget()
            cards_layout = QHBoxLayout(cards_widget)
            cards_layout.setContentsMargins(0, 0, 0, 0)
            cards_layout.setSpacing(8)

            self._card_total       = MetricCard("Total Signals",     "—", "",   "#EEEEEE")
            self._card_boost       = MetricCard("BOOST",             "—", "",   "#33CC66")
            self._card_keep        = MetricCard("KEEP",              "—", "",   "#AAAAFF")
            self._card_reduce      = MetricCard("REDUCE",            "—", "",   "#FF8800")
            self._card_disable     = MetricCard("DISABLE",           "—", "",   "#FF4444")
            self._card_insufficient= MetricCard("INSUFFICIENT",      "—", "",   "#888888")
            self._card_conf        = MetricCard("Overall Confidence","OBSERVATIONAL","", "#FF8800")

            for card in [self._card_total, self._card_boost, self._card_keep,
                         self._card_reduce, self._card_disable, self._card_insufficient,
                         self._card_conf]:
                cards_layout.addWidget(card)
            cards_layout.addStretch()
            layout.addWidget(cards_widget)
        else:
            self._card_total = self._card_boost = self._card_keep = None
            self._card_reduce = self._card_disable = self._card_insufficient = None
            self._card_conf = None

        layout.addStretch()
        return w

    def _build_action_tab(self) -> QWidget:
        """E. Rule Action Panel — text summary of each recommendation bucket."""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)
        self._action_text = QTextEdit()
        self._action_text.setReadOnly(True)
        self._action_text.setStyleSheet(
            "background:#0A0A14; color:#CCCCCC; font-family:monospace; font-size:11px;"
        )
        layout.addWidget(self._action_text)
        return w

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self):
        """Load existing CSV data into UI."""
        if not _SQ_DEPS_OK or self._adapter is None:
            return
        try:
            self._refresh_summary_cards()
            self._refresh_rec_table()
            self._refresh_group_table()
            self._refresh_action_text()
        except Exception as exc:
            logger.error("SignalQualityPanel._load_data: %s", exc)
            self._status_lbl.setText(f"Load error: {exc}")

    def _refresh_summary_cards(self):
        if not _SQ_DEPS_OK or self._adapter is None:
            return
        df = self._adapter.load_summary()
        if df.empty or self._card_total is None:
            return

        rec_col = "recommendation"
        counts  = df[rec_col].value_counts().to_dict() if rec_col in df.columns else {}
        total   = len(df)

        self._card_total.set_value(str(total))
        self._card_boost.set_value(str(counts.get("BOOST", 0)), "#33CC66")
        self._card_keep.set_value(str(counts.get("KEEP", 0)))
        self._card_reduce.set_value(str(counts.get("REDUCE", 0)), "#FF8800")
        self._card_disable.set_value(str(counts.get("DISABLE", 0)), "#FF4444")
        self._card_insufficient.set_value(str(counts.get("INSUFFICIENT_SAMPLE", 0)), "#888888")

    def _refresh_rec_table(self):
        if not _SQ_DEPS_OK or self._adapter is None:
            return
        df = self._adapter.load_recommendations()
        if df.empty:
            return

        import pandas as pd

        display_cols = [
            "recommendation", "source", "signal_name", "signal_group",
            "sample_count", "win_rate", "profit_factor", "avg_return",
            "max_drawdown", "confidence", "reason",
        ]
        cols = [c for c in display_cols if c in df.columns]
        if not cols:
            cols = list(df.columns)[:10]
        df_disp = df[cols].copy()

        # Sort: BOOST first, then KEEP, REDUCE, DISABLE, INSUFFICIENT
        _order = {"BOOST": 0, "KEEP": 1, "REDUCE": 2, "DISABLE": 3, "INSUFFICIENT_SAMPLE": 4}
        if "recommendation" in df_disp.columns:
            df_disp["_sort"] = df_disp["recommendation"].map(_order).fillna(5)
            df_disp = df_disp.sort_values("_sort").drop(columns=["_sort"])

        headers = {
            "recommendation": "Recommendation",
            "source":         "Source",
            "signal_name":    "Signal",
            "signal_group":   "Group",
            "sample_count":   "Sample Count",
            "win_rate":       "Win Rate",
            "profit_factor":  "Profit Factor",
            "avg_return":     "Avg Return",
            "max_drawdown":   "Max Drawdown",
            "confidence":     "Confidence",
            "reason":         "Reason",
        }
        formatters = {}
        for col in ["win_rate", "avg_return", "max_drawdown"]:
            if col in df_disp.columns:
                formatters[col] = _fmt_pct
        for col in ["profit_factor"]:
            if col in df_disp.columns:
                formatters[col] = lambda v: _fmt_ratio(v, 3)

        self._rec_view.load_dataframe(df_disp, headers=headers, formatters=formatters)

    def _refresh_group_table(self):
        if not _SQ_DEPS_OK or self._adapter is None:
            return
        df = self._adapter.load_group_summary()
        if df.empty:
            return

        headers = {
            "signal_group":   "Group",
            "signal_count":   "Signal Count",
            "avg_pf":         "Avg PF",
            "avg_win_rate":   "Avg Win Rate",
            "avg_return":     "Avg Return",
            "worst_mdd":      "Worst MDD",
            "best_signal":    "Best Signal",
            "worst_signal":   "Worst Signal",
            "recommendation": "Recommendation",
        }
        formatters = {}
        for col in ["avg_win_rate", "avg_return", "worst_mdd"]:
            if col in df.columns:
                formatters[col] = _fmt_pct
        for col in ["avg_pf"]:
            if col in df.columns:
                formatters[col] = lambda v: _fmt_ratio(v, 3)

        self._group_view.load_dataframe(df, headers=headers, formatters=formatters)

    def _refresh_action_text(self):
        if not _SQ_DEPS_OK or self._adapter is None:
            return
        df = self._adapter.load_summary()
        if df.empty:
            self._action_text.setPlainText(
                "No signal quality data found.\n"
                "Click 'Refresh Signal Quality' to generate.\n\n"
                "[Simulation Only] [No Real Orders]\n"
                "Recommendations do not automatically change strategy weights."
            )
            return

        rec_col = "recommendation"
        if rec_col not in df.columns:
            return

        lines = [
            "SIGNAL QUALITY ACTION LIST",
            "=" * 60,
            "[Simulation Only] [No Real Orders]",
            "Recommendations do not automatically change strategy weights.",
            "=" * 60,
            "",
        ]

        order = [
            ("BOOST",               "BOOST — Suggested for increased weighting:"),
            ("KEEP",                "KEEP — Maintain current weighting:"),
            ("REDUCE",              "REDUCE — Suggested for reduced weighting:"),
            ("DISABLE",             "DISABLE — Candidates for disabling:"),
            ("INSUFFICIENT_SAMPLE", "INSUFFICIENT_SAMPLE — Not enough data to judge:"),
        ]
        for rec_key, rec_label in order:
            subset = df[df[rec_col] == rec_key]
            if subset.empty:
                continue
            lines.append(rec_label)
            lines.append("-" * 50)
            for _, row in subset.iterrows():
                src  = row.get("source", "?")
                name = row.get("signal_name", "?")
                grp  = row.get("signal_group", "")
                rsn  = row.get("reason", "")
                lines.append(f"  [{src}] {grp}/{name}")
                if rsn:
                    lines.append(f"    -> {rsn}")
            lines.append("")

        self._action_text.setPlainText("\n".join(lines))

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _set_buttons_enabled(self, enabled: bool):
        self._btn_refresh.setEnabled(enabled)

    def _on_refresh(self):
        if self._adapter is None:
            self._status_lbl.setText("Signal quality adapter not available.")
            return
        if self._worker and self._worker.isRunning():
            self._status_lbl.setText("Already running…")
            return
        self._status_lbl.setText(f"Running SignalQualityEngine [mode={self._mode}]…")
        self._set_buttons_enabled(False)

        self._worker = _SQWorker(adapter=self._adapter, mode=self._mode)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_finished(self, result: dict):
        self._set_buttons_enabled(True)
        if result.get("status") == "ok":
            msg = result.get("message", "Signal quality complete.")
            rpt = result.get("report_path")
            if rpt:
                msg += f" Report: {rpt}"
            self._status_lbl.setText(msg)
            self._load_data()
        else:
            self._status_lbl.setText(f"Error: {result.get('message', 'Unknown error')}")

    def _on_error(self, msg: str):
        self._set_buttons_enabled(True)
        self._status_lbl.setText(f"Error: {msg}")
        logger.error("SignalQualityPanel worker error: %s", msg)

    def _on_open_report(self):
        if self._adapter is None:
            return
        path = self._adapter.load_latest_report_path()
        if not path:
            self._status_lbl.setText("No report found. Click Refresh Signal Quality first.")
            return
        try:
            import subprocess, sys
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as exc:
            self._status_lbl.setText(f"Cannot open report: {exc}")

    def _on_export(self):
        if self._adapter is None:
            return
        try:
            from datetime import datetime as _dt
            df = self._adapter.load_summary()
            if df.empty:
                self._status_lbl.setText("No data to export.")
                return
            ts  = _dt.now().strftime("%Y%m%d_%H%M%S")
            out = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "backtest_results", f"signal_quality_export_{ts}.csv"
            )
            os.makedirs(os.path.dirname(out), exist_ok=True)
            df.to_csv(out, index=False, encoding="utf-8-sig")
            self._status_lbl.setText(f"Exported: {out}")
        except Exception as exc:
            self._status_lbl.setText(f"Export error: {exc}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode: str):
        self._mode = mode
        if not _PYSIDE6_AVAILABLE:
            return
        mode_text  = "REAL" if mode == "real" else "MOCK"
        mode_color = "#FF8800" if mode == "real" else "#33CCFF"
        self._mode_badge.setText(f"Mode: {mode_text}")
        self._mode_badge.setStyleSheet(f"font-weight:bold; color:{mode_color}; font-size:12px;")

    def refresh(self):
        self._load_data()
