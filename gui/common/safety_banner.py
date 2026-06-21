"""
gui/common/safety_banner.py — Safety banner widget factory.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Returns a QGroupBox safety banner for GUI panels.
Must only be imported when PySide6 is available.
"""
from __future__ import annotations

from typing import Dict


def make_safety_banner(title: str, flags: Dict[str, bool]):
    """
    Return a QGroupBox safety banner widget.

    Parameters
    ----------
    title : str
        Panel title shown in the banner header.
    flags : dict
        Safety flags to display (key → bool).

    Returns
    -------
    QGroupBox with safety information.
    """
    from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QLabel
    from PySide6.QtCore import Qt

    box = QGroupBox("Research Safety")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(6, 4, 6, 4)

    header = QLabel(f"[!] {title}  |  Research Only  |  No Real Orders  |  Production Trading BLOCKED")
    header.setStyleSheet("color: #cc0000; font-weight: bold; font-size: 11px;")
    header.setWordWrap(True)
    layout.addWidget(header)

    for flag_name, flag_value in flags.items():
        label_text = flag_name.replace("_", " ").title()
        status = "✓" if flag_value else "✗"
        lbl = QLabel(f"  {status}  {label_text}")
        lbl.setStyleSheet("font-size: 10px; color: #333333;")
        layout.addWidget(lbl)

    return box
