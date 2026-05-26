"""
gui/stock_detail_panel.py - Single-stock detail panel for TW Quant Cockpit.

Shows full stock information for the currently selected symbol:
price, data mode/source, completeness, bull score, lifecycle, buy point details.
"""

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _dash(v, fmt=None):
    """Return formatted value or '—' if None/empty."""
    if v is None or v == '' or v == '-' or v == 'N/A':
        return '—'
    if fmt:
        try:
            return fmt.format(v)
        except Exception:
            pass
    return str(v)


def _mode_color(mode_str: str) -> str:
    if 'REAL DATA CSV' in str(mode_str):
        return '#44CC88'
    if 'REAL DATA SAMPLE' in str(mode_str):
        return '#FFAA44'
    if 'MOCK' in str(mode_str):
        return '#33CCFF'
    return '#888888'


class StockDetailPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Shows detailed information for the selected stock.
    """

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()
        self._labels = {}

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)

        header = QLabel("個股詳情")
        header.setStyleSheet("font-weight:bold; font-size:13px; color:#AAAAFF;")
        outer.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#0E1520; border:none;")

        content = QWidget()
        self._vlayout = QVBoxLayout(content)
        self._vlayout.setSpacing(3)
        self._vlayout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(content)
        outer.addWidget(scroll)

        # Build field rows
        fields = [
            ('sym',          '股票代號'),
            ('name',         '股票名稱'),
            ('price',        '目前價格'),
            ('change_pct',   '漲跌幅'),
            ('data_mode',    '資料模式'),
            ('data_source',  '資料來源'),
            ('is_sample',    '是否 sample'),
            ('completeness', '資料完整度'),
            ('formal',       '正式判斷允許'),
            ('bull_score',   '飆股分數'),
            ('lifecycle',    '生命週期'),
            ('bp_grade',     '買點等級'),
            ('bp_type',      '買點型態'),
            ('bp_support',   '支撐價'),
            ('bp_confirm',   '確認價'),
            ('bp_invalid',   '失效價'),
            ('no_entry',     '不可進場警告'),
            ('deductions',   '扣分原因'),
            ('missing_data', '缺失資料'),
        ]

        for key, label in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}："))
            lbl = QLabel("—")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color:#CCCCCC;")
            self._labels[key] = lbl
            row.addWidget(lbl)
            row.addStretch()
            self._vlayout.addLayout(row)

        # Data sources section
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#333355;")
        self._vlayout.addWidget(sep)
        self._vlayout.addWidget(QLabel("資料來源細節："))

        src_fields = ['profile', 'daily', 'institutional', 'margin',
                      'monthly_revenue', 'holder', 'trust_cost']
        for sf in src_fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"  {sf}："))
            lbl = QLabel("—")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color:#888888; font-size:11px;")
            self._labels[f'src_{sf}'] = lbl
            row.addWidget(lbl)
            row.addStretch()
            self._vlayout.addLayout(row)

        self._vlayout.addStretch()

    def update(self, candidate: dict, tick: dict = None, data_sources: dict = None):
        """
        Update panel from candidate dict + optional tick + data_sources.

        Parameters
        ----------
        candidate : dict
            From screener or DataWorker (may be empty dict).
        tick : dict, optional
            Latest tick data from broker.
        data_sources : dict, optional
            From RealDataLoader.load_all()['_sources'].
        """
        if not _PYSIDE6_AVAILABLE:
            return

        c = candidate or {}
        t = tick or {}

        def _set(key, val, color=None):
            lbl = self._labels.get(key)
            if lbl:
                lbl.setText(_dash(val))
                if color:
                    lbl.setStyleSheet(f"color:{color};")
                else:
                    lbl.setStyleSheet("color:#CCCCCC;")

        sym = c.get('symbol', t.get('symbol', ''))
        _set('sym',  sym)
        _set('name', c.get('name', t.get('name', sym)))

        price = t.get('price') or c.get('price') or c.get('latest_close')
        _set('price', f"{float(price):.1f}" if price else None)

        chg = t.get('change_pct')
        if chg is not None:
            try:
                chg_f = float(chg)
                color = '#FF4444' if chg_f > 0 else ('#33CC66' if chg_f < 0 else '#AAAAAA')
                _set('change_pct', f"{chg_f:+.2f}%", color=color)
            except Exception:
                _set('change_pct', None)
        else:
            _set('change_pct', None)

        # Data mode
        data_source_val = c.get('data_source', 'mock')
        if data_sources:
            any_sample = any(
                v and v.get('is_sample', True)
                for v in data_sources.values() if v
            )
            any_real = any(v is not None for v in data_sources.values())
            if any_real and not any_sample:
                mode_str = 'REAL DATA CSV'
            elif any_real:
                mode_str = 'REAL DATA SAMPLE'
            else:
                mode_str = 'REAL DATA MISSING'
        elif data_source_val == 'real':
            mode_str = 'REAL DATA'
        else:
            mode_str = 'MOCK DATA'
        _set('data_mode', mode_str, color=_mode_color(mode_str))

        _set('data_source', data_source_val)

        if data_sources:
            any_sample = any(
                v and v.get('is_sample', True)
                for v in data_sources.values() if v
            )
            _set('is_sample', '是 (sample)' if any_sample else '否')
        else:
            _set('is_sample', None)

        # Completeness (from screener or data_check)
        comp = c.get('data_completeness')
        _set('completeness', f"{float(comp):.0f}%" if comp is not None else None)

        formal = c.get('formal_allowed')
        if formal is not None:
            _set('formal', '✓ 允許' if formal else '✗ 不允許（資料不足）',
                 color='#44CC88' if formal else '#FF8888')
        else:
            _set('formal', None)

        score = c.get('bull_stock_score')
        if score is not None:
            try:
                s = float(score)
                color = '#FF4444' if s >= 80 else ('#FF8800' if s >= 65 else ('#CCCC00' if s >= 50 else '#888888'))
                _set('bull_score', f"{s:.1f}/100", color=color)
            except Exception:
                _set('bull_score', score)
        else:
            _set('bull_score', None)

        # Lifecycle from bull score
        lifecycle = _infer_lifecycle(score, c)
        _set('lifecycle', lifecycle)

        # Buy point
        bp_grade = c.get('buy_point_grade')
        grade_colors = {'A': '#FF4444', 'B': '#FF8800', 'C': '#CCCC00'}
        _set('bp_grade', bp_grade, color=grade_colors.get(str(bp_grade), '#AAAAAA'))
        _set('bp_type',    c.get('buy_point_type'))
        _set('bp_support', c.get('support_price'))
        _set('bp_confirm', c.get('confirm_price'))
        _set('bp_invalid', c.get('invalid_price'))

        no_entry = c.get('no_entry_conditions', [])
        if isinstance(no_entry, (list, tuple)) and no_entry:
            _set('no_entry', ' / '.join(str(x) for x in no_entry), color='#FF8888')
        else:
            _set('no_entry', None)

        deductions = c.get('deduction_reasons', [])
        if isinstance(deductions, (list, tuple)) and deductions:
            _set('deductions', ' / '.join(str(x) for x in deductions))
        else:
            _set('deductions', '無')

        missing = c.get('missing_data_reasons', [])
        if isinstance(missing, (list, tuple)) and missing:
            _set('missing_data', ' / '.join(str(x) for x in missing), color='#FF8888')
        else:
            _set('missing_data', '無')

        # Data source details
        src_fields = ['profile', 'daily', 'institutional', 'margin',
                      'monthly_revenue', 'holder', 'trust_cost']
        for sf in src_fields:
            lbl = self._labels.get(f'src_{sf}')
            if lbl:
                if data_sources and data_sources.get(sf):
                    src = data_sources[sf]
                    path = src.get('source_file', '—')
                    tag = ' (sample)' if src.get('is_sample') else ''
                    lbl.setText(f"{path}{tag}")
                    lbl.setStyleSheet(
                        "color:#FFAA44; font-size:11px;" if src.get('is_sample')
                        else "color:#44CC88; font-size:11px;"
                    )
                else:
                    lbl.setText("—")
                    lbl.setStyleSheet("color:#888888; font-size:11px;")

    def clear(self):
        if not _PYSIDE6_AVAILABLE:
            return
        for lbl in self._labels.values():
            lbl.setText("—")
            lbl.setStyleSheet("color:#888888;")


def _infer_lifecycle(score, candidate: dict) -> str:
    """Infer lifecycle phase from score or candidate fields."""
    try:
        if score is not None:
            s = float(score)
            if s >= 80:
                return "主升段 — 飆股候選，強勢股"
            elif s >= 65:
                return "初升段 / 第二波 — 可布局"
            elif s >= 50:
                return "盤整觀察 — 等待突破確認"
            else:
                return "弱勢 / 避開 — 建議觀望"
    except Exception:
        pass
    decision = candidate.get('decision', '')
    if decision in ('BUY_BREAKOUT', 'BUY_PULLBACK'):
        return "初升段 — 短線信號積極"
    return "不明 — 資料不足"
