"""
utils/console_format.py - Windows-safe CLI output formatting helpers.

Provides plain-text labels for mode, warnings, confidence levels, and
numeric formatting. Avoids emoji and Unicode symbols that may render
as garbled characters in Windows PowerShell / Command Prompt.

Usage:
    from utils.console_format import mode_label, warning_label, fmt_pct
    print(mode_label(mode='real', is_sample=False))   # 'REAL CSV'
    print(fmt_pct(0.0716))                             # '+7.16%'
"""

import pandas as pd


def mode_label(mode: str = '', source: str = '', is_sample: bool = False) -> str:
    """Return a Windows-safe data source label string.

    Returns one of:
        MOCK DATA
        REAL CSV SAMPLE
        REAL CSV
        MISSING
    """
    if mode == 'mock':
        return 'MOCK DATA'
    if is_sample:
        return 'REAL CSV SAMPLE'
    if source and source not in ('', 'unknown'):
        return 'REAL CSV'
    return 'MISSING'


def warning_label(text: str) -> str:
    """Prefix text with '[WARN]'."""
    return f'[WARN] {text}'


def ok_label(text: str) -> str:
    """Prefix text with '[OK]'."""
    return f'[OK] {text}'


def fail_label(text: str) -> str:
    """Prefix text with '[FAIL]'."""
    return f'[FAIL] {text}'


def confidence_label(level: str) -> str:
    """Return a normalised confidence level string.

    Accepts INSUFFICIENT / OBSERVATIONAL / RELIABLE (case-insensitive).
    Returns the canonical uppercase form.
    """
    lvl = (level or '').strip().upper()
    if lvl == 'RELIABLE':
        return 'RELIABLE'
    if lvl == 'OBSERVATIONAL':
        return 'OBSERVATIONAL'
    return 'INSUFFICIENT'


def fmt_pct(value, digits: int = 2) -> str:
    """Format *value* as a signed percentage string, e.g. '+7.16%'.

    Returns '\u2014' (em-dash) for None or NaN values.
    """
    if value is None:
        return '\u2014'
    try:
        f = float(value)
        if pd.isna(f):
            return '\u2014'
        return f'{f:+.{digits}f}%'
    except (TypeError, ValueError):
        return '\u2014'


def fmt_num(value, digits: int = 2) -> str:
    """Format *value* as a plain number string, e.g. '1.23'.

    Returns '\u2014' (em-dash) for None or NaN values.
    """
    if value is None:
        return '\u2014'
    try:
        f = float(value)
        if pd.isna(f):
            return '\u2014'
        return f'{f:.{digits}f}'
    except (TypeError, ValueError):
        return '\u2014'


def dash_if_none(value) -> str:
    """Return '\u2014' if *value* is None or NaN; otherwise return str(value)."""
    if value is None:
        return '\u2014'
    try:
        if pd.isna(value):
            return '\u2014'
    except (TypeError, ValueError):
        pass
    return str(value)
