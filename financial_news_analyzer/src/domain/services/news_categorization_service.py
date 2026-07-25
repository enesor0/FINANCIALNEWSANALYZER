"""Deterministic financial-news category policy."""

from __future__ import annotations

from ..entities.news_analysis import NewsCategory


class FinancialNewsCategorizer:
    """Classify headlines using transparent financial-news keywords."""

    _rules: tuple[tuple[NewsCategory, tuple[str, ...]], ...] = (
        (NewsCategory.EARNINGS, ("earnings", "revenue", "guidance", "quarter")),
        (NewsCategory.MERGER_AND_ACQUISITION, ("acquire", "acquisition", "merger", "takeover")),
        (NewsCategory.LEADERSHIP_CHANGE, ("ceo", "cfo", "executive", "appoints")),
        (NewsCategory.REGULATORY_UPDATE, ("regulator", "sec ", "lawsuit", "antitrust")),
    )

    def categorize(self, headline: str) -> NewsCategory:
        normalized_headline = headline.casefold()
        for category, keywords in self._rules:
            if any(keyword in normalized_headline for keyword in keywords):
                return category
        return NewsCategory.MARKET_ANALYSIS
