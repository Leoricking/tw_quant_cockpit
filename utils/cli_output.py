"""
utils/cli_output.py - Windows cp950-safe CLI output helpers (v0.3.22).

Provides a consistent, structured CLI output formatter.
No emoji. Plain ASCII / CJK only. Safe for Windows cp950 terminal.

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import sys
from typing import Any, List, Optional, Sequence


# ---------------------------------------------------------------------------
# CLIOutput
# ---------------------------------------------------------------------------

class CLIOutput:
    """
    Structured CLI output formatter.

    Produces consistent, structured text suitable for:
    - Windows cp950 / UTF-8 terminals (no emoji, no box-drawing chars)
    - Redirection to files
    - Piping to other tools

    Usage
    -----
        out = CLIOutput()
        out.header("Data Quality Gate", version="v0.3.20")
        out.safety_banner()
        out.section("Scores")
        out.key_value("Production Readiness", "82.5 (READY_FOR_RESEARCH)")
        out.status_line("data_freshness", "OK")
        out.footer()
        out.flush()
    """

    # Safety flags
    read_only          = True
    no_real_orders     = True
    production_blocked = True

    # Column widths
    _KEY_WIDTH    = 32
    _STATUS_WIDTH = 12

    def __init__(self, stream=None):
        self._stream = stream or sys.stdout
        self._lines: List[str] = []

    # ------------------------------------------------------------------
    # Core write
    # ------------------------------------------------------------------

    def _write(self, line: str) -> None:
        self._lines.append(line)

    def flush(self) -> None:
        """Write all buffered lines to the stream."""
        for line in self._lines:
            try:
                print(line, file=self._stream)
            except UnicodeEncodeError:
                # Fallback: replace unencodable chars
                safe = line.encode("ascii", errors="replace").decode("ascii")
                print(safe, file=self._stream)
        self._lines = []

    # ------------------------------------------------------------------
    # Structural elements
    # ------------------------------------------------------------------

    def header(self, title: str, version: str = "", width: int = 64) -> None:
        """Print a top-level section header."""
        self._write("")
        self._write("=" * width)
        ver_suffix = f"  ({version})" if version else ""
        self._write(f"  {title}{ver_suffix}")
        self._write("  Research Only | Read Only | No Real Orders")
        self._write("  Production Trading: BLOCKED")
        self._write("=" * width)
        self._write("")

    def section(self, title: str, width: int = 64) -> None:
        """Print a sub-section separator."""
        self._write(f"  --- {title} " + "-" * max(0, width - len(title) - 7))

    def key_value(self, key: str, value: Any, indent: int = 2) -> None:
        """Print a key: value pair."""
        prefix = " " * indent
        k = str(key).ljust(self._KEY_WIDTH)
        self._write(f"{prefix}{k}: {value}")

    def status_line(
        self,
        name: str,
        status: str,
        detail: str = "",
        indent: int = 2,
    ) -> None:
        """Print a step/item status line: [STATUS] name  detail"""
        prefix = " " * indent
        status_str = f"[{status}]".ljust(self._STATUS_WIDTH)
        line = f"{prefix}{status_str} {name}"
        if detail:
            line += f"  {detail}"
        self._write(line)

    def warning(self, message: str, indent: int = 2) -> None:
        """Print a [WARN] message."""
        prefix = " " * indent
        self._write(f"{prefix}[WARN] {message}")

    def error(self, message: str, indent: int = 2) -> None:
        """Print an [ERROR] message."""
        prefix = " " * indent
        self._write(f"{prefix}[ERROR] {message}")

    def info(self, message: str, indent: int = 2) -> None:
        """Print a plain informational line."""
        prefix = " " * indent
        self._write(f"{prefix}{message}")

    def blank(self) -> None:
        """Print a blank line."""
        self._write("")

    def table(
        self,
        headers: Sequence[str],
        rows: Sequence[Sequence[Any]],
        col_widths: Optional[Sequence[int]] = None,
        indent: int = 2,
    ) -> None:
        """Print a plain-text table.

        Parameters
        ----------
        headers   : Column header strings
        rows      : Row data (each row is a sequence of cell values)
        col_widths: Optional fixed widths; auto-calculated if None
        indent    : Left indent (spaces)
        """
        if not headers:
            return

        prefix = " " * indent
        n_cols = len(headers)

        # Calculate column widths
        if col_widths:
            widths = list(col_widths)[:n_cols]
            while len(widths) < n_cols:
                widths.append(10)
        else:
            widths = [len(str(h)) for h in headers]
            for row in rows:
                for i, cell in enumerate(row[:n_cols]):
                    widths[i] = max(widths[i], len(str(cell)))

        # Header row
        header_cells = [str(headers[i]).ljust(widths[i]) for i in range(n_cols)]
        self._write(f"{prefix}  {'  '.join(header_cells)}")

        # Separator
        sep = "  ".join("-" * w for w in widths)
        self._write(f"{prefix}  {sep}")

        # Data rows
        for row in rows:
            cells = []
            for i in range(n_cols):
                val = row[i] if i < len(row) else ""
                cells.append(str(val).ljust(widths[i]))
            self._write(f"{prefix}  {'  '.join(cells)}")

    def safety_banner(self) -> None:
        """Print the mandatory safety disclaimer banner."""
        self._write("")
        self._write("  " + "=" * 60)
        self._write("  SAFETY NOTICE")
        self._write("  " + "-" * 60)
        self._write("  Read Only              : YES")
        self._write("  No Real Orders         : YES")
        self._write("  Production Trading     : BLOCKED")
        self._write("  Real Order Ready       : NO (never in this system)")
        self._write("  Purpose                : Research, simulation, and")
        self._write("                           decision support only.")
        self._write("                           Not investment advice.")
        self._write("  " + "=" * 60)
        self._write("")

    def footer(self, extra: str = "") -> None:
        """Print a closing footer."""
        self._write("")
        self._write("  [!] Read Only. No Real Orders. Production Trading: BLOCKED.")
        if extra:
            self._write(f"  {extra}")
        self._write("")

    def user_facing_error(self, err: Any) -> None:
        """Print a UserFacingError in structured format.

        Accepts either a UserFacingError instance or a plain string.
        """
        if hasattr(err, "title"):
            self.blank()
            self._write(f"  [{err.severity}] {err.title}")
            self._write(f"  {err.plain_message}")
            if err.likely_cause:
                self._write(f"  Likely cause: {err.likely_cause}")
            if err.next_steps:
                self._write("  Next steps:")
                for step in err.next_steps:
                    self._write(f"    - {step}")
            if err.can_ignore:
                self._write("  (This issue can be ignored — system will continue.)")
            self.blank()
        else:
            self.error(str(err))

    # ------------------------------------------------------------------
    # Convenience: print immediately (no buffering)
    # ------------------------------------------------------------------

    def print_now(self, message: str) -> None:
        """Print *message* immediately to the stream, bypassing the buffer."""
        try:
            print(message, file=self._stream)
        except UnicodeEncodeError:
            safe = message.encode("ascii", errors="replace").decode("ascii")
            print(safe, file=self._stream)
