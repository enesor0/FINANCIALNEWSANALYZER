"""In-memory configuration adapter for the global market-clock schedules."""

from __future__ import annotations

from datetime import time

from ...domain.entities.market import Market, MarketRegion


class StaticMarketScheduleRepository:
    """Provide the fixed exchange schedule catalogue used by the UI."""

    _markets: tuple[Market, ...] = (
        Market("NYSE", "New York Stock Exchange", "US", "🇺🇸", "America/New_York", MarketRegion.AMERICAS, time(9, 30), time(16), currency="USD"),
        Market("NASDAQ", "NASDAQ", "US", "🇺🇸", "America/New_York", MarketRegion.AMERICAS, time(9, 30), time(16), currency="USD"),
        Market("TSX", "Toronto Stock Exchange", "CA", "🇨🇦", "America/Toronto", MarketRegion.AMERICAS, time(9, 30), time(16), currency="CAD"),
        Market("BOVESPA", "B3 - Brasil Bolsa Balcão", "BR", "🇧🇷", "America/Sao_Paulo", MarketRegion.AMERICAS, time(10), time(17), currency="BRL"),
        Market("LSE", "London Stock Exchange", "GB", "🇬🇧", "Europe/London", MarketRegion.EUROPE, time(8), time(16, 30), currency="GBP"),
        Market("DAX", "Frankfurt Stock Exchange", "DE", "🇩🇪", "Europe/Berlin", MarketRegion.EUROPE, time(9), time(17, 30), currency="EUR"),
        Market("EURONEXT", "Euronext Paris", "FR", "🇫🇷", "Europe/Paris", MarketRegion.EUROPE, time(9), time(17, 30), currency="EUR"),
        Market("BIST", "Borsa Istanbul", "TR", "🇹🇷", "Europe/Istanbul", MarketRegion.EUROPE, time(10), time(18), currency="TRY"),
        Market("TSE", "Tokyo Stock Exchange", "JP", "🇯🇵", "Asia/Tokyo", MarketRegion.ASIA_PACIFIC, time(9), time(15), currency="JPY"),
        Market("SSE", "Shanghai Stock Exchange", "CN", "🇨🇳", "Asia/Shanghai", MarketRegion.ASIA_PACIFIC, time(9, 30), time(15), currency="CNY"),
        Market("HKEX", "Hong Kong Stock Exchange", "HK", "🇭🇰", "Asia/Hong_Kong", MarketRegion.ASIA_PACIFIC, time(9, 30), time(16), currency="HKD"),
        Market("ASX", "Australian Securities Exchange", "AU", "🇦🇺", "Australia/Sydney", MarketRegion.ASIA_PACIFIC, time(10), time(16), currency="AUD"),
        Market("DFM", "Dubai Financial Market", "AE", "🇦🇪", "Asia/Dubai", MarketRegion.MENA_AFRICA, time(10), time(14), currency="AED"),
        Market("TADAWUL", "Saudi Stock Exchange", "SA", "🇸🇦", "Asia/Riyadh", MarketRegion.MENA_AFRICA, time(10), time(15), frozenset({6, 0, 1, 2, 3}), "SAR"),
    )

    def list_markets(self) -> tuple[Market, ...]:
        return self._markets
