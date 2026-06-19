"""
tests/conftest.py -- Shared test fixtures.

Provides a session-scoped QApplication for GUI tests when PySide6 is installed.
Uses the offscreen platform plugin so tests run headless without a display server.
Does NOT change production GUI startup behavior.
"""
from __future__ import annotations

import os
import pytest

# ---------------------------------------------------------------------------
# Qt offscreen platform for test isolation (does not affect production)
# ---------------------------------------------------------------------------
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="session")
def qapp():
    """
    Session-scoped QApplication instance.

    PySide6 requires exactly one QApplication per process.  Creating it in a
    session-scoped fixture ensures:
      - It exists before any QWidget is constructed.
      - It is shared across all tests (no double-creation crash).
      - It is torn down after the entire session completes.
    """
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        pytest.skip("PySide6 not installed")
        return

    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # Do NOT call app.quit() — let the process handle teardown naturally
