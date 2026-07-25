"""Business result types for financial-news classification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .analysis_result import SentimentScore
from .financial_news import FinancialNews


class NewsCategory(Enum):
    EARNINGS = "Earnings"
    MERGER_AND_ACQUISITION = "Merger & Acquisition"
    LEADERSHIP_CHANGE = "Leadership Change"
    REGULATORY_UPDATE = "Regulatory Update"
    MARKET_ANALYSIS = "Market Analysis"


@dataclass(frozen=True, slots=True)
class NewsAnalysis:
    """A news article enriched with deterministic domain analysis."""

    article: FinancialNews
    sentiment: SentimentScore
    category: NewsCategory

    @property
    def impact_score(self) -> float:
        return abs(self.sentiment.score)
