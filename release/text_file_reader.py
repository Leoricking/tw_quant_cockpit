"""
release/text_file_reader.py — Shared text file reader with encoding fallback.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import List, Optional, Tuple


def read_text_with_encoding_fallback(
    path: str,
    encodings: Optional[List[str]] = None,
) -> Tuple[str, str, bool, List[str]]:
    """
    Try encodings in order; return (text, encoding_used, fallback_used, warnings).

    Parameters
    ----------
    path : str
        File path to read.
    encodings : list[str], optional
        Ordered list of encodings to try. Defaults to
        ["utf-8-sig", "utf-8", "cp950", "latin-1"].

    Returns
    -------
    text : str
    encoding_used : str
    fallback_used : bool   True if a non-first encoding was needed
    warnings : list[str]

    Raises
    ------
    ValueError
        If no encoding succeeds.
    """
    if encodings is None:
        encodings = ["utf-8-sig", "utf-8", "cp950", "latin-1"]

    warnings: List[str] = []
    for i, enc in enumerate(encodings):
        try:
            with open(path, "r", encoding=enc) as f:
                text = f.read()
            fallback_used = i > 0
            if fallback_used:
                warnings.append(f"Used fallback encoding: {enc}")
            return text, enc, fallback_used, warnings
        except (UnicodeDecodeError, LookupError) as e:
            warnings.append(f"Encoding {enc} failed: {e}")

    raise ValueError(
        f"Could not decode {path} with any of {encodings}: {warnings}"
    )
