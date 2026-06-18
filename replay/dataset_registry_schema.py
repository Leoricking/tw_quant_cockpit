"""
replay/dataset_registry_schema.py — Dataset Registry Schemas v1.2.8

Dataclasses and enums for Replay Dataset Catalog, Registry, Manifest,
Version, Lineage, and File Entries.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Dataset Registry does not execute trades. Not Investment Advice.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
DATASET_REGISTRY_ONLY = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DatasetMode(str, Enum):
    REAL = "REAL"
    MOCK = "MOCK"


class DatasetQualification(str, Enum):
    VERIFIED_REAL    = "VERIFIED_REAL"
    REAL_UNVERIFIED  = "REAL_UNVERIFIED"
    MOCK_DEMO_ONLY   = "MOCK_DEMO_ONLY"
    INSUFFICIENT     = "INSUFFICIENT"
    BLOCKED          = "BLOCKED"
    INCOMPATIBLE     = "INCOMPATIBLE"


class DatasetStatus(str, Enum):
    ACTIVE       = "ACTIVE"
    FROZEN       = "FROZEN"
    ARCHIVED     = "ARCHIVED"
    MISSING      = "MISSING"
    CORRUPTED    = "CORRUPTED"
    INCOMPATIBLE = "INCOMPATIBLE"
    BLOCKED      = "BLOCKED"


class FileLogicalRole(str, Enum):
    DAILY_OHLCV        = "DAILY_OHLCV"
    INTRADAY_OHLCV     = "INTRADAY_OHLCV"
    TIMEFRAME_DATA     = "TIMEFRAME_DATA"
    FEATURE_DATA       = "FEATURE_DATA"
    STRATEGY_CONTEXT   = "STRATEGY_CONTEXT"
    FUNDAMENTAL_CONTEXT = "FUNDAMENTAL_CONTEXT"
    SECTOR_CONTEXT     = "SECTOR_CONTEXT"
    METADATA           = "METADATA"
    CALENDAR           = "CALENDAR"
    OTHER              = "OTHER"


class LineageOperation(str, Enum):
    IMPORT          = "IMPORT"
    SNAPSHOT        = "SNAPSHOT"
    REBUILD         = "REBUILD"
    DERIVE          = "DERIVE"
    AGGREGATE       = "AGGREGATE"
    MIGRATE         = "MIGRATE"
    RESTORE         = "RESTORE"
    PACKAGE_IMPORT  = "PACKAGE_IMPORT"
    MANUAL_REGISTER = "MANUAL_REGISTER"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ReplayDatasetFileEntry:
    """Represents one file within a dataset."""
    file_id:        str
    relative_path:  str
    logical_role:   str                      # FileLogicalRole value
    file_type:      str
    size_bytes:     int          = 0
    row_count:      int          = 0
    content_hash:   str          = ""
    modified_at:    str          = ""
    required:       bool         = True
    present:        bool         = True
    schema_version: str          = "1.0"
    warnings:       List[str]    = field(default_factory=list)

    # safety
    research_only:  bool         = True
    no_real_orders: bool         = True


@dataclass
class ReplayDatasetManifest:
    """Full manifest for a versioned replay dataset."""
    dataset_id:              str
    dataset_name:            str
    dataset_version:         str                  = "1.0.0"
    schema_version:          str                  = "1.0"
    mode:                    str                  = DatasetMode.MOCK.value
    qualification:           str                  = DatasetQualification.MOCK_DEMO_ONLY.value
    source_type:             str                  = "UNKNOWN"
    source_name:             str                  = ""
    source_reference:        str                  = ""
    created_at:              str                  = ""
    updated_at:              str                  = ""
    frozen_at:               Optional[str]        = None
    archived_at:             Optional[str]        = None
    parent_dataset_id:       Optional[str]        = None
    parent_dataset_version:  Optional[str]        = None
    symbols:                 List[str]            = field(default_factory=list)
    timeframes:              List[str]            = field(default_factory=list)
    start_timestamp:         str                  = ""
    end_timestamp:           str                  = ""
    row_count:               int                  = 0
    file_count:              int                  = 0
    total_size_bytes:        int                  = 0
    field_names:             List[str]            = field(default_factory=list)
    field_coverage:          Dict[str, Any]       = field(default_factory=dict)
    missing_fields:          List[str]            = field(default_factory=list)
    point_in_time_verified:  bool                 = False
    future_data_check:       str                  = "NOT_CHECKED"
    fingerprint:             str                  = ""
    content_hash:            str                  = ""
    manifest_hash:           str                  = ""
    relative_paths:          List[str]            = field(default_factory=list)
    path_remap_required:     bool                 = False
    files:                   List[ReplayDatasetFileEntry] = field(default_factory=list)
    warnings:                List[str]            = field(default_factory=list)
    status:                  str                  = DatasetStatus.ACTIVE.value
    research_only:           bool                 = True
    no_real_orders:          bool                 = True


@dataclass
class ReplayDatasetVersionRecord:
    """Version record for a dataset."""
    dataset_id:     str
    version:        str
    parent_version: Optional[str] = None
    version_reason: str           = ""
    created_at:     str           = ""
    created_by:     str           = "system"
    fingerprint:    str           = ""
    manifest_hash:  str           = ""
    frozen:         bool          = False
    immutable:      bool          = False
    qualification:  str           = DatasetQualification.MOCK_DEMO_ONLY.value
    warnings:       List[str]     = field(default_factory=list)

    research_only:  bool          = True
    no_real_orders: bool          = True


@dataclass
class ReplayDatasetLineageRecord:
    """Lineage record linking parent and child datasets."""
    lineage_id:       str
    dataset_id:       str
    version:          str
    parent_dataset_id: Optional[str] = None
    parent_version:    Optional[str] = None
    operation:         str           = LineageOperation.MANUAL_REGISTER.value
    source_reference:  str           = ""
    created_at:        str           = ""
    note:              str           = ""

    research_only:     bool          = True
    no_real_orders:    bool          = True
