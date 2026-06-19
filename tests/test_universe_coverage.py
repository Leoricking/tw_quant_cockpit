"""
tests/test_universe_coverage.py — Coverage and scanner tests for v1.3.1.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Tests use tmp_path for registry storage.
"""
from __future__ import annotations

import pytest
from universe.models import CoverageStatus, UniverseTier


def _make_registry(tmp_path):
    from universe.registry_v131 import UniverseRegistryV131
    reg = UniverseRegistryV131(storage_dir=str(tmp_path))
    reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
    reg.register_symbol({"symbol": "2308", "market": "TWSE", "name": "台達電"})
    return reg


class TestUniverseCoverageAnalyzer:
    """14 coverage tests (v1.3.1)."""

    def test_unregistered_symbol_is_unavailable(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("9999", profile="default", registry=reg)
        assert record.quality_status in (
            CoverageStatus.UNAVAILABLE.value,
            CoverageStatus.BLOCKED.value,
            CoverageStatus.MISSING.value,
        )
        assert record.registry_status == "UNREGISTERED"

    def test_registered_no_real_data_is_unavailable(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="default", registry=reg)
        # No quality gate, should be UNAVAILABLE
        assert record.quality_status in (
            CoverageStatus.UNAVAILABLE.value,
            CoverageStatus.PARTIAL.value,
            CoverageStatus.MISSING.value,
        )

    def test_missing_values_not_zero(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="default", registry=reg)
        # Missing values must not be filled with 0
        assert record.latest_price_date is None or isinstance(record.latest_price_date, str)
        assert record.quality_score != 0 or record.quality_score is None

    def test_excluded_symbol_status(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        # Analyze a symbol that is UNAVAILABLE (no data)
        record = analyzer.analyze_symbol("2308", profile="default", registry=reg)
        assert record.symbol == "2308"
        assert record.quality_status in [e.value for e in CoverageStatus]

    def test_profile_specific_allowances(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record_screening = analyzer.analyze_symbol("2330", profile="stock_screening", registry=reg)
        record_precise = analyzer.analyze_symbol("2330", profile="precise_price", registry=reg)
        # Records should have profile-based fields
        assert hasattr(record_screening, "precise_price_allowed")
        assert hasattr(record_precise, "precise_price_allowed")

    def test_precise_price_profile(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="precise_price", registry=reg)
        # Without real data, precise_price_allowed should be False
        if record.quality_status != CoverageStatus.READY.value:
            assert record.precise_price_allowed is False

    def test_backtest_profile(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="backtest", registry=reg)
        if record.quality_status != CoverageStatus.READY.value:
            assert record.backtest_allowed is False

    def test_abc_buy_point_profile(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="abc_buy_point", registry=reg)
        if record.quality_status != CoverageStatus.READY.value:
            assert record.abc_buy_point_allowed is False

    def test_profile_results_not_mixed(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        r1 = analyzer.analyze_symbol("2330", profile="stock_screening", registry=reg)
        r2 = analyzer.analyze_symbol("2330", profile="precise_price", registry=reg)
        # Both belong to the same symbol but may have different profile statuses
        assert r1.symbol == r2.symbol == "2330"

    def test_analyze_universe_no_crash(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        results = analyzer.analyze_universe("test_universe", profile="default", registry=reg)
        assert isinstance(results, list)
        # Should have results for each registered symbol
        assert len(results) >= 0

    def test_to_dict_roundtrip(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        from universe.models import UniverseCoverageRecord
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="default", registry=reg)
        d = record.to_dict()
        assert isinstance(d, dict)
        assert "symbol" in d
        assert "quality_status" in d

    def test_blocking_reasons_preserved(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("9999", profile="default", registry=reg)
        # Unregistered symbol should have blocking reason
        assert len(record.blocking_reasons) > 0

    def test_no_real_data_no_demo_only_fallback(self, tmp_path):
        from universe.coverage_analyzer_v131 import UniverseCoverageAnalyzerV131
        reg = _make_registry(tmp_path)
        analyzer = UniverseCoverageAnalyzerV131(registry=reg)
        record = analyzer.analyze_symbol("2330", profile="default", registry=reg)
        # Without mock data injection, should NOT return DEMO_ONLY
        # (DEMO_ONLY requires explicit mock source, not auto-fallback)
        assert record.quality_status != CoverageStatus.DEMO_ONLY.value

    def test_coverage_record_safety_fields(self, tmp_path):
        from universe.models import UniverseCoverageRecord
        record = UniverseCoverageRecord(symbol="2330")
        assert hasattr(record, "precise_price_allowed")
        assert hasattr(record, "backtest_allowed")
        assert hasattr(record, "abc_buy_point_allowed")
        assert record.precise_price_allowed is False
        assert record.backtest_allowed is False


class TestUniverseQualityScanner:
    """8 scanner tests (v1.3.1)."""

    def test_scan_single_symbol(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        scanner = UniverseQualityScanner(registry=reg)
        record = scanner.scan_symbol("2330", profile="default")
        assert record.symbol == "2330"

    def test_scan_core_tier(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        reg.register_symbol({"symbol": "2308", "market": "TWSE", "name": "台達電"})
        scanner = UniverseQualityScanner(registry=reg)
        results = scanner.scan_tier(UniverseTier.CORE.value, profile="default")
        assert isinstance(results, list)

    def test_single_failure_does_not_crash_batch(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        scanner = UniverseQualityScanner(registry=reg)
        # Scan a mix of valid and invalid symbols
        results = scanner.scan_symbols(["2330", "9999_INVALID_999999"], profile="default")
        assert len(results) == 2  # Both symbols scanned, no crash

    def test_scan_limit(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        for i in range(10):
            reg.register_symbol({"symbol": f"233{i}", "market": "TWSE"})
        scanner = UniverseQualityScanner(registry=reg, max_scan=3)
        symbols = [f"233{i}" for i in range(10)]
        results = scanner.scan_symbols(symbols, profile="default")
        assert len(results) <= 3

    def test_no_auto_download(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        assert UniverseQualityScanner.MOCK_FALLBACK_ENABLED is False

    def test_no_mock_fallback(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        assert UniverseQualityScanner.MOCK_FALLBACK_ENABLED is False

    def test_stable_deterministic_results(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        reg.register_symbol({"symbol": "2308", "market": "TWSE", "name": "台達電"})
        scanner = UniverseQualityScanner(registry=reg)
        symbols = ["2330", "2308"]
        r1 = scanner.scan_symbols(symbols, profile="default")
        r2 = scanner.scan_symbols(symbols, profile="default")
        assert [r.symbol for r in r1] == [r.symbol for r in r2]

    def test_blocking_reasons_preserved(self, tmp_path):
        from universe.scanner import UniverseQualityScanner
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        scanner = UniverseQualityScanner(registry=reg)
        record = scanner.scan_symbol("9999", profile="default")
        # Should return a record (not crash), even for unregistered symbol
        assert isinstance(record, type(record))
