"""
utils/user_facing_errors.py - User-facing error formatting (v0.3.22).

Wraps low-level exceptions into structured, actionable messages that are safe
to display in the CLI and GUI without exposing raw stack traces.

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

from typing import Any, List, Optional


# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------

SEV_INFO    = "INFO"
SEV_WARNING = "WARNING"
SEV_ERROR   = "ERROR"
SEV_FATAL   = "FATAL"


# ---------------------------------------------------------------------------
# UserFacingError
# ---------------------------------------------------------------------------

class UserFacingError:
    """
    A structured, user-readable error object.

    Fields
    ------
    title            : Short title (shown in bold / header)
    plain_message    : 1-2 sentence plain-English explanation
    technical_detail : Raw exception message or traceback excerpt (optional)
    likely_cause     : Most probable root cause
    can_ignore       : True if the system can continue without this data
    next_steps       : List of actionable fix suggestions
    severity         : INFO / WARNING / ERROR / FATAL
    source           : Originating module or step name
    """

    __slots__ = (
        "title",
        "plain_message",
        "technical_detail",
        "likely_cause",
        "can_ignore",
        "next_steps",
        "severity",
        "source",
    )

    def __init__(
        self,
        title: str,
        plain_message: str,
        technical_detail: str = "",
        likely_cause: str = "",
        can_ignore: bool = False,
        next_steps: Optional[List[str]] = None,
        severity: str = SEV_ERROR,
        source: str = "",
    ):
        self.title            = title
        self.plain_message    = plain_message
        self.technical_detail = technical_detail
        self.likely_cause     = likely_cause
        self.can_ignore       = can_ignore
        self.next_steps       = next_steps or []
        self.severity         = severity
        self.source           = source

    def to_dict(self) -> dict:
        return {
            "title":            self.title,
            "plain_message":    self.plain_message,
            "technical_detail": self.technical_detail,
            "likely_cause":     self.likely_cause,
            "can_ignore":       self.can_ignore,
            "next_steps":       self.next_steps,
            "severity":         self.severity,
            "source":           self.source,
        }

    def __str__(self) -> str:
        parts = [f"[{self.severity}] {self.title}", self.plain_message]
        if self.likely_cause:
            parts.append(f"Likely cause: {self.likely_cause}")
        if self.next_steps:
            parts.append("Next steps:")
            for step in self.next_steps:
                parts.append(f"  - {step}")
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# UserFacingErrorFormatter
# ---------------------------------------------------------------------------

class UserFacingErrorFormatter:
    """
    Converts raw Python exceptions and known error conditions into
    UserFacingError instances.

    Usage
    -----
        err = UserFacingErrorFormatter.from_exception(exc, source="data_freshness")
        print(err)
    """

    # Safety flags
    read_only          = True
    no_real_orders     = True
    production_blocked = True

    @classmethod
    def from_exception(
        cls,
        exc: Exception,
        source: str = "",
        can_ignore: bool = False,
    ) -> "UserFacingError":
        """Dispatch to the appropriate handler based on exception type."""
        exc_type = type(exc).__name__
        exc_str  = str(exc)

        # FileNotFoundError
        if isinstance(exc, FileNotFoundError):
            return cls._file_not_found(exc, source, can_ignore)

        # PermissionError
        if isinstance(exc, PermissionError):
            return cls._permission_error(exc, source, can_ignore)

        # UnicodeDecodeError
        if isinstance(exc, UnicodeDecodeError):
            return cls._unicode_error(exc, source, can_ignore)

        # pandas ParserError / EmptyDataError
        if exc_type in ("ParserError", "EmptyDataError"):
            return cls._pandas_parser_error(exc, source, can_ignore)

        # requests Timeout / ConnectionError
        if exc_type in ("Timeout", "ConnectTimeout", "ReadTimeout"):
            return cls._network_timeout(exc, source)
        if exc_type in ("ConnectionError", "NewConnectionError"):
            return cls._network_unavailable(exc, source)

        # Token / auth errors (common patterns in FinMind / TWSE)
        if any(kw in exc_str.lower() for kw in ("token", "unauthorized", "401", "403", "422")):
            return cls._token_not_configured(exc, source)

        # Data missing / empty DataFrame
        if any(kw in exc_str.lower() for kw in ("no data", "empty", "dataframe is empty")):
            return cls._data_missing(exc, source, can_ignore)

        # Stale data
        if "stale" in exc_str.lower():
            return cls._stale_data(exc, source, can_ignore)

        # Provider unsupported
        if any(kw in exc_str.lower() for kw in ("unsupported", "not supported", "not implemented")):
            return cls._provider_unsupported(exc, source)

        # Qt / GUI import error
        if any(kw in exc_str.lower() for kw in ("pyside6", "pyqt", "qt")):
            return cls._gui_import_error(exc, source)

        # ImportError
        if isinstance(exc, (ImportError, ModuleNotFoundError)):
            return cls._import_error(exc, source)

        # Generic fallback
        return cls._generic(exc, source, can_ignore)

    # ------------------------------------------------------------------
    # Specific handlers
    # ------------------------------------------------------------------

    @staticmethod
    def _file_not_found(exc, source, can_ignore) -> UserFacingError:
        path = str(exc).split(": ")[-1].strip("'\"")
        return UserFacingError(
            title="Data file not found",
            plain_message=f"A required data file could not be located: {path}",
            technical_detail=str(exc),
            likely_cause="The file has not been imported yet, or the path is incorrect.",
            can_ignore=can_ignore,
            next_steps=[
                "Run: python main.py import-csv --file <your_file>",
                "Or check the data/import/ directory for the expected file.",
                "If this is optional data, the system will continue with available data.",
            ],
            severity=SEV_WARNING if can_ignore else SEV_ERROR,
            source=source,
        )

    @staticmethod
    def _permission_error(exc, source, can_ignore) -> UserFacingError:
        return UserFacingError(
            title="File permission error",
            plain_message="The system cannot read or write a required file due to permissions.",
            technical_detail=str(exc),
            likely_cause="Another process may have the file open, or you lack write access.",
            can_ignore=can_ignore,
            next_steps=[
                "Close any Excel or spreadsheet programs that may have the file open.",
                "Check that you have write access to the data/ directory.",
                "Try running the command again.",
            ],
            severity=SEV_ERROR,
            source=source,
        )

    @staticmethod
    def _unicode_error(exc, source, can_ignore) -> UserFacingError:
        return UserFacingError(
            title="File encoding error",
            plain_message="A CSV file contains characters that cannot be decoded with the expected encoding.",
            technical_detail=str(exc),
            likely_cause="The file was saved with a different encoding (e.g., Big5 instead of UTF-8).",
            can_ignore=can_ignore,
            next_steps=[
                "Re-save the file as UTF-8 in Excel: Save As > CSV UTF-8.",
                "Or specify encoding with: python main.py import-csv --file <file> --encoding big5",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _pandas_parser_error(exc, source, can_ignore) -> UserFacingError:
        return UserFacingError(
            title="CSV parse error",
            plain_message="A CSV file could not be parsed — it may be malformed or have unexpected columns.",
            technical_detail=str(exc),
            likely_cause="The file format does not match the expected schema, or the header row is missing.",
            can_ignore=can_ignore,
            next_steps=[
                "Open the file and verify the column names in the first row.",
                "Run: python main.py clean-csv --file <file> to auto-fix common issues.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _network_timeout(exc, source) -> UserFacingError:
        return UserFacingError(
            title="Network request timed out",
            plain_message="An API request did not complete within the allowed time.",
            technical_detail=str(exc),
            likely_cause="Slow internet connection or the remote server is overloaded.",
            can_ignore=True,
            next_steps=[
                "Try again in a few minutes.",
                "Check your internet connection.",
                "The system will use cached CSV data if available.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _network_unavailable(exc, source) -> UserFacingError:
        return UserFacingError(
            title="Network unavailable",
            plain_message="The system cannot reach the data provider API.",
            technical_detail=str(exc),
            likely_cause="No internet connection, or the API server is down.",
            can_ignore=True,
            next_steps=[
                "Check your internet connection.",
                "The system will use cached CSV data if available.",
                "Try again later.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _token_not_configured(exc, source) -> UserFacingError:
        return UserFacingError(
            title="API token not configured",
            plain_message="An API token is required but has not been set in the environment.",
            technical_detail=str(exc),
            likely_cause="FINMIND_TOKEN or a similar environment variable is missing from .env",
            can_ignore=True,
            next_steps=[
                "Copy .env.example to .env and fill in your API token.",
                "Run: python main.py provider-health --create-env-example to generate a template.",
                "The system will continue using CSV data only.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _data_missing(exc, source, can_ignore) -> UserFacingError:
        return UserFacingError(
            title="No data available",
            plain_message="The requested dataset is empty or has not been imported yet.",
            technical_detail=str(exc),
            likely_cause="Data has not been imported for this stock or date range.",
            can_ignore=can_ignore,
            next_steps=[
                "Run: python main.py import-csv to import data from CSV files.",
                "Or run: python main.py provider-auto-fetch to fetch from APIs.",
                "Check: python main.py data-freshness for current data status.",
            ],
            severity=SEV_WARNING if can_ignore else SEV_ERROR,
            source=source,
        )

    @staticmethod
    def _stale_data(exc, source, can_ignore) -> UserFacingError:
        return UserFacingError(
            title="Data is stale",
            plain_message="The data available is older than the acceptable threshold.",
            technical_detail=str(exc),
            likely_cause="Data has not been updated recently.",
            can_ignore=can_ignore,
            next_steps=[
                "Run: python main.py update-data to refresh all data sources.",
                "Or: python main.py provider-auto-fetch --replace to force re-fetch.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _provider_unsupported(exc, source) -> UserFacingError:
        return UserFacingError(
            title="Provider not supported",
            plain_message="The requested data provider is not available in this configuration.",
            technical_detail=str(exc),
            likely_cause="The provider may require a paid subscription or additional setup.",
            can_ignore=True,
            next_steps=[
                "Check: python main.py provider-health for available providers.",
                "Use CSV data as a fallback.",
            ],
            severity=SEV_INFO,
            source=source,
        )

    @staticmethod
    def _gui_import_error(exc, source) -> UserFacingError:
        return UserFacingError(
            title="GUI library not available",
            plain_message="PySide6 (the GUI framework) is not installed or cannot be imported.",
            technical_detail=str(exc),
            likely_cause="PySide6 was not installed, or the virtual environment is incomplete.",
            can_ignore=True,
            next_steps=[
                "Install PySide6: pip install PySide6",
                "The CLI commands will continue to work without the GUI.",
            ],
            severity=SEV_WARNING,
            source=source,
        )

    @staticmethod
    def _import_error(exc, source) -> UserFacingError:
        module = str(exc).replace("No module named ", "").strip("'")
        return UserFacingError(
            title=f"Module not found: {module}",
            plain_message=f"A required Python module could not be imported: {module}",
            technical_detail=str(exc),
            likely_cause="The package is not installed or the virtual environment is incomplete.",
            can_ignore=False,
            next_steps=[
                "Run: pip install -r requirements.txt",
                f"Or install individually: pip install {module.split('.')[0]}",
            ],
            severity=SEV_ERROR,
            source=source,
        )

    @staticmethod
    def _generic(exc, source, can_ignore) -> UserFacingError:
        exc_type = type(exc).__name__
        return UserFacingError(
            title=f"Unexpected error ({exc_type})",
            plain_message="An unexpected error occurred. Check the log for details.",
            technical_detail=str(exc),
            likely_cause="An unhandled exception in the processing pipeline.",
            can_ignore=can_ignore,
            next_steps=[
                "Check the log output above for more details.",
                "If the problem persists, report it with the full error message.",
            ],
            severity=SEV_ERROR,
            source=source,
        )

    @classmethod
    def command_failed(
        cls,
        command: str,
        reason: str,
        source: str = "",
        can_ignore: bool = False,
    ) -> "UserFacingError":
        """Create an error for a failed CLI command."""
        return UserFacingError(
            title=f"Command failed: {command}",
            plain_message=reason,
            likely_cause="The command encountered an error during execution.",
            can_ignore=can_ignore,
            next_steps=[
                "Run with --log-level DEBUG for more details.",
                "Check that all required data files are present.",
            ],
            severity=SEV_ERROR,
            source=source,
        )

    @classmethod
    def qt_table_model_error(
        cls,
        context: str,
        exc: Exception,
    ) -> "UserFacingError":
        """Create an error for Qt table model issues."""
        return UserFacingError(
            title="GUI table display error",
            plain_message=f"The data table could not be displayed: {context}",
            technical_detail=str(exc),
            likely_cause="The data has an unexpected shape or missing columns.",
            can_ignore=True,
            next_steps=[
                "Try refreshing the data.",
                "If the error persists, the table will show an empty state instead.",
            ],
            severity=SEV_WARNING,
            source=context,
        )
