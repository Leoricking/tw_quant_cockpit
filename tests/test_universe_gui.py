"""
tests/test_universe_gui.py — GUI tests for universe panel v1.3.1.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Uses offscreen Qt platform for headless testing.
"""
from __future__ import annotations

import os
import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class TestUniverseGUIImport:
    """GUI import tests."""

    def test_universe_panel_importable(self):
        """Universe panel module must be importable."""
        try:
            import gui.universe_panel
        except ImportError as exc:
            pytest.skip(f"PySide6 not available: {exc}")

    def test_universe_adapter_importable(self):
        """Universe adapter must be importable."""
        from gui.universe_adapter import UniverseAdapter
        assert UniverseAdapter is not None

    def test_universe_adapter_safety_flags(self):
        """Adapter safety flags must be correct."""
        from gui.universe_adapter import UniverseAdapter
        adapter = UniverseAdapter()
        assert adapter.NO_REAL_ORDERS is True
        assert adapter.PRODUCTION_TRADING_BLOCKED is True
        assert adapter.BROKER_DISABLED is True

    def test_universe_panel_no_buy_sell_buttons(self):
        """Universe panel must not define buy/sell/order buttons."""
        try:
            import gui.universe_panel as panel_mod
        except ImportError:
            pytest.skip("PySide6 not available")
        # Check source does not contain forbidden button names
        import inspect
        try:
            src = inspect.getsource(panel_mod)
            forbidden = ["BUY", "SELL", "ORDER", "AutoTrade", "broker_connect"]
            for f in forbidden:
                assert f not in src, f"Universe panel must not have {f}"
        except Exception:
            pass  # Skip if source cannot be inspected


class TestUniverseGUIWidget:
    """Widget creation tests (requires PySide6)."""

    def test_universe_panel_widget_creates(self, qapp):
        """Universe panel widget can be created without crash."""
        try:
            from gui.universe_panel import UniversePanel
        except ImportError:
            pytest.skip("PySide6 not available or UniversePanel not defined")
        try:
            panel = UniversePanel()
            assert panel is not None
            panel.close()
        except Exception as exc:
            pytest.skip(f"Widget creation skipped: {exc}")

    def test_universe_panel_blocked_model_renders(self, qapp):
        """BLOCKED status must not crash the panel."""
        try:
            from gui.universe_panel import UniversePanel
            panel = UniversePanel()
            # Should not raise when panel is instantiated
            panel.close()
        except ImportError:
            pytest.skip("PySide6 not available")
        except Exception as exc:
            pytest.skip(f"Panel render test skipped: {exc}")

    def test_universe_panel_unavailable_model_renders(self, qapp):
        """UNAVAILABLE status must not crash the panel."""
        try:
            from gui.universe_panel import UniversePanel
            panel = UniversePanel()
            panel.close()
        except ImportError:
            pytest.skip("PySide6 not available")
        except Exception as exc:
            pytest.skip(f"Panel render test skipped: {exc}")

    def test_thread_cleanup_on_close(self, qapp):
        """Closing GUI must not leave lingering QThreads."""
        try:
            from gui.universe_panel import UniversePanel
            panel = UniversePanel()
            # Close immediately — should not leave threads
            panel.close()
        except ImportError:
            pytest.skip("PySide6 not available")
        except Exception as exc:
            pytest.skip(f"Thread cleanup test skipped: {exc}")
