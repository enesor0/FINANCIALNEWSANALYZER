"""Vercel entrypoint for the Financial News Analyzer HTTP API."""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from financial_news_analyzer.src.application.exceptions import DataProviderUnavailable
from financial_news_analyzer.src.bootstrap import build_application_services
from financial_news_analyzer.src.domain.entities.market_data import MarketInstrument
from financial_news_analyzer.src.domain.services.sentiment_analysis_service import (
    FinancialSentimentAnalyzer,
)


app = FastAPI(
    title="Financial News Analyzer API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

services = build_application_services()
sentiment_explainer = FinancialSentimentAnalyzer()

INSTRUMENTS: dict[str, MarketInstrument] = {
    "AAPL": MarketInstrument("AAPL", "Apple", "Technology"),
    "MSFT": MarketInstrument("MSFT", "Microsoft", "Technology"),
    "NVDA": MarketInstrument("NVDA", "NVIDIA", "Technology"),
    "JPM": MarketInstrument("JPM", "JPMorgan Chase", "Finance"),
    "BAC": MarketInstrument("BAC", "Bank of America", "Finance"),
    "GS": MarketInstrument("GS", "Goldman Sachs", "Finance"),
    "JNJ": MarketInstrument("JNJ", "Johnson & Johnson", "Healthcare"),
    "PFE": MarketInstrument("PFE", "Pfizer", "Healthcare"),
    "UNH": MarketInstrument("UNH", "UnitedHealth", "Healthcare"),
    "XOM": MarketInstrument("XOM", "ExxonMobil", "Energy"),
    "CVX": MarketInstrument("CVX", "Chevron", "Energy"),
    "COP": MarketInstrument("COP", "ConocoPhillips", "Energy"),
    "WMT": MarketInstrument("WMT", "Walmart", "Consumer"),
    "TGT": MarketInstrument("TGT", "Target", "Consumer"),
    "HD": MarketInstrument("HD", "Home Depot", "Consumer"),
    "TSLA": MarketInstrument("TSLA", "Tesla", "Automotive"),
    "F": MarketInstrument("F", "Ford", "Automotive"),
    "GM": MarketInstrument("GM", "General Motors", "Automotive"),
    "AMT": MarketInstrument("AMT", "American Tower", "Real Estate"),
    "PLD": MarketInstrument("PLD", "Prologis", "Real Estate"),
    "CCI": MarketInstrument("CCI", "Crown Castle", "Real Estate"),
    "BA": MarketInstrument("BA", "Boeing", "Industrial"),
    "LMT": MarketInstrument("LMT", "Lockheed Martin", "Industrial"),
    "RTX": MarketInstrument("RTX", "RTX", "Industrial"),
}

_symbol_pattern = re.compile(r"^[A-Z0-9.^=-]{1,15}$")
_cache: dict[str, tuple[float, Any]] = {}


def _cached(key: str, ttl_seconds: int, loader: Callable[[], Any]) -> Any:
    cached = _cache.get(key)
    now = time.monotonic()
    if cached and now - cached[0] < ttl_seconds:
        return cached[1]
    value = loader()
    _cache[key] = (now, value)
    return value


@app.exception_handler(DataProviderUnavailable)
async def data_provider_error(_request: Any, exc: DataProviderUnavailable) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def validation_error(_request: Any, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/api")
def api_root() -> dict[str, str]:
    return {"name": "Financial News Analyzer API", "status": "ok"}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/instruments")
def instruments() -> list[dict[str, str]]:
    return [
        {"symbol": item.symbol, "name": item.name, "category": item.category}
        for item in INSTRUMENTS.values()
    ]


@app.get("/api/search")
def search(
    q: str = Query(min_length=1, max_length=80),
    limit: int = Query(default=12, ge=1, le=20),
) -> dict[str, Any]:
    results = _cached(
        f"search:{q.strip().casefold()}:{limit}",
        900,
        lambda: services.search_instruments.execute(q, limit),
    )
    return {
        "query": q.strip(),
        "results": [
            {
                "symbol": item.symbol,
                "name": item.name,
                "exchange": item.exchange,
                "quoteType": item.quote_type,
                "sector": item.sector,
                "industry": item.industry,
            }
            for item in results
        ],
    }


@app.get("/api/market")
def market(
    symbols: str = Query(
        default="AAPL,MSFT,NVDA,JPM,JNJ,XOM,TSLA,BA",
        max_length=160,
    ),
) -> dict[str, Any]:
    requested_symbols = list(dict.fromkeys(value.strip().upper() for value in symbols.split(",")))
    requested_symbols = [value for value in requested_symbols if value]
    if not requested_symbols or len(requested_symbols) > 12:
        raise HTTPException(status_code=400, detail="Request between 1 and 12 symbols.")
    invalid = [value for value in requested_symbols if not _symbol_pattern.fullmatch(value)]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Unsupported symbol format: {', '.join(invalid)}")

    snapshot = _cached(
        f"market:{','.join(requested_symbols)}",
        300,
        lambda: services.get_market_snapshot.execute(
            INSTRUMENTS.get(value, MarketInstrument(value, value, "Discovered"))
            for value in requested_symbols
        ),
    )
    return {
        "provider": "Yahoo Finance via yfinance",
        "quotes": [
            {
                "symbol": quote.instrument.symbol,
                "name": quote.instrument.name,
                "category": quote.instrument.category,
                "price": round(quote.price, 4),
                "previousClose": (
                    round(quote.previous_close, 4) if quote.previous_close is not None else None
                ),
                "change": round(quote.change, 4),
                "changePercent": round(quote.change_percent, 4),
                "volume": quote.volume,
                "dayHigh": quote.day_high,
                "dayLow": quote.day_low,
                "observedAt": quote.observed_at.isoformat(),
            }
            for quote in snapshot.quotes
        ],
    }


@app.get("/api/profile/{symbol}")
def profile(symbol: str) -> dict[str, Any]:
    normalized_symbol = symbol.strip().upper()
    if not _symbol_pattern.fullmatch(normalized_symbol):
        raise HTTPException(status_code=400, detail="Unsupported symbol format.")
    item = _cached(
        f"profile:{normalized_symbol}",
        300,
        lambda: services.get_instrument_profile.execute(normalized_symbol),
    )
    return {
        "symbol": item.symbol,
        "name": item.name,
        "shortName": item.short_name,
        "quoteType": item.quote_type,
        "currency": item.currency,
        "exchange": item.exchange,
        "sector": item.sector,
        "industry": item.industry,
        "price": item.price,
        "previousClose": item.previous_close,
        "open": item.open_price,
        "dayHigh": item.day_high,
        "dayLow": item.day_low,
        "volume": item.volume,
        "marketCap": item.market_cap,
        "trailingPE": item.trailing_pe,
        "forwardPE": item.forward_pe,
        "dividendYield": item.dividend_yield,
        "fiftyTwoWeekHigh": item.fifty_two_week_high,
        "fiftyTwoWeekLow": item.fifty_two_week_low,
        "averageVolume": item.average_volume,
        "beta": item.beta,
        "website": item.website,
        "description": item.description,
        "change": item.change,
        "changePercent": item.change_percent,
    }


@app.get("/api/history/{symbol}")
def history(
    symbol: str,
    days: int = Query(default=90, ge=5, le=1825),
) -> dict[str, Any]:
    normalized_symbol = symbol.strip().upper()
    if not _symbol_pattern.fullmatch(normalized_symbol):
        raise HTTPException(status_code=400, detail="Unsupported symbol format.")
    result = _cached(
        f"history:{normalized_symbol}:{days}",
        300,
        lambda: services.get_price_history.execute(normalized_symbol, days),
    )
    return {
        "symbol": result.symbol,
        "adjusted": True,
        "bars": [
            {
                "date": bar.observed_at.isoformat(),
                "open": round(bar.open_price, 4),
                "high": round(bar.high_price, 4),
                "low": round(bar.low_price, 4),
                "close": round(bar.close_price, 4),
                "volume": bar.volume,
            }
            for bar in result.bars
        ],
    }


@app.get("/api/news")
def news(
    companies: str = Query(default="Apple,Microsoft,NVIDIA", max_length=400),
    limit: int = Query(default=8, ge=1, le=12),
) -> dict[str, Any]:
    requested_companies = list(dict.fromkeys(value.strip() for value in companies.split(",")))
    requested_companies = [value for value in requested_companies if value]
    if not requested_companies or len(requested_companies) > 8:
        raise HTTPException(status_code=400, detail="Request between 1 and 8 companies or topics.")
    if any(len(value) > 80 for value in requested_companies):
        raise HTTPException(status_code=400, detail="Each search term must be 80 characters or fewer.")

    analyses = _cached(
        f"news:{','.join(requested_companies)}:{limit}",
        300,
        lambda: services.analyze_financial_news.execute(requested_companies, limit),
    )
    articles = []
    for analysis in analyses:
        evidence = sentiment_explainer.keyword_evidence(analysis.article.text_for_analysis)
        articles.append(
            {
                "id": analysis.article.id,
                "title": analysis.article.title,
                "summary": analysis.article.summary,
                "source": analysis.article.source,
                "publishedAt": analysis.article.published_at.isoformat(),
                "company": analysis.article.company,
                "url": analysis.article.url,
                "category": analysis.category.value,
                "sentiment": analysis.sentiment.sentiment_type.value,
                "score": analysis.sentiment.score,
                "confidence": analysis.sentiment.confidence,
                "evidence": evidence,
            }
        )

    sentiment_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    company_counts: dict[str, int] = {}
    for article in articles:
        sentiment_counts[article["sentiment"]] = sentiment_counts.get(article["sentiment"], 0) + 1
        category_counts[article["category"]] = category_counts.get(article["category"], 0) + 1
        company_counts[article["company"]] = company_counts.get(article["company"], 0) + 1
    average_score = (
        round(sum(float(article["score"]) for article in articles) / len(articles), 4)
        if articles
        else 0.0
    )
    average_confidence = (
        round(sum(float(article["confidence"]) for article in articles) / len(articles), 4)
        if articles
        else 0.0
    )

    return {
        "provider": "Yahoo Finance via yfinance",
        "queryTerms": requested_companies,
        "analysis": {
            "totalArticles": len(articles),
            "averageScore": average_score,
            "averageConfidence": average_confidence,
            "sentimentCounts": sentiment_counts,
            "categoryCounts": category_counts,
            "companyCounts": company_counts,
        },
        "articles": articles,
    }


@app.get("/api/schedules")
def schedules() -> list[dict[str, Any]]:
    markets = services.get_market_schedules.execute()
    return [
        {
            "code": market.code,
            "name": market.name,
            "country": market.country_code,
            "flag": market.country_flag,
            "timezone": market.timezone,
            "region": market.region.value,
            "currency": market.currency,
            "openTime": market.open_time.strftime("%H:%M"),
            "closeTime": market.close_time.strftime("%H:%M"),
            "status": market.status_at().value,
            "localTime": market.local_time_at().isoformat(),
        }
        for market in markets
    ]
