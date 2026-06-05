"""
gui/strategy_memory_adapter.py — StrategyMemoryAdapter v0.7.2

Bridge between GUI and strategy_memory package.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyMemoryAdapter:
    """
    GUI adapter for strategy_memory package.

    All methods catch exceptions and return safe defaults.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/strategy_memory",
    ):
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        self._output_dir = output_dir

    def run_memory_extraction(self, mode: str = "real") -> dict:
        """Run full strategy memory extraction pipeline. Returns summary dict."""
        try:
            from strategy_memory.strategy_memory_engine import StrategyMemoryEngine
            engine = StrategyMemoryEngine(
                project_root=_BASE_DIR,
                output_dir=self._output_dir,
            )
            result = engine.run(mode=mode)
            summary = result.get("summary")
            memories = result.get("memories", [])
            links = result.get("links", [])
            summary_dict = summary.to_dict() if summary else {}
            return {
                "ok": True,
                "summary": summary_dict,
                "memory_count": len(memories),
                "link_count": len(links),
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.run_memory_extraction error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "no_real_orders": True,
                "production_blocked": True,
            }

    def generate_report(self, mode: str = "real") -> dict:
        """Generate strategy memory Markdown report."""
        try:
            from reports.strategy_memory_report import StrategyMemoryReportBuilder
            builder = StrategyMemoryReportBuilder()
            path = builder.build(
                mode=mode,
                output_dir=os.path.join(_BASE_DIR, "reports"),
                memory_output_dir=self._output_dir,
            )
            return {
                "ok": True,
                "report_path": path,
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.generate_report error: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "no_real_orders": True,
                "production_blocked": True,
            }

    def load_latest_summary(self) -> dict:
        """Load latest summary from store."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=self._output_dir)
            summary = store.load_latest_summary()
            if summary is None:
                return {"ok": False, "summary": {}}
            return {
                "ok": True,
                "summary": summary.to_dict(),
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.load_latest_summary error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def load_memories(self) -> list:
        """Load all memories from store. Returns list of dicts."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=self._output_dir)
            memories = store.load_memories()
            return [m.to_dict() for m in memories]
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.load_memories error: %s", exc)
            return []

    def load_links(self) -> list:
        """Load all links from store. Returns list of dicts."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=self._output_dir)
            links = store.load_links()
            return [lk.to_dict() for lk in links]
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.load_links error: %s", exc)
            return []

    def search_memories(self, **filters) -> list:
        """Search memories with optional filters. Returns list of dicts."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            from strategy_memory.memory_query import StrategyMemoryQuery
            store = StrategyMemoryStore(output_dir=self._output_dir)
            memories = store.load_memories()
            query = StrategyMemoryQuery()
            results = query.search(memories, **filters)
            return [m.to_dict() for m in results]
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.search_memories error: %s", exc)
            return []

    def update_status(self, memory_id: str, status: str) -> bool:
        """Update status of a memory item. Returns True if found."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=self._output_dir)
            return store.update_status(memory_id, status)
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.update_status error: %s", exc)
            return False

    def archive_memory(self, memory_id: str) -> bool:
        """Archive a memory item. Returns True if found."""
        try:
            from strategy_memory.memory_store import StrategyMemoryStore
            store = StrategyMemoryStore(output_dir=self._output_dir)
            return store.archive_memory(memory_id)
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.archive_memory error: %s", exc)
            return False

    def load_latest_report_path(self) -> str:
        """Return path to latest strategy memory report, or empty string."""
        try:
            import glob
            pattern = os.path.join(_BASE_DIR, "reports", "strategy_memory_report_*.md")
            files = sorted(glob.glob(pattern), reverse=True)
            return files[0] if files else ""
        except Exception as exc:
            logger.warning("StrategyMemoryAdapter.load_latest_report_path error: %s", exc)
            return ""
