"""
quality/mock_contamination_checker.py - Mock Contamination Checker (v0.3.20).

Scans CSV data, report strings, and backtest result mode fields for mock markers.
Distinguishes expected mock artifacts (paper trading, mock-realtime) from
real-mode mock contamination.

[!] Read Only. No Real Orders. Research Only.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Mock marker patterns to scan for
# ---------------------------------------------------------------------------

# Markers that indicate mock data contamination in real-mode output
_CONTAMINATION_MARKERS = [
    "mock",
    "MOCK",
    "fake",
    "FAKE",
    "dummy",
    "DUMMY",
    "simulated",
    "mode=mock",
    "mode='mock'",
    'mode="mock"',
    "\"mode\": \"mock\"",
    "'mode': 'mock'",
    "source=mock",
    "data_source=mock",
    "mock_data",
    "mock_price",
    "mock_volume",
]

# These are expected to appear — do NOT flag as contamination
_EXPECTED_MOCK_PATTERNS = [
    "mock-realtime",        # GUI simulation mode — expected
    "mock_realtime",
    "paper_state",          # paper trading state — expected
    "paper trading",
    "paper_trading",
    "PAPER_TRADING",
    "PaperTrading",
    "paper_trade",
    "no_real_orders",       # safety flag field name — expected
    "REAL_ORDER_READY",     # gate field name — expected
    "read_only",            # safety flag — expected
    "mock_contamination",   # this module's own output fields — expected
    "MockContamination",
    "contamination_score",
    "contamination_check",
    "contamination_result",
    "mock_contamination_score",
]

# Columns in CSVs that are allowed to contain mock-related values
_EXPECTED_MOCK_COLUMNS = {
    "source",           # allowed to say "mock" if it's labelled as such
    "mode",             # mode column in historical backtest results
    "data_mode",
}


class MockContaminationResult:
    """Result of a mock contamination check."""

    __slots__ = (
        "status",           # CLEAN / CONTAMINATED / PARTIAL / UNKNOWN
        "score",            # 0-100 (100 = no contamination)
        "contaminated_files",
        "contaminated_columns",
        "contamination_markers_found",
        "expected_artifacts",
        "details",
        "recommended_action",
    )

    def __init__(self):
        self.status: str = "UNKNOWN"
        self.score: float = 100.0
        self.contaminated_files: List[str] = []
        self.contaminated_columns: List[str] = []
        self.contamination_markers_found: List[str] = []
        self.expected_artifacts: List[str] = []
        self.details: List[str] = []
        self.recommended_action: str = ""

    def to_dict(self) -> dict:
        return {
            "status":                      self.status,
            "score":                       self.score,
            "contaminated_files":          self.contaminated_files,
            "contaminated_columns":        self.contaminated_columns,
            "contamination_markers_found": self.contamination_markers_found,
            "expected_artifacts":          self.expected_artifacts,
            "details":                     self.details,
            "recommended_action":          self.recommended_action,
        }


class MockContaminationChecker:
    """
    Scans data files and report content for mock data contamination.

    Parameters
    ----------
    import_root : root folder for data/import/ (default: {base_dir}/data/import)
    results_dir : backtest results folder (default: {base_dir}/data/backtest_results)
    reports_dir : reports folder (default: {base_dir}/reports)
    mode        : 'real' or 'mock'; in mock mode contamination is expected
    """

    VERSION = "v0.3.20"

    # Safety invariants
    read_only = True
    no_real_orders = True

    # CSV files to scan for mock markers in source/mode columns
    _IMPORT_CSV_FILES = {
        "daily_price":      "daily/daily_k.csv",
        "monthly_revenue":  "monthly_revenue/monthly_revenue.csv",
        "institutional":    "institutional/institutional.csv",
        "margin":           "margin/margin.csv",
        "fundamental":      "fundamental/fundamental.csv",
    }

    def __init__(
        self,
        import_root: Optional[str] = None,
        results_dir: Optional[str] = None,
        reports_dir: Optional[str] = None,
        mode: str = "real",
    ):
        self.import_root = import_root or os.path.join(_BASE_DIR, "data", "import")
        self.results_dir = results_dir or os.path.join(_BASE_DIR, "data", "backtest_results")
        self.reports_dir = reports_dir or os.path.join(_BASE_DIR, "reports")
        self.mode = mode

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> MockContaminationResult:
        """
        Run all contamination checks.

        Returns MockContaminationResult with:
          status  : CLEAN / CONTAMINATED / PARTIAL / UNKNOWN
          score   : 0-100 (100 = no contamination found)
        """
        result = MockContaminationResult()

        if self.mode == "mock":
            # In mock mode contamination is expected — always CLEAN
            result.status = "CLEAN"
            result.score  = 100.0
            result.details.append("Mode=mock: contamination check skipped (expected mock data)")
            return result

        issues: List[str] = []

        # 1. Check CSV source/mode columns
        csv_issues = self._check_csv_files()
        issues.extend(csv_issues)
        for issue in csv_issues:
            result.details.append(f"[CSV] {issue}")

        # 2. Check backtest result mode fields
        bt_issues = self._check_backtest_results()
        issues.extend(bt_issues)
        for issue in bt_issues:
            result.details.append(f"[Backtest] {issue}")

        # 3. Check report files for unexpected mock markers
        rpt_issues = self._check_report_files()
        issues.extend(rpt_issues)
        for issue in rpt_issues:
            result.details.append(f"[Report] {issue}")

        # Score: start at 100, penalise per issue (max -100)
        n_issues = len(issues)
        if n_issues == 0:
            result.status = "CLEAN"
            result.score  = 100.0
        elif n_issues <= 2:
            result.status = "PARTIAL"
            result.score  = max(70.0, 100.0 - n_issues * 15.0)
        else:
            result.status = "CONTAMINATED"
            result.score  = max(0.0, 100.0 - n_issues * 10.0)

        if result.status == "CLEAN":
            result.recommended_action = "No action needed."
        elif result.status == "PARTIAL":
            result.recommended_action = (
                "Inspect flagged files. Re-run data fetch with real provider to replace mock data."
            )
        else:
            result.recommended_action = (
                "BLOCKED: real-mode data contains mock markers. "
                "Re-import from real providers before running backtests."
            )

        return result

    # ------------------------------------------------------------------
    # CSV file checks
    # ------------------------------------------------------------------

    def _check_csv_files(self) -> List[str]:
        issues: List[str] = []
        try:
            import pandas as pd
        except ImportError:
            return ["pandas not available — CSV contamination check skipped"]

        for dataset, rel_path in self._IMPORT_CSV_FILES.items():
            full_path = os.path.join(self.import_root, rel_path)
            if not os.path.exists(full_path):
                continue
            try:
                df = pd.read_csv(full_path, nrows=500)
                issues.extend(self._scan_dataframe(dataset, df, full_path))
            except Exception as exc:
                logger.debug("Cannot read %s for contamination check: %s", full_path, exc)

        return issues

    def _scan_dataframe(self, dataset: str, df, full_path: str) -> List[str]:
        """Scan a DataFrame for mock contamination markers."""
        issues: List[str] = []
        str_cols = [c for c in df.columns if df[c].dtype == object]

        for col in str_cols:
            col_lower = col.lower()
            # Allow-listed columns may contain mode/source labels
            if col_lower in _EXPECTED_MOCK_COLUMNS:
                # Still check for real contamination: all values should NOT be 'mock'
                unique_vals = df[col].dropna().astype(str).str.lower().unique().tolist()
                contaminated = [
                    v for v in unique_vals
                    if any(m.lower() in v for m in _CONTAMINATION_MARKERS)
                    and not any(e.lower() in v for e in _EXPECTED_MOCK_PATTERNS)
                ]
                if contaminated:
                    issues.append(
                        f"{dataset}: column '{col}' contains mock markers {contaminated[:3]} "
                        f"in {os.path.basename(full_path)}"
                    )
                continue

            # For non-allow-listed columns, scan sample values
            sample = df[col].dropna().astype(str).head(100)
            for val in sample:
                val_lower = val.lower()
                for marker in _CONTAMINATION_MARKERS:
                    if marker.lower() in val_lower and not self._is_expected(val):
                        issues.append(
                            f"{dataset}: column '{col}' value '{val[:40]}' "
                            f"contains mock marker '{marker}'"
                        )
                        break  # one issue per column value is enough

        return issues

    # ------------------------------------------------------------------
    # Backtest results check
    # ------------------------------------------------------------------

    def _check_backtest_results(self) -> List[str]:
        issues: List[str] = []
        if not os.path.isdir(self.results_dir):
            return issues

        import glob as _glob
        csv_files = _glob.glob(os.path.join(self.results_dir, "*.csv"))

        try:
            import pandas as pd
        except ImportError:
            return ["pandas not available — backtest result contamination check skipped"]

        for fpath in csv_files[:20]:  # limit scan to 20 newest files
            try:
                df = pd.read_csv(fpath, nrows=100)
                # Check for mode='mock' in results
                if "mode" in df.columns:
                    modes = df["mode"].dropna().astype(str).str.lower().unique().tolist()
                    bad_modes = [m for m in modes if "mock" in m and "mock-realtime" not in m]
                    if bad_modes:
                        issues.append(
                            f"backtest_result {os.path.basename(fpath)}: "
                            f"mode column contains '{bad_modes[0]}' (expected 'real')"
                        )
                if "data_mode" in df.columns:
                    data_modes = df["data_mode"].dropna().astype(str).str.lower().unique().tolist()
                    bad = [m for m in data_modes if "mock" in m]
                    if bad:
                        issues.append(
                            f"backtest_result {os.path.basename(fpath)}: "
                            f"data_mode column contains '{bad[0]}'"
                        )
            except Exception as exc:
                logger.debug("Cannot scan backtest file %s: %s", fpath, exc)

        return issues

    # ------------------------------------------------------------------
    # Report file text scan
    # ------------------------------------------------------------------

    def _check_report_files(self) -> List[str]:
        issues: List[str] = []
        if not os.path.isdir(self.reports_dir):
            return issues

        import glob as _glob
        md_files = _glob.glob(os.path.join(self.reports_dir, "*.md"))

        for fpath in md_files[:10]:  # limit to 10 most recent
            try:
                with open(fpath, encoding="utf-8", errors="replace") as f:
                    content = f.read()
                for marker in _CONTAMINATION_MARKERS:
                    if marker in content and not self._content_is_expected(content, marker):
                        issues.append(
                            f"report {os.path.basename(fpath)}: "
                            f"contains mock marker '{marker}'"
                        )
                        break  # one issue per report file
            except Exception as exc:
                logger.debug("Cannot scan report %s: %s", fpath, exc)

        return issues

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_expected(value: str) -> bool:
        """Return True if the value matches an expected mock artifact pattern."""
        val_lower = value.lower()
        return any(e.lower() in val_lower for e in _EXPECTED_MOCK_PATTERNS)

    @staticmethod
    def _content_is_expected(content: str, marker: str) -> bool:
        """
        Return True if the marker appears only in expected contexts
        (e.g., in field names like 'mock_contamination_score', not in data values).
        """
        for expected in _EXPECTED_MOCK_PATTERNS:
            if expected.lower() in content.lower():
                # The marker may be part of an expected pattern
                idx = content.find(marker)
                if idx >= 0:
                    context_window = content[max(0, idx-30):idx+30+len(marker)]
                    if any(e.lower() in context_window.lower() for e in _EXPECTED_MOCK_PATTERNS):
                        return True
        return False
