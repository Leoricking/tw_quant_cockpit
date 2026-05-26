"""
utils/stable_hash.py - Process-stable integer hash utility.

Python's built-in hash() is randomised by PYTHONHASHSEED and varies between
interpreter processes, making it unsuitable for deterministic seeding.
Use stable_hash_int() everywhere a reproducible seed is needed.
"""

import hashlib

__all__ = ["stable_hash_int"]


def stable_hash_int(key: str, mod: int = 0) -> int:
    """
    Return a non-negative integer derived from *key* via MD5.

    The result is identical across all Python processes regardless of
    PYTHONHASHSEED.  Using this as a random seed gives deterministic,
    reproducible pseudo-random sequences per symbol.

    Parameters
    ----------
    key : str
        Any string identifier (symbol name, symbol + suffix, etc.).
    mod : int
        If > 0, return ``result % mod``; otherwise return the raw integer.

    Returns
    -------
    int
    """
    raw = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
    return raw % mod if mod > 0 else raw
