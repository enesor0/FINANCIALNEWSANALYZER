"""Streamlit adapter for displaying global financial-market schedules."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

import streamlit as st

from ...application.use_cases.get_market_schedules import GetMarketSchedulesUseCase
from ...domain.entities.market import Market, MarketRegion, MarketStatus


class WorldClockComponent:
    """Render market schedules supplied by an application use case."""

    _region_labels = {
        MarketRegion.AMERICAS: "🌎 Americas",
        MarketRegion.EUROPE: "🌍 Europe",
        MarketRegion.ASIA_PACIFIC: "🌏 Asia-Pacific",
        MarketRegion.MENA_AFRICA: "🌍 MENA & Africa",
    }
    _status_presentation = {
        MarketStatus.OPEN: ("🟢", "#28a745"),
        MarketStatus.CLOSED: ("🔴", "#dc3545"),
    }

    def __init__(self, get_market_schedules: GetMarketSchedulesUseCase) -> None:
        self._get_market_schedules = get_market_schedules

    def render(self, container: Any = None) -> None:
        """Render the market clock in ``container`` or the Streamlit sidebar."""
        target = container or st.sidebar
        target.markdown("### 🌍 Global Financial Markets")
        target.caption("Weekday schedules only; exchange holidays and early closes are not included.")
        target.markdown("---")
        for region_name, markets in self._group_markets_by_region().items():
            with target.expander(f"{region_name} ({len(markets)} markets)") as region_container:
                for market in markets:
                    self._render_market_card(market, region_container)

    def get_market_by_code(self, code: str) -> Market | None:
        """Find a configured market by exchange code."""
        return next(
            (market for market in self._markets() if market.code.casefold() == code.casefold()),
            None,
        )

    def get_open_markets(self) -> list[Market]:
        """Return the markets that are open according to their domain schedule."""
        return [market for market in self._markets() if market.status_at() is MarketStatus.OPEN]

    def get_markets_summary(self) -> dict[str, int | float]:
        """Return a small summary for other presentation components."""
        markets = self._markets()
        open_count = sum(market.status_at() is MarketStatus.OPEN for market in markets)
        total_count = len(markets)
        return {
            "total_markets": total_count,
            "open_markets": open_count,
            "closed_markets": total_count - open_count,
            "open_percentage": open_count / total_count * 100 if total_count else 0,
        }

    def _markets(self) -> tuple[Market, ...]:
        return self._get_market_schedules.execute()

    def _group_markets_by_region(self) -> dict[str, list[Market]]:
        grouped = {label: [] for label in self._region_labels.values()}
        for market in self._markets():
            grouped[self._region_labels[market.region]].append(market)
        return grouped

    def _render_market_card(self, market: Market, container: Any) -> None:
        local_now = market.local_time_at()
        status = market.status_at(local_now)
        emoji, color = self._status_presentation[status]
        countdown = self._countdown_text(market, status, local_now)
        card_html = (
            f'<div style="padding:8px;margin:4px 0;border-left:3px solid {color};'
            f'background-color:rgba(255,255,255,0.05);border-radius:5px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<div><strong style="font-size:0.9em;">{market.country_flag} {market.name}</strong><br>'
            f'<span style="font-size:1.1em;font-weight:bold;">{local_now:%H:%M}</span>'
            f'<span style="font-size:0.8em;color:#888;"> ({local_now:%m/%d})</span></div>'
            f'<div style="text-align:right;"><span style="color:{color};font-weight:bold;font-size:0.8em;">'
            f'{emoji} {status.value.upper()}</span><br><span style="font-size:0.7em;color:#999;">'
            f'{market.open_time:%H:%M} - {market.close_time:%H:%M}</span></div></div>{countdown}</div>'
        )
        container.markdown(card_html, unsafe_allow_html=True)

    @staticmethod
    def _countdown_text(market: Market, status: MarketStatus, local_now: Any) -> str:
        duration = (
            market.time_until_open_at(local_now)
            if status is MarketStatus.CLOSED
            else market.time_until_close_at(local_now)
        )
        if duration is None:
            return ""
        label = "Opens" if status is MarketStatus.CLOSED else "Closes"
        return (
            '<div style="margin-top:4px;font-size:0.7em;color:#999;">'
            f'{label} in: {WorldClockComponent._format_duration(duration)}</div>'
        )

    @staticmethod
    def _format_duration(duration: timedelta) -> str:
        total_minutes = max(0, int(duration.total_seconds() // 60))
        days, remaining_minutes = divmod(total_minutes, 24 * 60)
        hours, minutes = divmod(remaining_minutes, 60)
        return f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
