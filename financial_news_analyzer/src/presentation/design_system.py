"""Shared jade-and-pebble visual system for the Streamlit workspaces."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply the supplied jade palette consistently across every workspace."""
    st.markdown(
        """
        <style>
        :root {
            --jade: #7B9669;
            --pebble: #E6E6E6;
            --forest: #404E3B;
            --slate: #6C8480;
            --sage: #BAC8B1;
            --ink: var(--forest);
            --muted: var(--slate);
            --canvas: var(--pebble);
            --surface: rgba(255, 255, 255, .54);
            --line: rgba(64, 78, 59, .16);
            --brand: var(--jade);
            --brand-soft: rgba(123, 150, 105, .15);
            --success: var(--jade);
            --danger: var(--forest);
            --warning: var(--slate);
        }

        #MainMenu, footer { visibility: hidden; }
        [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
        .stApp {
            background:
                radial-gradient(circle at 5% 0%, rgba(186, 200, 177, .9), transparent 29rem),
                radial-gradient(circle at 98% 8%, rgba(123, 150, 105, .23), transparent 24rem),
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
            background: linear-gradient(180deg, var(--pebble), var(--sage)) !important;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label { color: var(--forest) !important; }

        .app-hero {
            position: relative; overflow: hidden; isolation: isolate;
            padding: clamp(1.6rem, 4vw, 3.2rem); border: 1px solid var(--line);
            border-radius: 24px; margin: .75rem 0 1.5rem;
            background: linear-gradient(120deg, rgba(255, 255, 255, .77), rgba(186, 200, 177, .74));
            box-shadow: 0 18px 45px rgba(64, 78, 59, .1), inset 0 1px rgba(255, 255, 255, .78);
        }
        .app-hero::before {
            content: ""; position: absolute; z-index: -1; width: 24rem; height: 24rem;
            top: -15rem; right: -8rem; border-radius: 50%; background: rgba(123, 150, 105, .22);
        }
        .eyebrow { color: var(--jade); font-size: .72rem; font-weight: 850;
            letter-spacing: .14em; text-transform: uppercase; margin-bottom: .7rem; }
        .app-hero h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.35rem); letter-spacing: -.055em; line-height: 1.05; color: var(--forest); }
        .app-hero p { max-width: 48rem; margin: .85rem 0 0; color: var(--slate); font-size: 1.02rem; line-height: 1.6; }
        .hero-badges { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1.25rem; }
        .hero-badge { border: 1px solid rgba(123, 150, 105, .3); background: rgba(255, 255, 255, .5); color: var(--forest);
            border-radius: 999px; padding: .35rem .66rem; font-size: .75rem; font-weight: 750; }

        h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 { color: var(--forest) !important; }
        p, li, [data-testid="stCaptionContainer"] { color: var(--slate); }
        a { color: var(--forest) !important; }

        .feature-card, .metric-card, .contact-method, .chart-container, .contact-card, .info-card,
        .support-panel, .news-card {
            background: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: 16px !important;
            box-shadow: 0 9px 22px rgba(64, 78, 59, .07), inset 0 1px rgba(255, 255, 255, .72) !important;
            color: var(--ink) !important;
        }
        .feature-card, .contact-method { min-height: 260px; height: calc(100% - 1rem); padding: 1.35rem !important; box-sizing: border-box; }
        .metric-card { min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; }
        .summary-card { height: 250px; min-height: 250px; }
        .stApp .feature-card:hover, .stApp .contact-method:hover, .stApp .metric-card:hover,
        .stApp .support-panel:hover, .stApp .news-card:hover, .stApp .chart-container:hover,
        .stApp [data-testid="stMetric"]:hover, .stApp [data-testid="stExpander"]:hover {
            transform: translateY(-2px) !important; border-color: rgba(123, 150, 105, .56) !important;
            box-shadow: 0 13px 26px rgba(64, 78, 59, .1) !important; animation: none !important; filter: none !important;
        }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, .56); border: 1px solid var(--line); border-radius: 16px;
            padding: 1.05rem; min-height: 108px; box-shadow: inset 0 1px rgba(255, 255, 255, .7);
        }
        [data-testid="stMetricLabel"] { color: var(--slate) !important; }
        [data-testid="stMetricValue"] { color: var(--forest) !important; font-weight: 800; }
        [data-testid="stMetricDelta"] { color: var(--jade) !important; }

        .stApp .stButton > button, .stApp .stButton > button[kind="secondary"],
        .stApp .stButton > button[kind="primary"], [data-testid="stDownloadButton"] > button {
            border: 1px solid var(--forest) !important; border-radius: 10px !important;
            background: var(--forest) !important; color: var(--pebble) !important;
            box-shadow: 0 4px 8px rgba(64, 78, 59, .1) !important; font-weight: 750 !important;
        }
        .stApp .stButton > button:hover, .stApp .stButton > button[kind="secondary"]:hover,
        .stApp .stButton > button[kind="primary"]:hover, .stApp [data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-1px) !important; border-color: var(--jade) !important;
            background: var(--jade) !important; box-shadow: 0 8px 15px rgba(64, 78, 59, .14) !important; filter: none !important;
        }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, .66) !important; border-color: var(--line) !important; border-radius: 10px !important;
        }
        [data-baseweb="input"] input, [data-baseweb="select"] * { color: var(--forest) !important; }
        .stApp .stSelectbox > div > div, .stApp .stMultiSelect > div > div { min-width: 0 !important; }
        .stApp .stSelectbox > div > div:hover, .stApp .stMultiSelect > div > div:hover,
        .stApp [data-baseweb="input"] > div:hover, .stApp [data-baseweb="select"] > div:hover {
            transform: none !important; border-color: var(--jade) !important; box-shadow: none !important;
        }
        [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 13px !important; background: rgba(255, 255, 255, .43); }
        [data-testid="stForm"] { padding: 1.25rem; border: 1px solid var(--line); border-radius: 16px; background: rgba(255, 255, 255, .45); }
        [data-testid="stDataFrame"], [data-testid="stTable"], .stPlotlyChart { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] { height: 42px; border-radius: 10px 10px 0 0; color: var(--slate); }
        .stTabs [aria-selected="true"] { color: var(--forest) !important; background: rgba(186, 200, 177, .52); }
        [data-testid="stAlert"] { border-radius: 13px; border: 1px solid var(--line); }

        .live-note { color: var(--slate); font-size: .88rem; margin: .25rem 0 1rem; }
        .news-card { min-height: 148px; box-sizing: border-box; padding: 1.15rem 1.25rem; margin: .7rem 0; border-left: 4px solid var(--jade) !important; }
        .news-card.negative { border-left-color: var(--forest) !important; }
        .news-card.neutral { border-left-color: var(--slate) !important; }
        .news-card h4 { color: var(--forest) !important; margin: 0 0 .6rem !important; font-size: 1.05rem; line-height: 1.45; }
        .news-meta { color: var(--slate); font-size: .84rem; margin-bottom: .9rem; }
        .news-footer { display: flex; justify-content: space-between; align-items: center; gap: .8rem; flex-wrap: wrap; }
        .sentiment-chip { border-radius: 999px; background: rgba(123, 150, 105, .16); color: var(--forest); padding: .28rem .6rem; font-size: .78rem; font-weight: 750; }
        .sentiment-chip.negative { background: rgba(64, 78, 59, .12); color: var(--forest); }
        .sentiment-chip.neutral { background: rgba(108, 132, 128, .14); color: var(--forest); }
        .article-link { color: var(--forest) !important; font-size: .85rem; font-weight: 800; text-decoration: none; }
        .article-link:hover { color: var(--jade) !important; text-decoration: underline; }
        .support-panel { min-height: 300px; box-sizing: border-box; padding: 1.35rem; }
        .support-panel h3, .support-panel h4 { color: var(--forest) !important; margin-top: 0; }
        .support-panel p, .support-panel li { color: var(--slate) !important; }
        .status-healthy, .status-active { background: rgba(123, 150, 105, .14) !important; color: var(--forest) !important; }
        .status-warning { background: rgba(108, 132, 128, .14) !important; color: var(--forest) !important; }
        .status-error { background: rgba(64, 78, 59, .12) !important; color: var(--forest) !important; }
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
        f'<h1>{escape(title)}</h1><p>{escape(description)}</p>'
        f'<div class="hero-badges">{badge_html}</div></section>',
        unsafe_allow_html=True,
    )
