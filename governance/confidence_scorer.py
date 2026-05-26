"""Confidence scorer — computes a 0-1 score for each AI response."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

from config import CONFIDENCE_THRESHOLD, ESCALATION_THRESHOLD


@dataclass
class ConfidenceResult:
    score: float
    label: str           # "high" | "medium" | "low" | "critical_low"
    needs_review: bool
    needs_escalation: bool
    factors: dict


class ConfidenceScorer:
    """
    Heuristic confidence scoring based on:
    - Retrieval score of best matching document
    - Number of retrieved docs
    - Whether API calls were successful
    - Whether intent classification was decisive
    - Presence of knowledge gaps in response
    """

    def score(
        self,
        intent: str,
        retrieval_scores: List[float],
        api_success: bool | None,
        intent_confidence: float,
        response_length: int,
        has_fallback_phrases: bool,
    ) -> ConfidenceResult:
        factors = {}

        # Component 1: retrieval quality (0-0.35)
        if retrieval_scores:
            best_score = max(retrieval_scores)
            avg_score = sum(retrieval_scores) / len(retrieval_scores)
            retrieval_component = min(best_score * 0.25 + avg_score * 0.10, 0.35)
        else:
            retrieval_component = 0.05  # Low if no docs found
        factors["retrieval"] = round(retrieval_component, 3)

        # Component 2: intent confidence (0-0.30)
        intent_component = min(intent_confidence * 0.30, 0.30)
        factors["intent_confidence"] = round(intent_component, 3)

        # Component 3: API result (0-0.20) — only if relevant
        if api_success is None:
            api_component = 0.15  # Neutral; not required
        elif api_success:
            api_component = 0.20
        else:
            api_component = 0.05
        factors["api_result"] = round(api_component, 3)

        # Component 4: response quality signals (0-0.15)
        quality_component = 0.15
        if has_fallback_phrases:
            quality_component -= 0.08
        if response_length < 50:
            quality_component -= 0.05
        quality_component = max(quality_component, 0.0)
        factors["response_quality"] = round(quality_component, 3)

        total = retrieval_component + intent_component + api_component + quality_component
        total = min(max(total, 0.0), 1.0)
        factors["total"] = round(total, 3)

        if total >= CONFIDENCE_THRESHOLD:
            label = "high" if total >= 0.80 else "medium"
            needs_review = False
            needs_escalation = False
        elif total >= ESCALATION_THRESHOLD:
            label = "low"
            needs_review = True
            needs_escalation = False
        else:
            label = "critical_low"
            needs_review = True
            needs_escalation = True

        return ConfidenceResult(
            score=round(total, 3),
            label=label,
            needs_review=needs_review,
            needs_escalation=needs_escalation,
            factors=factors,
        )

    def label_color(self, label: str) -> str:
        return {
            "high": "green",
            "medium": "blue",
            "low": "orange",
            "critical_low": "red",
        }.get(label, "gray")


FALLBACK_PHRASES = [
    "i'm not sure",
    "i don't know",
    "i cannot find",
    "i'm unable to",
    "i apologize, but",
    "unfortunately, i don't have",
    "i don't have information",
]


def has_fallback(response: str) -> bool:
    lower = response.lower()
    return any(phrase in lower for phrase in FALLBACK_PHRASES)


_SCORER: ConfidenceScorer | None = None


def get_scorer() -> ConfidenceScorer:
    global _SCORER
    if _SCORER is None:
        _SCORER = ConfidenceScorer()
    return _SCORER
