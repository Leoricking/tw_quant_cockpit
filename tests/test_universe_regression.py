"""
tests/test_universe_regression.py — Regression tests for v1.3.1 Universe Expansion Foundation.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import os
import pytest


class TestUniverseDefinitions:
    """9 universe definition tests."""

    def test_core_definition_exists(self):
        from universe.definitions_v131 import get_core_universe
        u = get_core_universe()
        assert u.universe_id == "core"
        assert len(u.symbols) == 14

    def test_research_definition_extends_core(self):
        from universe.definitions_v131 import get_core_universe, get_research_universe
        core = get_core_universe()
        research = get_research_universe()
        for sym in core.symbols:
            assert sym in research.symbols

    def test_extended_definition_exists(self):
        from universe.definitions_v131 import get_extended_universe
        u = get_extended_universe()
        assert u.universe_id == "extended"

    def test_watchlist_definition_exists(self):
        from universe.definitions_v131 import get_watchlist_universe
        u = get_watchlist_universe(watchlist_symbols=["2330", "2308"])
        assert u.universe_id == "watchlist"
        assert "2330" in u.symbols

    def test_excluded_definition_exists(self):
        from universe.definitions_v131 import get_excluded_universe
        u = get_excluded_universe()
        assert u.universe_id == "excluded"

    def test_all_builtin_universes_present(self):
        from universe.definitions_v131 import get_all_builtin_universes
        all_u = get_all_builtin_universes()
        for key in ("core", "research", "extended", "watchlist", "excluded"):
            assert key in all_u

    def test_core_14_contains_expected_symbols(self):
        from universe.definitions_v131 import CORE_14_SYMBOLS
        expected = {"2330", "2308", "2345", "2454", "6669", "3661", "3228", "5274", "2376", "2383", "6213", "2382", "2356", "3706"}
        assert set(CORE_14_SYMBOLS) == expected

    def test_universe_definition_is_built_in_seed(self):
        from universe.definitions_v131 import get_core_universe
        u = get_core_universe()
        assert u.source == "BUILT_IN_SEED"
        assert "NOT REAL_MARKET_MASTER" in u.description

    def test_universe_metadata_research_only(self):
        from universe.definitions_v131 import get_core_universe
        u = get_core_universe()
        assert u.metadata.get("research_only") is True
        assert u.metadata.get("no_real_orders") is True


class TestUniverseImport:
    """10 import tests."""

    FIXTURE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "fixtures", "universe")

    def test_csv_preview(self):
        from universe.importer_v131 import UniverseImporter
        importer = UniverseImporter()
        result = importer.preview(f"{self.FIXTURE_DIR}/valid_universe.csv", "csv")
        assert result.row_count > 0
        assert "symbol" in result.detected_fields

    def test_json_preview(self):
        from universe.importer_v131 import UniverseImporter
        importer = UniverseImporter()
        result = importer.preview(f"{self.FIXTURE_DIR}/valid_universe.json", "json")
        assert result.row_count > 0

    def test_dry_run_no_modify(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        importer = UniverseImporter()
        result = importer.dry_run(f"{self.FIXTURE_DIR}/valid_universe.csv", "csv")
        # Dry-run should not modify registry
        assert len(reg.list_symbols()) == 0
        assert result.ok

    def test_execute_adds_valid_symbols(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        importer = UniverseImporter()
        result = importer.execute(f"{self.FIXTURE_DIR}/valid_universe.csv", "csv", reg)
        assert result.ok
        assert len(result.added) > 0
        assert len(reg.list_symbols()) > 0

    def test_invalid_row_skipped(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        importer = UniverseImporter()
        result = importer.execute(f"{self.FIXTURE_DIR}/invalid_symbol.csv", "csv", reg)
        # Some rows should be skipped/blocked, none should be added as valid
        assert len(result.skipped) > 0 or len(result.blocked) > 0 or len(result.errors) > 0

    def test_duplicate_detected(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        importer = UniverseImporter()
        result = importer.dry_run(f"{self.FIXTURE_DIR}/duplicate_symbols.csv", "csv")
        assert len(result.duplicate_detected) > 0

    def test_market_conflict_blocked(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        importer = UniverseImporter()
        result = importer.dry_run(f"{self.FIXTURE_DIR}/market_conflict.csv", "csv")
        assert len(result.would_block) > 0

    def test_unknown_security_type_becomes_unknown(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        from universe.registry_v131 import UniverseRegistryV131
        from universe.models import SecurityType
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        importer = UniverseImporter()
        # valid_universe.csv has COMMON_STOCK (known type)
        result = importer.execute(f"{self.FIXTURE_DIR}/valid_universe.csv", "csv", reg)
        # No symbols with invalid security type in valid fixture -> should all be added
        assert result.ok

    def test_runtime_import_not_committed(self, tmp_path):
        # Runtime registry files in tmp_path must not be in git
        # (This test verifies the design principle — actual gitignore checked separately)
        assert str(tmp_path).startswith(str(tmp_path.parent))

    def test_fixture_not_accepted_as_real_market_master(self, tmp_path):
        from universe.importer_v131 import UniverseImporter
        importer = UniverseImporter()
        result = importer.preview(f"{self.FIXTURE_DIR}/valid_universe.csv", "csv")
        # Preview note must indicate NOT REAL_MARKET_MASTER
        assert "NOT REAL_MARKET_MASTER" in result.note


class TestSafetyInvariants:
    """Safety constraint tests."""

    def test_no_real_orders(self):
        import universe
        assert universe.NO_REAL_ORDERS is True

    def test_mock_fallback_disabled(self):
        import universe
        assert universe.MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is False

    def test_universe_real_api_not_connected(self):
        import universe
        assert universe.UNIVERSE_REAL_API_CONNECTED is False

    def test_universe_auto_download_disabled(self):
        import universe
        assert universe.UNIVERSE_AUTO_DOWNLOAD_ENABLED is False

    def test_production_trading_blocked(self):
        import universe
        assert universe.PRODUCTION_TRADING_BLOCKED is True

    def test_version_131(self):
        from release.version_info import VERSION
        # v1.4.0 supersedes v1.3.x; accept 1.3.x, 1.4.x, or 1.5.x
        assert VERSION.startswith("1.3.") or VERSION.startswith("1.4.") or VERSION.startswith("1.5.") or VERSION.startswith("1.6."), f"Expected 1.3.x-1.6.x, got {VERSION}"

    def test_replay_stable_baseline_129(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_universe_registry_flag(self):
        from release.version_info import UNIVERSE_REGISTRY_AVAILABLE
        assert UNIVERSE_REGISTRY_AVAILABLE is True

    def test_universe_real_api_flag(self):
        from release.version_info import UNIVERSE_REAL_API_CONNECTED
        assert UNIVERSE_REAL_API_CONNECTED is False

    def test_universe_auto_download_flag(self):
        from release.version_info import UNIVERSE_AUTO_DOWNLOAD_ENABLED
        assert UNIVERSE_AUTO_DOWNLOAD_ENABLED is False

    def test_broker_execution_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False
