"""
gui/data_quality_gate_adapter.py - Data Quality Gate GUI adapter (v0.3.20).

Bridges DataQualityGate backend to PySide6 GUI panel.
All operations are read-only. No real orders.

[!] Read Only. No Real Orders. Research Only.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataQualityGateAdapter:
    """
    Adapter that runs DataQualityGate and generates reports for the GUI.

    Parameters
    ----------
    mode       : 'real' or 'mock'
    report_dir : output folder for generated reports
    """

    # Safety invariants
    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        mode: str = "real",
        report_dir: Optional[str] = None,
    ):
        self.mode       = mode
        self.report_dir = report_dir or os.path.join(_BASE_DIR, "reports")

    def run_gate(self) -> dict:
        """
        Run DataQualityGate and return the full result dict.
        """
        from quality.data_quality_gate import DataQualityGate
        gate = DataQualityGate(mode=self.mode)
        return gate.run()

    def generate_report(self, gate_result: dict) -> str:
        """
        Build Markdown report from gate_result.
        Returns path to the generated file.
        """
        from reports.data_quality_gate_report import DataQualityGateReportBuilder
        builder = DataQualityGateReportBuilder(gate_result)
        return builder.build(output_dir=self.report_dir)

    def render_report(self, gate_result: dict) -> str:
        """Return rendered Markdown string without writing a file."""
        from reports.data_quality_gate_report import DataQualityGateReportBuilder
        builder = DataQualityGateReportBuilder(gate_result)
        return builder.render()
