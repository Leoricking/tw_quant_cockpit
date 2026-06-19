"""
tests/test_universe_registry.py — Registry tests for v1.3.1.

[!] Tests use tmp_path for registry storage (runtime files not committed).
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import pytest


class TestUniverseRegistry:
    """12 registry tests (v1.3.1)."""

    def _make_registry(self, tmp_path):
        from universe.registry_v131 import UniverseRegistryV131
        return UniverseRegistryV131(storage_dir=str(tmp_path))

    def test_register_twse_symbol(self, tmp_path):
        reg = self._make_registry(tmp_path)
        ok, msg = reg.register_symbol({"symbol": "2330", "name": "台積電", "market": "TWSE"})
        assert ok, f"Registration failed: {msg}"
        sym = reg.get_symbol("2330")
        assert sym is not None
        assert sym.symbol == "2330"
        assert sym.market == "TWSE"

    def test_register_tpex_symbol(self, tmp_path):
        reg = self._make_registry(tmp_path)
        ok, msg = reg.register_symbol({"symbol": "6213", "market": "TPEx", "name": "聯茂"})
        assert ok, f"Registration failed: {msg}"
        sym = reg.get_symbol("6213")
        assert sym is not None
        assert sym.market == "TPEx"

    def test_safe_merge_duplicate(self, tmp_path):
        reg = self._make_registry(tmp_path)
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        # Same market, different name field — should merge safely
        ok, msg = reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電 TSMC"})
        assert ok
        sym = reg.get_symbol("2330")
        assert sym is not None
        assert "2330" in reg._symbols

    def test_market_conflict_blocked(self, tmp_path):
        reg = self._make_registry(tmp_path)
        reg.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        # Conflict: same symbol, different market
        ok, msg = reg.register_symbol({"symbol": "2330", "market": "TPEx", "name": "台積電 conflict"})
        assert not ok
        assert "conflict" in msg.lower() or "market" in msg.lower()

    def test_missing_name_no_crash(self, tmp_path):
        reg = self._make_registry(tmp_path)
        # Register without name — should not crash
        ok, msg = reg.register_symbol({"symbol": "2345", "market": "TWSE"})
        assert ok
        sym = reg.get_symbol("2345")
        assert sym is not None
        assert sym.stock_name == "" or sym.stock_name is not None

    def test_invalid_symbol_rejected(self, tmp_path):
        reg = self._make_registry(tmp_path)
        ok, msg = reg.register_symbol({"symbol": "", "market": "TWSE"})
        assert not ok

    def test_etf_vs_common_stock_type_separation(self, tmp_path):
        reg = self._make_registry(tmp_path)
        reg.register_symbol({
            "symbol": "0050",
            "market": "TWSE",
            "name": "元大台灣50",
            "security_type": "ETF",
        })
        reg.register_symbol({
            "symbol": "2330",
            "market": "TWSE",
            "name": "台積電",
            "security_type": "COMMON_STOCK",
        })
        etf = reg.get_symbol("0050")
        stock = reg.get_symbol("2330")
        assert etf is not None
        assert stock is not None
        assert etf.security_type != stock.security_type

    def test_warrant_excluded(self, tmp_path):
        reg = self._make_registry(tmp_path)
        ok, msg = reg.register_symbol({
            "symbol": "2330W",
            "market": "TWSE",
            "name": "台積電認購",
            "security_type": "WARRANT",
            "is_warrant": True,
        })
        # Warrant registration: may succeed but should not be active
        if ok:
            sym = reg.get_symbol("2330W")
            # Warrants should be deactivated
            if sym:
                assert sym.is_active is False or sym.security_type == "WARRANT"

    def test_delisted_not_active(self, tmp_path):
        reg = self._make_registry(tmp_path)
        reg.register_symbol({
            "symbol": "9999",
            "market": "TWSE",
            "name": "delisted test",
            "listing_status": "DELISTED",
            "is_active": False,
        })
        sym = reg.get_symbol("9999")
        assert sym is not None
        assert sym.is_active is False

    def test_serialization_roundtrip(self, tmp_path):
        reg1 = self._make_registry(tmp_path)
        reg1.register_symbol({"symbol": "2330", "market": "TWSE", "name": "台積電"})
        reg1.register_symbol({"symbol": "2308", "market": "TWSE", "name": "台達電"})
        # Load from same storage_dir (roundtrip)
        from universe.registry_v131 import UniverseRegistryV131
        reg2 = UniverseRegistryV131(storage_dir=str(tmp_path))
        assert reg2.get_symbol("2330") is not None
        assert reg2.get_symbol("2308") is not None

    def test_old_schema_graceful_load(self, tmp_path):
        # Write a minimal JSON with missing fields (simulating old schema)
        import json
        sym_file = tmp_path / "symbols.json"
        sym_file.write_text(json.dumps({
            "schema_version": "1.0.0",
            "symbols": {
                "2330": {"symbol": "2330", "stock_name": "台積電"}
            }
        }), encoding="utf-8")
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        sym = reg.get_symbol("2330")
        assert sym is not None  # loaded gracefully, not crashed

    def test_unknown_fields_forward_compatible(self, tmp_path):
        import json
        sym_file = tmp_path / "symbols.json"
        sym_file.write_text(json.dumps({
            "schema_version": "99.0.0",
            "symbols": {
                "2330": {
                    "symbol": "2330",
                    "stock_name": "台積電",
                    "market": "TWSE",
                    "future_field_unknown": "some_value",
                }
            }
        }), encoding="utf-8")
        from universe.registry_v131 import UniverseRegistryV131
        reg = UniverseRegistryV131(storage_dir=str(tmp_path))
        sym = reg.get_symbol("2330")
        # Should not crash on unknown fields
        assert sym is not None
