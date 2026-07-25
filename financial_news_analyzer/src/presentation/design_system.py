"""Shared visual system for the Streamlit application."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply the product-wide visual language after page-specific styles."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #f7f9fc;
            --muted: #9aa7bd;
            --canvas: #0b1020;
            --surface: #121a2e;
            --surface-2: #18233b;
            --line: rgba(168, 188, 224, .16);
            --brand: #5eead4;
            --brand-2: #818cf8;
            --danger: #fb7185;
        }
        #MainMenu, footer { visibility: hidden; }
        .stApp {
            background:
                radial-gradient(circle at 10% -10%, rgba(94,234,212,.13), transparent 27rem),
                radial-gradient(circle at 88% 0%, rgba(129,140,248,.14), transparent 29rem),
                var(--canvas) !important;
            color: var(--ink) !important;
        }
        .main .block-container {
            max-width: 1440px;
            padding: 1.5rem 2.25rem 4rem !important;
            margin: 0 auto;
            background: transparent !important;
        }
        [data-testid="stHeader"] { background: rgba(11,16,32,.72); backdrop-filter: blur(16px); }
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #10182c 0%, #0c1223 100%) !important;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebarNav"] { padding-top: .75rem; }
        [data-testid="stSidebarNav"] a {
            border-radius: 10px; margin: 2px 8px; padding: .55rem .75rem;
        }
        [data-testid="stSidebarNav"] a:hover { background: rgba(129,140,248,.12); }
        .app-hero {
            position: relative; overflow: hidden; isolation: isolate;
            padding: clamp(1.4rem, 4vw, 3.1rem); border: 1px solid var(--line);
            border-radius: 24px; margin: .5rem 0 1.75rem;
            background: linear-gradient(118deg, rgba(24,35,59,.96), rgba(16,24,44,.84));
            box-shadow: 0 20px 60px rgba(0,0,0,.24);
        }
        .app-hero::after {
            content: ""; position: absolute; z-index: -1; width: 20rem; height: 20rem;
            top: -11rem; right: -5rem; border-radius: 50%; background: rgba(94,234,212,.13);
            filter: blur(8px);
        }
        .eyebrow { color: var(--brand); font-size: .76rem; font-weight: 800;
            letter-spacing: .13em; text-transform: uppercase; margin-bottom: .7rem; }
        .app-hero h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.45rem); letter-spacing: -.05em; line-height: 1.03; color: var(--ink); }
        .app-hero p { max-width: 48rem; margin: .85rem 0 0; color: var(--muted); font-size: 1.04rem; line-height: 1.55; }
        .hero-badges { display:flex; gap:.55rem; flex-wrap:wrap; margin-top:1.25rem; }
        .hero-badge { border:1px solid rgba(94,234,212,.22); background:rgba(94,234,212,.08); color:#cbfbf2;
            border-radius:999px; padding:.35rem .65rem; font-size:.78rem; font-weight:700; }
        .feature-card, .metric-card, .contact-method, .chart-container {
            background: linear-gradient(145deg, rgba(24,35,59,.9), rgba(15,23,42,.9)) !important;
            border: 1px solid var(--line) !important; border-radius: 16px !important;
            box-shadow: none !important; color: var(--ink) !important;
        }
        .feature-card, .contact-method { height: calc(100% - 1rem); padding: 1.35rem !important; }
        .feature-card:hover, .contact-method:hover, .metric-card:hover {
            transform: translateY(-3px) !important; border-color: rgba(94,234,212,.38) !important;
            box-shadow: 0 16px 35px rgba(0,0,0,.18) !important; animation: none !important;
        }
        [data-testid="stMetric"] {
            background: rgba(18,26,46,.84); border: 1px solid var(--line); border-radius: 14px;
            padding: 1.1rem; min-height: 112px;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; }
        [data-testid="stMetricValue"] { color: var(--ink) !important; font-weight: 750; }
        .stButton > button, [data-testid="stDownloadButton"] > button {
            border-radius: 10px !important; border: 1px solid rgba(129,140,248,.45) !important;
            background: linear-gradient(135deg, #6366f1, #4f46e5) !important; color: white !important;
            box-shadow: 0 8px 20px rgba(79,70,229,.2) !important; font-weight: 700 !important;
        }
        .stButton > button:hover, [data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-1px) !important; filter: brightness(1.08);
        }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div {
            background: rgba(11,16,32,.7) !important; border-color: var(--line) !important;
            border-radius: 10px !important;
        }
        [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 12px !important; background: rgba(18,26,46,.56); }
        [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] { height: 42px; border-radius: 9px 9px 0 0; color: var(--muted); }
        .stTabs [aria-selected="true"] { color: var(--brand) !important; background: rgba(94,234,212,.08); }
        [data-testid="stAlert"] { border-radius: 12px; border: 1px solid var(--line); }
        hr { border-color: var(--line) !important; }
        @media (max-width: 720px) {
            .main .block-container { padding: 1rem 1rem 3rem !important; }
            .app-hero { border-radius: 18px; margin-top: 0; }
            [data-testid="stMetric"] { min-height: 96px; padding: .8rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str, *, eyebrow: str, badges: list[str] | None = None) -> None:
    """Render a concise and responsive product header."""
    badge_html = "".join(f'<span class="hero-badge">{escape(badge)}</span>' for badge in badges or [])
    st.markdown(
        f'<section class="app-hero"><div class="eyebrow">{escape(eyebrow)}</div>'
        f'<h1>{escape(title)}</h1><p>{escape(description)}</p>'
        f'<div class="hero-badges">{badge_html}</div></section>',
        unsafe_allow_html=True,
    )
