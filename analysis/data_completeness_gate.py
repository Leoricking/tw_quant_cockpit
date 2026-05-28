"""
analysis/data_completeness_gate.py - Data completeness gate for formal analysis.

Distinguishes between mock/demo mode and formal analysis mode.

Rules
-----
- data_source == "mock"    → never sufficient for formal analysis; outputs are
                             demonstration estimates only.
- data_source == "real"    → check completeness >= FORMAL_MIN_PCT.
- data_source == "partial" → allow degraded output with clear warning.

Usage
-----
    gate = DataCompletenessGate("2330", data_source="mock", completeness=0.0)
    if not gate.is_formal_analysis_allowed():
        result["warning"] = gate.get_warning()
    result = gate.stamp(result)   # adds data_source + prices_are_estimates
"""

__all__ = [
    "DataCompletenessGate",
    "DATA_SOURCE_MOCK",
    "DATA_SOURCE_REAL",
    "DATA_SOURCE_PARTIAL",
    "FORMAL_MIN_PCT",
]

DATA_SOURCE_MOCK = "mock"
DATA_SOURCE_REAL = "real"
DATA_SOURCE_PARTIAL = "partial"

FORMAL_MIN_PCT = 60  # completeness % threshold to allow formal analysis

_MSG_MOCK = "[MOCK DATA] 模擬資料示範模式，非正式分析依據，勿作為實盤操作參考"
_MSG_INSUFFICIENT = "資料不足，只能做盤中初估，不能當正式短中長線操作依據"


class DataCompletenessGate:
    """
    Gate that checks whether available data is sufficient for formal analysis.

    Parameters
    ----------
    symbol : str
    data_source : str
        One of DATA_SOURCE_MOCK / DATA_SOURCE_REAL / DATA_SOURCE_PARTIAL.
    completeness : float
        0–100 percentage of required data fields available.
    """

    def __init__(self, symbol: str, data_source: str = DATA_SOURCE_MOCK,
                 completeness: float = 0.0):
        self.symbol = str(symbol)
        self.data_source = data_source
        self.completeness = float(completeness)

    def is_formal_analysis_allowed(self) -> bool:
        """Return True only when real data meets the completeness threshold."""
        if self.data_source == DATA_SOURCE_MOCK:
            return False
        return self.completeness >= FORMAL_MIN_PCT

    def get_warning(self) -> str:
        """Return the appropriate warning string (always non-empty for mock/partial)."""
        if self.data_source == DATA_SOURCE_MOCK:
            return _MSG_MOCK
        if not self.is_formal_analysis_allowed():
            return _MSG_INSUFFICIENT
        return ""

    def stamp(self, result: dict) -> dict:
        """
        Attach data_source and prices_are_estimates flags to a result dict.
        Does NOT mutate the original; returns a new dict.
        """
        out = dict(result)
        out["data_source"] = self.data_source
        out["prices_are_estimates"] = not self.is_formal_analysis_allowed()
        warning = self.get_warning()
        if warning:
            out["warning"] = warning
        return out

    @staticmethod
    def from_available_fields(symbol: str, available: set,
                              required_real: set) -> "DataCompletenessGate":
        """
        Factory: infer gate from available vs required field names.

        Parameters
        ----------
        available : set of str
            Field tags present in this analysis run.
        required_real : set of str
            Tags required for a formal (real-data) analysis.
        """
        real_fields = {f for f in available if not f.startswith("mock_")}
        if not real_fields:
            return DataCompletenessGate(symbol, DATA_SOURCE_MOCK, 0.0)

        completeness = len(real_fields & required_real) / max(len(required_real), 1) * 100
        if completeness >= FORMAL_MIN_PCT:
            source = DATA_SOURCE_REAL
        else:
            source = DATA_SOURCE_PARTIAL
        return DataCompletenessGate(symbol, source, completeness)
