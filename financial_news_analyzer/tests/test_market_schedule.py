"""Tests for timezone-aware weekday market schedule calculations."""
from datetime import datetime, time
import unittest
from zoneinfo import ZoneInfo

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
        eastern = ZoneInfo("America/New_York")
        saturday_morning = datetime(2026, 7, 25, 10, 0, tzinfo=eastern)

        self.assertEqual(make_market().get_current_status(saturday_morning), MarketStatus.CLOSED)

    def test_weekday_is_open_during_regular_hours(self):
        eastern = ZoneInfo("America/New_York")
        monday_morning = datetime(2026, 7, 27, 10, 0, tzinfo=eastern)

        self.assertEqual(make_market().get_current_status(monday_morning), MarketStatus.OPEN)

    def test_next_open_skips_weekend_and_month_boundary(self):
        eastern = ZoneInfo("America/New_York")
        friday_after_close = datetime(2026, 7, 31, 17, 0, tzinfo=eastern)

        next_open = make_market()._next_open_after(friday_after_close)

        self.assertEqual(next_open, datetime(2026, 8, 3, 9, 30, tzinfo=eastern))

    def test_sunday_thursday_schedule_supports_saudi_market(self):
        riyadh = ZoneInfo("Asia/Riyadh")
        market = Market(
            code="TADAWUL",
            name="Saudi Stock Exchange",
            country_code="SA",
            country_flag="🇸🇦",
            timezone="Asia/Riyadh",
            region=MarketRegion.MENA_AFRICA,
            open_time=time(10, 0),
            close_time=time(15, 0),
            trading_weekdays={6, 0, 1, 2, 3},
        )

        self.assertEqual(
            market.get_current_status(datetime(2026, 7, 26, 11, 0, tzinfo=riyadh)),
            MarketStatus.OPEN,
        )
        self.assertEqual(
            market.get_current_status(datetime(2026, 7, 24, 11, 0, tzinfo=riyadh)),
            MarketStatus.CLOSED,
        )


if __name__ == "__main__":
    unittest.main()
