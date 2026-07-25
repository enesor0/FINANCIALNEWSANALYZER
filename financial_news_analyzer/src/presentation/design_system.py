"""Shared visual system for the native Streamlit workspaces."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply the calm navy, cream, sage, and brown product palette."""
    st.markdown(
        """
        <style>
        :root {
            --navy: #103657;
            --navy-deep: #0B2B47;
            --cream: #F4E4C4;
            --cream-light: #FBF4E6;
            --sage: #CFD0BD;
            --sage-dark: #AEB2A0;
            --brown: #94613C;
            --brown-dark: #754727;
            --ink: #19324A;
            --muted: #617083;
            --line: rgba(16, 54, 87, .14);
            --positive: #4E8067;
            --negative: #B2564B;
            --warning: #A87A36;
        }

        #MainMenu, footer { visibility: hidden; }
        [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
        .stApp {
            background:
                radial-gradient(circle at 5% 0%, rgba(244, 228, 196, .95), transparent 32rem),
                radial-gradient(circle at 100% 12%, rgba(207, 208, 189, .7), transparent 28rem),
                var(--cream-light) !important;
            color: var(--ink) !important;
        }
        .main .block-container {
            max-width: 1180px;
            padding: .55rem 2.25rem 4rem !important;
            margin: 0 auto;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: var(--cream) !important;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] * { color: var(--ink) !important; }

        .app-hero {
            position: relative; overflow: hidden; isolation: isolate;
            padding: clamp(1.8rem, 5vw, 4rem); border-radius: 22px; margin: .75rem 0 1.5rem;
            background: var(--navy); color: var(--cream-light);
            box-shadow: 0 18px 44px rgba(16, 54, 87, .18);
        }
        .app-hero::after {
            content: ""; position: absolute; z-index: -1; width: 23rem; height: 23rem;
            top: -14rem; right: -8rem; border-radius: 50%; background: rgba(207, 208, 189, .18);
        }
        .eyebrow { color: var(--cream); font-size: .72rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .7rem; }
        .hero-title { margin: 0; color: var(--cream-light) !important; font-family: Georgia, serif; font-size: clamp(2rem, 4vw, 3.45rem); font-weight: 700; letter-spacing: -.05em; line-height: 1.06; }
        .app-hero p { max-width: 48rem; margin: .85rem 0 0; color: rgba(251, 244, 230, .8); font-size: 1.03rem; line-height: 1.6; }
        .hero-badges { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1.3rem; }
        .hero-badge { border: 1px solid rgba(244, 228, 196, .2); background: rgba(244, 228, 196, .13); color: var(--cream-light); border-radius: 999px; padding: .34rem .66rem; font-size: .76rem; font-weight: 700; }

        h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 { color: var(--navy) !important; }
        h2, h3 { font-family: Georgia, serif; letter-spacing: -.025em; }
        p, li, [data-testid="stCaptionContainer"] { color: var(--muted); }
        a, .article-link { color: var(--brown) !important; font-weight: 750; }

        .feature-card, .metric-card, .contact-method, .chart-container, .contact-card, .info-card,
        .support-panel, .news-card {
            background: rgba(255, 250, 240, .9) !important;
            border: 1px solid var(--line) !important; border-radius: 16px !important;
            box-shadow: 0 8px 24px rgba(16, 54, 87, .07) !important; color: var(--ink) !important;
        }
        .feature-card, .contact-method { min-height: 260px; height: calc(100% - 1rem); padding: 1.35rem !important; box-sizing: border-box; }
        .metric-card { min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; }
        .summary-card { height: 250px; min-height: 250px; }
        .stApp .feature-card:hover, .stApp .contact-method:hover, .stApp .metric-card:hover,
        .stApp .support-panel:hover, .stApp .news-card:hover, .stApp .chart-container:hover,
        .stApp [data-testid="stMetric"]:hover, .stApp [data-testid="stExpander"]:hover {
            transform: translateY(-2px) !important; border-color: rgba(148, 97, 60, .42) !important;
            box-shadow: 0 13px 26px rgba(16, 54, 87, .1) !important; animation: none !important; filter: none !important;
        }
        [data-testid="stMetric"] {
            background: rgba(207, 208, 189, .5); border: 1px solid var(--line); border-radius: 16px;
            padding: 1.05rem; min-height: 108px;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; }
        [data-testid="stMetricValue"] { color: var(--navy) !important; font-family: Georgia, serif; font-weight: 700; }
        [data-testid="stMetricDelta"] { color: var(--positive) !important; }

        .stApp .stButton > button, .stApp .stButton > button[kind="secondary"],
        .stApp .stButton > button[kind="primary"], [data-testid="stDownloadButton"] > button {
            border: 1px solid var(--brown) !important; border-radius: 10px !important;
            background: var(--brown) !important; color: var(--cream-light) !important;
            box-shadow: none !important; font-weight: 750 !important;
        }
        .stApp .stButton > button:hover, .stApp .stButton > button[kind="secondary"]:hover,
        .stApp .stButton > button[kind="primary"]:hover, .stApp [data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-1px) !important; background: var(--brown-dark) !important; box-shadow: 0 7px 15px rgba(117, 71, 39, .18) !important; filter: none !important;
        }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div {
            background: rgba(255, 250, 240, .94) !important; border-color: var(--line) !important; border-radius: 10px !important;
        }
        [data-baseweb="input"] input, [data-baseweb="select"] * { color: var(--ink) !important; }
        .stApp .stSelectbox > div > div, .stApp .stMultiSelect > div > div { min-width: 0 !important; }
        [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 13px !important; background: rgba(255, 250, 240, .75); }
        [data-testid="stForm"] { padding: 1.25rem; border: 1px solid var(--line); border-radius: 16px; background: rgba(255, 250, 240, .8); }
        [data-testid="stDataFrame"], [data-testid="stTable"], .stPlotlyChart { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] { height: 42px; border-radius: 10px 10px 0 0; color: var(--muted); }
        .stTabs [aria-selected="true"] { color: var(--navy) !important; background: rgba(207, 208, 189, .6); }
        [data-testid="stAlert"] { border-radius: 13px; border: 1px solid var(--line); }

        .live-note { color: var(--muted); font-size: .88rem; margin: .25rem 0 1rem; }
        .news-card { min-height: 148px; box-sizing: border-box; padding: 1.15rem 1.25rem; margin: .7rem 0; border-left: 4px solid var(--brown) !important; }
        .news-card.negative { border-left-color: var(--negative) !important; }
        .news-card.neutral { border-left-color: var(--sage-dark) !important; }
        .news-card h4 { color: var(--navy) !important; margin: 0 0 .6rem !important; font-size: 1.05rem; line-height: 1.45; }
        .news-meta { color: var(--muted); font-size: .84rem; margin-bottom: .9rem; }
        .news-footer { display: flex; justify-content: space-between; align-items: center; gap: .8rem; flex-wrap: wrap; }
        .sentiment-chip { border-radius: 999px; background: rgba(78, 128, 103, .12); color: var(--positive); padding: .28rem .6rem; font-size: .78rem; font-weight: 750; }
        .sentiment-chip.negative { background: rgba(178, 86, 75, .12); color: var(--negative); }
        .sentiment-chip.neutral { background: rgba(207, 208, 189, .7); color: var(--muted); }
        .support-panel { min-height: 300px; box-sizing: border-box; padding: 1.35rem; }
        .support-panel h3, .support-panel h4 { color: var(--navy) !important; margin-top: 0; }
        .support-panel p, .support-panel li { color: var(--muted) !important; }
        .status-healthy, .status-active { background: rgba(78, 128, 103, .12) !important; color: var(--positive) !important; }
        .status-warning { background: rgba(168, 122, 54, .13) !important; color: var(--warning) !important; }
        .status-error { background: rgba(178, 86, 75, .12) !important; color: var(--negative) !important; }
        hr { border-color: var(--line) !important; }
        @media (max-width: 720px) {
            .main .block-container { padding: .5rem 1rem 3rem !important; }
            .app-hero { border-radius: 18px; margin-top: .25rem; }
            [data-testid="stMetric"] { min-height: 96px; padding: .8rem; }
            .feature-card, .contact-method, .metric-card, .summary-card, .news-card, .support-panel { height: auto; min-height: 0; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str, *, eyebrow: str, badges: list[str] | None = None) -> None:
    """Render a concise product header in the shared visual system."""
    badge_html = "".join(f'<span class="hero-badge">{escape(badge)}</span>' for badge in badges or [])
    st.markdown(
        f'<section class="app-hero"><div class="eyebrow">{escape(eyebrow)}</div>'
        f'<div class="hero-title" role="heading" aria-level="1">{escape(title)}</div><p>{escape(description)}</p>'
        f'<div class="hero-badges">{badge_html}</div></section>',
        unsafe_allow_html=True,
    )
