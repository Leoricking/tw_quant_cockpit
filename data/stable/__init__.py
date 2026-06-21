"""
data/stable/__init__.py — Provider Stable Rollup v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Stable certification of all providers through v1.4.8 Integration baseline.
[!] No new providers. No authority drift. No silent fallback.
"""
from __future__ import annotations

VERSION      = "1.4.9"
RELEASE_NAME = "Provider Stable Rollup"

# Stable baseline test constants
PREVIOUS_FULL_COLLECTION_BASELINE = 3597
PREVIOUS_FULL_PASS_BASELINE       = 3597
PREVIOUS_SKIPPED_BASELINE         = 0

# Capability availability flags
STABLE_MANIFEST_AVAILABLE           = True
STABLE_PROVIDER_REGISTRY_AVAILABLE  = True
COMPATIBILITY_CONTRACT_AVAILABLE    = True
SCHEMA_VERSION_REGISTRY_AVAILABLE   = True
POLICY_VERSION_REGISTRY_AVAILABLE   = True
STABLE_BASELINE_SNAPSHOT_AVAILABLE  = True
TEST_MANIFEST_AVAILABLE             = True
COLLECTION_INTEGRITY_AVAILABLE      = True
HEALTH_BASELINE_AVAILABLE           = True
PROVIDER_STABLE_PROFILES_AVAILABLE  = True

# Provider constraint flags — ALWAYS FALSE
FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
PTT_STANDALONE_FORMAL_CONCLUSION      = False
PTT_CAN_GENERATE_BUY_SELL             = False

# Safety flags
NO_REAL_ORDERS             = True
BROKER_EXECUTION_ENABLED   = False  # ALWAYS FALSE
PRODUCTION_TRADING_BLOCKED = True
AUTO_FALLBACK_ENABLED      = False  # ALWAYS FALSE
AUTO_OVERRIDE_ENABLED      = False  # ALWAYS FALSE
AUTO_REPAIR_ENABLED        = False  # ALWAYS FALSE
MOCK_FALLBACK_ENABLED      = False  # ALWAYS FALSE
