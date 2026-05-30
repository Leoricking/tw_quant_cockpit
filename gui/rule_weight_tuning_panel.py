"""
gui/rule_weight_tuning_panel.py - Rule Weight Tuning Lab GUI panel (v0.3.15).

Provides a PySide6 tab panel for running and inspecting weight configuration
experiments.

Safety invariants:
  - Simulation Only banner always visible
  - "Advisory Only — Does NOT Auto-Apply Weights" always visible
  - No real orders banner always visible
  - Recommendations never automatically modify production strategy weights

Tabs:
  Summary       — Cards: n_configs, best_config, best_score, n_qualified
  Comparison    — Sortable table of all 7 configs + metrics
  Weights       — Weight matrix table showing all configs side-by-side
  Best Config   — Detail view for the best-balanced-score config
  Signal Quality Integration — How signal_quality_boosted was derived
  Action List   — Plain-text advisory output

Buttons:
  Run Tuning          — triggers background RuleWeightTuner.run()
  Load Latest Results — reloads CSVs from disk
  Open Report         — shows latest Markdown report path
  Export Summary      — logs summary CSV path
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTabWidget, QTextEdit, QSizePolicy, QScrollArea, QGroupBox,
        QFrame, QMessageBox,
    )
    from PySide6.QtCore import Qt, Signal, QThread
    from PySide6.QtGui import QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False

try:
    from gui.portfolio_widgets import (
        MetricCard, StatusBadge, EmptyStateWidget, PortfolioTableView,
    )
    _WIDGETS_OK = True
except Exception:
    _WIDGETS_OK = False

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Background tuning worker
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _TuningWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, adapter, mode: str, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._mode    = mode

        def run(self):
            try:
                results = self._adapter.run_tuning(mode=self._mode)
                self.finished.emit(results)
            except Exception as exc:
                self.error.emit(str(exc))
else:
    _TuningWorker = None


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class RuleWeightTuningPanel(QWidget if _PYSIDE6_OK else object):
    """
    GUI panel for the Rule Weight Tuning Lab.
    Embedded as a tab in CockpitWindow via gui/dashboard.py.
    """

    def __init__(self, mode: str = "real", parent=None):
        if _PYSIDE6_OK:
            super().__init__(parent)
        self._mode    = mode
        self._worker  = None
        self._results = None

        from gui.rule_weight_data_adapter import RuleWeightDataAdapter
        self._adapter = RuleWeightDataAdapter()

        if _PYSIDE6_OK:
            self._build_ui()
            self._load_if_available()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        root.addWidget(self._build_header())
        root.addWidget(self._build_buttons())
        self._status_lbl = QLabel("Ready.")
        self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:11px")
        root.addWidget(self._status_lbl)

        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )
        root.addWidget(self._tabs, stretch=1)

        self._build_summary_tab()
        self._build_comparison_tab()
        self._build_weights_tab()
        self._build_best_config_tab()
        self._build_sq_integration_tab()
        self._build_action_list_tab()

    def _build_header(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:#1A0A2A; border-radius:6px; padding:4px")
        layout = QHBoxLayout(w)
        layout.setContentsMargins(10, 6, 10, 6)

        title = QLabel("Rule Weight Tuning Lab")
        title.setStyleSheet("font-weight:bold; font-size:14px; color:#FFAAFF")
        layout.addWidget(title)
        layout.addSpacing(16)

        for text, color in [
            ("Simulation Only", "#FF4444"),
            ("Advisory Only", "#FF8800"),
            ("Does Not Auto-Apply Weights", "#FF8800"),
            ("No Real Orders", "#FF4444"),
        ]:
            badge = QLabel(f"[ {text} ]")
            badge.setStyleSheet(
                f"color:{color}; font-weight:bold; font-size:10px; "
                "background:#2A0A0A; border-radius:3px; padding:2px 6px"
            )
            layout.addWidget(badge)
            layout.addSpacing(4)

        layout.addStretch()

        self._mode_badge = StatusBadge(
            "MOCK" if self._mode == "mock" else "REAL",
            "OBSERVATIONAL",
        ) if _WIDGETS_OK else QLabel(self._mode.upper())
        layout.addWidget(self._mode_badge)
        return w

    def _build_buttons(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn_run = QPushButton("Run Tuning")
        self._btn_run.setStyleSheet(
            "QPushButton{background:#334488;color:#FFFFFF;padding:6px 14px;"
            "border-radius:4px} QPushButton:hover{background:#4455AA}"
        )
        self._btn_run.clicked.connect(self._on_run_tuning)
        layout.addWidget(self._btn_run)

        self._btn_load = QPushButton("Load Latest Results")
        self._btn_load.setStyleSheet(
            "QPushButton{background:#2A3A2A;color:#88FF88;padding:6px 14px;"
            "border-radius:4px} QPushButton:hover{background:#3A4A3A}"
        )
        self._btn_load.clicked.connect(self._on_load_results)
        layout.addWidget(self._btn_load)

        self._btn_report = QPushButton("Open Report")
        self._btn_report.setStyleSheet(
            "QPushButton{background:#2A2A3A;color:#AAAAFF;padding:6px 14px;"
            "border-radius:4px} QPushButton:hover{background:#3A3A4A}"
        )
        self._btn_report.clicked.connect(self._on_open_report)
        layout.addWidget(self._btn_report)

        self._btn_export = QPushButton("Export Summary")
        self._btn_export.setStyleSheet(
            "QPushButton{background:#2A2A2A;color:#AAAAAA;padding:6px 14px;"
            "border-radius:4px} QPushButton:hover{background:#3A3A3A}"
        )
        self._btn_export.clicked.connect(self._on_export_summary)
        layout.addWidget(self._btn_export)

        layout.addStretch()
        return w

    # ---- Summary tab ----

    def _build_summary_tab(self):
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(8)

        self._card_total     = MetricCard("Total Configs",    "—") if _WIDGETS_OK else None
        self._card_qualified = MetricCard("Qualified",         "—") if _WIDGETS_OK else None
        self._card_best      = MetricCard("Best Config",       "—") if _WIDGETS_OK else None
        self._card_bs        = MetricCard("Balanced Score",    "—") if _WIDGETS_OK else None
        self._card_sharpe    = MetricCard("Top Sharpe Config", "—") if _WIDGETS_OK else None
        self._card_pf        = MetricCard("Top PF Config",     "—") if _WIDGETS_OK else None

        for card in [self._card_total, self._card_qualified, self._card_best,
                     self._card_bs, self._card_sharpe, self._card_pf]:
            if card:
                cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Constraints note
        note = QLabel(
            "Disqualification: MaxDD > 25%  |  PF < 1.20  |  trade_count < 30"
        )
        note.setStyleSheet("color:#888888; font-size:11px; font-style:italic")
        layout.addWidget(note)

        if _WIDGETS_OK:
            self._empty_state_summary = EmptyStateWidget(
                message="No tuning results loaded.",
                hint="Press 'Run Tuning' to evaluate all 7 weight configurations.",
            )
            layout.addWidget(self._empty_state_summary)
        layout.addStretch()

        w.setWidget(inner)
        self._tabs.addTab(w, "Summary")

    # ---- Comparison tab ----

    def _build_comparison_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)

        if _WIDGETS_OK:
            self._comparison_table = PortfolioTableView()
            layout.addWidget(self._comparison_table)
        else:
            self._comparison_table = None
            layout.addWidget(QLabel("PySide6 / portfolio_widgets not available"))

        self._tabs.addTab(w, "Comparison")

    # ---- Weights tab ----

    def _build_weights_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)

        if _WIDGETS_OK:
            self._weights_table = PortfolioTableView()
            layout.addWidget(self._weights_table)
        else:
            self._weights_table = None
            layout.addWidget(QLabel("PySide6 / portfolio_widgets not available"))

        self._tabs.addTab(w, "Weights")

    # ---- Best Config tab ----

    def _build_best_config_tab(self):
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._best_config_text = QTextEdit()
        self._best_config_text.setReadOnly(True)
        self._best_config_text.setStyleSheet(
            "background:#0E1520; color:#CCCCCC; font-family:monospace; font-size:12px"
        )
        layout.addWidget(self._best_config_text)
        w.setWidget(inner)
        self._tabs.addTab(w, "Best Config")

    # ---- Signal Quality Integration tab ----

    def _build_sq_integration_tab(self):
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(8, 8, 8, 8)

        if _WIDGETS_OK:
            self._sq_effects_table = PortfolioTableView()
            layout.addWidget(self._sq_effects_table)

        self._sq_note = QTextEdit()
        self._sq_note.setReadOnly(True)
        self._sq_note.setMaximumHeight(120)
        self._sq_note.setStyleSheet(
            "background:#0E1520; color:#AAAACC; font-size:11px; font-style:italic"
        )
        layout.addWidget(self._sq_note)

        w.setWidget(inner)
        self._tabs.addTab(w, "Signal Quality Integration")

    # ---- Action List tab ----

    def _build_action_list_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)

        self._action_text = QTextEdit()
        self._action_text.setReadOnly(True)
        self._action_text.setStyleSheet(
            "background:#0A0A14; color:#CCFFCC; font-family:monospace; font-size:11px"
        )
        layout.addWidget(self._action_text)
        self._tabs.addTab(w, "Action List")

    # ------------------------------------------------------------------
    # Data loading / refresh
    # ------------------------------------------------------------------

    def _load_if_available(self):
        if self._adapter.has_results():
            self._refresh_from_csv()

    def _refresh_from_csv(self):
        comp_df  = self._adapter.load_config_comparison()
        se_df    = self._adapter.load_signal_effects()
        metrics  = self._adapter.load_summary_metrics()
        self._update_ui(comp_df=comp_df, se_df=se_df, metrics=metrics)

    def _update_ui(self, comp_df=None, se_df=None, metrics=None, full_results=None):
        import pandas as pd
        if metrics:
            self._update_cards(metrics)
        if comp_df is not None and not comp_df.empty:
            self._update_comparison_table(comp_df)
            self._update_weights_table(comp_df)
            self._update_best_config_text(comp_df)
            self._update_action_list(comp_df)
        if se_df is not None and not se_df.empty:
            self._update_sq_effects(se_df)
        self._set_status("Results loaded.")

    def _update_cards(self, metrics: dict):
        def _set(card, val):
            if card:
                try:
                    card.set_value(str(val) if val is not None else "—")
                except Exception:
                    pass

        _set(self._card_total,     metrics.get("n_configs", "—"))
        _set(self._card_qualified, metrics.get("n_qualified", "—"))
        _set(self._card_best,      metrics.get("best_config_name") or "—")
        bs = metrics.get("best_balanced_score")
        _set(self._card_bs,        f"{bs:.4f}" if bs is not None else "—")
        _set(self._card_sharpe,    metrics.get("top_sharpe_config") or "—")
        _set(self._card_pf,        metrics.get("top_pf_config") or "—")

        if self._card_total and hasattr(self, "_empty_state_summary"):
            try:
                self._empty_state_summary.hide()
            except Exception:
                pass

    def _update_comparison_table(self, df):
        if self._comparison_table is None:
            return
        cols = ["rank", "config_name", "total_return", "sharpe", "max_drawdown",
                "profit_factor", "win_rate", "trade_count", "balanced_score",
                "disqualified", "dq_reason"]
        existing = [c for c in cols if c in df.columns]
        headers = {
            "rank": "Rank", "config_name": "Config",
            "total_return": "Return", "sharpe": "Sharpe",
            "max_drawdown": "MaxDD", "profit_factor": "PF",
            "win_rate": "WinRate", "trade_count": "Trades",
            "balanced_score": "B.Score", "disqualified": "DQ",
            "dq_reason": "DQ Reason",
        }

        import pandas as pd

        def _fmt_pct(v):
            try:
                return f"{float(v)*100:+.2f}%"
            except Exception:
                return str(v) if v is not None else "—"

        def _fmt_f(v):
            try:
                return f"{float(v):.3f}"
            except Exception:
                return str(v) if v is not None else "—"

        formatters = {
            "total_return":   _fmt_pct,
            "max_drawdown":   _fmt_pct,
            "win_rate":       lambda v: _fmt_pct(v).replace("+", ""),
            "sharpe":         _fmt_f,
            "profit_factor":  _fmt_f,
            "balanced_score": lambda v: _fmt_f(v) if v else "—",
            "disqualified":   lambda v: "YES" if v else "no",
        }
        display_headers = [headers.get(c, c) for c in existing]
        self._comparison_table.load_dataframe(
            df[existing], display_headers, formatters
        )

    def _update_weights_table(self, df):
        if self._weights_table is None:
            return
        weight_cols = ["config_name", "bull_stock_w", "buy_point_w", "sk_w",
                       "fundamental_w", "intraday_w", "sector_w"]
        existing = [c for c in weight_cols if c in df.columns]
        headers = {
            "config_name": "Config", "bull_stock_w": "Bull",
            "buy_point_w": "BuyPt", "sk_w": "SK",
            "fundamental_w": "Fund", "intraday_w": "Intraday",
            "sector_w": "Sector",
        }
        display_headers = [headers.get(c, c) for c in existing]

        def _fmt_w(v):
            try:
                return f"{float(v):.4f}"
            except Exception:
                return str(v) if v is not None else "—"

        formatters = {c: _fmt_w for c in existing if c != "config_name"}
        self._weights_table.load_dataframe(df[existing], display_headers, formatters)

    def _update_best_config_text(self, df):
        import pandas as pd
        qualified = df[df.get("disqualified", pd.Series([False]*len(df))) == False]
        if qualified.empty:
            self._best_config_text.setPlainText(
                "No qualified configs found.\n\n"
                "All configs failed one or more disqualification constraints:\n"
                "  MaxDD > 25%\n  PF < 1.20\n  trade_count < 30"
            )
            return

        bs_col = "balanced_score"
        if bs_col in qualified.columns:
            q2 = qualified.dropna(subset=[bs_col])
            if not q2.empty:
                best_row = q2.loc[q2[bs_col].astype(float).idxmax()]
                name = best_row.get("config_name", "—")
                lines = [
                    f"Best Config: {name}",
                    "=" * 40,
                    f"  Description  : {best_row.get('description', '—')}",
                    f"  Balanced Score: {best_row.get(bs_col, '—')}",
                    f"  Total Return  : {_pct(best_row.get('total_return'))}",
                    f"  Sharpe        : {best_row.get('sharpe', '—')}",
                    f"  Max Drawdown  : {_pct(best_row.get('max_drawdown'))}",
                    f"  Profit Factor : {best_row.get('profit_factor', '—')}",
                    f"  Win Rate      : {_pct(best_row.get('win_rate'), sign=False)}",
                    f"  Trade Count   : {int(best_row.get('trade_count', 0))}",
                    "",
                    "  Weights:",
                    f"    bull_stock     : {best_row.get('bull_stock_w', '—')}",
                    f"    buy_point      : {best_row.get('buy_point_w', '—')}",
                    f"    strategy_know  : {best_row.get('sk_w', '—')}",
                    f"    fundamental    : {best_row.get('fundamental_w', '—')}",
                    f"    intraday       : {best_row.get('intraday_w', '—')}",
                    f"    sector_strength: {best_row.get('sector_w', '—')}",
                    "",
                    "[!] Advisory only. Does NOT auto-apply weights.",
                    "[!] Simulation Only. No Real Orders.",
                ]
                self._best_config_text.setPlainText("\n".join(lines))
                return

        self._best_config_text.setPlainText("No data available.")

    def _update_sq_effects(self, se_df):
        if not _WIDGETS_OK or self._sq_effects_table is None:
            return
        # Show signal vs baseline vs signal_quality_boosted
        cols = ["signal", "baseline"]
        sq_col = "signal_quality_boosted"
        delta_col = f"{sq_col}_delta"
        for c in [sq_col, delta_col]:
            if c in se_df.columns:
                cols.append(c)
        existing = [c for c in cols if c in se_df.columns]
        headers = {
            "signal": "Signal", "baseline": "Baseline",
            sq_col: "SQ Boosted", delta_col: "Delta",
        }
        disp = [headers.get(c, c) for c in existing]

        def _fmt_w(v):
            try:
                f = float(v)
                return f"{f:+.4f}" if "delta" in "delta" else f"{f:.4f}"
            except Exception:
                return str(v) if v is not None else "—"

        self._sq_effects_table.load_dataframe(
            se_df[existing], disp,
            {c: _fmt_w for c in existing if c != "signal"}
        )

        note = (
            "signal_quality_boosted adjusts weights from baseline using signal_quality_summary.csv:\n"
            "  BOOST ×1.15  |  KEEP ×1.00  |  REDUCE ×0.85  |  DISABLE ×0.60\n"
            "Falls back to balanced_v2 if signal_quality_summary.csv is missing."
        )
        self._sq_note.setPlainText(note)

    def _update_action_list(self, df):
        import pandas as pd
        qualified = df[df.get("disqualified", pd.Series([False]*len(df))) == False]
        disqualified = df[df.get("disqualified", pd.Series([False]*len(df))) == True]

        lines = [
            "Rule Weight Tuning Lab — Action List",
            "=" * 50,
            "[!] Advisory Only. Does NOT auto-apply weights.",
            "[!] Simulation Only. No Real Orders.",
            "",
        ]

        if not qualified.empty:
            lines.append("QUALIFIED CONFIGS (sorted by balanced_score):")
            for _, row in qualified.iterrows():
                bs = row.get("balanced_score")
                bs_s = f"{float(bs):.4f}" if bs is not None else "—"
                lines.append(
                    f"  [{row.get('config_name','?')}] "
                    f"BS={bs_s} "
                    f"Return={_pct(row.get('total_return'))} "
                    f"Sharpe={row.get('sharpe','—')} "
                    f"MaxDD={_pct(row.get('max_drawdown'))} "
                    f"PF={row.get('profit_factor','—')}"
                )

        if not disqualified.empty:
            lines.append("\nDISQUALIFIED CONFIGS:")
            for _, row in disqualified.iterrows():
                lines.append(
                    f"  [{row.get('config_name','?')}] — {row.get('dq_reason','?')}"
                )

        lines += [
            "",
            "To apply the best config in production, manually review the weights",
            "above and update backtest/portfolio_rules.py score_candidate().",
            "Never blindly apply tuning results without human review.",
        ]

        self._action_text.setPlainText("\n".join(lines))

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_run_tuning(self):
        if self._worker and self._worker.isRunning():
            self._set_status("Tuning already running…")
            return
        self._set_status("Running weight configurations… (this may take a moment)")
        self._btn_run.setEnabled(False)
        if _PYSIDE6_OK and _TuningWorker:
            self._worker = _TuningWorker(self._adapter, self._mode, parent=self)
            self._worker.finished.connect(self._on_tuning_finished)
            self._worker.error.connect(self._on_tuning_error)
            self._worker.start()

    def _on_tuning_finished(self, results: dict):
        self._btn_run.setEnabled(True)
        status = results.get("status", "error")
        if status == "insufficient_data":
            self._set_status(
                f"Insufficient data: {results.get('message', 'no data')}"
            )
            return
        if status == "error":
            self._set_status(f"Error: {results.get('message', 'unknown')}")
            return

        self._results = results
        comp_df = results.get("comparison_df")
        se_df   = results.get("signal_effects_df")
        metrics = self._adapter.load_summary_metrics()
        self._update_ui(comp_df=comp_df, se_df=se_df, metrics=metrics,
                        full_results=results)
        self._set_status(
            f"Tuning complete. {results.get('n_configs', 0)} configs evaluated."
        )

    def _on_tuning_error(self, msg: str):
        self._btn_run.setEnabled(True)
        self._set_status(f"Error: {msg}")

    def _on_load_results(self):
        self._refresh_from_csv()

    def _on_open_report(self):
        path = self._adapter.load_latest_report_path()
        if path:
            self._set_status(f"Latest report: {path}")
            try:
                import subprocess, sys
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", path])
            except Exception as exc:
                self._set_status(f"Cannot open report: {exc}")
        else:
            self._set_status("No report found. Run tuning first.")

    def _on_export_summary(self):
        from gui.rule_weight_data_adapter import RuleWeightDataAdapter
        path = os.path.join(self._adapter.results_dir, "rule_weight_config_comparison.csv")
        if os.path.exists(path):
            self._set_status(f"Summary CSV: {path}")
        else:
            self._set_status("No summary CSV found. Run tuning first.")

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def set_mode(self, mode: str):
        """Called by CockpitWindow when mode toggle changes."""
        self._mode = mode
        if _PYSIDE6_OK and hasattr(self, "_mode_badge"):
            try:
                self._mode_badge.setText(mode.upper())
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Status helper
    # ------------------------------------------------------------------

    def _set_status(self, msg: str):
        if _PYSIDE6_OK and hasattr(self, "_status_lbl"):
            self._status_lbl.setText(msg)


# ------------------------------------------------------------------
# Formatters
# ------------------------------------------------------------------

def _pct(v, sign=True) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
        return f"{f*100:+.2f}%" if sign else f"{f*100:.2f}%"
    except Exception:
        return str(v)
