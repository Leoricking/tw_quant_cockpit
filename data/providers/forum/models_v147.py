"""
data/providers/forum/models_v147.py — Forum Intelligence data models v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SUPPLEMENTARY authority only. No full IP storage. No real identity inference.
[!] standalone_conclusion_allowed=False always. formal_use_allowed=False always.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ForumAuthorityLevel(Enum):
    SUPPLEMENTARY = "SUPPLEMENTARY"
    UNVERIFIED_PUBLIC_DISCUSSION = "UNVERIFIED_PUBLIC_DISCUSSION"


class ForumDuplicateStatus(Enum):
    UNIQUE = "UNIQUE"
    EXACT_DUPLICATE = "EXACT_DUPLICATE"
    NEAR_DUPLICATE = "NEAR_DUPLICATE"
    CROSS_POST = "CROSS_POST"
    QUOTED_COPY = "QUOTED_COPY"
    COMMENT_SPAM = "COMMENT_SPAM"
    UNKNOWN = "UNKNOWN"


class CommentTag(Enum):
    PUSH = "PUSH"
    BOO = "BOO"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"


class SentimentPolarity(Enum):
    VERY_BEARISH = "VERY_BEARISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    BULLISH = "BULLISH"
    VERY_BULLISH = "VERY_BULLISH"
    UNKNOWN = "UNKNOWN"


class SentimentStance(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    HOLD = "HOLD"
    WATCH = "WATCH"
    QUESTION = "QUESTION"
    NEWS_REPORT = "NEWS_REPORT"
    JOKE = "JOKE"
    SARCASM = "SARCASM"
    UNKNOWN = "UNKNOWN"


class ManipulationRiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ForumFreshnessStatus(Enum):
    LIVE_WINDOW = "LIVE_WINDOW"
    RECENT = "RECENT"
    AGING = "AGING"
    STALE = "STALE"
    DELETED = "DELETED"
    UNKNOWN = "UNKNOWN"


class SymbolMatchConfidence(Enum):
    EXACT = "EXACT"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    AMBIGUOUS = "AMBIGUOUS"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ForumSource:
    """Represents a forum data source registration."""
    source_id: str
    display_name: str
    base_url: str
    board_id: str
    authority_level: str = "SUPPLEMENTARY"
    is_public: bool = True
    is_private: bool = False
    requires_login: bool = False
    allowlisted: bool = False
    max_pages: int = 10
    max_articles: int = 100
    rate_limit_sec: float = 2.0
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "display_name": self.display_name,
            "base_url": self.base_url,
            "board_id": self.board_id,
            "authority_level": self.authority_level,
            "is_public": self.is_public,
            "is_private": self.is_private,
            "requires_login": self.requires_login,
            "allowlisted": self.allowlisted,
            "max_pages": self.max_pages,
            "max_articles": self.max_articles,
            "rate_limit_sec": self.rate_limit_sec,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumSource":
        return cls(
            source_id=d["source_id"],
            display_name=d.get("display_name", ""),
            base_url=d.get("base_url", ""),
            board_id=d.get("board_id", ""),
            authority_level=d.get("authority_level", "SUPPLEMENTARY"),
            is_public=d.get("is_public", True),
            is_private=d.get("is_private", False),
            requires_login=d.get("requires_login", False),
            allowlisted=d.get("allowlisted", False),
            max_pages=d.get("max_pages", 10),
            max_articles=d.get("max_articles", 100),
            rate_limit_sec=d.get("rate_limit_sec", 2.0),
            notes=d.get("notes", ""),
        )


@dataclass
class ForumArticle:
    """
    Forum article. author_id_hash is salted one-way hash — NOT raw identity.
    No full IP stored. No real identity inference.
    """
    article_id: str
    source_id: str
    board_id: str
    canonical_url: str
    title: str
    category: str
    author_id_hash: str  # salted hash — NOT raw PTT ID, NOT real identity
    author_display_partial: str  # e.g. "A*****" — display safe partial
    published_at: Optional[str] = None
    fetched_at: Optional[str] = None
    body_text: str = ""
    body_normalized: str = ""
    raw_hash: str = ""
    normalized_hash: str = ""
    external_links: List[str] = field(default_factory=list)
    has_edit_history: bool = False
    deletion_state: str = "LIVE"
    freshness_status: str = "UNKNOWN"
    duplicate_status: str = "UNKNOWN"
    authority_level: str = "SUPPLEMENTARY"
    formal_use_allowed: bool = False
    standalone_conclusion_allowed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_id": self.article_id,
            "source_id": self.source_id,
            "board_id": self.board_id,
            "canonical_url": self.canonical_url,
            "title": self.title,
            "category": self.category,
            "author_id_hash": self.author_id_hash,
            "author_display_partial": self.author_display_partial,
            "published_at": self.published_at,
            "fetched_at": self.fetched_at,
            "body_text": self.body_text,
            "body_normalized": self.body_normalized,
            "raw_hash": self.raw_hash,
            "normalized_hash": self.normalized_hash,
            "external_links": self.external_links,
            "has_edit_history": self.has_edit_history,
            "deletion_state": self.deletion_state,
            "freshness_status": self.freshness_status,
            "duplicate_status": self.duplicate_status,
            "authority_level": self.authority_level,
            "formal_use_allowed": self.formal_use_allowed,
            "standalone_conclusion_allowed": self.standalone_conclusion_allowed,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumArticle":
        return cls(
            article_id=d["article_id"],
            source_id=d.get("source_id", ""),
            board_id=d.get("board_id", ""),
            canonical_url=d.get("canonical_url", ""),
            title=d.get("title", ""),
            category=d.get("category", ""),
            author_id_hash=d.get("author_id_hash", ""),
            author_display_partial=d.get("author_display_partial", ""),
            published_at=d.get("published_at"),
            fetched_at=d.get("fetched_at"),
            body_text=d.get("body_text", ""),
            body_normalized=d.get("body_normalized", ""),
            raw_hash=d.get("raw_hash", ""),
            normalized_hash=d.get("normalized_hash", ""),
            external_links=d.get("external_links", []),
            has_edit_history=d.get("has_edit_history", False),
            deletion_state=d.get("deletion_state", "LIVE"),
            freshness_status=d.get("freshness_status", "UNKNOWN"),
            duplicate_status=d.get("duplicate_status", "UNKNOWN"),
            authority_level=d.get("authority_level", "SUPPLEMENTARY"),
            formal_use_allowed=d.get("formal_use_allowed", False),
            standalone_conclusion_allowed=d.get("standalone_conclusion_allowed", False),
        )


@dataclass
class ForumComment:
    """Forum comment (push/boo/neutral). No real identity inference."""
    comment_id: str
    article_id: str
    tag: str  # PUSH / BOO / NEUTRAL / UNKNOWN
    author_id_hash: str  # salted hash
    author_display_partial: str
    text: str
    sequence: int = 0
    comment_time: Optional[str] = None
    time_precision: str = "UNKNOWN"  # FULL / DATE_ONLY / UNKNOWN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "comment_id": self.comment_id,
            "article_id": self.article_id,
            "tag": self.tag,
            "author_id_hash": self.author_id_hash,
            "author_display_partial": self.author_display_partial,
            "text": self.text,
            "sequence": self.sequence,
            "comment_time": self.comment_time,
            "time_precision": self.time_precision,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumComment":
        return cls(
            comment_id=d["comment_id"],
            article_id=d.get("article_id", ""),
            tag=d.get("tag", "UNKNOWN"),
            author_id_hash=d.get("author_id_hash", ""),
            author_display_partial=d.get("author_display_partial", ""),
            text=d.get("text", ""),
            sequence=d.get("sequence", 0),
            comment_time=d.get("comment_time"),
            time_precision=d.get("time_precision", "UNKNOWN"),
        )


@dataclass
class ForumEditEvent:
    """Edit event for a forum article. No full timestamp unless page provides it."""
    edit_id: str
    article_id: str
    sequence: int
    editor_id_hash: str  # hashed
    edit_source: str  # e.g. "footer_marker"
    edited_at: Optional[str] = None
    time_precision: str = "UNKNOWN"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edit_id": self.edit_id,
            "article_id": self.article_id,
            "sequence": self.sequence,
            "editor_id_hash": self.editor_id_hash,
            "edit_source": self.edit_source,
            "edited_at": self.edited_at,
            "time_precision": self.time_precision,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumEditEvent":
        return cls(
            edit_id=d["edit_id"],
            article_id=d.get("article_id", ""),
            sequence=d.get("sequence", 0),
            editor_id_hash=d.get("editor_id_hash", ""),
            edit_source=d.get("edit_source", ""),
            edited_at=d.get("edited_at"),
            time_precision=d.get("time_precision", "UNKNOWN"),
        )


@dataclass
class ForumDeletionEvent:
    """Tracks deleted articles detected in list pages."""
    deletion_id: str
    article_id: str
    list_page_url: str
    deletion_detected_at: str
    deletion_type: str  # e.g. "author_deleted", "moderator_deleted", "unknown"
    title_hint: str = ""
    author_hint_hash: str = ""  # hashed if available
    previous_lineage_ref: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deletion_id": self.deletion_id,
            "article_id": self.article_id,
            "list_page_url": self.list_page_url,
            "deletion_detected_at": self.deletion_detected_at,
            "deletion_type": self.deletion_type,
            "title_hint": self.title_hint,
            "author_hint_hash": self.author_hint_hash,
            "previous_lineage_ref": self.previous_lineage_ref,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumDeletionEvent":
        return cls(
            deletion_id=d["deletion_id"],
            article_id=d.get("article_id", ""),
            list_page_url=d.get("list_page_url", ""),
            deletion_detected_at=d.get("deletion_detected_at", ""),
            deletion_type=d.get("deletion_type", "unknown"),
            title_hint=d.get("title_hint", ""),
            author_hint_hash=d.get("author_hint_hash", ""),
            previous_lineage_ref=d.get("previous_lineage_ref", ""),
        )


@dataclass
class ForumSymbolMention:
    """A stock symbol mentioned in an article or comment."""
    mention_id: str
    article_id: str
    symbol: str
    confidence: str  # EXACT / HIGH / MEDIUM / LOW / AMBIGUOUS
    match_text: str  # the text fragment matched
    context_snippet: str = ""
    formal_use_eligible: bool = False  # only EXACT/HIGH may be True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mention_id": self.mention_id,
            "article_id": self.article_id,
            "symbol": self.symbol,
            "confidence": self.confidence,
            "match_text": self.match_text,
            "context_snippet": self.context_snippet,
            "formal_use_eligible": self.formal_use_eligible,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumSymbolMention":
        return cls(
            mention_id=d["mention_id"],
            article_id=d.get("article_id", ""),
            symbol=d.get("symbol", ""),
            confidence=d.get("confidence", "UNKNOWN"),
            match_text=d.get("match_text", ""),
            context_snippet=d.get("context_snippet", ""),
            formal_use_eligible=d.get("formal_use_eligible", False),
        )


@dataclass
class ForumTopicSignal:
    """Topic classification signal for an article."""
    signal_id: str
    article_id: str
    topic: str
    confidence: float = 0.0
    evidence_terms: List[str] = field(default_factory=list)
    classifier_version: str = "v147_lexicon"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "article_id": self.article_id,
            "topic": self.topic,
            "confidence": self.confidence,
            "evidence_terms": self.evidence_terms,
            "classifier_version": self.classifier_version,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumTopicSignal":
        return cls(
            signal_id=d["signal_id"],
            article_id=d.get("article_id", ""),
            topic=d.get("topic", ""),
            confidence=d.get("confidence", 0.0),
            evidence_terms=d.get("evidence_terms", []),
            classifier_version=d.get("classifier_version", "v147_lexicon"),
        )


@dataclass
class ForumSentimentSignal:
    """
    Sentiment analysis signal. polarity is author's assessed view, not comment tag shortcut.
    [!] push_tag != bullish. boo_tag != bearish. Must analyze content.
    """
    signal_id: str
    article_id: str
    polarity: str  # SentimentPolarity
    stance: str  # SentimentStance
    confidence: float = 0.0
    sarcasm_risk: float = 0.0
    negation_handled: bool = False
    quotation_excluded: bool = False
    news_headline_detected: bool = False
    analyzer_version: str = "v147_lexicon"
    formal_use_allowed: bool = False
    standalone_conclusion_allowed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "article_id": self.article_id,
            "polarity": self.polarity,
            "stance": self.stance,
            "confidence": self.confidence,
            "sarcasm_risk": self.sarcasm_risk,
            "negation_handled": self.negation_handled,
            "quotation_excluded": self.quotation_excluded,
            "news_headline_detected": self.news_headline_detected,
            "analyzer_version": self.analyzer_version,
            "formal_use_allowed": self.formal_use_allowed,
            "standalone_conclusion_allowed": self.standalone_conclusion_allowed,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumSentimentSignal":
        return cls(
            signal_id=d["signal_id"],
            article_id=d.get("article_id", ""),
            polarity=d.get("polarity", "UNKNOWN"),
            stance=d.get("stance", "UNKNOWN"),
            confidence=d.get("confidence", 0.0),
            sarcasm_risk=d.get("sarcasm_risk", 0.0),
            negation_handled=d.get("negation_handled", False),
            quotation_excluded=d.get("quotation_excluded", False),
            news_headline_detected=d.get("news_headline_detected", False),
            analyzer_version=d.get("analyzer_version", "v147_lexicon"),
            formal_use_allowed=d.get("formal_use_allowed", False),
            standalone_conclusion_allowed=d.get("standalone_conclusion_allowed", False),
        )


@dataclass
class ForumEngagementSignal:
    """Engagement analytics for an article. No real person identification."""
    signal_id: str
    article_id: str
    push_count: int = 0
    boo_count: int = 0
    neutral_count: int = 0
    total_comments: int = 0
    push_ratio: float = 0.0
    boo_ratio: float = 0.0
    neutral_ratio: float = 0.0
    velocity: float = 0.0
    burst_score: float = 0.0
    concentration: float = 0.0
    repeat_commenter_ratio: float = 0.0  # based on hash; no real person ID
    duplicate_adjusted_volume: int = 0
    unique_commenter_count: int = 0  # count of unique hashes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "article_id": self.article_id,
            "push_count": self.push_count,
            "boo_count": self.boo_count,
            "neutral_count": self.neutral_count,
            "total_comments": self.total_comments,
            "push_ratio": self.push_ratio,
            "boo_ratio": self.boo_ratio,
            "neutral_ratio": self.neutral_ratio,
            "velocity": self.velocity,
            "burst_score": self.burst_score,
            "concentration": self.concentration,
            "repeat_commenter_ratio": self.repeat_commenter_ratio,
            "duplicate_adjusted_volume": self.duplicate_adjusted_volume,
            "unique_commenter_count": self.unique_commenter_count,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumEngagementSignal":
        return cls(**{k: d.get(k, v) for k, v in cls.__dataclass_fields__.items()})  # type: ignore[attr-defined]


@dataclass
class ForumCredibilitySignal:
    """Content credibility signal. Evaluates content quality only — NOT person credit score."""
    signal_id: str
    article_id: str
    official_source_links: int = 0
    concrete_numbers: int = 0
    unsupported_claims: int = 0
    rumor_terms: int = 0
    guaranteed_profit_language: bool = False
    certainty_risk: float = 0.0
    edit_after_publish: bool = False
    deletion_risk: float = 0.0
    content_quality_score: float = 0.0  # 0-1, content only
    person_credit_score_generated: bool = False  # MUST be False always

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "article_id": self.article_id,
            "official_source_links": self.official_source_links,
            "concrete_numbers": self.concrete_numbers,
            "unsupported_claims": self.unsupported_claims,
            "rumor_terms": self.rumor_terms,
            "guaranteed_profit_language": self.guaranteed_profit_language,
            "certainty_risk": self.certainty_risk,
            "edit_after_publish": self.edit_after_publish,
            "deletion_risk": self.deletion_risk,
            "content_quality_score": self.content_quality_score,
            "person_credit_score_generated": self.person_credit_score_generated,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumCredibilitySignal":
        return cls(**{k: d.get(k, v) for k, v in cls.__dataclass_fields__.items()})  # type: ignore[attr-defined]


@dataclass
class ForumCoordinationRisk:
    """
    Coordination risk detection. NEVER identifies same real person across accounts.
    NEVER accuses of crime. NEVER cross-platform de-anonymization.
    """
    risk_id: str
    article_id: str
    repeated_text_score: float = 0.0
    synchronized_post_score: float = 0.0
    same_link_score: float = 0.0
    same_symbol_burst_score: float = 0.0
    commenter_overlap_score: float = 0.0
    copy_paste_cluster_count: int = 0
    risk_level: str = "UNKNOWN"  # LOW / MEDIUM / HIGH / CRITICAL / UNKNOWN
    identity_linking_performed: bool = False  # MUST be False
    cross_platform_deanon_performed: bool = False  # MUST be False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "article_id": self.article_id,
            "repeated_text_score": self.repeated_text_score,
            "synchronized_post_score": self.synchronized_post_score,
            "same_link_score": self.same_link_score,
            "same_symbol_burst_score": self.same_symbol_burst_score,
            "commenter_overlap_score": self.commenter_overlap_score,
            "copy_paste_cluster_count": self.copy_paste_cluster_count,
            "risk_level": self.risk_level,
            "identity_linking_performed": self.identity_linking_performed,
            "cross_platform_deanon_performed": self.cross_platform_deanon_performed,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumCoordinationRisk":
        return cls(**{k: d.get(k, v) for k, v in cls.__dataclass_fields__.items()})  # type: ignore[attr-defined]


@dataclass
class ForumManipulationRisk:
    """
    Manipulation risk detection.
    NEVER generates legal labels: 犯罪者/詐騙犯/主力/內線.
    """
    risk_id: str
    article_id: str
    promotional_language_score: float = 0.0
    urgency_score: float = 0.0
    guaranteed_profit_score: float = 0.0
    coordinated_activity_score: float = 0.0
    low_credibility_score: float = 0.0
    promotional_risk: str = "LOW"
    coordinated_risk: str = "LOW"
    misinformation_risk: str = "LOW"
    certainty_risk: str = "LOW"
    overall_risk_level: str = "LOW"
    legal_label_generated: bool = False  # MUST be False always

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "article_id": self.article_id,
            "promotional_language_score": self.promotional_language_score,
            "urgency_score": self.urgency_score,
            "guaranteed_profit_score": self.guaranteed_profit_score,
            "coordinated_activity_score": self.coordinated_activity_score,
            "low_credibility_score": self.low_credibility_score,
            "promotional_risk": self.promotional_risk,
            "coordinated_risk": self.coordinated_risk,
            "misinformation_risk": self.misinformation_risk,
            "certainty_risk": self.certainty_risk,
            "overall_risk_level": self.overall_risk_level,
            "legal_label_generated": self.legal_label_generated,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ForumManipulationRisk":
        return cls(**{k: d.get(k, v) for k, v in cls.__dataclass_fields__.items()})  # type: ignore[attr-defined]


@dataclass
class MarketSentimentSnapshot:
    """
    Aggregated market sentiment snapshot.
    [!] formal_use_allowed=False. standalone_conclusion_allowed=False.
    """
    snapshot_id: str
    window: str  # e.g. "1h", "1d", "3d"
    dimension: str  # e.g. "market", "stock:2330", "topic:AI_Server"
    as_of: str
    mention_count: int = 0
    unique_author_count: int = 0  # unique hashes
    bullish_ratio: float = 0.0
    bearish_ratio: float = 0.0
    net_sentiment: float = 0.0
    sentiment_velocity: float = 0.0
    disagreement: float = 0.0
    engagement: float = 0.0
    novelty: float = 0.0
    duplicate_adjusted_volume: int = 0
    coordination_risk: str = "LOW"
    manipulation_risk: str = "LOW"
    intraday_blocked: bool = False  # True if comment timestamp precision is insufficient
    formal_use_allowed: bool = False
    standalone_conclusion_allowed: bool = False
    auxiliary_feature_allowed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "window": self.window,
            "dimension": self.dimension,
            "as_of": self.as_of,
            "mention_count": self.mention_count,
            "unique_author_count": self.unique_author_count,
            "bullish_ratio": self.bullish_ratio,
            "bearish_ratio": self.bearish_ratio,
            "net_sentiment": self.net_sentiment,
            "sentiment_velocity": self.sentiment_velocity,
            "disagreement": self.disagreement,
            "engagement": self.engagement,
            "novelty": self.novelty,
            "duplicate_adjusted_volume": self.duplicate_adjusted_volume,
            "coordination_risk": self.coordination_risk,
            "manipulation_risk": self.manipulation_risk,
            "intraday_blocked": self.intraday_blocked,
            "formal_use_allowed": self.formal_use_allowed,
            "standalone_conclusion_allowed": self.standalone_conclusion_allowed,
            "auxiliary_feature_allowed": self.auxiliary_feature_allowed,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MarketSentimentSnapshot":
        return cls(**{k: d.get(k, v) for k, v in cls.__dataclass_fields__.items()})  # type: ignore[attr-defined]
