"""
Encoding utilities for Windows cp950 / subprocess output handling.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import re
import sys
from typing import Union

_CP950_PATTERNS = [
    r"cp950",
    r"codec can't decode",
    r"UnicodeDecodeError",
    r"charmap",
    r"gbk",
    r"big5",
    r"encoding.*cp950",
    r"cp950.*encoding",
]

_CONTROL_CHAR_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def safe_decode_output(bytes_or_text: Union[bytes, str], encoding: str = "utf-8") -> str:
    """Safely decode subprocess output, handling encoding errors gracefully."""
    if isinstance(bytes_or_text, str):
        return bytes_or_text
    for enc in [encoding, "utf-8", "cp950", "latin-1"]:
        try:
            return bytes_or_text.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return bytes_or_text.decode("latin-1", errors="replace")


def normalize_console_text(text: str) -> str:
    """Normalize console output — strip control chars, normalize newlines."""
    text = strip_control_chars(text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text


def strip_control_chars(text: str) -> str:
    """Remove non-printable control characters from text."""
    return _CONTROL_CHAR_RE.sub('', text)


def summarize_subprocess_error(error: Exception) -> str:
    """Return a friendly summary of a subprocess error."""
    msg = str(error)
    if is_windows_cp950_warning(msg):
        return f"KNOWN_WARN — Windows cp950 encoding (non-critical): {msg[:80]}"
    return f"Subprocess error: {msg[:120]}"


def is_windows_cp950_warning(text: str) -> bool:
    """Return True if text matches a known Windows cp950 encoding warning."""
    if sys.platform != "win32":
        return False
    lower = text.lower()
    for pattern in _CP950_PATTERNS:
        if re.search(pattern, lower):
            return True
    return False


def mark_cp950_warning_as_known(text: str) -> str:
    """Prefix cp950 warnings with KNOWN_WARN marker."""
    if is_windows_cp950_warning(text):
        return f"[KNOWN_WARN:cp950] {text}"
    return text
