"""Composition root that wires outer adapters to application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from .application.use_cases import (
    AnalyzeFinancialNewsUseCase,
    GetInstrumentProfileUseCase,
    GetMarketSchedulesUseCase,
    GetMarketSnapshotUseCase,
    GetPriceHistoryUseCase,
    SearchInstrumentsUseCase,
)
from .domain.services import FinancialNewsCategorizer, FinancialSentimentAnalyzer
from .infrastructure.repositories import StaticMarketScheduleRepository
from .infrastructure.services import YahooFinanceService


@dataclass(frozen=True, slots=True)
class ApplicationServices:
    """Use cases made available to Streamlit delivery code."""

    analyze_financial_news: AnalyzeFinancialNewsUseCase
    get_market_schedules: GetMarketSchedulesUseCase
    get_market_snapshot: GetMarketSnapshotUseCase
    get_price_history: GetPriceHistoryUseCase
    get_instrument_profile: GetInstrumentProfileUseCase
    search_instruments: SearchInstrumentsUseCase


def build_application_services() -> ApplicationServices:
    """Create the object graph in the outermost layer of the application."""
    yahoo_finance = YahooFinanceService()
    return ApplicationServices(
        analyze_financial_news=AnalyzeFinancialNewsUseCase(
            news_provider=yahoo_finance,
            sentiment_analyzer=FinancialSentimentAnalyzer(),
            categorizer=FinancialNewsCategorizer(),
        ),
        get_market_schedules=GetMarketSchedulesUseCase(StaticMarketScheduleRepository()),
        get_market_snapshot=GetMarketSnapshotUseCase(yahoo_finance),
        get_price_history=GetPriceHistoryUseCase(yahoo_finance),
        get_instrument_profile=GetInstrumentProfileUseCase(yahoo_finance),
        search_instruments=SearchInstrumentsUseCase(yahoo_finance),
    )
