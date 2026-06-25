"""
paper_trading/market_data/session_v161.py — Market Data Session v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Full session lifecycle: CREATED → CONNECTING → CONNECTED → SUBSCRIBING → ACTIVE → PAUSED/HALTED/COMPLETED.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from paper_trading.market_data.enums_v161 import (
    MarketDataSessionStatus, SourceClass, FreshnessStatus,
    SequenceStatus, DataQualityStatus,
)
from paper_trading.market_data.models_v161 import MarketDataSessionConfig, MarketDataCheckpoint
from paper_trading.market_data.adapter_base_v161 import AbstractMarketDataAdapter
from paper_trading.market_data.normalizer_v161 import MarketDataNormalizer
from paper_trading.market_data.sequence_v161 import SequenceValidator
from paper_trading.market_data.deduplication_v161 import MarketDataDeduplicator
from paper_trading.market_data.freshness_v161 import FreshnessClassifier
from paper_trading.market_data.quality_v161 import DataQualityGate
from paper_trading.market_data.store_v161 import MarketDataStore
from paper_trading.market_data.lineage_v161 import MarketDataLineageTracker
from paper_trading.market_data.checkpoint_v161 import CheckpointManager

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataSession:
    """
    Full lifecycle market data session.
    Orchestrates: adapter → dedup → normalize → sequence → freshness → quality → store → lineage.
    """

    def __init__(
        self,
        config: MarketDataSessionConfig,
        adapter: AbstractMarketDataAdapter,
    ) -> None:
        self._config = config
        self._adapter = adapter
        self._status = MarketDataSessionStatus.CREATED
        self._session_id = config.session_id
        self._normalizer = MarketDataNormalizer()
        self._sequence_validator = SequenceValidator()
        self._deduplicator = MarketDataDeduplicator()
        self._freshness_classifier = FreshnessClassifier()
        self._quality_gate = DataQualityGate()
        self._store = MarketDataStore()
        self._lineage = MarketDataLineageTracker()
        self._checkpoint_manager = CheckpointManager()
        self._event_count: int = 0
        self._started_at: Optional[str] = None

    @property
    def status(self) -> MarketDataSessionStatus:
        return self._status

    @property
    def session_id(self) -> str:
        return self._session_id

    def start(self) -> bool:
        """Connect adapter, subscribe to symbols, set ACTIVE."""
        self._status = MarketDataSessionStatus.CONNECTING
        if not self._adapter.connect():
            self._status = MarketDataSessionStatus.HALTED
            return False
        self._status = MarketDataSessionStatus.SUBSCRIBING
        self._adapter.subscribe(self._config.symbols)
        self._status = MarketDataSessionStatus.ACTIVE
        self._started_at = datetime.now(timezone.utc).isoformat()
        return True

    def pause(self) -> bool:
        if self._status == MarketDataSessionStatus.ACTIVE:
            self._status = MarketDataSessionStatus.PAUSED
            return True
        return False

    def resume(self) -> bool:
        """Resume from PAUSED → ACTIVE. Operator-initiated only."""
        if self._status == MarketDataSessionStatus.PAUSED:
            self._status = MarketDataSessionStatus.ACTIVE
            return True
        return False

    def halt(self) -> bool:
        self._adapter.disconnect()
        self._status = MarketDataSessionStatus.HALTED
        return True

    def complete(self) -> bool:
        self._adapter.disconnect()
        self._status = MarketDataSessionStatus.COMPLETED
        return True

    def poll_and_process(self) -> int:
        """Poll adapter, process events through pipeline. Returns processed count."""
        if self._status != MarketDataSessionStatus.ACTIVE:
            return 0

        raw_events = self._adapter.poll()
        processed = 0

        for raw in raw_events:
            # Deduplication
            if self._deduplicator.is_duplicate(raw):
                self._lineage.record(
                    session_id=self._session_id,
                    raw_event_id=raw.event_id,
                    adapter_id=raw.adapter_id,
                    source_class=raw.source_class.value,
                    symbol=raw.symbol,
                    timestamp_utc=raw.timestamp_utc,
                    pipeline_stage="DEDUPLICATED",
                )
                continue

            # Sequence
            seq_status = self._sequence_validator.check(raw)

            # Normalize
            canonical = self._normalizer.normalize(raw)
            if canonical is None:
                self._lineage.record(
                    session_id=self._session_id,
                    raw_event_id=raw.event_id,
                    adapter_id=raw.adapter_id,
                    source_class=raw.source_class.value,
                    symbol=raw.symbol,
                    timestamp_utc=raw.timestamp_utc,
                    pipeline_stage="NORMALIZATION_FAILED",
                )
                continue

            # Freshness
            freshness = self._freshness_classifier.classify(
                canonical.timestamp_utc, canonical.source_class
            )
            canonical.freshness_status = freshness
            canonical.sequence_status = seq_status

            # Quality gate
            quality = self._quality_gate.assess(
                freshness=freshness,
                sequence=seq_status,
                is_duplicate=False,
            )
            canonical.quality_status = quality

            # Store
            event_dict = {
                "event_id": canonical.event_id,
                "symbol": canonical.symbol,
                "source_class": canonical.source_class.value,
                "timestamp_utc": canonical.timestamp_utc,
                "freshness_status": canonical.freshness_status.value,
                "sequence_status": canonical.sequence_status.value,
                "quality_status": canonical.quality_status.value,
                "research_only": True,
                "market_data_only": True,
                "no_real_order": True,
            }

            from paper_trading.market_data.enums_v161 import MarketDataEventType
            if hasattr(canonical, "bid_price"):
                event_dict.update({
                    "bid_price": str(canonical.bid_price),
                    "ask_price": str(canonical.ask_price),
                    "mid_price": str(canonical.mid_price),
                })
                self._store.store_quote(canonical.symbol, event_dict)
            elif hasattr(canonical, "price"):
                event_dict.update({
                    "price": str(canonical.price),
                    "volume": canonical.volume,
                })
                self._store.store_trade(canonical.symbol, event_dict)

            self._lineage.record(
                session_id=self._session_id,
                raw_event_id=raw.event_id,
                adapter_id=raw.adapter_id,
                source_class=raw.source_class.value,
                symbol=raw.symbol,
                timestamp_utc=raw.timestamp_utc,
                pipeline_stage="STORED",
                canonical_event_id=canonical.event_id,
            )

            self._event_count += 1
            processed += 1

        return processed

    def create_checkpoint(self) -> MarketDataCheckpoint:
        adapter_cp = self._adapter.checkpoint_state()
        return self._checkpoint_manager.create(
            session_id=self._session_id,
            adapter_id=self._adapter.adapter_id,
            adapter_state=adapter_cp.adapter_state,
            sequence_number=adapter_cp.sequence_number,
            last_event_id=adapter_cp.last_event_id,
        )

    def restore_from_checkpoint(self, checkpoint: MarketDataCheckpoint) -> bool:
        """Restore always sets status=PAUSED."""
        self._adapter.restore_state(checkpoint)
        self._status = MarketDataSessionStatus.PAUSED
        return True

    def get_status_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self._session_id,
            "status": self._status.value,
            "adapter_id": self._adapter.adapter_id,
            "source_class": self._config.source_class.value,
            "event_count": self._event_count,
            "started_at": self._started_at,
            "no_real_orders": True,
            "market_data_only": True,
            "production_trading_blocked": True,
        }

    @property
    def store(self) -> MarketDataStore:
        return self._store

    @property
    def lineage(self) -> MarketDataLineageTracker:
        return self._lineage
