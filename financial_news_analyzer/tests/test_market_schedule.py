"""Tests for timezone-aware weekday market schedule calculations."""
from datetime import datetime, time
import unittest

import pytz

from financial_news_analyzer.src.domain.entities.market import Market, MarketRegion, MarketStatus


def make_market():
    return Market(
        code="TEST",
        name="Test Exchange",
        country_code="US",
        country_flag="🇺🇸",
        timezone="America/New_York",
        region=MarketRegion.AMERICAS,
        open_time=time(9, 30),
        close_time=time(16, 0),
    )


class MarketScheduleTests(unittest.TestCase):
    def test_weekend_is_closed_even_during_regular_hours(self):
        eastern = pytz.timezone("America/New_York")
        saturday_morning = eastern.localize(datetime(2026, 7, 25, 10, 0))

        self.assertEqual(make_market().get_current_status(saturday_morning), MarketStatus.CLOSED)

    def test_weekday_is_open_during_regular_hours(self):
        eastern = pytz.timezone("America/New_York")
        monday_morning = eastern.localize(datetime(2026, 7, 27, 10, 0))

        self.assertEqual(make_market().get_current_status(monday_morning), MarketStatus.OPEN)

    def test_next_open_skips_weekend_and_month_boundary(self):
        eastern = pytz.timezone("America/New_York")
        friday_after_close = eastern.localize(datetime(2026, 7, 31, 17, 0))

        next_open = make_market()._next_open_after(friday_after_close)

        self.assertEqual(next_open, eastern.localize(datetime(2026, 8, 3, 9, 30)))


if __name__ == "__main__":
    unittest.main()
