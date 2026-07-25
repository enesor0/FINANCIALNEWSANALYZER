"""Transparent keyword-based sentiment scoring for provider news."""

import math
import re
from collections.abc import Iterable

from ..entities.analysis_result import SentimentScore, SentimentType


class FinancialSentimentAnalyzer:
    """Score financial text using a small, explainable keyword baseline."""

    positive_keywords = frozenset({
        "growth", "profit", "gain", "increase", "rise", "bull", "bullish", "positive", "strong",
        "robust", "outperform", "exceed", "beat", "surge", "rally", "recovery", "expand", "improve",
        "optimistic", "breakthrough", "record", "success", "buy", "upgrade",
    })
    negative_keywords = frozenset({
        "loss", "decline", "fall", "drop", "bear", "bearish", "negative", "weak", "poor",
        "underperform", "miss", "fail", "crash", "plunge", "recession", "crisis", "risk", "concern",
        "uncertainty", "volatile", "sell", "downgrade", "warning", "threat", "bankruptcy", "debt",
    })
    neutral_keywords = frozenset({"stable", "maintain", "hold", "unchanged", "steady", "flat", "neutral"})

    def analyze_text(self, text: str) -> SentimentScore:
        words = re.findall(r"[a-z]+", text.lower())
        if not words:
            return SentimentScore(0.0, 0.0, SentimentType.NEUTRAL)

        positive = sum(word in self.positive_keywords for word in words)
        negative = sum(word in self.negative_keywords for word in words)
        neutral = sum(word in self.neutral_keywords for word in words)
        total = positive + negative + neutral
        if total == 0:
            return SentimentScore(0.0, 0.0, SentimentType.NEUTRAL)

        positive_probability = positive / total
        negative_probability = negative / total
        neutral_probability = neutral / total
        score = positive_probability - negative_probability
        confidence = self._confidence((positive_probability, negative_probability, neutral_probability))
        return SentimentScore(score, confidence, self._sentiment_type(score))

    def analyze_batch(self, texts: Iterable[str]) -> list[SentimentScore]:
        return [self.analyze_text(text) for text in texts]

    @staticmethod
    def _confidence(probabilities: tuple[float, float, float]) -> float:
        entropy = -sum(value * math.log(value) for value in probabilities if value)
        return round(max(0.0, 1 - entropy / math.log(3)), 3)

    @staticmethod
    def _sentiment_type(score: float) -> SentimentType:
        if score <= -0.6:
            return SentimentType.VERY_NEGATIVE
        if score <= -0.2:
            return SentimentType.NEGATIVE
        if score <= 0.2:
            return SentimentType.NEUTRAL
        if score <= 0.6:
            return SentimentType.POSITIVE
        return SentimentType.VERY_POSITIVE
