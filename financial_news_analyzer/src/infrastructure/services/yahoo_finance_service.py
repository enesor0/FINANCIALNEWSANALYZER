"""Yahoo Finance-backed market and news retrieval.

The service exposes data provenance and never invents a value when the live
provider is unavailable. Yahoo Finance data is suitable for development and
personal-use research; production use needs a separately licensed provider.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

import pandas as pd


class LiveDataUnavailable(RuntimeError):
    """Raised when the configured live provider cannot return usable data."""


class YahooFinanceService:
    """Read market prices, history, and linked news from Yahoo Finance."""

    source_name = "Yahoo Finance via yfinance"
    source_url = "https://finance.yahoo.com/"

    @staticmethod
    def _client() -> Any:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise LiveDataUnavailable(
                "The live-data dependency is missing. Install requirements.txt first."
            ) from exc
        return yf

    @staticmethod
    def _as_float(value: Any) -> float | None:
        if value is None or pd.isna(value):
            return None
        return float(value)

    @classmethod
    def get_market_snapshot(
        cls, instruments: Iterable[tuple[str, str, str]]
    ) -> pd.DataFrame:
        """Return a normalized snapshot for ``(symbol, name, category)`` rows."""
        items = list(instruments)
        if not items:
            return pd.DataFrame()

        yf = cls._client()
        symbols = [symbol for symbol, _, _ in items]
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
            raise LiveDataUnavailable("Live market data could not be retrieved.") from exc
        if history is None or history.empty:
            raise LiveDataUnavailable("The provider returned no market data.")

        rows: list[dict[str, Any]] = []
        for symbol, company, category in items:
            try:
                frame = history[symbol] if isinstance(history.columns, pd.MultiIndex) else history
                frame = frame.dropna(subset=["Close"])
                if frame.empty:
                    continue
                latest = frame.iloc[-1]
                previous_close = cls._as_float(frame.iloc[-2]["Close"]) if len(frame) > 1 else None
                price = cls._as_float(latest["Close"])
                if price is None:
                    continue
                change = price - previous_close if previous_close is not None else 0.0
                change_pct = (change / previous_close * 100) if previous_close else 0.0
                rows.append({
                    "Symbol": symbol, "Company": company, "Category": category,
                    "Price": round(price, 2), "Change": round(change, 2),
                    "Change_Pct": round(change_pct, 2), "Market_Cap": None,
                    "Volume": int(latest["Volume"]) if not pd.isna(latest["Volume"]) else None,
                    "Day_High": cls._as_float(latest["High"]),
                    "Day_Low": cls._as_float(latest["Low"]), "High_52w": None,
                    "Low_52w": None, "PE_Ratio": None, "Dividend_Yield": None,
                    "Last_Updated": frame.index[-1], "Data_Source": cls.source_name,
                })
            except (KeyError, IndexError, TypeError):
                continue
        if not rows:
            raise LiveDataUnavailable("The provider returned no usable market rows.")
        return pd.DataFrame(rows)

    @classmethod
    def get_history(cls, symbol: str, days: int) -> pd.DataFrame:
        """Return actual OHLCV history for one symbol."""
        yf = cls._client()
        try:
            frame = yf.Ticker(symbol).history(
                period=f"{max(days, 5)}d", interval="1d", auto_adjust=False
            )
        except Exception as exc:
            raise LiveDataUnavailable(f"History for {symbol} could not be retrieved.") from exc
        if frame is None or frame.empty:
            raise LiveDataUnavailable(f"No history is available for {symbol}.")
        frame = frame.reset_index()
        date_column = "Date" if "Date" in frame.columns else "Datetime"
        frame = frame.rename(columns={date_column: "Date"})
        required = ["Date", "Open", "High", "Low", "Close", "Volume"]
        return frame[[column for column in required if column in frame.columns]].copy()

    @classmethod
    def search_news(cls, company: str, limit: int = 12) -> list[dict[str, Any]]:
        """Return provider news for a company search, without invented URLs."""
        yf = cls._client()
        try:
            results = yf.Search(company, news_count=limit).news or []
        except Exception as exc:
            raise LiveDataUnavailable(f"News for {company} could not be retrieved.") from exc

        articles: list[dict[str, Any]] = []
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
            link = canonical_url.get("url") if isinstance(canonical_url, dict) else canonical_url
            click_through = content.get("clickThroughUrl", {})
            link = link or (click_through.get("url") if isinstance(click_through, dict) else None) or item.get("link")
            published = content.get("pubDate") or item.get("providerPublishTime")
            if isinstance(published, (int, float)):
                published_at = datetime.fromtimestamp(published, tz=timezone.utc)
            else:
                parsed = pd.to_datetime(published, utc=True, errors="coerce")
                published_at = parsed.to_pydatetime() if not pd.isna(parsed) else datetime.now(timezone.utc)
            articles.append({
                "id": str(content.get("id") or item.get("uuid") or f"{company}-{index}-{title}"),
                "title": title, "summary": content.get("summary") or item.get("summary") or title,
                "source": provider_name or cls.source_name, "published_at": published_at,
                "link": link, "company": company, "data_source": cls.source_name,
            })
        return articles
