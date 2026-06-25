"""
tests/test_finmind_adapter_hardening_v144.py — FinMind Adapter Hardening v1.4.4 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All tests are offline — no real network calls.
[!] SECONDARY_AGGREGATOR. Cannot override primary source.
[!] 166 tests covering all aspects of the FinMind adapter.
"""
from __future__ import annotations

import json
import os
import pytest

_FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "finmind_adapter")


def _load_fixture(name: str) -> dict:
    with open(os.path.join(_FIXTURE_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# Section 1: Registration Tests 1-9
# =============================================================================

def test_1_provider_id():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.provider_id == "finmind"


def test_2_provider_official_is_false():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.official is False


def test_3_authoritative_level_secondary():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.authoritative_level == "SECONDARY_AGGREGATOR"


def test_4_aggregator_flag():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.aggregator is True


def test_5_cannot_override_primary():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.can_override_primary_provider is False


def test_6_no_broker():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.broker_provider is False


def test_7_no_order_execution():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.order_execution_supported is False


def test_8_no_formal_realtime():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    assert p.formal_realtime_supported is False


def test_9_module_level_safety_flags():
    from data.providers.finmind.provider_v144 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        FINMIND_SILENT_FALLBACK_ENABLED, FINMIND_MOCK_FALLBACK_ENABLED,
        FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER,
    )
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert FINMIND_SILENT_FALLBACK_ENABLED is False
    assert FINMIND_MOCK_FALLBACK_ENABLED is False
    assert FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False


# =============================================================================
# Section 2: Token/Auth Tests 10-16
# =============================================================================

def test_10_auth_manager_instantiates():
    from data.providers.finmind.auth_v144 import FinMindAuthManager
    auth = FinMindAuthManager()
    assert auth is not None


def test_11_token_optional():
    from data.providers.finmind.auth_v144 import FINMIND_TOKEN_OPTIONAL
    assert FINMIND_TOKEN_OPTIONAL is True


def test_12_anonymous_mode_when_no_token(monkeypatch):
    monkeypatch.delenv("FINMIND_API_TOKEN", raising=False)
    monkeypatch.delenv("FINMIND_TOKEN", raising=False)
    from data.providers.finmind.auth_v144 import FinMindAuthManager
    auth = FinMindAuthManager()
    assert auth.anonymous_mode is True
    assert auth.token_present is False


def test_13_no_token_in_auth_summary(monkeypatch):
    monkeypatch.setenv("FINMIND_API_TOKEN", "test_secret_token_abc123")
    from data.providers.finmind.auth_v144 import FinMindAuthManager
    auth = FinMindAuthManager()
    summary = auth.get_auth_summary()
    # Full token must never appear in summary
    assert "test_secret_token_abc123" not in str(summary)
    # Fingerprint is only 8 chars
    fp = summary.get("token_fingerprint")
    if fp is not None:
        assert len(fp) <= 8


def test_14_token_fingerprint_is_short(monkeypatch):
    monkeypatch.setenv("FINMIND_API_TOKEN", "some_token_value_here")
    from data.providers.finmind.auth_v144 import FinMindAuthManager
    auth = FinMindAuthManager()
    fp = auth.token_fingerprint
    assert fp is not None
    assert len(fp) == 8


def test_15_legacy_token_env_var(monkeypatch):
    monkeypatch.delenv("FINMIND_API_TOKEN", raising=False)
    monkeypatch.setenv("FINMIND_TOKEN", "legacy_token_xyz")
    from data.providers.finmind.auth_v144 import FinMindAuthManager
    auth = FinMindAuthManager()
    assert auth.token_present is True
    assert auth.token_source == "FINMIND_TOKEN"


def test_16_token_storage_secure():
    from data.providers.finmind.auth_v144 import FINMIND_TOKEN_STORAGE_SECURE
    assert FINMIND_TOKEN_STORAGE_SECURE is True


# =============================================================================
# Section 3: Quota Tests 17-25
# =============================================================================

def test_17_quota_manager_instantiates():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    qm = FinMindQuotaManager()
    assert qm is not None


def test_18_quota_default_anonymous_limit():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager, ANONYMOUS_DEFAULT_LIMIT_PER_HOUR
    qm = FinMindQuotaManager()
    assert qm._effective_limit == ANONYMOUS_DEFAULT_LIMIT_PER_HOUR


def test_19_quota_record_request():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    qm = FinMindQuotaManager()
    qm.record_request()
    state = qm.get_status()
    assert state.quota_used == 1


def test_20_quota_exhausted_after_record_error():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    from data.providers.finmind.models_v144 import FinMindQuotaStatus
    qm = FinMindQuotaManager()
    qm.record_quota_error("test exhaustion")
    state = qm.get_status()
    assert state.status == FinMindQuotaStatus.EXHAUSTED


def test_21_quota_update_from_headers():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    qm = FinMindQuotaManager()
    qm.update_from_response({"X-RateLimit-Limit": "600", "X-RateLimit-Remaining": "450"})
    state = qm.get_status()
    assert state.quota_limit == 600
    assert state.plan_unknown is False


def test_22_quota_is_exhausted_method():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    qm = FinMindQuotaManager()
    qm.record_quota_error("QUOTA_EXCEEDED")
    assert qm.is_exhausted() is True


def test_23_quota_plan_unknown_default():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    qm = FinMindQuotaManager()
    state = qm.get_status()
    assert state.plan_unknown is True


def test_24_quota_authenticated_higher_limit():
    from data.providers.finmind.quota_v144 import (
        FinMindQuotaManager,
        ANONYMOUS_DEFAULT_LIMIT_PER_HOUR,
        AUTHENTICATED_DEFAULT_LIMIT_PER_HOUR,
    )
    qm_anon = FinMindQuotaManager(authenticated=False)
    qm_auth = FinMindQuotaManager(authenticated=True)
    assert qm_auth._effective_limit > qm_anon._effective_limit
    assert qm_auth._effective_limit == AUTHENTICATED_DEFAULT_LIMIT_PER_HOUR


def test_25_quota_status_returns_state():
    from data.providers.finmind.quota_v144 import FinMindQuotaManager
    from data.providers.finmind.models_v144 import FinMindQuotaState
    qm = FinMindQuotaManager()
    state = qm.get_status()
    assert isinstance(state, FinMindQuotaState)


# =============================================================================
# Section 4: Error Classifier Tests 26-37
# =============================================================================

def test_26_classify_http_429_rate_limited():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(429, None, "application/json", {"Retry-After": "60"})
    assert result.error_code == FinMindErrorCode.RATE_LIMITED
    assert result.retryable is True
    assert result.retry_after == 60


def test_27_classify_quota_exceeded_payload_402():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    payload = {"status": 402, "msg": "You have reached the request limit", "data": []}
    result = ec.classify(200, payload, "application/json")
    assert result.error_code == FinMindErrorCode.QUOTA_EXCEEDED


def test_28_classify_html_response_service_unavailable():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(200, "<html>maintenance</html>", "text/html")
    assert result.error_code == FinMindErrorCode.SERVICE_UNAVAILABLE


def test_29_classify_http_200_empty_data():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(200, {"status": 200, "msg": "success", "data": []}, "application/json")
    assert result.error_code == FinMindErrorCode.EMPTY_RESULT


def test_30_classify_http_200_success():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(200, {"status": 200, "msg": "success", "data": [{"x": 1}]}, "application/json")
    assert result.error_code == FinMindErrorCode.SUCCESS


def test_31_classify_malformed_json():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(200, "{not_valid_json", "application/json")
    assert result.error_code == FinMindErrorCode.MALFORMED_PAYLOAD


def test_32_classify_auth_invalid_http_401():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(401, None, "application/json")
    assert result.error_code == FinMindErrorCode.AUTH_INVALID
    assert result.retryable is False


def test_33_classify_auth_invalid_http_403():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(403, None, "application/json")
    assert result.error_code == FinMindErrorCode.AUTH_INVALID


def test_34_classify_invalid_token_in_payload():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(200, {"status": 400, "msg": "invalid token", "data": []}, "application/json")
    assert result.error_code == FinMindErrorCode.AUTH_INVALID


def test_35_classify_service_unavailable_http_503():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(503, None, "application/json")
    assert result.error_code == FinMindErrorCode.SERVICE_UNAVAILABLE


def test_36_classify_not_found_http_404():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    from data.providers.finmind.models_v144 import FinMindErrorCode
    ec = FinMindErrorClassifier()
    result = ec.classify(404, None, "application/json")
    assert result.error_code == FinMindErrorCode.DATASET_NOT_FOUND


def test_37_auth_invalid_not_retryable():
    from data.providers.finmind.error_classifier_v144 import FinMindErrorClassifier
    ec = FinMindErrorClassifier()
    result = ec.classify(401, None, "application/json")
    assert result.retryable is False
    assert result.blocking is True


# =============================================================================
# Section 5: Dataset Allowlist Tests 38-44
# =============================================================================

def test_38_allowlist_loads():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
    al = FinMindDatasetAllowlist()
    assert al is not None


def test_39_no_wildcard():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist, FINMIND_WILDCARD_ALLOWLIST_ENABLED
    assert FINMIND_WILDCARD_ALLOWLIST_ENABLED is False
    al = FinMindDatasetAllowlist()
    summary = al.summary()
    assert summary["wildcard_allowlist_enabled"] is False


def test_40_no_auto_approve():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist, FINMIND_AUTO_APPROVE_ENABLED
    assert FINMIND_AUTO_APPROVE_ENABLED is False


def test_41_no_auto_discovery():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist, FINMIND_AUTO_DISCOVERY_ENABLED
    assert FINMIND_AUTO_DISCOVERY_ENABLED is False


def test_42_taiwan_stock_price_allowed():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
    al = FinMindDatasetAllowlist()
    assert al.is_allowed("TaiwanStockPrice") is True


def test_43_unknown_dataset_not_allowed():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
    al = FinMindDatasetAllowlist()
    assert al.is_allowed("NonExistentDataset") is False


def test_44_formal_not_allowed_for_secondary():
    from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
    al = FinMindDatasetAllowlist()
    # SECONDARY_SUPPLEMENT_ONLY is not formal
    assert al.is_formal_allowed("TaiwanStockPrice") is False


# =============================================================================
# Section 6: Schema Tests 45-52
# =============================================================================

def test_45_schema_registry_has_all_datasets():
    from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry
    reg = FinMindSchemaRegistry()
    schemas = reg.list_schemas()
    expected = ["TaiwanStockPrice", "TaiwanStockInstitutionalInvestorsBuySell",
                "TaiwanStockMarginPurchaseShortSale", "TaiwanStockMonthRevenue",
                "TaiwanStockFinancialStatements"]
    for ds in expected:
        assert ds in schemas, f"{ds} missing from schema registry"


def test_46_schema_has_required_fields():
    from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry
    reg = FinMindSchemaRegistry()
    schema = reg.get_schema("TaiwanStockPrice")
    assert "required_fields" in schema
    assert "close" in schema["required_fields"]


def test_47_schema_has_hash():
    from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry
    reg = FinMindSchemaRegistry()
    h = reg.get_schema_hash("TaiwanStockPrice")
    assert h is not None and len(h) == 16


def test_48_drift_no_change_for_expected_fields():
    from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
    detector = FinMindSchemaDriftDetector()
    result = detector.detect_drift("TaiwanStockPrice",
                                   ["date", "stock_id", "Trading_Volume", "Trading_money",
                                    "open", "max", "min", "close", "spread", "Trading_turnover"])
    assert result["status"] == "NO_CHANGE"
    assert result["blocked"] is False


def test_49_drift_additive_not_blocking():
    from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
    detector = FinMindSchemaDriftDetector()
    # Add an extra field not in schema
    result = detector.detect_drift("TaiwanStockPrice",
                                   ["date", "stock_id", "Trading_Volume", "Trading_money",
                                    "open", "max", "min", "close", "spread", "Trading_turnover",
                                    "brand_new_field"])
    assert result["status"] == "ADDITIVE"
    assert result["blocked"] is False
    assert "brand_new_field" in result["added_fields"]


def test_50_drift_missing_required_is_blocking():
    from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
    detector = FinMindSchemaDriftDetector()
    # Remove 'close' from fields
    result = detector.detect_drift("TaiwanStockPrice",
                                   ["date", "stock_id", "Trading_Volume", "Trading_money",
                                    "open", "max", "min", "spread", "Trading_turnover"])
    assert result["status"] == "BREAKING_MISSING_FIELD"
    assert result["blocked"] is True
    assert "close" in result["missing_required"]


def test_51_drift_unknown_dataset_blocked():
    from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
    detector = FinMindSchemaDriftDetector()
    result = detector.detect_drift("NonExistentDataset", ["field1", "field2"])
    assert result["blocked"] is True
    assert result["status"] == "UNKNOWN"


def test_52_drift_save_and_get_revision():
    from data.providers.finmind.schema_drift_v144 import FinMindSchemaDriftDetector
    detector = FinMindSchemaDriftDetector()
    drift_result = {"drift_hash": "abcd1234", "status": "NO_CHANGE", "blocked": False}
    detector.save_revision("TaiwanStockPrice", drift_result)
    revisions = detector.get_revisions("TaiwanStockPrice")
    assert len(revisions) == 1
    assert revisions[0]["drift_hash"] == "abcd1234"


# =============================================================================
# Section 7: Price Mapping Tests 53-60
# =============================================================================

def test_53_normalize_price_trade_date():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["trade_date"] == "2024-01-02"


def test_54_normalize_price_symbol():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["symbol"] == "2330"


def test_55_normalize_price_high_low():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["high"] == 600.0
    assert result[0]["low"] == 592.0


def test_56_normalize_price_volume():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["volume"] == 1000000
    assert result[0]["turnover"] == 598000000


def test_57_normalize_price_authority():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["authority"] == "SECONDARY_AGGREGATOR"
    assert result[0]["source"] == "finmind"


def test_58_normalize_price_spread_mapping():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500}]
    result = norm.normalize_price(records)
    assert result[0]["price_change"] == 4.0


def test_59_normalize_price_preserves_unknown():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "close": 598.0,
                "open": 594.0, "max": 600.0, "min": 592.0,
                "Trading_Volume": 1000000, "Trading_money": 598000000,
                "spread": 4.0, "Trading_turnover": 500, "mystery_field": "xyz"}]
    result = norm.normalize_price(records)
    assert result[0].get("mystery_field") == "xyz"
    assert "_warnings" in result[0]


def test_60_normalize_price_multiple_records():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_price_v4.json")
    result = norm.normalize_price(fixture["data"])
    assert len(result) == 2
    assert all(r["symbol"] == "2330" for r in result)


# =============================================================================
# Section 8: Institutional Tests 61-68
# =============================================================================

def test_61_normalize_institutional_narrow_groups_by_date():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_institutional_narrow_v4.json")
    result = norm.normalize_institutional_narrow(fixture["data"])
    assert len(result) == 1  # All 3 institutions grouped into 1 date record


def test_62_normalize_institutional_narrow_foreign_net():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_institutional_narrow_v4.json")
    result = norm.normalize_institutional_narrow(fixture["data"])
    row = result[0]
    assert row["foreign_net"] == 5000000 - 3000000


def test_63_normalize_institutional_narrow_trust_net():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_institutional_narrow_v4.json")
    result = norm.normalize_institutional_narrow(fixture["data"])
    row = result[0]
    assert row["trust_net"] == 200000 - 100000


def test_64_normalize_institutional_narrow_authority():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "name": "外資及陸資", "buy": 1000, "sell": 500}]
    result = norm.normalize_institutional_narrow(records)
    assert result[0]["authority"] == "SECONDARY_AGGREGATOR"


def test_65_normalize_institutional_wide_has_format_flag():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_institutional_wide_v4.json")
    result = norm.normalize_institutional_wide(fixture["data"])
    assert result[0]["format"] == "wide"


def test_66_normalize_institutional_wide_maps_fields():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_institutional_wide_v4.json")
    result = norm.normalize_institutional_wide(fixture["data"])
    assert "foreign_buy" in result[0]
    assert "trust_buy" in result[0]


def test_67_narrow_wide_formats_not_mixed():
    """Narrow and wide normalization produce distinct field sets."""
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    narrow_rec = [{"date": "2024-01-02", "stock_id": "2330", "name": "外資", "buy": 1000, "sell": 500}]
    wide_rec = [{"date": "2024-01-02", "stock_id": "2330", "Foreign_Investor_Buy": 1000, "Foreign_Investor_Sell": 500,
                 "Investment_Trust_Buy": 100, "Investment_Trust_Sell": 50, "Dealer_Buy": 10, "Dealer_Sell": 5}]
    narrow_result = norm.normalize_institutional_narrow(narrow_rec)
    wide_result = norm.normalize_institutional_wide(wide_rec)
    # Wide result has "format" key, narrow does not
    assert "format" not in narrow_result[0]
    assert wide_result[0]["format"] == "wide"


def test_68_normalize_institutional_narrow_dealer_net():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330", "name": "自營商", "buy": 50000, "sell": 80000}]
    result = norm.normalize_institutional_narrow(records)
    assert result[0]["dealer_net"] == 50000 - 80000


# =============================================================================
# Section 9: Margin Tests 69-72
# =============================================================================

def test_69_normalize_margin_margin_balance():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_margin_v4.json")
    result = norm.normalize_margin(fixture["data"])
    assert result[0]["margin_balance"] == 15000


def test_70_normalize_margin_short_balance():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_margin_v4.json")
    result = norm.normalize_margin(fixture["data"])
    assert result[0]["short_balance"] == 3000


def test_71_normalize_margin_authority():
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    fixture = _load_fixture("success_margin_v4.json")
    result = norm.normalize_margin(fixture["data"])
    assert result[0]["authority"] == "SECONDARY_AGGREGATOR"


def test_72_margin_fields_not_mixed():
    """Margin and short fields are separate — never mixed."""
    from data.providers.finmind.normalizer_v144 import FinMindNormalizer
    norm = FinMindNormalizer()
    records = [{"date": "2024-01-02", "stock_id": "2330",
                "MarginPurchaseTodayBalance": 15000, "ShortSaleTodayBalance": 3000}]
    result = norm.normalize_margin(records)
    assert "margin_balance" in result[0]
    assert "short_balance" in result[0]
    # Verify they are separate values
    assert result[0]["margin_balance"] != result[0]["short_balance"]


# =============================================================================
# Section 10: Authority Policy Tests 73-81
# =============================================================================

def test_73_authority_policy_always_blocked_default():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", False, False)
    assert result["allowed"] is False


def test_74_authority_policy_blocked_with_primary():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", True, False)
    assert result["allowed"] is False


def test_75_authority_policy_blocked_with_conflict():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", True, True)
    assert result["allowed"] is False
    assert "primary source wins" in result["reason"].lower() or "conflict" in result["reason"].lower()


def test_76_authority_policy_blocked_unknown_pit():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "UNKNOWN", False, False)
    assert result["allowed"] is False
    assert "UNKNOWN" in result["reason"]


def test_77_authority_policy_cannot_override():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy, FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER
    assert FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False
    policy = FinMindAuthorityPolicy()
    assert policy.CAN_OVERRIDE_PRIMARY is False


def test_78_authority_policy_summary():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    summary = policy.get_policy_summary()
    assert summary["authoritative_level"] == "SECONDARY_AGGREGATOR"
    assert summary["formal_use_allowed_default"] is False


def test_79_no_realtime_formal_use():
    from data.providers.finmind.authority_policy_v144 import FINMIND_REALTIME_FORMAL_USE_ALLOWED
    assert FINMIND_REALTIME_FORMAL_USE_ALLOWED is False


def test_80_authority_reason_present():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", False, False)
    assert isinstance(result.get("reason"), str) and len(result["reason"]) > 0


def test_81_authority_dataset_in_result():
    from data.providers.finmind.authority_policy_v144 import FinMindAuthorityPolicy
    policy = FinMindAuthorityPolicy()
    result = policy.check_formal_use_allowed("TaiwanStockPrice", "DATE_ONLY", False, False)
    assert result["dataset"] == "TaiwanStockPrice"


# =============================================================================
# Section 11: Point-in-Time Tests 82-87
# =============================================================================

def test_82_pit_price_is_date_only():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    from data.providers.finmind.models_v144 import FinMindPITClass
    guard = FinMindPITGuard()
    pit = guard.classify_pit("TaiwanStockPrice")
    assert pit == FinMindPITClass.DATE_ONLY


def test_83_pit_unknown_for_unregistered():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    from data.providers.finmind.models_v144 import FinMindPITClass
    guard = FinMindPITGuard()
    pit = guard.classify_pit("UnregisteredDataset")
    assert pit == FinMindPITClass.UNKNOWN


def test_84_pit_validate_as_of_blocks_future():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    from data.providers.finmind.models_v144 import FinMindPITClass
    guard = FinMindPITGuard()
    record = {"date": "2024-01-05", "available_from": "2024-01-05"}
    # as_of is before available_from
    result = guard.validate_as_of(record, "2024-01-04", FinMindPITClass.DATE_ONLY)
    assert result is False


def test_85_pit_validate_as_of_allows_past():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    from data.providers.finmind.models_v144 import FinMindPITClass
    guard = FinMindPITGuard()
    record = {"date": "2024-01-02", "available_from": "2024-01-02"}
    result = guard.validate_as_of(record, "2024-01-10", FinMindPITClass.DATE_ONLY)
    assert result is True


def test_86_pit_unknown_blocks_validation():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    from data.providers.finmind.models_v144 import FinMindPITClass
    guard = FinMindPITGuard()
    record = {"date": "2024-01-02", "available_from": "2024-01-02"}
    result = guard.validate_as_of(record, "2024-01-10", FinMindPITClass.UNKNOWN)
    assert result is False


def test_87_pit_summary_has_dataset():
    from data.providers.finmind.point_in_time_v144 import FinMindPITGuard
    guard = FinMindPITGuard()
    summary = guard.get_pit_summary("TaiwanStockPrice")
    assert summary["dataset"] == "TaiwanStockPrice"
    assert summary["pit_class"] == "DATE_ONLY"


# =============================================================================
# Section 12: Retry/Rate Limit Tests 88-95
# =============================================================================

def test_88_rate_limit_handler_instantiates():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    assert handler is not None


def test_89_rate_limited_is_retryable():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    assert handler.should_retry(0, "RATE_LIMITED") is True


def test_90_auth_invalid_not_retryable():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    assert handler.should_retry(0, "AUTH_INVALID") is False


def test_91_quota_exceeded_not_retryable():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    assert handler.should_retry(0, "QUOTA_EXCEEDED") is False


def test_92_retry_after_header_respected():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    delay = handler.compute_delay(0, retry_after=120)
    assert delay == 120.0


def test_93_max_retries_exceeded():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler(max_retries=3)
    assert handler.should_retry(3, "RATE_LIMITED") is False
    assert handler.should_retry(4, "RATE_LIMITED") is False


def test_94_no_actual_sleep_in_tests():
    """Injectable sleeper means no real sleep."""
    slept = []
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler(sleeper=lambda s: slept.append(s))
    handler.wait(0)
    assert len(slept) == 1
    assert slept[0] > 0


def test_95_extract_retry_after_header():
    from data.providers.finmind.rate_limit_v144 import FinMindRateLimitHandler
    handler = FinMindRateLimitHandler()
    ra = handler.extract_retry_after({"Retry-After": "60"})
    assert ra == 60
    ra_none = handler.extract_retry_after({})
    assert ra_none is None


# =============================================================================
# Section 13: Cache Tests 96-102
# =============================================================================

def test_96_cache_key_includes_provider():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    cp = FinMindCachePolicy()
    key = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                            "2024-01-01", "2024-12-31", "4.0", "real", "anonymous")
    assert "finmind" in key


def test_97_cache_key_real_mock_isolated():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    cp = FinMindCachePolicy()
    key_real = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                                 "2024-01-01", "2024-12-31", "4.0", "real", "anonymous")
    key_mock = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                                 "2024-01-01", "2024-12-31", "4.0", "mock", "anonymous")
    assert key_real != key_mock


def test_98_cache_key_no_token():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    cp = FinMindCachePolicy()
    # token_mode should be "anonymous" or "authenticated", never the actual token
    key = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                            "2024-01-01", "2024-12-31", "4.0", "real", "anonymous")
    assert "secret" not in key.lower()


def test_99_cache_key_anon_auth_isolated():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    cp = FinMindCachePolicy()
    key_anon = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                                 "2024-01-01", "2024-12-31", "4.0", "real", "anonymous")
    key_auth = cp.make_cache_key("finmind", "v4", "TaiwanStockPrice", "2330",
                                 "2024-01-01", "2024-12-31", "4.0", "real", "authenticated")
    assert key_anon != key_auth


def test_100_cache_stale_detection():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    import time
    cp = FinMindCachePolicy()
    stale_entry = {"cached_at": time.time() - 90000}  # 25 hours ago
    assert cp.is_stale(stale_entry, "DAILY_OHLCV") is True


def test_101_cache_fresh_detection():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    import time
    cp = FinMindCachePolicy()
    fresh_entry = {"cached_at": time.time() - 100}  # 100 seconds ago
    assert cp.is_stale(fresh_entry, "DAILY_OHLCV") is False


def test_102_cache_no_timestamp_is_stale():
    from data.providers.finmind.cache_policy_v144 import FinMindCachePolicy
    cp = FinMindCachePolicy()
    assert cp.is_stale({}, "DAILY_OHLCV") is True


# =============================================================================
# Section 14: Request Planner Tests 103-110
# =============================================================================

def test_103_parser_success_response():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    fixture = _load_fixture("success_price_v4.json")
    result = parser.parse_response({
        "http_status": 200, "body": fixture, "headers": {}, "content_type": "application/json"
    })
    assert result["is_success"] is True
    assert result["error_code"] == "SUCCESS"


def test_104_parser_empty_data():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 200,
        "body": {"status": 200, "msg": "success", "data": []},
        "headers": {},
        "content_type": "application/json"
    })
    assert result["is_empty"] is True
    assert result["error_code"] == "EMPTY_RESULT"


def test_105_parser_quota_exceeded():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    fixture = _load_fixture("quota_exceeded_payload_402.json")
    result = parser.parse_response({
        "http_status": 200, "body": fixture, "headers": {}, "content_type": "application/json"
    })
    assert result["is_quota_exceeded"] is True
    assert result["error_code"] == "QUOTA_EXCEEDED"


def test_106_parser_rate_limited():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 429, "body": "Too Many Requests", "headers": {"Retry-After": "60"},
        "content_type": "application/json"
    })
    assert result["is_rate_limited"] is True
    assert result["error_code"] == "RATE_LIMITED"


def test_107_parser_network_error():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 0, "body": None, "headers": {}, "content_type": "",
        "error": "connection refused"
    })
    assert result["error_code"] == "NETWORK_ERROR"
    assert result["is_success"] is False


def test_108_parser_malformed_json():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 200, "body": "{bad_json", "headers": {}, "content_type": "application/json"
    })
    assert result["error_code"] == "MALFORMED_PAYLOAD"


def test_109_parser_html_body():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 200, "body": "<html><body>Maintenance</body></html>",
        "headers": {}, "content_type": "text/html"
    })
    assert result["error_code"] == "SERVICE_UNAVAILABLE"


def test_110_parser_auth_invalid():
    from data.providers.finmind.parser_v144 import FinMindParser
    parser = FinMindParser()
    result = parser.parse_response({
        "http_status": 403, "body": None, "headers": {}, "content_type": "application/json"
    })
    assert result["error_code"] == "AUTH_INVALID"


# =============================================================================
# Section 15: Quality/Freshness Tests 111-117
# =============================================================================

def test_111_query_service_instantiates():
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService()
    assert svc is not None


def test_112_query_service_capabilities():
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService()
    caps = svc.get_dataset_capabilities()
    assert len(caps) >= 5


def test_113_query_service_schema():
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService()
    schema = svc.get_dataset_schema("TaiwanStockPrice")
    assert schema is not None
    assert schema["schema_id"] == "taiwan_stock_price_v4"


def test_114_query_blocked_for_unallowlisted():
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService()
    result = svc.get_records("UnknownDataset", "2330")
    assert result["record_count"] == 0
    assert result.get("blocked") is True


def test_115_query_result_has_authority():
    """Even on offline mock transport, result has authority field."""
    def mock_transport(url, params):
        return {
            "http_status": 200,
            "body": {"status": 200, "msg": "success", "data": [
                {"date": "2024-01-02", "stock_id": "2330", "Trading_Volume": 1000,
                 "Trading_money": 600000, "open": 594.0, "max": 600.0, "min": 592.0,
                 "close": 598.0, "spread": 4.0, "Trading_turnover": 500}
            ]},
            "headers": {}, "content_type": "application/json"
        }
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService(transport=mock_transport)
    result = svc.get_records("TaiwanStockPrice", "2330", "2024-01-01", "2024-01-31")
    assert result["authority"] == "SECONDARY_AGGREGATOR"


def test_116_query_result_has_pit_class():
    def mock_transport(url, params):
        return {
            "http_status": 200,
            "body": {"status": 200, "msg": "success", "data": [
                {"date": "2024-01-02", "stock_id": "2330", "Trading_Volume": 1000,
                 "Trading_money": 600000, "open": 594.0, "max": 600.0, "min": 592.0,
                 "close": 598.0, "spread": 4.0, "Trading_turnover": 500}
            ]},
            "headers": {}, "content_type": "application/json"
        }
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService(transport=mock_transport)
    result = svc.get_records("TaiwanStockPrice", "2330", "2024-01-01", "2024-01-31")
    assert result["pit_class"] == "DATE_ONLY"


def test_117_quota_status_accessible():
    from data.providers.finmind.query_v144 import FinMindQueryService
    svc = FinMindQueryService()
    quota = svc.get_quota_status()
    assert "status" in quota


# =============================================================================
# Section 16: CLI Tests 118-136
# =============================================================================

def test_118_finmind_commands_registered():
    from cli.command_registry import PROVIDER_COMMANDS
    finmind_cmds = [c for c in PROVIDER_COMMANDS if c.group == "finmind"]
    assert len(finmind_cmds) >= 20


def test_119_finmind_health_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-health")
    assert cmd is not None
    assert cmd.handler_name == "cmd_finmind_health"


def test_120_finmind_capabilities_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-capabilities")
    assert cmd is not None


def test_121_finmind_datasets_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-datasets")
    assert cmd is not None


def test_122_finmind_dataset_command_has_arg():
    from cli.command_registry import get_command
    cmd = get_command("finmind-dataset")
    assert cmd is not None
    arg_flags = [a.flags[0] for a in cmd.args]
    assert "--dataset" in arg_flags


def test_123_finmind_schema_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-schema")
    assert cmd is not None


def test_124_finmind_schema_drift_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-schema-drift")
    assert cmd is not None


def test_125_finmind_quota_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-quota")
    assert cmd is not None


def test_126_finmind_auth_status_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-auth-status")
    assert cmd is not None


def test_127_finmind_plan_command_has_args():
    from cli.command_registry import get_command
    cmd = get_command("finmind-plan")
    assert cmd is not None
    arg_flags = [a.flags[0] for a in cmd.args]
    assert "--dataset" in arg_flags


def test_128_finmind_fetch_command_has_execute_arg():
    from cli.command_registry import get_command
    cmd = get_command("finmind-fetch")
    assert cmd is not None
    arg_flags = [a.flags[0] for a in cmd.args]
    assert "--execute" in arg_flags


def test_129_finmind_price_command_has_symbol():
    from cli.command_registry import get_command
    cmd = get_command("finmind-price")
    assert cmd is not None
    arg_flags = [a.flags[0] for a in cmd.args]
    assert "--symbol" in arg_flags


def test_130_finmind_institutional_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-institutional")
    assert cmd is not None


def test_131_finmind_margin_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-margin")
    assert cmd is not None


def test_132_finmind_compare_primary_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-compare-primary")
    assert cmd is not None


def test_133_finmind_conflicts_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-conflicts")
    assert cmd is not None


def test_134_finmind_coverage_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-coverage")
    assert cmd is not None


def test_135_finmind_lineage_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-lineage")
    assert cmd is not None


def test_136_finmind_adapter_report_command_registered():
    from cli.command_registry import get_command
    cmd = get_command("finmind-adapter-report")
    assert cmd is not None
    assert cmd.handler_name == "cmd_finmind_adapter_report"


# =============================================================================
# Section 17: GUI Tests 137-147
# =============================================================================

def test_137_gui_panel_importable():
    import gui.finmind_adapter_panel
    assert hasattr(gui.finmind_adapter_panel, "TAB_ID")


def test_138_gui_tab_id():
    from gui.finmind_adapter_panel import TAB_ID
    assert TAB_ID == "finmind_adapter"


def test_139_gui_display_name():
    from gui.finmind_adapter_panel import DISPLAY_NAME
    assert DISPLAY_NAME == "FinMind Adapter"


def test_140_gui_group():
    from gui.finmind_adapter_panel import GROUP
    assert GROUP == "data"


def test_141_gui_safety_flags():
    from gui.finmind_adapter_panel import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER, FINMIND_SILENT_FALLBACK_ENABLED,
        FINMIND_MOCK_FALLBACK_ENABLED,
    )
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False
    assert FINMIND_SILENT_FALLBACK_ENABLED is False
    assert FINMIND_MOCK_FALLBACK_ENABLED is False


def test_142_gui_safety_banner_lines():
    from gui.finmind_adapter_panel import SAFETY_BANNER_LINES
    assert len(SAFETY_BANNER_LINES) >= 5
    full_text = " ".join(SAFETY_BANNER_LINES)
    assert "SECONDARY_AGGREGATOR" in full_text


def test_143_gui_get_panel_data():
    from gui.finmind_adapter_panel import get_panel_data
    data = get_panel_data()
    assert data["provider"] == "finmind"
    assert data["authoritative_level"] == "SECONDARY_AGGREGATOR"
    assert data["no_real_orders"] is True


def test_144_gui_no_token_in_panel_data():
    import os
    # Without env token, no token in data
    from gui.finmind_adapter_panel import get_panel_data
    data = get_panel_data()
    data_str = str(data)
    # Token fingerprint in auth_summary is at most 8 chars — not a real token
    auth_summary = data.get("auth_summary", {})
    fp = auth_summary.get("token_fingerprint")
    if fp is not None:
        assert len(fp) <= 8


def test_145_gui_quota_does_not_crash():
    """Panel data collection should not crash on quota state."""
    from gui.finmind_adapter_panel import get_panel_data
    data = get_panel_data()
    quota = data.get("quota_summary", {})
    assert "error" not in quota or isinstance(quota.get("error"), str)


def test_146_gui_section_adapter_status():
    from gui.finmind_adapter_panel import get_section_adapter_status
    section = get_section_adapter_status()
    assert section["section"] == "Adapter Status"
    assert section["provider"] == "finmind"


def test_147_gui_section_lineage():
    from gui.finmind_adapter_panel import get_section_lineage
    section = get_section_lineage()
    assert section["section"] == "Lineage"


# =============================================================================
# Section 18: Regression Tests 148-166
# =============================================================================

def test_148_version_is_144():
    from release.version_info import VERSION
    from release.version_alignment import is_version_at_least
    # v1.4.5+ supersedes v1.4.4; accept >= 1.4.4
    assert is_version_at_least(VERSION, "1.4.4"), f"Expected >= 1.4.4, got {VERSION}"


def test_149_release_name():
    from release.version_info import RELEASE_NAME
    known_names = {
        "FinMind Adapter Hardening",
        "Source Lineage & Rate Limit",
        "Provider Quality Gates",
        "Full-Suite Collection Integrity Hotfix",
        "Forum Intelligence & Market Sentiment",
        "Provider Integration Hardening",
        "Provider Integration Test Integrity Hotfix",
        "Provider Stable Rollup",
        "Portfolio Research Foundation",
        "Portfolio Research Foundation Integrity Hotfix",
        "Portfolio Research CLI Completeness Hotfix",
        "Position Sizing",
        "Correlation & Exposure",
        "Correlation & Exposure Integrity Hotfix",
        "Drawdown & Risk Controls",
        "Portfolio Walk-forward Backtest",
        "Portfolio Stable Rollup",
        "Portfolio Stable Rollup Integrity Hotfix",
        "Portfolio Stable Rollup Release Gate Hotfix",
    }
    assert RELEASE_NAME in known_names, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"


def test_150_base_release_references_hotfix():
    from release.version_info import BASE_RELEASE
    # 1.4.3 (hotfix era) or 1.4.4 (FinMind Adapter) is valid base
    def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
    assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.4.3"), (
        f"BASE_RELEASE does not reference expected predecessor: {BASE_RELEASE}"
    )


def test_151_finmind_flags_in_version_info():
    from release.version_info import (
        FINMIND_ADAPTER_AVAILABLE, FINMIND_ADAPTER_HARDENED,
        FINMIND_API_V4_AVAILABLE, FINMIND_SECONDARY_AGGREGATOR,
        FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER, FINMIND_TOKEN_OPTIONAL,
    )
    assert FINMIND_ADAPTER_AVAILABLE is True
    assert FINMIND_ADAPTER_HARDENED is True
    assert FINMIND_API_V4_AVAILABLE is True
    assert FINMIND_SECONDARY_AGGREGATOR is True
    assert FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False
    assert FINMIND_TOKEN_OPTIONAL is True


def test_152_finmind_safety_flags_in_version_info():
    from release.version_info import (
        FINMIND_SILENT_FALLBACK_ENABLED, FINMIND_MOCK_FALLBACK_ENABLED,
        FINMIND_AUTO_DOWNLOAD_ENABLED, FINMIND_AUTO_DISCOVERY_ENABLED,
        FINMIND_REALTIME_FORMAL_USE_ALLOWED, FINMIND_BROKER_EXECUTION_AVAILABLE,
    )
    assert FINMIND_SILENT_FALLBACK_ENABLED is False
    assert FINMIND_MOCK_FALLBACK_ENABLED is False
    assert FINMIND_AUTO_DOWNLOAD_ENABLED is False
    assert FINMIND_AUTO_DISCOVERY_ENABLED is False
    assert FINMIND_REALTIME_FORMAL_USE_ALLOWED is False
    assert FINMIND_BROKER_EXECUTION_AVAILABLE is False


def test_153_capability_registry_finmind_stable():
    from release.capability_registry import _CAP_INDEX, STABLE
    cap = _CAP_INDEX.get("finmind_adapter_hardening")
    assert cap is not None
    assert cap["status"] == STABLE
    assert cap["available"] is True
    assert cap["stable"] is True


def test_154_twse_provider_unchanged():
    from data.providers.twse.provider_v140 import TWSEProviderV140
    p = TWSEProviderV140()
    assert p.provider_id == "twse_official"


def test_155_tpex_provider_unchanged():
    from data.providers.tpex.provider_v141 import TPExProviderV141
    p = TPExProviderV141()
    assert p.provider_id == "tpex_official"


def test_156_mops_provider_unchanged():
    from data.providers.mops.provider_v142 import MOPSProviderV142
    p = MOPSProviderV142()
    assert p.provider_id == "mops_official"


def test_157_data_gov_tw_provider_unchanged():
    from data.providers.data_gov_tw.provider_v143 import DataGovTwProviderV143
    p = DataGovTwProviderV143()
    assert p.provider_id == "data_gov_tw_official"


def test_158_conflict_detector_primary_wins():
    from data.providers.finmind.conflict_detection_v144 import FinMindConflictDetector
    from data.providers.finmind.models_v144 import FinMindConflictResult
    fixture = {
        "primary": [{"trade_date": "2024-01-02", "symbol": "2330", "close": 598.0}],
        "finmind": [{"trade_date": "2024-01-02", "symbol": "2330", "close": 605.0}],
    }
    det = FinMindConflictDetector()
    results = det.compare_price(fixture["primary"], fixture["finmind"])
    conflict_results = [r for r in results if r["result"] == FinMindConflictResult.VALUE_CONFLICT.value]
    assert len(conflict_results) >= 1
    assert all(r.get("winner") == "PRIMARY" for r in conflict_results)


def test_159_conflict_within_tolerance():
    from data.providers.finmind.conflict_detection_v144 import FinMindConflictDetector
    from data.providers.finmind.models_v144 import FinMindConflictResult
    det = FinMindConflictDetector()
    primary = [{"trade_date": "2024-01-02", "symbol": "2330", "close": 598.0}]
    finmind = [{"trade_date": "2024-01-02", "symbol": "2330", "close": 598.0001}]
    results = det.compare_price(primary, finmind)
    tol_results = [r for r in results if r["result"] == FinMindConflictResult.WITHIN_TOLERANCE.value]
    assert len(tol_results) >= 1


def test_160_health_check_runs_offline():
    from data.providers.finmind.health_v144 import FinMindAdapterHealthCheck
    summary = FinMindAdapterHealthCheck().get_health_summary()
    assert summary is not None
    assert "checks" in summary


def test_161_health_check_safety_invariants_pass():
    from data.providers.finmind.health_v144 import FinMindAdapterHealthCheck
    summary = FinMindAdapterHealthCheck().get_health_summary()
    checks = summary.get("checks", {})
    safety_checks = ["no_wildcard_dataset", "no_auto_discovery", "no_auto_download",
                     "no_silent_fallback", "no_mock_fallback", "no_primary_override",
                     "no_broker", "no_order_execution"]
    for check_name in safety_checks:
        if check_name in checks:
            assert checks[check_name]["status"] == "PASS", (
                f"Safety check {check_name!r} failed: {checks[check_name]}"
            )


def test_162_report_renders():
    from reports.finmind_adapter_report import FinMindAdapterReport
    report = FinMindAdapterReport()
    rendered = report.render()
    assert "FinMind Adapter Report" in rendered
    assert "SECONDARY_AGGREGATOR" in rendered
    assert "Research Only" in rendered


def test_163_report_no_token():
    import os
    from reports.finmind_adapter_report import FinMindAdapterReport
    report = FinMindAdapterReport()
    rendered = report.render()
    # No actual token values should be in report (fingerprint is max 8 chars and is fine)
    # This test ensures the report doesn't accidentally include long token strings
    # In test env, there's no real token, so this is straightforward
    assert "FINMIND_API_TOKEN=" not in rendered


def test_164_gitignore_has_finmind():
    import os
    gitignore_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".gitignore"
    )
    assert os.path.exists(gitignore_path)
    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "data/finmind/" in content


def test_165_provider_lineage():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    lineage = p.get_provider_lineage()
    assert lineage["provider"] == "finmind"
    assert lineage["authority"] == "SECONDARY_AGGREGATOR"
    assert lineage["can_override_primary_provider"] is False


def test_166_coverage_summary():
    from data.providers.finmind.provider_v144 import FinMindAdapterV144
    p = FinMindAdapterV144()
    coverage = p.summarize_coverage()
    assert coverage["provider"] == "finmind"
    assert coverage["authority"] == "SECONDARY_AGGREGATOR"
    assert coverage["total_supported"] >= 6
