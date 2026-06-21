"""
data/providers/forum/health_v147.py — ForumIntelligenceHealthCheck v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] 60+ offline checks. SUPPLEMENTARY authority. No live HTTP.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ForumIntelligenceHealthCheck:
    """
    60+ offline health checks for Forum Intelligence v1.4.7.
    [!] All checks are offline (no HTTP). Research Only.
    """

    VERSION = "1.4.7"

    def run_all(self) -> List[Dict]:
        checks = []
        # Safety invariant checks (12)
        checks += self._safety_checks()
        # Package import checks (12)
        checks += self._import_checks()
        # Store/DB checks (10)
        checks += self._store_checks()
        # Parser checks (8)
        checks += self._parser_checks()
        # PIT checks (6)
        checks += self._pit_checks()
        # Aggregation checks (6)
        checks += self._aggregation_checks()
        # Privacy checks (6)
        checks += self._privacy_checks()
        return checks

    def get_health_summary(self) -> Dict[str, Any]:
        checks = self.run_all()
        total = len(checks)
        passed = sum(1 for c in checks if c["status"] == "PASS")
        failed = sum(1 for c in checks if c["status"] == "FAIL")
        warned = sum(1 for c in checks if c["status"] == "WARN")
        checks_dict = {c["name"]: {"status": c["status"], "detail": c.get("detail", "")}
                       for c in checks}
        return {
            "version": self.VERSION,
            "total": total,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "checks": checks_dict,
        }

    # ------------------------------------------------------------------
    # Safety checks (12)
    # ------------------------------------------------------------------
    def _safety_checks(self) -> List[Dict]:
        results = []

        def _chk(name, ok, detail):
            return {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}

        try:
            from data.providers.forum import (
                FORUM_CAN_GENERATE_BUY_SELL,
                FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE,
                FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED,
                FORUM_PRIVATE_BOARD_ACCESS_ENABLED,
                FORUM_LOGIN_BYPASS_ENABLED,
                FORUM_CAPTCHA_BYPASS_ENABLED,
                FORUM_PROXY_ROTATION_ENABLED,
                FORUM_AUTO_POSTING_ENABLED,
                FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED,
                NO_REAL_ORDERS,
                BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
            )
            results.append(_chk(
                "safety_no_buy_sell",
                FORUM_CAN_GENERATE_BUY_SELL is False,
                f"FORUM_CAN_GENERATE_BUY_SELL={FORUM_CAN_GENERATE_BUY_SELL}"
            ))
            results.append(_chk(
                "safety_no_override_official",
                FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE is False,
                f"FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE={FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE}"
            ))
            results.append(_chk(
                "safety_no_standalone_conclusion",
                FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED is False,
                f"FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED={FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED}"
            ))
            results.append(_chk(
                "safety_no_private_board",
                FORUM_PRIVATE_BOARD_ACCESS_ENABLED is False,
                f"FORUM_PRIVATE_BOARD_ACCESS_ENABLED={FORUM_PRIVATE_BOARD_ACCESS_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_login_bypass",
                FORUM_LOGIN_BYPASS_ENABLED is False,
                f"FORUM_LOGIN_BYPASS_ENABLED={FORUM_LOGIN_BYPASS_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_captcha_bypass",
                FORUM_CAPTCHA_BYPASS_ENABLED is False,
                f"FORUM_CAPTCHA_BYPASS_ENABLED={FORUM_CAPTCHA_BYPASS_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_proxy_rotation",
                FORUM_PROXY_ROTATION_ENABLED is False,
                f"FORUM_PROXY_ROTATION_ENABLED={FORUM_PROXY_ROTATION_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_auto_posting",
                FORUM_AUTO_POSTING_ENABLED is False,
                f"FORUM_AUTO_POSTING_ENABLED={FORUM_AUTO_POSTING_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_identity_inference",
                FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED is False,
                f"FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED={FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED}"
            ))
            results.append(_chk(
                "safety_no_real_orders",
                NO_REAL_ORDERS is True,
                f"NO_REAL_ORDERS={NO_REAL_ORDERS}"
            ))
            results.append(_chk(
                "safety_broker_disabled",
                BROKER_EXECUTION_ENABLED is False,
                f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}"
            ))
            results.append(_chk(
                "safety_production_blocked",
                PRODUCTION_TRADING_BLOCKED is True,
                f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}"
            ))
        except Exception as exc:
            results.append({"name": "safety_import", "status": "FAIL", "detail": str(exc)})
        return results

    # ------------------------------------------------------------------
    # Import checks (12)
    # ------------------------------------------------------------------
    def _import_checks(self) -> List[Dict]:
        results = []
        modules = [
            "data.providers.forum.models_v147",
            "data.providers.forum.source_registry_v147",
            "data.providers.forum.store_v147",
            "data.providers.forum.query_v147",
            "data.providers.forum.point_in_time_v147",
            "data.providers.forum.aggregation_v147",
            "data.providers.forum.feature_export_v147",
            "data.providers.forum.dedup_v147",
            "data.providers.forum.sentiment_v147",
            "data.providers.forum.topic_v147",
            "data.providers.forum.coordination_risk_v147",
            "data.providers.forum.manipulation_risk_v147",
        ]
        for mod in modules:
            try:
                __import__(mod)
                results.append({"name": f"import_{mod.split('.')[-1]}", "status": "PASS", "detail": "ok"})
            except Exception as exc:
                results.append({"name": f"import_{mod.split('.')[-1]}", "status": "FAIL", "detail": str(exc)})
        return results

    # ------------------------------------------------------------------
    # Store checks (10)
    # ------------------------------------------------------------------
    def _store_checks(self) -> List[Dict]:
        results = []
        try:
            import tempfile
            import os
            from data.providers.forum.store_v147 import ForumStore
            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
                tmp_path = f.name
            store = ForumStore(db_path=tmp_path)
            hc = store.health_check()

            results.append({"name": "store_init", "status": "PASS", "detail": "SQLite store init ok"})
            results.append({
                "name": "store_table_count",
                "status": "PASS" if hc["table_count"] >= 15 else "FAIL",
                "detail": f"tables={hc['table_count']}, expected>=15"
            })
            results.append({
                "name": "store_no_full_ip",
                "status": "PASS" if hc["full_ip_stored"] is False else "FAIL",
                "detail": f"full_ip_stored={hc['full_ip_stored']}"
            })
            results.append({
                "name": "store_no_formal_standalone",
                "status": "PASS" if hc["formal_standalone_allowed"] is False else "FAIL",
                "detail": f"formal_standalone_allowed={hc['formal_standalone_allowed']}"
            })
            # Idempotent migration test
            store2 = ForumStore(db_path=tmp_path)
            hc2 = store2.health_check()
            results.append({
                "name": "store_idempotent_migration",
                "status": "PASS" if hc2["table_count"] >= 15 else "FAIL",
                "detail": f"second init table_count={hc2['table_count']}"
            })
            # Source upsert
            store.upsert_source({
                "source_id": "test_src", "display_name": "Test", "base_url": "http://test.example",
                "board_id": "Test", "authority_level": "SUPPLEMENTARY", "is_public": 1, "is_private": 0,
                "allowlisted": 1, "max_pages": 5, "max_articles": 50, "rate_limit_sec": 1.0,
                "notes": "", "registered_at": "2024-01-01T00:00:00Z"
            })
            src = store.get_source("test_src")
            results.append({
                "name": "store_upsert_source",
                "status": "PASS" if src is not None else "FAIL",
                "detail": f"source retrieved: {src is not None}"
            })
            # Article upsert
            store.upsert_article({
                "article_id": "art1", "source_id": "test_src",
                "canonical_url": "http://test.example/art1", "board_id": "Test",
                "category": "Test", "title": "Test Article", "author_display_id": "user_abc",
                "published_at": "2024-01-01T12:00:00Z", "published_at_precision": "MINUTE",
                "first_seen_at": "2024-01-01T12:01:00Z", "last_seen_at": "2024-01-01T12:01:00Z",
                "body_hash": "abc123", "body_length": 100, "duplicate_status": "UNIQUE",
                "is_deleted": 0, "deletion_type": None, "formal_standalone": 0,
            })
            art = store.get_article("art1")
            results.append({
                "name": "store_upsert_article",
                "status": "PASS" if art is not None else "FAIL",
                "detail": f"article retrieved: {art is not None}"
            })
            # Append-only version
            store.append_article_version({
                "article_id": "art1", "version_seq": 1, "captured_at": "2024-01-01T12:01:00Z",
                "body_hash": "abc123", "title": "Test Article", "change_type": "INITIAL"
            })
            versions = store.get_article_versions("art1")
            results.append({
                "name": "store_article_version",
                "status": "PASS" if len(versions) == 1 else "FAIL",
                "detail": f"versions={len(versions)}"
            })
            # Fetch run
            run_id = store.start_fetch_run("test_src", dry_run=True)
            store.complete_fetch_run(run_id, 5, 1, "COMPLETE")
            runs = store.list_fetch_runs("test_src")
            results.append({
                "name": "store_fetch_run",
                "status": "PASS" if len(runs) == 1 else "FAIL",
                "detail": f"fetch_runs={len(runs)}"
            })
            os.unlink(tmp_path)
        except Exception as exc:
            results.append({"name": "store_checks", "status": "FAIL", "detail": str(exc)})
        return results

    # ------------------------------------------------------------------
    # Parser checks (8)
    # ------------------------------------------------------------------
    def _parser_checks(self) -> List[Dict]:
        results = []
        parser_modules = [
            ("data.providers.forum.ptt.list_parser_v147", "PTTListParser"),
            ("data.providers.forum.ptt.article_parser_v147", "PTTArticleParser"),
            ("data.providers.forum.ptt.push_parser_v147", "PTTPushParser"),
            ("data.providers.forum.ptt.edit_history_v147", "PTTEditHistoryParser"),
            ("data.providers.forum.ptt.deletion_v147", "PTTDeletionTracker"),
            ("data.providers.forum.ptt.pagination_v147", "PTTPagination"),
            ("data.providers.forum.ptt.cache_policy_v147", "PTTCachePolicy"),
            ("data.providers.forum.ptt.bridge_v147", "PTTGovernanceBridge"),
        ]
        for mod_name, cls_name in parser_modules:
            try:
                mod = __import__(mod_name, fromlist=[cls_name])
                cls = getattr(mod, cls_name, None)
                results.append({
                    "name": f"parser_{cls_name}",
                    "status": "PASS" if cls is not None else "FAIL",
                    "detail": f"{cls_name} importable"
                })
            except Exception as exc:
                results.append({
                    "name": f"parser_{cls_name}",
                    "status": "FAIL",
                    "detail": str(exc)
                })
        return results

    # ------------------------------------------------------------------
    # PIT checks (6)
    # ------------------------------------------------------------------
    def _pit_checks(self) -> List[Dict]:
        results = []
        try:
            import tempfile, os
            from data.providers.forum.store_v147 import ForumStore
            from data.providers.forum.point_in_time_v147 import ForumPointInTimeService
            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
                tmp = f.name
            store = ForumStore(db_path=tmp)
            pit = ForumPointInTimeService(store=store)
            store.upsert_source({
                "source_id": "pit_src", "display_name": "PIT Test", "base_url": "http://test.example",
                "board_id": "Test", "authority_level": "SUPPLEMENTARY", "is_public": 1, "is_private": 0,
                "allowlisted": 1, "max_pages": 5, "max_articles": 50, "rate_limit_sec": 1.0,
                "notes": "", "registered_at": "2024-01-01T00:00:00Z"
            })
            store.upsert_article({
                "article_id": "pit1", "source_id": "pit_src",
                "canonical_url": "http://test.example/pit1", "board_id": "Test",
                "category": "Test", "title": "PIT Test", "author_display_id": "u1",
                "published_at": "2024-01-02T10:00:00Z", "published_at_precision": "MINUTE",
                "first_seen_at": "2024-01-02T10:01:00Z", "last_seen_at": "2024-01-02T10:01:00Z",
                "body_hash": "h1", "body_length": 50, "duplicate_status": "UNIQUE",
                "is_deleted": 0, "deletion_type": None, "formal_standalone": 0,
            })
            # Visible at as_of after first_seen
            r1 = pit.get_article_as_of("pit1", "2024-01-02T11:00:00Z")
            results.append({
                "name": "pit_visible_after_first_seen",
                "status": "PASS" if r1 is not None else "FAIL",
                "detail": f"article visible after first_seen: {r1 is not None}"
            })
            # Not visible before first_seen
            r2 = pit.get_article_as_of("pit1", "2024-01-01T00:00:00Z")
            results.append({
                "name": "pit_not_visible_before_first_seen",
                "status": "PASS" if r2 is None else "FAIL",
                "detail": f"article not visible before first_seen: {r2 is None}"
            })
            # Future comment blocked
            store.insert_comment({
                "article_id": "pit1", "sequence": 1, "author_display_id": "u2",
                "tag": "PUSH", "text": "future comment",
                "comment_time": "2024-01-10T10:00:00Z", "time_precision": "MINUTE",
                "first_seen_at": "2024-01-10T10:01:00Z"
            })
            comments_as_of = pit.get_comments_as_of("pit1", "2024-01-05T00:00:00Z")
            results.append({
                "name": "pit_future_comment_blocked",
                "status": "PASS" if len(comments_as_of) == 0 else "FAIL",
                "detail": f"future comments blocked: {len(comments_as_of) == 0}"
            })
            # Deletion state
            del_state = pit.get_deletion_state_as_of("pit1", "2024-01-03T00:00:00Z")
            results.append({
                "name": "pit_deletion_state",
                "status": "PASS" if del_state["deleted"] is False else "FAIL",
                "detail": f"not deleted before deletion event: {del_state['deleted'] is False}"
            })
            # Leakage check
            leak = pit.check_future_leakage("pit1", "2024-01-01T00:00:00Z")
            results.append({
                "name": "pit_future_leakage_detected",
                "status": "PASS" if leak["leakage"] is True else "FAIL",
                "detail": f"future leakage detected for past as_of: {leak['leakage']}"
            })
            # Explain availability
            exp = pit.explain_forum_availability("2024-01-03T00:00:00Z")
            results.append({
                "name": "pit_explain_availability",
                "status": "PASS" if isinstance(exp, dict) else "FAIL",
                "detail": f"explain_forum_availability returns dict"
            })
            os.unlink(tmp)
        except Exception as exc:
            results.append({"name": "pit_checks", "status": "FAIL", "detail": str(exc)})
        return results

    # ------------------------------------------------------------------
    # Aggregation checks (6)
    # ------------------------------------------------------------------
    def _aggregation_checks(self) -> List[Dict]:
        results = []
        try:
            import tempfile, os
            from data.providers.forum.store_v147 import ForumStore
            from data.providers.forum.aggregation_v147 import MarketSentimentAggregator, SUPPORTED_WINDOWS
            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
                tmp = f.name
            store = ForumStore(db_path=tmp)
            agg = MarketSentimentAggregator(store=store)
            # Supported windows
            results.append({
                "name": "agg_supported_windows",
                "status": "PASS" if len(SUPPORTED_WINDOWS) == 7 else "FAIL",
                "detail": f"windows={SUPPORTED_WINDOWS}"
            })
            # Basic aggregation (empty store)
            r = agg.aggregate("1d", "market")
            results.append({
                "name": "agg_1d_market",
                "status": "PASS" if isinstance(r, dict) else "FAIL",
                "detail": f"1d market aggregation returned dict"
            })
            # formal_standalone always False
            results.append({
                "name": "agg_formal_standalone_false",
                "status": "PASS" if r.get("formal_standalone") is False else "FAIL",
                "detail": f"formal_standalone={r.get('formal_standalone')}"
            })
            # Intraday blocked without precision (empty DB = no precision)
            r15 = agg.aggregate("15min", "market")
            results.append({
                "name": "agg_intraday_blocked_no_precision",
                "status": "PASS" if r15.get("blocked") is True else "FAIL",
                "detail": f"15min blocked without precision: {r15.get('blocked')}"
            })
            # Unsupported window blocked
            r_bad = agg.aggregate("30d", "market")
            results.append({
                "name": "agg_unsupported_window_blocked",
                "status": "PASS" if r_bad.get("blocked") is True else "FAIL",
                "detail": f"unsupported window blocked: {r_bad.get('blocked')}"
            })
            # All windows aggregation
            all_r = agg.aggregate_all_windows("market")
            results.append({
                "name": "agg_all_windows",
                "status": "PASS" if len(all_r) == 7 else "FAIL",
                "detail": f"all_windows returns {len(all_r)} results"
            })
            os.unlink(tmp)
        except Exception as exc:
            results.append({"name": "aggregation_checks", "status": "FAIL", "detail": str(exc)})
        return results

    # ------------------------------------------------------------------
    # Privacy checks (6)
    # ------------------------------------------------------------------
    def _privacy_checks(self) -> List[Dict]:
        results = []
        try:
            from data.providers.forum.privacy_v147 import ForumPrivacyRedactor
            redactor = ForumPrivacyRedactor()
            # IP redaction
            text_with_ip = "發文者: 123.456.789.000"
            redacted = redactor.redact_text(text_with_ip)
            results.append({
                "name": "privacy_ip_redacted",
                "status": "PASS" if "123.456.789.000" not in redacted else "FAIL",
                "detail": f"IP redacted from text"
            })
            # No full IP in output
            result = redactor.process_article_footer("發文IP: 192.168.1.1")
            results.append({
                "name": "privacy_no_full_ip_output",
                "status": "PASS" if "192.168.1.1" not in str(result.get("redacted_text", "")) else "FAIL",
                "detail": f"full IP not in output"
            })
            # Hashed display ID deterministic
            h1 = redactor.hash_display_id("user123")
            h2 = redactor.hash_display_id("user123")
            results.append({
                "name": "privacy_hash_deterministic",
                "status": "PASS" if h1 == h2 else "FAIL",
                "detail": f"hash deterministic: {h1 == h2}"
            })
            # Different IDs hash differently
            h3 = redactor.hash_display_id("user456")
            results.append({
                "name": "privacy_hash_different_ids",
                "status": "PASS" if h1 != h3 else "FAIL",
                "detail": f"different IDs hash differently"
            })
            # No identity inference
            results.append({
                "name": "privacy_no_identity_inference",
                "status": "PASS" if not hasattr(redactor, "infer_real_identity") else "FAIL",
                "detail": "no infer_real_identity method"
            })
            # No credentials in output
            text_with_cred = "密碼: mypassword123"
            redacted_cred = redactor.redact_text(text_with_cred)
            results.append({
                "name": "privacy_no_credentials",
                "status": "PASS" if "mypassword123" not in redacted_cred else "FAIL",
                "detail": "credentials redacted"
            })
        except Exception as exc:
            results.append({"name": "privacy_checks", "status": "FAIL", "detail": str(exc)})
        return results
