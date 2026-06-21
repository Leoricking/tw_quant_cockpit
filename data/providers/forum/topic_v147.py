"""
data/providers/forum/topic_v147.py — Forum Topic Classifier v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Rule/lexicon-based. No external LLM required. Multi-label.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Set, Tuple

from data.providers.forum.models_v147 import ForumTopicSignal

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

CLASSIFIER_VERSION = "v147_lexicon"

# 35 topic taxonomy with lexicon terms
_TOPIC_LEXICON: Dict[str, List[str]] = {
    "AI_Server": ["ai伺服器", "ai server", "人工智慧伺服器", "液冷", "散熱模組", "gpu server", "hgx", "nvl", "gb200", "h100", "b200"],
    "ASIC": ["asic", "特殊應用晶片", "客製晶片", "訓練晶片", "推論晶片"],
    "CoWoS": ["cowos", "晶圓級封裝", "先進封裝", "cpp封裝", "soi", "chiplet"],
    "Semiconductor_Fab": ["晶圓代工", "fab", "台積電", "tsmc", "聯電", "力積電", "12吋", "3奈米", "5奈米", "7奈米"],
    "Semiconductor_Design": ["ic設計", "soc", "ap", "modem", "聯發科", "瑞昱", "novatek", "聯詠"],
    "PCB": ["pcb", "電路板", "基板", "欣興", "南電", "ttm"],
    "CCL": ["ccl", "覆銅板", "台光電", "聯茂", "prismark"],
    "Networking": ["網通", "交換器", "路由器", "智邦", "中磊", "正文", "100g", "400g", "800g"],
    "Memory": ["dram", "nand", "hbm", "南亞科", "力晶", "美光", "三星記憶體"],
    "Passive_Components": ["被動元件", "mlcc", "國巨", "華新科", "yageo"],
    "Power_Management": ["電源管理", "pmic", "mosfet", "安森美", "茂達", "日月光電源"],
    "EV_Auto": ["電動車", "ev", "特斯拉", "tesla", "byd", "車用電子", "lidar"],
    "Solar_Energy": ["太陽能", "solar", "新能源", "綠電", "碳中和"],
    "Banking_Finance": ["金融股", "銀行股", "壽險", "富邦金", "國泰金", "玉山金", "中信金"],
    "ETF_Dividend": ["etf", "0050", "0056", "高股息", "00878", "配息", "除息"],
    "Real_Estate": ["房地產", "建商", "南山人壽", "遠雄", "cbre"],
    "Steel_Materials": ["鋼鐵", "中鋼", "燁輝", "鋼鐵股"],
    "Petrochemical": ["石化", "台塑", "南亞", "塑化", "中油"],
    "Telecom": ["電信", "中華電", "台灣大", "遠傳", "5g"],
    "ODM_OEM": ["odm", "oem", "代工", "鴻海", "廣達", "仁寶", "緯創"],
    "Display": ["面板", "auo", "群創", "innolux", "amoled", "oled"],
    "Medical_Biotech": ["生技", "醫療", "新藥", "食藥署", "解盲"],
    "Retail_Consumer": ["通路", "零售", "統一超", "全家", "好市多"],
    "Gaming": ["遊戲", "電競", "mmorpg", "gamepad", "艾訊"],
    "Cloud_SaaS": ["雲端", "saas", "paas", "iaas", "微軟", "google雲", "aws"],
    "Macro_Rate": ["升息", "降息", "fed", "利率", "通膨", "cpi", "pce"],
    "Geopolitics_Trade": ["地緣政治", "貿易戰", "關稅", "美中關係", "台海"],
    "Earnings_Season": ["財報", "獲利", "eps", "法說會", "業績"],
    "Technical_Analysis": ["技術面", "k線", "均線", "macd", "rsi", "黃金交叉", "死亡交叉"],
    "Fundamental_Analysis": ["基本面", "pe", "pb", "本益比", "淨值", "殖利率"],
    "Market_Sentiment": ["市場氣氛", "恐慌", "vix", "多空", "散戶", "法人"],
    "IPO_Capital": ["ipo", "上市", "上櫃", "興櫃", "現增", "可轉債", "cb"],
    "Dividend_Policy": ["股利", "配股", "配息", "殖利率", "除息日", "填息"],
    "Short_Selling": ["融券", "放空", "借券", "回補", "軋空"],
    "Miscellaneous": ["閒聊", "心得", "請益", "新聞", "情報"],
}


class ForumTopicClassifier:
    """
    Forum topic classifier v1.4.7.
    Rule/lexicon-based, multi-label.
    Returns ForumTopicSignal list with evidence_terms.
    [!] No external LLM. No network required.
    """

    VERSION = CLASSIFIER_VERSION

    def classify(self, text: str, article_id: str) -> List[ForumTopicSignal]:
        """Classify text into topics. Returns list of ForumTopicSignal."""
        if not text:
            return []
        text_lower = text.lower()
        results: List[ForumTopicSignal] = []
        for topic, terms in _TOPIC_LEXICON.items():
            matched = [t for t in terms if t.lower() in text_lower]
            if matched:
                conf = min(1.0, 0.3 + 0.15 * len(matched))
                results.append(ForumTopicSignal(
                    signal_id=str(uuid.uuid4())[:8],
                    article_id=article_id,
                    topic=topic,
                    confidence=round(conf, 3),
                    evidence_terms=matched[:5],
                    classifier_version=CLASSIFIER_VERSION,
                ))
        # If no match, classify as Miscellaneous
        if not results:
            results.append(ForumTopicSignal(
                signal_id=str(uuid.uuid4())[:8],
                article_id=article_id,
                topic="Miscellaneous",
                confidence=0.1,
                evidence_terms=[],
                classifier_version=CLASSIFIER_VERSION,
            ))
        return results

    def list_topics(self) -> List[str]:
        return list(_TOPIC_LEXICON.keys())


class ForumTopicModel:
    """
    Simplified interface for forum topic classification.
    Wraps ForumTopicClassifier with text-only classify(text) method.
    Returns list of dicts (not ForumTopicSignal objects) for easy consumption.
    """

    def __init__(self) -> None:
        self._classifier = ForumTopicClassifier()

    def classify(self, text: str) -> List[Dict]:
        """Classify text into topics. Returns list of dicts."""
        import uuid as _uuid
        signals = self._classifier.classify(text, article_id=_uuid.uuid4().hex[:8])
        return [
            {
                "topic": s.topic,
                "confidence": s.confidence,
                "evidence_terms": s.evidence_terms,
                "model_version": s.classifier_version,
            }
            for s in signals
        ]
