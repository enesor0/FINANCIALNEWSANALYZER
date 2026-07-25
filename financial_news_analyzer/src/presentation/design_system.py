"""Shared visual system for the Streamlit application."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply a calm, consistent visual language after page-specific styles."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #edf1f8;
            --muted: #aab5c7;
            --canvas: #111827;
            --surface: #182235;
            --surface-2: #202c42;
            --surface-3: #293750;
            --line: rgba(171, 187, 215, .18);
            --brand: #8da7ff;
            --brand-strong: #6686ec;
            --brand-soft: rgba(141, 167, 255, .12);
            --success: #5fb59a;
            --danger: #f28b9a;
            --warning: #e9bf6d;
        }

        #MainMenu, footer { visibility: hidden; }
        [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
        .stApp {
            background:
                radial-gradient(circle at 0% 0%, rgba(100, 132, 210, .16), transparent 30rem),
                radial-gradient(circle at 100% 8%, rgba(127, 103, 177, .11), transparent 27rem),
                var(--canvas) !important;
            color: var(--ink) !important;
        }
        .main .block-container {
            max-width: 1440px;
            padding: .55rem 2.25rem 4rem !important;
            margin: 0 auto;
            background: transparent !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: #161f30 !important;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebarNav"] { padding-top: .75rem; }
        [data-testid="stSidebarNav"] a {
            border-radius: 10px; margin: 2px 8px; padding: .55rem .75rem;
        }
        [data-testid="stSidebarNav"] a:hover { background: var(--brand-soft); }

        .app-hero {
            position: relative; overflow: hidden; isolation: isolate;
            padding: clamp(1.5rem, 4vw, 3.15rem); border: 1px solid var(--line);
            border-radius: 20px; margin: .75rem 0 1.5rem;
            background: linear-gradient(120deg, rgba(31, 43, 65, .98), rgba(23, 32, 49, .98));
            box-shadow: 0 18px 45px rgba(3, 8, 20, .18);
        }
        .app-hero::after {
            content: ""; position: absolute; z-index: -1; width: 23rem; height: 23rem;
            top: -14rem; right: -7rem; border-radius: 50%; background: rgba(120, 143, 221, .15);
            filter: blur(18px);
        }
        .eyebrow { color: var(--brand); font-size: .73rem; font-weight: 800;
            letter-spacing: .14em; text-transform: uppercase; margin-bottom: .7rem; }
        .app-hero h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.35rem); letter-spacing: -.045em; line-height: 1.08; color: var(--ink); }
        .app-hero p { max-width: 48rem; margin: .85rem 0 0; color: var(--muted); font-size: 1.02rem; line-height: 1.6; }
        .hero-badges { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1.25rem; }
        .hero-badge { border: 1px solid rgba(141, 167, 255, .27); background: var(--brand-soft); color: #dbe4ff;
            border-radius: 999px; padding: .34rem .64rem; font-size: .76rem; font-weight: 700; }

        h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 { color: var(--ink) !important; }
        p, li, [data-testid="stCaptionContainer"] { color: var(--muted); }

        .feature-card, .metric-card, .contact-method, .chart-container, .contact-card, .info-card {
            background: rgba(25, 35, 54, .88) !important;
            border: 1px solid var(--line) !important; border-radius: 14px !important;
            box-shadow: 0 8px 24px rgba(3, 8, 20, .1) !important; color: var(--ink) !important;
        }
        .feature-card, .contact-method {
            min-height: 300px; height: calc(100% - 1rem); padding: 1.35rem !important;
            box-sizing: border-box;
        }
        .metric-card {
            min-height: 150px; display: flex; flex-direction: column; justify-content: space-between;
            box-sizing: border-box;
        }
        .summary-card { height: 250px; min-height: 250px; }
        .stApp .feature-card:hover, .stApp .contact-method:hover, .stApp .metric-card:hover,
        .stApp .support-panel:hover, .stApp .news-card:hover, .stApp .chart-container:hover,
        .stApp [data-testid="stMetric"]:hover, .stApp [data-testid="stExpander"]:hover {
            transform: none !important; border-color: rgba(141, 167, 255, .42) !important;
            box-shadow: 0 8px 24px rgba(3, 8, 20, .1) !important; animation: none !important; filter: none !important;
        }
        [data-testid="stMetric"] {
            background: rgba(25, 35, 54, .84); border: 1px solid var(--line); border-radius: 14px;
            padding: 1.05rem; min-height: 108px;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; }
        [data-testid="stMetricValue"] { color: var(--ink) !important; font-weight: 750; }
        [data-testid="stMetricDelta"] { color: var(--success) !important; }

        .stApp .stButton > button, .stApp .stButton > button[kind="secondary"],
        .stApp .stButton > button[kind="primary"], [data-testid="stDownloadButton"] > button {
            border-radius: 9px !important; border: 1px solid rgba(141, 167, 255, .46) !important;
            background: #536fcb !important; color: #f7f9ff !important;
            box-shadow: none !important; font-weight: 700 !important;
        }
        .stApp .stButton > button:hover, .stApp .stButton > button[kind="secondary"]:hover,
        .stApp .stButton > button[kind="primary"]:hover, .stApp [data-testid="stDownloadButton"] > button:hover {
            transform: none !important; background: #6686ec !important; box-shadow: none !important; filter: none !important;
        }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div {
            background: rgba(15, 23, 38, .86) !important; border-color: var(--line) !important;
            border-radius: 9px !important;
        }
        .stApp .stSelectbox > div > div, .stApp .stMultiSelect > div > div { min-width: 0 !important; }
        .stApp .stSelectbox > div > div:hover, .stApp .stMultiSelect > div > div:hover,
        .stApp [data-baseweb="input"] > div:hover, .stApp [data-baseweb="select"] > div:hover {
            transform: none !important; box-shadow: none !important;
        }
        [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 12px !important; background: rgba(25, 35, 54, .72); }
        [data-testid="stForm"] {
            padding: 1.25rem; border: 1px solid var(--line); border-radius: 14px;
            background: rgba(25, 35, 54, .86);
        }
        [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] { height: 42px; border-radius: 9px 9px 0 0; color: var(--muted); }
        .stTabs [aria-selected="true"] { color: var(--brand) !important; background: var(--brand-soft); }
        [data-testid="stAlert"] { border-radius: 12px; border: 1px solid var(--line); }
        .live-note { color: var(--muted); font-size: .88rem; margin: .25rem 0 1rem; }
        .news-card {
            min-height: 148px; box-sizing: border-box; padding: 1.15rem 1.25rem; margin: .7rem 0; border-radius: 14px;
            background: rgba(25, 35, 54, .92); border: 1px solid var(--line); border-left: 4px solid var(--brand);
        }
        .news-card.negative { border-left-color: var(--danger); }
        .news-card.neutral { border-left-color: var(--warning); }
        .news-card h4 { color: var(--ink) !important; margin: 0 0 .6rem !important; font-size: 1.05rem; line-height: 1.45; }
        .news-meta { color: var(--muted); font-size: .84rem; margin-bottom: .9rem; }
        .news-footer { display: flex; justify-content: space-between; align-items: center; gap: .8rem; flex-wrap: wrap; }
        .sentiment-chip { border-radius: 999px; background: rgba(95, 181, 154, .13); color: #b9e5d5; padding: .28rem .6rem; font-size: .78rem; font-weight: 700; }
        .sentiment-chip.negative { background: rgba(242, 139, 154, .13); color: #ffc5cd; }
        .sentiment-chip.neutral { background: rgba(233, 191, 109, .12); color: #f6d899; }
        .article-link { color: #b9c9ff !important; font-size: .85rem; font-weight: 750; text-decoration: none; }
        .article-link:hover { color: #edf1ff !important; text-decoration: underline; }
        .support-panel {
            min-height: 300px; box-sizing: border-box; background: rgba(25, 35, 54, .9);
            border: 1px solid var(--line); border-radius: 14px; padding: 1.35rem;
        }
        .support-panel h3, .support-panel h4 { color: var(--ink) !important; margin-top: 0; }
        .support-panel p, .support-panel li { color: var(--muted) !important; }
        [style*="#00D4AA"] { color: var(--brand) !important; }
        .status-healthy, .status-active { background: rgba(95, 181, 154, .14) !important; color: #c3e6d8 !important; }
        .status-warning { background: rgba(233, 191, 109, .14) !important; color: #f6d899 !important; }
        .status-error { background: rgba(242, 139, 154, .14) !important; color: #ffc5cd !important; }
        hr { border-color: var(--line) !important; }
        @media (max-width: 720px) {
            .main .block-container { padding: .5rem 1rem 3rem !important; }
            .app-hero { border-radius: 16px; margin-top: .25rem; }
            [data-testid="stMetric"] { min-height: 96px; padding: .8rem; }
            .feature-card, .contact-method, .metric-card, .summary-card, .news-card, .support-panel { height: auto; min-height: 0; }
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
