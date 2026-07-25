"""Contract tests for the live Yahoo Finance adapter without network access."""
from __future__ import annotations

import unittest
from unittest.mock import patch

import pandas as pd

from financial_news_analyzer.src.infrastructure.services.yahoo_finance_service import YahooFinanceService


class _FakeSearch:
    news = [{
        "content": {
            "id": "article-1",
            "title": "Apple reports strong revenue growth",
            "summary": "Quarterly results exceeded expectations.",
            "provider": {"displayName": "Example News"},
            "canonicalUrl": {"url": "https://example.test/article-1"},
            "pubDate": "2026-07-25T10:00:00Z",
        }
    }]


class _FakeTicker:
    def history(self, **_kwargs):
        return pd.DataFrame({
            "Open": [100.0], "High": [102.0], "Low": [99.0],
            "Close": [101.0], "Volume": [1_000],
        }, index=pd.to_datetime(["2026-07-25"]))


class _FakeYFinance:
    def download(self, **_kwargs):
        frame = pd.DataFrame({
            "Open": [100.0, 102.0], "High": [103.0, 105.0],
            "Low": [99.0, 101.0], "Close": [101.0, 104.0],
            "Volume": [1_000, 2_000],
        }, index=pd.to_datetime(["2026-07-24", "2026-07-25"]))
        return pd.concat({"AAPL": frame}, axis=1)

    def Ticker(self, _symbol):
        return _FakeTicker()

    def Search(self, _query, news_count):
        self.news_count = news_count
        return _FakeSearch()


class YahooFinanceServiceTests(unittest.TestCase):
    def setUp(self):
        self.client_patch = patch.object(YahooFinanceService, "_client", return_value=_FakeYFinance())
        self.client_patch.start()
        self.addCleanup(self.client_patch.stop)

    def test_snapshot_normalizes_provider_prices(self):
        snapshot = YahooFinanceService.get_market_snapshot([("AAPL", "Apple", "Technology")])

        self.assertEqual(snapshot.iloc[0]["Symbol"], "AAPL")
        self.assertEqual(snapshot.iloc[0]["Price"], 104.0)
        self.assertAlmostEqual(snapshot.iloc[0]["Change_Pct"], 2.97, places=2)
        self.assertEqual(snapshot.iloc[0]["Data_Source"], YahooFinanceService.source_name)

    def test_news_keeps_the_provider_link_and_metadata(self):
        article = YahooFinanceService.search_news("Apple", limit=5)[0]

        self.assertEqual(article["company"], "Apple")
        self.assertEqual(article["source"], "Example News")
        self.assertEqual(article["link"], "https://example.test/article-1")
        self.assertEqual(article["data_source"], YahooFinanceService.source_name)


if __name__ == "__main__":
    unittest.main()
