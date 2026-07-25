"""Shared visual system for the Streamlit application."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply the product-wide visual language after page-specific styles."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #f4fff8;
            --muted: #9bbbad;
            --canvas: #06130e;
            --surface: #0c2119;
            --surface-2: #123126;
            --line: rgba(154, 211, 176, .18);
            --brand: #4ade80;
            --brand-2: #15803d;
            --danger: #fb7185;
        }
        #MainMenu, footer { visibility: hidden; }
        [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
        .stApp {
            background:
                radial-gradient(circle at 10% -10%, rgba(74,222,128,.18), transparent 27rem),
                radial-gradient(circle at 88% 0%, rgba(22,163,74,.14), transparent 29rem),
                var(--canvas) !important;
            color: var(--ink) !important;
        }
        .main .block-container {
            max-width: 1440px;
            padding: .35rem 2.25rem 4rem !important;
            margin: 0 auto;
            background: transparent !important;
        }
        [data-testid="stHeader"] { background: rgba(6,19,14,.78); backdrop-filter: blur(16px); }
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #0d251b 0%, #07150f 100%) !important;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebarNav"] { padding-top: .75rem; }
        [data-testid="stSidebarNav"] a {
            border-radius: 10px; margin: 2px 8px; padding: .55rem .75rem;
        }
        [data-testid="stSidebarNav"] a:hover { background: rgba(74,222,128,.12); }
        .app-hero {
            position: relative; overflow: hidden; isolation: isolate;
            padding: clamp(1.4rem, 4vw, 3.1rem); border: 1px solid var(--line);
            border-radius: 24px; margin: .5rem 0 1.75rem;
            background: linear-gradient(118deg, rgba(17,50,36,.96), rgba(9,31,21,.88));
            box-shadow: 0 20px 60px rgba(0,0,0,.24);
        }
        .app-hero::after {
            content: ""; position: absolute; z-index: -1; width: 20rem; height: 20rem;
            top: -11rem; right: -5rem; border-radius: 50%; background: rgba(74,222,128,.16);
            filter: blur(8px);
        }
        .eyebrow { color: var(--brand); font-size: .76rem; font-weight: 800;
            letter-spacing: .13em; text-transform: uppercase; margin-bottom: .7rem; }
        .app-hero h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.45rem); letter-spacing: -.05em; line-height: 1.03; color: var(--ink); }
        .app-hero p { max-width: 48rem; margin: .85rem 0 0; color: var(--muted); font-size: 1.04rem; line-height: 1.55; }
        .hero-badges { display:flex; gap:.55rem; flex-wrap:wrap; margin-top:1.25rem; }
        .hero-badge { border:1px solid rgba(74,222,128,.26); background:rgba(74,222,128,.09); color:#d5ffe3;
            border-radius:999px; padding:.35rem .65rem; font-size:.78rem; font-weight:700; }
        .feature-card, .metric-card, .contact-method, .chart-container {
            background: linear-gradient(145deg, rgba(15,47,33,.9), rgba(8,31,20,.92)) !important;
            border: 1px solid var(--line) !important; border-radius: 16px !important;
            box-shadow: none !important; color: var(--ink) !important;
        }
        .feature-card, .contact-method {
            min-height: 335px; height: calc(100% - 1rem); padding: 1.35rem !important;
            box-sizing: border-box;
        }
        .stApp .feature-card:hover, .stApp .contact-method:hover, .stApp .metric-card:hover,
        .stApp .support-panel:hover, .stApp .news-card:hover, .stApp .chart-container:hover,
        .stApp [data-testid="stMetric"]:hover, .stApp [data-testid="stExpander"]:hover {
            transform: none !important; border-color: rgba(74,222,128,.42) !important;
            box-shadow: none !important; animation: none !important; filter: none !important;
        }
        [data-testid="stMetric"] {
            background: rgba(11,39,26,.84); border: 1px solid var(--line); border-radius: 14px;
            padding: 1.1rem; min-height: 112px;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; }
        [data-testid="stMetricValue"] { color: var(--ink) !important; font-weight: 750; }
        .metric-card {
            min-height: 154px; display: flex; flex-direction: column; justify-content: space-between;
            box-sizing: border-box;
        }
        .summary-card { height: 270px; min-height: 270px; }
        .stApp .stButton > button, .stApp .stButton > button[kind="secondary"], .stApp .stButton > button[kind="primary"], [data-testid="stDownloadButton"] > button {
            border-radius: 10px !important; border: 1px solid rgba(74,222,128,.45) !important;
            background: linear-gradient(135deg, #22c55e, #15803d) !important; color: #f4fff8 !important;
            box-shadow: 0 8px 20px rgba(21,128,61,.24) !important; font-weight: 700 !important;
        }
        .stApp .stButton > button:hover, .stApp .stButton > button[kind="secondary"]:hover,
        .stApp .stButton > button[kind="primary"]:hover, .stApp [data-testid="stDownloadButton"] > button:hover {
            transform: none !important; box-shadow: none !important; filter: brightness(1.04) !important;
        }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div {
            background: rgba(5,24,14,.76) !important; border-color: var(--line) !important;
            border-radius: 10px !important;
        }
        .stApp .stSelectbox > div > div:hover, .stApp .stMultiSelect > div > div:hover,
        .stApp [data-baseweb="input"] > div:hover, .stApp [data-baseweb="select"] > div:hover {
            transform: none !important; box-shadow: none !important;
        }
        [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 12px !important; background: rgba(10,35,23,.7); }
        [data-testid="stForm"] {
            padding: 1.25rem; border: 1px solid var(--line); border-radius: 16px;
            background: linear-gradient(145deg, rgba(15,47,33,.86), rgba(8,31,20,.9));
        }
        [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] { height: 42px; border-radius: 9px 9px 0 0; color: var(--muted); }
        .stTabs [aria-selected="true"] { color: var(--brand) !important; background: rgba(74,222,128,.08); }
        [data-testid="stAlert"] { border-radius: 12px; border: 1px solid var(--line); }
        .live-note { color: var(--muted); font-size: .88rem; margin: .25rem 0 1rem; }
        .news-card {
            min-height: 148px; box-sizing: border-box; padding: 1.15rem 1.25rem; margin: .7rem 0; border-radius: 14px;
            background: linear-gradient(120deg, rgba(16,51,35,.95), rgba(8,31,20,.95));
            border: 1px solid var(--line); border-left: 4px solid var(--brand);
        }
        .news-card.negative { border-left-color: #fb7185; }
        .news-card.neutral { border-left-color: #facc15; }
        .news-card h4 { color: var(--ink) !important; margin: 0 0 .6rem !important; font-size: 1.05rem; line-height: 1.45; }
        .news-meta { color: var(--muted); font-size: .84rem; margin-bottom: .9rem; }
        .news-footer { display:flex; justify-content:space-between; align-items:center; gap:.8rem; flex-wrap:wrap; }
        .sentiment-chip { border-radius:999px; background:rgba(74,222,128,.12); color:#c8ffda; padding:.28rem .6rem; font-size:.78rem; font-weight:700; }
        .sentiment-chip.negative { background:rgba(251,113,133,.13); color:#fecdd3; }
        .sentiment-chip.neutral { background:rgba(250,204,21,.12); color:#fde68a; }
        .article-link { color: #bbf7d0 !important; font-size:.85rem; font-weight:750; text-decoration:none; }
        .article-link:hover { color: #f0fdf4 !important; text-decoration:underline; }
        .support-panel {
            min-height: 312px; box-sizing: border-box;
            background: linear-gradient(145deg, rgba(15,47,33,.92), rgba(8,31,20,.96));
            border:1px solid var(--line); border-radius:16px; padding:1.35rem;
        }
        .support-panel h3, .support-panel h4 { color: var(--ink) !important; margin-top:0; }
        .support-panel p, .support-panel li { color: var(--muted) !important; }
        hr { border-color: var(--line) !important; }
        @media (max-width: 720px) {
            .main .block-container { padding: 1rem 1rem 3rem !important; }
            .app-hero { border-radius: 18px; margin-top: 0; }
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
