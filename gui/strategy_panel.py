"""
gui/strategy_panel.py - Four-timeframe strategy panel for TW Quant Cockpit.

Shows daytrade, short-term, mid-term, and long-term strategy information
for the selected stock, including entry prices, stop-loss, and conditions.
"""

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QScrollArea,
        QFrame,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _dash(v):
    """Return '—' for None/empty/'-'."""
    if v is None or v == '' or v == '-' or v == 'N/A':
        return '—'
    return str(v)


def _lbl(text, bold=False, color=None, wrap=True):
    l = QLabel(text)
    if wrap:
        l.setWordWrap(True)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if parts:
        l.setStyleSheet(";".join(parts))
    return l


class _SingleStrategyWidget(QWidget if _PYSIDE6_AVAILABLE else object):
    """One tab showing a single timeframe strategy result."""

    def __init__(self, timeframe_label: str):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self._tf = timeframe_label
        if _PYSIDE6_AVAILABLE:
            self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#0E1520; border:none;")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        self._rows = {}
        fields = [
            ('decision',     '操作決策'),
            ('confidence',   '信心度'),
            ('add_price',    '補倉價位'),
            ('exit_price',   '出倉價位'),
            ('stop_price',   '停損價位'),
            ('no_entry',     '不可進場條件'),
            ('reasoning',    '判斷依據'),
            ('completeness', '資料完整度'),
            ('formal',       '是否允許正式判斷'),
            ('warning',      '資料警告'),
        ]

        for key, label in fields:
            row = QHBoxLayout()
            key_lbl = _lbl(f"{label}：", bold=True, color="#AAAAAA", wrap=False)
            key_lbl.setFixedWidth(130)
            row.addWidget(key_lbl)
            val_lbl = _lbl("—")
            val_lbl.setStyleSheet("color:#CCCCCC;")
            self._rows[key] = val_lbl
            row.addWidget(val_lbl)
            layout.addLayout(row)

        layout.addStretch()

    def update(self, result: dict, mode: str = 'mock'):
        """Update from analyzer result dict."""
        if not _PYSIDE6_AVAILABLE:
            return
        if not result:
            self.clear()
            return

        r = result

        def _set(key, val, color=None):
            lbl = self._rows.get(key)
            if lbl:
                lbl.setText(_dash(val))
                lbl.setStyleSheet(f"color:{color};" if color else "color:#CCCCCC;")

        decision = r.get('decision', '—')
        confidence = r.get('confidence', 0)
        data_source = r.get('data_source', 'mock')
        suppress = (mode == 'real' and data_source == 'mock')

        src_tag = ' 🟡[MOCK]' if data_source == 'mock' else ' 🟢[REAL]'
        _set('decision', f"{decision}{src_tag}", color='#FF8800' if decision not in ('AVOID', 'HOLD', '—') else '#CCCCCC')
        _set('confidence', f"{confidence}%" if confidence else None)

        def _price(key, val):
            if suppress or val is None:
                txt = '— （real mode 缺真實資料）' if suppress else '—'
                _set(key, txt, color='#888888')
            else:
                is_est = r.get('prices_are_estimates', True)
                note = '（估算值）' if is_est else ''
                _set(key, f"{val}{note}")

        _price('add_price',  r.get('add_position_price'))
        _price('exit_price', r.get('exit_price'))
        _price('stop_price', r.get('stop_loss_price'))

        no_entry = r.get('no_entry_conditions', [])
        if isinstance(no_entry, (list, tuple)) and no_entry:
            _set('no_entry', ' / '.join(str(x) for x in no_entry), color='#FF8888')
        elif suppress:
            _set('no_entry', '缺少真實資料，禁止正式進場判斷', color='#FF8888')
        else:
            _set('no_entry', '無')

        _set('reasoning', r.get('reasoning'))

        comp = r.get('data_completeness', 0)
        _set('completeness', f"{float(comp):.0f}%" if comp is not None else None)

        formal = not r.get('prices_are_estimates', True)
        _set('formal', '✓ 是' if formal else '✗ 否', color='#44CC88' if formal else '#FF8888')

        warning = r.get('warning')
        if warning:
            _set('warning', warning, color='#FF8888')
        else:
            _set('warning', None)

    def clear(self):
        if not _PYSIDE6_AVAILABLE:
            return
        for lbl in self._rows.values():
            lbl.setText("—")
            lbl.setStyleSheet("color:#888888;")


class StrategyPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Four-tab strategy panel: 當沖 / 短線 / 中線 / 長線.
    """

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("策略與風控")
        header.setStyleSheet("font-weight:bold; font-size:12px; color:#AAAAFF; padding:4px;")
        layout.addWidget(header)

        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 12px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )

        self._daytrade   = _SingleStrategyWidget("當沖")
        self._short      = _SingleStrategyWidget("短線")
        self._mid        = _SingleStrategyWidget("中線")
        self._long       = _SingleStrategyWidget("長線")

        self._tabs.addTab(self._daytrade,  "當沖")
        self._tabs.addTab(self._short,     "短線（5-20日）")
        self._tabs.addTab(self._mid,       "中線（1-3月）")
        self._tabs.addTab(self._long,      "長線（3-12月）")

        layout.addWidget(self._tabs)

    def update(self, daytrade=None, short=None, mid=None, long_=None, mode='mock'):
        """Update all four tabs."""
        if not _PYSIDE6_AVAILABLE:
            return
        self._daytrade.update(daytrade, mode=mode)
        self._short.update(short,     mode=mode)
        self._mid.update(mid,         mode=mode)
        self._long.update(long_,      mode=mode)

    def clear(self):
        if not _PYSIDE6_AVAILABLE:
            return
        self._daytrade.clear()
        self._short.clear()
        self._mid.clear()
        self._long.clear()
