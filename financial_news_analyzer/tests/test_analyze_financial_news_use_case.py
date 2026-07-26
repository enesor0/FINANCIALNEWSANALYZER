"""Unit tests for the application boundary around news analysis."""

from datetime import datetime, timezone
import unittest

from financial_news_analyzer.src.application.use_cases.analyze_financial_news import AnalyzeFinancialNewsUseCase
from financial_news_analyzer.src.domain.entities.financial_news import FinancialNews
from financial_news_analyzer.src.domain.entities.news_analysis import NewsCategory
from financial_news_analyzer.src.domain.services.news_categorization_service import FinancialNewsCategorizer
from financial_news_analyzer.src.domain.services.sentiment_analysis_service import FinancialSentimentAnalyzer


class _FakeNewsProvider:
    def search_news(self, company: str, limit: int = 12):
        common_article = FinancialNews(
            id="shared-article",
            title="Company reports strong revenue growth",
            summary="The quarter beat expectations.",
            source="Test Wire",
            published_at=datetime(2026, 7, 25, 10, tzinfo=timezone.utc),
            company=company,
            url="https://example.test/shared",
        )
        return (common_article,)


class AnalyzeFinancialNewsUseCaseTests(unittest.TestCase):
    def test_deduplicates_articles_and_applies_domain_policies(self):
        use_case = AnalyzeFinancialNewsUseCase(
            news_provider=_FakeNewsProvider(),
            sentiment_analyzer=FinancialSentimentAnalyzer(),
            categorizer=FinancialNewsCategorizer(),
        )

        analyses = use_case.execute(["Apple", "Microsoft"])

        self.assertEqual(len(analyses), 1)
        self.assertEqual(analyses[0].category, NewsCategory.EARNINGS)
        self.assertGreater(analyses[0].sentiment.score, 0)
        self.assertGreater(analyses[0].impact_score, 0)

    def test_sentiment_exposes_keyword_evidence(self):
        evidence = FinancialSentimentAnalyzer().keyword_evidence(
            "Strong revenue growth beat estimates despite debt risk."
        )

        self.assertEqual(
            evidence["positive"],
            ("beat", "beat estimates", "growth", "revenue growth", "strong"),
        )
        self.assertEqual(evidence["negative"], ("debt", "risk"))

    def test_sentiment_understands_simple_negation(self):
        analyzer = FinancialSentimentAnalyzer()

        self.assertLess(analyzer.analyze_text("Results were not strong.").score, 0)
        self.assertIn("not strong", analyzer.keyword_evidence("Results were not strong.")["negative"])


if __name__ == "__main__":
    unittest.main()
