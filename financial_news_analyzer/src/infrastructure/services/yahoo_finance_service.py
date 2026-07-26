"""Yahoo Finance implementation of the application's outbound data ports."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd

from ...application.exceptions import DataProviderUnavailable
from ...domain.entities.financial_news import FinancialNews
from ...domain.entities.market_data import (
    InstrumentProfile,
    InstrumentSearchResult,
    MarketInstrument,
    MarketQuote,
    PriceBar,
)


class YahooFinanceService:
    """Translate yfinance responses into provider-neutral domain models.

    This adapter is the only application module that knows about pandas and
    yfinance's response shapes.  It deliberately does not return DataFrames or
    provider dictionaries beyond the infrastructure boundary.
    """

    source_name = "Yahoo Finance via yfinance"
    @staticmethod
    def _client() -> Any:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise DataProviderUnavailable(
                "The live-data dependency is missing. Install requirements.txt first."
            ) from exc
        return yf

    @staticmethod
    def _as_float(value: Any) -> float | None:
        if value is None or pd.isna(value):
            return None
        return float(value)

    @staticmethod
    def _as_int(value: Any) -> int | None:
        if value is None or pd.isna(value):
            return None
        return int(value)

    @staticmethod
    def _as_text(value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @staticmethod
    def _as_datetime(value: Any) -> datetime:
        timestamp = pd.Timestamp(value)
        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize(timezone.utc)
        return timestamp.to_pydatetime()

    def get_market_snapshot(self, instruments: Sequence[MarketInstrument]) -> tuple[MarketQuote, ...]:
        """Return normalized latest quotes for the requested instruments."""
        requested_instruments = tuple(instruments)
        if not requested_instruments:
            return ()

        yf = self._client()
        symbols = [instrument.symbol for instrument in requested_instruments]
        try:
            history = yf.download(
                tickers=symbols,
                period="5d",
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False,
                group_by="ticker",
            )
        except Exception as exc:
            raise DataProviderUnavailable("Live market data could not be retrieved.") from exc
        if history is None or history.empty:
            raise DataProviderUnavailable("The provider returned no market data.")

        quotes: list[MarketQuote] = []
        for instrument in requested_instruments:
            try:
                frame = history[instrument.symbol] if isinstance(history.columns, pd.MultiIndex) else history
                frame = frame.dropna(subset=["Close"])
                if frame.empty:
                    continue
                latest = frame.iloc[-1]
                price = self._as_float(latest["Close"])
                if price is None:
                    continue
                previous_close = self._as_float(frame.iloc[-2]["Close"]) if len(frame) > 1 else None
                raw_volume = latest.get("Volume")
                quotes.append(
                    MarketQuote(
                        instrument=instrument,
                        price=price,
                        previous_close=previous_close,
                        volume=None if raw_volume is None or pd.isna(raw_volume) else int(raw_volume),
                        day_high=self._as_float(latest.get("High")),
                        day_low=self._as_float(latest.get("Low")),
                        observed_at=self._as_datetime(frame.index[-1]),
                        provider=self.source_name,
                    )
                )
            except (KeyError, IndexError, TypeError, ValueError):
                continue
        if not quotes:
            raise DataProviderUnavailable("The provider returned no usable market rows.")
        return tuple(quotes)

    def get_history(self, symbol: str, days: int) -> tuple[PriceBar, ...]:
        """Return actual daily OHLCV bars for one symbol."""
        yf = self._client()
        end = datetime.now(timezone.utc) + timedelta(days=1)
        start = end - timedelta(days=max(days, 5))
        try:
            frame = yf.Ticker(symbol).history(
                start=start.date(),
                end=end.date(),
                interval="1d",
                auto_adjust=True,
            )
        except Exception as exc:
            raise DataProviderUnavailable(f"History for {symbol} could not be retrieved.") from exc
        if frame is None or frame.empty:
            raise DataProviderUnavailable(f"No history is available for {symbol}.")

        bars: list[PriceBar] = []
        for observed_at, row in frame.iterrows():
            try:
                open_price = self._as_float(row["Open"])
                high_price = self._as_float(row["High"])
                low_price = self._as_float(row["Low"])
                close_price = self._as_float(row["Close"])
                if None in (open_price, high_price, low_price, close_price):
                    continue
                raw_volume = row.get("Volume")
                bars.append(
                    PriceBar(
                        observed_at=self._as_datetime(observed_at),
                        open_price=open_price,
                        high_price=high_price,
                        low_price=low_price,
                        close_price=close_price,
                        volume=None if raw_volume is None or pd.isna(raw_volume) else int(raw_volume),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue
        if not bars:
            raise DataProviderUnavailable(f"No usable history is available for {symbol}.")
        return tuple(bars)

    def search_instruments(self, query: str, limit: int = 12) -> tuple[InstrumentSearchResult, ...]:
        """Discover equities, funds, indices, currencies, futures, and crypto assets."""
        yf = self._client()
        try:
            results = yf.Search(
                query,
                max_results=limit,
                news_count=0,
                lists_count=0,
                include_cb=False,
                include_nav_links=False,
                include_research=False,
                include_cultural_assets=False,
                enable_fuzzy_query=True,
                recommended=0,
            ).quotes or []
        except Exception as exc:
            raise DataProviderUnavailable(f"Instruments matching {query} could not be retrieved.") from exc

        matches: list[InstrumentSearchResult] = []
        seen_symbols: set[str] = set()
        for item in results:
            if not isinstance(item, dict):
                continue
            symbol = self._as_text(item.get("symbol"))
            if not symbol or symbol in seen_symbols:
                continue
            seen_symbols.add(symbol)
            matches.append(
                InstrumentSearchResult(
                    symbol=symbol,
                    name=self._as_text(item.get("longname") or item.get("shortname")) or symbol,
                    exchange=self._as_text(item.get("exchDisp") or item.get("exchange")),
                    quote_type=self._as_text(item.get("typeDisp") or item.get("quoteType")) or "Unknown",
                    sector=self._as_text(item.get("sectorDisp") or item.get("sector")),
                    industry=self._as_text(item.get("industryDisp") or item.get("industry")),
                )
            )
        return tuple(matches)

    def get_instrument_profile(self, symbol: str) -> InstrumentProfile:
        """Return descriptive metadata and the latest available headline metrics."""
        yf = self._client()
        try:
            info = yf.Ticker(symbol).info or {}
        except Exception as exc:
            raise DataProviderUnavailable(f"Details for {symbol} could not be retrieved.") from exc
        if not isinstance(info, dict) or not info:
            raise DataProviderUnavailable(f"No details are available for {symbol}.")

        return InstrumentProfile(
            symbol=self._as_text(info.get("symbol")) or symbol,
            name=self._as_text(info.get("longName") or info.get("shortName")) or symbol,
            short_name=self._as_text(info.get("shortName")),
            quote_type=self._as_text(info.get("quoteType")) or "Unknown",
            currency=self._as_text(info.get("currency")),
            exchange=self._as_text(info.get("fullExchangeName") or info.get("exchange")),
            sector=self._as_text(info.get("sector")),
            industry=self._as_text(info.get("industry")),
            price=self._as_float(info.get("regularMarketPrice") or info.get("currentPrice")),
            previous_close=self._as_float(
                info.get("regularMarketPreviousClose") or info.get("previousClose")
            ),
            open_price=self._as_float(info.get("regularMarketOpen") or info.get("open")),
            day_high=self._as_float(info.get("regularMarketDayHigh") or info.get("dayHigh")),
            day_low=self._as_float(info.get("regularMarketDayLow") or info.get("dayLow")),
            volume=self._as_int(info.get("regularMarketVolume") or info.get("volume")),
            market_cap=self._as_int(info.get("marketCap")),
            trailing_pe=self._as_float(info.get("trailingPE")),
            forward_pe=self._as_float(info.get("forwardPE")),
            dividend_yield=self._as_float(info.get("dividendYield")),
            fifty_two_week_high=self._as_float(info.get("fiftyTwoWeekHigh")),
            fifty_two_week_low=self._as_float(info.get("fiftyTwoWeekLow")),
            average_volume=self._as_int(info.get("averageVolume")),
            beta=self._as_float(info.get("beta")),
            website=self._as_text(info.get("website")),
            description=self._as_text(info.get("longBusinessSummary")),
        )

    def search_news(self, company: str, limit: int = 12) -> tuple[FinancialNews, ...]:
        """Return provider articles without fabricating missing metadata or links."""
        yf = self._client()
        try:
            results = yf.Search(company, news_count=limit).news or []
        except Exception as exc:
            raise DataProviderUnavailable(f"News for {company} could not be retrieved.") from exc

        articles: list[FinancialNews] = []
        for index, item in enumerate(results):
            if not isinstance(item, dict):
                continue
            content = item.get("content") or item
            if not isinstance(content, dict):
                continue
            title = content.get("title") or item.get("title")
            if not title:
                continue
            provider = content.get("provider", {})
            provider_name = provider.get("displayName") if isinstance(provider, dict) else provider
            canonical_url = content.get("canonicalUrl", {})
            url = canonical_url.get("url") if isinstance(canonical_url, dict) else canonical_url
            click_through = content.get("clickThroughUrl", {})
            url = url or (click_through.get("url") if isinstance(click_through, dict) else None) or item.get("link")
            published = content.get("pubDate") or item.get("providerPublishTime")
            articles.append(
                FinancialNews(
                    id=str(content.get("id") or item.get("uuid") or f"{company}-{index}-{title}"),
                    title=str(title),
                    summary=str(content.get("summary") or item.get("summary") or title),
                    source=str(provider_name or self.source_name),
                    published_at=self._parse_published_at(published),
                    url=str(url) if url else None,
                    company=company,
                )
            )
        return tuple(articles)

    @staticmethod
    def _parse_published_at(value: Any) -> datetime:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)
        parsed = pd.to_datetime(value, utc=True, errors="coerce")
        if not pd.isna(parsed):
            return parsed.to_pydatetime()
        return datetime.now(timezone.utc)
