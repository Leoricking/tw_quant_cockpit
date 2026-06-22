"""
tests/test_source_lineage_rate_limit_v145.py — Source Lineage & Rate Limit Tests v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All tests are OFFLINE. No real network requests.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

import pytest

# Safety flags
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
RATE_LIMIT_AUTO_BYPASS_ENABLED = False

# =====================================================================
# Helpers
# =====================================================================

def _make_lineage(
    lineage_id=None, provider_id="twse_official",
    authority_level="PRIMARY_OFFICIAL", dataset="daily_ohlcv",
    observation_date="2024-01-02", source_content_hash="abc",
    normalized_content_hash="def", schema_version="1.0",
    parser_version="1.4.0", fetched_at=None, quality_status="VALID",
    freshness_status="FRESH", mode="real", **kwargs,
):
    from data.governance.models_v145 import SourceLineageRecord
    now = datetime.now(timezone.utc).isoformat()
    return SourceLineageRecord(
        lineage_id=lineage_id or str(uuid.uuid4()),
        parent_lineage_ids=[],
        root_lineage_id="",
        provider_id=provider_id,
        source_id="twse_official_v140",
        authority_level=authority_level,
        dataset=dataset,
        endpoint="/v1/daily",
        request_fingerprint="fp_" + (lineage_id or "x"),
        fetch_run_id="run_001",
        response_id="resp_001",
        cache_entry_id="",
        record_key="2330/2024-01-02",
        observation_date=observation_date,
        reporting_period=None,
        published_at=now,
        available_from=now,
        fetched_at=fetched_at or now,
        normalized_at=now,
        source_content_hash=source_content_hash,
        normalized_content_hash=normalized_content_hash,
        schema_id="twse_daily_v1",
        schema_version=schema_version,
        parser_version=parser_version,
        transformation_ids=[],
        quality_status=quality_status,
        freshness_status=freshness_status,
        PIT_status="DATE_ONLY",
        conflict_status="NONE",
        formal_use_allowed=False,
        provenance_complete=False,
        **kwargs,
    )


def _make_request_entry(request_id=None, provider_id="twse", host="www.twse.com.tw",
                        status="COMPLETED"):
    from data.governance.models_v145 import RequestLedgerEntry
    now = datetime.now(timezone.utc).isoformat()
    return RequestLedgerEntry(
        request_id=request_id or str(uuid.uuid4()),
        provider_id=provider_id,
        host=host,
        endpoint="/v1/daily",
        endpoint_family="daily",
        dataset="daily_ohlcv",
        request_fingerprint="fp_test",
        method="GET",
        mode="real",
        started_at=now,
        finished_at=now,
        status=status,
    )


# =====================================================================
# Group 1: Authority (10 tests)
# =====================================================================

class TestSourceAuthority:

    def test_authority_level_enum_values(self):
        from data.governance.models_v145 import SourceAuthorityLevel
        assert SourceAuthorityLevel.PRIMARY_OFFICIAL.value == "PRIMARY_OFFICIAL"
        assert SourceAuthorityLevel.SECONDARY_AGGREGATOR.value == "SECONDARY_AGGREGATOR"
        assert SourceAuthorityLevel.MOCK.value == "MOCK"
        assert SourceAuthorityLevel.UNKNOWN.value == "UNKNOWN"

    def test_authority_registry_builtin_mappings(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.get_authority("twse") == SourceAuthorityLevel.PRIMARY_OFFICIAL
        assert reg.get_authority("tpex") == SourceAuthorityLevel.PRIMARY_OFFICIAL
        assert reg.get_authority("mops") == SourceAuthorityLevel.PRIMARY_OFFICIAL
        assert reg.get_authority("data_gov_tw") == SourceAuthorityLevel.PRIMARY_DOMAIN_OFFICIAL
        assert reg.get_authority("finmind") == SourceAuthorityLevel.SECONDARY_AGGREGATOR

    def test_authority_unknown_provider(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.get_authority("nonexistent_provider") == SourceAuthorityLevel.UNKNOWN

    def test_authority_cannot_override_higher(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert not reg.can_override(
            SourceAuthorityLevel.SECONDARY_AGGREGATOR,
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
        )

    def test_authority_can_override_lower(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.can_override(
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
            SourceAuthorityLevel.SECONDARY_AGGREGATOR,
        )

    def test_authority_equal_level_no_override(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert not reg.can_override(
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
        )

    def test_formal_use_not_allowed_for_mock(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert not reg.is_formal_allowed(SourceAuthorityLevel.MOCK)
        assert not reg.is_formal_allowed(SourceAuthorityLevel.TEST_FIXTURE)
        assert not reg.is_formal_allowed(SourceAuthorityLevel.UNKNOWN)

    def test_formal_use_allowed_for_primary(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.is_formal_allowed(SourceAuthorityLevel.PRIMARY_OFFICIAL)
        assert reg.is_formal_allowed(SourceAuthorityLevel.PRIMARY_DOMAIN_OFFICIAL)

    def test_compare_authority_ordering(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.compare_authority(
            SourceAuthorityLevel.PRIMARY_OFFICIAL, SourceAuthorityLevel.SECONDARY_AGGREGATOR
        ) == 1
        assert reg.compare_authority(
            SourceAuthorityLevel.MOCK, SourceAuthorityLevel.PRIMARY_OFFICIAL
        ) == -1
        assert reg.compare_authority(
            SourceAuthorityLevel.PRIMARY_OFFICIAL, SourceAuthorityLevel.PRIMARY_OFFICIAL
        ) == 0

    def test_validate_authority_decision_valid(self):
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        result = reg.validate_authority_decision(
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
            SourceAuthorityLevel.SECONDARY_AGGREGATOR,
        )
        assert result["valid"] is True
        assert result["decision"] == "PRIMARY_WINS"


# =====================================================================
# Group 2: Fingerprint (8 tests)
# =====================================================================

class TestRequestFingerprint:

    def test_fingerprint_sha256_length(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                         "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                         "1.0", "real", "v1")
        assert len(fp) == 64

    def test_fingerprint_deterministic(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp1 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1")
        fp2 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1")
        assert fp1 == fp2

    def test_fingerprint_different_provider(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp_twse = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                              "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                              "1.0", "real", "v1")
        fp_tpex = svc.compute("tpex", "www.twse.com.tw", "/v1/daily", "GET",
                              "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                              "1.0", "real", "v1")
        assert fp_twse != fp_tpex

    def test_fingerprint_different_mode(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp_real = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                              "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                              "1.0", "real", "v1")
        fp_mock = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                              "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                              "1.0", "mock", "v1")
        assert fp_real != fp_mock

    def test_fingerprint_secrets_removed(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp1 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1",
                          extra_params={"token": "secret_value"})
        fp2 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1",
                          extra_params={"token": "different_secret"})
        assert fp1 == fp2  # Token excluded → same fingerprint

    def test_fingerprint_param_order_independent(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp1 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1",
                          extra_params={"a": 1, "b": 2})
        fp2 = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1",
                          extra_params={"b": 2, "a": 1})
        assert fp1 == fp2

    def test_fingerprint_method_case_insensitive(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp_lower = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "get",
                               "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                               "1.0", "real", "v1")
        fp_upper = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                               "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                               "1.0", "real", "v1")
        assert fp_lower == fp_upper

    def test_fingerprint_remove_secrets_utility(self):
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        cleaned = svc._remove_secrets({
            "token": "secret",
            "api_key": "key123",
            "symbol": "2330",
            "date": "2024-01-02",
        })
        assert "token" not in cleaned
        assert "api_key" not in cleaned
        assert "symbol" in cleaned
        assert "date" in cleaned


# =====================================================================
# Group 3: Lineage (12 tests)
# =====================================================================

class TestLineageRegistry:

    def test_register_and_get_source(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        from data.governance.models_v145 import SourceIdentity
        reg = SourceLineageRegistry()
        si = SourceIdentity(
            source_id="test_src", provider_id="twse", provider_name="TWSE",
            source_type="official", authority_level="PRIMARY_OFFICIAL",
            official=True, aggregator=False, market="TW", domain="equity",
            agency="TWSE", host="www.twse.com.tw", endpoint_family="daily",
            dataset="daily_ohlcv",
        )
        reg.register_source(si)
        retrieved = reg.get_source("test_src")
        assert retrieved is not None
        assert retrieved.source_id == "test_src"

    def test_list_sources_empty(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        assert reg.list_sources() == []

    def test_list_sources_filtered_by_provider(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        from data.governance.models_v145 import SourceIdentity
        reg = SourceLineageRegistry()
        for pid, sid in [("twse", "twse_src"), ("tpex", "tpex_src")]:
            si = SourceIdentity(
                source_id=sid, provider_id=pid, provider_name=pid,
                source_type="official", authority_level="PRIMARY_OFFICIAL",
                official=True, aggregator=False, market="TW", domain="equity",
                agency=pid, host=f"www.{pid}.com.tw",
                endpoint_family="daily", dataset="daily_ohlcv",
            )
            reg.register_source(si)
        twse_sources = reg.list_sources(provider_id="twse")
        assert len(twse_sources) == 1
        assert twse_sources[0]["source_id"] == "twse_src"

    def test_record_and_get_lineage(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        record = _make_lineage("lin001")
        reg.record_lineage(record)
        retrieved = reg.get_lineage("lin001")
        assert retrieved is not None
        assert retrieved.lineage_id == "lin001"

    def test_trace_to_root_single(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        record = _make_lineage("lin_root")
        reg.record_lineage(record)
        chain = reg.trace_to_root("lin_root")
        assert "lin_root" in chain

    def test_trace_to_root_chain(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        parent = _make_lineage("parent_001")
        child = _make_lineage("child_001")
        reg.record_lineage(parent)
        reg.record_lineage(child)
        reg.link_parent_lineage("child_001", "parent_001")
        chain = reg.trace_to_root("child_001")
        assert "child_001" in chain
        assert "parent_001" in chain

    def test_validate_lineage_complete(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        record = _make_lineage("lin_valid")
        reg.record_lineage(record)
        result = reg.validate_lineage("lin_valid")
        assert result["is_valid"] is True

    def test_validate_lineage_missing_fields(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        from data.governance.models_v145 import SourceLineageRecord
        reg = SourceLineageRegistry()
        from datetime import timezone
        now = datetime.now(timezone.utc).isoformat()
        bad = SourceLineageRecord(
            lineage_id="lin_bad",
            parent_lineage_ids=[], root_lineage_id="",
            provider_id="",  # Missing
            source_id="", authority_level="PRIMARY_OFFICIAL",
            dataset="daily", endpoint="", request_fingerprint="fp",
            fetch_run_id="", response_id="", cache_entry_id="", record_key="",
            observation_date="2024-01-01", reporting_period=None,
            published_at=now, available_from=now, fetched_at=now, normalized_at=now,
            source_content_hash="hash", normalized_content_hash="hash",
            schema_id="s", schema_version="1.0", parser_version="1.0",
            transformation_ids=[], quality_status="VALID", freshness_status="FRESH",
            PIT_status="UNKNOWN", conflict_status="NONE",
        )
        reg.record_lineage(bad)
        result = reg.validate_lineage("lin_bad")
        assert result["is_valid"] is False
        assert len(result["issues"]) > 0

    def test_validate_provenance_completeness_pass(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        from data.governance.models_v145 import ProvenanceGateResult
        reg = SourceLineageRegistry()
        record = _make_lineage("lin_prov")
        reg.record_lineage(record)
        result = reg.validate_provenance_completeness("lin_prov")
        assert result == ProvenanceGateResult.PASS

    def test_validate_provenance_completeness_blocked_mock(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        from data.governance.models_v145 import ProvenanceGateResult
        reg = SourceLineageRegistry()
        record = _make_lineage("lin_mock", authority_level="MOCK")
        reg.record_lineage(record)
        result = reg.validate_provenance_completeness("lin_mock")
        assert result == ProvenanceGateResult.BLOCKED

    def test_compare_lineage(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        a = _make_lineage("lin_a")
        b = _make_lineage("lin_b")
        reg.record_lineage(a)
        reg.record_lineage(b)
        result = reg.compare_lineage("lin_a", "lin_b")
        assert result["a_found"] is True
        assert result["b_found"] is True

    def test_list_incomplete_lineage(self):
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        record = _make_lineage("lin_inc")
        record.provenance_complete = False
        reg.record_lineage(record)
        incomplete = reg.list_incomplete_lineage()
        assert any(r["lineage_id"] == "lin_inc" for r in incomplete)


# =====================================================================
# Group 4: Provenance Gate (7 tests)
# =====================================================================

class TestProvenanceGate:

    def test_gate_pass_all_fields(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov001")
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "PASS"
        assert result["passed"] is True

    def test_gate_fail_missing_source_hash(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        # Use SECONDARY_AGGREGATOR so PRIMARY_OFFICIAL blocking logic does not trigger
        record = _make_lineage("prov002", authority_level="SECONDARY_AGGREGATOR", source_content_hash="")
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "FAIL"

    def test_gate_fail_missing_parser_version(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov003", parser_version="")
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "FAIL"

    def test_gate_blocked_mock_in_real_mode(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov004", authority_level="MOCK")
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "BLOCKED"

    def test_gate_blocked_fixture_in_real_mode(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov005", authority_level="TEST_FIXTURE")
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "BLOCKED"

    def test_gate_fail_missing_observation_date(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov006", observation_date=None)
        record.reporting_period = None
        result = gate.check(record, mode="real")
        assert result["gate_result"] == "FAIL"

    def test_gate_fail_pit_required_no_available_from(self):
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        record = _make_lineage("prov007")
        record.available_from = None
        result = gate.check(record, mode="real", pit_required=True)
        assert result["gate_result"] == "BLOCKED"


# =====================================================================
# Group 5: Request Ledger (14 tests)
# =====================================================================

class TestRequestLedger:

    def test_record_and_get(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        entry = _make_request_entry("req001")
        ledger.record(entry)
        retrieved = ledger.get("req001")
        assert retrieved is not None
        assert retrieved.request_id == "req001"

    def test_append_only_no_duplicate(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        entry = _make_request_entry("req002")
        ledger.record(entry)
        ledger.record(entry)  # Same entry twice
        assert len(ledger._order) == 1

    def test_token_redacted(self):
        from data.governance.request_ledger_v145 import RequestLedger
        from data.governance.models_v145 import RequestLedgerEntry
        ledger = RequestLedger()
        now = datetime.now(timezone.utc).isoformat()
        entry = RequestLedgerEntry(
            request_id="req_tok", provider_id="finmind", host="api.finmindtrade.com",
            endpoint="/v4/data", endpoint_family="v4", dataset="TaiwanStockPrice",
            request_fingerprint="fp", method="GET", mode="real", started_at=now,
            safe_request_metadata={"token": "super_secret_value", "param": "ok"},
        )
        ledger.record(entry)
        stored = ledger.get("req_tok")
        assert stored.safe_request_metadata.get("token") == "[REDACTED]"
        assert stored.safe_request_metadata.get("param") == "ok"

    def test_auth_header_redacted(self):
        from data.governance.request_ledger_v145 import RequestLedger
        from data.governance.models_v145 import RequestLedgerEntry
        ledger = RequestLedger()
        now = datetime.now(timezone.utc).isoformat()
        entry = RequestLedgerEntry(
            request_id="req_auth", provider_id="finmind", host="api.finmindtrade.com",
            endpoint="/v4/data", endpoint_family="v4", dataset="TaiwanStockPrice",
            request_fingerprint="fp", method="GET", mode="real", started_at=now,
            safe_request_metadata={"Authorization": "Bearer token123"},
        )
        ledger.record(entry)
        stored = ledger.get("req_auth")
        assert stored.safe_request_metadata.get("Authorization") == "[REDACTED]"

    def test_update_status(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        entry = _make_request_entry("req003", status="PLANNED")
        ledger.record(entry)
        ledger.update_status("req003", "COMPLETED", records_received=10)
        stored = ledger.get("req003")
        assert stored.status == "COMPLETED"
        assert stored.records_received == 10

    def test_list_by_provider(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        ledger.record(_make_request_entry("r1", provider_id="twse"))
        ledger.record(_make_request_entry("r2", provider_id="tpex"))
        ledger.record(_make_request_entry("r3", provider_id="twse"))
        twse = ledger.list_by_provider("twse")
        assert len(twse) == 2

    def test_list_by_host(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        ledger.record(_make_request_entry("h1", host="www.twse.com.tw"))
        ledger.record(_make_request_entry("h2", host="www.tpex.org.tw"))
        twse_list = ledger.list_by_host("www.twse.com.tw")
        assert len(twse_list) == 1

    def test_list_by_fetch_run(self):
        from data.governance.request_ledger_v145 import RequestLedger
        from data.governance.models_v145 import RequestLedgerEntry
        ledger = RequestLedger()
        now = datetime.now(timezone.utc).isoformat()
        entry = RequestLedgerEntry(
            request_id="fr1", provider_id="twse", host="www.twse.com.tw",
            endpoint="/v1/daily", endpoint_family="daily", dataset="daily_ohlcv",
            request_fingerprint="fp", method="GET", mode="real", started_at=now,
            fetch_run_id="run_xyz",
        )
        ledger.record(entry)
        result = ledger.list_by_fetch_run("run_xyz")
        assert len(result) == 1

    def test_list_by_time_range(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        entry = _make_request_entry("time1")
        entry.started_at = "2024-01-02T10:00:00+00:00"
        ledger.record(entry)
        results = ledger.list_by_time_range("2024-01-01", "2024-01-03")
        assert len(results) == 1

    def test_get_stats_empty(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        stats = ledger.get_stats()
        assert stats["total"] == 0
        assert stats["success_rate"] == 0.0

    def test_get_stats_with_entries(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        ledger.record(_make_request_entry("s1", status="COMPLETED"))
        ledger.record(_make_request_entry("s2", status="FAILED"))
        stats = ledger.get_stats()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["failed"] == 1

    def test_get_stats_filtered_by_provider(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        ledger.record(_make_request_entry("p1", provider_id="twse"))
        ledger.record(_make_request_entry("p2", provider_id="tpex"))
        stats = ledger.get_stats(provider_id="twse")
        assert stats["total"] == 1

    def test_record_returns_request_id(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        entry = _make_request_entry("ret001")
        result = ledger.record(entry)
        assert result == "ret001"

    def test_get_nonexistent_returns_none(self):
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        assert ledger.get("nonexistent_id") is None


# =====================================================================
# Group 6: Fetch Run (9 tests)
# =====================================================================

class TestFetchRunAudit:

    def test_create_run(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test_user", "real", dry_run=True, request_budget=10)
        assert run is not None
        assert run.overall_status == "PLANNED"
        assert run.dry_run is True
        assert run.request_budget == 10

    def test_start_run(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.start_run(run.fetch_run_id)
        updated = svc.get_run(run.fetch_run_id)
        assert updated.overall_status == "RUNNING"
        assert updated.started_at is not None

    def test_complete_run_success(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.start_run(run.fetch_run_id)
        svc.record_request_outcome(run.fetch_run_id, "COMPLETED", records=5)
        svc.complete_run(run.fetch_run_id)
        updated = svc.get_run(run.fetch_run_id)
        assert updated.overall_status == "SUCCESS"

    def test_complete_run_partial(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.start_run(run.fetch_run_id)
        svc.record_request_outcome(run.fetch_run_id, "COMPLETED", records=3)
        svc.record_request_outcome(run.fetch_run_id, "FAILED")
        svc.complete_run(run.fetch_run_id)
        updated = svc.get_run(run.fetch_run_id)
        assert updated.overall_status == "PARTIAL_SUCCESS"

    def test_fail_run(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.fail_run(run.fetch_run_id, errors=["Connection error"])
        updated = svc.get_run(run.fetch_run_id)
        assert updated.overall_status == "FAILED"
        assert "Connection error" in updated.errors

    def test_cancel_run(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.cancel_run(run.fetch_run_id)
        updated = svc.get_run(run.fetch_run_id)
        assert updated.overall_status == "CANCELLED"

    def test_list_runs(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        for pid in ["twse", "tpex", "twse"]:
            svc.create_run(pid, "test", "real")
        all_runs = svc.list_runs()
        assert len(all_runs) == 3
        twse_runs = svc.list_runs(provider_id="twse")
        assert len(twse_runs) == 2

    def test_fetch_run_id_unique(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run1 = svc.create_run("twse", "test", "real")
        run2 = svc.create_run("twse", "test", "real")
        assert run1.fetch_run_id != run2.fetch_run_id

    def test_cache_hits_tracked(self):
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real")
        svc.record_request_outcome(run.fetch_run_id, "COMPLETED", cache_hit=True)
        updated = svc.get_run(run.fetch_run_id)
        assert updated.cache_hits == 1


# =====================================================================
# Group 7: Rate Limit (14 tests)
# =====================================================================

class TestRateLimitManager:

    def _mock_clock(self, start=1000.0):
        self._time = start
        return lambda: self._time

    def test_acquire_allows_first_request(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        clock = lambda: 1000.0
        mgr = CentralRateLimitManager(clock=clock)
        result = mgr.acquire("twse", "www.twse.com.tw", "daily", "daily_ohlcv")
        assert result is True

    def test_acquire_respects_minimum_interval(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.acquire("twse", "www.twse.com.tw", "daily", "daily_ohlcv")
        mgr.release("twse", "www.twse.com.tw")
        # Try immediately again (within minimum interval)
        result = mgr.acquire("twse", "www.twse.com.tw", "daily", "daily_ohlcv")
        assert result is False  # Blocked by minimum interval

    def test_release_decrements_concurrent(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        clock = lambda: 1000.0
        mgr = CentralRateLimitManager(clock=clock)
        mgr.acquire("twse", "www.twse.com.tw", "daily", "daily_ohlcv")
        state_before = mgr.get_host_state("www.twse.com.tw")
        assert state_before["concurrent"] == 1
        mgr.release("twse", "www.twse.com.tw")
        state_after = mgr.get_host_state("www.twse.com.tw")
        assert state_after["concurrent"] == 0

    def test_can_request_true_on_fresh_start(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        clock = lambda: 1000.0
        mgr = CentralRateLimitManager(clock=clock)
        result = mgr.can_request("twse", "www.twse.com.tw", "daily")
        assert result["allowed"] is True

    def test_can_request_false_during_cooldown(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.start_cooldown("twse", "www.twse.com.tw", 60.0)
        result = mgr.can_request("twse", "www.twse.com.tw", "daily")
        assert result["allowed"] is False
        assert result["reason"] == "cooldown"

    def test_record_rate_limit_sets_retry_after(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.record_rate_limit("twse", "www.twse.com.tw", retry_after_seconds=30.0)
        result = mgr.can_request("twse", "www.twse.com.tw", "daily")
        assert result["allowed"] is False
        assert result["reason"] == "retry_after"

    def test_retry_after_expires(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.record_rate_limit("twse", "www.twse.com.tw", retry_after_seconds=10.0)
        t[0] = 1011.0  # Advance past retry-after
        mgr.reset_expired_windows()
        result = mgr.can_request("twse", "www.twse.com.tw", "daily")
        assert result["allowed"] is True

    def test_estimate_wait_zero_when_allowed(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        clock = lambda: 1000.0
        mgr = CentralRateLimitManager(clock=clock)
        wait = mgr.estimate_wait("twse", "www.twse.com.tw")
        assert wait == 0.0

    def test_estimate_wait_positive_during_cooldown(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.start_cooldown("twse", "www.twse.com.tw", 60.0)
        wait = mgr.estimate_wait("twse", "www.twse.com.tw")
        assert wait > 0.0

    def test_record_response_updates_state(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        clock = lambda: 1000.0
        mgr = CentralRateLimitManager(clock=clock)
        mgr.record_response("twse", "www.twse.com.tw", "COMPLETED", 150.0)
        state = mgr.get_provider_state("twse")
        assert state.get("last_status") == "COMPLETED"

    def test_get_budget_state(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        mgr = CentralRateLimitManager()
        state = mgr.get_budget_state("twse")
        assert "provider_id" in state
        assert state["provider_id"] == "twse"

    def test_rate_limit_auto_bypass_disabled(self):
        from data.governance.rate_limit_manager_v145 import RATE_LIMIT_AUTO_BYPASS_ENABLED
        assert RATE_LIMIT_AUTO_BYPASS_ENABLED is False

    def test_apply_retry_after(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [1000.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        mgr.apply_retry_after("twse", "www.twse.com.tw", 30.0)
        state = mgr.get_host_state("www.twse.com.tw")
        assert state["retry_after_until"] == 1030.0

    def test_thread_safety_acquire(self):
        from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
        t = [0.0]
        clock = lambda: t[0]
        mgr = CentralRateLimitManager(clock=clock)
        results = []
        def do_acquire():
            r = mgr.acquire("twse", "www.twse.com.tw", "daily", "daily_ohlcv")
            results.append(r)
        threads = [threading.Thread(target=do_acquire) for _ in range(3)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        # Only 1 should succeed (concurrency_limit=1, first request sets last_request_at)
        assert results.count(True) <= 1


# =====================================================================
# Group 8: Budget (9 tests)
# =====================================================================

class TestProviderBudget:

    def test_get_builtin_budget(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        budget = reg.get_budget("twse")
        assert budget.session_limit == 50
        assert budget.hourly_limit == 200

    def test_check_budget_available(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        result = reg.check_budget("twse", 1)
        assert result["allowed"] is True
        assert result["status"] == "AVAILABLE"

    def test_check_budget_exhausted_after_consume(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        budget = reg.get_budget("finmind")
        reg.consume("finmind", budget.session_limit)
        result = reg.check_budget("finmind", 1)
        assert result["allowed"] is False

    def test_consume_increments_count(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        reg.consume("twse", 5)
        result = reg.check_budget("twse", 1)
        remaining = result.get("remaining")
        assert remaining == 45

    def test_retry_consumes_budget(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        reg.consume("twse", 1, is_retry=True)
        result = reg.check_budget("twse", 1)
        assert result.get("remaining") == 49

    def test_reset_session(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        reg.consume("twse", 20)
        reg.reset_session("twse")
        result = reg.check_budget("twse", 1)
        assert result["allowed"] is True
        assert result.get("remaining") == 50

    def test_unknown_provider_default_budget(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        budget = reg.get_budget("unknown_provider_xyz")
        assert budget is not None
        assert budget.session_limit > 0

    def test_block_large_batch_on_low_confidence(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        result = reg.check_budget("twse", 15, is_batch=True)
        # confidence=LOW → block large batch
        assert result["allowed"] is False

    def test_finmind_has_lower_budget(self):
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        twse = reg.get_budget("twse")
        finmind = reg.get_budget("finmind")
        assert finmind.session_limit < twse.session_limit


# =====================================================================
# Group 9: Quota Evidence (9 tests)
# =====================================================================

class TestQuotaEvidence:

    def test_extract_from_headers_ratelimit(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        ev = svc.extract_from_headers("finmind", "api.finmindtrade.com",
                                      {"X-RateLimit-Remaining": "42"})
        assert ev is not None
        assert ev.remaining == 42

    def test_no_auth_headers_stored(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        ev = svc.extract_from_headers("finmind", "api.finmindtrade.com", {
            "X-RateLimit-Remaining": "50",
            "Authorization": "Bearer secret_token",
            "Cookie": "session=abc",
        })
        assert ev is not None
        assert "Authorization" not in ev.HTTP_headers
        assert "Cookie" not in ev.HTTP_headers
        assert "X-RateLimit-Remaining" in ev.HTTP_headers

    def test_extract_from_payload_402(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        ev = svc.extract_from_payload("finmind", 402, "Quota exceeded")
        assert ev is not None
        assert ev.payload_message_class == "QUOTA_EXCEEDED"

    def test_extract_from_payload_429(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        ev = svc.extract_from_payload("finmind", 429, "Too many requests")
        assert ev is not None
        assert ev.payload_message_class == "RATE_LIMITED"

    def test_record_and_get_latest(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        from data.governance.models_v145 import QuotaEvidence
        svc = QuotaEvidenceService()
        ev = QuotaEvidence(
            evidence_id="ev001", provider_id="finmind",
            host="api.finmindtrade.com", source="TEST",
            captured_at=datetime.now(timezone.utc).isoformat(),
            remaining=30, confidence="HIGH",
        )
        svc.record_evidence(ev)
        latest = svc.get_latest("finmind", "api.finmindtrade.com")
        assert latest is not None
        assert latest.remaining == 30

    def test_is_stale_fresh_evidence(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        from data.governance.models_v145 import QuotaEvidence
        svc = QuotaEvidenceService()
        ev = QuotaEvidence(
            evidence_id="ev_fresh", provider_id="finmind",
            host="api.finmindtrade.com", source="TEST",
            captured_at=datetime.now(timezone.utc).isoformat(),
        )
        svc.record_evidence(ev)
        assert svc.is_stale("ev_fresh", max_age_seconds=3600) is False

    def test_is_stale_nonexistent(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        assert svc.is_stale("nonexistent_evidence_id") is True

    def test_classify_payload_message(self):
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        assert svc.classify_payload_message("quota_exceeded today") == "QUOTA_EXCEEDED"
        assert svc.classify_payload_message("Rate limited please retry") == "RATE_LIMITED"

    def test_no_secret_header_prefixes(self):
        from data.governance.quota_evidence_v145 import _SECRET_HEADER_PREFIXES
        assert "authorization" in _SECRET_HEADER_PREFIXES
        assert "cookie" in _SECRET_HEADER_PREFIXES


# =====================================================================
# Group 10: Cross-Process Lock (8 tests)
# =====================================================================

class TestCrossProcessLock:

    def test_acquire_and_release(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        lock_name = f"test_lock_{uuid.uuid4().hex[:8]}"
        try:
            acquired = lock.acquire(lock_name, timeout_seconds=5)
            assert acquired is True
            assert lock.is_locked(lock_name) is True
        finally:
            lock.release(lock_name)
        assert lock.is_locked(lock_name) is False

    def test_is_locked_false_when_not_acquired(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        lock_name = f"test_nolock_{uuid.uuid4().hex[:8]}"
        assert lock.is_locked(lock_name) is False

    def test_recover_stale_nonexistent(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        result = lock.recover_stale(f"nonexistent_{uuid.uuid4().hex[:8]}")
        assert result is False

    def test_get_owner_locked(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        lock_name = f"test_owner_{uuid.uuid4().hex[:8]}"
        try:
            lock.acquire(lock_name, timeout_seconds=5)
            owner = lock.get_owner(lock_name)
            assert "process_id" in owner
        finally:
            lock.release(lock_name)

    def test_get_owner_not_locked(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        owner = lock.get_owner(f"no_lock_{uuid.uuid4().hex[:8]}")
        assert owner == {}

    def test_lock_path_safe_chars(self):
        from data.governance.cross_process_lock_v145 import _lock_path
        path = _lock_path("test/lock:name")
        assert "/" not in os.path.basename(path)
        assert ":" not in os.path.basename(path)

    def test_double_release_safe(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        lock_name = f"test_double_{uuid.uuid4().hex[:8]}"
        lock.acquire(lock_name, timeout_seconds=5)
        lock.release(lock_name)
        lock.release(lock_name)  # Double release must not raise

    def test_owner_pid_is_current_process(self):
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        import os as _os
        lock = CrossProcessLock()
        lock_name = f"test_pid_{uuid.uuid4().hex[:8]}"
        try:
            lock.acquire(lock_name, timeout_seconds=5)
            owner = lock.get_owner(lock_name)
            assert owner.get("process_id") == _os.getpid()
        finally:
            lock.release(lock_name)


# =====================================================================
# Group 11: Cache Lineage (7 tests)
# =====================================================================

class TestCacheLineage:

    def test_record_and_get(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        svc.record_cache_entry(
            cache_entry_id="cache001",
            provider_id="twse",
            request_fingerprint="fp_001",
            source_lineage_id="lin_001",
            schema_version="1.0",
            parser_version="1.4.0",
            content_hash="hash_abc",
            mode="real",
            authority="PRIMARY_OFFICIAL",
            freshness_at_write="FRESH",
        )
        entry = svc.get_cache_entry("cache001")
        assert entry is not None
        assert entry["source_lineage_id"] == "lin_001"

    def test_trace_to_source(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        svc.record_cache_entry(
            cache_entry_id="cache002", provider_id="twse",
            request_fingerprint="fp_002", source_lineage_id="lin_002",
            schema_version="1.0", parser_version="1.4.0",
            content_hash="hash_def", mode="real",
            authority="PRIMARY_OFFICIAL", freshness_at_write="FRESH",
        )
        result = svc.trace_to_source("cache002")
        assert result["found"] is True
        assert "lin_002" in result["source_lineage_chain"]

    def test_trace_nonexistent(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        result = svc.trace_to_source("nonexistent_cache_id")
        assert result["found"] is False

    def test_invalidate_cache_entry(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        svc.record_cache_entry(
            cache_entry_id="cache003", provider_id="twse",
            request_fingerprint="fp_003", source_lineage_id="lin_003",
            schema_version="1.0", parser_version="1.4.0",
            content_hash="hash_ghi", mode="real",
            authority="PRIMARY_OFFICIAL", freshness_at_write="FRESH",
        )
        svc.invalidate("cache003", "schema_changed")
        validation = svc.validate_cache_lineage("cache003")
        assert not validation["is_complete"]

    def test_validate_mock_cache_incomplete(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        svc.record_cache_entry(
            cache_entry_id="cache_mock", provider_id="mock",
            request_fingerprint="fp_mock", source_lineage_id="lin_mock",
            schema_version="1.0", parser_version="1.4.0",
            content_hash="hash_mock", mode="mock",
            authority="MOCK", freshness_at_write="UNKNOWN",
        )
        validation = svc.validate_cache_lineage("cache_mock")
        assert not validation["is_complete"]

    def test_validate_complete_cache_entry(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        svc.record_cache_entry(
            cache_entry_id="cache_good", provider_id="twse",
            request_fingerprint="fp_good", source_lineage_id="lin_good",
            schema_version="1.0", parser_version="1.4.0",
            content_hash="hash_good", mode="real",
            authority="PRIMARY_OFFICIAL", freshness_at_write="FRESH",
        )
        validation = svc.validate_cache_lineage("cache_good")
        assert validation["is_complete"] is True

    def test_validate_nonexistent_incomplete(self):
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        result = svc.validate_cache_lineage("nonexistent_cache")
        assert result["is_complete"] is False


# =====================================================================
# Group 12: Conflict Lineage (7 tests)
# =====================================================================

class TestConflictLineage:

    def _make_conflict(self, conflict_id=None):
        from data.governance.models_v145 import ConflictLineage
        return ConflictLineage(
            conflict_id=conflict_id or str(uuid.uuid4()),
            primary_lineage_id="lin_primary",
            secondary_lineage_id="lin_secondary",
            primary_provider="twse",
            secondary_provider="finmind",
            field_name="close_price",
            difference=0.5,
            tolerance=0.1,
            conflict_type="VALUE_CONFLICT",
            formal_use_blocked=True,
        )

    def test_record_and_get_conflict(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        conflict = self._make_conflict("conf001")
        svc.record_conflict(conflict)
        retrieved = svc.get_conflict("conf001")
        assert retrieved is not None
        assert retrieved.conflict_id == "conf001"

    def test_list_blocking_conflicts(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        conflict = self._make_conflict("conf002")
        svc.record_conflict(conflict)
        blocking = svc.list_blocking_conflicts()
        assert any(c["conflict_id"] == "conf002" for c in blocking)

    def test_list_conflicts_by_provider(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        svc.record_conflict(self._make_conflict("conf003"))
        results = svc.list_conflicts(primary_provider="twse")
        assert len(results) == 1

    def test_resolve_conflict(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        conflict = self._make_conflict("conf004")
        svc.record_conflict(conflict)
        svc.resolve_conflict("conf004", "PRIMARY_WINS_TWSE_AUTHORITATIVE", "reviewer_a")
        resolved = svc.get_conflict("conf004")
        assert resolved.reviewed is True
        assert "PRIMARY_WINS" in resolved.resolution

    def test_unresolved_only_filter(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        c1 = self._make_conflict("unresolved_1")
        c2 = self._make_conflict("resolved_2")
        svc.record_conflict(c1)
        svc.record_conflict(c2)
        svc.resolve_conflict("resolved_2", "RESOLVED", "reviewer")
        unresolved = svc.list_conflicts(unresolved_only=True)
        assert any(c["conflict_id"] == "unresolved_1" for c in unresolved)
        assert not any(c["conflict_id"] == "resolved_2" for c in unresolved)

    def test_old_record_preserved_on_resolve(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        conflict = self._make_conflict("conf005")
        svc.record_conflict(conflict)
        svc.resolve_conflict("conf005", "RESOLUTION_1", "reviewer_b")
        assert "conf005" in svc._resolutions
        assert svc._resolutions["conf005"]["previous_reviewed"] is False

    def test_get_nonexistent_returns_none(self):
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        assert svc.get_conflict("nonexistent_id") is None


# =====================================================================
# Group 13: Provider Bridges (6 tests)
# =====================================================================

class TestProviderBridges:

    def test_twse_bridge_identity(self):
        from data.governance.bridge_twse_v145 import TWSEGovernanceBridge
        bridge = TWSEGovernanceBridge()
        identity = bridge.get_source_identity()
        assert identity.authority_level == "PRIMARY_OFFICIAL"
        assert identity.provider_id == "twse_official"
        assert identity.official is True
        assert identity.aggregator is False

    def test_tpex_bridge_identity(self):
        from data.governance.bridge_tpex_v145 import TPExGovernanceBridge
        bridge = TPExGovernanceBridge()
        identity = bridge.get_source_identity()
        assert identity.authority_level == "PRIMARY_OFFICIAL"

    def test_mops_bridge_identity(self):
        from data.governance.bridge_mops_v145 import MOPSGovernanceBridge
        bridge = MOPSGovernanceBridge()
        identity = bridge.get_source_identity()
        assert identity.authority_level == "PRIMARY_OFFICIAL"

    def test_data_gov_tw_bridge_identity(self):
        from data.governance.bridge_data_gov_tw_v145 import DataGovTwGovernanceBridge
        bridge = DataGovTwGovernanceBridge()
        identity = bridge.get_source_identity()
        assert identity.authority_level == "PRIMARY_DOMAIN_OFFICIAL"

    def test_finmind_bridge_identity_secondary(self):
        from data.governance.bridge_finmind_v145 import FinMindGovernanceBridge
        bridge = FinMindGovernanceBridge()
        identity = bridge.get_source_identity()
        assert identity.authority_level == "SECONDARY_AGGREGATOR"
        assert identity.aggregator is True

    def test_finmind_cannot_override_primary(self):
        from data.governance.bridge_finmind_v145 import FINMIND_CAN_OVERRIDE_PRIMARY
        assert FINMIND_CAN_OVERRIDE_PRIMARY is False


# =====================================================================
# Group 14: Quality/Freshness/Repair (7 tests)
# =====================================================================

class TestQualityFreshnessRepair:

    def test_source_identity_to_dict_from_dict(self):
        from data.governance.models_v145 import SourceIdentity
        si = SourceIdentity(
            source_id="si_test", provider_id="twse", provider_name="TWSE",
            source_type="official", authority_level="PRIMARY_OFFICIAL",
            official=True, aggregator=False, market="TW", domain="equity",
            agency="TWSE", host="www.twse.com.tw", endpoint_family="daily",
            dataset="daily_ohlcv",
        )
        d = si.to_dict()
        si2 = SourceIdentity.from_dict(d)
        assert si2.source_id == si.source_id
        assert si2.authority_level == si.authority_level

    def test_lineage_record_to_dict_from_dict(self):
        record = _make_lineage("lin_roundtrip")
        d = record.to_dict()
        from data.governance.models_v145 import SourceLineageRecord
        record2 = SourceLineageRecord.from_dict(d)
        assert record2.lineage_id == "lin_roundtrip"
        assert record2.authority_level == "PRIMARY_OFFICIAL"

    def test_fetch_run_audit_to_dict_from_dict(self):
        from data.governance.models_v145 import FetchRunAudit
        fa = FetchRunAudit(
            fetch_run_id="run_test", provider_id="twse",
            requested_by="test", mode="real",
        )
        d = fa.to_dict()
        fa2 = FetchRunAudit.from_dict(d)
        assert fa2.fetch_run_id == "run_test"

    def test_host_rate_limit_policy_to_dict_from_dict(self):
        from data.governance.models_v145 import HostRateLimitPolicy
        p = HostRateLimitPolicy(
            policy_id="test_pol", host="www.test.com", provider_id="test",
            requests_per_minute=30.0, minimum_interval_ms=2000,
        )
        d = p.to_dict()
        p2 = HostRateLimitPolicy.from_dict(d)
        assert p2.policy_id == "test_pol"
        assert p2.minimum_interval_ms == 2000

    def test_provider_budget_to_dict_from_dict(self):
        from data.governance.models_v145 import ProviderRequestBudget
        b = ProviderRequestBudget(provider_id="test_prov", session_limit=25)
        d = b.to_dict()
        b2 = ProviderRequestBudget.from_dict(d)
        assert b2.provider_id == "test_prov"
        assert b2.session_limit == 25

    def test_quota_evidence_to_dict_from_dict(self):
        from data.governance.models_v145 import QuotaEvidence
        ev = QuotaEvidence(
            evidence_id="ev_test", provider_id="finmind",
            host="api.finmindtrade.com", source="TEST",
            captured_at=datetime.now(timezone.utc).isoformat(),
            remaining=50,
        )
        d = ev.to_dict()
        ev2 = QuotaEvidence.from_dict(d)
        assert ev2.evidence_id == "ev_test"
        assert ev2.remaining == 50

    def test_conflict_lineage_to_dict_from_dict(self):
        from data.governance.models_v145 import ConflictLineage
        c = ConflictLineage(
            conflict_id="conf_test",
            primary_lineage_id="lin_a", secondary_lineage_id="lin_b",
            primary_provider="twse", secondary_provider="finmind",
            field_name="close", formal_use_blocked=True,
        )
        d = c.to_dict()
        c2 = ConflictLineage.from_dict(d)
        assert c2.conflict_id == "conf_test"
        assert c2.formal_use_blocked is True


# =====================================================================
# Group 15: CLI (16 tests)
# =====================================================================

class TestCLI:

    def test_source_governance_commands_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        required = [
            "source-governance-health", "source-lineage-sources", "source-lineage-show",
            "source-lineage-trace", "source-lineage-record", "source-lineage-incomplete",
            "request-ledger-list", "request-ledger-show", "fetch-run-list", "fetch-run-show",
            "rate-limit-status", "rate-limit-host", "rate-limit-provider",
            "rate-limit-endpoint", "request-budget-status", "quota-evidence-list",
            "retry-evidence-list", "cache-lineage-show", "conflict-lineage-list",
            "conflict-lineage-show", "source-governance-report",
        ]
        missing = [r for r in required if r not in names]
        assert missing == [], f"Missing commands: {missing}"

    def test_governance_commands_in_source_governance_group(self):
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("source_governance")
        assert len(cmds) == 21

    def test_governance_commands_introduced_in_145(self):
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("source_governance")
        for cmd in cmds:
            assert cmd.introduced_in == "1.4.5"

    def test_no_duplicate_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        assert len(names) == len(set(names))

    def test_source_governance_health_handler_exists(self):
        import main
        assert hasattr(main, "cmd_source_governance_health")

    def test_rate_limit_status_handler_exists(self):
        import main
        assert hasattr(main, "cmd_rate_limit_status")

    def test_request_budget_status_handler_exists(self):
        import main
        assert hasattr(main, "cmd_request_budget_status")

    def test_source_governance_report_handler_exists(self):
        import main
        assert hasattr(main, "cmd_source_governance_report")

    def test_source_lineage_sources_handler_exists(self):
        import main
        assert hasattr(main, "cmd_source_lineage_sources")

    def test_conflict_lineage_list_handler_exists(self):
        import main
        assert hasattr(main, "cmd_conflict_lineage_list")

    def test_cache_lineage_show_handler_exists(self):
        import main
        assert hasattr(main, "cmd_cache_lineage_show")

    def test_quota_evidence_list_handler_exists(self):
        import main
        assert hasattr(main, "cmd_quota_evidence_list")

    def test_retry_evidence_list_handler_exists(self):
        import main
        assert hasattr(main, "cmd_retry_evidence_list")

    def test_fetch_run_list_handler_exists(self):
        import main
        assert hasattr(main, "cmd_fetch_run_list")

    def test_request_ledger_list_handler_exists(self):
        import main
        assert hasattr(main, "cmd_request_ledger_list")

    def test_governance_report_renders(self):
        from reports.source_lineage_rate_limit_report import SourceLineageRateLimitReport
        report = SourceLineageRateLimitReport()
        rendered = report.render()
        assert "Source Lineage & Rate Limit" in rendered
        assert "NO_REAL_ORDERS" in rendered
        assert "source-governance-health" in rendered


# =====================================================================
# Group 16: GUI (11 tests)
# =====================================================================

class TestGUI:

    def test_panel_importable(self):
        from gui.source_governance_panel import SourceGovernancePanel
        assert SourceGovernancePanel is not None

    def test_panel_tab_id(self):
        from gui.source_governance_panel import TAB_ID
        assert TAB_ID == "source_governance"

    def test_panel_group(self):
        from gui.source_governance_panel import GROUP
        assert GROUP == "data"

    def test_panel_priority(self):
        from gui.source_governance_panel import PRIORITY
        assert PRIORITY == "P1"

    def test_safety_banner_present(self):
        from gui.source_governance_panel import SAFETY_BANNER_LINES
        assert len(SAFETY_BANNER_LINES) > 0
        banner_text = " ".join(SAFETY_BANNER_LINES)
        assert "Research Only" in banner_text
        assert "No Real Orders" in banner_text

    def test_no_rate_bypass_in_panel(self):
        from gui.source_governance_panel import RATE_LIMIT_AUTO_BYPASS_ENABLED
        assert RATE_LIMIT_AUTO_BYPASS_ENABLED is False

    def test_no_token_rotation_in_panel(self):
        from gui.source_governance_panel import TOKEN_ROTATION_ENABLED
        assert TOKEN_ROTATION_ENABLED is False

    def test_no_primary_override_in_panel(self):
        from gui.source_governance_panel import PRIMARY_SOURCE_OVERRIDE_ENABLED
        assert PRIMARY_SOURCE_OVERRIDE_ENABLED is False

    def test_panel_safety_info(self):
        from gui.source_governance_panel import SourceGovernancePanel
        info = SourceGovernancePanel.get_safety_info()
        assert info["no_real_orders"] is True
        assert info["broker_disabled"] is True
        assert info["rate_bypass_disabled"] is True

    def test_panel_sections(self):
        from gui.source_governance_panel import SourceGovernancePanel
        sections = SourceGovernancePanel.get_sections()
        assert len(sections) > 0
        assert "rate_limit_manager" in sections

    def test_panel_instantiable(self):
        from gui.source_governance_panel import SourceGovernancePanel
        panel = SourceGovernancePanel(parent=None)
        assert panel is not None


# =====================================================================
# Group 17: Regression (23 tests)
# =====================================================================

class TestRegression:

    def test_safety_no_real_orders(self):
        assert NO_REAL_ORDERS is True

    def test_safety_broker_disabled(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_safety_production_blocked(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_safety_rate_bypass_disabled(self):
        assert RATE_LIMIT_AUTO_BYPASS_ENABLED is False

    def test_safety_no_token_rotation(self):
        import data.governance as pkg
        assert pkg.TOKEN_ROTATION_ENABLED is False

    def test_safety_no_proxy_rotation(self):
        import data.governance as pkg
        assert pkg.PROXY_ROTATION_ENABLED is False

    def test_governance_package_safety_flags(self):
        import data.governance as pkg
        assert pkg.NO_REAL_ORDERS is True
        assert pkg.BROKER_EXECUTION_ENABLED is False
        assert pkg.PRODUCTION_TRADING_BLOCKED is True

    def test_version_145(self):
        from release.version_info import VERSION, RELEASE_NAME
        # v1.4.5 source lineage feature; accept any successor release
        assert VERSION >= "1.4.5", f"Expected v1.4.5 or later, got {VERSION}"
        _KNOWN_NAMES = (
            "Source Lineage & Rate Limit",
            "Provider Quality Gates",
            "Forum Intelligence & Market Sentiment",
            "Data Provider Stable Rollup",
            "Full-Suite Collection Integrity Hotfix",
            "Provider Integration Hardening",
            "Provider Integration Test Integrity Hotfix",
            "Provider Stable Rollup",
            "Portfolio Research Foundation",
            "Portfolio Research Foundation Integrity Hotfix",
            "Portfolio Research CLI Completeness Hotfix",
        )
        assert any(name in RELEASE_NAME for name in _KNOWN_NAMES), (
            f"Unexpected RELEASE_NAME for v1.4.5+ release: {RELEASE_NAME}"
        )

    def test_version_145_flags(self):
        from release.version_info import (
            SOURCE_LINEAGE_AVAILABLE, CENTRAL_RATE_LIMIT_MANAGER_AVAILABLE,
            RATE_LIMIT_AUTO_BYPASS_ENABLED, TOKEN_ROTATION_ENABLED,
        )
        assert SOURCE_LINEAGE_AVAILABLE is True
        assert CENTRAL_RATE_LIMIT_MANAGER_AVAILABLE is True
        assert RATE_LIMIT_AUTO_BYPASS_ENABLED is False
        assert TOKEN_ROTATION_ENABLED is False

    def test_capability_registry_has_lineage(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("provider_lineage_rate_limit") is True

    def test_capability_registry_v145_stable(self):
        from release.capability_registry import get_capabilities
        caps = {c["id"]: c for c in get_capabilities()}
        v145 = caps.get("provider_lineage_rate_limit")
        assert v145 is not None
        assert v145["status"] == "STABLE"
        assert v145["allows_auto_trading"] is False

    def test_health_check_all_pass(self):
        from data.governance.health_v145 import SourceGovernanceHealthCheck
        summary = SourceGovernanceHealthCheck().get_health_summary()
        assert summary["failed"] == 0

    def test_health_check_safety_invariants(self):
        from data.governance.health_v145 import SourceGovernanceHealthCheck
        summary = SourceGovernanceHealthCheck().get_health_summary()
        checks = summary["checks"]
        safety_checks = ["no_rate_bypass", "no_proxy_rotation", "no_token_rotation",
                         "no_primary_override", "no_mock_fallback", "no_broker",
                         "no_order_execution"]
        for key in safety_checks:
            assert checks[key]["status"] == "PASS", f"Safety check {key} failed"

    def test_query_service_governance_report(self):
        from data.governance.query_v145 import SourceGovernanceQueryService
        svc = SourceGovernanceQueryService()
        report = svc.governance_report()
        assert report["no_real_orders"] is True
        assert report["research_only"] is True

    def test_store_in_memory_mode(self):
        from data.governance.store_v145 import SourceGovernanceStore
        store = SourceGovernanceStore()
        store.setup(db_path=None)
        assert store.mode == "memory"
        assert "source_lineage" in store.tables

    def test_store_sqlite_mode(self):
        from data.governance.store_v145 import SourceGovernanceStore
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            store = SourceGovernanceStore()
            store.setup(db_path=db_path)
            assert store.mode == "sqlite"
        finally:
            os.unlink(db_path)

    def test_retry_evidence_backoff_exponential(self):
        from data.governance.retry_evidence_v145 import RetryEvidenceService
        svc = RetryEvidenceService(clock=lambda: 1000.0)
        b1 = svc.calculate_backoff(1, base_seconds=1.0, jitter=False)
        b2 = svc.calculate_backoff(2, base_seconds=1.0, jitter=False)
        b3 = svc.calculate_backoff(3, base_seconds=1.0, jitter=False)
        assert b1 == 1.0
        assert b2 == 2.0
        assert b3 == 4.0

    def test_retry_evidence_parse_retry_after_seconds(self):
        from data.governance.retry_evidence_v145 import RetryEvidenceService
        svc = RetryEvidenceService()
        val = svc.parse_retry_after_header("30")
        assert val == 30.0

    def test_retry_evidence_parse_retry_after_invalid(self):
        from data.governance.retry_evidence_v145 import RetryEvidenceService
        svc = RetryEvidenceService()
        val = svc.parse_retry_after_header("not_a_date_not_a_number")
        assert val == 0.0

    def test_endpoint_policy_allowed_by_default(self):
        from data.governance.endpoint_policy_v145 import EndpointPolicyRegistry
        reg = EndpointPolicyRegistry()
        result = reg.is_allowed("any_provider", "any_family", "any_dataset")
        assert result["allowed"] is True

    def test_endpoint_policy_enforced_when_registered(self):
        from data.governance.endpoint_policy_v145 import EndpointPolicyRegistry
        from data.governance.models_v145 import EndpointRequestPolicy
        reg = EndpointPolicyRegistry()
        policy = EndpointRequestPolicy(
            provider_id="twse", endpoint_family="daily", dataset="daily_ohlcv",
            maximum_symbols=5,
        )
        reg.register_policy(policy)
        result = reg.is_allowed("twse", "daily", "daily_ohlcv", symbol_count=10)
        assert result["allowed"] is False

    def test_fixture_files_have_required_metadata(self):
        fixtures_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "tests", "fixtures", "source_governance",
        )
        if os.path.exists(fixtures_dir):
            for fname in os.listdir(fixtures_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(fixtures_dir, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    assert "_note" in data or "_fixture_type" in data, (
                        f"Fixture {fname} missing _note or _fixture_type"
                    )
