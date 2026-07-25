"""Small value objects used by the live-news sentiment analyser."""

from dataclasses import dataclass
from enum import Enum


class SentimentType(Enum):
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


@dataclass(frozen=True)
class SentimentScore:
    score: float
    confidence: float
    sentiment_type: SentimentType

    def __post_init__(self) -> None:
        if not -1.0 <= self.score <= 1.0:
            raise ValueError("Sentiment score must be between -1.0 and 1.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Sentiment confidence must be between 0.0 and 1.0")
