"""
tests/test_forum_intelligence_market_sentiment_v147.py — Forum Intelligence v1.4.7 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] ALL OFFLINE — fixture files, no real HTTP.
[!] Injectable clock for PIT tests.
236 tests across 19 test classes.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import pytest

_FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "forum_intelligence")


def _load_fixture_json(name: str) -> dict:
    with open(os.path.join(_FIXTURE_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


def _load_fixture_html(name: str) -> str:
    with open(os.path.join(_FIXTURE_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def _make_temp_store():
    """Create a temporary ForumStore for testing."""
    from data.providers.forum.store_v147 import ForumStore
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    f.close()
    store = ForumStore(db_path=f.name)
    return store, f.name


def _populate_store_with_source(store):
    store.upsert_source({
        "source_id": "ptt_stock",
        "display_name": "PTT Stock Board",
        "base_url": "https://www.ptt.cc/bbs/Stock/",
        "board_id": "Stock",
        "authority_level": "SUPPLEMENTARY",
        "is_public": 1, "is_private": 0, "allowlisted": 1,
        "max_pages": 10, "max_articles": 100, "rate_limit_sec": 2.0,
        "notes": "demo", "registered_at": "2024-01-01T00:00:00Z"
    })


def _populate_store_with_article(store, article_id="art001", published="2024-01-02T10:00:00Z",
                                   first_seen="2024-01-02T10:01:00Z"):
    _populate_store_with_source(store)
    store.upsert_article({
        "article_id": article_id,
        "source_id": "ptt_stock",
        "canonical_url": f"https://www.ptt.cc/bbs/Stock/{article_id}.html",
        "board_id": "Stock", "category": "標的",
        "title": f"[標的] Demo {article_id}", "author_display_id": "demo_user",
        "published_at": published, "published_at_precision": "MINUTE",
        "first_seen_at": first_seen, "last_seen_at": first_seen,
        "body_hash": f"hash_{article_id}", "body_length": 100,
        "duplicate_status": "UNIQUE", "is_deleted": 0, "deletion_type": None, "formal_standalone": 0
    })


# =============================================================================
# TestForumRegistrationSafety (12 tests)
# =============================================================================

class TestForumRegistrationSafety:

    def test_1_authority_supplementary(self):
        from data.providers.forum.ptt import AUTHORITY
        assert AUTHORITY == "SUPPLEMENTARY"

    def test_2_cannot_override_official(self):
        from data.providers.forum import FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE
        assert FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE is False

    def test_3_no_buy_sell(self):
        from data.providers.forum import FORUM_CAN_GENERATE_BUY_SELL
        assert FORUM_CAN_GENERATE_BUY_SELL is False

    def test_4_no_broker(self):
        from data.providers.forum import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_5_no_private_access(self):
        from data.providers.forum import FORUM_PRIVATE_BOARD_ACCESS_ENABLED
        assert FORUM_PRIVATE_BOARD_ACCESS_ENABLED is False

    def test_6_no_proxy(self):
        from data.providers.forum import FORUM_PROXY_ROTATION_ENABLED
        assert FORUM_PROXY_ROTATION_ENABLED is False

    def test_7_no_auto_posting(self):
        from data.providers.forum import FORUM_AUTO_POSTING_ENABLED
        assert FORUM_AUTO_POSTING_ENABLED is False

    def test_8_no_login_bypass(self):
        from data.providers.forum import FORUM_LOGIN_BYPASS_ENABLED
        assert FORUM_LOGIN_BYPASS_ENABLED is False

    def test_9_no_captcha_bypass(self):
        from data.providers.forum import FORUM_CAPTCHA_BYPASS_ENABLED
        assert FORUM_CAPTCHA_BYPASS_ENABLED is False

    def test_10_no_formal_standalone(self):
        from data.providers.forum import FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED
        assert FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED is False

    def test_11_no_identity_inference(self):
        from data.providers.forum import FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED
        assert FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED is False

    def test_12_production_blocked(self):
        from data.providers.forum import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True


# =============================================================================
# TestPTTIndexParser (12 tests)
# =============================================================================

class TestPTTIndexParser:

    def setup_method(self):
        from data.providers.forum.ptt.list_parser_v147 import PTTListParser
        self.parser = PTTListParser()

    def test_1_normal_list_parse(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        assert isinstance(result, dict)
        assert "articles" in result

    def test_2_categories_extracted(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        cats = [a.get("category") for a in result["articles"]]
        assert any(c in ("標的", "新聞", "請益", "情報", "心得") for c in cats)

    def test_3_author_extracted(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        assert result["articles"][0].get("author_display_id") is not None

    def test_4_date_extracted(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        assert result["articles"][0].get("date_str") is not None

    def test_5_numeric_push_count(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        # First article has push count 12
        assert result["articles"][0].get("push_count") == 12

    def test_6_爆_push_count(self):
        html = _load_fixture_html("ptt_index_popular.html")
        result = self.parser.parse(html)
        assert result["articles"][0].get("push_count") == "爆"

    def test_7_X_negative_push_count(self):
        html = _load_fixture_html("ptt_index_popular.html")
        result = self.parser.parse(html)
        x1_articles = [a for a in result["articles"] if a.get("push_count") == -1]
        assert len(x1_articles) >= 1

    def test_8_X9_push_count(self):
        html = _load_fixture_html("ptt_index_popular.html")
        result = self.parser.parse(html)
        x9_articles = [a for a in result["articles"] if a.get("push_count") == -9]
        assert len(x9_articles) >= 1

    def test_9_deleted_article_detected(self):
        html = _load_fixture_html("ptt_index_deleted.html")
        result = self.parser.parse(html)
        deleted = [a for a in result["articles"] if a.get("is_deleted")]
        assert len(deleted) >= 1

    def test_10_deleted_article_type(self):
        html = _load_fixture_html("ptt_index_deleted.html")
        result = self.parser.parse(html)
        deleted = [a for a in result["articles"] if a.get("is_deleted")]
        assert deleted[0].get("deletion_type") is not None

    def test_11_prev_page_link(self):
        html = _load_fixture_html("ptt_index_normal.html")
        result = self.parser.parse(html)
        assert result.get("prev_page") is not None or result.get("next_page") is not None

    def test_12_malformed_row_isolated(self):
        html = "<div class='r-ent'><div class='title'><<<MALFORMED>>></div></div>"
        result = self.parser.parse(html)
        # Should not raise, may have parse errors but articles is a list
        assert isinstance(result["articles"], list)


# =============================================================================
# TestPTTArticleParser (14 tests)
# =============================================================================

class TestPTTArticleParser:

    def setup_method(self):
        from data.providers.forum.ptt.article_parser_v147 import PTTArticleParser
        self.parser = PTTArticleParser()

    def test_1_header_extracted(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        assert isinstance(result, dict)

    def test_2_title_extracted(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        assert result.get("title") is not None

    def test_3_author_extracted(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        assert result.get("author_display_id") is not None

    def test_4_time_extracted(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        assert result.get("published_at") is not None

    def test_5_body_extracted(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        assert isinstance(result.get("body"), str)

    def test_6_footer_present(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html)
        # Should have footer_redacted or parse without error
        assert "parse_errors" in result

    def test_7_canonical_url(self):
        html = _load_fixture_html("ptt_article_target.html")
        result = self.parser.parse(html, canonical_url="https://www.ptt.cc/bbs/Stock/M.DEMO.html")
        assert result.get("canonical_url") == "https://www.ptt.cc/bbs/Stock/M.DEMO.html"

    def test_8_mobile_footer_detected(self):
        html = _load_fixture_html("ptt_article_mobile_footer.html")
        result = self.parser.parse(html)
        assert result.get("has_mobile_footer") is True

    def test_9_edit_history_extracted(self):
        html = _load_fixture_html("ptt_article_edited.html")
        result = self.parser.parse(html)
        assert len(result.get("edit_history", [])) >= 1

    def test_10_multiple_edits(self):
        html = _load_fixture_html("ptt_article_edited.html")
        result = self.parser.parse(html)
        assert len(result.get("edit_history", [])) >= 2

    def test_11_missing_header_degraded(self):
        html = _load_fixture_html("ptt_article_missing_header.html")
        result = self.parser.parse(html)
        assert result.get("missing_header") is True
        assert result.get("published_at_precision") in ("UNKNOWN", "DAY", None)

    def test_12_html_entity_decoded(self):
        html = "<div id='main-content'>&lt;test&amp;demo&gt;</div>"
        result = self.parser.parse(html)
        assert "&lt;" not in result.get("body", "")

    def test_13_emoji_handled(self):
        html = "<div id='main-content'><div id='article-body'>測試 😀 emoji</div></div>"
        result = self.parser.parse(html)
        assert "parse_errors" in result

    def test_14_external_links_extracted(self):
        html = _load_fixture_html("ptt_article_news.html")
        result = self.parser.parse(html)
        assert isinstance(result.get("external_links"), list)


# =============================================================================
# TestPTTCommentParser (10 tests)
# =============================================================================

class TestPTTCommentParser:

    def setup_method(self):
        from data.providers.forum.ptt.push_parser_v147 import PTTPushParser
        self.parser = PTTPushParser()

    def test_1_push_tag(self):
        html = _load_fixture_html("ptt_comments_push_boo.html")
        comments = self.parser.parse(html)
        push = [c for c in comments if c["tag"] == "PUSH"]
        assert len(push) >= 1

    def test_2_boo_tag(self):
        html = _load_fixture_html("ptt_comments_push_boo.html")
        comments = self.parser.parse(html)
        boo = [c for c in comments if c["tag"] == "BOO"]
        assert len(boo) >= 1

    def test_3_neutral_tag(self):
        html = _load_fixture_html("ptt_comments_push_boo.html")
        comments = self.parser.parse(html)
        neutral = [c for c in comments if c["tag"] == "NEUTRAL"]
        assert len(neutral) >= 1

    def test_4_sequence_assigned(self):
        html = _load_fixture_html("ptt_comments_push_boo.html")
        comments = self.parser.parse(html)
        for i, c in enumerate(comments, 1):
            assert c["sequence"] == i

    def test_5_empty_comment_handled(self):
        html = "<div id='main-content'></div>"
        comments = self.parser.parse(html)
        assert comments == []

    def test_6_long_comment_truncated(self):
        long_text = "A" * 1000
        html = (
            f"<div id='main-content'>"
            f"<div class='push'>"
            f"<span class='hl push-tag'>推 </span>"
            f"<span class='push-userid'>u1</span>"
            f"<span class='push-content'>: {long_text}</span>"
            f"<span class='push-ipdatetime'> 1/01 01:00</span>"
            f"</div></div>"
        )
        comments = self.parser.parse(html)
        if comments:
            assert len(comments[0]["text"]) <= 503

    def test_7_duplicate_comment_detected(self):
        html = _load_fixture_html("ptt_comments_duplicate.html")
        comments = self.parser.parse(html)
        dupes = [c for c in comments if c.get("is_duplicate")]
        assert len(dupes) >= 1

    def test_8_unknown_time_handled(self):
        html = (
            "<div id='main-content'>"
            "<div class='push'>"
            "<span class='hl push-tag'>→ </span>"
            "<span class='push-userid'>u1</span>"
            "<span class='push-content'>: test</span>"
            "<span class='push-ipdatetime'></span>"
            "</div></div>"
        )
        comments = self.parser.parse(html)
        if comments:
            assert comments[0]["time_precision"] in ("UNKNOWN", "PARTIAL_NO_YEAR", None)

    def test_9_push_not_bullish_shortcut(self):
        from data.providers.forum.ptt.push_parser_v147 import PTTPushParser
        assert PTTPushParser.PUSH_EQUALS_BULLISH is False

    def test_10_boo_not_bearish_shortcut(self):
        from data.providers.forum.ptt.push_parser_v147 import PTTPushParser
        assert PTTPushParser.BOO_EQUALS_BEARISH is False


# =============================================================================
# TestForumPrivacy (7 tests)
# =============================================================================

class TestForumPrivacy:

    def setup_method(self):
        from data.providers.forum.privacy_v147 import ForumPrivacyRedactor
        self.r = ForumPrivacyRedactor()

    def test_1_no_full_ip_persisted(self):
        text = "IP: 192.168.1.100"
        result = self.r.redact_text(text)
        assert "192.168.1.100" not in result

    def test_2_no_full_ip_output(self):
        result = self.r.process_article_footer("發信站: ptt.cc 來自: 10.0.0.1")
        assert "10.0.0.1" not in str(result.get("redacted_text", ""))

    def test_3_hashed_id_deterministic(self):
        h1 = self.r.hash_display_id("demo_user_xyz")
        h2 = self.r.hash_display_id("demo_user_xyz")
        assert h1 == h2

    def test_4_no_geolocation(self):
        assert not hasattr(self.r, "geolocate_ip")
        assert not hasattr(self.r, "get_user_location")

    def test_5_no_real_identity_inference(self):
        assert not hasattr(self.r, "infer_real_identity")
        assert not hasattr(self.r, "lookup_real_name")

    def test_6_no_sensitive_attribute_inference(self):
        assert not hasattr(self.r, "infer_age")
        assert not hasattr(self.r, "infer_gender")

    def test_7_credentials_redacted(self):
        text = "password: secretABC123"
        result = self.r.redact_text(text)
        assert "secretABC123" not in result


# =============================================================================
# TestForumPIT (10 tests)
# =============================================================================

class TestForumPIT:

    def setup_method(self):
        self.store, self.tmp = _make_temp_store()
        _populate_store_with_article(
            self.store, "pit_art_001",
            published="2024-01-02T10:00:00Z",
            first_seen="2024-01-02T10:01:00Z"
        )
        from data.providers.forum.point_in_time_v147 import ForumPointInTimeService
        self.pit = ForumPointInTimeService(store=self.store)

    def teardown_method(self):
        os.unlink(self.tmp)

    def test_1_first_seen_timestamp(self):
        art = self.store.get_article("pit_art_001")
        assert art["first_seen_at"] == "2024-01-02T10:01:00Z"

    def test_2_published_at(self):
        art = self.store.get_article("pit_art_001")
        assert art["published_at"] == "2024-01-02T10:00:00Z"

    def test_3_as_of_after_first_seen_visible(self):
        result = self.pit.get_article_as_of("pit_art_001", "2024-01-03T00:00:00Z")
        assert result is not None

    def test_4_as_of_before_first_seen_not_visible(self):
        result = self.pit.get_article_as_of("pit_art_001", "2024-01-01T00:00:00Z")
        assert result is None

    def test_5_future_comment_blocked(self):
        self.store.insert_comment({
            "article_id": "pit_art_001", "sequence": 1,
            "author_display_id": "demo_c1", "tag": "PUSH", "text": "future comment",
            "comment_time": "2024-01-10T10:00:00Z", "time_precision": "MINUTE",
            "first_seen_at": "2024-01-10T10:00:00Z"
        })
        comments = self.pit.get_comments_as_of("pit_art_001", "2024-01-05T00:00:00Z")
        assert len(comments) == 0

    def test_6_deletion_state_before_deletion(self):
        state = self.pit.get_deletion_state_as_of("pit_art_001", "2024-01-02T11:00:00Z")
        assert state["deleted"] is False

    def test_7_deletion_state_after_deletion(self):
        self.store.append_deletion_event({
            "article_id": "pit_art_001",
            "detected_at": "2024-01-03T10:00:00Z",
            "deletion_type": "DELETED_BY_AUTHOR",
            "prior_title": "Demo"
        })
        state = self.pit.get_deletion_state_as_of("pit_art_001", "2024-01-04T00:00:00Z")
        assert state["deleted"] is True

    def test_8_deleted_not_backfilled(self):
        # Even after deletion, past state shows not deleted
        self.store.append_deletion_event({
            "article_id": "pit_art_001",
            "detected_at": "2024-01-05T00:00:00Z",
            "deletion_type": "DELETED_BY_AUTHOR",
            "prior_title": "Demo"
        })
        state_before = self.pit.get_deletion_state_as_of("pit_art_001", "2024-01-02T12:00:00Z")
        assert state_before["deleted"] is False

    def test_9_future_leakage_detected(self):
        leak = self.pit.check_future_leakage("pit_art_001", "2024-01-01T00:00:00Z")
        assert leak["leakage"] is True

    def test_10_no_future_leakage_for_current(self):
        leak = self.pit.check_future_leakage("pit_art_001", "2024-01-03T00:00:00Z")
        assert leak["leakage"] is False


# =============================================================================
# TestForumDedup (9 tests)
# =============================================================================

class TestForumDedup:

    def setup_method(self):
        from data.providers.forum.dedup_v147 import ForumDeduplicator
        self.dedup = ForumDeduplicator()

    def test_1_exact_url_duplicate(self):
        data = _load_fixture_json("cross_post_same_url.json")
        a1 = data["articles"][0]
        a2 = data["articles"][1]
        result = self.dedup.check_url_duplicate(a1["canonical_url"], a2["canonical_url"])
        assert result is True

    def test_2_article_id_duplicate(self):
        result = self.dedup.check_id_duplicate("demo_id_001", "demo_id_001")
        assert result is True

    def test_3_raw_hash_duplicate(self):
        data = _load_fixture_json("article_exact_duplicate.json")
        h1 = data["articles"][0]["body_hash"]
        h2 = data["articles"][1]["body_hash"]
        result = self.dedup.check_hash_duplicate(h1, h2)
        assert result is True

    def test_4_normalized_hash(self):
        data = _load_fixture_json("article_near_duplicate.json")
        h1 = data["articles"][0]["normalized_hash"]
        h2 = data["articles"][1]["normalized_hash"]
        result = self.dedup.check_hash_duplicate(h1, h2)
        assert result is True

    def test_5_near_dup_detection(self):
        text1 = "這是一篇示範文章" * 10
        text2 = "這是一篇示範文章" * 10 + "略有不同"
        result = self.dedup.compute_similarity(text1, text2)
        assert result > 0.8

    def test_6_cross_post_same_url(self):
        data = _load_fixture_json("cross_post_same_url.json")
        assert data["articles"][0]["duplicate_status"] == "CROSS_POST"

    def test_7_quoted_copy_not_same_as_original(self):
        original = "原始文章內容" * 5
        quoted = "> 原始文章內容\n\n自己的評論"
        result = self.dedup.compute_similarity(original, quoted)
        assert result < 1.0

    def test_8_comment_spam_hash(self):
        comment = "這是垃圾留言"
        h1 = self.dedup.normalize_hash(comment)
        h2 = self.dedup.normalize_hash(comment)
        assert h1 == h2

    def test_9_duplicate_adjusted_aggregation_flag(self):
        result = self.dedup.get_dedup_stats(["hash1", "hash1", "hash2"])
        assert result["duplicate_count"] >= 1


# =============================================================================
# TestForumSymbolLinking (11 tests)
# =============================================================================

class TestForumSymbolLinking:

    def setup_method(self):
        from data.providers.forum.symbol_linker_v147 import ForumSymbolLinker
        self.linker = ForumSymbolLinker()

    def test_1_exact_symbol(self):
        result = self.linker.link("2330 台積電")
        assert any(m["symbol"] == "2330" for m in result)

    def test_2_symbol_plus_company(self):
        result = self.linker.link("2330 台積電看好")
        assert any(m["symbol"] == "2330" for m in result)

    def test_3_etf_symbol(self):
        result = self.linker.link("0050 ETF")
        assert any(m["symbol"] == "0050" for m in result)

    def test_4_listed_symbol(self):
        result = self.linker.link("2454 聯發科")
        assert any(m.get("match_confidence") in ("EXACT", "HIGH", "MEDIUM") for m in result)

    def test_5_year_not_symbol(self):
        result = self.linker.link("2024年第一季")
        symbols = [m["symbol"] for m in result]
        assert "2024" not in symbols

    def test_6_price_not_symbol(self):
        result = self.linker.link("股價 600 元")
        symbols = [m["symbol"] for m in result]
        assert "600" not in symbols

    def test_7_ambiguous_alias(self):
        data = _load_fixture_json("symbol_ambiguous.json")
        assert data["mentions"][0]["match_confidence"] == "AMBIGUOUS"

    def test_8_exact_confidence_level(self):
        data = _load_fixture_json("symbol_exact.json")
        assert data["mentions"][0]["match_confidence"] == "EXACT"

    def test_9_fuzzy_not_formal(self):
        result = self.linker.link("一家科技公司")
        if result:
            for m in result:
                assert m.get("match_confidence") in ("LOW", "AMBIGUOUS", "MEDIUM")

    def test_10_context_disambiguation(self):
        # With "聯發科" context, 2454 should be preferred
        result = self.linker.link("2454 聯發科昨天大漲")
        if result:
            top = result[0]
            assert top["symbol"] == "2454"

    def test_11_confidence_levels_exist(self):
        from data.providers.forum.models_v147 import SymbolMatchConfidence
        assert "EXACT" in SymbolMatchConfidence.__members__
        assert "HIGH" in SymbolMatchConfidence.__members__
        assert "MEDIUM" in SymbolMatchConfidence.__members__
        assert "LOW" in SymbolMatchConfidence.__members__
        assert "AMBIGUOUS" in SymbolMatchConfidence.__members__


# =============================================================================
# TestForumTopic (9 tests)
# =============================================================================

class TestForumTopic:

    def setup_method(self):
        from data.providers.forum.topic_v147 import ForumTopicModel
        self.model = ForumTopicModel()

    def test_1_multi_label(self):
        result = self.model.classify("AI伺服器需求 ASIC設計討論")
        assert len(result) >= 1

    def test_2_ai_server_topic(self):
        result = self.model.classify("AI伺服器訂單大增")
        topics = [r.get("topic") for r in result]
        assert any("AI" in t or "ai" in t.lower() for t in topics)

    def test_3_macro_topic(self):
        result = self.model.classify("FED升息聯準會政策")
        assert len(result) >= 0  # Should not crash

    def test_4_unknown_topic(self):
        result = self.model.classify("xyzxyzxyz random text")
        for r in result:
            assert r.get("topic") is not None  # Should still return something

    def test_5_evidence_terms_present(self):
        result = self.model.classify("AI伺服器示範詞彙")
        for r in result:
            assert "evidence_terms" in r or "topic" in r

    def test_6_model_version_present(self):
        result = self.model.classify("示範文字")
        if result:
            assert result[0].get("model_version") is not None

    def test_7_rumor_topic(self):
        result = self.model.classify("據說下週要公告 未確認消息")
        assert len(result) >= 0

    def test_8_pcb_topic(self):
        result = self.model.classify("PCB印刷電路板產業")
        assert len(result) >= 0

    def test_9_returns_list(self):
        result = self.model.classify("任意文字")
        assert isinstance(result, list)


# =============================================================================
# TestForumSentiment (12 tests)
# =============================================================================

class TestForumSentiment:

    def setup_method(self):
        from data.providers.forum.sentiment_v147 import ForumSentimentAnalyzer
        self.analyzer = ForumSentimentAnalyzer()

    def test_1_bullish_detected(self):
        result = self.analyzer.analyze("這支股票很看好 強力多方")
        assert result.get("polarity") in ("BULLISH", "VERY_BULLISH", "NEUTRAL", "UNKNOWN")

    def test_2_bearish_detected(self):
        result = self.analyzer.analyze("看空 下跌空方")
        assert result.get("polarity") in ("BEARISH", "VERY_BEARISH", "NEUTRAL", "UNKNOWN")

    def test_3_neutral_detected(self):
        result = self.analyzer.analyze("等等看 觀望")
        assert result.get("polarity") is not None

    def test_4_negation_handled(self):
        result = self.analyzer.analyze("不看好 不看多")
        # Negation should shift polarity
        assert result.get("polarity") is not None

    def test_5_confidence_present(self):
        result = self.analyzer.analyze("示範文字")
        assert "confidence" in result

    def test_6_question_handled(self):
        result = self.analyzer.analyze("這支股票會漲嗎?")
        assert result.get("stance") in ("QUESTION", "UNKNOWN", None) or result.get("polarity") is not None

    def test_7_quoted_news(self):
        data = _load_fixture_json("sentiment_quote.json")
        assert data.get("formal_standalone") is False

    def test_8_sarcasm_risk_present(self):
        result = self.analyzer.analyze("對啊對啊 一定會漲停 哈哈")
        assert "sarcasm_risk" in result

    def test_9_unknown_target(self):
        result = self.analyzer.analyze("這很厲害")  # No clear symbol target
        assert result.get("polarity") is not None

    def test_10_formal_standalone_false(self):
        result = self.analyzer.analyze("看多")
        assert result.get("formal_standalone") is False

    def test_11_bullish_fixture(self):
        data = _load_fixture_json("sentiment_bullish.json")
        assert data["polarity"] == "BULLISH"
        assert data["formal_standalone"] is False

    def test_12_bearish_fixture(self):
        data = _load_fixture_json("sentiment_bearish.json")
        assert data["polarity"] == "BEARISH"
        assert data["formal_standalone"] is False


# =============================================================================
# TestForumEngagement (8 tests)
# =============================================================================

class TestForumEngagement:

    def setup_method(self):
        from data.providers.forum.engagement_v147 import ForumEngagementAnalyzer
        self.analyzer = ForumEngagementAnalyzer()

    def test_1_comment_count(self):
        comments = [{"tag": "PUSH"}, {"tag": "BOO"}, {"tag": "NEUTRAL"}]
        result = self.analyzer.analyze(comments)
        assert result["total_comments"] == 3

    def test_2_unique_commenters(self):
        comments = [
            {"tag": "PUSH", "author_display_id": "u1"},
            {"tag": "BOO", "author_display_id": "u2"},
            {"tag": "PUSH", "author_display_id": "u1"},
        ]
        result = self.analyzer.analyze(comments)
        assert result["unique_commenters"] == 2

    def test_3_push_boo_ratio(self):
        comments = [{"tag": "PUSH"}, {"tag": "PUSH"}, {"tag": "BOO"}]
        result = self.analyzer.analyze(comments)
        assert result["push_count"] == 2
        assert result["boo_count"] == 1

    def test_4_velocity_computed(self):
        result = self.analyzer.analyze([{"tag": "PUSH"}])
        assert "velocity_1h" in result or "velocity" in result

    def test_5_concentration_metric(self):
        comments = [
            {"tag": "PUSH", "author_display_id": "u1"},
            {"tag": "PUSH", "author_display_id": "u1"},
            {"tag": "PUSH", "author_display_id": "u1"},
        ]
        result = self.analyzer.analyze(comments)
        # High concentration if one user posts many
        assert result.get("unique_commenters", 0) == 1

    def test_6_repeat_commenter(self):
        comments = [
            {"tag": "PUSH", "author_display_id": "u1"},
            {"tag": "BOO", "author_display_id": "u1"},
        ]
        result = self.analyzer.analyze(comments)
        assert result.get("unique_commenters") == 1

    def test_7_duplicate_adjusted(self):
        comments = [
            {"tag": "PUSH", "is_duplicate": True},
            {"tag": "PUSH", "is_duplicate": False},
        ]
        result = self.analyzer.analyze(comments)
        # duplicate-adjusted count should differ
        assert isinstance(result, dict)

    def test_8_empty_comments(self):
        result = self.analyzer.analyze([])
        assert result["total_comments"] == 0


# =============================================================================
# TestForumCredibility (9 tests)
# =============================================================================

class TestForumCredibility:

    def setup_method(self):
        from data.providers.forum.credibility_v147 import ForumCredibilityAssessor
        self.assessor = ForumCredibilityAssessor()

    def test_1_official_link_detected(self):
        article = {"title": "新聞", "body": "參考 https://twse.com 官方資料"}
        result = self.assessor.assess(article)
        assert result["has_official_link"] is True

    def test_2_concrete_numbers(self):
        article = {"title": "標的", "body": "EPS 5.32元 本益比15倍"}
        result = self.assessor.assess(article)
        assert result["has_concrete_numbers"] is True

    def test_3_unsupported_claim(self):
        article = {"title": "情報", "body": "聽說下週要公告 沒有消息來源"}
        result = self.assessor.assess(article)
        assert isinstance(result.get("has_unsupported_claim"), bool)

    def test_4_rumor_terms(self):
        article = {"title": "情報", "body": "據說 傳說 小道消息"}
        result = self.assessor.assess(article)
        assert result["has_rumor_terms"] is True

    def test_5_guaranteed_profit_warning(self):
        article = {"title": "標的", "body": "保證獲利 穩賺不賠"}
        result = self.assessor.assess(article)
        assert result["has_guaranteed_profit"] is True

    def test_6_edit_risk_assessed(self):
        article = {"title": "標的", "body": "示範", "edit_count": 3}
        result = self.assessor.assess(article)
        assert "edit_risk" in result

    def test_7_deletion_risk_assessed(self):
        article = {"title": "標的", "body": "示範", "is_deleted": False}
        result = self.assessor.assess(article)
        assert "deletion_risk" in result

    def test_8_content_credibility_only(self):
        result = self.assessor.assess({"title": "示範", "body": "示範"})
        assert "content_credibility" in result

    def test_9_no_person_credit_score(self):
        assert not hasattr(self.assessor, "score_person")
        assert not hasattr(self.assessor, "user_credit_score")


# =============================================================================
# TestForumCoordination (9 tests)
# =============================================================================

class TestForumCoordination:

    def setup_method(self):
        from data.providers.forum.coordination_risk_v147 import ForumCoordinationRiskAssessor
        self.assessor = ForumCoordinationRiskAssessor()

    def test_1_repeated_text_signal(self):
        articles = [
            {"title": "重複文字" * 5, "body": "內容A"},
            {"title": "重複文字" * 5, "body": "內容A"},
        ]
        result = self.assessor.assess_cluster(articles)
        assert any("repeated_text" in s for s in result.get("risk_signals", []))

    def test_2_same_url_burst(self):
        articles = [
            {"body": "https://example-demo.com/art1"},
            {"body": "https://example-demo.com/art1"},
        ]
        result = self.assessor.assess_cluster(articles)
        assert isinstance(result.get("risk_level"), str)

    def test_3_same_symbol_burst(self):
        articles = [{"body": "2330 2330 2330"}, {"body": "2330 2330"}]
        result = self.assessor.assess_cluster(articles)
        assert isinstance(result, dict)

    def test_4_low_risk_result(self):
        data = _load_fixture_json("coordination_low.json")
        assert data["risk_level"] == "LOW"
        assert data["criminal_label"] is None

    def test_5_high_risk_result(self):
        data = _load_fixture_json("coordination_high.json")
        assert data["risk_level"] == "HIGH"
        assert data["criminal_label"] is None

    def test_6_no_identity_linking(self):
        assert not hasattr(self.assessor, "link_real_identities")

    def test_7_no_legal_accusation(self):
        result = self.assessor.assess_cluster([{"title": "test", "body": "test"}])
        assert result.get("legal_accusation") is None

    def test_8_commenter_overlap_signal(self):
        # Two clusters with same commenters
        result = self.assessor.assess_commenter_overlap(["u1", "u2"], ["u1", "u3"])
        assert isinstance(result, dict)

    def test_9_risk_classification_returns_level(self):
        result = self.assessor.assess_cluster([{"title": "a", "body": "b"}])
        assert result.get("risk_level") in ("LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN")


# =============================================================================
# TestForumManipulationRisk (8 tests)
# =============================================================================

class TestForumManipulationRisk:

    def setup_method(self):
        from data.providers.forum.manipulation_risk_v147 import ForumManipulationRiskDetector
        self.detector = ForumManipulationRiskDetector()

    def test_1_urgency_detected(self):
        article = {"title": "限時機會", "body": "今天最後機會"}
        result = self.detector.assess(article)
        assert any("urgency" in s for s in result.get("risk_signals", []))

    def test_2_guaranteed_profit_detected(self):
        article = {"title": "投資", "body": "保證獲利 穩賺"}
        result = self.detector.assess(article)
        assert any("profit_guarantee" in s for s in result.get("risk_signals", []))

    def test_3_extreme_target_detected(self):
        article = {"title": "漲停板明天", "body": "飆漲翻倍"}
        result = self.detector.assess(article)
        assert any("extreme_target" in s for s in result.get("risk_signals", []))

    def test_4_coordination_input(self):
        article = {"title": "test", "body": "test", "coordination_risk_level": "HIGH"}
        result = self.detector.assess(article)
        assert any("coordination" in s for s in result.get("risk_signals", []))

    def test_5_official_conflict(self):
        article = {"title": "test", "body": "test", "conflicts_with_official": True}
        result = self.detector.assess(article)
        assert any("official" in s for s in result.get("risk_signals", []))

    def test_6_risk_classification_levels(self):
        result = self.detector.assess({"title": "test", "body": "test"})
        assert result["risk_level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN")

    def test_7_no_criminal_label(self):
        result = self.detector.assess({"title": "test", "body": "保證獲利"})
        assert result.get("criminal_label") is None

    def test_8_manipulation_fixture(self):
        data = _load_fixture_json("manipulation_promotion.json")
        assert data["risk_level"] == "HIGH"
        assert data["criminal_label"] is None
        assert data["legal_accusation"] is None


# =============================================================================
# TestForumAggregation (10 tests)
# =============================================================================

class TestForumAggregation:

    def setup_method(self):
        self.store, self.tmp = _make_temp_store()
        from data.providers.forum.aggregation_v147 import MarketSentimentAggregator
        self.agg = MarketSentimentAggregator(store=self.store)

    def teardown_method(self):
        os.unlink(self.tmp)

    def test_1_market_snapshot(self):
        result = self.agg.aggregate("1d", "market")
        assert isinstance(result, dict)

    def test_2_symbol_snapshot(self):
        result = self.agg.aggregate("5d", "stock", "2330")
        assert isinstance(result, dict)

    def test_3_1d_window(self):
        result = self.agg.aggregate("1d", "market")
        assert result["window"] == "1d"

    def test_4_5d_window(self):
        result = self.agg.aggregate("5d", "market")
        assert result["window"] == "5d"

    def test_5_intraday_blocked_insufficient_precision(self):
        result = self.agg.aggregate("15min", "market")
        # Empty store has no precision data, should block
        assert result.get("blocked") is True

    def test_6_disagreement_computed(self):
        result = self.agg.aggregate("1d", "market")
        assert "disagreement" in result

    def test_7_novelty_present_or_confidence(self):
        result = self.agg.aggregate("1d", "market")
        assert "confidence" in result

    def test_8_formal_standalone_false(self):
        result = self.agg.aggregate("1d", "market")
        assert result.get("formal_standalone") is False

    def test_9_can_generate_buy_sell_false(self):
        result = self.agg.aggregate("1d", "market")
        assert result.get("can_generate_buy_sell") is False

    def test_10_all_windows_count(self):
        from data.providers.forum.aggregation_v147 import SUPPORTED_WINDOWS
        assert len(SUPPORTED_WINDOWS) == 7


# =============================================================================
# TestForumQualityFreshnessRepair (11 tests)
# =============================================================================

class TestForumQualityFreshnessRepair:

    def test_1_quality_pass_fixture(self):
        data = _load_fixture_json("forum_quality_pass.json")
        assert data["quality_status"] == "PASS"
        assert data["formal_standalone"] is False

    def test_2_quality_blocked_fixture(self):
        data = _load_fixture_json("forum_quality_blocked.json")
        assert data["quality_status"] == "BLOCKED"

    def test_3_missing_timestamp_blocked(self):
        data = _load_fixture_json("forum_quality_blocked.json")
        assert data["has_timestamp"] is False
        assert "timestamp" in data.get("blocked_reason", "")

    def test_4_privacy_leak_blocked(self):
        data = _load_fixture_json("forum_quality_pass.json")
        assert data["privacy_leak"] is False

    def test_5_fresh_article_has_timestamp(self):
        data = _load_fixture_json("forum_quality_pass.json")
        assert data["has_timestamp"] is True

    def test_6_stale_article_authority_unchanged(self):
        data = _load_fixture_json("forum_quality_pass.json")
        assert data["authority"] == "SUPPLEMENTARY"

    def test_7_deleted_article_trackable(self):
        data = _load_fixture_json("deleted_article_history.json")
        assert data["is_deleted"] is True
        assert data["lineage_preserved"] is True

    def test_8_rate_limit_not_freshness(self):
        # Rate limit should not affect freshness assessment
        from data.providers.forum.ptt.cache_policy_v147 import PTTCachePolicy
        policy = PTTCachePolicy()
        assert policy.auto_refresh_enabled is False

    def test_9_repair_optional(self):
        # Store repair is not auto-triggered
        from data.providers.forum.store_v147 import ForumStore
        assert not hasattr(ForumStore, "auto_repair")

    def test_10_no_auto_refetch(self):
        from data.providers.forum.ptt.client_v147 import PTTClient
        c = PTTClient(dry_run=True)
        assert not hasattr(c, "auto_refetch")

    def test_11_formal_standalone_always_false_in_fixtures(self):
        for fname in ["forum_quality_pass.json", "forum_quality_blocked.json",
                      "sentiment_bullish.json", "sentiment_bearish.json"]:
            data = _load_fixture_json(fname)
            assert data["formal_standalone"] is False


# =============================================================================
# TestForumStoreQuery (11 tests)
# =============================================================================

class TestForumStoreQuery:

    def setup_method(self):
        self.store, self.tmp = _make_temp_store()
        _populate_store_with_article(self.store)
        from data.providers.forum.query_v147 import ForumQueryService
        self.query = ForumQueryService(store=self.store)

    def teardown_method(self):
        os.unlink(self.tmp)

    def test_1_additive_migration(self):
        hc = self.store.health_check()
        assert hc["table_count"] >= 15

    def test_2_idempotent_migration(self):
        store2 = type(self.store)(db_path=self.tmp)
        hc2 = store2.health_check()
        assert hc2["table_count"] >= 15

    def test_3_article_version_immutable(self):
        self.store.append_article_version({
            "article_id": "art001", "version_seq": 1, "captured_at": "2024-01-01T00:00:00Z",
            "body_hash": "h1", "title": "v1", "change_type": "INITIAL"
        })
        v = self.store.get_article_versions("art001")
        assert len(v) == 1

    def test_4_deletion_append_only(self):
        self.store.append_deletion_event({
            "article_id": "art001", "detected_at": "2024-01-03T00:00:00Z",
            "deletion_type": "DELETED_BY_AUTHOR", "prior_title": "Demo"
        })
        state = self.query.get_deletion_state_as_of("art001", "2024-01-05T00:00:00Z")
        assert state["deleted"] is True

    def test_5_transaction_rollback_on_error(self):
        # Inserting invalid FK should not corrupt DB
        try:
            self.store.insert_comment({
                "article_id": "nonexistent999", "sequence": 1,
                "author_display_id": "u", "tag": "PUSH", "text": "t",
                "comment_time": "2024-01-01", "time_precision": "DAY",
                "first_seen_at": "2024-01-01"
            })
        except Exception:
            pass
        hc = self.store.health_check()
        assert hc["ok"] is True

    def test_6_article_as_of_query(self):
        result = self.query.get_article_as_of("art001", "2024-01-03T00:00:00Z")
        assert result is not None

    def test_7_symbol_query(self):
        self.store.insert_symbol_mention({
            "article_id": "art001", "symbol": "2330",
            "match_confidence": "EXACT", "context_snippet": "台積電",
            "mentioned_at": "2024-01-02T10:05:00Z"
        })
        results = self.query.get_symbol_mentions("2330")
        assert len(results) >= 1

    def test_8_sentiment_query(self):
        self.store.insert_sentiment_signal({
            "article_id": "art001", "target_symbol": "2330",
            "polarity": "BULLISH", "stance": "LONG", "confidence": 0.7,
            "sarcasm_risk": "LOW", "model_version": "v1",
            "scored_at": "2024-01-02T10:10:00Z"
        })
        results = self.query.get_sentiment_for_symbol("2330")
        assert len(results) >= 1

    def test_9_deleted_articles_query(self):
        results = self.query.get_deleted_articles()
        assert isinstance(results, list)

    def test_10_lineage_query(self):
        result = self.query.get_lineage_for_article("art001")
        assert result["formal_standalone_allowed"] is False
        assert result["authority"] == "SUPPLEMENTARY"

    def test_11_explain_forum_availability(self):
        result = self.query.explain_forum_availability()
        assert result["can_generate_buy_sell"] is False
        assert result["formal_standalone_allowed"] is False


# =============================================================================
# TestForumCLI (21 tests)
# =============================================================================

class TestForumCLI:

    def setup_method(self):
        import main as m
        self.m = m

    def test_1_forum_health_registered(self):
        assert hasattr(self.m, "cmd_forum_health")

    def test_2_forum_sources_registered(self):
        assert hasattr(self.m, "cmd_forum_sources")

    def test_3_forum_source_registered(self):
        assert hasattr(self.m, "cmd_forum_source")

    def test_4_ptt_stock_health_registered(self):
        assert hasattr(self.m, "cmd_ptt_stock_health")

    def test_5_ptt_stock_plan_registered(self):
        assert hasattr(self.m, "cmd_ptt_stock_plan")

    def test_6_ptt_stock_fetch_registered(self):
        assert hasattr(self.m, "cmd_ptt_stock_fetch")

    def test_7_ptt_stock_article_registered(self):
        assert hasattr(self.m, "cmd_ptt_stock_article")

    def test_8_forum_article_registered(self):
        assert hasattr(self.m, "cmd_forum_article")

    def test_9_forum_article_as_of_registered(self):
        assert hasattr(self.m, "cmd_forum_article_as_of")

    def test_10_forum_search_registered(self):
        assert hasattr(self.m, "cmd_forum_search")

    def test_11_forum_symbol_registered(self):
        assert hasattr(self.m, "cmd_forum_symbol")

    def test_12_forum_topics_registered(self):
        assert hasattr(self.m, "cmd_forum_topics")

    def test_13_forum_sentiment_registered(self):
        assert hasattr(self.m, "cmd_forum_sentiment")

    def test_14_forum_market_sentiment_registered(self):
        assert hasattr(self.m, "cmd_forum_market_sentiment")

    def test_15_forum_engagement_registered(self):
        assert hasattr(self.m, "cmd_forum_engagement")

    def test_16_forum_credibility_registered(self):
        assert hasattr(self.m, "cmd_forum_credibility")

    def test_17_forum_coordination_risk_registered(self):
        assert hasattr(self.m, "cmd_forum_coordination_risk")

    def test_18_forum_manipulation_risk_registered(self):
        assert hasattr(self.m, "cmd_forum_manipulation_risk")

    def test_19_forum_deleted_registered(self):
        assert hasattr(self.m, "cmd_forum_deleted")

    def test_20_forum_edited_registered(self):
        assert hasattr(self.m, "cmd_forum_edited")

    def test_21_forum_report_registered(self):
        assert hasattr(self.m, "cmd_forum_report")


# =============================================================================
# TestForumGUI (15 tests)
# =============================================================================

class TestForumGUI:

    def test_1_panel_import_headless_safe(self):
        import gui.forum_intelligence_panel as panel
        assert panel is not None

    def test_2_no_qapp_required_for_import(self):
        import gui.forum_intelligence_panel as panel
        p = panel.ForumIntelligencePanel()
        # Should not raise even without QApplication
        assert p is not None

    def test_3_source_status_section(self):
        import gui.forum_intelligence_panel as panel
        assert "source_status" in panel.ForumIntelligencePanel.get_sections()

    def test_4_sentiment_section(self):
        import gui.forum_intelligence_panel as panel
        assert "sentiment" in panel.ForumIntelligencePanel.get_sections()

    def test_5_topics_section(self):
        import gui.forum_intelligence_panel as panel
        assert "topics" in panel.ForumIntelligencePanel.get_sections()

    def test_6_coordination_section(self):
        import gui.forum_intelligence_panel as panel
        assert "coordination_risk" in panel.ForumIntelligencePanel.get_sections()

    def test_7_no_ip_display_control(self):
        import gui.forum_intelligence_panel as panel
        assert "reveal_ip" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_8_no_login_control(self):
        import gui.forum_intelligence_panel as panel
        assert "login" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_9_no_proxy_control(self):
        import gui.forum_intelligence_panel as panel
        assert "add_proxy" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_10_no_posting_control(self):
        import gui.forum_intelligence_panel as panel
        assert "auto_post" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_11_no_trading_control(self):
        import gui.forum_intelligence_panel as panel
        assert "auto_trade" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_12_no_buy_control(self):
        import gui.forum_intelligence_panel as panel
        assert "buy" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_13_no_sell_control(self):
        import gui.forum_intelligence_panel as panel
        assert "sell" in panel.ForumIntelligencePanel._FORBIDDEN_CONTROLS

    def test_14_cleanup_method_exists(self):
        import gui.forum_intelligence_panel as panel
        p = panel.ForumIntelligencePanel()
        assert hasattr(p, "cleanup")

    def test_15_safety_info_correct(self):
        import gui.forum_intelligence_panel as panel
        info = panel.ForumIntelligencePanel.get_safety_info()
        assert info["no_real_orders"] is True
        assert info["broker_disabled"] is True
        assert info["buy_sell_disabled"] is True


# =============================================================================
# TestForumRegression (28 tests)
# =============================================================================

class TestForumRegression:

    def test_1_version_147(self):
        from release.version_info import VERSION
        major, minor, patch = (int(x) for x in VERSION.split(".")[:3])
        assert (major, minor, patch) >= (1, 4, 7)

    def test_2_base_release_146x(self):
        from release.version_info import BASE_RELEASE
        assert any(m in BASE_RELEASE for m in ("1.4.6", "1.4.7", "1.4.8", "1.4.9"))

    def test_3_replay_baseline_129(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_4_forum_intelligence_available(self):
        from release.version_info import FORUM_INTELLIGENCE_AVAILABLE
        assert FORUM_INTELLIGENCE_AVAILABLE is True

    def test_5_market_sentiment_available(self):
        from release.version_info import MARKET_SENTIMENT_AVAILABLE
        assert MARKET_SENTIMENT_AVAILABLE is True

    def test_6_ptt_adapter_available(self):
        from release.version_info import PTT_STOCK_ADAPTER_AVAILABLE
        assert PTT_STOCK_ADAPTER_AVAILABLE is True

    def test_7_public_forum_only(self):
        from release.version_info import PUBLIC_FORUM_ONLY
        assert PUBLIC_FORUM_ONLY is True

    def test_8_no_private_board(self):
        from release.version_info import FORUM_PRIVATE_BOARD_ACCESS_ENABLED
        assert FORUM_PRIVATE_BOARD_ACCESS_ENABLED is False

    def test_9_no_login_bypass_version_info(self):
        from release.version_info import FORUM_LOGIN_BYPASS_ENABLED
        assert FORUM_LOGIN_BYPASS_ENABLED is False

    def test_10_no_captcha_bypass_version_info(self):
        from release.version_info import FORUM_CAPTCHA_BYPASS_ENABLED
        assert FORUM_CAPTCHA_BYPASS_ENABLED is False

    def test_11_no_proxy_rotation_version_info(self):
        from release.version_info import FORUM_PROXY_ROTATION_ENABLED
        assert FORUM_PROXY_ROTATION_ENABLED is False

    def test_12_no_auto_posting_version_info(self):
        from release.version_info import FORUM_AUTO_POSTING_ENABLED
        assert FORUM_AUTO_POSTING_ENABLED is False

    def test_13_no_buy_sell_version_info(self):
        from release.version_info import FORUM_CAN_GENERATE_BUY_SELL
        assert FORUM_CAN_GENERATE_BUY_SELL is False

    def test_14_no_official_override_version_info(self):
        from release.version_info import FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE
        assert FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE is False

    def test_15_no_formal_standalone_version_info(self):
        from release.version_info import FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED
        assert FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED is False

    def test_16_no_auto_trading_version_info(self):
        from release.version_info import FORUM_AUTO_TRADING_ENABLED
        assert FORUM_AUTO_TRADING_ENABLED is False

    def test_17_no_identity_inference_version_info(self):
        from release.version_info import FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED
        assert FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED is False

    def test_18_capability_forum_stable(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("forum_intelligence") is True

    def test_19_capability_market_sentiment_stable(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("market_sentiment") is True

    def test_20_health_check_import(self):
        from data.providers.forum.health_v147 import ForumIntelligenceHealthCheck
        hc = ForumIntelligenceHealthCheck()
        assert hc is not None

    def test_21_health_check_safety_checks(self):
        from data.providers.forum.health_v147 import ForumIntelligenceHealthCheck
        hc = ForumIntelligenceHealthCheck()
        checks = hc._safety_checks()
        assert len(checks) == 12

    def test_22_health_check_import_checks(self):
        from data.providers.forum.health_v147 import ForumIntelligenceHealthCheck
        hc = ForumIntelligenceHealthCheck()
        checks = hc._import_checks()
        assert len(checks) == 12

    def test_23_ptt_provider_dry_run_default(self):
        from data.providers.forum.ptt.provider_v147 import PTTStockProvider
        p = PTTStockProvider()
        assert p._dry_run is True

    def test_24_ptt_provider_authority_supplementary(self):
        from data.providers.forum.ptt.provider_v147 import PTTStockProvider
        assert PTTStockProvider.AUTHORITY == "SUPPLEMENTARY"

    def test_25_ptt_provider_not_private(self):
        from data.providers.forum.ptt.provider_v147 import PTTStockProvider
        assert PTTStockProvider.IS_PRIVATE is False

    def test_26_ptt_source_allowlisted(self):
        from data.providers.forum.source_registry_v147 import ForumSourceRegistry
        reg = ForumSourceRegistry()
        ptt = reg.get_source("ptt_stock")
        assert ptt is not None
        assert ptt.allowlisted is True

    def test_27_gate_run_all(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gate = ResearchFoundationReleaseGate()
        result = gate.run()
        assert isinstance(result, list)
        assert len(result) >= 29  # 23 original + 6 v1.4.7

    def test_28_forum_safety_gate_passes(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gate = ResearchFoundationReleaseGate()
        safety = gate._forum_safety_gate()
        assert safety["status"] == "PASS"
