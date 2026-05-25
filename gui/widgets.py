"""
gui/widgets.py - PySide6 widget helper functions for TW Quant Cockpit.
"""

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not installed. Widget functions will return None.")


def create_stock_table(data):
    """
    Create a QTableWidget from a list of dicts.

    Parameters
    ----------
    data : list of dicts
        Each dict represents a row. Keys become column headers.

    Returns
    -------
    QTableWidget or None (if PySide6 not available)
    """
    if not _PYSIDE6_AVAILABLE or not data:
        return None

    try:
        columns = list(data[0].keys()) if data else []
        table = QTableWidget(len(data), len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)

        for row_idx, row_data in enumerate(data):
            for col_idx, col in enumerate(columns):
                val = row_data.get(col, '')
                if isinstance(val, float):
                    item = QTableWidgetItem(f'{val:.2f}')
                elif isinstance(val, list):
                    item = QTableWidgetItem(', '.join(str(v) for v in val))
                else:
                    item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        return table

    except Exception as exc:
        logger.error("create_stock_table error: %s", exc)
        return None


def create_score_label(score, thresholds=None):
    """
    Create a colored QLabel for a numeric score.

    Parameters
    ----------
    score : float
        Score value to display.
    thresholds : dict, optional
        {'red': 80, 'orange': 65, 'yellow': 50}
        Score >= red -> red, >= orange -> orange, etc.

    Returns
    -------
    QLabel or None
    """
    if not _PYSIDE6_AVAILABLE:
        return None

    try:
        thresholds = thresholds or {'red': 80, 'orange': 65, 'yellow': 50}
        score_val = float(score or 0)

        if score_val >= thresholds.get('red', 80):
            color = '#FF4444'
            text_color = 'white'
        elif score_val >= thresholds.get('orange', 65):
            color = '#FF8800'
            text_color = 'white'
        elif score_val >= thresholds.get('yellow', 50):
            color = '#FFCC00'
            text_color = 'black'
        else:
            color = '#888888'
            text_color = 'white'

        label = QLabel(f'{score_val:.1f}')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            f'background-color: {color}; color: {text_color}; '
            f'border-radius: 4px; padding: 2px 6px; font-weight: bold;'
        )
        return label

    except Exception as exc:
        logger.error("create_score_label error: %s", exc)
        return None


def create_status_bar_widget(text, color='green'):
    """
    Create a status bar QLabel widget.

    Parameters
    ----------
    text : str
    color : str

    Returns
    -------
    QLabel or None
    """
    if not _PYSIDE6_AVAILABLE:
        return None

    try:
        label = QLabel(text)
        label.setStyleSheet(
            f'background-color: {color}; color: white; '
            f'padding: 2px 8px; border-radius: 3px;'
        )
        return label

    except Exception as exc:
        logger.error("create_status_bar_widget error: %s", exc)
        return None


def format_pnl(value):
    """
    Format a PnL value as a colored string.

    Parameters
    ----------
    value : float
        PnL value in NTD.

    Returns
    -------
    str formatted with color hint (e.g. '+1,234' in red or '-567' in green)
    Note: Color tags are not actual HTML, just indicators for console use.
    """
    try:
        v = float(value or 0)
        if v > 0:
            return f'+{v:,.0f}'
        elif v < 0:
            return f'{v:,.0f}'
        else:
            return '0'
    except Exception:
        return str(value)
