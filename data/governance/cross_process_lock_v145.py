"""
data/governance/cross_process_lock_v145.py — Cross-Process Lock v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] File-based locking. Crash-safe. Stale lock recovery.
[!] Lock timeout prevents permanent deadlock.
"""
from __future__ import annotations

import json
import os
import tempfile
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_LOCK_DIR = tempfile.gettempdir()
_DEFAULT_TIMEOUT = 30
_DEFAULT_MAX_AGE = 300


def _lock_path(lock_name: str) -> str:
    safe = lock_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    return os.path.join(_LOCK_DIR, f"tw_quant_{safe}.lock")


def _now_ts() -> float:
    return time.time()


def _pid_exists(pid: int) -> bool:
    """Check if a process with given PID exists."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False
    except Exception:
        return True  # Unknown — assume exists


class CrossProcessLock:
    """
    File-based cross-process lock.
    [!] Stale lock recovery if PID no longer exists or expired.
    [!] Lock timeout prevents permanent deadlock.
    [!] Crash-safe via OS file operations.
    """

    def acquire(self, lock_name: str, timeout_seconds: int = _DEFAULT_TIMEOUT) -> bool:
        path = _lock_path(lock_name)
        deadline = _now_ts() + timeout_seconds
        pid = os.getpid()

        while _now_ts() < deadline:
            if not os.path.exists(path):
                try:
                    self._write_lock(path, pid)
                    # Verify we own it (race condition check)
                    owner = self._read_lock(path)
                    if owner and owner.get("process_id") == pid:
                        return True
                except Exception:
                    pass
            else:
                # Try stale recovery
                if self.recover_stale(lock_name, max_age_seconds=_DEFAULT_MAX_AGE):
                    continue
            time.sleep(0.1)
        return False

    def release(self, lock_name: str) -> None:
        path = _lock_path(lock_name)
        pid = os.getpid()
        try:
            owner = self._read_lock(path)
            if owner and owner.get("process_id") == pid:
                os.remove(path)
        except Exception:
            pass

    def is_locked(self, lock_name: str) -> bool:
        return os.path.exists(_lock_path(lock_name))

    def recover_stale(self, lock_name: str, max_age_seconds: int = _DEFAULT_MAX_AGE) -> bool:
        """Recover stale lock if PID no longer exists or lock is expired."""
        path = _lock_path(lock_name)
        try:
            owner = self._read_lock(path)
            if owner is None:
                return False
            expires_at = owner.get("expires_at", 0)
            pid = owner.get("process_id", -1)
            # Recover if expired or PID gone
            if _now_ts() > expires_at or not _pid_exists(pid):
                os.remove(path)
                return True
        except Exception:
            pass
        return False

    def get_owner(self, lock_name: str) -> Dict[str, Any]:
        path = _lock_path(lock_name)
        owner = self._read_lock(path)
        if owner is None:
            return {}
        return owner

    def _write_lock(self, path: str, pid: int) -> None:
        now = _now_ts()
        data = {
            "process_id": pid,
            "acquired_at": now,
            "expires_at": now + _DEFAULT_MAX_AGE,
            "heartbeat": now,
        }
        # Write atomically via temp file
        tmp_path = path + f".tmp.{pid}"
        with open(tmp_path, "w") as f:
            json.dump(data, f)
        os.replace(tmp_path, path)

    def _read_lock(self, path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return None
