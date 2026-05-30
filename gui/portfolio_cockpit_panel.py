"""
gui/portfolio_cockpit_panel.py - Portfolio Cockpit main panel (v0.3.13).

Displays portfolio simulation results in a structured GUI panel.

Sections:
  A. Header / Safety Banner  — mode, confidence, simulation-only notice
  B. Scenario Summary Cards  — total return, sharpe, max drawdown, etc.
  C. Scenario Comparison     — table comparing all 4 scenarios
  D. Candidate Ranking       — per-symbol trade statistics
  E. Suggested Positions     — symbol weight + risk parameters
  F. Sector Exposure         — sector concentration vs limit
  G. Recent Simulated Trades — latest trades with PnL
  H. Risk Warnings           — consolidated warning messages

Action buttons:
  - Refresh Portfolio Simulation (balanced, current mode)
  - Run Balanced Scenario
  - Run All Scenarios
  - Open Latest Report
  - Export Summary

Rules:
  - Does NOT submit orders.
  - Does NOT call broker APIs.
  - Empty state shown when no CSV exists — no crash.
  - Simulation Only / Real Order Execution: DISABLED always visible.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTabWidget, QGroupBox, QScrollArea, QFrame, QSplitter,
        QMessageBox, QSizePolicy, QStatusBar,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — PortfolioCockpitPanel will be stub.")

try:
    from gui.portfolio_widgets import (
        MetricCard, StatusBadge, RiskBadge,
        PortfolioTableView, EmptyStateWidget,
        _fmt_pct, _fmt_ratio, _fmt_ntd, _fmt_any,
    )
    from gui.portfolio_data_adapter import PortfolioDataAdapter
    _PORTFOLIO_WIDGETS_OK = True
except Exception as _pw_exc:
    logger.warning("Portfolio widgets unavailable: %s", _pw_exc)
    _PORTFOLIO_WIDGETS_OK = False


# ---------------------------------------------------------------------------
# Background simulation worker
# ---------------------------------------------------------------------------

class _SimWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Runs simulation in background thread to avoid blocking GUI."""

    if _PYSIDE6_AVAILABLE:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, adapter: "PortfolioDataAdapter", scenario: str, mode: str, run_all: bool = False):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self._adapter  = adapter
        self._scenario = scenario
        self._mode     = mode
        self._run_all  = run_all

    def run(self):
        try:
            if self._run_all:
                result = self._adapter.run_all_scenarios(mode=self._mode)
            else:
                result = self._adapter.run_simulation(scenario=self._scenario, mode=self._mode)
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
# PortfolioCockpitPanel
# ---------------------------------------------------------------------------

class PortfolioCockpitPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Portfolio Cockpit main panel.

    Can be embedded as a tab in an existing QTabWidget (e.g., dashboard).
    """

    def __init__(self, mode: str = 'mock', parent=None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(parent)
        self._mode      = mode
        self._adapter   = PortfolioDataAdapter() if _PORTFOLIO_WIDGETS_OK else None
        self._sim_worker: Optional[_SimWorker] = None
        self._build_ui()
        self._load_data()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(4)

        # A. Header / Safety Banner
        root.addWidget(self._build_header())

        # Action buttons row
        root.addWidget(self._build_buttons())

        # Status label (shows "Running…" / errors)
        self._status_lbl = QLabel("")
        self._status_lbl.setStyleSheet("color:#FF8800; font-size:11px;")
        root.addWidget(self._status_lbl)

        # Content tabs
        self._content_tabs = QTabWidget()
        _tab_style = (
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 12px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )
        self._content_tabs.setStyleSheet(_tab_style)
        root.addWidget(self._content_tabs, stretch=1)

        # B. Scenario Summary tab
        self._summary_tab = self._build_summary_tab()
        self._content_tabs.addTab(self._summary_tab, "Summary")

        # C. Scenario Comparison tab
        self._scenario_view = PortfolioTableView("Scenario Comparison") if _PORTFOLIO_WIDGETS_OK else QLabel("unavailable")
        self._content_tabs.addTab(self._scenario_view, "Scenarios")

        # G. Recent Trades tab
        self._trades_view = PortfolioTableView("Recent Simulated Trades") if _PORTFOLIO_WIDGETS_OK else QLabel("unavailable")
        self._content_tabs.addTab(self._trades_view, "Trades")

        # E. Suggested Positions tab
        self._positions_view = PortfolioTableView("Suggested Positions") if _PORTFOLIO_WIDGETS_OK else QLabel("unavailable")
        self._content_tabs.addTab(self._positions_view, "Positions")

        # D. Candidate Ranking tab
        self._candidates_view = PortfolioTableView("Candidate Ranking") if _PORTFOLIO_WIDGETS_OK else QLabel("unavailable")
        self._content_tabs.addTab(self._candidates_view, "Candidates")

        # F. Sector Exposure tab
        self._sector_view = PortfolioTableView("Sector Exposure") if _PORTFOLIO_WIDGETS_OK else QLabel("unavailable")
        self._content_tabs.addTab(self._sector_view, "Sector")

    def _build_header(self) -> QWidget:
        w = QFrame()
        w.setFrameShape(QFrame.StyledPanel)
        w.setStyleSheet("background:#1A0A28; border:1px solid #553366; border-radius:4px;")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(3)

        # Title row
        title_row = QHBoxLayout()
        title_lbl = _lbl("Portfolio Simulation Cockpit", bold=True, color="#CC88FF", size=15)
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        mode_text = "REAL" if self._mode == 'real' else "MOCK"
        mode_color = "#FF8800" if self._mode == 'real' else "#33CCFF"
        self._mode_badge = _lbl(f"Mode: {mode_text}", bold=True, color=mode_color, size=12)
        title_row.addWidget(self._mode_badge)
        layout.addLayout(title_row)

        # Safety row
        safety_row = QHBoxLayout()
        safety_row.addWidget(_lbl("[ Simulation Only ]", bold=True, color="#FF4444", size=11))
        safety_row.addSpacing(12)
        safety_row.addWidget(_lbl("Real Order Execution: DISABLED", bold=True, color="#FF4444", size=11))
        safety_row.addSpacing(12)
        safety_row.addWidget(_lbl("No real orders will be sent", color="#FF8800", size=11))
        safety_row.addStretch()

        self._confidence_badge = StatusBadge("OBSERVATIONAL") if _PORTFOLIO_WIDGETS_OK else QLabel("OBSERVATIONAL")
        safety_row.addWidget(_lbl("Confidence:", color="#AAAAAA", size=11))
        safety_row.addWidget(self._confidence_badge)
        layout.addLayout(safety_row)

        return w

    def _build_buttons(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)

        btn_style = (
            "QPushButton { background:#252545; color:#CCCCFF; border:1px solid #444466; "
            "border-radius:3px; padding:4px 10px; font-size:11px; } "
            "QPushButton:hover { background:#333366; } "
            "QPushButton:disabled { color:#555555; }"
        )

        self._btn_refresh = QPushButton("Refresh Portfolio Simulation")
        self._btn_balanced = QPushButton("Run Balanced Scenario")
        self._btn_all = QPushButton("Run All Scenarios")
        self._btn_report = QPushButton("Open Latest Report")
        self._btn_export = QPushButton("Export Summary")

        for btn in [self._btn_refresh, self._btn_balanced, self._btn_all, self._btn_report, self._btn_export]:
            btn.setStyleSheet(btn_style)
            layout.addWidget(btn)

        layout.addStretch()

        self._btn_refresh.clicked.connect(self._on_refresh)
        self._btn_balanced.clicked.connect(self._on_run_balanced)
        self._btn_all.clicked.connect(self._on_run_all)
        self._btn_report.clicked.connect(self._on_open_report)
        self._btn_export.clicked.connect(self._on_export_summary)

        return w

    def _build_summary_tab(self) -> QWidget:
        """Build the B (scenario cards) + H (risk warnings) combined tab."""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        # Best scenario label
        self._best_scenario_lbl = _lbl("Best Scenario: —", bold=True, color="#FF8800", size=13)
        layout.addWidget(self._best_scenario_lbl)

        # KPI cards row
        cards_widget = QWidget()
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(8)

        if _PORTFOLIO_WIDGETS_OK:
            self._card_return      = MetricCard("Total Return",     "—", "—",  "#EEEEEE")
            self._card_annualized  = MetricCard("Ann. Return",      "—", "—",  "#EEEEEE")
            self._card_sharpe      = MetricCard("Sharpe Ratio",     "—", "> 1.5", "#EEEEEE")
            self._card_drawdown    = MetricCard("Max Drawdown",     "—", "< 20%", "#EEEEEE")
            self._card_pf          = MetricCard("Profit Factor",    "—", "> 1.5", "#EEEEEE")
            self._card_winrate     = MetricCard("Win Rate",         "—", "—",  "#EEEEEE")
            self._card_exposure    = MetricCard("Avg Exposure",     "—", "—",  "#EEEEEE")
            self._card_trades      = MetricCard("Trade Count",      "—", "—",  "#EEEEEE")
            for card in [self._card_return, self._card_annualized, self._card_sharpe,
                         self._card_drawdown, self._card_pf, self._card_winrate,
                         self._card_exposure, self._card_trades]:
                cards_layout.addWidget(card)
        else:
            self._card_return = self._card_annualized = self._card_sharpe = None
            self._card_drawdown = self._card_pf = self._card_winrate = None
            self._card_exposure = self._card_trades = None

        cards_layout.addStretch()
        layout.addWidget(cards_widget)

        # H. Risk Warnings section
        warn_box = QGroupBox("Risk Warnings")
        warn_box.setStyleSheet(
            "QGroupBox { color:#FF8800; font-weight:bold; border:1px solid #553322; "
            "border-radius:4px; margin-top:6px; padding:4px; } "
            "QGroupBox::title { subcontrol-origin:margin; left:8px; }"
        )
        warn_layout = QVBoxLayout(warn_box)
        warn_layout.setSpacing(4)

        if _PORTFOLIO_WIDGETS_OK:
            self._warn_observational = RiskBadge(
                "OBSERVATIONAL confidence: 14-symbol universe. "
                "Results are for framework validation only — not a trading recommendation.", "warning"
            )
            self._warn_simulation = RiskBadge(
                "Simulation Only. Entry uses signal-date close price (first version). "
                "Fundamental data is a static snapshot. No forward-return leakage.", "warning"
            )
            self._warn_no_order = RiskBadge(
                "Real Order Execution: DISABLED. "
                "No broker API connected. No orders submitted.", "error"
            )
            self._warn_drawdown = RiskBadge("")
            self._warn_timing = RiskBadge(
                "TIMING_ESTIMATED: some financial announcement dates are estimated "
                "by legal deadline, not confirmed MOPS publication date.", "warning"
            )
            self._warn_sector = RiskBadge("")
            for w_item in [self._warn_observational, self._warn_simulation,
                           self._warn_no_order, self._warn_timing]:
                warn_layout.addWidget(w_item)
            self._warn_drawdown.hide()
            self._warn_sector.hide()
            warn_layout.addWidget(self._warn_drawdown)
            warn_layout.addWidget(self._warn_sector)
        else:
            self._warn_observational = self._warn_simulation = None
            self._warn_no_order = self._warn_drawdown = self._warn_timing = None
            self._warn_sector = None

        layout.addWidget(warn_box)
        layout.addStretch()
        return w

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self):
        """Load all available simulation results into the UI."""
        if not _PORTFOLIO_WIDGETS_OK or self._adapter is None:
            return
        try:
            self._refresh_metrics()
            self._refresh_scenario_table()
            self._refresh_trades_table()
            self._refresh_positions_table()
            self._refresh_candidates_table()
            self._refresh_sector_table()
        except Exception as exc:
            logger.error("PortfolioCockpitPanel._load_data error: %s", exc)
            self._status_lbl.setText(f"Load error: {exc}")

    def _refresh_metrics(self):
        """Update KPI cards from latest metrics CSV."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        metrics = self._adapter.load_latest_metrics()
        if not metrics:
            return

        def _pct_color(v, good_positive=True) -> str:
            if v is None:
                return "#EEEEEE"
            try:
                fv = float(v)
                if good_positive:
                    return "#33CC66" if fv > 0 else "#FF4444"
                else:
                    return "#33CC66" if fv > -0.10 else ("#FF8800" if fv > -0.20 else "#FF4444")
            except Exception:
                return "#EEEEEE"

        tr = metrics.get('total_return')
        ar = metrics.get('annualized_return')
        sh = metrics.get('sharpe')
        md = metrics.get('max_drawdown')
        pf = metrics.get('profit_factor')
        wr = metrics.get('win_rate')
        ex = metrics.get('average_exposure')
        tc = metrics.get('trade_count')
        conf = metrics.get('confidence', 'OBSERVATIONAL')
        scenario = metrics.get('scenario', metrics.get('scenario_name', '—'))

        if self._card_return:
            self._card_return.set_value(_fmt_pct(tr), _pct_color(tr))
        if self._card_annualized:
            self._card_annualized.set_value(_fmt_pct(ar), _pct_color(ar))
        if self._card_sharpe:
            sh_v = float(sh) if sh is not None else None
            sh_color = "#33CC66" if sh_v and sh_v >= 1.5 else ("#FF8800" if sh_v and sh_v >= 1.0 else "#FF4444")
            self._card_sharpe.set_value(_fmt_ratio(sh, 3) if sh is not None else "—", sh_color)
        if self._card_drawdown:
            self._card_drawdown.set_value(_fmt_pct(md), _pct_color(md, good_positive=False))
        if self._card_pf:
            pf_v = float(pf) if pf is not None else None
            pf_color = "#33CC66" if pf_v and pf_v >= 1.5 else ("#FF8800" if pf_v and pf_v >= 1.0 else "#FF4444")
            self._card_pf.set_value(_fmt_ratio(pf, 3) if pf is not None else "—", pf_color)
        if self._card_winrate:
            self._card_winrate.set_value(_fmt_pct(wr))
        if self._card_exposure:
            self._card_exposure.set_value(_fmt_pct(ex))
        if self._card_trades:
            self._card_trades.set_value(str(int(tc)) if tc is not None else "—")

        if self._confidence_badge:
            c_str = str(conf).upper() if conf else "OBSERVATIONAL"
            self._confidence_badge.set_status(c_str)

        if scenario and scenario != '—':
            self._best_scenario_lbl.setText(f"Scenario: {scenario}")

        # Update drawdown warning
        if self._warn_drawdown and md is not None:
            try:
                md_v = float(md)
                if md_v < -0.20:
                    self._warn_drawdown.setText(
                        f"MAX DRAWDOWN WARNING: {_fmt_pct(md)} exceeds -20% target. "
                        "Risk controls may be insufficient."
                    )
                    self._warn_drawdown.show()
                else:
                    self._warn_drawdown.hide()
            except Exception:
                self._warn_drawdown.hide()

    def _refresh_scenario_table(self):
        """Load scenario comparison table."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        df = self._adapter.load_scenario_comparison()
        if df.empty:
            return

        import pandas as pd

        display_cols = [
            'scenario_name', 'total_return', 'annualized_return', 'sharpe',
            'max_drawdown', 'profit_factor', 'win_rate', 'trade_count',
            'avg_exposure',
        ]
        cols = [c for c in display_cols if c in df.columns]
        if not cols:
            cols = list(df.columns)
        df_disp = df[cols].copy() if cols else df.copy()

        headers = {
            'scenario_name':    'Scenario',
            'total_return':     'Total Return',
            'annualized_return':'Ann. Return',
            'sharpe':           'Sharpe',
            'max_drawdown':     'Max Drawdown',
            'profit_factor':    'Profit Factor',
            'win_rate':         'Win Rate',
            'trade_count':      'Trades',
            'avg_exposure':     'Avg Exposure',
            'confidence':       'Confidence',
        }
        formatters = {}
        for col in ['total_return', 'annualized_return', 'win_rate', 'max_drawdown', 'avg_exposure']:
            if col in df_disp.columns:
                formatters[col] = _fmt_pct
        for col in ['sharpe', 'profit_factor']:
            if col in df_disp.columns:
                formatters[col] = lambda v: _fmt_ratio(v, 3)

        self._scenario_view.load_dataframe(df_disp, headers=headers, formatters=formatters)

    def _refresh_trades_table(self):
        """Load recent trades table (last 50)."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        df = self._adapter.load_trades()
        if df.empty:
            return

        import pandas as pd

        display_cols = ['date', 'symbol', 'name', 'action', 'price', 'quantity', 'reason', 'pnl']
        cols = [c for c in display_cols if c in df.columns]
        if not cols:
            cols = list(df.columns)[:8]

        # Show most recent 50 trades
        df_disp = df[cols].tail(50).copy() if cols else df.tail(50).copy()

        headers = {
            'date':     'Date',
            'symbol':   'Symbol',
            'name':     'Name',
            'action':   'Action',
            'price':    'Price',
            'quantity': 'Qty',
            'reason':   'Reason',
            'pnl':      'PnL',
        }
        formatters = {}
        if 'pnl' in df_disp.columns:
            formatters['pnl'] = _fmt_ntd
        if 'price' in df_disp.columns:
            formatters['price'] = lambda v: f"{float(v):.1f}" if v not in (None, '') else "—"

        self._trades_view.load_dataframe(df_disp, headers=headers, formatters=formatters)

    def _refresh_positions_table(self):
        """Build suggested positions from open trades (entries without exits)."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        df = self._adapter.load_trades()
        if df.empty:
            return

        import pandas as pd

        try:
            # Find symbols that were entered but not fully exited
            entries = df[df['action'].str.upper().isin(['BUY', 'ENTRY'])] if 'action' in df.columns else df
            exits   = df[df['action'].str.upper().isin(['SELL', 'EXIT', 'STOP_LOSS', 'TRAILING_STOP',
                                                         'TAKE_PROFIT_HALF', 'TAKE_PROFIT'])] \
                if 'action' in df.columns else pd.DataFrame()

            entry_syms = set(entries['symbol'].unique()) if 'symbol' in entries.columns else set()
            exit_syms  = set(exits['symbol'].unique())  if not exits.empty and 'symbol' in exits.columns else set()

            # Consider last position entries for display
            rows = []
            for sym, grp in entries.groupby('symbol') if 'symbol' in entries.columns else []:
                last = grp.sort_values('date').iloc[-1] if 'date' in grp.columns else grp.iloc[-1]
                row = {
                    'symbol':           sym,
                    'name':             last.get('name', sym),
                    'entry_date':       last.get('date', '—'),
                    'entry_price':      last.get('price', None),
                    'suggested_weight': '20%',  # default from balanced scenario
                    'entry_reason':     last.get('reason', '—'),
                    'stop_loss':        f"{last.get('stop_loss_price', '—')}",
                    'take_profit_half': f"{last.get('take_profit_price', '—')}",
                    'trailing_stop':    '—',
                    'risk_warning':     last.get('warning', '—'),
                }
                rows.append(row)

            if not rows:
                return
            df_pos = pd.DataFrame(rows)

            headers = {
                'symbol':           'Symbol',
                'name':             'Name',
                'entry_date':       'Entry Date',
                'entry_price':      'Entry Price',
                'suggested_weight': 'Suggested Weight',
                'entry_reason':     'Entry Reason',
                'stop_loss':        'Stop Loss',
                'take_profit_half': 'Take Profit Half',
                'trailing_stop':    'Trailing Stop',
                'risk_warning':     'Risk Warning',
            }
            self._positions_view.load_dataframe(df_pos, headers=headers)
        except Exception as exc:
            logger.warning("_refresh_positions_table: %s", exc)

    def _refresh_candidates_table(self):
        """Load candidate ranking from trade statistics."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        df = self._adapter.load_candidates()
        if df.empty:
            return

        import pandas as pd

        display_cols = ['symbol', 'name', 'sector', 'trade_count', 'total_pnl', 'avg_pnl', 'win_rate']
        cols = [c for c in display_cols if c in df.columns]
        if not cols:
            cols = list(df.columns)
        df_disp = df[cols].copy()
        if 'total_pnl' in df_disp.columns:
            df_disp = df_disp.sort_values('total_pnl', ascending=False)

        headers = {
            'symbol':       'Symbol',
            'name':         'Name',
            'sector':       'Sector',
            'trade_count':  'Trades',
            'total_pnl':    'Total PnL',
            'avg_pnl':      'Avg PnL',
            'win_rate':     'Win Rate',
        }
        formatters = {}
        if 'total_pnl' in df_disp.columns:
            formatters['total_pnl'] = _fmt_ntd
        if 'avg_pnl' in df_disp.columns:
            formatters['avg_pnl'] = _fmt_ntd
        if 'win_rate' in df_disp.columns:
            formatters['win_rate'] = _fmt_pct

        self._candidates_view.load_dataframe(df_disp, headers=headers, formatters=formatters)

    def _refresh_sector_table(self):
        """Build sector exposure table from daily positions data."""
        if self._adapter is None or not _PORTFOLIO_WIDGETS_OK:
            return
        df_pos = self._adapter.load_positions()
        if df_pos.empty:
            return

        import pandas as pd

        try:
            if 'sector' not in df_pos.columns or 'exposure_pct' not in df_pos.columns:
                # Try to compute from trades
                trades = self._adapter.load_trades()
                if trades.empty or 'sector' not in trades.columns:
                    return
                sector_counts = trades.groupby('sector').size().reset_index(name='trade_count')
                sector_counts['exposure_pct'] = sector_counts['trade_count'] / sector_counts['trade_count'].sum()
                sector_counts['limit_pct'] = 0.50
                sector_counts['status'] = sector_counts['exposure_pct'].apply(
                    lambda v: 'OVER_LIMIT' if v > 0.50 else 'OK'
                )
                df_sector = sector_counts[['sector', 'exposure_pct', 'limit_pct', 'status']]
            else:
                # Use last date's sector breakdown
                last_date = df_pos['date'].max() if 'date' in df_pos.columns else None
                if last_date:
                    df_last = df_pos[df_pos['date'] == last_date]
                else:
                    df_last = df_pos
                df_sector = df_last[['sector', 'exposure_pct']].copy() if 'sector' in df_last.columns else pd.DataFrame()
                if df_sector.empty:
                    return
                df_sector['limit_pct'] = 0.50
                df_sector['status'] = df_sector['exposure_pct'].apply(
                    lambda v: 'OVER_LIMIT' if v > 0.50 else 'OK'
                )

            headers = {
                'sector':       'Sector',
                'exposure_pct': 'Exposure %',
                'trade_count':  'Trade Count',
                'limit_pct':    'Limit %',
                'status':       'Status',
            }
            formatters = {}
            if 'exposure_pct' in df_sector.columns:
                formatters['exposure_pct'] = _fmt_pct
            if 'limit_pct' in df_sector.columns:
                formatters['limit_pct'] = _fmt_pct

            self._sector_view.load_dataframe(df_sector, headers=headers, formatters=formatters)

            # Update sector warning
            if _PORTFOLIO_WIDGETS_OK and self._warn_sector is not None:
                over_sectors = []
                if 'status' in df_sector.columns and 'sector' in df_sector.columns:
                    over_sectors = df_sector[df_sector['status'] == 'OVER_LIMIT']['sector'].tolist()
                if over_sectors:
                    self._warn_sector.setText(
                        f"SECTOR CONCENTRATION WARNING: {', '.join(str(s) for s in over_sectors)} "
                        "exceeds sector exposure limit."
                    )
                    self._warn_sector.show()
                else:
                    self._warn_sector.hide()

        except Exception as exc:
            logger.warning("_refresh_sector_table: %s", exc)

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _set_buttons_enabled(self, enabled: bool):
        for btn in [self._btn_refresh, self._btn_balanced, self._btn_all]:
            btn.setEnabled(enabled)

    def _on_refresh(self):
        self._run_sim(scenario='balanced', run_all=False)

    def _on_run_balanced(self):
        self._run_sim(scenario='balanced', run_all=False)

    def _on_run_all(self):
        self._run_sim(scenario='balanced', run_all=True)

    def _run_sim(self, scenario: str, run_all: bool):
        if self._adapter is None:
            self._status_lbl.setText("Portfolio adapter not available.")
            return
        if self._sim_worker and self._sim_worker.isRunning():
            self._status_lbl.setText("Simulation already running…")
            return

        action = "all scenarios" if run_all else f"scenario={scenario}"
        self._status_lbl.setText(f"Running {action} [mode={self._mode}]…")
        self._set_buttons_enabled(False)

        self._sim_worker = _SimWorker(
            adapter=self._adapter,
            scenario=scenario,
            mode=self._mode,
            run_all=run_all,
        )
        self._sim_worker.finished.connect(self._on_sim_finished)
        self._sim_worker.error.connect(self._on_sim_error)
        self._sim_worker.start()

    def _on_sim_finished(self, result: dict):
        self._set_buttons_enabled(True)
        if result.get('status') == 'ok':
            self._status_lbl.setText(f"Done: {result.get('message', 'Simulation complete.')}")
            self._load_data()
        else:
            msg = result.get('message', 'Unknown error')
            self._status_lbl.setText(f"Simulation error: {msg}")
            logger.warning("PortfolioCockpitPanel: sim error: %s", msg)

    def _on_sim_error(self, msg: str):
        self._set_buttons_enabled(True)
        self._status_lbl.setText(f"Error: {msg}")
        logger.error("PortfolioCockpitPanel: worker error: %s", msg)

    def _on_open_report(self):
        if self._adapter is None:
            return
        path = self._adapter.load_latest_report_path()
        if not path:
            self._status_lbl.setText("No report found. Run a simulation first.")
            return
        try:
            import subprocess, sys
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
        except Exception as exc:
            self._status_lbl.setText(f"Cannot open report: {exc}")

    def _on_export_summary(self):
        if self._adapter is None:
            return
        try:
            import pandas as pd
            metrics = self._adapter.load_latest_metrics()
            if not metrics:
                self._status_lbl.setText("No metrics to export. Run a simulation first.")
                return
            from datetime import datetime as _dt
            ts = _dt.now().strftime('%Y%m%d_%H%M%S')
            out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   'data', 'backtest_results')
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f'portfolio_summary_export_{ts}.csv')
            pd.DataFrame([metrics]).to_csv(out_path, index=False, encoding='utf-8-sig')
            self._status_lbl.setText(f"Exported: {out_path}")
        except Exception as exc:
            self._status_lbl.setText(f"Export error: {exc}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode: str):
        """Update the displayed mode (called when dashboard mode changes)."""
        self._mode = mode
        if not _PYSIDE6_AVAILABLE:
            return
        mode_text = "REAL" if mode == 'real' else "MOCK"
        mode_color = "#FF8800" if mode == 'real' else "#33CCFF"
        self._mode_badge.setText(f"Mode: {mode_text}")
        self._mode_badge.setStyleSheet(f"font-weight:bold; color:{mode_color}; font-size:12px;")

    def refresh(self):
        """Public refresh trigger."""
        self._load_data()
