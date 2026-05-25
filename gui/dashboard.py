"""
gui/dashboard.py - TW Quant Cockpit v1 Main Dashboard (PySide6).

Launch via:
    python main.py cockpit

Features:
  - 大盤狀態區  (Market status bar)
  - 股票監控表  (Stock monitoring table)
  - 飆股候選   (Bull candidates panel)
  - 個股五檔   (Order book panel)
  - 分析評分   (Scores panel)
  - AI 建議    (Decision panel)
  - 模擬持倉   (Paper positions panel)
  - 今日損益   (Today P&L)
  - Log 視窗   (Log window)

All data comes from MockBroker / screener_pipeline in mock mode.
Real-order execution is NOT implemented and is explicitly blocked.
"""

import sys
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PySide6 availability guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QSplitter, QLabel, QTableWidget, QTableWidgetItem, QTextEdit,
        QGroupBox, QPushButton, QHeaderView, QSizePolicy, QStatusBar,
        QTabWidget, QFrame,
    )
    from PySide6.QtCore import Qt, QTimer, Signal, QThread
    from PySide6.QtGui import QColor, QFont, QPalette
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.error("PySide6 not installed. Run: pip install PySide6")


# ---------------------------------------------------------------------------
# Colour helpers (Taiwan convention: red = up, green = down)
# ---------------------------------------------------------------------------

def _change_color(pct: float) -> str:
    if pct > 0:
        return "#FF4444"   # red = up
    if pct < 0:
        return "#33CC66"   # green = down
    return "#AAAAAA"


def _score_color(score: float) -> str:
    if score >= 80:
        return "#FF4444"
    if score >= 65:
        return "#FF8800"
    if score >= 50:
        return "#CCCC00"
    return "#888888"


# ---------------------------------------------------------------------------
# Data refresh worker (runs in background thread)
# ---------------------------------------------------------------------------

class DataWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Background thread that fetches mock market data every N seconds."""

    if _PYSIDE6_AVAILABLE:
        data_ready = Signal(dict)

    def __init__(self, broker, screener_pipeline, paper_trader, interval=3):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self.broker = broker
        self.screener_pipeline = screener_pipeline
        self.paper_trader = paper_trader
        self.interval = interval
        self._running = False

    def run(self):
        import time
        self._running = True
        while self._running:
            try:
                payload = self._fetch()
                if _PYSIDE6_AVAILABLE:
                    self.data_ready.emit(payload)
            except Exception as exc:
                logger.error("DataWorker error: %s", exc)
            time.sleep(self.interval)

    def stop(self):
        self._running = False

    def _fetch(self) -> dict:
        """Collect all data needed by the dashboard."""
        # Market snapshot from mock broker
        market = self.broker.get_market_snapshot() if self.broker else {}

        # Screener top candidates
        try:
            candidates = self.screener_pipeline.run() if self.screener_pipeline else []
        except Exception:
            candidates = []

        # Paper trader summary
        try:
            positions = self.paper_trader.get_positions() if self.paper_trader else []
            pnl_summary = self.paper_trader.get_pnl_summary() if self.paper_trader else {}
        except Exception:
            positions = []
            pnl_summary = {}

        # Per-symbol tick data
        ticks = {}
        if self.broker:
            for sym in self.broker.get_symbols():
                try:
                    ticks[sym] = self.broker.get_tick(sym)
                except Exception:
                    pass

        return {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'market': market,
            'candidates': candidates,
            'positions': positions,
            'pnl_summary': pnl_summary,
            'ticks': ticks,
        }


# ---------------------------------------------------------------------------
# Helper: styled QLabel
# ---------------------------------------------------------------------------

def _label(text, bold=False, color=None, size=None):
    lbl = QLabel(text)
    style_parts = []
    if bold:
        style_parts.append("font-weight:bold")
    if color:
        style_parts.append(f"color:{color}")
    if size:
        style_parts.append(f"font-size:{size}px")
    if style_parts:
        lbl.setStyleSheet(";".join(style_parts))
    return lbl


# ---------------------------------------------------------------------------
# Market Status Bar widget
# ---------------------------------------------------------------------------

class MarketStatusBar(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows TAIEX index, date/time, and market session state."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)

        self._lbl_title = _label("TW Quant Cockpit v1", bold=True, size=16)
        self._lbl_time = _label("--:--:--", color="#AAAAAA")
        self._lbl_taiex = _label("加權指數: ---", bold=True, color="#FF8800", size=13)
        self._lbl_mode = _label("[MOCK MODE]", bold=True, color="#33CCFF")
        self._lbl_session = _label("盤前", color="#AAAAAA")

        layout.addWidget(self._lbl_title)
        layout.addSpacing(20)
        layout.addWidget(self._lbl_taiex)
        layout.addSpacing(10)
        layout.addWidget(self._lbl_session)
        layout.addStretch()
        layout.addWidget(self._lbl_mode)
        layout.addSpacing(10)
        layout.addWidget(self._lbl_time)

        self.setStyleSheet("background:#1E1E2E; border-radius:4px; padding:2px")

    def update(self, market: dict, timestamp: str):
        if not _PYSIDE6_AVAILABLE:
            return
        self._lbl_time.setText(timestamp)
        taiex = market.get('taiex', 0)
        taiex_chg = market.get('taiex_change_pct', 0)
        color = _change_color(taiex_chg)
        self._lbl_taiex.setText(f"加權指數: {taiex:,.0f}  ({taiex_chg:+.2f}%)")
        self._lbl_taiex.setStyleSheet(f"font-weight:bold;color:{color};font-size:13px")
        session = market.get('session', '盤前')
        self._lbl_session.setText(session)


# ---------------------------------------------------------------------------
# Stock Monitoring Table
# ---------------------------------------------------------------------------

_TABLE_COLS = [
    'symbol', 'name', 'price', 'change_pct',
    'bull_score', 'daytrade_score', 'swing_score', 'risk_score',
    'orderbook_state', 'decision', 'position', 'pnl',
]
_TABLE_HEADERS = [
    '代號', '名稱', '價格', '漲跌%',
    '飆股分', '當沖分', '波段分', '風險分',
    '五檔狀態', '建議', '持倉', '損益',
]


class StockTable(QWidget if _PYSIDE6_AVAILABLE else object):
    """Main stock monitoring table."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()
        self._rows = {}   # symbol -> row_index

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = _label("股票監控表", bold=True, size=12)
        layout.addWidget(header)

        self._table = QTableWidget()
        self._table.setColumnCount(len(_TABLE_COLS))
        self._table.setHorizontalHeaderLabels(_TABLE_HEADERS)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setStyleSheet("""
            QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
            QTableWidget::item:alternate { background:#1A1A2E; }
            QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
        """)
        layout.addWidget(self._table)

    def update(self, ticks: dict, candidates: list, positions: list):
        if not _PYSIDE6_AVAILABLE:
            return

        # Build a lookup for candidate scores
        cand_map = {str(c.get('symbol', '')): c for c in candidates}
        pos_map = {}
        for p in positions:
            sym = str(p.get('symbol', ''))
            pos_map[sym] = p

        # Merge symbols from ticks + candidates + positions
        all_syms = list(dict.fromkeys(
            list(ticks.keys()) +
            [str(c.get('symbol', '')) for c in candidates] +
            list(pos_map.keys())
        ))

        self._table.setRowCount(len(all_syms))

        for row, sym in enumerate(all_syms):
            tick = ticks.get(sym, {})
            cand = cand_map.get(sym, {})
            pos = pos_map.get(sym, {})

            price = tick.get('price', cand.get('price', 0)) or 0
            change_pct = tick.get('change_pct', 0) or 0
            name = tick.get('name', cand.get('name', sym))
            bull_score = cand.get('bull_stock_score', 0)
            daytrade_score = cand.get('daytrade_score', 0)
            swing_score = cand.get('swing_score', 0)
            risk_score = cand.get('risk_score', 0)
            ob_state = cand.get('orderbook_state', '-')
            decision = cand.get('decision', '-')
            position = pos.get('quantity', 0)
            pnl = pos.get('unrealized_pnl', 0)

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            chg_color = _change_color(change_pct)

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{price:.1f}" if price else '-'))
            self._table.setItem(row, 3, _cell(f"{change_pct:+.2f}%" if change_pct else '-', color=chg_color))
            self._table.setItem(row, 4, _cell(f"{bull_score:.0f}" if bull_score else '-', color=_score_color(bull_score)))
            self._table.setItem(row, 5, _cell(f"{daytrade_score:.0f}" if daytrade_score else '-'))
            self._table.setItem(row, 6, _cell(f"{swing_score:.0f}" if swing_score else '-'))
            self._table.setItem(row, 7, _cell(f"{risk_score:.0f}" if risk_score else '-'))
            self._table.setItem(row, 8, _cell(ob_state))
            self._table.setItem(row, 9, _cell(decision))
            self._table.setItem(row, 10, _cell(str(position) if position else '-'))
            pnl_color = _change_color(pnl)
            self._table.setItem(row, 11, _cell(f"{pnl:+,.0f}" if pnl else '-', color=pnl_color))


# ---------------------------------------------------------------------------
# Bull Candidates Panel
# ---------------------------------------------------------------------------

class CandidatesPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows top 3-8 bull candidates with scores."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("飆股候選 Top 3~8", bold=True, size=12, color="#FF8800")
        layout.addWidget(header)

        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(['代號', '名稱', '綜合分', '主題', '建議'])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setMaximumHeight(260)
        self._table.setStyleSheet("""
            QTableWidget { background:#0E1520; color:#EEEEEE; }
            QHeaderView::section { background:#252540; color:#FFAA44; font-weight:bold; }
        """)
        layout.addWidget(self._table)
        layout.addStretch()

    def update(self, candidates: list):
        if not _PYSIDE6_AVAILABLE:
            return
        top = candidates[:8]
        self._table.setRowCount(len(top))
        for row, c in enumerate(top):
            sym = str(c.get('symbol', ''))
            name = str(c.get('name', sym))
            score = float(c.get('bull_stock_score', 0))
            themes = ','.join(c.get('theme_tags', [])) if c.get('theme_tags') else '-'
            decision = str(c.get('decision', '-'))

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{score:.0f}", color=_score_color(score)))
            self._table.setItem(row, 3, _cell(themes))
            self._table.setItem(row, 4, _cell(decision))


# ---------------------------------------------------------------------------
# Order Book Panel
# ---------------------------------------------------------------------------

class OrderBookPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows 5-level bid/ask for a selected symbol."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("五檔委買委賣", bold=True, size=12)
        layout.addWidget(header)

        self._sym_label = _label("---", color="#AAAAFF", size=11)
        layout.addWidget(self._sym_label)

        # Bid table (委買)
        layout.addWidget(_label("委買", color="#FF5555"))
        self._bid_table = self._make_table()
        layout.addWidget(self._bid_table)

        # Ask table (委賣)
        layout.addWidget(_label("委賣", color="#55CC55"))
        self._ask_table = self._make_table()
        layout.addWidget(self._ask_table)

        layout.addStretch()

    def _make_table(self):
        t = QTableWidget(5, 2)
        t.setHorizontalHeaderLabels(['價格', '數量'])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.setMaximumHeight(160)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setStyleSheet("QTableWidget { background:#0E1520; color:#EEEEEE; } QHeaderView::section { background:#252540; }")
        return t

    def update(self, symbol: str, bidask: dict):
        if not _PYSIDE6_AVAILABLE:
            return
        self._sym_label.setText(f"代號：{symbol}")

        for i in range(1, 6):
            row = i - 1
            bp = bidask.get(f'bid_price_{i}', '-')
            bv = bidask.get(f'bid_volume_{i}', '-')
            ap = bidask.get(f'ask_price_{i}', '-')
            av = bidask.get(f'ask_volume_{i}', '-')

            self._bid_table.setItem(row, 0, QTableWidgetItem(str(bp)))
            self._bid_table.setItem(row, 1, QTableWidgetItem(str(bv)))
            self._ask_table.setItem(row, 0, QTableWidgetItem(str(ap)))
            self._ask_table.setItem(row, 1, QTableWidgetItem(str(av)))


# ---------------------------------------------------------------------------
# Score / Decision Panel
# ---------------------------------------------------------------------------

class ScorePanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows scores and AI decision for a selected stock."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("評分 & 建議", bold=True, size=12)
        layout.addWidget(header)

        self._sym_label = _label("---", color="#AAAAFF", size=11)
        layout.addWidget(self._sym_label)

        rows_data = [
            ('飆股分', '_lbl_bull'),
            ('當沖分', '_lbl_daytrade'),
            ('波段分', '_lbl_swing'),
            ('風險分', '_lbl_risk'),
            ('建議',   '_lbl_decision'),
        ]
        for label_text, attr in rows_data:
            row = QHBoxLayout()
            row.addWidget(_label(f"{label_text}：", bold=True))
            lbl = _label('---')
            setattr(self, attr, lbl)
            row.addWidget(lbl)
            row.addStretch()
            layout.addLayout(row)

        layout.addSpacing(8)
        layout.addWidget(_label("判斷依據：", bold=True))
        self._txt_reasoning = QTextEdit()
        self._txt_reasoning.setReadOnly(True)
        self._txt_reasoning.setMaximumHeight(100)
        self._txt_reasoning.setStyleSheet("background:#0E1520; color:#CCCCCC; font-size:11px")
        layout.addWidget(self._txt_reasoning)

        layout.addStretch()

    def update(self, symbol: str, candidate: dict):
        if not _PYSIDE6_AVAILABLE:
            return
        self._sym_label.setText(f"代號：{symbol}")

        bull = candidate.get('bull_stock_score', 0)
        dt = candidate.get('daytrade_score', 0)
        sw = candidate.get('swing_score', 0)
        risk = candidate.get('risk_score', 0)
        decision = candidate.get('decision', '---')
        reasoning = candidate.get('reason_summary', candidate.get('reasoning', '資料不足，只能做盤中初估，不能當正式短中長線操作依據'))

        def _set_score(lbl, val):
            lbl.setText(f"{val:.0f}" if val else '---')
            lbl.setStyleSheet(f"color:{_score_color(float(val or 0))};font-weight:bold")

        _set_score(self._lbl_bull, bull)
        _set_score(self._lbl_daytrade, dt)
        _set_score(self._lbl_swing, sw)
        _set_score(self._lbl_risk, risk)
        self._lbl_decision.setText(str(decision))
        self._txt_reasoning.setPlainText(str(reasoning))


# ---------------------------------------------------------------------------
# Paper Positions Panel
# ---------------------------------------------------------------------------

class PositionsPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows current paper trading positions and P&L."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("模擬持倉", bold=True, size=12)
        layout.addWidget(header)

        self._pnl_label = _label("今日損益: ---", bold=True, size=13, color="#FFAA44")
        layout.addWidget(self._pnl_label)

        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(['代號', '名稱', '均成本', '現價', '持倉', '浮動損益'])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setMaximumHeight(200)
        self._table.setStyleSheet("""
            QTableWidget { background:#0E1520; color:#EEEEEE; }
            QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
        """)
        layout.addWidget(self._table)
        layout.addStretch()

    def update(self, positions: list, pnl_summary: dict):
        if not _PYSIDE6_AVAILABLE:
            return

        today_pnl = pnl_summary.get('realized_pnl', 0) + pnl_summary.get('unrealized_pnl', 0)
        pnl_color = _change_color(today_pnl)
        self._pnl_label.setText(f"今日損益: {today_pnl:+,.0f} NTD")
        self._pnl_label.setStyleSheet(f"font-weight:bold;font-size:13px;color:{pnl_color}")

        self._table.setRowCount(len(positions))
        for row, pos in enumerate(positions):
            sym = str(pos.get('symbol', ''))
            name = str(pos.get('name', sym))
            cost = float(pos.get('avg_cost', 0) or 0)
            price = float(pos.get('current_price', 0) or 0)
            qty = int(pos.get('quantity', 0) or 0)
            upnl = float(pos.get('unrealized_pnl', 0) or 0)

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{cost:.1f}"))
            self._table.setItem(row, 3, _cell(f"{price:.1f}"))
            self._table.setItem(row, 4, _cell(str(qty)))
            self._table.setItem(row, 5, _cell(f"{upnl:+,.0f}", color=_change_color(upnl)))


# ---------------------------------------------------------------------------
# Log Window
# ---------------------------------------------------------------------------

class LogPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Scrollable log output panel."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("系統 Log", bold=True)
        layout.addWidget(header)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setMaximumHeight(130)
        self._text.setStyleSheet(
            "background:#0A0A14; color:#88FF88; font-family:monospace; font-size:11px"
        )
        layout.addWidget(self._text)

    def append(self, msg: str):
        if not _PYSIDE6_AVAILABLE:
            return
        ts = datetime.now().strftime('%H:%M:%S')
        self._text.append(f"[{ts}] {msg}")
        # Auto-scroll
        sb = self._text.verticalScrollBar()
        sb.setValue(sb.maximum())


# ---------------------------------------------------------------------------
# Qt Log Handler
# ---------------------------------------------------------------------------

class _QLogHandler(logging.Handler if _PYSIDE6_AVAILABLE else object):
    """Redirect Python logging to the LogPanel."""

    def __init__(self, log_panel):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self.log_panel = log_panel

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_panel.append(msg)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------

class CockpitWindow(QMainWindow if _PYSIDE6_AVAILABLE else object):
    """TW Quant Cockpit v1 Main Window."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()

        self._broker = None
        self._screener = None
        self._paper_trader = None
        self._worker = None
        self._candidates = []
        self._ticks = {}
        self._selected_symbol = None

        self._init_backends()
        if _PYSIDE6_AVAILABLE:
            self._build_ui()
            self._start_worker()

    # ---- Backend init ----

    def _init_backends(self):
        """Initialize mock broker, screener, and paper trader."""
        try:
            from broker.mock_broker import MockBroker
            import os
            wl = os.path.join(os.path.dirname(__file__), '..', 'config', 'watchlist.csv')
            self._broker = MockBroker(watchlist_path=wl)
            logger.info("MockBroker initialized.")
        except Exception as exc:
            logger.warning("MockBroker init failed: %s", exc)

        try:
            from screener.screener_pipeline import ScreenerPipeline
            self._screener = ScreenerPipeline()
        except Exception as exc:
            logger.warning("Screener init failed: %s", exc)

        try:
            from sim.simulator import PaperTrader
            self._paper_trader = PaperTrader(initial_capital=1_000_000)
            logger.info("PaperTrader initialized.")
        except Exception as exc:
            logger.warning("PaperTrader init failed: %s", exc)

    # ---- UI Build ----

    def _build_ui(self):
        self.setWindowTitle("TW Quant Cockpit v1  [MOCK MODE — 禁止實盤下單]")
        self.resize(1400, 900)
        self.setStyleSheet("background:#12121E; color:#DDDDDD;")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(4)
        root.setContentsMargins(6, 6, 6, 6)

        # ---- Market status bar ----
        self._market_bar = MarketStatusBar()
        root.addWidget(self._market_bar)

        # ---- Main content splitter (left | right) ----
        h_split = QSplitter(Qt.Horizontal)

        # LEFT: stock table + candidates
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self._stock_table = StockTable()
        left_layout.addWidget(self._stock_table, stretch=3)

        self._candidates_panel = CandidatesPanel()
        left_layout.addWidget(self._candidates_panel, stretch=2)

        h_split.addWidget(left)

        # RIGHT: tabs for details
        right_tabs = QTabWidget()
        right_tabs.setMaximumWidth(450)
        right_tabs.setStyleSheet("QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }")

        self._ob_panel = OrderBookPanel()
        right_tabs.addTab(self._ob_panel, "五檔")

        self._score_panel = ScorePanel()
        right_tabs.addTab(self._score_panel, "評分")

        self._pos_panel = PositionsPanel()
        right_tabs.addTab(self._pos_panel, "持倉")

        h_split.addWidget(right_tabs)
        h_split.setStretchFactor(0, 3)
        h_split.setStretchFactor(1, 1)

        root.addWidget(h_split, stretch=5)

        # ---- Bottom: log panel ----
        self._log_panel = LogPanel()
        root.addWidget(self._log_panel, stretch=1)

        # ---- Status bar ----
        sb = QStatusBar()
        sb.showMessage("⚠ 第一版禁止實盤自動下單。本系統僅供研究、模擬交易與決策輔助，不構成投資建議。")
        sb.setStyleSheet("color:#FF8888; background:#1A0A0A")
        self.setStatusBar(sb)

        # ---- Attach log handler ----
        handler = _QLogHandler(self._log_panel)
        handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(message)s'))
        logging.getLogger().addHandler(handler)

        self._log_panel.append("TW Quant Cockpit v1 啟動 [MOCK MODE]")
        self._log_panel.append("⚠ 第一版禁止實盤自動下單")

    # ---- Worker ----

    def _start_worker(self):
        if not _PYSIDE6_AVAILABLE:
            return

        class _ScreenerWrapper:
            @staticmethod
            def run():
                try:
                    from screener.screener_pipeline import ScreenerPipeline
                    p = ScreenerPipeline()
                    p.run(mock_data=True)
                    return p.get_top_candidates(n=8)
                except Exception:
                    return []

        class _BrokerWrapper:
            def __init__(self, broker):
                self._b = broker

            def get_market_snapshot(self):
                if self._b and hasattr(self._b, 'get_market_snapshot'):
                    return self._b.get_market_snapshot()
                import random
                return {
                    'taiex': 21500 + random.randint(-200, 200),
                    'taiex_change_pct': random.uniform(-1.5, 1.5),
                    'session': '盤中',
                }

            def get_symbols(self):
                if self._b and hasattr(self._b, 'get_symbols'):
                    return self._b.get_symbols()
                return []

            def get_tick(self, sym):
                if self._b and hasattr(self._b, 'get_tick'):
                    return self._b.get_tick(sym)
                return {}

        class _PaperWrapper:
            def __init__(self, pt):
                self._pt = pt

            def get_positions(self):
                if self._pt and hasattr(self._pt, 'get_positions'):
                    return self._pt.get_positions()
                return []

            def get_pnl_summary(self):
                if self._pt and hasattr(self._pt, 'get_pnl_summary'):
                    return self._pt.get_pnl_summary()
                return {}

        self._worker = DataWorker(
            broker=_BrokerWrapper(self._broker),
            screener_pipeline=_ScreenerWrapper(),
            paper_trader=_PaperWrapper(self._paper_trader),
            interval=5,
        )
        self._worker.data_ready.connect(self._on_data)
        self._worker.start()

    def _on_data(self, payload: dict):
        """Called from worker thread with fresh data."""
        try:
            ts = payload.get('timestamp', '')
            market = payload.get('market', {})
            candidates = payload.get('candidates', [])
            ticks = payload.get('ticks', {})
            positions = payload.get('positions', [])
            pnl_summary = payload.get('pnl_summary', {})

            self._candidates = candidates
            self._ticks = ticks

            self._market_bar.update(market, ts)
            self._stock_table.update(ticks, candidates, positions)
            self._candidates_panel.update(candidates)
            self._pos_panel.update(positions, pnl_summary)

            # Update detail panels for first candidate or selected symbol
            sym = self._selected_symbol
            if not sym and candidates:
                sym = str(candidates[0].get('symbol', ''))
            if sym:
                tick = ticks.get(sym, {})
                cand = next((c for c in candidates if str(c.get('symbol', '')) == sym), {})
                bidask = tick.get('bidask', {})
                self._ob_panel.update(sym, bidask)
                self._score_panel.update(sym, cand)

        except Exception as exc:
            logger.error("Dashboard update error: %s\n%s", exc, traceback.format_exc())

    def closeEvent(self, event):
        if self._worker:
            self._worker.stop()
            self._worker.wait(2000)
        if _PYSIDE6_AVAILABLE:
            super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def launch():
    """Launch the Cockpit GUI. Called by main.py cockpit command."""
    if not _PYSIDE6_AVAILABLE:
        print("ERROR: PySide6 is required to run the Cockpit GUI.")
        print("Install with: pip install PySide6")
        return

    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#12121E"))
    palette.setColor(QPalette.WindowText, QColor("#DDDDDD"))
    palette.setColor(QPalette.Base, QColor("#0E1520"))
    palette.setColor(QPalette.AlternateBase, QColor("#1A1A2E"))
    palette.setColor(QPalette.Text, QColor("#EEEEEE"))
    palette.setColor(QPalette.Button, QColor("#252540"))
    palette.setColor(QPalette.ButtonText, QColor("#EEEEEE"))
    palette.setColor(QPalette.Highlight, QColor("#3344AA"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    window = CockpitWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    launch()
