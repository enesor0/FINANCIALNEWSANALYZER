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
    positive_phrases = frozenset({
        "beats estimates", "beat estimates", "raises guidance", "raised guidance",
        "record high", "revenue growth", "margin expansion", "share buyback",
        "dividend increase", "contract win", "regulatory approval",
    })
    negative_phrases = frozenset({
        "misses estimates", "missed estimates", "cuts guidance", "cut guidance",
        "revenue decline", "margin compression", "regulatory investigation",
        "credit downgrade", "dividend cut", "data breach", "mass layoffs",
    })
    negations = frozenset({"not", "no", "never", "without", "hardly"})

    def analyze_text(self, text: str) -> SentimentScore:
        words = re.findall(r"[a-z]+", text.lower())
        if not words:
            return SentimentScore(0.0, 0.0, SentimentType.NEUTRAL)

        positive = 0.0
        negative = 0.0
        neutral = 0.0
        for index, word in enumerate(words):
            is_negated = self._is_negated(words, index)
            if word in self.positive_keywords:
                negative += 1 if is_negated else 0
                positive += 0 if is_negated else 1
            elif word in self.negative_keywords:
                positive += 1 if is_negated else 0
                negative += 0 if is_negated else 1
            elif word in self.neutral_keywords:
                neutral += 1

        normalized_text = " ".join(words)
        positive += sum(normalized_text.count(phrase) * 2 for phrase in self.positive_phrases)
        negative += sum(normalized_text.count(phrase) * 2 for phrase in self.negative_phrases)
        total = positive + negative + neutral
        if total == 0:
            return SentimentScore(0.0, 0.0, SentimentType.NEUTRAL)

        positive_probability = positive / total
        negative_probability = negative / total
        neutral_probability = neutral / total
        score = positive_probability - negative_probability
        evidence_sufficiency = min(1.0, total / 3)
        confidence = round(
            self._confidence((positive_probability, negative_probability, neutral_probability))
            * evidence_sufficiency,
            3,
        )
        return SentimentScore(score, confidence, self._sentiment_type(score))

    def analyze_batch(self, texts: Iterable[str]) -> list[SentimentScore]:
        return [self.analyze_text(text) for text in texts]

    def keyword_evidence(self, text: str) -> dict[str, tuple[str, ...]]:
        """Return the unique keyword matches that explain a sentiment score."""
        words = re.findall(r"[a-z]+", text.lower())
        normalized_text = " ".join(words)
        positive: set[str] = set()
        negative: set[str] = set()
        neutral: set[str] = set()
        for index, word in enumerate(words):
            is_negated = self._is_negated(words, index)
            if word in self.positive_keywords:
                (negative if is_negated else positive).add(f"not {word}" if is_negated else word)
            elif word in self.negative_keywords:
                (positive if is_negated else negative).add(f"not {word}" if is_negated else word)
            elif word in self.neutral_keywords:
                neutral.add(word)
        positive.update(phrase for phrase in self.positive_phrases if phrase in normalized_text)
        negative.update(phrase for phrase in self.negative_phrases if phrase in normalized_text)
        return {
            "positive": tuple(sorted(positive)),
            "negative": tuple(sorted(negative)),
            "neutral": tuple(sorted(neutral)),
        }

    def _is_negated(self, words: list[str], index: int) -> bool:
        return any(word in self.negations for word in words[max(0, index - 2):index])

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
