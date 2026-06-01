"""replay/training_mode.py — Replay Training Mode: questions and scoring (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Training answers are NOT trading instructions. No orders. No broker calls.
[!] Not investment advice."""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Question type constants
# ---------------------------------------------------------------------------
OPENING_RANGE_DECISION = "OPENING_RANGE_DECISION"
VWAP_DECISION = "VWAP_DECISION"
FAKE_BREAKOUT_RISK = "FAKE_BREAKOUT_RISK"
CHASE_OR_WAIT = "CHASE_OR_WAIT"
SUPPORT_PRESSURE = "SUPPORT_PRESSURE"
EXIT_OR_HOLD = "EXIT_OR_HOLD"


# ---------------------------------------------------------------------------
# ReplayTrainingQuestion dataclass
# ---------------------------------------------------------------------------
@dataclass
class ReplayTrainingQuestion:
    """A single training question presented during replay.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    Answers are NOT trading instructions.
    """

    question_id: str
    bar_index: int = 0
    time: str = ""
    question_type: str = ""
    prompt: str = ""
    choices: list = field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    related_event_id: str = ""
    revealed_after_answer: bool = True

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "bar_index": self.bar_index,
            "time": self.time,
            "question_type": self.question_type,
            "prompt": self.prompt,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "related_event_id": self.related_event_id,
            "revealed_after_answer": self.revealed_after_answer,
        }


def _make_qid() -> str:
    return "Q-" + str(uuid.uuid4())[:8].upper()


# ---------------------------------------------------------------------------
# Question templates
# ---------------------------------------------------------------------------
_QUESTIONS = {
    "OPENING_RANGE_BREAK": {
        "question_type": OPENING_RANGE_DECISION,
        "prompt": "Price just broke above the opening range high. What is the training-appropriate response?",
        "choices": [
            "A. Wait for a retest of the OR high before acting",
            "B. Chase the break immediately",
            "C. Avoid — volume is too low to confirm the break",
            "D. Short immediately — it will fail",
        ],
        "correct_answer": "A",
        "explanation": (
            "Waiting for a retest of the breakout level reduces chase risk. "
            "Chasing a fresh breakout without confirmation is a common training mistake. "
            "Volume confirmation matters — low volume breaks have higher failure rates."
        ),
    },
    "VWAP_RECLAIM": {
        "question_type": VWAP_DECISION,
        "prompt": "Price just reclaimed VWAP after trading below it. How does this change the intraday context?",
        "choices": [
            "A. Bullish context shift — buyers regained control",
            "B. Bearish — VWAP reclaims are always traps",
            "C. Neutral — VWAP crossings mean nothing intraday",
            "D. Sell everything — VWAP reclaims trigger stops",
        ],
        "correct_answer": "A",
        "explanation": (
            "VWAP reclaims after a period below often signal a shift in intraday momentum. "
            "This is a training observation, not a trade signal. Always consider volume and "
            "the broader context."
        ),
    },
    "VWAP_LOST": {
        "question_type": VWAP_DECISION,
        "prompt": "Price just lost VWAP after trading above it for several bars. What does this suggest?",
        "choices": [
            "A. Potential bearish shift — sellers pushing back",
            "B. Guaranteed reversal to the day's low",
            "C. Time to buy aggressively",
            "D. Ignore VWAP — it is irrelevant",
        ],
        "correct_answer": "A",
        "explanation": (
            "Losing VWAP can indicate weakening momentum. It is not a guaranteed reversal, "
            "but it shifts the intraday context toward the sellers."
        ),
    },
    "FAKE_BREAKOUT_WARNING": {
        "question_type": FAKE_BREAKOUT_RISK,
        "prompt": "A potential fake breakout pattern has been detected. What training lesson applies here?",
        "choices": [
            "A. The cost of chasing a breakout that fails exceeds the missed gain from waiting",
            "B. Fake breakouts always recover — keep holding",
            "C. Double down at the break level",
            "D. Volume does not matter for breakout quality",
        ],
        "correct_answer": "A",
        "explanation": (
            "Fake breakouts are one of the most expensive patterns to chase. "
            "The asymmetry of risk: missing a real breakout costs opportunity; "
            "chasing a fake one costs capital. Patience and confirmation are key training principles."
        ),
    },
    "VOLUME_SPIKE": {
        "question_type": CHASE_OR_WAIT,
        "prompt": "A volume spike 2x+ the recent average has appeared. What is the training-appropriate analysis?",
        "choices": [
            "A. Volume spikes signal conviction — note the direction and wait for confirmation",
            "B. Chase the move immediately — high volume is always bullish",
            "C. Volume spikes mean nothing intraday",
            "D. Sell immediately — spikes always reverse",
        ],
        "correct_answer": "A",
        "explanation": (
            "Volume spikes indicate strong participation in that bar's direction. "
            "The training lesson: note the direction, wait for price to confirm "
            "before acting. High volume can support both reversals and continuations."
        ),
    },
    "POC_TOUCH": {
        "question_type": SUPPORT_PRESSURE,
        "prompt": "Price is testing the Point of Control (POC) from today's volume profile. What does this level represent?",
        "choices": [
            "A. The price at which the most trading activity occurred — often acts as support/resistance",
            "B. An arbitrary price level with no significance",
            "C. A guaranteed bounce level",
            "D. A guaranteed breakdown level",
        ],
        "correct_answer": "A",
        "explanation": (
            "The POC is the price level with the most traded volume. Market memory often "
            "causes price to respect these levels. It is not a guaranteed reaction point, "
            "but it is a significant area of trader interest."
        ),
    },
}


# ---------------------------------------------------------------------------
# ReplayTrainingMode
# ---------------------------------------------------------------------------
class ReplayTrainingMode:
    """Manages training questions, scoring, and answer recording.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    Training answers are NOT trading instructions. No orders. No broker calls.
    """

    read_only = True
    no_real_orders = True

    def __init__(self):
        self._questions: dict = {}       # question_id -> ReplayTrainingQuestion
        self._answers: dict = {}         # question_id -> {"answer": str, "correct": bool}
        self._score: int = 0
        self._total_score_possible: int = 0

    # ------------------------------------------------------------------
    # Generate questions
    # ------------------------------------------------------------------
    def generate_questions(self, replay_events: list, df) -> list:
        """Create training questions based on detected events. No crash if events empty."""
        if not replay_events:
            return []

        questions = []

        # map event type to question template key
        event_type_map = {
            "OPENING_RANGE_BREAK": "OPENING_RANGE_BREAK",
            "VWAP_RECLAIM": "VWAP_RECLAIM",
            "VWAP_LOST": "VWAP_LOST",
            "FAKE_BREAKOUT_WARNING": "FAKE_BREAKOUT_WARNING",
            "VOLUME_SPIKE": "VOLUME_SPIKE",
            "POC_TOUCH": "POC_TOUCH",
        }

        seen_types: set = set()

        for event in replay_events:
            try:
                event_type = event.event_type if hasattr(event, "event_type") else event.get("event_type", "")
                bar_index = event.bar_index if hasattr(event, "bar_index") else event.get("bar_index", 0)
                event_id = event.event_id if hasattr(event, "event_id") else event.get("event_id", "")
                event_time = event.time if hasattr(event, "time") else event.get("time", "")

                template_key = event_type_map.get(event_type)
                if template_key is None:
                    continue

                # Avoid duplicate question types in a short session
                if template_key in seen_types:
                    continue
                seen_types.add(template_key)

                tmpl = _QUESTIONS.get(template_key)
                if tmpl is None:
                    continue

                qid = _make_qid()
                q = ReplayTrainingQuestion(
                    question_id=qid,
                    bar_index=bar_index,
                    time=event_time,
                    question_type=tmpl["question_type"],
                    prompt=tmpl["prompt"],
                    choices=list(tmpl["choices"]),
                    correct_answer=tmpl["correct_answer"],
                    explanation=tmpl["explanation"],
                    related_event_id=event_id,
                )
                self._questions[qid] = q
                self._total_score_possible += 10
                questions.append(q)

            except Exception as exc:
                logger.warning("[ReplayTrainingMode] generate_questions error: %s", exc)

        return questions

    # ------------------------------------------------------------------
    # Answer recording
    # ------------------------------------------------------------------
    def answer_question(self, question_id: str, answer: str) -> dict:
        """Record answer. Returns correctness, explanation, and score delta.
        Answers are NOT trading instructions.
        """
        question = self._questions.get(question_id)
        if question is None:
            return {"ok": False, "error": "question_not_found", "research_only": True}

        correct = answer.strip().upper().startswith(question.correct_answer.upper())
        score_delta = 10 if correct else 0
        self._score += score_delta

        self._answers[question_id] = {
            "answer": answer,
            "correct": correct,
            "score_delta": score_delta,
        }

        return {
            "ok": True,
            "correct": correct,
            "explanation": question.explanation if question.revealed_after_answer else "",
            "score_delta": score_delta,
            "research_only": True,
            "no_real_orders": True,
            "training_note": "These answers are NOT trading instructions.",
        }

    # ------------------------------------------------------------------
    # Session scoring
    # ------------------------------------------------------------------
    def score_session(self) -> dict:
        total_questions = len(self._questions)
        answered = len(self._answers)
        correct = sum(1 for a in self._answers.values() if a.get("correct", False))
        accuracy = correct / max(answered, 1)
        training_score = (self._score / max(self._total_score_possible, 1)) * 100.0
        training_score = min(100.0, training_score)

        if training_score >= 90:
            grade = "A"
        elif training_score >= 80:
            grade = "B"
        elif training_score >= 70:
            grade = "C"
        elif training_score >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "total_questions": total_questions,
            "answered": answered,
            "correct": correct,
            "accuracy": round(accuracy, 4),
            "training_score": round(training_score, 2),
            "grade": grade,
            "research_only": True,
            "no_real_orders": True,
            "training_note": "Training score only. Not a performance metric for real trading.",
        }
