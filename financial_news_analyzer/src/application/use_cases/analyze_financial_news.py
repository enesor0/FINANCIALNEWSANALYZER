"""Use case that enriches provider articles with domain analysis."""

from __future__ import annotations

from collections.abc import Iterable

from ...domain.entities.news_analysis import NewsAnalysis
from ...domain.services.news_categorization_service import FinancialNewsCategorizer
from ...domain.services.sentiment_analysis_service import FinancialSentimentAnalyzer
from ..ports.financial_news_provider import FinancialNewsProvider


class AnalyzeFinancialNewsUseCase:
    """Coordinate article retrieval, sentiment scoring, and categorization."""

    def __init__(
        self,
        news_provider: FinancialNewsProvider,
        sentiment_analyzer: FinancialSentimentAnalyzer,
        categorizer: FinancialNewsCategorizer,
    ) -> None:
        self._news_provider = news_provider
        self._sentiment_analyzer = sentiment_analyzer
        self._categorizer = categorizer

    def execute(self, companies: Iterable[str], limit_per_company: int = 12) -> tuple[NewsAnalysis, ...]:
        """Return unique, newest-first analyses for the selected companies."""
        analyses: list[NewsAnalysis] = []
        seen_articles: set[str] = set()
        for company in dict.fromkeys(company.strip() for company in companies if company.strip()):
            for article in self._news_provider.search_news(company, limit_per_company):
                article_key = article.url or article.id
                if article_key in seen_articles:
                    continue
                seen_articles.add(article_key)
                analyses.append(
                    NewsAnalysis(
                        article=article,
                        sentiment=self._sentiment_analyzer.analyze_text(article.text_for_analysis),
                        category=self._categorizer.categorize(article.title),
                    )
                )
        return tuple(sorted(analyses, key=lambda analysis: analysis.article.published_at, reverse=True))
