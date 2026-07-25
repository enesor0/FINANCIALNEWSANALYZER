"""A polished NiceGUI alternative to the Streamlit presentation layer.

Run from the repository root with:
    python financial_news_analyzer/nicegui_app.py

The existing Streamlit application remains untouched so either interface can be
used while the product direction is evaluated.
"""

from __future__ import annotations

import sys
import importlib.util
import os
import pkgutil
from datetime import datetime
from functools import lru_cache
from html import escape
from pathlib import Path
from typing import Callable

# Python 3.14 removed ``pkgutil.find_loader``. NiceGUI 2.x's optional asset
# builder still reads it during import, so restore the equivalent lookup until
# its dependency updates. Earlier Python versions use their native function.
if not hasattr(pkgutil, "find_loader"):
    pkgutil.find_loader = lambda name: importlib.util.find_spec(name)  # type: ignore[attr-defined]

import plotly.graph_objects as go
from nicegui import run, ui


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from financial_news_analyzer.src.domain.entities.market_data import MarketInstrument, MarketQuote, PriceBar
from financial_news_analyzer.src.domain.services.sentiment_analysis_service import FinancialSentimentAnalyzer
from financial_news_analyzer.src.infrastructure.services.yahoo_finance_service import (
    LiveDataUnavailable,
    YahooFinanceService,
)
from financial_news_analyzer.src.presentation.support import build_support_mailto, validate_support_request


# Palette sampled from the supplied reference image.
NAVY = "#103657"
NAVY_DEEP = "#0B2B47"
CREAM = "#F4E4C4"
CREAM_LIGHT = "#FBF4E6"
SAGE = "#CFD0BD"
SAGE_DARK = "#AEB2A0"
BROWN = "#94613C"
BROWN_DARK = "#754727"
INK = "#19324A"
MUTED = "#617083"
POSITIVE = "#4E8067"
NEGATIVE = "#B2564B"

INSTRUMENTS = (
    MarketInstrument("AAPL", "Apple", "Technology"),
    MarketInstrument("MSFT", "Microsoft", "Technology"),
    MarketInstrument("NVDA", "NVIDIA", "Technology"),
    MarketInstrument("AMZN", "Amazon", "Consumer"),
    MarketInstrument("TSLA", "Tesla", "Automotive"),
    MarketInstrument("JPM", "JPMorgan Chase", "Finance"),
    MarketInstrument("KO", "Coca-Cola", "Consumer"),
    MarketInstrument("GARAN.IS", "Garanti BBVA", "Borsa Istanbul"),
)
INSTRUMENTS_BY_SYMBOL = {instrument.symbol: instrument for instrument in INSTRUMENTS}


HEAD_HTML = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap" rel="stylesheet">
    <meta name="theme-color" content="#103657">
    """

THEME_CSS = f"""
    :root {{
        --navy: {NAVY};
        --navy-deep: {NAVY_DEEP};
        --cream: {CREAM};
        --cream-light: {CREAM_LIGHT};
        --sage: {SAGE};
        --sage-dark: {SAGE_DARK};
        --brown: {BROWN};
        --brown-dark: {BROWN_DARK};
        --ink: {INK};
        --muted: {MUTED};
        --positive: {POSITIVE};
        --negative: {NEGATIVE};
    }}
    body {{
        background: var(--cream-light) !important;
        color: var(--ink);
        font-family: 'DM Sans', Arial, sans-serif;
    }}
    .q-page-container, .q-page {{ background: var(--cream-light); }}
    .q-layout {{ min-height: 100vh; }}
    .app-header {{
        background: rgba(16, 54, 87, .97) !important;
        border-bottom: 1px solid rgba(244, 228, 196, .2);
        box-shadow: 0 4px 20px rgba(11, 43, 71, .16);
    }}
    .brand-name {{
        color: var(--cream-light);
        font-family: 'Fraunces', Georgia, serif;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: -.02em;
    }}
    .brand-mark {{
        width: 2rem; height: 2rem; border-radius: .65rem; display: inline-flex;
        align-items: center; justify-content: center; background: var(--cream);
        color: var(--navy); font-family: 'Fraunces', Georgia, serif; font-weight: 700;
    }}
    .nav-link {{ color: rgba(251, 244, 230, .75) !important; border-radius: .5rem; font-weight: 600; }}
    .nav-link:hover, .nav-link.active {{ color: var(--cream-light) !important; background: rgba(244, 228, 196, .14) !important; }}
    .mobile-nav-button {{ color: var(--cream-light) !important; }}
    .app-shell {{ width: min(1180px, calc(100% - 2.5rem)); margin: 0 auto; padding: 3.2rem 0 4rem; gap: 1.5rem; }}
    .eyebrow {{ color: var(--brown); font-size: .72rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; }}
    .hero {{
        position: relative; overflow: hidden; padding: clamp(2rem, 5vw, 4.5rem);
        border-radius: 1.45rem; background: var(--navy); color: var(--cream-light);
        box-shadow: 0 18px 44px rgba(16, 54, 87, .18);
    }}
    .hero::after {{ content: ''; position: absolute; width: 23rem; height: 23rem; right: -9rem; top: -12rem; border-radius: 50%; background: rgba(207, 208, 189, .14); }}
    .hero-title {{ position: relative; max-width: 47rem; margin: .65rem 0 1rem; color: var(--cream-light); font-family: 'Fraunces', Georgia, serif; font-size: clamp(2.2rem, 5vw, 4.25rem); font-weight: 700; line-height: 1.02; letter-spacing: -.045em; }}
    .hero-copy {{ position: relative; max-width: 39rem; color: rgba(251, 244, 230, .78); font-size: 1.05rem; line-height: 1.65; }}
    .section-title {{ color: var(--navy); font-family: 'Fraunces', Georgia, serif; font-size: clamp(1.55rem, 3vw, 2.15rem); font-weight: 700; letter-spacing: -.03em; }}
    .section-copy {{ color: var(--muted); max-width: 42rem; line-height: 1.6; }}
    .surface {{ background: #fffaf0; border: 1px solid rgba(16, 54, 87, .1); border-radius: 1rem; box-shadow: 0 8px 24px rgba(16, 54, 87, .06); }}
    .soft-surface {{ background: rgba(207, 208, 189, .56); border: 1px solid rgba(16, 54, 87, .1); border-radius: 1rem; }}
    .metric-card {{ min-height: 9.5rem; padding: 1.25rem; }}
    .metric-label {{ color: var(--muted); font-size: .83rem; font-weight: 600; }}
    .metric-value {{ color: var(--navy); font-family: 'Fraunces', Georgia, serif; font-size: 2.15rem; font-weight: 700; letter-spacing: -.04em; }}
    .metric-note {{ color: var(--muted); font-size: .8rem; }}
    .workspace-card {{ min-height: 16rem; padding: 1.5rem; transition: transform .2s ease, box-shadow .2s ease; }}
    .workspace-card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 30px rgba(16, 54, 87, .12); }}
    .workspace-icon {{ width: 2.7rem; height: 2.7rem; display: grid; place-items: center; border-radius: .75rem; background: var(--sage); color: var(--navy); }}
    .card-title {{ color: var(--navy); font-family: 'Fraunces', Georgia, serif; font-size: 1.35rem; font-weight: 700; }}
    .card-copy {{ color: var(--muted); line-height: 1.55; }}
    .primary-action {{ background: var(--brown) !important; color: #fffaf0 !important; border-radius: .6rem !important; font-weight: 700 !important; box-shadow: none !important; }}
    .primary-action:hover {{ background: var(--brown-dark) !important; }}
    .secondary-action {{ border: 1px solid rgba(16, 54, 87, .26) !important; color: var(--navy) !important; background: transparent !important; border-radius: .6rem !important; font-weight: 700 !important; }}
    .secondary-action:hover {{ background: rgba(207, 208, 189, .45) !important; }}
    .tag {{ color: var(--navy); background: rgba(207, 208, 189, .72); border-radius: 999px; padding: .3rem .65rem; font-size: .75rem; font-weight: 700; }}
    .stat-line {{ padding: .8rem 0; border-bottom: 1px solid rgba(16, 54, 87, .1); }}
    .stat-line:last-child {{ border-bottom: 0; }}
    .quote-card {{ padding: 1.15rem; min-height: 9.5rem; }}
    .quote-symbol {{ color: var(--navy); font-weight: 700; font-size: 1rem; }}
    .quote-name {{ color: var(--muted); font-size: .79rem; }}
    .quote-price {{ color: var(--navy); font-family: 'Fraunces', Georgia, serif; font-size: 1.7rem; font-weight: 700; }}
    .positive {{ color: var(--positive) !important; }}
    .negative {{ color: var(--negative) !important; }}
    .neutral {{ color: var(--muted) !important; }}
    .sentiment-chip {{ display: inline-flex; border-radius: 999px; padding: .25rem .55rem; font-size: .74rem; font-weight: 700; }}
    .sentiment-chip.positive {{ background: rgba(78, 128, 103, .12); }}
    .sentiment-chip.negative {{ background: rgba(178, 86, 75, .11); }}
    .sentiment-chip.neutral {{ background: rgba(97, 112, 131, .11); }}
    .article-card {{ padding: 1.1rem 1.2rem; border-left: 4px solid var(--sage-dark); }}
    .article-card.positive {{ border-left-color: var(--positive); }}
    .article-card.negative {{ border-left-color: var(--negative); }}
    .article-title {{ color: var(--navy); font-size: 1rem; font-weight: 700; line-height: 1.45; }}
    .article-meta {{ color: var(--muted); font-size: .78rem; }}
    .chart-shell {{ padding: .65rem; min-height: 27rem; }}
    .data-source {{ color: var(--muted); font-size: .78rem; }}
    .footer {{ color: rgba(251, 244, 230, .72); background: var(--navy-deep); padding: 2.2rem max(1.25rem, calc((100% - 1180px) / 2)); }}
    .q-field__control {{ background: #fffaf0 !important; border-radius: .65rem !important; }}
    .q-field--outlined .q-field__control:before {{ border-color: rgba(16, 54, 87, .2) !important; }}
    .q-field__label, .q-field input, .q-field textarea {{ color: var(--ink) !important; }}
    .q-table__container {{ border: 1px solid rgba(16, 54, 87, .12); border-radius: .8rem; overflow: hidden; box-shadow: none; }}
    .q-table thead tr {{ background: var(--sage); }}
    .q-table tbody td {{ color: var(--ink); }}
    @media (max-width: 700px) {{
        .app-shell {{ width: min(100% - 1.5rem, 1180px); padding-top: 1.6rem; }}
        .hero {{ border-radius: 1.1rem; }}
        .desktop-nav {{ display: none !important; }}
    }}
    @media (min-width: 701px) {{ .mobile-nav-button {{ display: none !important; }} }}
    """


def apply_theme() -> None:
    """Attach the shared font and palette inside the current NiceGUI page."""
    ui.add_head_html(HEAD_HTML)
    ui.add_css(THEME_CSS)


def currency(value: float | None) -> str:
    """Return a compact presentation-safe price."""
    return "—" if value is None else f"${value:,.2f}"


def compact_volume(value: int | None) -> str:
    """Format volumes without noisy long numbers."""
    if value is None:
        return "—"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def sentiment_label(score: float) -> tuple[str, str]:
    """Map explainable scores to compact UI labels and palette classes."""
    if score > 0.2:
        return "Olumlu", "positive"
    if score < -0.2:
        return "Olumsuz", "negative"
    return "Nötr", "neutral"


@lru_cache(maxsize=1)
def get_snapshot() -> tuple[MarketQuote, ...]:
    """Retrieve a coherent provider-backed snapshot once per process window."""
    return YahooFinanceService().get_market_snapshot(INSTRUMENTS)


@lru_cache(maxsize=16)
def get_history(symbol: str, days: int) -> tuple[PriceBar, ...]:
    """Retrieve daily OHLCV history for the requested instrument."""
    return YahooFinanceService().get_history(symbol, days)


def clear_market_cache() -> None:
    """Offer an explicit refresh without presenting cached data as real time."""
    get_snapshot.cache_clear()
    get_history.cache_clear()


def nav_item(label: str, target: str, active: str) -> None:
    classes = "nav-link active" if active == target else "nav-link"
    ui.link(label, target).classes(classes).style("padding: .5rem .7rem; text-decoration: none;")


def header(active: str) -> None:
    """Render the shared application header and responsive navigation."""
    with ui.header().classes("app-header items-center").style("height: 4.6rem; padding: 0 max(1.25rem, calc((100% - 1180px) / 2));"):
        with ui.row().classes("items-center no-wrap").style("gap: .7rem;"):
            ui.label("F").classes("brand-mark").props("aria-label=Financial News Analyzer")
            ui.label("Financial News Analyzer").classes("brand-name")
        ui.space()
        with ui.row().classes("desktop-nav items-center").style("gap: .25rem;"):
            nav_item("Genel Bakış", "/", active)
            nav_item("Piyasa", "/market", active)
            nav_item("Haber Analizi", "/news", active)
            nav_item("Destek", "/support", active)
        with ui.button(icon="menu").props("flat round aria-label=Menüyü aç").classes("mobile-nav-button") as menu_button:
            with ui.menu().props("auto-close").style("min-width: 13rem; background: #fffaf0;"):
                for label, target in (("Genel Bakış", "/"), ("Piyasa", "/market"), ("Haber Analizi", "/news"), ("Destek", "/support")):
                    ui.menu_item(label, on_click=lambda path=target: ui.navigate.to(path))


def footer() -> None:
    with ui.element("footer").classes("footer w-full"):
        with ui.row().classes("items-center justify-between w-full").style("gap: 1rem;"):
            ui.label("Financial News Analyzer").style("font-family: 'Fraunces', Georgia, serif; color: #fbf4e6; font-size: 1.1rem;")
            ui.label("Yahoo Finance verileri eğitim ve araştırma amaçlıdır; yatırım tavsiyesi değildir.").style("font-size: .78rem;")


def page_intro(eyebrow: str, title: str, copy: str, tags: tuple[str, ...] = ()) -> None:
    with ui.element("section").classes("hero w-full"):
        ui.label(eyebrow).classes("eyebrow").style(f"color: {CREAM};")
        ui.html(f'<h1 class="hero-title">{escape(title)}</h1>')
        ui.label(copy).classes("hero-copy")
        if tags:
            with ui.row().classes("relative").style("gap: .5rem; margin-top: 1.5rem;"):
                for tag in tags:
                    ui.label(tag).classes("tag").style(f"background: rgba(244, 228, 196, .16); color: {CREAM_LIGHT};")


def section_heading(title: str, copy: str) -> None:
    with ui.column().classes("w-full").style("gap: .25rem;"):
        ui.label(title).classes("section-title")
        ui.label(copy).classes("section-copy")


def workspace_card(icon: str, title: str, copy: str, tags: tuple[str, ...], target: str, action: str) -> None:
    with ui.column().classes("surface workspace-card").style("gap: .95rem; flex: 1 1 16rem;"):
        ui.icon(icon).classes("workspace-icon").style("font-size: 1.35rem;")
        ui.label(title).classes("card-title")
        ui.label(copy).classes("card-copy")
        with ui.row().style("gap: .35rem; flex-wrap: wrap;"):
            for tag in tags:
                ui.label(tag).classes("tag")
        ui.space()
        ui.button(action, icon="arrow_forward", on_click=lambda: ui.navigate.to(target)).props("no-caps").classes("secondary-action")


@ui.page("/")
def home_page() -> None:
    apply_theme()
    header("/")
    with ui.column().classes("app-shell"):
        page_intro(
            "Araştırma çalışma alanı",
            "Piyasa gürültüsünü değil, bağlamı görün.",
            "Güncel fiyatlar, kaynak bağlantılı haberler ve açıklanabilir duygu sinyalleri; sakin, odaklı bir araştırma akışında bir arada.",
            ("Yahoo Finance veri sağlayıcısı", "Açıklanabilir sinyal", "Araştırma odaklı"),
        )
        with ui.row().classes("w-full").style("gap: 1rem; flex-wrap: wrap;"):
            with ui.column().classes("soft-surface metric-card").style("flex: 1 1 12rem; gap: .55rem;"):
                ui.label("Canlı fiyat verisi").classes("metric-label")
                ui.label("Günlük kapanış").classes("metric-value")
                ui.label("Yahoo Finance üzerinden alınır").classes("metric-note")
            with ui.column().classes("soft-surface metric-card").style("flex: 1 1 12rem; gap: .55rem;"):
                ui.label("Haber içgörüsü").classes("metric-label")
                ui.label("Kaynak bağlantılı").classes("metric-value").style("font-size: 1.7rem;")
                ui.label("Her haber doğrulanabilir kaynağıyla sunulur").classes("metric-note")
            with ui.column().classes("soft-surface metric-card").style("flex: 1 1 12rem; gap: .55rem;"):
                ui.label("Duygu yaklaşımı").classes("metric-label")
                ui.label("Şeffaf").classes("metric-value")
                ui.label("Anahtar kelime tabanlı ve açıklanabilir").classes("metric-note")

        section_heading("İhtiyacınız olan çalışma alanını seçin", "Her ekran tek bir göreve odaklanır; karmaşık paneller ve anlamsız metrikler yoktur.")
        with ui.row().classes("w-full").style("gap: 1rem; flex-wrap: wrap;"):
            workspace_card("show_chart", "Piyasa verileri", "Seçili enstrümanların son günlük kapanışlarını, hacmini ve fiyat geçmişini inceleyin.", ("Güncel kapanış", "Etkileşimli grafik"), "/market", "Piyasayı aç")
            workspace_card("newspaper", "Haber analizi", "Şirket haberlerini kaynaklarıyla okuyun; duygu etiketlerini nasıl üretildiği belli bir yöntemle görün.", ("Bağlantılı haber", "Duygu sinyali"), "/news", "Haberleri aç")
            workspace_card("support_agent", "Destek", "Veri kaynağı, uygulama kullanımı veya bir sorun hakkında doğrudan iletişime geçin.", ("E-posta taslağı", "Şeffaf süreç"), "/support", "Desteğe git")

        with ui.row().classes("surface w-full items-stretch").style("padding: 1.4rem; gap: 1.5rem; flex-wrap: wrap;"):
            with ui.column().style("flex: 1 1 20rem; gap: .35rem;"):
                ui.label("Veriye yaklaşımımız").classes("section-title").style("font-size: 1.45rem;")
                ui.label("Bu uygulama, veriyi tahmin ya da yatırım önerisi olarak sunmaz. Mevcut günlük kapanışları ve sağlayıcının bağlantılı içeriklerini araştırma için düzenler.").classes("section-copy")
            with ui.column().style("flex: 1 1 18rem; gap: 0;"):
                for heading, detail in (("1. Kaynağı seçin", "Piyasa veya haber çalışma alanını açın."), ("2. Canlı veriyi yükleyin", "Sorgu yalnızca talep ettiğinizde başlar."), ("3. Bağlamı değerlendirin", "Fiyat ve haber bağlantılarını birlikte inceleyin.")):
                    with ui.row().classes("stat-line items-center"):
                        ui.label(heading).style(f"color: {NAVY}; font-weight: 700;")
                        ui.space()
                        ui.label(detail).classes("metric-note").style("max-width: 14rem; text-align: right;")
    footer()


def quote_card(quote: MarketQuote) -> None:
    change = quote.change_percent
    change_class = "positive" if change > 0 else "negative" if change < 0 else "neutral"
    change_prefix = "+" if change > 0 else ""
    with ui.column().classes("surface quote-card").style("flex: 1 1 13rem; gap: .35rem;"):
        with ui.row().classes("items-start w-full"):
            with ui.column().style("gap: 0;"):
                ui.label(quote.instrument.symbol).classes("quote-symbol")
                ui.label(quote.instrument.name).classes("quote-name")
            ui.space()
            ui.label(quote.instrument.category).classes("tag").style("font-size: .67rem;")
        ui.label(currency(quote.price)).classes("quote-price")
        with ui.row().classes("items-center").style("gap: .45rem;"):
            ui.icon("trending_up" if change >= 0 else "trending_down").classes(change_class).style("font-size: 1rem;")
            ui.label(f"{change_prefix}{change:.2f}%").classes(change_class).style("font-size: .86rem; font-weight: 700;")
            ui.label(f"Hacim {compact_volume(quote.volume)}").classes("metric-note")


def price_figure(bars: tuple[PriceBar, ...], symbol: str) -> go.Figure:
    """Create a restrained chart using the supplied palette."""
    dates = [bar.observed_at for bar in bars]
    closes = [bar.close_price for bar in bars]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=closes,
        mode="lines",
        name="Kapanış",
        line={"color": NAVY, "width": 3},
        fill="tozeroy",
        fillcolor="rgba(207, 208, 189, .55)",
        hovertemplate="%{x|%d %b %Y}<br><b>$%{y:,.2f}</b><extra></extra>",
    ))
    fig.update_layout(
        title={"text": f"{symbol} günlük kapanış", "font": {"family": "DM Sans", "color": NAVY, "size": 17}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 15, "r": 15, "t": 55, "b": 15},
        font={"family": "DM Sans", "color": MUTED},
        hoverlabel={"bgcolor": NAVY, "font": {"color": CREAM_LIGHT}},
        showlegend=False,
        xaxis={"showgrid": False, "zeroline": False, "fixedrange": False},
        yaxis={"showgrid": True, "gridcolor": "rgba(16, 54, 87, .1)", "zeroline": False, "tickprefix": "$", "fixedrange": False},
    )
    return fig


def empty_market_state(container: ui.column) -> None:
    container.clear()
    with container:
        with ui.column().classes("soft-surface w-full items-center").style("padding: 3rem 1.5rem; gap: .7rem;"):
            ui.icon("query_stats").style(f"color: {NAVY}; font-size: 2.4rem;")
            ui.label("Canlı veriler henüz yüklenmedi").classes("card-title")
            ui.label("Seçili piyasa görünümünü oluşturmak için “Verileri yenile” düğmesine basın.").classes("section-copy").style("text-align: center;")


@ui.page("/market")
def market_page() -> None:
    apply_theme()
    header("/market")
    with ui.column().classes("app-shell"):
        page_intro(
            "Piyasa çalışma alanı",
            "Fiyatları bir bakışta, bağlamıyla değerlendirin.",
            "Güncel olarak erişilebilen günlük kapanışları, hacmi ve tek bir enstrümanın fiyat geçmişini sade bir görünümde inceleyin.",
            ("Günlük kapanış", "Yahoo Finance", "Yatırım tavsiyesi değildir"),
        )
        with ui.row().classes("surface w-full items-end").style("padding: 1rem; gap: .75rem; flex-wrap: wrap;"):
            ui.icon("monitoring").style(f"color: {BROWN}; font-size: 1.55rem;")
            with ui.column().style("gap: .05rem; flex: 1 1 18rem;"):
                ui.label("Piyasa özeti").classes("card-title").style("font-size: 1.15rem;")
                ui.label("Veriler isteğiniz üzerine Yahoo Finance üzerinden alınır; en son günlük kapanışı temsil eder.").classes("metric-note")
            load_button = ui.button("Verileri yenile", icon="refresh").props("no-caps").classes("primary-action")

        quote_container = ui.column().classes("w-full").style("gap: .9rem;")
        empty_market_state(quote_container)
        with ui.column().classes("surface w-full").style("padding: 1.25rem; gap: 1rem;"):
            with ui.row().classes("w-full items-end").style("gap: .75rem; flex-wrap: wrap;"):
                with ui.column().style("gap: .1rem; flex: 1 1 16rem;"):
                    ui.label("Fiyat geçmişi").classes("card-title").style("font-size: 1.2rem;")
                    ui.label("Bir enstrüman seçin ve günlük kapanış grafiğini yükleyin.").classes("metric-note")
                symbol_select = ui.select({symbol: f"{instrument.name} ({symbol})" for symbol, instrument in INSTRUMENTS_BY_SYMBOL.items()}, value="AAPL", label="Enstrüman").style("min-width: 14rem;")
                days_select = ui.select({30: "30 gün", 90: "90 gün", 180: "180 gün"}, value=90, label="Dönem").style("min-width: 8rem;")
                history_button = ui.button("Grafiği yükle", icon="show_chart").props("no-caps").classes("secondary-action")
            chart_container = ui.column().classes("chart-shell w-full")
            with chart_container:
                ui.label("Grafik, seçiminizden sonra burada görüntülenecek.").classes("data-source").style("padding: 1rem;")

        async def load_snapshot() -> None:
            load_button.disable()
            load_button.props("loading")
            try:
                clear_market_cache()
                quotes = await run.io_bound(get_snapshot)
            except LiveDataUnavailable as exc:
                ui.notify(str(exc), type="negative")
            except Exception:
                ui.notify("Piyasa verisi şu anda yüklenemedi. Lütfen tekrar deneyin.", type="negative")
            else:
                quote_container.clear()
                with quote_container:
                    with ui.row().classes("items-end justify-between w-full").style("gap: .75rem; flex-wrap: wrap;"):
                        with ui.column().style("gap: .1rem;"):
                            ui.label("Güncel piyasa görünümü").classes("section-title").style("font-size: 1.65rem;")
                            ui.label("Sağlayıcının erişilebilir son günlük kapanışları.").classes("section-copy")
                        ui.label(f"Son sorgu: {datetime.now().strftime('%d.%m.%Y %H:%M')}").classes("data-source")
                    with ui.row().classes("w-full").style("gap: .8rem; flex-wrap: wrap;"):
                        for quote in quotes:
                            quote_card(quote)
                    rows = [
                        {
                            "symbol": quote.instrument.symbol,
                            "company": quote.instrument.name,
                            "price": currency(quote.price),
                            "change": f"{quote.change_percent:+.2f}%",
                            "volume": compact_volume(quote.volume),
                        }
                        for quote in quotes
                    ]
                    ui.table(
                        columns=[
                            {"name": "symbol", "label": "Sembol", "field": "symbol", "align": "left"},
                            {"name": "company", "label": "Şirket", "field": "company", "align": "left"},
                            {"name": "price", "label": "Kapanış", "field": "price", "align": "right"},
                            {"name": "change", "label": "Günlük değişim", "field": "change", "align": "right"},
                            {"name": "volume", "label": "Hacim", "field": "volume", "align": "right"},
                        ],
                        rows=rows,
                        row_key="symbol",
                    ).classes("w-full").props("flat dense")
                    ui.label("Veri kaynağı: Yahoo Finance via yfinance. Değerler gecikmeli olabilir; yatırım tavsiyesi değildir.").classes("data-source")
            finally:
                load_button.enable()
                load_button.props("loading=false")

        async def load_history_chart() -> None:
            history_button.disable()
            history_button.props("loading")
            try:
                bars = await run.io_bound(get_history, symbol_select.value, int(days_select.value))
            except LiveDataUnavailable as exc:
                ui.notify(str(exc), type="negative")
            except Exception:
                ui.notify("Fiyat geçmişi şu anda yüklenemedi. Lütfen tekrar deneyin.", type="negative")
            else:
                chart_container.clear()
                with chart_container:
                    ui.plotly(price_figure(bars, symbol_select.value)).classes("w-full").style("height: 25rem;")
                    ui.label("Grafik, sağlayıcının günlük OHLCV verisindeki kapanış fiyatlarını gösterir.").classes("data-source")
            finally:
                history_button.enable()
                history_button.props("loading=false")

        load_button.on("click", load_snapshot)
        history_button.on("click", load_history_chart)
    footer()


def empty_news_state(container: ui.column) -> None:
    container.clear()
    with container:
        with ui.column().classes("soft-surface w-full items-center").style("padding: 3rem 1.5rem; gap: .7rem;"):
            ui.icon("newspaper").style(f"color: {NAVY}; font-size: 2.4rem;")
            ui.label("Haber araması bekliyor").classes("card-title")
            ui.label("Bir şirket seçip sağlayıcının bağlantılı haberlerini getirin.").classes("section-copy").style("text-align: center;")


@ui.page("/news")
def news_page() -> None:
    apply_theme()
    header("/news")
    analyzer = FinancialSentimentAnalyzer()
    with ui.column().classes("app-shell"):
        page_intro(
            "Haber araştırma alanı",
            "Başlığı değil, kaynağıyla birlikte sinyali okuyun.",
            "Şirket adına göre sağlayıcının haberlerini getirir; başlık ve özet içindeki anahtar kelimelerden şeffaf bir duygu etiketi üretir.",
            ("Bağlantılı kaynaklar", "Açıklanabilir analiz", "Sinyal ≠ öneri"),
        )
        with ui.row().classes("surface w-full items-end").style("padding: 1rem; gap: .75rem; flex-wrap: wrap;"):
            with ui.column().style("gap: .1rem; flex: 1 1 16rem;"):
                ui.label("Şirket haberleri").classes("card-title").style("font-size: 1.2rem;")
                ui.label("Arama yalnızca düğmeye bastığınızda başlar.").classes("metric-note")
            company_select = ui.select({"Apple": "Apple", "Microsoft": "Microsoft", "NVIDIA": "NVIDIA", "Tesla": "Tesla", "Garanti BBVA": "Garanti BBVA"}, value="Apple", label="Şirket").style("min-width: 13rem;")
            search_button = ui.button("Haberleri getir", icon="search").props("no-caps").classes("primary-action")

        news_container = ui.column().classes("w-full").style("gap: .8rem;")
        empty_news_state(news_container)

        async def load_news() -> None:
            search_button.disable()
            search_button.props("loading")
            company = company_select.value
            try:
                articles = await run.io_bound(YahooFinanceService().search_news, company, 10)
            except LiveDataUnavailable as exc:
                ui.notify(str(exc), type="negative")
            except Exception:
                ui.notify("Haberler şu anda yüklenemedi. Lütfen tekrar deneyin.", type="negative")
            else:
                news_container.clear()
                with news_container:
                    with ui.row().classes("items-end justify-between w-full").style("gap: .75rem; flex-wrap: wrap;"):
                        with ui.column().style("gap: .1rem;"):
                            ui.label(f"{company} için haberler").classes("section-title").style("font-size: 1.65rem;")
                            ui.label(f"{len(articles)} kaynak bağlantılı haber bulundu.").classes("section-copy")
                        ui.label("Duygu etiketi, başlık ve özetteki anahtar kelime dengesine dayanır.").classes("data-source")
                    if not articles:
                        ui.label("Sağlayıcı bu arama için erişilebilir haber döndürmedi.").classes("section-copy")
                    for article in articles:
                        result = analyzer.analyze_text(article.text_for_analysis)
                        label, tone = sentiment_label(result.score)
                        with ui.column().classes(f"surface article-card {tone} w-full").style("gap: .55rem;"):
                            with ui.row().classes("items-center w-full").style("gap: .55rem; flex-wrap: wrap;"):
                                ui.label(article.company).classes("tag")
                                ui.label(label).classes(f"sentiment-chip {tone}")
                                ui.space()
                                ui.label(article.published_at.strftime("%d %b %Y, %H:%M UTC")).classes("article-meta")
                            ui.label(article.title).classes("article-title")
                            ui.label(article.summary).classes("card-copy")
                            with ui.row().classes("items-center").style("gap: .55rem;"):
                                ui.label(f"Kaynak: {article.source}").classes("article-meta")
                                if article.url:
                                    ui.link("Kaynağı aç", article.url, new_tab=True).style(f"color: {BROWN}; font-weight: 700; font-size: .82rem;")
                    ui.label("Haber metni, sağlayıcıdan gelen başlık ve özetle sınırlıdır. Bu analiz yatırım önerisi değildir.").classes("data-source")
            finally:
                search_button.enable()
                search_button.props("loading=false")

        search_button.on("click", load_news)
    footer()


@ui.page("/support")
def support_page() -> None:
    apply_theme()
    header("/support")
    with ui.column().classes("app-shell"):
        page_intro(
            "Destek merkezi",
            "Size yardımcı olmamız için doğru bağlamı paylaşın.",
            "Mesajınız gönderilmez veya saklanmaz. Form, tercih ettiğiniz e-posta uygulamasında düzenleyebileceğiniz bir taslak açar.",
            ("E-posta taslağı", "Veri saklanmaz", "Şeffaf iletişim"),
        )
        with ui.row().classes("w-full").style("gap: 1rem; flex-wrap: wrap;"):
            with ui.column().classes("surface").style("padding: 1.5rem; gap: .9rem; flex: 2 1 30rem;"):
                ui.label("Destek talebi oluşturun").classes("section-title").style("font-size: 1.55rem;")
                ui.label("En az 20 karakterlik bir açıklama ekleyin; e-posta taslağınızda tüm alanları değiştirebilirsiniz.").classes("section-copy")
                name = ui.input("Adınız").props("outlined").classes("w-full")
                email = ui.input("E-posta adresiniz").props("outlined type=email").classes("w-full")
                topic = ui.select({"Genel soru": "Genel soru", "Piyasa verisi": "Piyasa verisi", "Haber analizi": "Haber analizi", "Teknik sorun": "Teknik sorun"}, value="Genel soru", label="Konu").props("outlined").classes("w-full")
                message = ui.textarea("Mesajınız").props("outlined autogrow").classes("w-full")

                def open_email_draft() -> None:
                    error = validate_support_request(name.value or "", email.value or "", message.value or "")
                    if error:
                        ui.notify(error, type="warning")
                        return
                    ui.open(build_support_mailto(topic.value or "", name.value, email.value, message.value), new_tab=True)
                    ui.notify("E-posta taslağı açılıyor. Göndermeden önce içeriği gözden geçirin.", type="positive")

                ui.button("E-posta taslağını aç", icon="mail", on_click=open_email_draft).props("no-caps").classes("primary-action")
            with ui.column().classes("soft-surface").style("padding: 1.5rem; gap: 1rem; flex: 1 1 18rem;"):
                ui.label("Hızlı bilgiler").classes("card-title")
                for icon, title, copy in (("database", "Veri kaynağı", "Fiyatlar Yahoo Finance üzerinden erişilebilen son günlük verilerden gelir."), ("visibility", "Duygu yöntemi", "Analiz, görülebilir anahtar kelime setiyle üretilir."), ("lock", "Gizlilik", "Bu formda yazdıklarınız uygulama tarafından saklanmaz.")):
                    with ui.row().classes("items-start").style("gap: .65rem;"):
                        ui.icon(icon).style(f"color: {BROWN}; font-size: 1.2rem; margin-top: .1rem;")
                        with ui.column().style("gap: .08rem;"):
                            ui.label(title).style(f"color: {NAVY}; font-weight: 700;")
                            ui.label(copy).classes("metric-note")
                ui.separator().style("background: rgba(16, 54, 87, .14);")
                ui.label("Alternatif iletişim").style(f"color: {NAVY}; font-weight: 700;")
                ui.link("enesor8@gmail.com", "mailto:enesor8@gmail.com").style(f"color: {BROWN}; font-weight: 700;")
    footer()


def run_app() -> None:
    """Launch the default NiceGUI presentation layer."""
    ui.run(
        title="Financial News Analyzer",
        favicon="📈",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=False,
        show=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    run_app()
